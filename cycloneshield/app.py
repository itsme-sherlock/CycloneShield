"""
CycloneShield - Interactive Geospatial & AI Advisory Dashboard (Chapter 7)
==========================================================================
Streamlit-based Emergency Management Command Center for Tropical Cyclones.
Integrates Chapters 1-6 outputs into an operational, executive dashboard:
  - Track & synoptic intensity timeline (NOAA IBTrACS)
  - Dynamic wind swath buffers (Core, Moderate, Outer)
  - Coastal bathtub storm surge inundation (SRTM 30m DEM)
  - Multi-hazard infrastructure exposure (hospitals, shelters, power, severed highways)
  - Explainable AI (XAI) district vulnerability ranking (0-100)
  - Google Gemini multilingual emergency advisories & simulated NDRF dispatch logs

Google Ecosystem Integration:
  - Google Material Design 3 theme with Outfit typography
  - Google Maps & Google Earth Engine basemap styles
  - Google Gemini API (gemini-2.5-flash / gemini-1.5-flash) live re-generation
"""

import os
import sys
import json
import base64
from typing import Dict, Any, List, Optional

import streamlit as st
import streamlit.components.v1 as components
import pandas as pd

# Base directories
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")
DATA_DIR = os.path.join(BASE_DIR, "data")

# Add BASE_DIR to sys.path to ensure local imports succeed
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

try:
    from gemini_advisory import call_gemini_api, get_calibrated_offline_advisories
except ImportError:
    call_gemini_api = None
    get_calibrated_offline_advisories = None

# Streamlit Page Configuration
st.set_page_config(
    page_title="CycloneShield | AI Disaster Command Center",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================================================================
# 1. Custom CSS & Google Material 3 Design
# ==============================================================================

CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Outfit', sans-serif;
}

/* Background & Main Container */
.stApp {
    background-color: #0b1120;
    color: #f1f5f9;
}

/* Header Container */
.header-box {
    background: linear-gradient(135deg, rgba(15, 23, 42, 0.9) 0%, rgba(30, 41, 59, 0.85) 100%);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(56, 189, 248, 0.25);
    border-radius: 14px;
    padding: 20px 24px;
    margin-bottom: 20px;
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
}

