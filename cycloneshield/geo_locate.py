"""
CycloneShield - Geo-location for field damage photos.

Gemini judges damage type and severity ONLY. Location always comes from here,
from one of these sources (in priority order):

    1. "gps"        - EXIF GPS tags embedded in the uploaded photo
    2. "device"     - browser/device location captured at upload time
    3. "manual"     - district chosen by the operator (dropdown or map click)
    4. "unverified" - nothing available; district stays None

Coordinates are mapped to a district with a point-in-polygon test against
data/coastal_districts.geojson (WGS84 lon/lat). No nearest-district guessing.
"""

import io
import os
from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Optional, Tuple

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DISTRICTS_PATH = os.path.join(BASE_DIR, "data", "coastal_districts.geojson")

SOURCE_GPS = "gps"
SOURCE_DEVICE = "device"
SOURCE_MANUAL = "manual"
SOURCE_UNVERIFIED = "unverified"

OUTSIDE_COVERAGE = "outside coverage area"

_GPS_IFD_TAG = 0x8825

try:
    import streamlit as st
    _cache_resource = st.cache_resource
except Exception:  # pragma: no cover - streamlit is optional for tests/CLI
    from functools import lru_cache

    def _cache_resource(func):  # type: ignore[no-redef]
        return lru_cache(maxsize=None)(func)


@dataclass
class LocationResult:
    """Resolved location of an incident photo."""

    location_source: str = SOURCE_UNVERIFIED
    lat: Optional[float] = None
    lon: Optional[float] = None
    district: Optional[str] = None
    state: Optional[str] = None
    district_id: Optional[str] = None
    # True when the point lies in more than one (overlapping) polygon.
    ambiguous: bool = False
    candidates: List[str] = field(default_factory=list)

    @property
    def is_verified(self) -> bool:
        """True when a district was resolved from a real source."""
        return self.location_source != SOURCE_UNVERIFIED and self.district is not None

    @property
    def outside_coverage(self) -> bool:
        """True when coordinates exist but fall outside every district polygon."""
        return self.district == OUTSIDE_COVERAGE

    def to_dict(self) -> Dict[str, Any]:
        """JSON-serializable view of the result."""
        return asdict(self)


# ------------------------------------------------------------------------------
# District polygons
# ------------------------------------------------------------------------------

@_cache_resource
def load_districts():
    """Load coastal district polygons once as a GeoDataFrame in EPSG:4326."""
    import geopandas as gpd

    gdf = gpd.read_file(DISTRICTS_PATH)
    # The file declares no CRS; its coordinates are WGS84 lon/lat.
    gdf = gdf.set_crs("EPSG:4326") if gdf.crs is None else gdf.to_crs("EPSG:4326")
    # Planar degree area is fine here: only used to rank overlapping polygons.
    gdf["_area"] = [geom.area for geom in gdf.geometry]
    return gdf


def list_districts() -> List[Dict[str, str]]:
    """Return district_id / district / state for every polygon, sorted by state then name."""
    gdf = load_districts()
    rows = [
        {
            "district_id": str(r["district_id"]),
            "district": str(r["district_name"]),
            "state": str(r["state_or_division"]),
        }
        for _, r in gdf.iterrows()
    ]
    return sorted(rows, key=lambda r: (r["state"], r["district"]))


def lookup_district(lat: float, lon: float, gdf=None) -> Dict[str, Any]:
    """
    Point-in-polygon lookup. Returns district, state, district_id, ambiguous,
    candidates. Outside every polygon -> district == "outside coverage area".

    The bundled polygons overlap, so a point can fall in several. The smallest
    containing polygon wins and ``ambiguous`` is set so the UI can flag it.
    """
    from shapely.geometry import Point

    gdf = load_districts() if gdf is None else gdf
    point = Point(float(lon), float(lat))
    hits = gdf.iloc[list(gdf.sindex.query(point, predicate="intersects"))]
    if hits.empty:
        return {
            "district": OUTSIDE_COVERAGE,
            "state": None,
            "district_id": None,
            "ambiguous": False,
            "candidates": [],
        }
    hits = hits.sort_values("_area")
    best = hits.iloc[0]
    return {
        "district": str(best["district_name"]),
        "state": str(best["state_or_division"]),
        "district_id": str(best["district_id"]),
        "ambiguous": len(hits) > 1,
        "candidates": [str(n) for n in hits["district_name"]],
    }


# ------------------------------------------------------------------------------
# Location sources
# ------------------------------------------------------------------------------

def _dms_to_degrees(dms: Any, ref: Any) -> float:
    """Convert an EXIF (deg, min, sec) triple plus N/S/E/W reference to signed degrees."""
    deg, minutes, seconds = (float(x) for x in dms)
    value = deg + minutes / 60.0 + seconds / 3600.0
    if str(ref).strip().upper() in ("S", "W"):
        value = -value
    return value


def extract_exif_gps(image_bytes: bytes) -> Optional[Tuple[float, float]]:
    """
    Read GPS coordinates from a photo's EXIF data (Pillow).
    Returns (lat, lon) or None when missing, malformed, out of range or (0, 0).
    """
    try:
        from PIL import Image

        with Image.open(io.BytesIO(image_bytes)) as img:
            gps = img.getexif().get_ifd(_GPS_IFD_TAG)
        if not gps or 2 not in gps or 4 not in gps:
            return None
        lat = _dms_to_degrees(gps[2], gps.get(1, "N"))
        lon = _dms_to_degrees(gps[4], gps.get(3, "E"))
    except Exception:
        return None
    if not (-90 <= lat <= 90 and -180 <= lon <= 180) or (lat == 0 and lon == 0):
        return None
    return lat, lon


def _from_point(lat: float, lon: float, source: str) -> LocationResult:
    """Build a LocationResult from coordinates via district lookup."""
    info = lookup_district(lat, lon)
    return LocationResult(
        location_source=source,
        lat=round(float(lat), 6),
        lon=round(float(lon), 6),
        district=info["district"],
        state=info["state"],
        district_id=info["district_id"],
        ambiguous=info["ambiguous"],
        candidates=info["candidates"],
    )


def _from_district_id(district_id: str) -> Optional[LocationResult]:
    """Build a manual LocationResult from a chosen district (no coordinates)."""
    gdf = load_districts()
    match = gdf[gdf["district_id"] == district_id]
    if match.empty:
        return None
    row = match.iloc[0]
    return LocationResult(
        location_source=SOURCE_MANUAL,
        district=str(row["district_name"]),
        state=str(row["state_or_division"]),
        district_id=str(row["district_id"]),
    )


def resolve_location(
    image_bytes: Optional[bytes] = None,
    device_coords: Optional[Tuple[float, float]] = None,
    manual_district_id: Optional[str] = None,
    manual_coords: Optional[Tuple[float, float]] = None,
) -> LocationResult:
    """
    Resolve location in priority order: EXIF GPS, device location, manual
    (map click coordinates, else chosen district), else unverified.
    """
    if image_bytes:
        exif = extract_exif_gps(image_bytes)
        if exif:
            return _from_point(exif[0], exif[1], SOURCE_GPS)
    if device_coords:
        return _from_point(device_coords[0], device_coords[1], SOURCE_DEVICE)
    if manual_coords:
        return _from_point(manual_coords[0], manual_coords[1], SOURCE_MANUAL)
    if manual_district_id:
        manual = _from_district_id(manual_district_id)
        if manual:
            return manual
    return LocationResult()
