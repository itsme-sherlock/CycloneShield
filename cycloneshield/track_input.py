"""
CycloneShield - Track Input Module (Step 1)
Fetches and standardizes cyclone tracks from NOAA IBTrACS v4 North Indian Ocean dataset.
Outputs clean track DataFrame [time, lat, lon, wind_kts, pressure_mb] and GeoDataFrame.
"""

import os
import urllib.request
import pandas as pd
import numpy as np
import geopandas as gpd
from shapely.geometry import Point, LineString
import folium
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Default data paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

IBTRACS_NI_URL = "https://www.ncei.noaa.gov/data/international-best-track-archive-for-climate-stewardship-ibtracs/v04r01/access/csv/ibtracs.NI.list.v04r01.csv"
LOCAL_CSV_PATH = os.path.join(DATA_DIR, "ibtracs_ni.csv")


def ensure_ibtracs_data(url: str = IBTRACS_NI_URL, dest_path: str = LOCAL_CSV_PATH) -> str:
    """Download NOAA IBTrACS North Indian Ocean CSV if not cached locally."""
    if not os.path.exists(dest_path) or os.path.getsize(dest_path) < 1000000:
        print(f"[CycloneShield] Downloading IBTrACS NI dataset from {url}...")
        headers = {"User-Agent": "Mozilla/5.0"}
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as resp, open(dest_path, "wb") as out_file:
            out_file.write(resp.read())
        print(f"[CycloneShield] Download complete: {dest_path} ({os.path.getsize(dest_path):,} bytes)")
    else:
        print(f"[CycloneShield] Using cached IBTrACS dataset at {dest_path}")
    return dest_path


def get_wind_category(wind_kts: float) -> str:
    """Classify storm category based on IMD / Saffir-Simpson intensity scale."""
    if pd.isna(wind_kts):
        return "Unknown"
    if wind_kts < 28:
        return "Depression (<28 kts)"
    elif wind_kts < 34:
        return "Deep Depression (28-33 kts)"
    elif wind_kts < 48:
        return "Cyclonic Storm (34-47 kts)"
    elif wind_kts < 64:
        return "Severe Cyclonic Storm (48-63 kts)"
    elif wind_kts < 90:
        return "Very Severe Cyclonic Storm (64-89 kts)"
    elif wind_kts < 120:
        return "Extremely Severe Cyclonic Storm (90-119 kts)"
    else:
        return "Super Cyclonic Storm (>=120 kts)"


def get_wind_color(wind_kts: float) -> str:
    """Color palette for cyclone wind intensity."""
    if pd.isna(wind_kts) or wind_kts < 28:
        return "#3b82f6"  # Blue (Depression)
    elif wind_kts < 34:
        return "#06b6d4"  # Cyan (Deep Depression)
    elif wind_kts < 48:
        return "#10b981"  # Green (Cyclonic Storm)
    elif wind_kts < 64:
        return "#f59e0b"  # Amber (Severe Cyclonic Storm)
    elif wind_kts < 90:
        return "#f97316"  # Orange (Very Severe)
    elif wind_kts < 120:
        return "#ef4444"  # Red (Extremely Severe)
    else:
        return "#9333ea"  # Purple (Super Cyclonic)


