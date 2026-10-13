"""
CycloneShield - Standards-referenced district risk engine
=========================================================
Replaces position-based tiering with a hazard model driven by the storm track.

Reference scales
----------------
* IMD cyclonic-disturbance classes (wind, knots, 3-min sustained):
  Depression 17-27, Deep Depression 28-33, Cyclonic Storm 34-47,
  Severe CS 48-63, Very Severe CS 64-89, Extremely Severe CS 90-119,
  Super CS >= 120.
* IMD / NDMA colour-coded warnings: Green (no action), Yellow (watch: be
  aware), Orange (alert: be prepared), Red (warning: take action).

Method
------
1. Wind at a district = max over track points of a parametric radial profile
   (linear rise to R_MAX, then (R_MAX/r)^0.6 decay) times that point's
   sustained wind.
2. Surge at a district = max over track points near the coast of the
   inverted-barometer proxy 0.099 * (1013 - P_min) m, decayed with distance.
3. Wind and surge are mapped to 0-100 sub-scores by piecewise-linear
   interpolation through anchors placed on the IMD category boundaries.
4. Score = min(100, max(W, S) + 0.1 * min(W, S)).
5. Colour/tier is read from the score, so the score and the tier always agree:
   >= 70 Red (CRITICAL), >= 50 Orange (HIGH), >= 30 Yellow (MODERATE),
   otherwise Green (LOW).

Limits: the profile and surge proxy are simplified and the surge-to-colour
mapping is a project convention (IMD publishes no surge-based colour rule).
This is decision support, not an official IMD/NDMA warning.
"""

import json
import math
import os
from typing import Any, Dict, List, Optional

import numpy as np
import pandas as pd

IMD_CLASSES = [
    (120.0, "Super Cyclonic Storm"),
    (90.0, "Extremely Severe Cyclonic Storm"),
    (64.0, "Very Severe Cyclonic Storm"),
    (48.0, "Severe Cyclonic Storm"),
    (34.0, "Cyclonic Storm"),
    (28.0, "Deep Depression"),
    (17.0, "Depression"),
]

WIND_ANCHORS = ([0, 17, 34, 48, 64, 90, 120], [0, 10, 30, 50, 70, 85, 100])
SURGE_ANCHORS = ([0, 0.5, 1.0, 2.0, 3.0, 4.0], [0, 30, 50, 70, 85, 100])

# (min score, IMD colour, tier, evacuation priority, NDMA/IMD meaning)
COLOUR_BANDS = [
    (70.0, "Red", "CRITICAL", 1, "Take action"),
    (50.0, "Orange", "HIGH", 2, "Be prepared"),
    (30.0, "Yellow", "MODERATE", 3, "Watch - be aware"),
    (0.0, "Green", "LOW", 4, "No action - monitor"),
]

R_MAX_KM = 30.0
WIND_DECAY_EXP = 0.6
SURGE_DECAY_KM = 80.0
SURGE_MAX_DIST2LAND_KM = 100.0
EARTH_R_KM = 6371.0


def classify_imd_wind(wind_kts: float) -> str:
    for threshold, name in IMD_CLASSES:
        if wind_kts >= threshold:
            return name
    return "Low Pressure Area"


def colour_band(score: float) -> Dict[str, Any]:
    for min_score, colour, tier, prio, meaning in COLOUR_BANDS:
        if score >= min_score:
            return {"colour": colour, "tier": tier, "priority": prio, "meaning": meaning}
    return {"colour": "Green", "tier": "LOW", "priority": 4, "meaning": "No action - monitor"}


def wind_score(wind_kts: float) -> float:
    return float(np.interp(wind_kts, *WIND_ANCHORS))


def surge_score(surge_m: float) -> float:
    return float(np.interp(surge_m, *SURGE_ANCHORS))


def composite_score(w: float, s: float) -> float:
    return round(min(100.0, max(w, s) + 0.1 * min(w, s)), 1)


