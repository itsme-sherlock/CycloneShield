"""
CycloneShield - Wind Hazard Swath Engine (Chapter 2)
===================================================
Transforms linear cyclone track into dynamic, physically-grounded spatial wind swaths:
  - Core Zone     (Base 60 km radius):  Destructive storm-force wind zone (>48 kts / >89 km/h)
  - Moderate Zone (Base 120 km radius): Gale-force wind zone (34-47 kts / 63-88 km/h)
  - Outer Zone    (Base 200 km radius): Squally peripheral zone (25-33 kts / 46-62 km/h)

Key Capabilities:
  - Metric UTM projection (EPSG:32645 for Bay of Bengal) preventing equatorial/polar distortions.
  - Dynamic scaling: R(V) = R_base * (V / V_thresh)^alpha based on segment wind speed.
  - Seamless topological GeoJSON generation (EPSG:4326) compatible with Google Earth Engine & Google Maps.
  - Google Material Design palette (#ef4444 Red, #f59e0b Amber, #3b82f6 Blue).
  - Google Satellite Hybrid & Carto Dark Folium interactive mapping with layer toggles.
  - Publication-grade multi-panel static visualization for reports and pitch decks.
"""

import os
import shutil
import argparse
from typing import Tuple, Dict, Any, List

import numpy as np
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point, LineString, Polygon, MultiPolygon
from shapely.ops import unary_union
import folium
from folium import plugins
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.patches as mpatches

# Base directory paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")
MIRROR_DIR = r"C:\mnt\agents\output\cycloneshield"

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Google Material Design Hazard Color Palette & Parameters
HAZARD_ZONES: List[Dict[str, Any]] = [
    {
        "zone_id": "core",
        "zone_name": "Core Destructive Swath (>48 kts)",
        "hazard_level": "CRITICAL",
        "wind_threshold_kts": 48.0,
        "wind_threshold_kmh": 88.9,
        "base_radius_km": 60.0,
        "scale_exponent": 0.5,
        "fill_color": "#ef4444",      # Material Red 500
        "stroke_color": "#b91c1c",    # Material Red 700
        "fill_opacity": 0.45,
        "stroke_opacity": 0.90,
        "weight": 2.5,
        "description": "Destructive hurricane/severe storm-force winds. Extreme structural threat to roofing, unreinforced masonry, power distribution pylons, and widespread tree falls.",
        "evacuation_directive": "Immediate mandatory evacuation to cyclone shelters; complete shutdown of ports, airports, and transport."
    },
    {
        "zone_id": "moderate",
        "zone_name": "Moderate Gale Swath (34-47 kts)",
        "hazard_level": "HIGH",
        "wind_threshold_kts": 34.0,
        "wind_threshold_kmh": 63.0,
        "base_radius_km": 120.0,
        "scale_exponent": 0.5,
        "fill_color": "#f59e0b",      # Material Amber 500
        "stroke_color": "#b45309",    # Material Amber 700
        "fill_opacity": 0.35,
        "stroke_opacity": 0.80,
        "weight": 2.0,
        "description": "Gale-force sustained winds. Risk of damage to thatched/tin homes, overhead wires, communication towers, and minor boat capsizing.",
        "evacuation_directive": "Relocate vulnerable coastal populations; reinforce temporary dwellings and clear storm drainage canals."
    },
    {
        "zone_id": "outer",
        "zone_name": "Outer Squall Swath (25-33 kts)",
        "hazard_level": "MODERATE",
        "wind_threshold_kts": 25.0,
        "wind_threshold_kmh": 46.3,
        "base_radius_km": 200.0,
        "scale_exponent": 0.4,
        "fill_color": "#3b82f6",      # Material Blue 500
        "stroke_color": "#1d4ed8",    # Material Blue 700
        "fill_opacity": 0.22,
        "stroke_opacity": 0.70,
        "weight": 1.5,
        "description": "Squally peripheral wind field with persistent gusting rainbands, high oceanic swell, and localized flash waterlogging.",
        "evacuation_directive": "Total ban on offshore fishing; secure harbor vessels and activate district emergency response teams."
    }
]


def get_utm_epsg(lon: float, lat: float) -> int:
    """
    Determine appropriate UTM EPSG code based on central longitude and latitude.
    For Bay of Bengal (~88-90°E), returns 32645 (UTM Zone 45N).
    """
    zone = int((lon + 180) / 6) + 1
    return 32600 + zone if lat >= 0 else 32700 + zone


def calculate_dynamic_radius(wind_kts: float, base_radius_km: float, threshold_kts: float, exponent: float = 0.5, max_scale: float = 1.6) -> float:
    """
    Compute dynamically scaled wind swath radius in kilometers.
    R(V) = R_base * (V / V_thresh)^exponent (capped at max_scale * R_base).
    Returns 0.0 if wind speed is below the zone threshold.
    """
    if pd.isna(wind_kts) or wind_kts < threshold_kts:
        return 0.0
    scale = (wind_kts / threshold_kts) ** exponent
    scale = min(scale, max_scale)
    return base_radius_km * scale