def load_cyclone_track(storm_name: str = "REMAL", season: int = None, csv_path: str = LOCAL_CSV_PATH) -> gpd.GeoDataFrame:
    """
    Load and filter IBTrACS data for a specific cyclone.
    Returns a GeoDataFrame with columns: [time, lat, lon, wind_kts, pressure_mb, geometry, category]
    """
    ensure_ibtracs_data(dest_path=csv_path)

    # Read IBTrACS CSV, skipping line 1 (units)
    df = pd.read_csv(csv_path, skiprows=[1], low_memory=False)

    # Clean storm name and season
    df["NAME"] = df["NAME"].astype(str).str.strip().str.upper()
    target_name = storm_name.strip().upper()

    mask = df["NAME"] == target_name
    if season is not None:
        df["SEASON"] = pd.to_numeric(df["SEASON"], errors="coerce")
        mask = mask & (df["SEASON"] == season)

    storm_df = df[mask].copy()

    if len(storm_df) == 0:
        available = df[df["SEASON"] >= 2022]["NAME"].unique().tolist()
        available = [n for n in available if n != "UNNAMED"]
        raise ValueError(f"Cyclone '{storm_name}' not found. Recent named storms include: {available}")

    # Standardize timestamp
    storm_df["time"] = pd.to_datetime(storm_df["ISO_TIME"])
    storm_df = storm_df.sort_values("time").reset_index(drop=True)

    # Convert coordinates
    storm_df["lat"] = pd.to_numeric(storm_df["LAT"], errors="coerce")
    storm_df["lon"] = pd.to_numeric(storm_df["LON"], errors="coerce")

    # Wind speed in knots (combine USA_WIND and WMO_WIND, take max if both exist, interpolate missing)
    usa_w = pd.to_numeric(storm_df["USA_WIND"], errors="coerce").astype(float)
    wmo_w = pd.to_numeric(storm_df["WMO_WIND"], errors="coerce").astype(float)
    combined_wind = usa_w.combine_first(wmo_w)
    both_mask = usa_w.notna() & wmo_w.notna()
    combined_wind.loc[both_mask] = np.maximum(usa_w[both_mask], wmo_w[both_mask])
    storm_df["wind_kts"] = combined_wind.interpolate(method="linear").bfill().ffill()

    # Pressure in mb (combine WMO_PRES and USA_PRES, take min if both exist, interpolate missing)
    usa_p = pd.to_numeric(storm_df["USA_PRES"], errors="coerce").astype(float)
    wmo_p = pd.to_numeric(storm_df["WMO_PRES"], errors="coerce").astype(float)
    combined_pres = wmo_p.combine_first(usa_p)
    both_p_mask = usa_p.notna() & wmo_p.notna()
    combined_pres.loc[both_p_mask] = np.minimum(usa_p[both_p_mask], wmo_p[both_p_mask])
    storm_df["pressure_mb"] = combined_pres.interpolate(method="linear").bfill().ffill()

    # Select core columns
    clean_cols = ["time", "lat", "lon", "wind_kts", "pressure_mb"]
    clean_df = storm_df[clean_cols].dropna(subset=["lat", "lon"]).copy()

    # Categorize
    clean_df["category"] = clean_df["wind_kts"].apply(get_wind_category)

    # Build geometry
    geometry = [Point(xy) for xy in zip(clean_df["lon"], clean_df["lat"])]
    gdf = gpd.GeoDataFrame(clean_df, geometry=geometry, crs="EPSG:4326")

    return gdf