def _haversine_km(lat1: float, lon1: float, lat2: np.ndarray, lon2: np.ndarray) -> np.ndarray:
    p1, p2 = math.radians(lat1), np.radians(lat2)
    dlat = p2 - p1
    dlon = np.radians(lon2) - math.radians(lon1)
    a = np.sin(dlat / 2) ** 2 + math.cos(p1) * np.cos(p2) * np.sin(dlon / 2) ** 2
    return 2 * EARTH_R_KM * np.arcsin(np.sqrt(a))


def district_hazard(lat: float, lon: float, track: pd.DataFrame) -> Dict[str, float]:
    """Wind (kts), surge (m) and closest-approach distance (km) at a point."""
    d = _haversine_km(lat, lon, track["lat"].to_numpy(float), track["lon"].to_numpy(float))
    vmax = track["wind_kts"].to_numpy(float)
    r = np.maximum(d, 1e-6)
    profile = np.where(r < R_MAX_KM, r / R_MAX_KM, (R_MAX_KM / r) ** WIND_DECAY_EXP)
    wind = float((vmax * profile).max())

    pres = track["pressure_mb"].to_numpy(float) if "pressure_mb" in track else np.full(len(track), 1013.0)
    near_coast = np.ones(len(track), bool)
    if "dist2land_km" in track:
        near_coast = track["dist2land_km"].to_numpy(float) <= SURGE_MAX_DIST2LAND_KM
    surge_pts = np.maximum(0.0, 0.099 * (1013.0 - pres)) * np.exp(-d / SURGE_DECAY_KM)
    surge = float(surge_pts[near_coast].max()) if near_coast.any() else 0.0
    return {"wind_kts": wind, "surge_m": surge, "closest_km": float(d.min())}


def _line_km(coords: List[List[float]]) -> float:
    arr = np.asarray(coords, float)
    if len(arr) < 2:
        return 0.0
    return float(sum(
        _haversine_km(arr[i][1], arr[i][0], arr[i + 1:i + 2, 1], arr[i + 1:i + 2, 0])[0]
        for i in range(len(arr) - 1)
    ))


def load_facilities(path: str) -> Dict[str, Any]:
    """Facility baseline grouped by district; empty if the file is missing."""
    out: Dict[str, Any] = {}
    if not os.path.exists(path):
        return out
    with open(path, "r", encoding="utf-8") as f:
        feats = json.load(f).get("features", [])
    for ft in feats:
        p, g = ft.get("properties", {}), ft.get("geometry", {})
        dist = p.get("district")
        if not dist:
            continue
        bucket = out.setdefault(dist, {"hospital": [], "shelter": [], "power_substation": [], "road_km": 0.0})
        kind = p.get("infra_type")
        if kind in bucket and g.get("type") == "Point":
            elev = p.get("elevation_m")
            bucket[kind].append(float(elev) if elev is not None and not pd.isna(elev) else None)
        elif g.get("type") == "LineString":
            bucket["road_km"] += _line_km(g.get("coordinates", []))
    return out


def _exposure(fac: Optional[Dict[str, Any]], surge_m: float) -> Dict[str, Any]:
    if not fac:
        return {"has_data": False, "fh": 0, "th": 0, "fs": 0, "ts": 0, "fp": 0, "road": 0.0}

    def flooded(elevs: List[Optional[float]]) -> int:
        return sum(1 for e in elevs if e is not None and surge_m > e)

    depth_factor = min(1.0, surge_m / 3.0) if surge_m >= 1.0 else 0.0
    return {
        "has_data": True,
        "fh": flooded(fac["hospital"]), "th": len(fac["hospital"]),
        "fs": flooded(fac["shelter"]), "ts": len(fac["shelter"]),
        "fp": flooded(fac["power_substation"]),
        "road": round(fac["road_km"] * depth_factor, 1),
    }