def generate_wind_swaths(
    track_gdf: gpd.GeoDataFrame,
    storm_name: str = "REMAL",
    step_meters: float = 5000.0
) -> Tuple[gpd.GeoDataFrame, gpd.GeoDataFrame]:
    """
    Transform cyclone track into seamless topological wind swaths and time segments.

    Parameters:
        track_gdf: GeoDataFrame with columns ['time', 'lat', 'lon', 'wind_kts', 'pressure_mb', 'geometry']
        storm_name: Name of cyclone (e.g. REMAL)
        step_meters: Densification distance along track in meters (default 5 km for smooth curve union)

    Returns:
        swaths_gdf: Unified GeoDataFrame with 3 hazard zone polygons (Outer, Moderate, Core) in EPSG:4326
        segments_gdf: Time-stepped segment GeoDataFrame for interactive timeline animation
    """
    # Ensure track is sorted chronologically
    track = track_gdf.sort_values("time").copy().reset_index(drop=True)
    if "time" in track.columns:
        track["time"] = pd.to_datetime(track["time"])

    # Determine UTM CRS
    mean_lon = track["lon"].mean()
    mean_lat = track["lat"].mean()
    utm_epsg = get_utm_epsg(mean_lon, mean_lat)
    print(f"[CycloneShield] Projecting track to UTM Zone {utm_epsg % 100}N (EPSG:{utm_epsg}) for meter-accurate buffering...")

    track_utm = track.to_crs(epsg=utm_epsg)
    coords = np.array([[g.x, g.y] for g in track_utm.geometry])

    # Compute cumulative distance along the track
    diffs = np.diff(coords, axis=0)
    seg_dists = np.sqrt((diffs ** 2).sum(axis=1))
    cum_dists = np.insert(np.cumsum(seg_dists), 0, 0.0)
    total_length_m = cum_dists[-1]

    # Densify sampling points along track line for seamless swath corridor
    num_samples = max(int(total_length_m / step_meters) + 1, len(coords) * 5)
    sample_dists = np.linspace(0, total_length_m, num_samples)

    # Linearly interpolate wind speed and pressure along cumulative distance
    winds = track_utm["wind_kts"].values
    pressures = track_utm["pressure_mb"].values if "pressure_mb" in track_utm.columns else np.full(len(winds), 1000.0)
    sample_winds = np.interp(sample_dists, cum_dists, winds)
    sample_pressures = np.interp(sample_dists, cum_dists, pressures)

    # Build continuous track line
    track_line = LineString(coords)
    sample_points = [track_line.interpolate(d) for d in sample_dists]

    # 1. Generate Unified Cumulative Hazard Swaths
    swath_records = []
    # Process from Outer to Core
    for zone in HAZARD_ZONES:
        z_id = zone["zone_id"]
        thresh = zone["wind_threshold_kts"]
        base_r = zone["base_radius_km"]
        exp = zone["scale_exponent"]

        buffers = []
        max_r_km = 0.0

        for pt, w in zip(sample_points, sample_winds):
            if w >= thresh:
                r_km = calculate_dynamic_radius(w, base_r, thresh, exp)
                max_r_km = max(max_r_km, r_km)
                # Buffer in meters
                buffers.append(pt.buffer(r_km * 1000.0))

        if buffers:
            unified_poly = unary_union(buffers)
            # Gentle simplification (500 meters) to optimize vertex count for web rendering
            unified_poly = unified_poly.simplify(500.0, preserve_topology=True)
            area_sqkm = unified_poly.area / 1e6
        else:
            unified_poly = Polygon()
            area_sqkm = 0.0

        rec = {
            "storm_name": storm_name.upper(),
            "zone_id": z_id,
            "zone_name": zone["zone_name"],
            "hazard_level": zone["hazard_level"],
            "wind_threshold_kts": thresh,
            "wind_threshold_kmh": zone["wind_threshold_kmh"],
            "base_radius_km": base_r,
            "max_scaled_radius_km": round(max_r_km, 1),
            "area_sqkm": round(area_sqkm, 1),
            "fill_color": zone["fill_color"],
            "stroke_color": zone["stroke_color"],
            "fill_opacity": zone["fill_opacity"],
            "stroke_opacity": zone["stroke_opacity"],
            "weight": zone["weight"],
            "description": zone["description"],
            "evacuation_directive": zone["evacuation_directive"],
            "geometry": unified_poly
        }
        swath_records.append(rec)

    swaths_utm = gpd.GeoDataFrame(swath_records, crs=f"EPSG:{utm_epsg}")
    swaths_gdf = swaths_utm.to_crs("EPSG:4326")

    # 2. Generate Time-Stepped Segment Swaths for Timeline Animation
    segment_records = []
    for i in range(len(track) - 1):
        pt1 = track_utm.geometry.iloc[i]
        pt2 = track_utm.geometry.iloc[i + 1]
        line_seg = LineString([pt1, pt2])
        w_seg = (winds[i] + winds[i + 1]) / 2.0
        p_seg = (pressures[i] + pressures[i + 1]) / 2.0

        # Dynamic radii for segment
        r_core = calculate_dynamic_radius(w_seg, 60.0, 48.0)
        r_mod = calculate_dynamic_radius(w_seg, 120.0, 34.0)
        r_outer = calculate_dynamic_radius(w_seg, 200.0, 25.0)

        # Buffer segment by moderate radius as primary segment footprint
        active_r_km = r_mod if r_mod > 0 else (r_outer if r_outer > 0 else 20.0)
        seg_poly = line_seg.buffer(active_r_km * 1000.0).simplify(500.0, preserve_topology=True)

        segment_records.append({
            "storm_name": storm_name.upper(),
            "segment_id": i + 1,
            "time_start": str(track["time"].iloc[i]),
            "time_end": str(track["time"].iloc[i + 1]),
            "wind_kts": round(float(w_seg), 1),
            "pressure_mb": round(float(p_seg), 1),
            "core_radius_km": round(r_core, 1),
            "moderate_radius_km": round(r_mod, 1),
            "outer_radius_km": round(r_outer, 1),
            "geometry": seg_poly
        })

    segments_utm = gpd.GeoDataFrame(segment_records, crs=f"EPSG:{utm_epsg}")
    segments_gdf = segments_utm.to_crs("EPSG:4326")

    return swaths_gdf, segments_gdf