def plot_track(gdf: gpd.GeoDataFrame, storm_name: str, output_html: str = None, output_png: str = None):
    """Generate both an interactive Folium HTML map and a static high-res Matplotlib figure."""
    if output_html is None:
        output_html = os.path.join(OUTPUT_DIR, f"{storm_name.lower()}_track_map.html")
    if output_png is None:
        output_png = os.path.join(OUTPUT_DIR, f"{storm_name.lower()}_track_plot.png")

    center_lat = gdf["lat"].mean()
    center_lon = gdf["lon"].mean()

    # 1. Interactive Folium Map
    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=6,
        tiles="OpenStreetMap",
        name="OpenStreetMap Standard"
    )

    # Add alternate satellite tile layer
    folium.TileLayer(
        tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
        attr="Esri World Imagery",
        name="Satellite Hybrid"
    ).add_to(m)

    # Draw track polyline with color gradient
    coordinates = list(zip(gdf["lat"], gdf["lon"]))
    folium.PolyLine(
        locations=coordinates,
        color="#38bdf8",
        weight=4,
        opacity=0.8,
        tooltip=f"Cyclone {storm_name} Track Path"
    ).add_to(m)

    # Highlight peak intensity point
    peak_idx = gdf["wind_kts"].idxmax()
    peak_row = gdf.loc[peak_idx]

    # Add circles for each track point
    for idx, row in gdf.iterrows():
        is_peak = (idx == peak_idx)
        color = get_wind_color(row["wind_kts"])
        radius = 8 if is_peak else 5

        popup_html = f"""
        <div style="font-family: Arial, sans-serif; font-size: 13px; min-width: 200px;">
            <b style="color: {color}; font-size: 14px;">Cyclone {storm_name}</b><br/>
            <b>Time:</b> {row['time'].strftime('%Y-%m-%d %H:%M UTC')}<br/>
            <b>Intensity:</b> {row['category']}<br/>
            <b>Wind:</b> {row['wind_kts']:.1f} kts ({row['wind_kts']*1.852:.1f} km/h)<br/>
            <b>Central Pressure:</b> {row['pressure_mb']:.1f} mb<br/>
            <b>Location:</b> {row['lat']:.2f}°N, {row['lon']:.2f}°E
            {'<br/><b style=\"color: #ef4444;\">★ PEAK INTENSITY</b>' if is_peak else ''}
        </div>
        """

        folium.CircleMarker(
            location=[row["lat"], row["lon"]],
            radius=radius,
            color="#ffffff" if is_peak else color,
            weight=2 if is_peak else 1,
            fill=True,
            fill_color=color,
            fill_opacity=0.9,
            popup=folium.Popup(popup_html, max_width=300),
            tooltip=f"{row['time'].strftime('%b %d %H:%M')} | {row['wind_kts']:.0f} kts | {row['category']}"
        ).add_to(m)

    # Add Landfall marker (last point or point with highest latitude in Bay of Bengal)
    landfall_row = gdf.iloc[-1]
    folium.Marker(
        location=[landfall_row["lat"], landfall_row["lon"]],
        icon=folium.Icon(color="red", icon="flag"),
        tooltip=f"Dissipation / Inland: {landfall_row['time'].strftime('%b %d %H:%M')}"
    ).add_to(m)

    folium.LayerControl().add_to(m)
    m.save(output_html)
    print(f"[CycloneShield] Interactive Folium map saved to: {output_html}")

    # 2. Static Matplotlib Multi-Panel Figure
    fig = plt.figure(figsize=(14, 6), facecolor="#0f172a")

    # Subplot 1: Map Track
    ax1 = fig.add_subplot(1, 2, 1, facecolor="#1e293b")
    ax1.plot(gdf["lon"], gdf["lat"], color="#94a3b8", linestyle="--", linewidth=1.5, zorder=1)
    scatter = ax1.scatter(
        gdf["lon"], gdf["lat"],
        c=gdf["wind_kts"],
        cmap="YlOrRd",
        s=gdf["wind_kts"] * 1.5,
        edgecolors="white",
        linewidth=0.8,
        zorder=2
    )
    cbar = plt.colorbar(scatter, ax=ax1, pad=0.02)
    cbar.set_label("Wind Speed (Knots)", color="#f8fafc", fontsize=10)
    cbar.ax.yaxis.set_tick_params(color="#94a3b8")
    plt.setp(plt.getp(cbar.ax.axes, "yticklabels"), color="#f8fafc")

    # Annotate start, peak, end
    start_row = gdf.iloc[0]
    ax1.annotate("Start", (start_row["lon"], start_row["lat"]), color="#38bdf8",
                 fontsize=9, fontweight="bold", textcoords="offset points", xytext=(8, -8))
    ax1.annotate(f"Peak ({peak_row['wind_kts']:.0f} kts)", (peak_row["lon"], peak_row["lat"]),
                 color="#ef4444", fontsize=10, fontweight="bold", textcoords="offset points", xytext=(8, 8))
    ax1.annotate("Landfall", (landfall_row["lon"], landfall_row["lat"]), color="#fbbf24",
                 fontsize=9, fontweight="bold", textcoords="offset points", xytext=(8, -8))

    ax1.set_title(f"Cyclone {storm_name} - Track Path (Bay of Bengal)", color="#f8fafc", fontsize=12, fontweight="bold", pad=10)
    ax1.set_xlabel("Longitude (°E)", color="#94a3b8", fontsize=10)
    ax1.set_ylabel("Latitude (°N)", color="#94a3b8", fontsize=10)
    ax1.tick_params(colors="#94a3b8")
    ax1.grid(color="#334155", linestyle=":", linewidth=0.7)

    # Subplot 2: Wind & Pressure Profile
    ax2 = fig.add_subplot(1, 2, 2, facecolor="#1e293b")
    line1 = ax2.plot(gdf["time"], gdf["wind_kts"], color="#f97316", linewidth=2.5, marker="o", markersize=4, label="Wind (kts)")
    ax2.set_xlabel("Time (UTC)", color="#94a3b8", fontsize=10)
    ax2.set_ylabel("Max Sustained Wind (Knots)", color="#f97316", fontsize=10)
    ax2.tick_params(axis="y", labelcolor="#f97316", colors="#94a3b8")
    ax2.tick_params(axis="x", colors="#94a3b8")
    ax2.xaxis.set_major_formatter(mdates.DateFormatter("%b %d\n%H:%M"))

    ax2_twin = ax2.twinx()
    line2 = ax2_twin.plot(gdf["time"], gdf["pressure_mb"], color="#38bdf8", linewidth=2, linestyle="--", marker="s", markersize=3, label="Pressure (mb)")
    ax2_twin.set_ylabel("Central Pressure (mb)", color="#38bdf8", fontsize=10)
    ax2_twin.tick_params(axis="y", labelcolor="#38bdf8", colors="#94a3b8")
    ax2_twin.invert_yaxis()  # Lower pressure = higher intensity

    lines = line1 + line2
    labels = [l.get_label() for l in lines]
    ax2.legend(lines, labels, loc="upper right", facecolor="#0f172a", edgecolor="#475569", labelcolor="#f8fafc")

    ax2.set_title(f"Intensity Timeline (Peak: {peak_row['wind_kts']:.0f} kts / {peak_row['pressure_mb']:.0f} mb)", color="#f8fafc", fontsize=12, fontweight="bold", pad=10)
    ax2.grid(color="#334155", linestyle=":", linewidth=0.7)

    plt.tight_layout()
    plt.savefig(output_png, dpi=200, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close()
    print(f"[CycloneShield] Static plot saved to: {output_png}")

    return output_html, output_png


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="CycloneShield Step 1: Track Input Module")
    parser.add_argument("--cyclone", type=str, default="REMAL", help="Storm name (e.g. REMAL, DANA, MICHAUNG)")
    parser.add_argument("--season", type=int, default=None, help="Season/Year (optional)")
    args = parser.parse_args()

    print(f"\n==========================================")
    print(f"CycloneShield - STEP 1: TRACK INPUT")
    print(f"Target Cyclone: {args.cyclone}")
    print(f"==========================================")

    gdf = load_cyclone_track(storm_name=args.cyclone, season=args.season)

    # Save to outputs
    csv_out = os.path.join(OUTPUT_DIR, f"{args.cyclone.lower()}_track.csv")
    geojson_out = os.path.join(OUTPUT_DIR, f"{args.cyclone.lower()}_track.geojson")
    
    # Save standard track_df with columns: [time, lat, lon, wind_kts, pressure_mb]
    track_df = gdf[["time", "lat", "lon", "wind_kts", "pressure_mb"]]
    track_df.to_csv(csv_out, index=False)
    gdf.to_file(geojson_out, driver="GeoJSON")

    print(f"\n[+] Extracted Track Data ({len(track_df)} synoptic observations):")
    print("-" * 70)
    print(track_df.head(6).to_string())
    print("...")
    print(track_df.tail(4).to_string())
    print("-" * 70)
    print(f"Time Range: {track_df['time'].min()} to {track_df['time'].max()}")
    print(f"Peak Wind: {track_df['wind_kts'].max():.1f} kts ({track_df['wind_kts'].max()*1.852:.1f} km/h)")
    print(f"Min Central Pressure: {track_df['pressure_mb'].min():.1f} mb")
    print(f"Exported CSV: {csv_out}")
    print(f"Exported GeoJSON: {geojson_out}")

    # Generate Map and Plot
    html_map, png_plot = plot_track(gdf, storm_name=args.cyclone)
    print(f"\n[+] Step 1 completed successfully for Cyclone {args.cyclone}!\n")