def _driver_and_action(w: float, s: float, wind_kts: float, surge_m: float, band: Dict[str, Any], hq: str) -> Dict[str, str]:
    cls = classify_imd_wind(wind_kts)
    if band["tier"] == "LOW":
        return {
            "driver": "Peripheral winds and rain (below Cyclonic Storm strength)",
            "action": "IMD Green: no action; continue monitoring bulletins.",
        }
    if s > w:
        driver = f"Storm surge inundation (~{surge_m:.1f} m proxy)"
        focus = "Prepare low-lying coastal evacuation and shelter activation."
    else:
        driver = f"{cls}-force winds (~{wind_kts:.0f} kts)"
        focus = "Secure loose structures, power and communication lines; prepare shelters."
    prefix = {
        "Red": "IMD Red (take action)",
        "Orange": "IMD Orange (be prepared)",
        "Yellow": "IMD Yellow (be aware)",
    }[band["colour"]]
    return {"driver": driver, "action": f"{prefix}: {focus} Coordinate with DDMA/SDMA at {hq}."}


def compute_district_risk(
    districts: List[Dict[str, Any]],
    track: pd.DataFrame,
    state_name: str,
    fallback_wind_kts: float,
    fallback_pressure_mb: float,
    facilities: Optional[Dict[str, Any]] = None,
    fallback_point: Optional[tuple] = None,
) -> pd.DataFrame:
    """Return one scored row per district, sorted by score then population."""
    if track is None or track.empty or not {"lat", "lon", "wind_kts"}.issubset(track.columns):
        lat0, lon0 = fallback_point or (
            float(np.mean([d["lat"] for d in districts if d.get("lat") is not None] or [20.5])),
            float(np.mean([d["lon"] for d in districts if d.get("lon") is not None] or [85.0])),
        )
        track = pd.DataFrame({"lat": [lat0], "lon": [lon0], "wind_kts": [fallback_wind_kts], "pressure_mb": [fallback_pressure_mb]})
    if "pressure_mb" not in track.columns:
        track = track.assign(pressure_mb=fallback_pressure_mb)

    rows = []
    for d in districts:
        lat, lon = d.get("lat"), d.get("lon")
        if lat is None or lon is None:
            continue
        hz = district_hazard(float(lat), float(lon), track)
        w, s = wind_score(hz["wind_kts"]), surge_score(hz["surge_m"])
        score = composite_score(w, s)
        band = colour_band(score)
        ex = _exposure((facilities or {}).get(d["district_name"]), hz["surge_m"])
        txt = _driver_and_action(w, s, hz["wind_kts"], hz["surge_m"], band, d.get("hq", "the district HQ"))
        rows.append({
            "district_name": d["district_name"],
            "state_or_division": state_name,
            "country": d.get("country", "India"),
            "lat": float(lat),
            "lon": float(lon),
            "population": int(d.get("population", 0)),
            "district_wind_kts": round(hz["wind_kts"], 1),
            "imd_wind_class": classify_imd_wind(hz["wind_kts"]),
            "district_surge_m": round(hz["surge_m"], 2),
            "closest_approach_km": round(hz["closest_km"], 0),
            "wind_subscore": round(w, 1),
            "surge_subscore": round(s, 1),
            "vulnerability_score": score,
            "imd_colour": band["colour"],
            "imd_colour_meaning": band["meaning"],
            "threat_tier": band["tier"],
            "evacuation_priority": band["priority"],
            "primary_risk_driver": txt["driver"],
            "flooded_hospitals": ex["fh"],
            "total_hospitals": ex["th"],
            "flooded_shelters": ex["fs"],
            "total_shelters": ex["ts"],
            "submerged_road_km": ex["road"],
            "flooded_power_substations": ex["fp"],
            "facility_data_available": ex["has_data"],
            "action_directive": txt["action"],
        })
    df = pd.DataFrame(rows)
    if df.empty:
        return df
    df = df.sort_values(["vulnerability_score", "population"], ascending=False).reset_index(drop=True)
    df.insert(0, "rank", np.arange(1, len(df) + 1))
    return df