def generate_swaths_summary(swaths_gdf: gpd.GeoDataFrame, track_gdf: gpd.GeoDataFrame) -> pd.DataFrame:
    """Generate a clean tabular summary of the 3 wind hazard zones."""
    peak_wind = track_gdf["wind_kts"].max()
    min_pressure = track_gdf["pressure_mb"].min() if "pressure_mb" in track_gdf.columns else 977.0

    summary_rows = []
    for _, row in swaths_gdf.iterrows():
        summary_rows.append({
            "Hazard Zone": row["zone_name"],
            "Threat Level": row["hazard_level"],
            "Wind Threshold (kts)": f">= {row['wind_threshold_kts']:.0f} kts",
            "Wind Threshold (km/h)": f">= {row['wind_threshold_kmh']:.1f} km/h",
            "Base Radius (km)": f"{row['base_radius_km']:.0f} km",
            "Peak Scaled Radius (km)": f"{row['max_scaled_radius_km']:.1f} km",
            "Total Swath Area (sq km)": f"{row['area_sqkm']:,.1f}",
            "Peak Observed Wind": f"{peak_wind:.1f} kts",
            "Min Central Pressure": f"{min_pressure:.1f} mb",
            "Recommended Action": row["evacuation_directive"]
        })

    return pd.DataFrame(summary_rows)