.title-text {
    font-size: 28px;
    font-weight: 800;
    background: linear-gradient(90deg, #38bdf8 0%, #818cf8 50%, #c084fc 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0;
    letter-spacing: -0.5px;
}

.subtitle-text {
    font-size: 13.5px;
    color: #94a3b8;
    margin-top: 4px;
}

/* KPI Metric Cards */
.kpi-card {
    background: rgba(30, 41, 59, 0.7);
    backdrop-filter: blur(8px);
    border: 1px solid rgba(148, 163, 184, 0.15);
    border-radius: 12px;
    padding: 14px 18px;
    transition: transform 0.2s ease, border-color 0.2s ease;
}
.kpi-card:hover {
    transform: translateY(-2px);
    border-color: rgba(56, 189, 248, 0.4);
}
.kpi-label {
    font-size: 11px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    color: #94a3b8;
}
.kpi-value {
    font-size: 22px;
    font-weight: 700;
    color: #f8fafc;
    margin-top: 2px;
}
.kpi-sub {
    font-size: 11px;
    color: #38bdf8;
    margin-top: 2px;
}

/* Threat Badges */
.badge-critical {
    background: rgba(239, 68, 68, 0.2);
    color: #ef4444;
    border: 1px solid #ef4444;
    padding: 3px 8px;
    border-radius: 6px;
    font-size: 12px;
    font-weight: 700;
}
.badge-high {
    background: rgba(249, 115, 22, 0.2);
    color: #f97316;
    border: 1px solid #f97316;
    padding: 3px 8px;
    border-radius: 6px;
    font-size: 12px;
    font-weight: 700;
}
.badge-moderate {
    background: rgba(245, 158, 11, 0.2);
    color: #f59e0b;
    border: 1px solid #f59e0b;
    padding: 3px 8px;
    border-radius: 6px;
    font-size: 12px;
    font-weight: 700;
}
.badge-low {
    background: rgba(59, 130, 246, 0.2);
    color: #3b82f6;
    border: 1px solid #3b82f6;
    padding: 3px 8px;
    border-radius: 6px;
    font-size: 12px;
    font-weight: 700;
}

/* Glass Cards */
.glass-panel {
    background: rgba(30, 41, 59, 0.65);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(148, 163, 184, 0.15);
    border-radius: 12px;
    padding: 18px;
    margin-bottom: 16px;
}

/* Dispatch Table */
.dispatch-item {
    background: rgba(15, 23, 42, 0.6);
    border-left: 3px solid #38bdf8;
    border-radius: 6px;
    padding: 10px 14px;
    margin-bottom: 8px;
}
.dispatch-crit {
    border-left-color: #ef4444 !important;
}
.dispatch-high {
    border-left-color: #f97316 !important;
}

/* Custom Scrollbars */
::-webkit-scrollbar {
    width: 6px;
    height: 6px;
}
::-webkit-scrollbar-track {
    background: #0b1120;
}
::-webkit-scrollbar-thumb {
    background: #334155;
    border-radius: 3px;
}
::-webkit-scrollbar-thumb:hover {
    background: #475569;
}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


# ==============================================================================
# 2. Data Loading Helpers
# ==============================================================================

@st.cache_data
def load_vulnerability_data():
    """Loads Chapter 5 vulnerability ranking scores and metadata."""
    csv_path = os.path.join(OUTPUT_DIR, "remal_vulnerability_scores.csv")
    json_path = os.path.join(OUTPUT_DIR, "remal_vulnerability_scores.json")
    
    df = pd.DataFrame()
    records = []
    
    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
    if os.path.exists(json_path):
        with open(json_path, "r", encoding="utf-8") as f:
            records = json.load(f)
            
    return df, records


@st.cache_data
def load_advisories_data():
    """Loads Chapter 6 Gemini emergency disaster advisories."""
    json_path = os.path.join(OUTPUT_DIR, "remal_advisories.json")
    if not os.path.exists(json_path):
        json_path = os.path.join(OUTPUT_DIR, "advisories.json")
        
    advisories = []
    if os.path.exists(json_path):
        with open(json_path, "r", encoding="utf-8") as f:
            advisories = json.load(f)
            
    return advisories


@st.cache_data
def load_exposure_data():
    """Loads Chapter 4 facility exposure records."""
    json_path = os.path.join(OUTPUT_DIR, "remal_district_exposure.json")
    data = []
    if os.path.exists(json_path):
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    return {d["district_name"]: d for d in data}


@st.cache_data
def load_map_html(filename: str) -> Optional[str]:
    """Loads pre-generated interactive Folium maps from outputs directory."""
    path = os.path.join(OUTPUT_DIR, filename)
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    return None


# Load Core State Data
vuln_df, vuln_records = load_vulnerability_data()
advisories_list = load_advisories_data()
exposure_dict = load_exposure_data()
advisory_by_district = {a["district_name"]: a for a in advisories_list}


# ==============================================================================
# 3. Header KPI Ribbon
# ==============================================================================

st.markdown("""
<div class="header-box">
    <div style="display:flex; justify-content:space-between; align-items:flex-start;">
        <div>
            <div style="display:flex; align-items:center; gap:10px;">
                <span style="font-size:26px;">🛡️</span>
                <h1 class="title-text">CycloneShield</h1>
                <span style="background:rgba(56,189,248,0.15); color:#38bdf8; border:1px solid rgba(56,189,248,0.3); font-size:11px; font-weight:700; padding:2px 8px; border-radius:12px;">DEV-FEST DEMO</span>
            </div>
            <div class="subtitle-text">
                Track-Based Cyclone Impact & Infrastructure Vulnerability Forecaster • Powered by Google Earth Engine & Google Gemini API
            </div>
        </div>
        <div style="text-align:right;">
            <div style="font-size:11px; color:#94a3b8; font-weight:600;">ACTIVE EVENT</div>
            <div style="font-size:16px; font-weight:700; color:#ef4444; display:flex; align-items:center; gap:6px; justify-content:flex-end;">
                <span style="width:8px; height:8px; border-radius:50%; background:#ef4444; box-shadow:0 0 8px #ef4444;"></span>
                CYCLONE REMAL (MAY 2024)
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# 6 Strategic KPI Metrics
kpi_cols = st.columns(6)

with kpi_cols[0]:
    st.markdown("""
    <div class="kpi-card">
        <div class="kpi-label">Storm Intensity</div>
        <div class="kpi-value" style="color:#ef4444;">60 kts</div>
        <div class="kpi-sub">Cat 1 / Severe Cyclonic</div>
    </div>
    """, unsafe_allow_html=True)

with kpi_cols[1]:
    st.markdown("""
    <div class="kpi-card">
        <div class="kpi-label">Central Pressure</div>
        <div class="kpi-value">977 mb</div>
        <div class="kpi-sub">Eye Wall Landfall</div>
    </div>
    """, unsafe_allow_html=True)

with kpi_cols[2]:
    st.markdown("""
    <div class="kpi-card">
        <div class="kpi-label">Peak Surge (DEM)</div>
        <div class="kpi-value" style="color:#38bdf8;">3.56 m</div>
        <div class="kpi-sub">GEE SRTM Elevation</div>
    </div>
    """, unsafe_allow_html=True)

with kpi_cols[3]:
    st.markdown("""
    <div class="kpi-card">
        <div class="kpi-label">Submerged Highways</div>
        <div class="kpi-value" style="color:#f97316;">39.6 km</div>
        <div class="kpi-sub">SH-3 & R760 Arteries</div>
    </div>
    """, unsafe_allow_html=True)

with kpi_cols[4]:
    st.markdown("""
    <div class="kpi-card">
        <div class="kpi-label">Flooded Lifelines</div>
        <div class="kpi-value" style="color:#ef4444;">5 Hosp / 6 Shlt</div>
        <div class="kpi-sub">Sundarbans Estuary</div>
    </div>
    """, unsafe_allow_html=True)

with kpi_cols[5]:
    st.markdown("""
    <div class="kpi-card">
        <div class="kpi-label">Priority 1 Districts</div>
        <div class="kpi-value" style="color:#ef4444;">2 Districts</div>
        <div class="kpi-sub">S 24 Parganas & Satkhira</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)


# ==============================================================================
# 4. Main Two-Column Layout (Geospatial Viewport + District AI Inspector)
# ==============================================================================

left_col, right_col = st.columns([1.55, 1.0], gap="medium")

# ------------------------------------------------------------------------------
# Left Column: Interactive Multi-Hazard Geospatial Viewer
# ------------------------------------------------------------------------------
with left_col:
    st.markdown("""
    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
        <div style="font-size:16px; font-weight:700; color:#38bdf8; display:flex; align-items:center; gap:8px;">
            <span>🗺️</span> Multi-Hazard Geospatial Intelligence Viewport
        </div>
        <div style="font-size:12px; color:#94a3b8;">Google Maps & Satellite Hybrid Basemaps</div>
    </div>
    """, unsafe_allow_html=True)

    # Layer View Selector
    map_options = {
        "Chapter 5: Vulnerability Choropleth & Lifelines": "remal_vulnerability_map.html",
        "Chapter 4: Infrastructure Exposure & Severed Roads": "remal_infrastructure_map.html",
        "Chapter 3: Storm Surge Inundation & Precipitation": "remal_surge_rainfall_map.html",
        "Chapter 2: Dynamic Wind Swaths (Core/Mod/Outer)": "remal_wind_swaths_map.html",
        "Chapter 1: Cyclone Track & Pressure Timeline": "remal_track_map.html"
    }

    selected_map_label = st.selectbox(
        "Select Hazard View / Cartographic Layer:",
        options=list(map_options.keys()),
        index=0,
        label_visibility="collapsed"
    )

    selected_map_file = map_options[selected_map_label]
    map_html = load_map_html(selected_map_file)

    if map_html:
        components.html(map_html, height=580, scrolling=False)
    else:
        st.warning(f"Map file `{selected_map_file}` not found in outputs directory.")

    # Geospatial Quick Telemetry
    st.markdown("""
    <div style="display:flex; justify-content:space-between; font-size:11.5px; color:#94a3b8; background:rgba(30,41,59,0.5); padding:8px 12px; border-radius:8px; margin-top:6px;">
        <div>📡 <b>Projection</b>: UTM 45N (EPSG:32645) & WGS84</div>
        <div>🛰️ <b>DEM Source</b>: USGS/NASA SRTM 30m via GEE</div>
        <div>🌪️ <b>Track Data</b>: NOAA IBTrACS v4 North Indian Ocean</div>
    </div>
    """, unsafe_allow_html=True)


# ------------------------------------------------------------------------------
# Right Column: District Deep-Dive Inspector & Gemini AI Advisory Card
# ------------------------------------------------------------------------------
with right_col:
    st.markdown("""
    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
        <div style="font-size:16px; font-weight:700; color:#38bdf8; display:flex; align-items:center; gap:8px;">
            <span>🤖</span> District AI Inspector & Tactical Directives
        </div>
        <div style="font-size:12px; color:#94a3b8;">Google Gemini 2.5 Flash</div>
    </div>
    """, unsafe_allow_html=True)

    # District Selector Dropdown
    district_names = vuln_df["district_name"].tolist() if not vuln_df.empty else [
        "South 24 Parganas", "Satkhira", "North 24 Parganas", "Khulna", "Bagerhat",
        "Purba Medinipur", "Patuakhali", "Barguna", "Kolkata", "Howrah"
    ]

    selected_district = st.selectbox(
        "Select Coastal District for Operational Briefing:",
        options=district_names,
        index=0
    )

    # Fetch district stats
    dist_row = vuln_df[vuln_df["district_name"] == selected_district].iloc[0] if not vuln_df.empty else {}
    adv_data = advisory_by_district.get(selected_district, {})
    exp_data = exposure_dict.get(selected_district, {})

    score = dist_row.get("vulnerability_score", adv_data.get("vulnerability_score", 0.0))
    tier = dist_row.get("threat_tier", adv_data.get("threat_level", "LOW"))
    prio = dist_row.get("evacuation_priority", adv_data.get("evacuation_priority", 5))
    driver = dist_row.get("primary_risk_driver", adv_data.get("primary_risk_driver", "General Hazard"))
    state = dist_row.get("state_or_division", adv_data.get("state_or_division", ""))
    country = dist_row.get("country", adv_data.get("country", ""))

    badge_class = "badge-critical" if tier == "CRITICAL" else ("badge-high" if tier == "HIGH" else ("badge-moderate" if tier == "MODERATE" else "badge-low"))

    # District Score Card Header
    st.markdown(f"""
    <div class="glass-panel" style="border-left: 4px solid {'#ef4444' if tier=='CRITICAL' else ('#f97316' if tier=='HIGH' else '#38bdf8')}; padding:14px 18px;">
        <div style="display:flex; justify-content:space-between; align-items:center;">
            <div>
                <h3 style="margin:0; font-size:20px; font-weight:700; color:#f8fafc;">{selected_district}</h3>
                <div style="font-size:12px; color:#94a3b8;">{state}, {country}</div>
            </div>
            <div style="text-align:right;">
                <span class="{badge_class}">{tier} RISK</span>
                <div style="font-size:18px; font-weight:800; color:#f8fafc; margin-top:4px;">{score:.1f} <span style="font-size:11px; color:#94a3b8;">/ 100</span></div>
            </div>
        </div>
        <div style="font-size:11.5px; color:#cbd5e1; margin-top:10px; border-top:1px solid rgba(148,163,184,0.15); padding-top:8px;">
            ⚠️ <b>Primary Risk Driver</b>: {driver}<br>
            🚨 <b>Evacuation Directive</b>: Priority {prio} ({'Immediate Evacuation & Airlift' if prio==1 else ('Pre-position NDRF & Clear Roads' if prio==2 else 'Active Watch')})
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Lifeline Metrics Grid
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        fh = dist_row.get("flooded_hospitals", exp_data.get("hospitals_surge_flooded", 0))
        th = dist_row.get("total_hospitals", exp_data.get("total_hospitals", 0))
        st.markdown(f"""
        <div style="background:rgba(15,23,42,0.6); padding:8px 10px; border-radius:8px; text-align:center;">
            <div style="font-size:10px; color:#94a3b8;">HOSPITALS</div>
            <div style="font-size:15px; font-weight:700; color:{'#ef4444' if fh>0 else '#10b981'};">{fh}/{th}</div>
            <div style="font-size:9.5px; color:#94a3b8;">{'Flooded' if fh>0 else 'Intact'}</div>
        </div>
        """, unsafe_allow_html=True)
    with m2:
        fs = dist_row.get("flooded_shelters", exp_data.get("shelters_surge_flooded", 0))
        ts = dist_row.get("total_shelters", exp_data.get("total_shelters", 0))
        st.markdown(f"""
        <div style="background:rgba(15,23,42,0.6); padding:8px 10px; border-radius:8px; text-align:center;">
            <div style="font-size:10px; color:#94a3b8;">SHELTERS</div>
            <div style="font-size:15px; font-weight:700; color:{'#ef4444' if fs>0 else '#10b981'};">{fs}/{ts}</div>
            <div style="font-size:9.5px; color:#94a3b8;">{'Flooded' if fs>0 else 'Operational'}</div>
        </div>
        """, unsafe_allow_html=True)
    with m3:
        sr = dist_row.get("submerged_road_km", exp_data.get("submerged_road_km", 0.0))
        st.markdown(f"""
        <div style="background:rgba(15,23,42,0.6); padding:8px 10px; border-radius:8px; text-align:center;">
            <div style="font-size:10px; color:#94a3b8;">ROAD CUT</div>
            <div style="font-size:15px; font-weight:700; color:{'#ef4444' if sr>0 else '#10b981'};">{sr:.1f} km</div>
            <div style="font-size:9.5px; color:#94a3b8;">{'Submerged' if sr>0 else 'Passable'}</div>
        </div>
        """, unsafe_allow_html=True)
    with m4:
        fp = dist_row.get("flooded_power_substations", exp_data.get("power_substations_surge_flooded", 0))
        st.markdown(f"""
        <div style="background:rgba(15,23,42,0.6); padding:8px 10px; border-radius:8px; text-align:center;">
            <div style="font-size:10px; color:#94a3b8;">POWER GRID</div>
            <div style="font-size:15px; font-weight:700; color:{'#ef4444' if fp>0 else '#10b981'};">{fp} Sub</div>
            <div style="font-size:9.5px; color:#94a3b8;">{'Outage Risk' if fp>0 else 'Stable'}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

    # Explainable AI (XAI) Attribution Breakdown
    st.markdown("<div style='font-size:12px; font-weight:600; color:#cbd5e1; margin-bottom:4px;'>XAI Risk Attribution Breakdown:</div>", unsafe_allow_html=True)
    h_pct = float(dist_row.get("attribution_healthcare_pct", 35.0))
    s_pct = float(dist_row.get("attribution_shelters_pct", 25.0))
    r_pct = float(dist_row.get("attribution_roads_pct", 25.0))
    p_pct = float(dist_row.get("attribution_power_pct", 15.0))

    xai_cols = st.columns(4)
    xai_cols[0].caption(f"🏥 Health: {h_pct:.1f}%")
    xai_cols[1].caption(f"🛡️ Shelter: {s_pct:.1f}%")
    xai_cols[2].caption(f"🛣️ Roads: {r_pct:.1f}%")
    xai_cols[3].caption(f"⚡ Power: {p_pct:.1f}%")

    # Tabs for Multilingual Broadcast Advisories & Tactical NDRF Dispatch Logs
    tab_adv, tab_dispatch, tab_live = st.tabs(["📢 Broadcast Advisories", "🚒 NDRF Dispatch Logs", "⚡ Live Gemini API"])

    with tab_adv:
        subtab_en, subtab_hi, subtab_bn = st.tabs(["🇬🇧 English", "🇮🇳 Hindi (हिंदी)", "🇧🇩 Bengali (বাংলা)"])
        
        with subtab_en:
            en_text = adv_data.get("public_advisory_en", "No advisory available.")
            st.info(en_text)
            
        with subtab_hi:
            hi_text = adv_data.get("advisory_hindi", "हिंदी परामर्श उपलब्ध नहीं है।")
            st.warning(hi_text)
            
        with subtab_bn:
            bn_text = adv_data.get("advisory_bengali", "বাংলা সতর্কবার্তা উপলব্ধ নেই।")
            st.error(bn_text)

    with tab_dispatch:
        dispatches = adv_data.get("ndrf_incident_dispatch_log", [])
        if dispatches:
            for item in dispatches:
                status = item.get("status", "MONITORING")
                stat_badge = "🔴 IMMEDIATE" if status == "IMMEDIATE_EXECUTION" else ("🟠 STAGED" if status == "STAGED_STANDBY" else "🔵 MONITORING")
                st.markdown(f"""
                <div class="dispatch-item {'dispatch-crit' if status=='IMMEDIATE_EXECUTION' else ('dispatch-high' if status=='STAGED_STANDBY' else '')}">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <span style="font-weight:700; color:#38bdf8; font-size:12px;">{item.get('log_id', 'LOG')} • {item.get('unit', 'Unit')}</span>
                        <span style="font-size:11px; font-weight:700;">{stat_badge}</span>
                    </div>
                    <div style="font-size:11.5px; color:#f1f5f9; margin-top:3px;"><b>Target</b>: {item.get('target_zone', 'N/A')}</div>
                    <div style="font-size:11.5px; color:#cbd5e1; margin-top:2px;"><b>Action</b>: {item.get('action', 'N/A')}</div>
                    <div style="font-size:10.5px; color:#94a3b8; margin-top:2px;">🛠️ {item.get('equipment', 'Standard kit')}</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.write("No active incident dispatch logs for this peripheral district.")

    with tab_live:
        st.markdown("<div style='font-size:12px; color:#94a3b8; margin-bottom:8px;'>Trigger a live call to Google Gemini 2.5 Flash with custom parameters:</div>", unsafe_allow_html=True)
        user_key = st.text_input("Google AI Studio API Key:", type="password", placeholder="AIzaSy... (leave blank to use env)", key="gemini_key_input")
        model_choice = st.selectbox("Gemini Model:", ["gemini-2.5-flash", "gemini-1.5-flash"], index=0)
        temp_val = st.slider("Generation Temperature:", 0.0, 1.0, 0.2, 0.1)

        if st.button("🚀 Re-Generate with Google Gemini", use_container_width=True):
            resolved_key = user_key or os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
            if not resolved_key:
                st.error("No Gemini API key provided. Set GEMINI_API_KEY or enter your Google AI Studio key above.")
            else:
                with st.spinner(f"Querying Google Gemini ({model_choice}) for {selected_district}..."):
                    try:
                        # Construct real-time district prompt
                        single_prompt = f"""
                        You are NDRF Chief Operations AI. Generate an emergency disaster advisory JSON for:
                        District: {selected_district}, Vulnerability: {score:.1f}/100, Tier: {tier}, Priority: {prio}.
                        Lifelines: {dist_row.get('flooded_hospitals', 0)} flooded hospitals, {dist_row.get('submerged_road_km', 0.0):.1f} km severed highway.
                        Return a single JSON object with keys:
                        district_name, threat_level, evacuation_priority, lifeline_impact_summary,
                        public_advisory_en, advisory_hindi, advisory_bengali.
                        """
                        result = call_gemini_api(single_prompt, resolved_key, model_name=model_choice)
                        if result:
                            st.success("Successfully generated live response from Google Gemini API!")
                            st.json(result)
                        else:
                            st.error("Gemini call completed but returned empty or fallback payload.")
                    except Exception as ex:
                        st.error(f"Error querying Gemini: {ex}")


# ==============================================================================
# 5. Full District Vulnerability Ranking & Export Table
# ==============================================================================

st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

with st.expander("📊 Complete Multi-District Vulnerability & Exposure Comparative Table (All 10 Districts)", expanded=False):
    if not vuln_df.empty:
        display_cols = [
            "rank", "district_name", "state_or_division", "country", "vulnerability_score",
            "threat_tier", "evacuation_priority", "primary_risk_driver", "flooded_hospitals",
            "flooded_shelters", "submerged_road_km", "hazard_intensity_multiplier"
        ]
        available_cols = [c for c in display_cols if c in vuln_df.columns]
        table_df = vuln_df[available_cols].copy()
        
        st.dataframe(
            table_df,
            use_container_width=True,
            hide_index=True
        )
        
        csv_data = table_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Vulnerability Scores CSV",
            data=csv_data,
            file_name="cycloneshield_vulnerability_scores.csv",
            mime="text/csv"
        )
    else:
        st.write("Vulnerability scores table unavailable.")


# ==============================================================================
# 6. Google Hackathon Ecosystem Architecture Footer
# ==============================================================================

st.markdown("""
<div style="background:rgba(15,23,42,0.8); border:1px solid rgba(148,163,184,0.15); border-radius:12px; padding:16px 20px; margin-top:20px;">
    <div style="font-size:13.5px; font-weight:700; color:#38bdf8; margin-bottom:8px;">
        🏛️ Google Ecosystem Architecture (100% Free Tier Implementation)
    </div>
    <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap:12px; font-size:11.5px; color:#cbd5e1;">
        <div><b>1. Google Earth Engine (GEE)</b><br>USGS/NASA SRTM 30m Digital Elevation Model coastal bathtub contour extraction.</div>
        <div><b>2. Google Gemini 2.5 Flash</b><br>Multilingual life-saving disaster advisories (English, Hindi, Bengali) with structured JSON schema.</div>
        <div><b>3. NOAA & Google Public Datasets</b><br>Synoptic IBTrACS v4 central pressure deficit empirical surge modeling.</div>
        <div><b>4. Google Material Design 3</b><br>Glassmorphic interface, Outfit typography & responsive disaster ops color hierarchy.</div>
    </div>
</div>
""", unsafe_allow_html=True)