def plot_wind_swaths_map(
    track_gdf: gpd.GeoDataFrame,
    swaths_gdf: gpd.GeoDataFrame,
    storm_name: str = "REMAL",
    output_html: str = None
) -> str:
    """
    Build rich interactive Folium map with Google Basemaps, Google Material Design swaths,
    detailed click cards, and floating hazard legend.
    """
    if output_html is None:
        output_html = os.path.join(OUTPUT_DIR, f"{storm_name.lower()}_wind_swaths_map.html")

    center_lat = track_gdf["lat"].mean()
    center_lon = track_gdf["lon"].mean()

    # 1. Initialize Map with Google Cartography Base
    m = folium.Map(
        location=[center_lat + 1.0, center_lon],
        zoom_start=6,
        tiles=None
    )

    # 100% Free Basemaps (No API Key Required)
    folium.TileLayer(
        tiles="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png",
        attr='&copy; <a href="https://carto.com/">CARTO</a> &copy; OpenStreetMap',
        name="CartoDB Dark Matter",
        overlay=False,
        control=True
    ).add_to(m)

    folium.TileLayer("OpenStreetMap", name="OpenStreetMap Standard").add_to(m)

    # 2. Add Wind Swaths (Render from Outer -> Moderate -> Core)
    zone_order = ["outer", "moderate", "core"]
    for zid in zone_order:
        match = swaths_gdf[swaths_gdf["zone_id"] == zid]
        if match.empty:
            continue
        row = match.iloc[0]
        if row.geometry.is_empty:
            continue

        fg = folium.FeatureGroup(name=f"Hazard Swath: {row['zone_name']}", show=True)

        popup_html = f"""
        <div style="font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; min-width: 260px; padding: 4px;">
            <div style="background-color: {row['fill_color']}; color: white; padding: 6px 10px; border-radius: 4px; font-weight: bold; font-size: 13px;">
                {row['zone_name']} [{row['hazard_level']}]
            </div>
            <div style="margin-top: 8px; font-size: 12px; color: #1e293b; line-height: 1.5;">
                <b>Storm:</b> Cyclone {storm_name}<br/>
                <b>Wind Threshold:</b> ≥ {row['wind_threshold_kts']:.0f} kts ({row['wind_threshold_kmh']:.1f} km/h)<br/>
                <b>Base Radius:</b> {row['base_radius_km']:.0f} km &nbsp;|&nbsp; <b>Max Scaled:</b> {row['max_scaled_radius_km']:.1f} km<br/>
                <b>Swath Coverage:</b> <span style="font-weight: bold; color: {row['stroke_color']};">{row['area_sqkm']:,.1f} km²</span><br/>
                <hr style="border: 0; border-top: 1px solid #e2e8f0; margin: 6px 0;"/>
                <b>Impact:</b> {row['description']}<br/>
                <div style="margin-top: 6px; padding: 4px 6px; background-color: #f1f5f9; border-left: 3px solid {row['fill_color']}; font-size: 11px;">
                    <b>NDRF Protocol:</b> {row['evacuation_directive']}
                </div>
            </div>
        </div>
        """

        folium.GeoJson(
            row.geometry,
            name=row["zone_name"],
            style_function=lambda x, fc=row["fill_color"], sc=row["stroke_color"], fo=row["fill_opacity"], so=row["stroke_opacity"], w=row["weight"]: {
                "fillColor": fc,
                "color": sc,
                "weight": w,
                "fillOpacity": fo,
                "opacity": so
            },
            highlight_function=lambda x: {"weight": 3.5, "fillOpacity": 0.65},
            tooltip=f"{row['zone_name']} | Area: {row['area_sqkm']:,.0f} km²",
            popup=folium.Popup(popup_html, max_width=320)
        ).add_to(fg)

        fg.add_to(m)

    # 3. Add Track Path Line & Synoptic Points
    track_fg = folium.FeatureGroup(name=f"Cyclone {storm_name} Track Path", show=True)
    coords_ll = list(zip(track_gdf["lat"], track_gdf["lon"]))

    # Polyline Glow & Core Line
    folium.PolyLine(
        locations=coords_ll,
        color="#38bdf8",
        weight=4.5,
        opacity=0.9,
        tooltip=f"Cyclone {storm_name} Path"
    ).add_to(track_fg)

    # Track Points
    peak_idx = track_gdf["wind_kts"].idxmax()
    for idx, row in track_gdf.iterrows():
        is_peak = (idx == peak_idx)
        w = row["wind_kts"]
        color = "#ef4444" if w >= 60 else ("#f59e0b" if w >= 48 else ("#10b981" if w >= 34 else "#3b82f6"))

        pt_popup = f"""
        <div style="font-family: Arial, sans-serif; font-size: 12px; min-width: 180px;">
            <b style="color: {color}; font-size: 13px;">Cyclone {storm_name}</b><br/>
            <b>Observation:</b> {pd.to_datetime(row['time']).strftime('%b %d, %H:%M UTC')}<br/>
            <b>Wind:</b> {w:.1f} kts ({w*1.852:.1f} km/h)<br/>
            <b>Pressure:</b> {row['pressure_mb']:.1f} mb<br/>
            <b>Position:</b> {row['lat']:.2f}°N, {row['lon']:.2f}°E
            {'<br/><b style="color:#ef4444;">★ PEAK INTENSITY</b>' if is_peak else ''}
        </div>
        """

        folium.CircleMarker(
            location=[row["lat"], row["lon"]],
            radius=8 if is_peak else 4.5,
            color="#ffffff" if is_peak else color,
            weight=2 if is_peak else 1,
            fill=True,
            fill_color=color,
            fill_opacity=0.95,
            popup=folium.Popup(pt_popup, max_width=240),
            tooltip=f"{pd.to_datetime(row['time']).strftime('%b %d %H:%M')} | {w:.0f} kts"
        ).add_to(track_fg)

    # Landfall Marker
    landfall_row = track_gdf.iloc[-1]
    folium.Marker(
        location=[landfall_row["lat"], landfall_row["lon"]],
        icon=folium.Icon(color="red", icon="flag", prefix="fa"),
        tooltip=f"Inland Dissipation: {pd.to_datetime(landfall_row['time']).strftime('%b %d %H:%M UTC')}"
    ).add_to(track_fg)

    track_fg.add_to(m)

    # 4. Floating Google Material Legend & Control Card
    core_area = swaths_gdf[swaths_gdf["zone_id"] == "core"]["area_sqkm"].values[0] if not swaths_gdf[swaths_gdf["zone_id"] == "core"].empty else 0
    mod_area = swaths_gdf[swaths_gdf["zone_id"] == "moderate"]["area_sqkm"].values[0] if not swaths_gdf[swaths_gdf["zone_id"] == "moderate"].empty else 0
    outer_area = swaths_gdf[swaths_gdf["zone_id"] == "outer"]["area_sqkm"].values[0] if not swaths_gdf[swaths_gdf["zone_id"] == "outer"].empty else 0

    legend_html = f"""
    <div style="
        position: fixed;
        bottom: 24px;
        right: 24px;
        width: 320px;
        background: rgba(15, 23, 42, 0.92);
        color: #f8fafc;
        border: 1px solid rgba(148, 163, 184, 0.25);
        border-radius: 12px;
        padding: 14px 16px;
        font-family: 'Segoe UI', Roboto, sans-serif;
        font-size: 12px;
        z-index: 9999;
        box-shadow: 0 10px 25px rgba(0,0,0,0.5);
        backdrop-filter: blur(8px);
    ">
        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 8px; border-bottom: 1px solid #334155; padding-bottom: 6px;">
            <b style="font-size: 14px; color: #38bdf8;">CycloneShield</b>
            <span style="background: #ef4444; color: white; padding: 2px 6px; border-radius: 4px; font-size: 10px; font-weight: bold;">CH. 2 ACTIVE</span>
        </div>
        <div style="font-weight: 600; color: #f1f5f9; margin-bottom: 8px;">Cyclone {storm_name} Wind Hazard Swaths</div>
        
        <div style="display: flex; align-items: center; margin-bottom: 6px;">
            <span style="width: 14px; height: 14px; background: #ef4444; border: 1.5px solid #b91c1c; border-radius: 3px; display: inline-block; margin-right: 8px;"></span>
            <div style="flex-grow: 1;"><b>Core Zone</b> (&gt;48 kts / &gt;89 km/h)</div>
            <span style="color: #94a3b8; font-size: 11px;">{core_area:,.0f} km²</span>
        </div>
        <div style="display: flex; align-items: center; margin-bottom: 6px;">
            <span style="width: 14px; height: 14px; background: #f59e0b; border: 1.5px solid #b45309; border-radius: 3px; display: inline-block; margin-right: 8px;"></span>
            <div style="flex-grow: 1;"><b>Moderate Zone</b> (34-47 kts)</div>
            <span style="color: #94a3b8; font-size: 11px;">{mod_area:,.0f} km²</span>
        </div>
        <div style="display: flex; align-items: center; margin-bottom: 8px;">
            <span style="width: 14px; height: 14px; background: #3b82f6; border: 1.5px solid #1d4ed8; border-radius: 3px; display: inline-block; margin-right: 8px;"></span>
            <div style="flex-grow: 1;"><b>Outer Zone</b> (25-33 kts)</div>
            <span style="color: #94a3b8; font-size: 11px;">{outer_area:,.0f} km²</span>
        </div>

        <div style="border-top: 1px solid #334155; padding-top: 6px; display: flex; justify-content: space-between; color: #94a3b8; font-size: 11px;">
            <span>Projected: UTM 45N / EPSG:32645</span>
            <span>Google Ecosystem</span>
        </div>
    </div>
    """
    m.get_root().html.add_child(folium.Element(legend_html))

    # Add LayerControl
    folium.LayerControl(collapsed=False).add_to(m)

    m.save(output_html)
    print(f"[CycloneShield] Interactive Folium map saved to: {output_html}")
    return output_html


def plot_wind_swaths_static(
    track_gdf: gpd.GeoDataFrame,
    swaths_gdf: gpd.GeoDataFrame,
    storm_name: str = "REMAL",
    output_png: str = None
) -> str:
    """
    Generate high-resolution multi-panel static visualization:
      Panel 1: Spatial Map of Bay of Bengal with Coastlines, Swaths & Track
      Panel 2: Dynamic Swath Radii vs Time Expansion Profile
      Panel 3: Geographic Impact Footprint (Area & Intensity Breakdown)
    """
    if output_png is None:
        output_png = os.path.join(OUTPUT_DIR, f"{storm_name.lower()}_wind_swaths_plot.png")

    fig = plt.figure(figsize=(18, 9), facecolor="#0f172a")

    # Grid layout: Left = Map (large), Right Top = Radii expansion, Right Bottom = Area bar chart
    gs = fig.add_gridspec(2, 2, width_ratios=[1.25, 1.0], wspace=0.18, hspace=0.30)

    # -------------------------------------------------------------
    # PANEL 1: Spatial Hazard Map
    # -------------------------------------------------------------
    ax_map = fig.add_subplot(gs[:, 0], facecolor="#090d16")

    # Load regional boundaries if available
    reg_path = os.path.join(DATA_DIR, "regional_boundaries.geojson")
    if os.path.exists(reg_path):
        try:
            reg_gdf = gpd.read_file(reg_path)
            reg_gdf.plot(ax=ax_map, facecolor="#1e293b", edgecolor="#334155", linewidth=1.0, zorder=1)
        except Exception:
            pass

    # Plot swaths from Outer -> Moderate -> Core
    zone_order = ["outer", "moderate", "core"]
    for zid in zone_order:
        sub = swaths_gdf[swaths_gdf["zone_id"] == zid]
        if not sub.empty and not sub.iloc[0].geometry.is_empty:
            row = sub.iloc[0]
            gpd.GeoSeries([row.geometry], crs="EPSG:4326").plot(
                ax=ax_map,
                facecolor=row["fill_color"],
                edgecolor=row["stroke_color"],
                alpha=row["fill_opacity"] + 0.1,
                linewidth=row["weight"],
                zorder=2 if zid == "outer" else (3 if zid == "moderate" else 4),
                label=f"{row['zone_name']} ({row['area_sqkm']:,.0f} km²)"
            )

    # Plot Track Polyline
    ax_map.plot(track_gdf["lon"], track_gdf["lat"], color="#38bdf8", linestyle="-", linewidth=2.8, zorder=5, alpha=0.9)

    # Scatter points colored by wind intensity
    scatter = ax_map.scatter(
        track_gdf["lon"], track_gdf["lat"],
        c=track_gdf["wind_kts"],
        cmap="YlOrRd",
        s=track_gdf["wind_kts"] * 1.8,
        edgecolors="white",
        linewidth=0.8,
        zorder=6
    )

    # Highlight peak point & landfall
    peak_idx = track_gdf["wind_kts"].idxmax()
    peak_row = track_gdf.loc[peak_idx]
    landfall_row = track_gdf.iloc[-1]
    start_row = track_gdf.iloc[0]

    ax_map.scatter([peak_row["lon"]], [peak_row["lat"]], color="#ef4444", s=220, marker="*", edgecolors="white", linewidth=1.2, zorder=7)
    ax_map.annotate(f"Peak ({peak_row['wind_kts']:.0f} kts)\n{peak_row['pressure_mb']:.0f} mb",
                    (peak_row["lon"], peak_row["lat"]),
                    color="#ffffff", fontsize=10, fontweight="bold",
                    textcoords="offset points", xytext=(-85, 10),
                    bbox=dict(boxstyle="round,pad=0.3", fc="#ef4444", ec="white", alpha=0.9))

    ax_map.annotate("Landfall", (landfall_row["lon"], landfall_row["lat"]),
                    color="#fbbf24", fontsize=10, fontweight="bold",
                    textcoords="offset points", xytext=(12, -8))

    # Set spatial bounds around Bay of Bengal swath
    total_bounds = swaths_gdf.total_bounds  # [minx, miny, maxx, maxy]
    ax_map.set_xlim(total_bounds[0] - 1.2, total_bounds[2] + 1.2)
    ax_map.set_ylim(total_bounds[1] - 1.0, total_bounds[3] + 1.5)

    ax_map.set_title(f"Cyclone {storm_name} — Spatial Wind Hazard Swaths (Bay of Bengal)", color="#f8fafc", fontsize=13, fontweight="bold", pad=12)
    ax_map.set_xlabel("Longitude (°E)", color="#94a3b8", fontsize=10)
    ax_map.set_ylabel("Latitude (°N)", color="#94a3b8", fontsize=10)
    ax_map.tick_params(colors="#94a3b8")
    ax_map.grid(color="#1e293b", linestyle=":", linewidth=0.8)

    # Legend for Map
    map_legend = ax_map.legend(loc="lower left", facecolor="#0f172a", edgecolor="#475569", labelcolor="#f8fafc", fontsize=9)
    map_legend.get_frame().set_alpha(0.85)

    # -------------------------------------------------------------
    # PANEL 2: Dynamic Radii Expansion Timeline
    # -------------------------------------------------------------
    ax_time = fig.add_subplot(gs[0, 1], facecolor="#1e293b")
    times = pd.to_datetime(track_gdf["time"])
    winds = track_gdf["wind_kts"].values

    r_cores = [calculate_dynamic_radius(w, 60.0, 48.0) for w in winds]
    r_mods = [calculate_dynamic_radius(w, 120.0, 34.0) for w in winds]
    r_outers = [calculate_dynamic_radius(w, 200.0, 25.0) for w in winds]

    ax_time.plot(times, r_outers, color="#3b82f6", linewidth=2.2, label="Outer Swath Radius (Base 200 km)")
    ax_time.plot(times, r_mods, color="#f59e0b", linewidth=2.4, label="Moderate Swath Radius (Base 120 km)")
    ax_time.plot(times, r_cores, color="#ef4444", linewidth=2.6, label="Core Swath Radius (Base 60 km)")

    ax_time.fill_between(times, 0, r_cores, color="#ef4444", alpha=0.25)
    ax_time.fill_between(times, r_cores, r_mods, color="#f59e0b", alpha=0.15)
    ax_time.fill_between(times, r_mods, r_outers, color="#3b82f6", alpha=0.08)

    ax_time.set_title("Dynamic Wind Swath Radial Expansion Profile vs Time", color="#f8fafc", fontsize=11, fontweight="bold", pad=8)
    ax_time.set_ylabel("Dynamic Radius (km)", color="#f8fafc", fontsize=10)
    ax_time.tick_params(axis="y", labelcolor="#f8fafc", colors="#94a3b8")
    ax_time.tick_params(axis="x", colors="#94a3b8")
    ax_time.xaxis.set_major_formatter(mdates.DateFormatter("%b %d\n%H:%M"))
    ax_time.grid(color="#334155", linestyle=":", linewidth=0.7)

    # Twin axis for actual wind speed
    ax_twin = ax_time.twinx()
    ax_twin.plot(times, winds, color="#38bdf8", linestyle="--", linewidth=1.8, label="Vmax (kts)")
    ax_twin.set_ylabel("Sustained Wind (kts)", color="#38bdf8", fontsize=10)
    ax_twin.tick_params(axis="y", labelcolor="#38bdf8", colors="#94a3b8")

    lines_1, labels_1 = ax_time.get_legend_handles_labels()
    lines_2, labels_2 = ax_twin.get_legend_handles_labels()
    ax_time.legend(lines_1 + lines_2, labels_1 + labels_2, loc="upper left", facecolor="#0f172a", edgecolor="#475569", labelcolor="#f8fafc", fontsize=8)

    # -------------------------------------------------------------
    # PANEL 3: Surface Footprint Area & Severity Breakdown
    # -------------------------------------------------------------
    ax_bar = fig.add_subplot(gs[1, 1], facecolor="#1e293b")

    zone_labels = ["Outer\n(Squall ≥25 kts)", "Moderate\n(Gale ≥34 kts)", "Core\n(Storm ≥48 kts)"]
    areas = [
        swaths_gdf[swaths_gdf["zone_id"] == "outer"]["area_sqkm"].values[0] if not swaths_gdf[swaths_gdf["zone_id"] == "outer"].empty else 0,
        swaths_gdf[swaths_gdf["zone_id"] == "moderate"]["area_sqkm"].values[0] if not swaths_gdf[swaths_gdf["zone_id"] == "moderate"].empty else 0,
        swaths_gdf[swaths_gdf["zone_id"] == "core"]["area_sqkm"].values[0] if not swaths_gdf[swaths_gdf["zone_id"] == "core"].empty else 0
    ]
    bar_colors = ["#3b82f6", "#f59e0b", "#ef4444"]

    bars = ax_bar.barh(zone_labels, areas, color=bar_colors, edgecolor="#ffffff", linewidth=0.8, height=0.55)

    for bar, val in zip(bars, areas):
        ax_bar.text(
            bar.get_width() + (max(areas) * 0.02),
            bar.get_y() + bar.get_height() / 2,
            f"{val:,.0f} km²",
            va="center", ha="left", color="#f8fafc", fontsize=9, fontweight="bold"
        )

    ax_bar.set_xlim(0, max(areas) * 1.25)
    ax_bar.set_title("Geographic Impact Area by Hazard Severity Tier", color="#f8fafc", fontsize=11, fontweight="bold", pad=8)
    ax_bar.set_xlabel("Surface Area (sq km)", color="#94a3b8", fontsize=10)
    ax_bar.tick_params(colors="#94a3b8")
    ax_bar.grid(axis="x", color="#334155", linestyle=":", linewidth=0.7)

    fig.subplots_adjust(left=0.06, right=0.94, top=0.93, bottom=0.08, wspace=0.22, hspace=0.32)
    plt.savefig(output_png, dpi=250, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close()
    print(f"[CycloneShield] Static plot saved to: {output_png}")
    return output_png


def sync_to_mirror():
    """Sync outputs and modular code to C:\\mnt\\agents\\output\\cycloneshield."""
    if os.path.exists(MIRROR_DIR):
        try:
            if os.path.samefile(BASE_DIR, MIRROR_DIR):
                print(f"[CycloneShield] Mirror directory {MIRROR_DIR} is linked directly to workspace (all artifacts synced).")
                return
            mirror_out = os.path.join(MIRROR_DIR, "outputs")
            os.makedirs(mirror_out, exist_ok=True)
            shutil.copy2(os.path.abspath(__file__), os.path.join(MIRROR_DIR, "wind_swath.py"))
            for f in os.listdir(OUTPUT_DIR):
                src = os.path.join(OUTPUT_DIR, f)
                dst = os.path.join(mirror_out, f)
                if os.path.isfile(src):
                    shutil.copy2(src, dst)
            print(f"[CycloneShield] Successfully mirrored files to {MIRROR_DIR}")
        except Exception as e:
            print(f"[CycloneShield] Mirror sync note: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CycloneShield Chapter 2: Wind Hazard Swath Engine")
    parser.add_argument("--cyclone", type=str, default="REMAL", help="Cyclone name (e.g. REMAL, DANA)")
    parser.add_argument("--input-track", type=str, default=None, help="Path to input track GeoJSON/CSV")
    parser.add_argument("--step-km", type=float, default=5.0, help="Track densification step in km (default 5.0)")
    args = parser.parse_args()

    storm_name = args.cyclone.upper()

    print(f"\n========================================================")
    print(f"CycloneShield - CHAPTER 2: WIND HAZARD SWATH ENGINE")
    print(f"Target Cyclone: {storm_name}")
    print(f"Projection Standard: UTM Meter-Accurate Buffering")
    print(f"========================================================")

    # 1. Load Track Data
    track_path = args.input_track
    if track_path is None:
        track_path = os.path.join(OUTPUT_DIR, f"{storm_name.lower()}_track.geojson")

    if not os.path.exists(track_path):
        # Fallback to CSV
        csv_fallback = os.path.join(OUTPUT_DIR, f"{storm_name.lower()}_track.csv")
        if os.path.exists(csv_fallback):
            df = pd.read_csv(csv_fallback)
            geometry = [Point(xy) for xy in zip(df["lon"], df["lat"])]
            track_gdf = gpd.GeoDataFrame(df, geometry=geometry, crs="EPSG:4326")
        else:
            from track_input import load_cyclone_track
            track_gdf = load_cyclone_track(storm_name=storm_name)
    else:
        track_gdf = gpd.read_file(track_path)

    print(f"[+] Loaded Track Data: {len(track_gdf)} observations ({track_gdf['time'].min()} to {track_gdf['time'].max()})")
    print(f"[+] Peak Sustained Wind: {track_gdf['wind_kts'].max():.1f} kts ({track_gdf['wind_kts'].max()*1.852:.1f} km/h)")

    # 2. Generate Swaths
    swaths_gdf, segments_gdf = generate_wind_swaths(track_gdf, storm_name=storm_name, step_meters=args.step_km * 1000.0)

    # 3. Export Swaths & Segments GeoJSON
    out_swaths_geojson = os.path.join(OUTPUT_DIR, f"{storm_name.lower()}_wind_swaths.geojson")
    out_swaths_generic = os.path.join(OUTPUT_DIR, "wind_swaths.geojson")
    out_segments_geojson = os.path.join(OUTPUT_DIR, f"{storm_name.lower()}_wind_segments.geojson")

    swaths_gdf.to_file(out_swaths_geojson, driver="GeoJSON")
    swaths_gdf.to_file(out_swaths_generic, driver="GeoJSON")
    segments_gdf.to_file(out_segments_geojson, driver="GeoJSON")

    # 4. Export Summary Table
    summary_df = generate_swaths_summary(swaths_gdf, track_gdf)
    summary_csv = os.path.join(OUTPUT_DIR, f"{storm_name.lower()}_wind_swaths_summary.csv")
    summary_df.to_csv(summary_csv, index=False)

    print(f"\n[+] Generated Wind Hazard Swaths Summary:")
    print("-" * 80)
    for _, r in summary_df.iterrows():
        print(f"[*] {r['Hazard Zone']} [{r['Threat Level']}]:")
        print(f"    Threshold: {r['Wind Threshold (kts)']} ({r['Wind Threshold (km/h)']}) | Peak Scaled Radius: {r['Peak Scaled Radius (km)']}")
        print(f"    Total Geographic Impact Area: {r['Total Swath Area (sq km)']} sq km")
        print(f"    Protocol: {r['Recommended Action']}")
    print("-" * 80)

    # 5. Generate Interactive Folium Map
    html_map = plot_wind_swaths_map(track_gdf, swaths_gdf, storm_name=storm_name)

    # 6. Generate Static Multi-Panel Figure
    png_plot = plot_wind_swaths_static(track_gdf, swaths_gdf, storm_name=storm_name)

    # 7. Sync to mirror directory
    sync_to_mirror()

    print(f"\n[+] CHAPTER 2 ARTIFACTS CREATED SUCCESSFULLY:")
    print(f"    1. Unified GeoJSON:     {out_swaths_geojson}")
    print(f"    2. Generic GeoJSON:     {out_swaths_generic}")
    print(f"    3. Segment GeoJSON:     {out_segments_geojson}")
    print(f"    4. Summary CSV:         {summary_csv}")
    print(f"    5. Interactive Map:     {html_map}")
    print(f"    6. Publication Figure:  {png_plot}")
    print(f"========================================================\n")
