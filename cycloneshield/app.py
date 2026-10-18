"""
CycloneShield - Interactive Geospatial & AI Disaster Command Center
====================================================================
Streamlit-based Emergency Management Command Center for Tropical Cyclones across India.
Designed for District Magistrates (DMs), SDMA duty officers, and NDRF commanders.

Key Capabilities:
  - Configured state and historical storm scenarios for decision-support demonstrations
  - User-supplied track files and optional connected bulletin/data-service integrations
  - Screening estimates for storm surge and district lifeline risks
  - Configured geospatial baselines and optional Earth Engine processing
  - Explicit, optional Gemini Vision image analysis with an offline benchmark fallback
  - Draft multilingual messages and CAP export for human review (not alert delivery)
  - Local scenario model trained on synthetic physics-inspired data
  - Optional BigQuery historical-track query and Cloud Run deployment blueprint
"""

import os
import sys
import json
import base64
import math
import datetime
import html as html_lib
from typing import Dict, Any, List, Optional, Tuple
from PIL import Image
import textwrap

import streamlit as st
import streamlit.components.v1 as components

def render_html(html_str: str):
    """Safely renders HTML without triggering Markdown indented code block parsing."""
    st.markdown(textwrap.dedent(html_str).strip(), unsafe_allow_html=True)

import pandas as pd
import numpy as np
import folium

# Base directories
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")
DATA_DIR = os.path.join(BASE_DIR, "data")
AUDIO_DIR = os.path.join(OUTPUT_DIR, "audio")
MODELS_DIR = os.path.join(OUTPUT_DIR, "models")

# Ensure BASE_DIR is in sys.path
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

# Safe API key resolution supporting st.secrets and local .env
def get_secret(key: str, default: Optional[str] = None) -> Optional[str]:
    """Retrieve secret from Streamlit secrets, OS environment, or .env files."""
    try:
        if hasattr(st, "secrets") and key in st.secrets:
            return str(st.secrets[key])
    except Exception:
        pass
    val = os.environ.get(key)
    if val:
        return val
    if key == "GEMINI_API_KEY":
        alt = os.environ.get("GOOGLE_API_KEY")
        if alt:
            return alt
        try:
            if hasattr(st, "secrets") and "GOOGLE_API_KEY" in st.secrets:
                return str(st.secrets["GOOGLE_API_KEY"])
        except Exception:
            pass
    return default

# Populate environment variable so subordinate modules read it
active_gemini_key = get_secret("GEMINI_API_KEY")
if active_gemini_key:
    os.environ["GEMINI_API_KEY"] = active_gemini_key

# Module imports with resilient fallbacks
from risk_engine import compute_district_risk, load_facilities

try:
    from gemini_advisory import (
        call_gemini_api,
        get_calibrated_offline_advisories,
        translate_advisory_text,
        export_cap_alert,
        get_resolved_api_key,
        get_localized_broadcast,
        parse_imd_bulletin_gemini,
        generate_whatif_tactical_playbook,
        generate_parametric_liquidity_audit,
        generate_compound_hazard_briefing
    )
except ImportError:
    call_gemini_api = None
    get_calibrated_offline_advisories = None
    translate_advisory_text = None
    export_cap_alert = None
    get_resolved_api_key = lambda: active_gemini_key
    get_localized_broadcast = None
    parse_imd_bulletin_gemini = None
    generate_whatif_tactical_playbook = None
    generate_parametric_liquidity_audit = None
    generate_compound_hazard_briefing = None

try:
    from multimodal_damage import (
        analyze_damage_image,
        load_sample_damage_images,
        DEFAULT_VISION_MODEL,
        FALLBACK_VISION_MODEL,
        SAMPLE_DIR
    )
except ImportError:
    analyze_damage_image = None
    load_sample_damage_images = None
    DEFAULT_VISION_MODEL = "gemini-3.8-flash"
    FALLBACK_VISION_MODEL = "gemini-3.5-flash-lite"
    SAMPLE_DIR = os.path.join(DATA_DIR, "sample_damage")

from geo_locate import (
    LocationResult,
    DISTRICTS_PATH,
    extract_exif_gps,
    list_districts,
    resolve_location,
)
from evidence_store import new_incident_id, save_incident
from alerts import publish_alert, should_alert

try:
    from voice_engine import (
        get_audio_path,
        get_or_create_district_audio,
        LANGUAGE_CONFIGS
    )
except ImportError:
    get_audio_path = None
    get_or_create_district_audio = None
    LANGUAGE_CONFIGS = {}

try:
    from predictive_model import (
        LifelineRiskPredictor,
        batch_predict_coastal_districts,
        EVAL_PLOT_PATH,
        VERTEX_MANIFEST_PATH,
        METRICS_JSON_PATH,
        FEATURE_NAMES,
        FEATURE_DESCRIPTIONS
    )
except ImportError:
    LifelineRiskPredictor = None
    batch_predict_coastal_districts = None
    EVAL_PLOT_PATH = os.path.join(MODELS_DIR, "lifeline_model_evaluation.png")
    VERTEX_MANIFEST_PATH = os.path.join(MODELS_DIR, "vertex_model_config.json")
    METRICS_JSON_PATH = os.path.join(MODELS_DIR, "model_metrics.json")
    FEATURE_NAMES = []
    FEATURE_DESCRIPTIONS = {}

try:
    from bigquery_pipeline import (
        BigQueryCyclonePipeline,
        get_bigquery_pipeline,
        DEFAULT_BQ_DATASET,
        DEFAULT_BQ_TABLE
    )
except ImportError:
    bigquery_pipeline = None
    get_bigquery_pipeline = None
    DEFAULT_BQ_DATASET = "bigquery-public-data.noaa_hurricanes"
    DEFAULT_BQ_TABLE = "bigquery-public-data.noaa_hurricanes.ibtracs_all"

try:
    from parametric_insurance import (
        evaluate_parametric_trigger,
        compute_district_parametric_matrix,
        get_aggregate_payout_summary,
        TRIGGER_TIERS,
        STATE_DEFAULT_SUM_INSURED_CR,
        SDRF_CORPUS_CR
    )
except ImportError:
    evaluate_parametric_trigger = None
    compute_district_parametric_matrix = None
    get_aggregate_payout_summary = None
    TRIGGER_TIERS = []
    STATE_DEFAULT_SUM_INSURED_CR = {}
    SDRF_CORPUS_CR = {}

try:
    from realtime_met import (
        fetch_landfall_forecast,
        fetch_marine_conditions,
        fetch_district_met_snapshot
    )
except ImportError:
    fetch_landfall_forecast = None
    fetch_marine_conditions = None
    fetch_district_met_snapshot = None

try:
    from imd_live_ingestion import (
        check_live_imd_rsmc_status,
        fetch_latest_imd_bulletin,
        parse_imd_bulletin_text,
        load_emerging_scenario,
        build_custom_approach_track,
        classify_imd_wind,
        EMERGING_SCENARIOS
    )
except ImportError:
    check_live_imd_rsmc_status = None
    fetch_latest_imd_bulletin = None
    parse_imd_bulletin_text = None
    load_emerging_scenario = None
    build_custom_approach_track = None
    classify_imd_wind = None
    EMERGING_SCENARIOS = {}

# Page configuration
st.set_page_config(
    page_title="CycloneShield | AI Disaster Operations Command",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling (Google Material Design 3 Dark Theme with WCAG AA compliance)
CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Outfit', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    font-size: 16px;
}

.stApp {
    background-color: #0b1120;
    color: #f1f5f9;
}

/* Executive Situation Card */
.situation-card {
    background: linear-gradient(135deg, rgba(15, 23, 42, 0.95) 0%, rgba(30, 41, 59, 0.90) 100%);
    border-left: 6px solid #ef4444;
    border-radius: 12px;
    padding: 20px 24px;
    margin-bottom: 20px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
    border-top: 1px solid rgba(239, 68, 68, 0.25);
    border-right: 1px solid rgba(56, 189, 248, 0.2);
    border-bottom: 1px solid rgba(56, 189, 248, 0.2);
}

.title-text {
    font-size: 26px;
    font-weight: 800;
    background: linear-gradient(90deg, #38bdf8 0%, #818cf8 50%, #c084fc 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0;
    letter-spacing: -0.5px;
}

/* Strategic KPI Metric Cards */
.kpi-card {
    background: rgba(30, 41, 59, 0.85);
    border: 1px solid rgba(148, 163, 184, 0.2);
    border-radius: 10px;
    padding: 14px 16px;
    transition: transform 0.15s ease, border-color 0.15s ease;
    height: 100%;
    cursor: help;
}
.kpi-card:hover {
    border-color: rgba(56, 189, 248, 0.5);
    transform: translateY(-2px);
}
.kpi-label {
    font-size: 12px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.6px;
    color: #cbd5e1;
}
.kpi-value {
    font-size: 24px;
    font-weight: 800;
    color: #f8fafc;
    margin-top: 4px;
}
.kpi-sub {
    font-size: 12px;
    color: #94a3b8;
    margin-top: 2px;
    line-height: 1.3;
}

/* Severity Badges (Color + Text + Icon) */
.badge-critical {
    background: rgba(239, 68, 68, 0.25);
    color: #fca5a5;
    border: 1.5px solid #ef4444;
    padding: 4px 10px;
    border-radius: 6px;
    font-size: 13px;
    font-weight: 800;
    display: inline-flex;
    align-items: center;
    gap: 6px;
}
.badge-high {
    background: rgba(249, 115, 22, 0.25);
    color: #fdba74;
    border: 1.5px solid #f97316;
    padding: 4px 10px;
    border-radius: 6px;
    font-size: 13px;
    font-weight: 800;
    display: inline-flex;
    align-items: center;
    gap: 6px;
}
.badge-moderate {
    background: rgba(245, 158, 11, 0.25);
    color: #fde68a;
    border: 1.5px solid #f59e0b;
    padding: 4px 10px;
    border-radius: 6px;
    font-size: 13px;
    font-weight: 800;
    display: inline-flex;
    align-items: center;
    gap: 6px;
}
.badge-low {
    background: rgba(59, 130, 246, 0.25);
    color: #bfdbfe;
    border: 1.5px solid #3b82f6;
    padding: 4px 10px;
    border-radius: 6px;
    font-size: 13px;
    font-weight: 800;
    display: inline-flex;
    align-items: center;
    gap: 6px;
}

/* Glass Panels */
.glass-panel {
    background: rgba(30, 41, 59, 0.75);
    border: 1px solid rgba(148, 163, 184, 0.2);
    border-radius: 10px;
    padding: 16px 20px;
    margin-bottom: 16px;
}

/* Directives & Action Boxes */
.directive-box {
    background: rgba(239, 68, 68, 0.12);
    border-left: 4px solid #ef4444;
    border-radius: 8px;
    padding: 14px 18px;
    margin: 10px 0;
}

.action-pill {
    background: rgba(56, 189, 248, 0.12);
    color: #38bdf8;
    border: 1px solid rgba(56, 189, 248, 0.3);
    padding: 6px 12px;
    border-radius: 6px;
    font-size: 12.5px;
    font-weight: 600;
    display: inline-block;
    margin: 3px 4px 3px 0;
}

/* Dispatch Row */
.dispatch-item {
    background: rgba(15, 23, 42, 0.7);
    border-left: 4px solid #38bdf8;
    border-radius: 6px;
    padding: 12px 16px;
    margin-bottom: 10px;
}
.dispatch-crit {
    border-left-color: #ef4444 !important;
}
.dispatch-high {
    border-left-color: #f97316 !important;
}

/* Provenance & Transparency Pills */
.source-badge-real {
    background: rgba(16, 185, 129, 0.15);
    color: #6ee7b7;
    border: 1px solid rgba(16, 185, 129, 0.35);
    padding: 3px 8px;
    border-radius: 4px;
    font-size: 11px;
    font-weight: 700;
    display: inline-flex;
    align-items: center;
    gap: 4px;
    cursor: help;
    transition: all 0.15s ease;
}
.source-badge-real:hover {
    background: rgba(16, 185, 129, 0.25);
    border-color: #10b981;
    transform: translateY(-1px);
}
.source-badge-est {
    background: rgba(56, 189, 248, 0.15);
    color: #7dd3fc;
    border: 1px solid rgba(56, 189, 248, 0.35);
    padding: 3px 8px;
    border-radius: 4px;
    font-size: 11px;
    font-weight: 700;
    display: inline-flex;
    align-items: center;
    gap: 4px;
    cursor: help;
    transition: all 0.15s ease;
}
.source-badge-est:hover {
    background: rgba(56, 189, 248, 0.25);
    border-color: #38bdf8;
    transform: translateY(-1px);
}
.source-badge-sim {
    background: rgba(245, 158, 11, 0.15);
    color: #fde68a;
    border: 1px solid rgba(245, 158, 11, 0.35);
    padding: 3px 8px;
    border-radius: 4px;
    font-size: 11px;
    font-weight: 700;
    display: inline-flex;
    align-items: center;
    gap: 4px;
    cursor: help;
    transition: all 0.15s ease;
}
.source-badge-sim:hover {
    background: rgba(245, 158, 11, 0.25);
    border-color: #f59e0b;
    transform: translateY(-1px);
}

/* Google Product Highlighting System */
.badge-google {
    background: linear-gradient(135deg, rgba(66, 133, 244, 0.20), rgba(219, 68, 85, 0.15), rgba(244, 180, 0, 0.15), rgba(15, 157, 88, 0.15));
    color: #f8fafc;
    border: 1px solid rgba(66, 133, 244, 0.45);
    border-bottom: 2px solid rgba(66, 133, 244, 0.7);
    padding: 4px 10px;
    border-radius: 6px;
    font-size: 11.5px;
    font-weight: 700;
    display: inline-flex;
    align-items: center;
    gap: 5px;
    letter-spacing: 0.2px;
    cursor: help;
    transition: all 0.15s ease;
}
.badge-google:hover, .badge-google-live:hover, .badge-google-fallback:hover {
    filter: brightness(1.2);
    transform: translateY(-1.5px);
    box-shadow: 0 4px 12px rgba(66, 133, 244, 0.3);
}
.badge-google-live {
    background: rgba(66, 133, 244, 0.25);
    color: #93c5fd;
    border: 1px solid #3b82f6;
    border-bottom: 2px solid #60a5fa;
    padding: 3px 8px;
    border-radius: 4px;
    font-size: 11px;
    font-weight: 700;
    display: inline-flex;
    align-items: center;
    gap: 4px;
    cursor: help;
    transition: all 0.15s ease;
}
.badge-google-fallback {
    background: rgba(245, 158, 11, 0.18);
    color: #fde68a;
    border: 1px solid rgba(245, 158, 11, 0.4);
    border-bottom: 2px solid rgba(245, 158, 11, 0.7);
    padding: 3px 8px;
    border-radius: 4px;
    font-size: 11px;
    font-weight: 700;
    display: inline-flex;
    align-items: center;
    gap: 4px;
    cursor: help;
    transition: all 0.15s ease;
}
.google-card {
    background: rgba(15, 23, 42, 0.85);
    border: 1px solid rgba(66, 133, 244, 0.3);
    border-top: 3px solid #4285f4;
    border-radius: 8px;
    padding: 14px 18px;
    margin-top: 12px;
    margin-bottom: 12px;
}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# Additional typography and layout helpers for explanation sections
EXPLANATION_CSS = """
<style>
/* Explanation Section Typography Scale */
.exp-section {
    margin-bottom: 14px;
    padding: 12px 16px;
    background: rgba(30, 41, 59, 0.6);
    border: 1px solid rgba(148, 163, 184, 0.15);
    border-radius: 8px;
    border-left: 3px solid #38bdf8;
}
.exp-title {
    font-size: 15px;
    font-weight: 700;
    color: #38bdf8;
    margin-bottom: 8px;
    display: flex;
    align-items: center;
    gap: 6px;
    text-transform: uppercase;
    letter-spacing: 0.4px;
}
.exp-question {
    font-size: 14px;
    font-weight: 600;
    color: #f1f5f9;
    margin: 10px 0 4px 0;
    line-height: 1.3;
}
.exp-answer {
    font-size: 14px;
    font-weight: 400;
    color: #cbd5e1;
    line-height: 1.6;
    margin: 0 0 6px 0;
}
.exp-answer strong {
    color: #f8fafc;
    font-weight: 600;
}
.exp-bullet {
    font-size: 13.5px;
    color: #cbd5e1;
    line-height: 1.55;
    margin: 3px 0 3px 18px;
}
.exp-bullet::before {
    content: "▸ ";
    color: #38bdf8;
    font-weight: 600;
}
.exp-numbered {
    font-size: 13.5px;
    color: #cbd5e1;
    line-height: 1.55;
    margin: 4px 0 4px 22px;
}
.exp-numbered::before {
    content: counter(exp-counter) ". ";
    color: #38bdf8;
    font-weight: 700;
    counter-increment: exp-counter;
}
.exp-numbered-list {
    counter-reset: exp-counter;
}
.exp-tech-list {
    font-size: 13px;
    color: #cbd5e1;
    line-height: 1.5;
    margin: 4px 0 4px 18px;
}
.exp-tech-list::before {
    content: "• ";
    color: #38bdf8;
    font-weight: 600;
}
.exp-note {
    font-size: 12.5px;
    color: #94a3b8;
    font-style: italic;
    margin-top: 8px;
    padding-top: 8px;
    border-top: 1px solid rgba(148, 163, 184, 0.15);
    line-height: 1.45;
}
/* Override Streamlit expander header size */
.streamlit-expanderHeader {
    font-size: 14.5px !important;
    font-weight: 600 !important;
}
.streamlit-expanderHeader p {
    font-size: 14.5px !important;
    font-weight: 600 !important;
    margin: 0 !important;
}
</style>
"""
st.markdown(EXPLANATION_CSS, unsafe_allow_html=True)

# Helper function for rendering consistent explanation sections
def render_explanation(title: str, sections: dict, icon: str = "ℹ️", expanded: bool = False):
    """Render a consistent explanation expander with the standard structure.
    
    sections: dict with keys like 'what', 'how', 'benefit', 'tech', 'limitations', 'note'
    Values can be strings, lists (for bullets/numbered), or None to skip.
    """
    lines = []
    for key, value in sections.items():
        if value is None:
            continue
        if key == 'what':
            lines.append(f'<div class="exp-section"><div class="exp-title">{icon} What it does</div><div class="exp-answer">{value}</div></div>')
        elif key == 'how':
            if isinstance(value, list):
                html = '<div class="exp-section"><div class="exp-title">{icon} How it works</div><div class="exp-numbered-list">'.format(icon=icon)
                for item in value:
                    html += f'<div class="exp-numbered">{item}</div>'
                html += '</div></div>'
                lines.append(html)
            else:
                lines.append(f'<div class="exp-section"><div class="exp-title">{icon} How it works</div><div class="exp-answer">{value}</div></div>')
        elif key == 'benefit':
            lines.append(f'<div class="exp-section"><div class="exp-title">{icon} Real-world benefit</div><div class="exp-answer">{value}</div></div>')
        elif key == 'tech':
            if isinstance(value, list):
                html = '<div class="exp-section"><div class="exp-title">{icon} Technology</div>'.format(icon=icon)
                for item in value:
                    html += f'<div class="exp-tech-list">{item}</div>'
                html += '</div>'
                lines.append(html)
            else:
                lines.append(f'<div class="exp-section"><div class="exp-title">{icon} Technology</div><div class="exp-answer">{value}</div></div>')
        elif key == 'limitations':
            lines.append(f'<div class="exp-section"><div class="exp-title">📋 Data status & limitations</div><div class="exp-answer">{value}</div></div>')
        elif key == 'note':
            lines.append(f'<div class="exp-note">{value}</div>')
    with st.expander(f"{icon} {title}", expanded=expanded):
        render_html("".join(lines))

# Google Ecosystem Masthead Showcase Banner
render_html("""
<div style="background: linear-gradient(135deg, rgba(15, 23, 42, 0.95), rgba(30, 41, 59, 0.90)); border: 1px solid rgba(66, 133, 244, 0.35); border-radius: 12px; padding: 14px 20px; margin-bottom: 14px; box-shadow: 0 4px 20px rgba(0,0,0,0.3);">
    <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px;">
        <div style="display:flex; align-items:center; gap:12px;">
            <div style="font-size:30px;">🌀</div>
            <div>
                <div style="font-size:22px; font-weight:800; color:#f8fafc; letter-spacing:-0.5px;">
                    CycloneShield <span style="font-size:13px; font-weight:700; color:#38bdf8; background:rgba(56,189,248,0.15); border:1px solid rgba(56,189,248,0.3); padding:2px 8px; border-radius:4px; margin-left:6px;">Google Ecosystem Powered</span>
                </div>
                <div style="font-size:12.5px; color:#cbd5e1; margin-top:2px;">
                    Multi-Hazard Cyclone Impact & Lifeline Infrastructure Vulnerability Command Center for Indian Coastal States
                </div>
            </div>
        </div>
        <div style="display:flex; flex-wrap:wrap; gap:6px; align-items:center;">
            <span class="badge-google" title="Optional Gemini features support specific user-requested tasks when connected. They do not issue directives, send alerts, or release funds.">✨ Google Gemini integrations</span>
            <span class="badge-google" title="Earth Engine can provide or process geospatial layers when authenticated; it does not generate live cyclone forecasts.">🌍 Earth Engine (GEE)</span>
            <span class="badge-google" title="Google BigQuery: Searches historical storm records in seconds to compare the current cyclone with past major Indian storms.">🛰️ BigQuery NOAA</span>
            <span class="badge-google" title="Cloud Run deployment blueprint; this does not describe the current hosted runtime or guarantee capacity/cost.">☁️ Cloud Run blueprint</span>
            <span class="badge-google" title="Google Colab: Run the entire project in 1 click in Google Colab without needing to install anything on your computer.">🧪 Colab 1-Click</span>
        </div>
    </div>
</div>
""")

# Interactive Architecture Guide Accordion
with st.expander("ℹ️ CycloneShield Architecture Guide: Turning Cyclone Warnings into Life-Saving Actions", expanded=False):
    st.markdown("""
    ### 🌀 CycloneShield: Decision Support for Cyclone Preparedness
    **A prototype designed to help authorized teams turn complex information into clearer priorities and faster decisions.**

    CycloneShield presents configured storm scenarios, screening estimates, and possible preparedness actions for human review. It does not replace weather agencies or rescue officers.

    Instead of looking at multiple reports and maps separately, officers can use one dashboard to understand the danger and plan their response.

    #### Our Technology:
    - ✨ **Google Gemini:** Optional, user-requested AI features run only when configured and a successful response is confirmed.
    - 🌍 **Google Earth Engine:** Can provide or process geospatial data when authenticated; it does not predict cyclones.
    - 🛰️ **Google BigQuery:** Optional path for querying historical cyclone information.
    - ☁️ **Google Cloud Run:** A deployment option; it is not necessarily the current host.
    - 🧪 **Google Colab:** Helps developers test the system and demonstrate its calculations.

    *Historical and prepared examples are distinct from live responses. Forecasts require a connected weather source; check source/status labels before calling data live.*

    ---

    #### How Google Technology Helps CycloneShield:
    1. **Google Gemini:** Can support configured, user-requested analysis; outputs are recommendations for human review, not operational decisions.
    2. **Gemini Vision:** Can analyze an explicitly submitted photo when a live response is confirmed; offline benchmark results are prepared demonstrations, not model output.
    3. **Google Earth Engine:** Can support geospatial/elevation data access and processing; it does not generate live cyclone predictions.
    4. **Google BigQuery — Helps Learn from Past Cyclones:** Stores and searches historical cyclone records to compare current storms with past disasters.
    5. **Google Cloud Run:** Deployment blueprint; actual hosting, scaling, and costs depend on a configured deployment.
    6. **Google Colab — Helps Test the System:** An online 1-click test notebook for evaluators and developers without local setup.
    """, unsafe_allow_html=True)

    g_col1, g_col2, g_col3 = st.columns(3, gap="medium")
    with g_col1:
        render_html("""
        <div style="background:rgba(15,23,42,0.7); border:1px solid rgba(66,133,244,0.35); border-top:3px solid #4285f4; border-radius:8px; padding:12px 14px; height:100%;">
            <div style="font-size:12.5px; font-weight:800; color:#38bdf8; display:flex; align-items:center; gap:6px;">
                <span>✨</span> GOOGLE GEMINI AI
            </div>
            <div style="font-size:11.5px; color:#94a3b8; margin-top:2px;"><b>Role</b>: Decision support for human review</div>
            <div style="font-size:12px; color:#cbd5e1; margin-top:8px; line-height:1.5;">
                • <b>Possible Actions</b>: Scenario outputs can help officers review resource priorities; they do not deploy rescue units.<br>
                • <b>Insurance Demo</b>: Calculates illustrative trigger tiers and payout scenarios; it does not release funds.<br>
                • <b>Weather Reports</b>: Forecasts require a connected meteorological source and confirmed live response.<br>
                • <b>Messages</b>: Prepared multilingual templates and CAP exports are drafts for authorized review, not public alerts.<br>
                • <b>Offline Mode</b>: Prepared fallbacks demonstrate workflows and are labeled as estimates or simulations.
            </div>
        </div>
        """)
    with g_col2:
        render_html("""
        <div style="background:rgba(15,23,42,0.7); border:1px solid rgba(16,185,129,0.35); border-top:3px solid #10b981; border-radius:8px; padding:12px 14px; height:100%;">
            <div style="font-size:12.5px; font-weight:800; color:#6ee7b7; display:flex; align-items:center; gap:6px;">
                <span>📸</span> GEMINI VISION & EARTH ENGINE
            </div>
            <div style="font-size:11.5px; color:#94a3b8; margin-top:2px;"><b>Role</b>: Photo inspection & flood ground maps</div>
            <div style="font-size:12px; color:#cbd5e1; margin-top:8px; line-height:1.5;">
                • <b>Disaster Photos (Tab 3)</b>: Gemini Vision is called only on request; offline benchmark output is not model analysis.<br>
                • <b>Flood Check (Tab 1)</b>: Elevation layers inform screening estimates; Earth Engine does not predict cyclones.<br>
                • <b>Map (Tab 1)</b>: Displays the selected scenario and configured geospatial layers, not a live satellite feed.
            </div>
        </div>
        """)
    with g_col3:
        render_html("""
        <div style="background:rgba(15,23,42,0.7); border:1px solid rgba(245,158,11,0.35); border-top:3px solid #f59e0b; border-radius:8px; padding:12px 14px; height:100%;">
            <div style="font-size:12.5px; font-weight:800; color:#fde68a; display:flex; align-items:center; gap:6px;">
                <span>🛰️</span> BIGQUERY, CLOUD RUN & COLAB
            </div>
            <div style="font-size:11.5px; color:#94a3b8; margin-top:2px;"><b>Role</b>: Cloud database, scale & easy test notebook</div>
            <div style="font-size:12px; color:#cbd5e1; margin-top:8px; line-height:1.5;">
                • <b>Past Storms (Tab 8)</b>: Historical records may come from a bundled cache or an optional confirmed BigQuery query.<br>
                • <b>Cloud Hosting</b>: Cloud Run is a deployment option, not the current hosted runtime.<br>
                • <b>Easy Testing</b>: 1-click test notebook on Google Cloud with zero setup.<br>
                • <b>Plain Explanations (Tab 4)</b>: Explains in simple terms why each district is at risk (wind, seawater surge, or low ground).
            </div>
        </div>
        """)

    render_html("""
    <div style="margin-top:14px; background:rgba(30,41,59,0.5); border:1px solid rgba(148,163,184,0.25); border-radius:8px; padding:12px 16px;">
        <div style="font-size:12.5px; font-weight:700; color:#38bdf8; margin-bottom:8px;">
            🔍 What Each Google Tool Does in Plain Words:
        </div>
        <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap:10px; font-size:11.5px; color:#cbd5e1; line-height:1.45;">
            <div>
                <span class="badge-google" title="Parses bulletin text supplied by the user; Gemini is optional and the local regex parser is the fallback.">Sidebar: Weather Bulletin Text Parser</span><br>
                <b>What it does</b>: Extracts track details from a supplied bulletin; it does not generate or predict a forecast.<br>
                <i>Fallback</i>: Local regex parser.
            </div>
            <div>
                <span class="badge-google" title="Displays configured scenario layers with geospatial/elevation inputs">Tab 1: Scenario & Hazard Map</span><br>
                <b>What it does</b>: Uses elevation and scenario estimates to support screening; it is not a live satellite feed or cyclone forecast.<br>
                <i>Offline example</i>: Configured geospatial baseline.
            </div>
            <div>
                <span class="badge-google" title="Summarizes configured scenario indicators for human review">Tab 1: District Scenario Review</span><br>
                <b>What it does</b>: Presents scenario-based lifeline indicators and possible actions for authorized review.<br>
                <i>Note</i>: Not an official warning or observed impact report.
            </div>
            <div>
                <span class="badge-google" title="Shows prepared message templates and optional voice previews">Tab 2: Draft Messages & Voice Preview</span><br>
                <b>What it does</b>: Prepares multilingual draft text and optional audio for review.<br>
                <i>Note</i>: Does not issue or transmit public alerts.
            </div>
            <div>
                <span class="badge-google" title="Gemini Vision is used only for a confirmed live request; otherwise results are prepared benchmark examples">Tab 3: Photo-Triage Demonstration</span><br>
                <b>What it does</b>: Demonstrates image triage; an offline benchmark is not Gemini analysis.<br>
                <i>Live mode</i>: Requires configured access and a confirmed successful response.
            </div>
            <div>
                <span class="badge-google" title="Explains configured scenario screening scores">Tab 4: Scenario Risk Matrix</span><br>
                <b>What it does</b>: Compares configured district indicators using project-defined scoring rules.<br>
                <i>Note</i>: Scores are screening outputs, not field-validated probabilities.
            </div>
            <div>
                <span class="badge-google" title="Produces scenario-based action suggestions for officer review">Tab 5: Possible Actions</span><br>
                <b>What it does</b>: Recommends possible resource and route considerations for human review.<br>
                <i>Note</i>: Does not deploy rescue resources or issue evacuation decisions.
            </div>
            <div>
                <span class="badge-google" title="Demonstrates configured insurance trigger and payout calculations">Tab 6: Insurance Trigger Demonstration</span><br>
                <b>What it does</b>: Maps scenario inputs to illustrative payout tiers.<br>
                <i>Note</i>: Not an active policy, verified trigger, or payment.
            </div>
            <div>
                <span class="badge-google" title="Separate weather forecast feed; check status and source">Tab 7: Weather Forecast Feed</span><br>
                <b>What it does</b>: Requests forecast data from a connected weather source when available.<br>
                <i>Note</i>: Not an official IMD forecast; does not drive scenario risk scores.
            </div>
        </div>
    </div>
    """)



# ==============================================================================
# 1. State, Cyclone & Language Selection Header
# ==============================================================================

# Dictionary of Supported States & Historical Cyclones
STATE_CYCLONES: Dict[str, List[Dict[str, Any]]] = {
    "West Bengal": [
        {"name": "REMAL", "year": 2024, "category": "Very Severe Cyclonic Storm", "wind_kts": 60.0, "landfall": "Sundarbans / Sagar Island", "pres_mb": 977.0},
        {"name": "AMPHAN", "year": 2020, "category": "Super Cyclonic Storm", "wind_kts": 145.0, "landfall": "Digha - Sundarbans Belt", "pres_mb": 901.0}
    ],
    "Odisha": [
        {"name": "FANI", "year": 2019, "category": "Extremely Severe Cyclonic Storm", "wind_kts": 150.0, "landfall": "Puri Coast", "pres_mb": 900.0},
        {"name": "YAAS", "year": 2021, "category": "Very Severe Cyclonic Storm", "wind_kts": 75.0, "landfall": "Dhamra Port, Bhadrak", "pres_mb": 970.0},
        {"name": "DANA", "year": 2024, "category": "Severe Cyclonic Storm", "wind_kts": 65.0, "landfall": "Dhamra - Bhadrak Coast", "pres_mb": 985.0}
    ],
    "Andhra Pradesh": [
        {"name": "HUDHUD", "year": 2014, "category": "Extremely Severe Cyclonic Storm", "wind_kts": 115.0, "landfall": "Visakhapatnam Major Port", "pres_mb": 937.0},
        {"name": "MICHAUNG", "year": 2023, "category": "Severe Cyclonic Storm", "wind_kts": 65.0, "landfall": "Bapatla Coastal Plain", "pres_mb": 985.0}
    ],
    "Tamil Nadu": [
        {"name": "VARDAH", "year": 2016, "category": "Very Severe Cyclonic Storm", "wind_kts": 85.0, "landfall": "Chennai Coromandel Coast", "pres_mb": 959.0},
        {"name": "GAJA", "year": 2018, "category": "Very Severe Cyclonic Storm", "wind_kts": 80.0, "landfall": "Nagapattinam - Vedaranyam", "pres_mb": 963.0},
        {"name": "MICHAUNG", "year": 2023, "category": "Severe Cyclonic Storm", "wind_kts": 65.0, "landfall": "Chennai Urban Inundation", "pres_mb": 985.0}
    ],
    "Gujarat": [
        {"name": "BIPARJOY", "year": 2023, "category": "Extremely Severe Cyclonic Storm", "wind_kts": 110.0, "landfall": "Jakhau Port, Kutch", "pres_mb": 944.0},
        {"name": "TAUKTAE", "year": 2021, "category": "Extremely Severe Cyclonic Storm", "wind_kts": 120.0, "landfall": "Una / Saurashtra Coast, Gir Somnath", "pres_mb": 931.0}
    ]
}

STATE_REGIONAL_LANG: Dict[str, Tuple[str, str]] = {
    "West Bengal": ("bn", "Bengali (বাংলা)"),
    "Odisha": ("or", "Odia (ଓଡ଼ିଆ)"),
    "Andhra Pradesh": ("te", "Telugu (తెలుగు)"),
    "Tamil Nadu": ("ta", "Tamil (தமிழ்)"),
    "Gujarat": ("gu", "Gujarati (ગુજરાતી)")
}

# Top Navigation Bar: Language & Operating Mode
ctrl_col1, ctrl_col2, ctrl_col3 = st.columns([1.4, 1.2, 1.0], gap="medium")

with ctrl_col1:
    selected_state = st.selectbox(
        "📍 Select Vulnerable Coastal State:",
        options=list(STATE_CYCLONES.keys()),
        index=0,
        key="selected_coastal_state",
        help="Select any major disaster-prone Indian coastal state to evaluate regional district lifelines."
    )

with ctrl_col2:
    cyclone_options = [
        *[f"{c['name']} ({c['year']}) — {c['category']}" for c in STATE_CYCLONES[selected_state]],
        "🔴 [LIVE] Fetch Latest IMD Bulletin / Track"
    ]
    
    selected_cyclone_label = st.selectbox(
        "🌀 Select Cyclone Event:",
        options=cyclone_options,
        index=0,
        key=f"cyclone_event_for_{selected_state}",
        help="Select a historical benchmark or fetch the latest official RSMC bulletin. A track is loaded only if explicit waypoints can be parsed."
    )
    is_custom_track = any(k in selected_cyclone_label for k in ["[LIVE]", "Custom", "Ingest"])
    selected_storm_name = selected_cyclone_label.split()[0] if not is_custom_track else "CUSTOM"

with ctrl_col3:
    lang_choices = [
        "English", "Hindi (हिंदी)", "Bengali (বাংলা)",
        "Odia (ଓଡ଼ିଆ)", "Telugu (తెలుగు)", "Tamil (தமிழ்)", "Gujarati (ગુજરાતી)"
    ]
    LANG_NAME_TO_CODE: Dict[str, Tuple[str, str]] = {
        "English": ("en", "English"),
        "Hindi (हिंदी)": ("hi", "Hindi (हिंदी)"),
        "Bengali (বাংলা)": ("bn", "Bengali (বাংলা)"),
        "Odia (ଓଡ଼ିଆ)": ("or", "Odia (ଓଡ଼ିଆ)"),
        "Telugu (తెలుగు)": ("te", "Telugu (తెలుగు)"),
        "Tamil (தமிழ்)": ("ta", "Tamil (தமிழ்)"),
        "Gujarati (ગુજરાતી)": ("gu", "Gujarati (ગુજરાતી)")
    }
    reg_code, reg_label = STATE_REGIONAL_LANG.get(selected_state, ("hi", "Hindi"))
    # Default to regional language of selected state if present, else English
    default_lang_idx = 0
    for idx, l in enumerate(lang_choices):
        if reg_label.split()[0] in l:
            default_lang_idx = idx
            break
            
    active_ui_lang = st.selectbox(
        "🌐 App & Broadcast Language:",
        options=lang_choices,
        index=default_lang_idx,
        key=f"app_lang_for_{selected_state}",
        help="Translates operational headings, broadcast alerts, and audio voiceover to the local language."
    )
    active_lang_code, active_lang_label = LANG_NAME_TO_CODE.get(active_ui_lang, (reg_code, reg_label))


# ==============================================================================
# 2. Dynamic Coastal District Geospatial Database
# ==============================================================================

@st.cache_data
def load_all_coastal_districts() -> List[Dict[str, Any]]:
    """Loads all 35 coastal districts across West Bengal, Odisha, AP, TN, Gujarat."""
    dist_path = os.path.join(DATA_DIR, "coastal_districts.geojson")
    if os.path.exists(dist_path):
        with open(dist_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return [feat["properties"] for feat in data.get("features", [])]
    return []

@st.cache_data
def load_cyclone_track_data(storm_name: str, state_name: str) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """Fetches standardized cyclone track from local NOAA cache or BigQuery pipeline."""
    sample_path = os.path.join(DATA_DIR, "noaa_sample_tracks.json")
    if os.path.exists(sample_path):
        with open(sample_path, "r", encoding="utf-8") as f:
            catalog = json.load(f)
            if storm_name.upper() in catalog:
                s_meta = catalog[storm_name.upper()]
                df = pd.DataFrame(s_meta.get("track", []))
                if not df.empty and "time" in df.columns:
                    df["time"] = pd.to_datetime(df["time"])
                return df, s_meta

    # Fallback to BigQuery pipeline client
    if get_bigquery_pipeline:
        try:
            pipeline = get_bigquery_pipeline()
            df, meta = pipeline.fetch_cyclone_track(storm_name)
            return df, meta
        except Exception:
            pass

    return pd.DataFrame(), {}

# Fallback district database covering all 5 key coastal disaster states
STATE_FALLBACK_DISTRICTS: Dict[str, List[Dict[str, Any]]] = {
    "West Bengal": [
        {"district_name": "South 24 Parganas", "lat": 22.15, "lon": 88.55, "population": 8161961, "coastal_zone": "Sundarbans Estuary", "hq": "Alipore"},
        {"district_name": "North 24 Parganas", "lat": 22.72, "lon": 88.48, "population": 10009781, "coastal_zone": "Ichamati Estuary", "hq": "Barasat"},
        {"district_name": "Purba Medinipur", "lat": 21.93, "lon": 87.77, "population": 5095875, "coastal_zone": "Digha - Mandarmani Coast", "hq": "Tamluk"},
        {"district_name": "Kolkata", "lat": 22.57, "lon": 88.36, "population": 4496694, "coastal_zone": "Hooghly Urban Basin", "hq": "Kolkata"},
        {"district_name": "Howrah", "lat": 22.59, "lon": 88.26, "population": 4850029, "coastal_zone": "Lower Damodar Basin", "hq": "Howrah"},
    ],
    "Odisha": [
        {"district_name": "Puri", "lat": 19.81, "lon": 85.83, "population": 1698730, "coastal_zone": "Chilika - Puri Shoreline", "hq": "Puri"},
        {"district_name": "Jagatsinghpur", "lat": 20.25, "lon": 86.17, "population": 1136971, "coastal_zone": "Paradeep Port Sector", "hq": "Jagatsinghpur"},
        {"district_name": "Kendrapara", "lat": 20.50, "lon": 86.42, "population": 1440361, "coastal_zone": "Bhitarkanika Mangroves", "hq": "Kendrapara"},
        {"district_name": "Bhadrak", "lat": 21.05, "lon": 86.50, "population": 1506522, "coastal_zone": "Dhamra Port Shore", "hq": "Bhadrak"},
        {"district_name": "Balasore", "lat": 21.49, "lon": 86.93, "population": 2320529, "coastal_zone": "Chandipur Coast", "hq": "Balasore"},
        {"district_name": "Ganjam", "lat": 19.38, "lon": 85.05, "population": 3529031, "coastal_zone": "Gopalpur Port Coast", "hq": "Chatrapur"},
    ],
    "Andhra Pradesh": [
        {"district_name": "Visakhapatnam", "lat": 17.68, "lon": 83.21, "population": 4290589, "coastal_zone": "Vizag Major Port & Harbor", "hq": "Visakhapatnam"},
        {"district_name": "Srikakulam", "lat": 18.29, "lon": 83.89, "population": 2703114, "coastal_zone": "North AP Coastal Border", "hq": "Srikakulam"},
        {"district_name": "Vizianagaram", "lat": 18.11, "lon": 83.40, "population": 2344474, "coastal_zone": "Bhimunipatnam Sector", "hq": "Vizianagaram"},
        {"district_name": "East Godavari", "lat": 16.98, "lon": 82.24, "population": 5286474, "coastal_zone": "Kakinada - Godavari Delta", "hq": "Kakinada"},
        {"district_name": "Krishna", "lat": 16.18, "lon": 81.13, "population": 4517398, "coastal_zone": "Machilipatnam Coast", "hq": "Machilipatnam"},
        {"district_name": "Bapatla", "lat": 15.90, "lon": 80.46, "population": 1586918, "coastal_zone": "Suryalanka - Nizampatnam Shore", "hq": "Bapatla"},
        {"district_name": "SPSR Nellore", "lat": 14.44, "lon": 79.98, "population": 2963557, "coastal_zone": "Krishnapatnam Port Belt", "hq": "Nellore"},
    ],
    "Tamil Nadu": [
        {"district_name": "Chennai", "lat": 13.08, "lon": 80.27, "population": 7088403, "coastal_zone": "Coromandel Urban Coast", "hq": "Chennai"},
        {"district_name": "Chengalpattu", "lat": 12.68, "lon": 79.98, "population": 2556244, "coastal_zone": "Mahabalipuram Shore", "hq": "Chengalpattu"},
        {"district_name": "Cuddalore", "lat": 11.75, "lon": 79.76, "population": 2605914, "coastal_zone": "Cuddalore Port Shoreline", "hq": "Cuddalore"},
        {"district_name": "Nagapattinam", "lat": 10.76, "lon": 79.84, "population": 1616450, "coastal_zone": "Vedaranyam - Point Calimere", "hq": "Nagapattinam"},
        {"district_name": "Thiruvarur", "lat": 10.77, "lon": 79.63, "population": 1264277, "coastal_zone": "Cauvery Delta Estuary", "hq": "Thiruvarur"},
        {"district_name": "Ramanathapuram", "lat": 9.36, "lon": 78.83, "population": 1353445, "coastal_zone": "Pamban - Rameswaram Island", "hq": "Ramanathapuram"},
    ],
    "Gujarat": [
        {"district_name": "Kutch", "lat": 23.24, "lon": 69.66, "population": 2092371, "coastal_zone": "Gulf of Kutch - Jakhau Port", "hq": "Bhuj"},
        {"district_name": "Devbhumi Dwarka", "lat": 22.24, "lon": 68.96, "population": 752484, "coastal_zone": "Dwarka Promontory", "hq": "Khambhalia"},
        {"district_name": "Jamnagar", "lat": 22.47, "lon": 70.07, "population": 2160119, "coastal_zone": "Marine National Park Shore", "hq": "Jamnagar"},
        {"district_name": "Porbandar", "lat": 21.64, "lon": 69.60, "population": 585449, "coastal_zone": "Saurashtra Open Arabian Sea", "hq": "Porbandar"},
        {"district_name": "Gir Somnath", "lat": 20.90, "lon": 70.36, "population": 1217477, "coastal_zone": "Veraval Fishing Port", "hq": "Veraval"},
        {"district_name": "Bhavnagar", "lat": 21.76, "lon": 72.15, "population": 2880365, "coastal_zone": "Gulf of Khambhat", "hq": "Bhavnagar"},
    ]
}

# Load District Data
all_districts = load_all_coastal_districts()
state_districts = [
    d for d in all_districts 
    if d.get("state_or_division", "").strip().lower() == selected_state.strip().lower()
]
if not state_districts:
    state_districts = STATE_FALLBACK_DISTRICTS.get(selected_state, STATE_FALLBACK_DISTRICTS.get("West Bengal", []))


# ==============================================================================
# 3. Live IMD / RSMC Bulletin Retrieval & Cyclone Track Ingestion
# ==============================================================================
custom_track_df = None
if is_custom_track:
    with st.expander("🛰️ IMD / RSMC Live Bulletin & Track Ingestion", expanded=True):
        st.markdown("""
        <div style="font-size:13px; color:#cbd5e1; margin-bottom:10px; line-height:1.5;">
            Fetch the latest published cyclone outlook/bulletin from <b>IMD / RSMC New Delhi</b>. The app changes the active track only when the official document contains at least two complete, explicit waypoints; demo scenarios and operator uploads are separate.
        </div>
        """, unsafe_allow_html=True)

        # Live RSMC product status
        rsmc_info = None
        if st.session_state.get("refresh_rsmc_requested", False) and fetch_latest_imd_bulletin:
            with st.spinner("Fetching the latest official RSMC bulletin and checking for explicit track waypoints..."):
                live_track_df, rsmc_info = fetch_latest_imd_bulletin()
                st.session_state["live_rsmc_status"] = rsmc_info
                if live_track_df is not None and not live_track_df.empty:
                    st.session_state["custom_track_df"] = live_track_df
                    st.session_state["custom_track_meta"] = rsmc_info
                    st.session_state["imd_refresh_notice"] = {
                        "level": "success",
                        "message": f"Loaded {len(live_track_df)} explicit waypoints from {rsmc_info.get('latest_product_title', 'the latest IMD product')}."
                    }
                else:
                    st.session_state["imd_refresh_notice"] = {
                        "level": "warning",
                        "message": rsmc_info.get("track_status", "No verified track was found; the active dashboard track was not changed.")
                    }
                st.session_state["refresh_rsmc_requested"] = False
        elif check_live_imd_rsmc_status:
            if "live_rsmc_status" not in st.session_state:
                with st.spinner("Connecting to RSMC New Delhi live server..."):
                    st.session_state["live_rsmc_status"] = check_live_imd_rsmc_status()
            rsmc_info = st.session_state.get("live_rsmc_status")

        stat_col1, stat_col2 = st.columns([2.2, 1.0])
        with stat_col1:
            badge_txt = html_lib.escape(rsmc_info.get("status_badge", "⚪ IMD CONNECTION UNAVAILABLE")) if rsmc_info else "⚪ IMD CONNECTION UNAVAILABLE"
            summary_txt = html_lib.escape(rsmc_info.get("summary", "IMD / RSMC status is not available.")) if rsmc_info else "IMD / RSMC status is not available."
            checked_at = html_lib.escape(rsmc_info.get("timestamp", "Not checked")) if rsmc_info else "Not checked"
            st.markdown(f"""
            <div style="background:rgba(15,23,42,0.85); border:1px solid rgba(56,189,248,0.25); border-radius:8px; padding:10px 14px; margin-bottom:12px;">
                <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px;">
                    <div>
                        <span style="font-size:12px; font-weight:800; color:#38bdf8; background:rgba(56,189,248,0.15); padding:3px 8px; border-radius:4px;">{badge_txt}</span>
                        <span style="font-size:11px; color:#94a3b8; margin-left:8px;">Source: <a href="https://rsmcnewdelhi.imd.gov.in" target="_blank" style="color:#7dd3fc; text-decoration:none;">RSMC New Delhi</a></span>
                    </div>
                    <div style="font-size:11px; color:#94a3b8;">Checked: {checked_at}</div>
                </div>
                <div style="font-size:12px; color:#cbd5e1; margin-top:6px;">{summary_txt}</div>
            </div>
            """, unsafe_allow_html=True)
            if rsmc_info and rsmc_info.get("latest_product_url"):
                st.link_button(
                    f"Open latest IMD product: {rsmc_info.get('latest_product_title', 'RSMC bulletin')}",
                    rsmc_info["latest_product_url"],
                    use_container_width=True
                )
            if rsmc_info and rsmc_info.get("issued_at"):
                st.caption(f"Official issue date: {rsmc_info['issued_at']}")
            notice = st.session_state.pop("imd_refresh_notice", None)
            if notice:
                if notice["level"] == "success":
                    st.success(notice["message"])
                else:
                    st.warning(notice["message"])
        with stat_col2:
            if st.button("🔄 Fetch Latest IMD Update", use_container_width=True, help="Downloads the latest dated RSMC outlook/bulletin and loads a track only if explicit waypoints are present."):
                st.session_state["refresh_rsmc_requested"] = True
                st.rerun()

        # Ingestion Modes
        ingest_t1, ingest_t2, ingest_t3, ingest_t4 = st.tabs([
            "🧪 Synthetic Demo Scenarios",
            "📋 Paste Raw IMD Bulletin Text",
            "🎯 Coastal Landfall Builder",
            "📁 Upload IMD CSV Track"
        ])

        with ingest_t1:
            st.markdown("<div style='font-size:12.5px; color:#cbd5e1; margin-bottom:8px;'><b>Demo-only scenarios</b>: Hard-coded synthetic tracks for testing; these are not current IMD alerts or observations.</div>", unsafe_allow_html=True)
            sc_keys = list(EMERGING_SCENARIOS.keys()) if EMERGING_SCENARIOS else []
            sel_sc_key = st.selectbox("Select a synthetic demo scenario:", options=sc_keys, index=0)
            
            sc_preview = EMERGING_SCENARIOS.get(sel_sc_key, {})
            p_c1, p_c2, p_c3, p_c4 = st.columns(4)
            p_c1.metric("Storm Name", sc_preview.get("storm_name", "—"))
            p_c2.metric("Target State", sc_preview.get("target_state", "—"))
            p_c3.metric("Peak Wind", f"{sc_preview.get('peak_wind_kts', 0):.0f} kts")
            p_c4.metric("Min Pressure", f"{sc_preview.get('min_pressure_mb', 0):.0f} mb")
            
            if st.button(f"🧪 Load demo scenario '{sc_preview.get('storm_name','Demo')}'", type="primary", use_container_width=True):
                if load_emerging_scenario:
                    s_df, s_meta = load_emerging_scenario(sel_sc_key)
                    st.session_state["custom_track_df"] = s_df
                    st.session_state["custom_track_meta"] = s_meta
                    st.success(f"Loaded synthetic demo track {s_meta['name']} ({s_meta['category']}); this is not an IMD observation.")
                    st.rerun()

        with ingest_t2:
            st.markdown("""
            <div style='display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;'>
                <div style='font-size:12.5px; color:#cbd5e1;'><b>IMD Bulletin Text Parser</b>: Extract track details from bulletin text you provide; this does not create a forecast.</div>
                <span class='badge-google' title="Gemini can extract details from supplied bulletin text when configured and successfully connected; otherwise the local regex parser is used.">✨ Optional Google Gemini 2.5 Flash</span>
            </div>
            """, unsafe_allow_html=True)
            sample_imd_bulletin_text = (
                "INDIA METEOROLOGICAL DEPARTMENT\n"
                "BULLETIN NO. 14 (BOB/01/2026)\n"
                "TIME OF ISSUE: 1400 HOURS IST DATED 14.10.2026\n"
                "FROM: INDIA METEOROLOGICAL DEPARTMENT (CYCLONE WARNING DIVISION, NEW DELHI)\n"
                "SUBJECT: SEVERE CYCLONIC STORM SHAKTI OVER WESTCENTRAL BAY OF BENGAL\n"
                "ESTIMATED CENTRAL PRESSURE IS 978 HPA.\n"
                "MAXIMUM SUSTAINED SURFACE WIND SPEED IS 70 KNOTS GUSTING TO 85 KNOTS.\n"
                "FORECAST TRACK AND INTENSITY:\n"
                "14.10.2026/1130 | 17.8 / 84.6 | 70 KNOTS | SEVERE CYCLONIC STORM\n"
                "14.10.2026/1730 | 18.3 / 84.9 | 80 KNOTS | VERY SEVERE CYCLONIC STORM\n"
                "14.10.2026/2330 | 18.9 / 85.2 | 85 KNOTS | VERY SEVERE CYCLONIC STORM\n"
                "15.10.2026/0530 | 19.4 / 85.6 | 90 KNOTS | VERY SEVERE CYCLONIC STORM (LANDFALL)\n"
                "15.10.2026/1130 | 20.0 / 85.9 | 65 KNOTS | CYCLONIC STORM"
            )
            col_b1, col_b2 = st.columns([1.0, 1.0])
            with col_b1:
                if st.button("📋 Paste Synthetic Sample Bulletin (SHAKTI)", use_container_width=True):
                    st.session_state["raw_bulletin_input"] = sample_imd_bulletin_text
                    st.rerun()
            with col_b2:
                if st.button("🧹 Clear Bulletin Field", use_container_width=True):
                    st.session_state["raw_bulletin_input"] = ""
                    st.rerun()

            bulletin_val = st.session_state.get("raw_bulletin_input", "")
            raw_input = st.text_area("Paste Raw IMD Text Bulletin:", value=bulletin_val, height=140, placeholder="Paste IMD bulletin text here...")
            
            p_btn1, p_btn2 = st.columns([1.2, 1.0])
            with p_btn1:
                run_gemini_parse = st.button("✨ Parse with Gemini (Regex fallback)", type="primary", use_container_width=True)
            with p_btn2:
                run_regex_parse = st.button("🔄 Fast Regex Parse", use_container_width=True)

            if (run_gemini_parse or run_regex_parse) and raw_input.strip():
                with st.spinner("Parsing bulletin with Google Gemini / regex engine..."):
                    p_df, p_meta = None, {}
                    if run_gemini_parse and parse_imd_bulletin_gemini:
                        p_df, p_meta = parse_imd_bulletin_gemini(raw_input, api_key=active_gemini_key)
                    elif parse_imd_bulletin_text:
                        p_df, p_meta = parse_imd_bulletin_text(raw_input)
                        if p_meta:
                            p_meta["engine"] = "🛡️ Calibrated Regex Parser"

                    if p_df is not None and not p_df.empty:
                        st.session_state["custom_track_df"] = p_df
                        st.session_state["custom_track_meta"] = p_meta
                        eng_badge = p_meta.get("engine", "Parser Engine")
                        st.success(f"✅ Ingested {len(p_df)} track waypoints for Cyclone {p_meta.get('name','Alert')} ({p_meta.get('category','Storm')})! [{eng_badge}]")
                        st.dataframe(p_df, use_container_width=True, hide_index=True)
                        st.rerun()
                    else:
                        st.error(f"Could not parse bulletin: {p_meta.get('error', 'Invalid format')}")

        with ingest_t3:
            st.markdown("<div style='font-size:12.5px; color:#cbd5e1; margin-bottom:8px;'><b>Interactive Coastal Landfall Simulator</b>: Model an arbitrary custom cyclone approaching any coastal district.</div>", unsafe_allow_html=True)
            c_d1, c_d2 = st.columns(2)
            with c_d1:
                target_dist_options = [d["district_name"] for d in state_districts] if state_districts else ["Visakhapatnam", "Puri", "South 24 Parganas"]
                sim_target_dist = st.selectbox("Target Landfall District:", options=target_dist_options, index=0)
                sim_wind = st.slider("Peak Landfall Wind Speed (knots):", 35, 140, 75, 5, help="1 knot ≈ 1.852 km/h")
            with c_d2:
                sim_pres = st.slider("Minimum Central Pressure (hPa / mb):", 910, 995, 970, 2, help="Lower central pressure produces higher storm surge inundation.")
                sim_name = st.text_input("Assigned Storm Name:", value="CYCLONE-ALPHA")
            
            # Find coordinates for selected target district
            t_lat, t_lon = 20.0, 86.0
            for d in state_districts:
                if d.get("district_name") == sim_target_dist:
                    t_lat = float(d.get("lat", 20.0))
                    t_lon = float(d.get("lon", 86.0))
                    break
            
            if st.button(f"🛠️ Synthesize Landfall Trajectory on {sim_target_dist}", type="primary", use_container_width=True):
                if build_custom_approach_track:
                    b_df, b_meta = build_custom_approach_track(
                        landfall_lat=t_lat,
                        landfall_lon=t_lon,
                        peak_wind_kts=float(sim_wind),
                        min_pressure_mb=float(sim_pres),
                        storm_name=sim_name
                    )
                    st.session_state["custom_track_df"] = b_df
                    st.session_state["custom_track_meta"] = b_meta
                    st.success(f"✅ Synthesized 5-waypoint approach trajectory for {sim_name}!")
                    st.rerun()

        with ingest_t4:
            st.markdown("<div style='font-size:12.5px; color:#cbd5e1; margin-bottom:8px;'><b>Upload IMD CSV Track</b>: Columns required: <code>time, lat, lon, wind_kts, pressure_mb</code>.</div>", unsafe_allow_html=True)
            uploaded_csv = st.file_uploader("Upload IMD Track CSV File:", type=["csv"])
            if uploaded_csv:
                try:
                    c_df = pd.read_csv(uploaded_csv)
                    st.session_state["custom_track_df"] = c_df
                    st.session_state["custom_track_meta"] = {
                        "name": uploaded_csv.name.replace(".csv", "").upper()[:12],
                        "category": "Very Severe Cyclonic Storm" if float(c_df["wind_kts"].max()) >= 64 else "Cyclonic Storm",
                        "peak_wind_kts": float(c_df["wind_kts"].max()),
                        "min_pressure_mb": float(c_df["pressure_mb"].min()),
                        "landfall_location": f"{selected_state} Coastline",
                        "data_source": f"CSV Upload ({uploaded_csv.name})"
                    }
                    st.success(f"Ingested {len(c_df)} track points from `{uploaded_csv.name}`!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error parsing uploaded CSV: {e}")

        # Active Ingestion Ribbon & Reset Button
        if "custom_track_df" in st.session_state and st.session_state["custom_track_df"] is not None:
            c_meta = st.session_state.get("custom_track_meta", {})
            c_df_len = len(st.session_state["custom_track_df"])
            c_name = c_meta.get("name", "LIVE-IMD")
            st.markdown(f"""
            <div style="background:rgba(16,185,129,0.15); border:1px solid rgba(16,185,129,0.4); border-radius:8px; padding:10px 14px; margin-top:12px; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px;">
                <div>
                    <span style="font-size:12px; font-weight:800; color:#34d399;">🌊 ACTIVE INGESTED SYSTEM: {c_name}</span>
                    <span style="font-size:12px; color:#f1f5f9; margin-left:8px;">{c_meta.get('category','Cyclonic Storm')} · Peak: <b>{c_meta.get('peak_wind_kts',0):.0f} kts</b> · Pres: <b>{c_meta.get('min_pressure_mb',0):.0f} mb</b> · <b>{c_df_len} Waypoints</b></span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("🧹 Clear Ingested System (Revert to Default)", use_container_width=False):
                st.session_state["custom_track_df"] = None
                st.session_state["custom_track_meta"] = None
                st.rerun()

    custom_track_df = st.session_state.get("custom_track_df")




# ==============================================================================
# 4. Load Cyclone Track Data & Landfall Parameters
# ==============================================================================

# Load Track Data
if is_custom_track and custom_track_df is not None and not custom_track_df.empty:
    active_track_df = custom_track_df
    c_meta = st.session_state.get("custom_track_meta") or {}
    max_w = float(custom_track_df["wind_kts"].max())
    min_p = float(custom_track_df["pressure_mb"].min())
    s_name = c_meta.get("name", "LIVE-IMD")
    active_meta = {
        "name": s_name,
        "category": c_meta.get("category", ("Very Severe Cyclonic Storm" if max_w >= 64 else "Cyclonic Storm")),
        "peak_wind_kts": float(c_meta.get("peak_wind_kts", max_w)),
        "min_pressure_mb": float(c_meta.get("min_pressure_mb", min_p)),
        "landfall_location": c_meta.get("landfall_location", f"{selected_state} Coastline"),
        "landfall_time": str(custom_track_df["time"].iloc[-1]),
        "total_observations": len(custom_track_df),
        "data_source": c_meta.get("data_source", "Configured scenario / historical track")
    }
    selected_storm_name = s_name
else:
    active_track_df, active_meta = load_cyclone_track_data(selected_storm_name, selected_state)
    if not active_meta:
        # Fallback values from dictionary
        storm_specs = next((c for c in STATE_CYCLONES.get(selected_state, []) if c["name"] == selected_storm_name), {})
        active_meta = {
            "name": selected_storm_name,
            "category": storm_specs.get("category", "Severe Cyclonic Storm"),
            "peak_wind_kts": storm_specs.get("wind_kts", 65.0),
            "min_pressure_mb": storm_specs.get("pres_mb", 980.0),
            "landfall_location": storm_specs.get("landfall", f"{selected_state} Coast"),
            "landfall_time": f"{storm_specs.get('year', 2024)}-05-28 06:00:00",
            "total_observations": len(active_track_df) if not active_track_df.empty else 40,
            "data_source": "NOAA IBTrACS v4 Local Cache"
        }

# Landfall & Metric Constants
peak_wind = float(active_meta.get("peak_wind_kts", 60.0))
min_pres = float(active_meta.get("min_pressure_mb", 977.0))
# Jelesnianski inverted barometer proxy: Surge (m) ~ 0.099 * (1013 - P_min)
calc_surge_m = max(1.0, round(0.099 * (1013.0 - min_pres), 2))
landfall_loc = active_meta.get("landfall_location", f"{selected_state} Coastal Sector")
landfall_time = active_meta.get("landfall_time", "Within 24 Hours")

# Compute District Vulnerability Matrix for Selected State & Cyclone
@st.cache_data
def compute_state_district_vulnerability(
    state_name: str,
    storm_name: str,
    peak_wind_kts: float,
    peak_surge_m: float,
    track_df: pd.DataFrame
) -> pd.DataFrame:
    """Scores each district from the storm track using IMD wind classes and IMD/NDMA colour bands (see risk_engine.py)."""
    loaded_districts = load_all_coastal_districts()
    state_clean = state_name.strip().lower()
    dists = [
        d for d in loaded_districts 
        if d.get("state_or_division", "").strip().lower() == state_clean
    ]
    if not dists:
        dists = STATE_FALLBACK_DISTRICTS.get(state_name, STATE_FALLBACK_DISTRICTS.get("West Bengal", []))

    state_defaults = {
        "West Bengal": (22.15, 88.55),
        "Odisha": (20.30, 86.20),
        "Andhra Pradesh": (16.50, 81.80),
        "Tamil Nadu": (12.20, 79.90),
        "Gujarat": (22.30, 69.80)
    }
    fallback_coord = state_defaults.get(state_name, (20.5, 85.0))
    dists = [
        {**d, "lat": d.get("lat") if d.get("lat") is not None else fallback_coord[0],
         "lon": d.get("lon") if d.get("lon") is not None else fallback_coord[1]}
        for d in dists
    ]
    return compute_district_risk(
        dists,
        track_df,
        state_name,
        fallback_wind_kts=peak_wind_kts,
        fallback_pressure_mb=1013.0 - peak_surge_m / 0.099,
        facilities=load_facilities(os.path.join(DATA_DIR, "osm_infrastructure_baseline.geojson")),
        fallback_point=fallback_coord,
    )

state_vuln_df = compute_state_district_vulnerability(
    selected_state, selected_storm_name, peak_wind, calc_surge_m, active_track_df
)

# Total Exposure Statistics
total_pop_at_risk = int(state_vuln_df["population"].sum())
crit_districts = (state_vuln_df["threat_tier"] == "CRITICAL").sum()
total_flooded_roads = round(float(state_vuln_df["submerged_road_km"].sum()), 1)
total_flooded_hosps = int(state_vuln_df["flooded_hospitals"].sum())
total_flooded_shelters = int(state_vuln_df["flooded_shelters"].sum())
total_flooded_power = int(state_vuln_df["flooded_power_substations"].sum()) if "flooded_power_substations" in state_vuln_df.columns else 0

# Parametric insurance — evaluate state-level trigger
_ins_result = None
if evaluate_parametric_trigger:
    try:
        _ins_result = evaluate_parametric_trigger(
            wind_kts=peak_wind,
            surge_m=calc_surge_m,
            state_name=selected_state
        )
    except Exception:
        _ins_result = None


# ==============================================================================
# 4. Situation at a Glance (Executive Plain-Language Card)
# ==============================================================================

# Determine overall storm threat tier
if peak_wind >= 90 or calc_surge_m >= 3.0:
    overall_threat_level = "CRITICAL / CATASTROPHIC"
    overall_badge_class = "badge-critical"
    overall_color = "#ef4444"
elif peak_wind >= 64 or calc_surge_m >= 2.0:
    overall_threat_level = "HIGH RISK"
    overall_badge_class = "badge-high"
    overall_color = "#f97316"
else:
    overall_threat_level = "MODERATE RISK"
    overall_badge_class = "badge-moderate"
    overall_color = "#f59e0b"

top_dist_name = state_vuln_df.iloc[0]["district_name"] if not state_vuln_df.empty else selected_state
top_directive = state_vuln_df.iloc[0]["action_directive"] if not state_vuln_df.empty else "Review possible preparedness actions for low-lying areas."

render_html(f"""
    <div class="situation-card" style="border-left-color: {overall_color};">
    <div style="display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap; gap:12px;">
    <div>
    <div style="font-size:12px; font-weight:700; color:#38bdf8; text-transform:uppercase; letter-spacing:0.8px;">
        {'🧭 CUSTOM TRACK SCENARIO • SCREENING OUTPUTS' if is_custom_track else '🚨 SITUATION AT A GLANCE • SCENARIO SCREENING'}
    </div>
    <h2 style="margin:4px 0 6px 0; font-size:24px; font-weight:800; color:#f8fafc;">
        Cyclone {selected_storm_name.upper()} • {selected_state.upper()}
    </h2>
    <div style="font-size:14px; color:#cbd5e1; line-height:1.5;">
        📍 <b>Where the storm is expected to hit</b>: <span style="color:#f8fafc; font-weight:700;">{landfall_loc}</span> ({landfall_time})<br>
        👥 <b>People living in the districts shown</b>: <span style="color:#38bdf8; font-weight:700;">{total_pop_at_risk/1000000:.1f} Million</span> across <b>{len(state_vuln_df)} Coastal Districts</b><br>
        <span style="font-size:12px; color:#94a3b8;">📡 Data Provenance: <b style="color:#38bdf8;">{active_meta.get('data_source', 'NOAA IBTrACS v4 Archive')}</b></span>
    </div>
    </div>
    <div style="text-align:right;">
        <span class="{overall_badge_class}" style="font-size:14px; padding:6px 14px;">
        ● {overall_threat_level}
        </span>
        <div style="font-size:12.5px; color:#94a3b8; margin-top:6px;">
        Max Winds: <b style="color:#f8fafc;">{peak_wind:.0f} kts ({peak_wind*1.852:.0f} km/h)</b> • Surge: <b style="color:#38bdf8;">{calc_surge_m:.2f} m</b>
        </div>
    </div>
    </div>
    <div class="directive-box" style="margin-top:14px; margin-bottom:4px;">
    <div style="font-size:12px; font-weight:800; color:#ef4444; text-transform:uppercase; letter-spacing:0.8px; margin-bottom:4px;">
        ⚠️ POSSIBLE PREPAREDNESS ACTIONS — FOR AUTHORIZED REVIEW:
    </div>
    <div style="font-size:13.5px; color:#f1f5f9; line-height:1.5;">
        1. <b>Review evacuation needs ({top_dist_name})</b>: {top_directive}<br>
        2. <b>Review route contingencies</b>: Consider access options along modeled coastal highway exposure ({total_flooded_roads:.1f} km screening estimate).<br>
        3. <b>Review healthcare continuity</b>: Consider backup power and other facility-continuity plans using locally verified information.
    </div>
    </div>
    </div>
    """)


# ==============================================================================
# 5. Strategic KPI Ribbon (Plain-Language with Context Tooltips)
# ==============================================================================
kpi_cols = st.columns(6)

with kpi_cols[0]:
    render_html(f"""
    <div class="kpi-card" title="The strongest steady wind the storm is producing. Sustained winds above 64 knots (120 km/h) qualify as a Very Severe Cyclonic Storm on the Indian scale.">
        <div class="kpi-label">Peak Sustained Wind</div>
        <div class="kpi-value" style="color:#ef4444;">{peak_wind:.0f} kts</div>
        <div class="kpi-sub">≈ {peak_wind*1.852:.0f} km/h · {active_meta.get('category', 'Severe Storm').split('(')[0].strip()}</div>
    </div>
    """)

with kpi_cols[1]:
    render_html(f"""
    <div class="kpi-card" title="Air pressure at the centre of the storm eye. A lower number means a more powerful storm. Normal sea-level pressure is 1013 hPa — the bigger the gap, the more destructive the winds.">
        <div class="kpi-label">Storm Eye Pressure</div>
        <div class="kpi-value">{min_pres:.0f} hPa</div>
        <div class="kpi-sub">↓ {1013.0-min_pres:.0f} hPa below normal sea-level pressure</div>
    </div>
    """)

with kpi_cols[2]:
    render_html(f"""
    <div class="kpi-card" title="How high the sea will rise above its normal level because the storm's winds push water ashore. Even 1 metre of surge can submerge entire coastal villages.">
        <div class="kpi-label">Peak Coastal Surge</div>
        <div class="kpi-value" style="color:#38bdf8;">{calc_surge_m:.2f} m</div>
        <div class="kpi-sub">Seawater rise above normal tide <span class="source-badge-est" title="Calculated from the barometric pressure difference — a fast estimate. A full physics simulation (SLOSH model) is on the roadmap.">Estimated</span></div>
    </div>
    """)

with kpi_cols[3]:
    render_html(f"""
    <div class="kpi-card" title="Total length of main roads (state and national highways) expected to be submerged by floodwater, blocking ambulances and rescue trucks from reaching coastal villages.">
        <div class="kpi-label">Flooded & Cut-Off Roads</div>
        <div class="kpi-value" style="color:#f97316;">{total_flooded_roads:.1f} km</div>
        <div class="kpi-sub">Main roads impassable for emergency vehicles</div>
    </div>
    """)

with kpi_cols[4]:
    render_html(f"""
    <div class="kpi-card" title="Hospitals and cyclone shelters expected to flood. Flooded hospitals cannot admit patients; flooded shelters cannot protect evacuees — both need contingency plans now.">
        <div class="kpi-label">Flooded Hospitals & Shelters</div>
        <div class="kpi-value" style="color:#ef4444;">{total_flooded_hosps} Hospitals / {total_flooded_shelters} Shelters</div>
        <div class="kpi-sub">{'Facilities below modelled surge level' if state_vuln_df["facility_data_available"].any() else 'No facility inventory for this state'}</div>
    </div>
    """)

with kpi_cols[5]:
    _ins_label = "NO TRIGGER"
    _ins_color = "#3b82f6"
    _ins_payout = "₹ 0 Cr"
    if _ins_result and _ins_result.is_triggered:
        _ins_label = f"TIER {_ins_result.active_tier} — {_ins_result.tier_name}"
        _ins_color = _ins_result.color
        _ins_payout = f"₹ {_ins_result.payout_amount_cr:.0f} Cr"
    render_html(f"""
    <div class="kpi-card" title="Illustrative parametric insurance trigger calculation using configured scenario values. This is not an active policy or payment.">
        <div class="kpi-label">Parametric Insurance Trigger</div>
        <div class="kpi-value" style="color:{_ins_color}; font-size:17px;">{_ins_label}</div>
        <div class="kpi-sub">Example payout calculation: <b style="color:#f8fafc;">{_ins_payout}</b> · No funds released</div>
    </div>
    """)

render_html("<div style='height: 12px;'></div>")



# ==============================================================================
# 6. Master Step-by-Step Navigation Tabs
# ==============================================================================

tab_geo, tab_voice, tab_vision, tab_matrix, tab_sim, tab_insurance, tab_met, tab_tech = st.tabs([
    "🗺️ 1. Situation & Hazard Maps",
    "📢 2. Voice Alerts & Broadcast Hub",
    "📸 3. Ground Damage Photo Triage",
    "📊 4. Multi-District Risk Matrix",
    "🌪️ 5. What-If Landfall Scenario Modeler",
    "💰 6. Emergency Relief Funds Dashboard",
    "🌤️ 7. Real-Time Met Feed",
    "🛰️ 8. Technical Architecture & Evaluator Audit"
])


# ==============================================================================
# TAB 1: Scenario Map & District Review
# ==============================================================================
with tab_geo:
    district_list = state_vuln_df["district_name"].tolist() if not state_vuln_df.empty else ["Coastal Sector"]
    inspect_key = f"sel_district_inspect_{selected_state}"
    if inspect_key not in st.session_state or st.session_state[inspect_key] not in district_list:
        st.session_state[inspect_key] = district_list[0] if district_list else "Coastal Sector"
    current_inspect_dist = st.session_state.get(inspect_key, district_list[0] if district_list else None)

    geo_left, geo_right = st.columns([1.55, 1.0], gap="medium")

    with geo_left:
        st.markdown("""
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
            <div style="font-size:16px; font-weight:700; color:#38bdf8; display:flex; align-items:center; gap:8px;">
                <span>🗺️</span> Interactive Multi-Hazard Geospatial Intelligence Viewport
            </div>
            <div style="display:flex; gap:6px; align-items:center; flex-wrap:wrap;">
                <span class="badge-google" title="Google Earth Engine: Uses satellite ground height maps to check which coastal areas, villages, and hospitals are too low and likely to get flooded by rising sea water.">🌍 Google Earth Engine (GEE)</span>
                <span class="badge-google" title="Google Satellite Maps: Clear aerial satellite view of the coastline, villages, and main evacuation roads.">🗺️ Google Satellite Cartography</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Map Selector
        map_layer_options = [
            "🏥 District Risk & Critical Lifelines (Recommended)",
            "🚧 Road Access Screening & Evacuation Corridors",
            "🌊 Areas at Risk of Sea Water Flooding",
            "🌪️ Areas Hit by Damaging Winds",
            "🗺️ Cyclone Track & Landfall Eye Timeline"
        ]
        chosen_layer = st.selectbox(
            "Select Map Layer:",
            options=map_layer_options,
            index=0,
            label_visibility="collapsed",
            help="Choose a scenario layer to review. Flood and wind layers show screening estimates, not verified impacts; the cyclone track reflects the selected scenario input."
        )

        # Dynamic Folium Map Builder
        def render_dynamic_folium_map(
            districts_df: pd.DataFrame,
            track_df: pd.DataFrame,
            layer_type: str,
            state: str,
            inspect_district: Optional[str] = None
        ) -> str:
            state_coords = {
                "West Bengal": (22.20, 88.40),
                "Odisha": (20.30, 86.20),
                "Andhra Pradesh": (16.50, 81.80),
                "Tamil Nadu": (11.80, 79.80),
                "Gujarat": (22.30, 70.00)
            }
            st_lat, st_lon = state_coords.get(state, (20.5, 85.0))

            # 1. Determine Map Centering
            c_lat, c_lon = st_lat, st_lon
            zoom_lvl = 7
            if inspect_district and not districts_df.empty:
                m_row = districts_df[districts_df["district_name"] == inspect_district]
                if not m_row.empty and pd.notna(m_row["lat"].iloc[0]):
                    c_lat = float(m_row["lat"].iloc[0])
                    c_lon = float(m_row["lon"].iloc[0])
                    zoom_lvl = 8
            elif not districts_df.empty and "lat" in districts_df.columns:
                valid_d = districts_df[districts_df["lat"].notna() & (districts_df["lat"] > 0)]
                if not valid_d.empty:
                    c_lat = float(valid_d["lat"].mean())
                    c_lon = float(valid_d["lon"].mean())

            # 2. Determine Genuine Landfall Point along Track
            landfall_pt = [st_lat, st_lon]
            track_pts = []
            if not track_df.empty and "lat" in track_df.columns:
                valid_t = track_df[track_df["lat"].notna() & track_df["lon"].notna()]
                in_box = valid_t[(valid_t["lat"] >= 6) & (valid_t["lat"] <= 26) & (valid_t["lon"] >= 65) & (valid_t["lon"] <= 95)]
                use_t = in_box if not in_box.empty else valid_t
                if not use_t.empty:
                    dists = (use_t["lat"] - st_lat)**2 + (use_t["lon"] - st_lon)**2
                    min_idx = dists.idxmin()
                    landfall_pt = [float(use_t.loc[min_idx, "lat"]), float(use_t.loc[min_idx, "lon"])]
                    track_pts = [[float(r["lat"]), float(r["lon"])] for _, r in use_t.iterrows()]

            # 3. Initialize Folium Map with Verified Working Tiles
            m = folium.Map(
                location=[c_lat, c_lon],
                zoom_start=zoom_lvl,
                tiles="OpenStreetMap",
                name="OpenStreetMap Standard"
            )
            folium.TileLayer(
                tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
                attr="Esri World Imagery",
                name="Satellite Hybrid"
            ).add_to(m)

            # 4. Layer-Specific Features
            if "Road Access Screening" in layer_type:
                coords_list = []
                for _, d in districts_df.iterrows():
                    if pd.notna(d.get("lat")) and pd.notna(d.get("lon")):
                        coords_list.append((float(d["lat"]), float(d["lon"]), d["district_name"], float(d.get("submerged_road_km", 0.0)), d.get("threat_tier", "MODERATE")))
                coords_list.sort(key=lambda x: x[0])

                for i in range(len(coords_list) - 1):
                    p1, p2 = coords_list[i], coords_list[i+1]
                    cut_km = max(p1[3], p2[3])
                    tier = "CRITICAL" if (p1[4] == "CRITICAL" or p2[4] == "CRITICAL") else ("HIGH" if (p1[4] == "HIGH" or p2[4] == "HIGH") else "MODERATE")
                    if cut_km >= 10.0 or tier == "CRITICAL":
                        r_col, r_stat, r_wt, r_dash = "#ef4444", f"SCENARIO SCREENING: elevated access risk ({cut_km:.1f} km estimated)", 5, None
                    elif cut_km > 0.0 or tier == "HIGH":
                        r_col, r_stat, r_wt, r_dash = "#f97316", f"SCENARIO SCREENING: possible access disruption ({cut_km:.1f} km estimated)", 4, "6, 6"
                    else:
                        r_col, r_stat, r_wt, r_dash = "#10b981", "SCENARIO SCREENING: lower modeled risk; passability not verified", 4, None

                    folium.PolyLine(
                        [[p1[0], p1[1]], [p2[0], p2[1]]],
                        color=r_col, weight=r_wt, dash_array=r_dash, opacity=0.9,
                        tooltip=f"<b>Illustrative route between {p1[2]} ↔ {p2[2]}</b><br>{r_stat}<br>Not a verified road condition."
                    ).add_to(m)

                for _, d in districts_df.iterrows():
                    d_lat, d_lon = float(d.get("lat", c_lat)), float(d.get("lon", c_lon))
                    folium.CircleMarker(
                        [d_lat, d_lon], radius=7, color="#38bdf8", fill=True, fill_color="#0f172a", fill_opacity=0.9,
                        tooltip=f"<b>{d['district_name']} Road Access Screening</b><br>Estimated affected road length: {d.get('submerged_road_km',0):.1f} km; not field-verified."
                    ).add_to(m)

            elif "Areas at Risk of Sea Water Flooding" in layer_type:
                for _, d in districts_df.iterrows():
                    d_lat, d_lon = float(d.get("lat", c_lat)), float(d.get("lon", c_lon))
                    d_tier = d.get("threat_tier", "MODERATE")
                    surge_r = 25000 if d_tier == "CRITICAL" else (16000 if d_tier == "HIGH" else 10000)
                    folium.Circle(
                        location=[d_lat, d_lon], radius=surge_r, color="#0284c7",
                        fill=True, fill_color="#38bdf8", fill_opacity=0.45, weight=2,
                        tooltip=f"<b>{d['district_name']} Scenario Screening Area</b><br>Surge estimate: <b>+{calc_surge_m:.2f} m</b>; not an observed inundation boundary."
                    ).add_to(m)
                    folium.CircleMarker(
                        [d_lat, d_lon], radius=6, color="#0369a1", fill=True, fill_color="#38bdf8", fill_opacity=0.9,
                        tooltip=f"🌊 Tide Gauge: {d['district_name']} (+{calc_surge_m:.2f}m Surge)"
                    ).add_to(m)

                folium.Marker(
                    landfall_pt, tooltip=f"🌊 Scenario surge estimate: +{calc_surge_m:.2f}m; not an observed boundary",
                    icon=folium.Icon(color="blue", icon="tint", prefix="fa")
                ).add_to(m)

            elif "Areas Hit by Damaging Winds" in layer_type:
                folium.Circle(
                    landfall_pt, radius=220000, color="#eab308", weight=1.5,
                    fill=True, fill_color="#eab308", fill_opacity=0.14,
                    tooltip="Peripheral Squall Zone (34–47 kts) • Radius: 220 km"
                ).add_to(m)
                folium.Circle(
                    landfall_pt, radius=120000, color="#f97316", weight=2,
                    fill=True, fill_color="#f97316", fill_opacity=0.25,
                    tooltip="Gale Force Destructive Zone (48–63 kts) • Radius: 120 km"
                ).add_to(m)
                folium.Circle(
                    landfall_pt, radius=60000, color="#ef4444", weight=2.5,
                    fill=True, fill_color="#ef4444", fill_opacity=0.40,
                    tooltip=f"Core Eyewall Swath (Peak: {peak_wind:.0f} kts / {peak_wind*1.852:.0f} km/h) • Radius: 60 km"
                ).add_to(m)
                folium.Marker(
                    landfall_pt, tooltip=f"🌪️ Cyclone Eyewall: {selected_storm_name} ({peak_wind:.0f} kts)",
                    icon=folium.Icon(color="red", icon="bullseye", prefix="fa")
                ).add_to(m)

                for _, d in districts_df.iterrows():
                    d_lat, d_lon = float(d.get("lat", c_lat)), float(d.get("lon", c_lon))
                    folium.CircleMarker(
                        [d_lat, d_lon], radius=6, color="#f97316", fill=True, fill_color="#0f172a", fill_opacity=0.8,
                        tooltip=f"<b>{d['district_name']}</b> (Risk: {d.get('vulnerability_score',50):.1f})"
                    ).add_to(m)

            elif "Cyclone Track" in layer_type:
                if track_pts:
                    folium.PolyLine(
                        track_pts, color="#38bdf8", weight=4, opacity=0.85,
                        tooltip=f"NOAA Official Cyclone Track: {selected_storm_name}"
                    ).add_to(m)
                    step = max(1, len(track_df) // 8)
                    for idx, (_, r) in enumerate(track_df.iloc[::step].iterrows()):
                        if pd.notna(r.get("lat")) and pd.notna(r.get("lon")):
                            t_lat, t_lon = float(r["lat"]), float(r["lon"])
                            w_val = float(r.get("wind_kts", 40.0))
                            p_val = float(r.get("pressure_mb", 990.0))
                            t_str = str(r.get("time", f"T+{idx*6}h"))[:16]
                            pt_col = "#ef4444" if w_val >= 64 else ("#f97316" if w_val >= 48 else "#38bdf8")
                            folium.CircleMarker(
                                [t_lat, t_lon], radius=5, color=pt_col, fill=True, fill_color=pt_col, fill_opacity=0.9,
                                tooltip=f"<b>{selected_storm_name} Observation</b><br>Time: {t_str}<br>Wind: {w_val:.0f} kts<br>Pressure: {p_val:.0f} mb"
                            ).add_to(m)

                    folium.Marker(
                        landfall_pt, tooltip=f"🎯 Landfall Sector: {selected_storm_name} (Peak Wind: {peak_wind:.0f} kts)",
                        icon=folium.Icon(color="red", icon="crosshairs", prefix="fa")
                    ).add_to(m)

                for _, d in districts_df.iterrows():
                    d_lat, d_lon = float(d.get("lat", c_lat)), float(d.get("lon", c_lon))
                    folium.CircleMarker(
                        [d_lat, d_lon], radius=6, color="#38bdf8", fill=True, fill_color="#0f172a", fill_opacity=0.8,
                        tooltip=f"<b>{d['district_name']}</b>"
                    ).add_to(m)

            else:
                # Default Layer: District Risk & Critical Lifelines
                for _, d in districts_df.iterrows():
                    d_lat = float(d.get("lat", c_lat))
                    d_lon = float(d.get("lon", c_lon))
                    d_tier = d.get("threat_tier", "MODERATE")
                    d_score = float(d.get("vulnerability_score", 50.0))
                    d_col = "#ef4444" if d_tier == "CRITICAL" else ("#f97316" if d_tier == "HIGH" else ("#f59e0b" if d_tier == "MODERATE" else "#3b82f6"))
                    is_selected = (inspect_district and d.get("district_name") == inspect_district)

                    folium.CircleMarker(
                        location=[d_lat, d_lon],
                        radius=14 if is_selected else (11 if d_tier == "CRITICAL" else 8),
                        color="#ffffff" if is_selected else d_col,
                        weight=3 if is_selected else 1.5,
                        fill=True, fill_color=d_col, fill_opacity=0.85,
                        tooltip=f"<b>{d['district_name']}</b><br>Risk: <b>{d_score:.1f}/100 ({d_tier})</b><br>Evacuation Priority: <b>{d['evacuation_priority']}</b><br>Flooded Hospitals: {d.get('flooded_hospitals',0)}<br>Road Cut: {d.get('submerged_road_km',0):.1f} km"
                    ).add_to(m)

                    if is_selected:
                        folium.Circle(
                            location=[d_lat, d_lon], radius=18000, color="#38bdf8", weight=2.5,
                            dash_array="5, 5", fill=True, fill_color="#38bdf8", fill_opacity=0.15,
                            tooltip=f"🎯 Inspected District: {d['district_name']}"
                        ).add_to(m)

                    fh = int(d.get("flooded_hospitals", 0))
                    if fh > 0:
                        folium.Marker(
                            [d_lat + 0.05, d_lon - 0.05],
                            tooltip=f"🏥 {d['district_name']}: {fh} Flooded Hospital(s)",
                            icon=folium.Icon(color="red", icon="plus", prefix="fa")
                        ).add_to(m)

                folium.Marker(
                    landfall_pt, tooltip=f"Eye Landfall: {selected_storm_name}",
                    icon=folium.Icon(color="red", icon="crosshairs", prefix="fa")
                ).add_to(m)

            folium.LayerControl(position="topright", collapsed=True).add_to(m)
            return m.get_root().render()

        # Render dynamic Folium map
        dyn_map_html = render_dynamic_folium_map(
            districts_df=state_vuln_df,
            track_df=active_track_df,
            layer_type=chosen_layer,
            state=selected_state,
            inspect_district=current_inspect_dist
        )
        components.html(dyn_map_html, height=580, scrolling=False)

        # Quick Plain-Language Cartographic Bar with honest GEE badge
        st.markdown("""
        <div style="display:flex; justify-content:space-between; font-size:12px; color:#cbd5e1; background:rgba(30,41,59,0.7); padding:8px 14px; border-radius:8px; margin-top:6px;">
            <div title="SRTM elevation via the configured geospatial path supports screening estimates. Earth Engine is optional geospatial processing, not a cyclone prediction service.">🗺️ <b>Elevation</b>: SRTM 30m <span style='background:#f59e0b22;color:#f59e0b;border:1px solid #f59e0b;border-radius:4px;padding:1px 6px;font-size:10px;'>Screening input</span></div>
            <div title="NOAA IBTrACS is a historical cyclone archive; the selected track source is shown in the scenario metadata.">🌪️ <b>Storm Tracks</b>: Historical / selected input <span style='background:#f59e0b22;color:#f59e0b;border:1px solid #f59e0b;border-radius:4px;padding:1px 6px;font-size:10px;'>Check source</span></div>
            <div title="OpenStreetMap-derived baseline or configured infrastructure data; this map does not imply a fresh live Overpass query.">🏥 <b>Infrastructure</b>: Configured OSM-derived data <span style='background:#f59e0b22;color:#f59e0b;border:1px solid #f59e0b;border-radius:4px;padding:1px 6px;font-size:10px;'>Baseline</span></div>
            <div title="Weather is requested separately. Check the status and retrieval time in the weather tab; this feed does not drive the displayed risk score.">🌤️ <b>Weather</b>: Separate forecast feed <span style='background:#f59e0b22;color:#f59e0b;border:1px solid #f59e0b;border-radius:4px;padding:1px 6px;font-size:10px;'>Check status</span></div>
        </div>
        """, unsafe_allow_html=True)

    # --------------------------------------------------------------------------
    # Right Column: District Deep-Dive Inspector & One-Click Broadcast
    # --------------------------------------------------------------------------
    with geo_right:
        st.markdown("""
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
            <div style="font-size:16px; font-weight:700; color:#38bdf8; display:flex; align-items:center; gap:8px;">
                <span>🧭</span> District Scenario Review & Possible Actions
            </div>
            <span class="source-badge-est" title="Configured district profile and scenario-based screening output; not live Gemini analysis or an official warning.">Scenario estimate</span>
        </div>
        """, unsafe_allow_html=True)

        sel_dist = st.selectbox(
            "Select Coastal District to Inspect:",
            options=district_list,
            index=district_list.index(current_inspect_dist) if current_inspect_dist in district_list else 0,
            key=inspect_key
        )

        # District Data Lookup
        dist_row = state_vuln_df[state_vuln_df["district_name"] == sel_dist].iloc[0] if not state_vuln_df.empty else {}
        d_score = float(dist_row.get("vulnerability_score", 75.0))
        d_tier = dist_row.get("threat_tier", "HIGH")
        d_prio = int(dist_row.get("evacuation_priority", 2))
        d_driver = dist_row.get("primary_risk_driver", "High Cyclone Exposure")
        d_action = dist_row.get("action_directive", "Review preparedness needs for low-lying areas.")
        d_pop = int(dist_row.get("population", 1500000))

        d_badge = "badge-critical" if d_tier == "CRITICAL" else ("badge-high" if d_tier == "HIGH" else "badge-moderate")
        d_border = "#ef4444" if d_tier == "CRITICAL" else ("#f97316" if d_tier == "HIGH" else "#38bdf8")

        # District Score Header Card
        st.markdown(f"""
        <div class="glass-panel" style="border-left: 5px solid {d_border}; padding:14px 18px; margin-bottom:12px;">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <div>
                    <h3 style="margin:0; font-size:22px; font-weight:800; color:#f8fafc;">{sel_dist}</h3>
                    <div style="font-size:13px; color:#94a3b8;">{selected_state}, India • Pop: <b>{d_pop/100000:.1f} Lakh</b> ({d_pop:,})</div>
                </div>
                <div style="text-align:right;">
                    <span class="{d_badge}" title="Scenario tier based on configured wind/surge scoring rules; not an official warning or observed impact.">● Scenario: {d_tier}</span>
                    <div style="font-size:20px; font-weight:800; color:#f8fafc; margin-top:4px;">
                        {d_score:.1f} <span style="font-size:12px; color:#94a3b8;">/ 100 scenario score</span>
                    </div>
                </div>
            </div>
            <div style="font-size:13px; color:#cbd5e1; margin-top:10px; border-top:1px solid rgba(148,163,184,0.2); padding-top:8px; line-height:1.4;">
                ⚠️ <b>What is dangerous here</b>: {d_driver}<br>
                🚨 <b>What officials should consider doing</b>: {d_action}
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Lifeline Metric Grid
        l1, l2, l3, l4 = st.columns(4)
        fh_val = int(dist_row.get("flooded_hospitals", 0))
        th_val = int(dist_row.get("total_hospitals", 6))
        fs_val = int(dist_row.get("flooded_shelters", 0))
        ts_val = int(dist_row.get("total_shelters", 14))
        sr_val = float(dist_row.get("submerged_road_km", 0.0))
        fp_val = int(dist_row.get("flooded_power_substations", 0))

        with l1:
            st.markdown(f"""
            <div style="background:rgba(15,23,42,0.7); padding:8px 10px; border-radius:8px; text-align:center; cursor:help;" title="Hospitals and shelters flagged by scenario rules; this is not a verified live flood assessment or operational status.">
                <div style="font-size:11px; color:#94a3b8;">HOSPITALS & SHELTERS FLAGGED</div>
                <div style="font-size:16px; font-weight:800; color:{'#ef4444' if fh_val>0 else '#10b981'};">{fh_val}/{th_val}</div>
                <div style="font-size:10.5px; color:#94a3b8;">{'Scenario flag' if fh_val>0 else 'No scenario flag'}</div>
            </div>
            """, unsafe_allow_html=True)
        with l2:
            st.markdown(f"""
            <div style="background:rgba(15,23,42,0.7); padding:8px 10px; border-radius:8px; text-align:center; cursor:help;" title="Shelters flagged by scenario rules; this does not establish current safety or operational status.">
                <div style="font-size:11px; color:#94a3b8;">SHELTERS FLAGGED</div>
                <div style="font-size:16px; font-weight:800; color:{'#ef4444' if fs_val>0 else '#10b981'};">{fs_val}/{ts_val}</div>
                <div style="font-size:10.5px; color:#94a3b8;">{'Scenario flag' if fs_val>0 else 'No scenario flag'}</div>
            </div>
            """, unsafe_allow_html=True)
        with l3:
            st.markdown(f"""
            <div style="background:rgba(15,23,42,0.7); padding:8px 10px; border-radius:8px; text-align:center; cursor:help;" title="Road exposure estimate for this scenario; verify access conditions with current local information.">
                <div style="font-size:11px; color:#94a3b8;">ROAD EXPOSURE ESTIMATE</div>
                <div style="font-size:16px; font-weight:800; color:{'#ef4444' if sr_val>0 else '#10b981'};">{sr_val:.1f} km</div>
                <div style="font-size:10.5px; color:#94a3b8;">Scenario estimate; verify locally</div>
            </div>
            """, unsafe_allow_html=True)
        with l4:
            st.markdown(f"""
            <div style="background:rgba(15,23,42,0.7); padding:8px 10px; border-radius:8px; text-align:center; cursor:help;" title="Substation exposure estimate; it does not establish current grid stability.">
                <div style="font-size:11px; color:#94a3b8;">SUBSTATION EXPOSURE</div>
                <div style="font-size:16px; font-weight:800; color:{'#ef4444' if fp_val>0 else '#10b981'};">{fp_val} Substations</div>
                <div style="font-size:10.5px; color:#94a3b8;">Scenario estimate; verify locally</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

        # Multi-Language Disaster Voice Broadcast Console
        st.markdown("""
        <div style="font-size:13px; font-weight:700; color:#38bdf8; margin-bottom:6px; display:flex; align-items:center; gap:6px;">
            <span>📢</span> Draft Scenario Message & Voice Preview — Not an Official Alert
        </div>
        """, unsafe_allow_html=True)

        # Advisory Text fallback
        sample_advisory_text = (
            f"EMERGENCY CYCLONE ADVISORY FOR {sel_dist.upper()}: Threat Level {d_tier}. "
            f"{d_driver}. {fh_val} hospitals and {sr_val:.1f} km of arterial roadway at risk. "
            f"Suggested action for local review: {d_action}"
        )

        # Determine regional target language from user's active choice or state default
        if active_lang_code in ["bn", "or", "te", "ta", "gu"]:
            r_code, r_label = active_lang_code, active_lang_label
        else:
            r_code, r_label = reg_code, reg_label

        voice_tabs = st.tabs([
            "🇬🇧 English",
            "🇮🇳 Hindi (हिंदी)",
            f"🏛️ {r_label}"
        ])

        voice_configs = [
            ("en", "English", voice_tabs[0]),
            ("hi", "Hindi (हिंदी)", voice_tabs[1]),
            (r_code, r_label, voice_tabs[2])
        ]

        for target_l_code, target_l_label, tab_obj in voice_configs:
            with tab_obj:
                # 1. Fetch localized broadcast text
                if get_localized_broadcast:
                    loc_payload = get_localized_broadcast(
                        district=sel_dist,
                        state=selected_state,
                        storm=selected_storm_name,
                        tier=d_tier,
                        score=d_score,
                        wind_kts=peak_wind,
                        surge_m=calc_surge_m,
                        action=d_action,
                        driver=d_driver,
                        hosp_cnt=fh_val,
                        road_km=sr_val,
                        lang=target_l_code
                    )
                    v_script = loc_payload.get("spoken", sample_advisory_text)
                else:
                    v_script = sample_advisory_text

                # 2. Check cached or existing audio
                cur_audio_path = None
                if get_audio_path:
                    cur_audio_path = get_audio_path(sel_dist, target_l_code, storm_name=selected_storm_name.lower())

                vc_1, vc_2 = st.columns([1.5, 1.0])
                with vc_1:
                    st.caption(f"🎙️ **Voice preview**: {target_l_label} • not transmitted")
                with vc_2:
                    v_btn = st.button(
                        f"🔊 Synthesize Voice",
                        key=f"synth_{sel_dist}_{target_l_code}_{selected_storm_name}",
                        use_container_width=True
                    )

                if v_btn and get_or_create_district_audio:
                    with st.spinner(f"Synthesizing broadcast in {target_l_label}..."):
                        p, t = get_or_create_district_audio(
                            sel_dist, target_l_code, v_script,
                            storm_name=selected_storm_name.lower(),
                            force=True
                        )
                        if p and os.path.exists(p):
                            cur_audio_path = p
                            st.rerun()

                # Stream audio if available
                if cur_audio_path and os.path.exists(cur_audio_path) and os.path.getsize(cur_audio_path) > 1000:
                    with open(cur_audio_path, "rb") as af:
                        st.audio(af.read(), format="audio/mp3")
                else:
                    if get_or_create_district_audio:
                        try:
                            p, t = get_or_create_district_audio(
                                sel_dist, target_l_code, v_script,
                                storm_name=selected_storm_name.lower(),
                                force=False
                            )
                            if p and os.path.exists(p) and os.path.getsize(p) > 1000:
                                with open(p, "rb") as af:
                                    st.audio(af.read(), format="audio/mp3")
                        except Exception:
                            st.info(f"Audio broadcast ready. Click 'Synthesize Voice' to stream {target_l_label} voice.")

                with st.expander(f"📄 Spoken Broadcast Script ({target_l_label})", expanded=False):
                    st.markdown(f"> {v_script}")

    render_explanation(
        "How does Situation & Hazard Mapping work?",
        {
            "what": "The map brings cyclone tracks, hazard layers, and critical infrastructure together so teams can see which coastal areas may need closer attention.",
            "how": [
                "Choose a state and cyclone scenario — the dashboard loads the selected track and district data.",
                "Select a map layer: district risk & lifelines, impassable highways, surge zones, wind swaths, or the cyclone track timeline.",
                "Compare exposed places using terrain elevation and mapped roads, hospitals, and shelters to identify where flooding or loss of access could matter.",
                "Inspect individual districts — the side panel shows scenario-based risk scores and infrastructure indicators for the selected area."
            ],
            "benefit": "Officials can use one view to identify areas, roads, hospitals, or shelters that may deserve field checks or preparedness planning before landfall.",
            "tech": [
                "Google Earth Engine / SRTM elevation data — supports terrain and exposure screening (when authenticated).",
                "OpenStreetMap-derived infrastructure baseline — supplies mapped roads and facilities where available.",
                "Interactive Folium map layers — display cyclone tracks and selected hazard overlays.",
                "NOAA IBTrACS historical tracks / configured scenarios — provide the storm track input."
            ],
            "limitations": "The cyclone track reflects the selected scenario (historical, synthetic, or user-supplied), not a live satellite feed. Surge and wind layers are screening estimates based on simplified physics proxies, not verified impacts or official forecasts. Infrastructure data is from a configured OSM-derived baseline, not a live Overpass query.",
            "note": "Live ingestion of IMD/RSMC bulletins would need to be connected for real-time use. All displayed layers are decision-support aids, not confirmation of ground conditions."
        },
        icon="🗺️"
    )



# ==============================================================================
# TAB 2: Voice Alerts & Broadcast Hub (Multi-Channel Delivery & CAP Export)
# ==============================================================================
with tab_voice:
    st.markdown("""
    <div style="display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap; gap:8px; margin-bottom:4px;">
        <div style="font-size:18px; font-weight:800; color:#38bdf8; display:flex; align-items:center; gap:8px;">
            <span>📢</span> Multi-Channel Disaster Alert Delivery & Common Alerting Protocol (CAP) Hub
        </div>
        <div style="display:flex; gap:6px; flex-wrap:wrap;">
            <span class="badge-google" title="Google Gemini AI: Translates urgent life-saving warning messages into natural everyday speech in 7 local Indian languages (Bengali, Hindi, Odia, etc.).">✨ Google Gemini Emergency Translations</span>
            <span class="badge-google" title="Google Cloud Voice: Converts warning text into clear spoken voice announcements for radio broadcasts and loudspeaker vans.">🔊 Google Cloud Text-to-Speech</span>
        </div>
    </div>
    <div style="font-size:13px; color:#cbd5e1; margin-bottom:14px;">
        Pre-formatted, copy-ready emergency broadcast messages for <b>SMS (160-char)</b>, <b>WhatsApp</b>, <b>Community Radio</b>, and <b>OASIS CAP 1.2 XML</b> for State Disaster Management Authorities.
    </div>
    """, unsafe_allow_html=True)

    v_left, v_right = st.columns([1.1, 1.0], gap="large")

    with v_left:
        if active_lang_code == "bn":
            message_section_title = "📱 পরিস্থিতিভিত্তিক খসড়া বার্তা (বাংলা)"
            message_preview_notice = (
                "এটি শুধুমাত্র প্রস্তুত করা বার্তার প্রিভিউ। এটি কোনো সরকারি সতর্কবার্তা নয় এবং "
                "পাঠানো হয়নি; ব্যবহারের আগে সব তথ্য যাচাই করুন এবং সংশ্লিষ্ট কর্তৃপক্ষের অনুমোদন নিন।"
            )
        else:
            message_section_title = f"📱 Draft Scenario Messages ({active_lang_label})"
            message_preview_notice = (
                "Prepared message preview only. Not an official warning and not transmitted; "
                "verify all details and obtain agency approval before any use."
            )
        st.markdown(
            f"<div style='font-size:14px; font-weight:700; color:#38bdf8; margin-bottom:8px;'>{message_section_title}</div>",
            unsafe_allow_html=True
        )
        st.warning(message_preview_notice)
        
        if get_localized_broadcast:
            tab2_loc = get_localized_broadcast(
                district=sel_dist,
                state=selected_state,
                storm=selected_storm_name,
                tier=d_tier,
                score=d_score,
                wind_kts=peak_wind,
                surge_m=calc_surge_m,
                action=d_action,
                driver=d_driver,
                hosp_cnt=fh_val,
                road_km=sr_val,
                lang=active_lang_code
            )
            sms_text = tab2_loc.get("sms", "")
            whatsapp_text = tab2_loc.get("whatsapp", "")
            pa_text = tab2_loc.get("pa", "")
        else:
            sms_text = f"DRAFT SCENARIO: Cyclone {selected_storm_name} near {landfall_loc}. {sel_dist}: {d_tier} screening estimate. Verify current official guidance before acting."[:160]
            whatsapp_text = f"""*DRAFT SCENARIO MESSAGE — NOT AN OFFICIAL ALERT*
Cyclone {selected_storm_name.upper()}
*District*: {sel_dist}, {selected_state}
*Scenario screening tier*: {d_tier} (Score {d_score:.1f}/100)
*Scenario wind input*: {peak_wind:.0f} kts ({peak_wind*1.852:.0f} km/h)
*Estimated surge*: {calc_surge_m:.2f} meters

⚠️ *Possible action for authorized review*: {d_action}
Verify conditions, official guidance, and shelter status with local authorities.
_Prepared by CycloneShield for review — not sent_"""
            pa_text = f"Draft scenario message: Cyclone {selected_storm_name} near {sel_dist}. Check official local guidance and verified shelter information."

        # 1. SMS (160 characters limit)
        st.markdown(f"**1. Draft SMS (160 Characters Max — {active_lang_label}):**")
        st.code(sms_text, language="text")

        # 2. WhatsApp Emergency Broadcast
        st.markdown(f"**2. Draft WhatsApp Message (Formatted — {active_lang_label}):**")
        st.code(whatsapp_text, language="markdown")

        # 3. Community Radio & Megaphone Broadcast Script
        st.markdown(f"**3. Community Radio / Public Address Announcement ({active_lang_label}):**")
        st.code(pa_text, language="text")

    with v_right:
        st.markdown("<div style='font-size:14px; font-weight:700; color:#38bdf8; margin-bottom:8px;'>🏛️ Machine-Readable Emergency Alert File (International CAP Standard)</div>", unsafe_allow_html=True)
        
        advisory_payload = {
            "district_name": sel_dist,
            "state_or_division": selected_state,
            "threat_level": d_tier,
            "public_advisory_en": sample_advisory_text,
            "lifeline_impact_summary": f"{fh_val} flooded hospitals, {sr_val:.1f} km submerged roadway."
        }
        
        if export_cap_alert:
            cap_xml_data = export_cap_alert(advisory_payload, storm_name=selected_storm_name)
        else:
            cap_xml_data = f"<alert><identifier>CS-{selected_storm_name}-{sel_dist}</identifier></alert>"

        st.markdown("""
        <div style="background:rgba(15,23,42,0.6); border:1px solid rgba(56,189,248,0.25); border-radius:8px; padding:12px; margin-bottom:12px; font-size:12px; color:#cbd5e1;">
            <b>What is this file?</b> The <b>Common Alerting Protocol (CAP v1.2)</b> is an international standard format for emergency alerts used by governments worldwide. Clicking Download generates an XML file that can be directly fed into India's <b>SACHET</b> national alert gateway, Doordarshan broadcast systems, and cell-broadcast networks — <b>no manual re-typing needed</b>. Officials can upload this one file to trigger alerts across all channels simultaneously.
        </div>
        """, unsafe_allow_html=True)

        st.code(cap_xml_data[:650] + "\n  <!-- Complete OASIS CAP 1.2 Payload Formatted -->\n</alert>", language="xml")

        st.download_button(
            label=f"📥 Download CAP 1.2 XML Alert for {sel_dist}",
            data=cap_xml_data.encode("utf-8"),
            file_name=f"CAP_alert_{selected_storm_name.lower()}_{sel_dist.lower().replace(' ', '_')}.xml",
            mime="application/xml",
            use_container_width=True
        )

    render_explanation(
        "How do Voice Alerts and Broadcasts work?",
        {
            "what": "Prepares draft cyclone warning messages in multiple formats — SMS, WhatsApp, community radio scripts, and CAP 1.2 XML — with optional multilingual text and voice preview for officer review.",
            "how": [
                "Select the district and language — the app assembles an advisory using the current scenario's threat tier, wind, surge, and action guidance.",
                "Review copy-ready drafts for SMS (160-char), WhatsApp (formatted), and public address scripts.",
                "Generate a voice preview using text-to-speech when the voice service is available (click 'Synthesize Voice' to test).",
                "Download a CAP 1.2 XML file — a machine-readable alert format compatible with India's SACHET gateway and broadcast systems — for authorised upload."
            ],
            "benefit": "Officials can prepare consistent, locally relevant warnings across channels in minutes instead of drafting and translating each one by hand, helping communities understand and act sooner.",
            "tech": [
                "Google Gemini (optional) — translates and localizes advisory text when a live API response is confirmed.",
                "Google Cloud Text-to-Speech (optional) — generates spoken audio previews for supported languages when configured.",
                "CAP 1.2 XML export — produces a standard alert file for authorised systems (SACHET, cell broadcast, radio).",
                "Prepared offline templates and audio fallbacks — keep the workflow demonstrable when live services are unavailable."
            ],
            "limitations": "This tab prepares messages and files only; it does not transmit alerts to the public, send SMS/WhatsApp, or broadcast audio. All drafts require authorised review and approval before any use. Voice preview depends on the configured TTS service; offline fallback audio is pre-generated, not live synthesis.",
            "note": "Live delivery would require integration with SDMA SACHET, cell broadcast gateways, SMS providers, or All India Radio — each needing official approval and configuration."
        },
        icon="📢"
    )


# ==============================================================================
# Location + evidence helpers for Tab 3 (Gemini never judges location)
# ==============================================================================
LOCATION_SOURCE_LABELS = {
    "gps": "📡 GPS (photo EXIF)",
    "device": "📱 Device location",
    "manual": "✍️ Manual",
    "unverified": "⚠️ Unverified",
}


def get_device_coords(key: str) -> Optional[Tuple[float, float]]:
    """Ask the browser for its location (needs streamlit-js-eval); None until granted."""
    try:
        from streamlit_js_eval import get_geolocation
    except ImportError:
        st.caption("Device location needs the `streamlit-js-eval` package.")
        return None
    geo = get_geolocation(component_key=f"{key}_geo")
    coords = (geo or {}).get("coords") if isinstance(geo, dict) else None
    if not coords:
        st.caption("Waiting for browser location permission...")
        return None
    return float(coords["latitude"]), float(coords["longitude"])


def get_map_click(key: str) -> Optional[Tuple[float, float]]:
    """Let the operator click a point on a folium map (needs streamlit-folium)."""
    try:
        from streamlit_folium import st_folium
    except ImportError:
        return None
    fmap = folium.Map(location=[19.5, 82.0], zoom_start=5, tiles="CartoDB positron")
    folium.GeoJson(DISTRICTS_PATH, style_function=lambda _f: {"weight": 1, "fillOpacity": 0.05}).add_to(fmap)
    out = st_folium(fmap, height=320, key=f"{key}_map", returned_objects=["last_clicked"])
    click = (out or {}).get("last_clicked")
    return (click["lat"], click["lng"]) if click else None


def render_location_picker(photo_bytes: bytes, key: str) -> LocationResult:
    """Collect location inputs (EXIF > device > manual) and resolve them to a district."""
    st.markdown("**📍 Photo location** — set from GPS/device/operator input, never inferred by Gemini")
    device_coords = manual_coords = manual_id = None
    if extract_exif_gps(photo_bytes):
        st.caption("EXIF GPS found in the photo; it takes priority over other sources.")
    else:
        st.caption("No EXIF GPS in this photo. Use device location or pick a district.")
        if st.checkbox("Use this device's location (browser will ask permission)", key=f"{key}_dev"):
            device_coords = get_device_coords(key)
        districts = list_districts()
        by_id = {d["district_id"]: d for d in districts}
        manual_id = st.selectbox(
            "Or choose the district manually:",
            options=[None] + list(by_id),
            format_func=lambda i: "— not set —" if i is None else f"{by_id[i]['district']}, {by_id[i]['state']}",
            key=f"{key}_dist",
        )
        with st.expander("Or click a point on the map"):
            manual_coords = get_map_click(key)
    return resolve_location(photo_bytes, device_coords, manual_id, manual_coords)


def run_cloud_pipeline(
    triage: Dict[str, Any], photo_bytes: bytes, filename: str, loc: LocationResult
) -> Dict[str, Any]:
    """Attach location, store evidence in Cloud Storage and publish an alert. Never raises."""
    loc_dict = loc.to_dict()
    triage["location"] = loc_dict
    triage["location_source"] = loc.location_source
    triage["model_incident_id"] = triage.get("incident_id")
    triage["incident_id"] = new_incident_id()
    stored = save_incident(photo_bytes, filename, triage, loc_dict, triage["incident_id"])
    alert = publish_alert(triage, loc_dict, stored.photo_uri)
    triage["cloud"] = {
        "stored": stored.ok,
        "store_message": stored.message,
        "photo_uri": stored.photo_uri,
        "alert_attempted": should_alert(triage),
        "alert_published": alert.published,
        "alert_message": alert.message,
    }
    return triage


# ==============================================================================
# TAB 3: Ground Damage AI Photo Triage (Google Gemini Multimodal Vision)
# ==============================================================================
with tab_vision:
    backend_vkey = get_resolved_api_key()
    vision_status_pill = (
        '<span class="source-badge-est" title="A Gemini API key is configured; this does not verify that a live request will succeed.">🔑 Gemini API key detected • Request unverified</span>'
        if backend_vkey else
        '<span class="source-badge-sim" title="Prepared offline benchmark results demonstrate the workflow; they are not Gemini analysis of the image.">🛡️ Prepared Offline Benchmark</span>'
    )

    st.markdown(f"""
    <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:12px; flex-wrap:wrap; gap:8px;">
        <div>
            <div style="font-size:18px; font-weight:800; color:#38bdf8; display:flex; align-items:center; gap:8px;">
                <span>📸</span> Field Ground Damage AI Photo Triage
            </div>
            <div style="font-size:13px; color:#cbd5e1; margin-top:2px;">
                Run live Gemini Vision when available, or inspect a clearly labeled offline benchmark result.
            </div>
        </div>
        <div style="display:flex; gap:6px; align-items:center; flex-wrap:wrap;">
            <span class="badge-google" title="Google Gemini Vision AI: Looks at disaster photos from drones or phones to check flood water depth, broken roofs, blocked roads, and rescue gear needed.">📸 Google Gemini Multimodal Vision</span>
            {vision_status_pill}
        </div>
    </div>
    """, unsafe_allow_html=True)

    v_c1, v_c2 = st.columns([1.6, 1.0], gap="medium")
    with v_c1:
        photo_mode = st.radio(
            "Select Disaster Photo Source:",
            ["Benchmark Field Incident Scenes (4 Scenarios)", "Upload Custom Field Photo (JPEG / PNG)"],
            horizontal=True
        )
    with v_c2:
        vis_model_choice = st.selectbox("Gemini Vision Model:", ["gemini-3.8-flash", "gemini-3.5-flash-lite", "gemini-3.1-flash-lite"], index=0)

    sample_items = load_sample_damage_images() if load_sample_damage_images else []
    sel_img_path = None
    up_img_bytes = None
    target_img_name = None

    if photo_mode == "Benchmark Field Incident Scenes (4 Scenarios)":
        if sample_items:
            scenario_names = [f"{s['id'].replace('_', ' ').title()}: {s['name']}" for s in sample_items]
            chosen_s_idx = st.selectbox(
                "Choose Benchmark Field Scene:",
                options=range(len(sample_items)),
                format_func=lambda i: scenario_names[i],
                index=0
            )
            sel_sample = sample_items[chosen_s_idx]
            sel_img_path = sel_sample["path"]
            target_img_name = sel_sample["filename"]
            st.caption(f"📍 **Ground Truth Scenario**: {sel_sample.get('scenario')}")
    else:
        up_file = st.file_uploader("Upload ground-truth disaster photograph:", type=["jpg", "jpeg", "png", "webp"])
        if up_file:
            up_img_bytes = up_file.read()
            target_img_name = up_file.name
            st.caption(f"📍 **Field Photo Uploaded**: {up_file.name} ({len(up_img_bytes)//1024} KB)")

    photo_bytes: Optional[bytes] = up_img_bytes
    if photo_bytes is None and sel_img_path and os.path.exists(sel_img_path):
        with open(sel_img_path, "rb") as _f:
            photo_bytes = _f.read()
    loc_result = LocationResult()
    if photo_bytes:
        loc_result = render_location_picker(photo_bytes, f"loc_{target_img_name}")

    # Execute Triage
    triage_res = None
    if sel_img_path or up_img_bytes:
        img_payload = sel_img_path if sel_img_path else up_img_bytes
        cache_key = f"triage_{target_img_name}"
        live_attempt_key = f"{cache_key}_live_attempted"

        run_triage_btn = st.button("🔍 Run Damage Triage", type="primary", use_container_width=False)
        if run_triage_btn:
            st.session_state[live_attempt_key] = True
            spinner_text = "Calling Google Gemini Vision..." if backend_vkey else "Running calibrated offline triage..."
            with st.spinner(spinner_text):
                if analyze_damage_image:
                    try:
                        triage_res = analyze_damage_image(
                            image_input=img_payload,
                            api_key=backend_vkey,
                            model_name=vis_model_choice,
                            filename=target_img_name,
                            force_offline=False
                        )
                        triage_res = run_cloud_pipeline(triage_res, photo_bytes, target_img_name, loc_result)
                        st.session_state[cache_key] = triage_res
                    except Exception as e:
                        st.error(f"Error during vision triage: {e}")
        elif cache_key not in st.session_state:
            # First load: instantaneous offline calibration benchmark without blocking initial page load
            if sel_img_path and analyze_damage_image:
                try:
                    triage_res = analyze_damage_image(
                        image_input=img_payload,
                        api_key=backend_vkey,
                        model_name=vis_model_choice,
                        filename=target_img_name,
                        force_offline=True
                    )
                    st.session_state[cache_key] = triage_res
                except Exception as e:
                    pass
        else:
            triage_res = st.session_state.get(cache_key)

    # Display Triage Results in Clean Plain-Language Cards
    if triage_res:
        is_live_vision = triage_res.get("is_live_api", False)
        if is_live_vision:
            st.success("Live response received from Google Gemini Vision.")
        elif backend_vkey:
            if st.session_state.get(live_attempt_key, False):
                failure_reason = triage_res.get(
                    "live_api_error",
                    "Gemini did not return a usable response."
                )
                st.warning(
                    f"Live Gemini analysis failed: {failure_reason} "
                    "Showing a calibrated offline fallback, not image analysis. "
                    "Resolve the API issue and retry before presenting."
                )
            else:
                st.info("Showing an offline benchmark reference. Click Run Damage Triage to test whether the configured Gemini key can return a live result.")
        else:
            st.warning("No Gemini API key is configured. This is an offline benchmark/fallback result, not live image analysis.")

        t_col1, t_col2 = st.columns([1.1, 1.35], gap="large")

        with t_col1:
            st.markdown("<div style='font-size:14px; font-weight:700; color:#cbd5e1; margin-bottom:6px;'>📸 Field Incident Evidence Photo</div>", unsafe_allow_html=True)
            if sel_img_path and os.path.exists(sel_img_path):
                st.image(Image.open(sel_img_path), use_container_width=True)
            elif up_img_bytes:
                st.image(up_img_bytes, use_container_width=True)

            st.markdown(f"""
            <div style="background:rgba(30,41,59,0.5); padding:8px 12px; border-radius:8px; font-size:12px; color:#94a3b8; margin-top:6px;">
                📁 <b>File</b>: {triage_res.get('filename', 'incident.jpg')} • ⏱️ <b>Analyzed</b>: {triage_res.get('analyzed_at', 'Now')}
            </div>
            """, unsafe_allow_html=True)

        with t_col2:
            sev_score = triage_res.get("severity_score", 4)
            t_tier = triage_res.get("threat_tier", "HIGH")
            t_border = "#ef4444" if sev_score >= 4 else ("#f97316" if sev_score == 3 else "#10b981")
            water_depth = triage_res.get("estimated_water_depth_m")
            water_str = f"{water_depth:.1f} m" if water_depth is not None else "N/A"
            road_stat = triage_res.get("access_impediment", "Blockage")
            urgency_txt = triage_res.get("urgency_window_hours", "< 2 hrs")

            render_html(f"""
            <div class="glass-panel" style="border-left: 5px solid {t_border}; padding:14px 18px; margin-bottom:12px;">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <div>
                        <div style="font-size:11px; font-weight:700; color:#94a3b8; text-transform:uppercase;">INCIDENT: {triage_res.get('incident_id', 'INC-01')}</div>
                        <h3 style="margin:2px 0 0 0; font-size:20px; font-weight:800; color:#f8fafc;">
                            {triage_res.get('damage_type', 'Disaster Impact')}
                        </h3>
                        <div style="font-size:12.5px; color:#38bdf8; margin-top:2px;">🏗️ {triage_res.get('affected_infrastructure', 'Corridor')}</div>
                    </div>
                    <div style="text-align:right;">
                        <span class="{'badge-critical' if sev_score>=4 else 'badge-high'}" title="Damage severity from Level 1 (minor damage) to Level 5 (completely destroyed or deep underwater).">● LEVEL {sev_score} / 5</span>
                        <div style="font-size:12px; color:#cbd5e1; margin-top:4px;">Threat: <b>{t_tier}</b></div>
                    </div>
                </div>
            </div>
            """)

            # Trust labels: location, assessment source, confidence, human confirmation
            cloud = triage_res.get("cloud")
            shown_loc = triage_res.get("location") if cloud else loc_result.to_dict()
            loc_src = shown_loc.get("location_source", "unverified")
            loc_district = shown_loc.get("district")
            loc_text = f"{loc_district}, {shown_loc.get('state')}" if shown_loc.get("state") else (loc_district or "Location unverified")
            conf_text = f"{triage_res.get('confidence_score', 0.95)*100:.0f}%" if is_live_vision else "n/a (offline)"
            assess_text = "Gemini live" if is_live_vision else "Offline fallback"
            chips = [
                (f"Location: {LOCATION_SOURCE_LABELS.get(loc_src, loc_src)}", "#ef4444" if loc_src == "unverified" else "#10b981"),
                (f"Assessment: {assess_text}", "#10b981" if is_live_vision else "#f59e0b"),
                (f"Confidence: {conf_text}", "#38bdf8"),
            ]
            if str(t_tier).upper() == "CRITICAL":
                chips.append(("🧑‍⚖️ Needs human confirmation", "#ef4444"))
            chip_html = "".join(
                f"<span style='display:inline-block; margin:0 6px 6px 0; padding:3px 10px; border-radius:12px; "
                f"font-size:12px; font-weight:700; color:{c}; border:1px solid {c};'>{html_lib.escape(t)}</span>"
                for t, c in chips
            )
            st.markdown(f"<div>{chip_html}</div>", unsafe_allow_html=True)
            if loc_src == "unverified":
                st.warning("Location unverified — no EXIF GPS, device location or manual district. Evidence is filed under _unverified.")
            elif loc_district == "outside coverage area":
                st.warning("Location is outside the coverage area (no district match).")
            else:
                st.markdown(f"📍 **{loc_text}**" + (" — _overlapping district boundaries; verify_" if shown_loc.get("ambiguous") else ""))
            if cloud is None:
                st.caption("☁️ Not saved yet — click Run Damage Triage to store evidence and send alerts.")
            else:
                if cloud["stored"]:
                    st.caption(f"☁️ Stored: {cloud['photo_uri']}")
                else:
                    note = "Cloud features not configured" if "not configured" in cloud["store_message"] else "Cloud storage failed"
                    st.caption(f"☁️ {note} — evidence not stored ({cloud['store_message']})")
                if cloud["alert_published"]:
                    st.caption("🔔 Alert published to Pub/Sub.")
                elif cloud["alert_attempted"]:
                    st.caption(f"🔔 Alert not sent ({cloud['alert_message']})")
            m1, m2, m3, m4 = st.columns(4)
            m1.markdown(f"<div class='kpi-card'><div class='kpi-label'>Flood Water Level</div><div class='kpi-value' style='font-size:18px; color:#38bdf8;'>{water_str}</div></div>", unsafe_allow_html=True)
            m2.markdown(f"<div class='kpi-card'><div class='kpi-label'>Road Access</div><div class='kpi-value' style='font-size:16px; color:#ef4444;'>{road_stat}</div></div>", unsafe_allow_html=True)
            m3.markdown(f"<div class='kpi-card'><div class='kpi-label'>Response Window</div><div class='kpi-value' style='font-size:16px; color:#f97316;'>{urgency_txt}</div></div>", unsafe_allow_html=True)
            confidence_value = f"{triage_res.get('confidence_score', 0.95)*100:.0f}%" if is_live_vision else "N/A"
            confidence_label = "Gemini Confidence" if is_live_vision else "Live Confidence"
            m4.markdown(f"<div class='kpi-card'><div class='kpi-label'>{confidence_label}</div><div class='kpi-value' style='font-size:18px; color:#10b981;'>{confidence_value}</div></div>", unsafe_allow_html=True)

            render_html("<div style='height: 10px;'></div>")

            # Visual Evidence
            observation_heading = "🔍 Gemini Vision Observations:" if is_live_vision else "🔍 Offline Benchmark Reference (not model output):"
            render_html(f"<div style='font-size:13px; font-weight:700; color:#cbd5e1;'>{observation_heading}</div>")
            for obs in triage_res.get("visual_observations", []):
                render_html(f"<div style='font-size:13px; color:#cbd5e1; margin-bottom:4px;'>▸ {obs}</div>")

            # Tactical Action Directive
            render_html(f"""
            <div class="directive-box">
                <div style="font-size:11px; font-weight:800; color:#ef4444; text-transform:uppercase;">🚨 RECOMMENDED NDRF TACTICAL ACTION:</div>
                <div style="font-size:13px; color:#f1f5f9; margin-top:2px;">{triage_res.get('recommended_ndrf_action', 'Deploy emergency unit.')}</div>
            </div>
            """)

            # Required Equipment
            eq_html = "".join([f"<span class='action-pill'>📦 {e}</span>" for e in triage_res.get("required_equipment", [])])
            st.markdown(f"<div>{eq_html}</div>", unsafe_allow_html=True)

            with st.expander("📄 View Machine-Parsable JSON (Collapsed)", expanded=False):
                st.json(triage_res)

    render_explanation(
        "How does Ground Damage Photo Triage work?",
        {
            "what": "Examines a disaster photo using Google Gemini Vision (when live access is available) to produce an initial damage assessment — severity level, estimated water depth, road access status, and suggested equipment — helping responders prioritize which reports to verify first.",
            "how": [
                "Choose a benchmark scene or upload a field photo (JPEG/PNG).",
                "Select a Gemini vision model and click 'Run Damage Triage' — the app calls the API when a valid key is configured and a live response succeeds.",
                "Review the structured output: damage type, severity score (1–5), threat tier, estimated water depth, road access impediment, and response window.",
                "Check the recommended NDRF tactical action and required equipment list.",
                "Use the severity score to prioritize human verification — the app does not auto-dispatch."
            ],
            "benefit": "After landfall, photos arrive faster than people can review them. Instant severity scores and suggested equipment let control rooms push the most serious incidents to the front of the queue and send the right resources sooner.",
            "tech": [
                "Google Gemini Multimodal Vision (gemini-3.8-flash, 3.5-flash-lite, or 3.1-flash-lite) — analyzes images only when a live API request succeeds.",
                "Structured JSON response — organizes findings into severity, observations, water depth, access status, urgency, and recommended actions.",
                "Prepared offline benchmark scenes — four predefined scenarios with reference outputs for demonstration when live API is unavailable.",
                "Clear live/offline status badges — every result shows whether it came from a confirmed Gemini response or the offline fallback."
            ],
            "limitations": "The prototype analyses one photo at a time. Offline fallback shows only predefined benchmark examples, not live analysis of new uploads. AI findings are initial assessments only and must be verified by responders before any dispatch decision. Confidence scores are shown only for live Gemini responses.",
            "note": "Scaling would require connecting photo sources (drones, field apps, citizen reports), bulk processing on cloud infrastructure, GPS/timestamp tagging for map integration, and a mandatory human-in-the-loop verification step."
        },
        icon="📸"
    )


# ==============================================================================
# TAB 4: Multi-District Risk Matrix & Impact Panel
# ==============================================================================
with tab_matrix:
    st.markdown(f"""
    <div style="display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap; gap:8px; margin-bottom:4px;">
        <div style="font-size:18px; font-weight:800; color:#38bdf8; display:flex; align-items:center; gap:8px;">
            <span>📊</span> {selected_state} District Scenario Risk Matrix
        </div>
        <span class="source-badge-est" title="Configured scenario screening output. Not a current impact report or official warning.">Scenario estimate</span>
    </div>
    <div style="font-size:13px; color:#cbd5e1; margin-bottom:12px;">
        Uses Census-era population references, available OSM-derived infrastructure data, and simplified wind/surge screening estimates. Outputs are scenario indicators for review, not observed impacts or official warnings.
    </div>
    """, unsafe_allow_html=True)

    if not state_vuln_df.empty:
        display_df = state_vuln_df[[
            "rank", "district_name", "population", "district_wind_kts", "imd_wind_class", "district_surge_m",
            "wind_subscore", "surge_subscore", "vulnerability_score", "imd_colour", "threat_tier",
            "evacuation_priority", "flooded_hospitals", "flooded_shelters", "submerged_road_km", "action_directive"
        ]].copy()
        
        display_df.columns = [
            "Rank", "District", "Population", "Scenario Wind (km/h)", "Wind Strength Estimate", "Seawater Rise (m)",
            "Wind Rating", "Seawater Rise Rating", "Scenario Risk Score (0-100)", "Danger Level", "Threat Tier",
            "Review Priority", "Hospitals at Modeled Risk", "Shelters at Modeled Risk", "Road Exposure Estimate (km)", "Possible Action (Review)"
        ]

        st.dataframe(display_df, use_container_width=True, hide_index=True)

        render_explanation(
            "How are these risk scores and colours calculated?",
            {
                "what": "Compares coastal districts using scenario-based wind and seawater rise exposure, producing a 0–100 risk score, danger tier (LOW to CRITICAL), and infrastructure indicators for each district.",
                "how": [
                    "Estimate local wind exposure — storm-track wind values adjusted by distance from each district.",
                    "Estimate seawater exposure — simplified pressure-based surge proxy adjusted by distance from the track.",
                    "Convert inputs to sub-scores — wind and surge values mapped to project-defined 0–100 scales.",
                    "Combine sub-scores — the higher sub-score contributes most, with a smaller contribution from the lower one; result capped at 100.",
                    "Assign a danger tier — scores map to LOW, MODERATE, HIGH, or CRITICAL categories with corresponding display colours."
                ],
                "benefit": "Officers can see at a glance which districts rank highest and why, helping them decide where to pre-position rescue teams, prioritize evacuations, and focus hospital/shelter attention.",
                "tech": [
                    "Storm-track and district data — provide inputs for exposure estimates.",
                    "Wind and seawater rise scoring — produces comparable district-level indicators using project-defined rules.",
                    "Mapped lifeline data — adds road, hospital, and shelter indicators from configured OSM-derived baseline where available."
                ],
                "limitations": "Scores use simplified estimates and project-defined cut-offs, not official IMD/NDMA warning rules. Population references are Census-era; infrastructure data is from a configured OSM-derived baseline, not live verified status. Outputs are scenario screening indicators, not observed impacts or field-validated probabilities.",
                "note": "Follow official IMD/NDMA orders. For real-time use, scores would need automatic recalculation on each new track/forecast, richer inputs (tide, rainfall, terrain), and wider state coverage."
            },
            icon="📊"
        )

        csv_bytes = state_vuln_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label=f"📥 Download {selected_state} Risk Matrix CSV",
            data=csv_bytes,
            file_name=f"cycloneshield_{selected_state.lower().replace(' ', '_')}_{selected_storm_name.lower()}_risk.csv",
            mime="text/csv"
        )


# ==============================================================================
# TAB 5: What-If Landfall Scenario Modeler
# ==============================================================================
with tab_sim:
    st.markdown("""
    <div style="font-size:18px; font-weight:800; color:#38bdf8; display:flex; align-items:center; gap:8px; margin-bottom:4px;">
        <span>🌪️</span> Landfall "What-If" Scenario Simulator
    </div>
    <div style="font-size:13px; color:#cbd5e1; margin-bottom:14px;">
        Test how sudden eyewall intensification or spring tide surge amplification alters road cut-offs and hospital inundation risk across coastal districts.
    </div>
    """, unsafe_allow_html=True)

    sim_c1, sim_c2 = st.columns([1.1, 1.9], gap="large")

    with sim_c1:
        st.markdown("<div style='font-size:14px; font-weight:700; color:#38bdf8; margin-bottom:8px;'>🎛️ Meteorological Scenario Sliders</div>", unsafe_allow_html=True)
        
        # Working preset buttons that modify session state
        if "sim_surge_val" not in st.session_state:
            st.session_state["sim_surge_val"] = 0.0
        if "sim_wind_val" not in st.session_state:
            st.session_state["sim_wind_val"] = 0
        if "sim_rain_val" not in st.session_state:
            st.session_state["sim_rain_val"] = 0

        p1, p2 = st.columns(2)
        if p1.button("🌊 Spring Tide (+1.5m)", use_container_width=True):
            st.session_state["sim_surge_val"] = 1.5
            st.rerun()
        if p2.button("🌀 Super Cyclone (+2.5m)", use_container_width=True):
            st.session_state["sim_surge_val"] = 2.5
            st.session_state["sim_wind_val"] = 40
            st.rerun()

        sim_surge = st.slider(
            "🌊 Seawater Rise Shift (metres):", -2.0, 3.0,
            float(st.session_state["sim_surge_val"]), 0.2,
            help="How much to raise or lower the storm surge. Positive = more seawater pushed ashore. +1.5 m means 1.5 metres higher than the base forecast."
        )
        sim_wind = st.slider(
            "💨 Wind Speed Shift:", -30, 50,
            int(st.session_state["sim_wind_val"]), 5,
            help="How much to increase or decrease peak wind speed. Positive = stronger winds. 1 knot ≈ 1.85 km/h."
        )
        sim_rain = st.slider(
            "🌧️ 48-hour Extra Rainfall (mm):", -100, 250,
            int(st.session_state["sim_rain_val"]), 10,
            help="Extra rainfall over 48 hours. Heavy rain fills drainage and causes roads to flood even far from the coast."
        )

    with sim_c2:
        if batch_predict_coastal_districts:
            try:
                # Reload module to bypass any stale __pycache__ that lacks the state_name parameter
                import importlib, predictive_model as _pm_mod
                importlib.reload(_pm_mod)
                _batch_fn = _pm_mod.batch_predict_coastal_districts

                sim_res_df = _batch_fn(
                    surge_delta_m=sim_surge,
                    wind_delta_kts=float(sim_wind),
                    rain_delta_mm=float(sim_rain),
                    state_name=selected_state
                )
                st.markdown("<div style='font-size:14px; font-weight:700; color:#38bdf8; margin-bottom:8px;'>📊 Lifeline Screening Scores Under Your Scenario</div>", unsafe_allow_html=True)
                st.caption("These model outputs use synthetic physics-inspired training scenarios and are not field-validated probabilities of real-world road closures or hospital flooding. Use them only to compare scenarios.")

                show_sim = sim_res_df[[
                    "district_name", "sim_surge_m", "ml_road_cutoff_pct", "ml_road_tier",
                    "ml_hosp_inundation_pct", "ml_hosp_tier", "road_action"
                ]].rename(columns={
                    "district_name": "District",
                    "sim_surge_m": "Seawater Rise (m)",
                    "ml_road_cutoff_pct": "Road Screening Score (%)",
                    "ml_road_tier": "Road Status",
                    "ml_hosp_inundation_pct": "Hospital Screening Score (%)",
                    "ml_hosp_tier": "Hospital Status",
                    "road_action": "Recommended Action"
                })
                st.dataframe(show_sim, use_container_width=True, hide_index=True)

                # Scenario-based action recommendations for review
                st.markdown("<div style='height:14px;'></div>", unsafe_allow_html=True)
                cmd_header_col1, cmd_header_col2 = st.columns([1.8, 1.0])
                with cmd_header_col1:
                    st.markdown("""
                    <div style='font-size:15px; font-weight:800; color:#38bdf8; display:flex; align-items:center; gap:8px;'>
                        <span>🧭</span> Possible Preparedness Actions — For Officer Review
                    </div>
                    """, unsafe_allow_html=True)
                with cmd_header_col2:
                    st.markdown("<div style='text-align:right;'><span class='source-badge-est' title='Scenario-based recommendations for review; no rescue resources are automatically deployed.'>Scenario recommendations</span></div>", unsafe_allow_html=True)

                playbook_cache_key = f"whatif_playbook_{selected_state}_{sim_surge}_{sim_wind}_{sim_rain}"
                if st.button("🧭 Generate Possible Actions for Review", type="primary", use_container_width=True):
                    with st.spinner("Preparing scenario-based recommendations..."):
                        if generate_whatif_tactical_playbook:
                            playbook = generate_whatif_tactical_playbook(
                                sim_res_df=sim_res_df,
                                scenario_params={
                                    "state_name": selected_state,
                                    "surge_delta_m": sim_surge,
                                    "wind_delta_kts": sim_wind,
                                    "rain_delta_mm": sim_rain
                                },
                                api_key=active_gemini_key
                            )
                            st.session_state[playbook_cache_key] = playbook

                active_playbook = st.session_state.get(playbook_cache_key)
                if not active_playbook and generate_whatif_tactical_playbook:
                    active_playbook = generate_whatif_tactical_playbook(
                        sim_res_df=sim_res_df,
                        scenario_params={
                            "state_name": selected_state,
                            "surge_delta_m": sim_surge,
                            "wind_delta_kts": sim_wind,
                            "rain_delta_mm": sim_rain
                        },
                        api_key=None
                    )

                if active_playbook:
                    rcode = active_playbook.get("readiness_code", "CRITICAL RED")
                    rcolor = "#ef4444" if "RED" in rcode else ("#f97316" if "ORANGE" in rcode else "#38bdf8")
                    rbadge = active_playbook.get("engine", "Google Gemini")
                    is_live = active_playbook.get("is_live_gemini", False)
                    badge_cls = "badge-google-live" if is_live else "badge-google-fallback"
                    playbook_tooltip = (
                        "Live Gemini response for this request; recommendations are for human review and do not deploy resources."
                        if is_live else
                        "Prepared fallback recommendations for review; they do not deploy resources."
                    )

                    render_html(f"""
                    <div class="google-card" style="border-left: 5px solid {rcolor};">
                        <div style="display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap; gap:8px;">
                            <div>
                                <span style="background:{rcolor}22; color:{rcolor}; border:1px solid {rcolor}; padding:2px 8px; border-radius:4px; font-size:11px; font-weight:800;">● {rcode}</span>
                                <h3 style="margin:6px 0 4px 0; font-size:18px; font-weight:800; color:#f8fafc;">Possible actions: {active_playbook.get('readiness_headline', 'review scenario')}</h3>
                                <div style="font-size:13px; color:#cbd5e1; line-height:1.5;">{active_playbook.get('executive_brief', '')}</div>
                            </div>
                            <div>
                                <span class="{badge_cls}" title="{playbook_tooltip}">{rbadge}</span>
                            </div>
                        </div>
                    </div>
                    """)

                    pb_c1, pb_c2 = st.columns([1.1, 1.0], gap="medium")
                    with pb_c1:
                        st.markdown("**🚨 Possible Resource Actions (For Officer Review):**")
                        for dep in active_playbook.get("tactical_deployments", []):
                            render_html(f"""
                            <div class="dispatch-item" style="border-left-color:{rcolor}; margin-bottom:8px; padding:10px 14px;">
                                <div style="font-size:12px; font-weight:800; color:#38bdf8;">{dep.get('unit','NDRF Unit')} ➔ {dep.get('target_district','District')}</div>
                                <div style="font-size:13px; color:#f1f5f9; margin-top:3px;"><b>Suggested action</b>: {dep.get('action','')}</div>
                                <div style="font-size:11.5px; color:#94a3b8; margin-top:2px;">⚙️ <b>Equipment</b>: {dep.get('equipment','')}</div>
                            </div>
                            """)
                    with pb_c2:
                        st.markdown("**🚧 Evacuation Corridor & Lifeline Bypasses:**")
                        render_html(f"""
                        <div style="background:rgba(15,23,42,0.7); border:1px solid rgba(148,163,184,0.2); border-radius:8px; padding:12px 14px; margin-bottom:10px;">
                            <div style="font-size:11.5px; font-weight:800; color:#f97316; text-transform:uppercase;">POSSIBLE CORRIDOR ACTION — REVIEW LOCALLY</div>
                            <div style="font-size:13px; color:#cbd5e1; margin-top:4px; line-height:1.5;">{active_playbook.get('evacuation_corridor_directive','')}</div>
                        </div>
                        <div style="background:rgba(15,23,42,0.7); border:1px solid rgba(148,163,184,0.2); border-radius:8px; padding:12px 14px;">
                            <div style="font-size:11.5px; font-weight:800; color:#38bdf8; text-transform:uppercase;">HOSPITAL SURGE DEFENSE</div>
                            <div style="font-size:13px; color:#cbd5e1; margin-top:4px; line-height:1.5;">{active_playbook.get('hospital_resilience_action','')}</div>
                        </div>
                        """)
            except TypeError as te:
                st.warning(
                    f"⚠️ The simulator engine needs a restart to pick up the latest version. "
                    f"Please **stop the Streamlit app and run it again** — this clears the module cache. (Detail: `{te}`)"
                )
            except Exception as e:
                st.error(f"Simulation error: {e}")
        else:
            st.info("Predictive ML engine not loaded — check that `predictive_model.py` is present in the project folder.")

    render_explanation(
        "How does the What-If Landfall Simulator work?",
        {
            "what": "Estimates how changes to a cyclone scenario (surge, wind, rainfall) could affect road access and hospital flooding across coastal districts, using a gradient-boosting model trained on synthetic physics-inspired scenarios.",
            "how": [
                "Adjust sliders for surge shift (±3 m), wind shift (±50 kts), and 48-hour rainfall shift (±250 mm), or click a preset (Spring Tide, Super Cyclone).",
                "The model combines these changes with district features to produce scenario-based screening scores and impact tiers for road cut-offs and hospital inundation.",
                "Review the district-level results table showing seawater rise, road/hospital screening scores, status tiers, and recommended actions.",
                "Optionally generate a tactical playbook (when Gemini is available) with possible resource actions, evacuation corridor guidance, and hospital resilience measures for officer review."
            ],
            "benefit": "Officials can quickly test 'what if the storm gets stronger or the tide is higher?' and see which roads and hospitals could be at risk, so they can plan resources before conditions worsen.",
            "tech": [
                "Scikit-learn gradient-boosting model — estimates scenario-based road and hospital impacts from synthetic training data.",
                "Interactive scenario sliders — apply user-selected changes to wind, surge, and rainfall inputs.",
                "Optional Google Gemini playbook — generates a response summary when a live API response is confirmed; otherwise uses prepared fallback."
            ],
            "limitations": "The model is trained on synthetic physics-inspired scenarios, not real observed flooding or road-closure records. Results are screening estimates for scenario comparison, not forecasts or validated predictions. The playbook provides suggestions for human review only — no resources are deployed automatically.",
            "note": "Real-time scaling would require linking to live official forecasts, retraining on observed events, parallel scenario execution on cloud infrastructure, and integration with response-planning workflows."
        },
        icon="🌪️"
    )


# ==============================================================================
# TAB 6: Parametric Insurance Liquidity Trigger Dashboard
# ==============================================================================
with tab_insurance:
    st.markdown("""
    <div style="font-size:18px; font-weight:800; color:#38bdf8; display:flex; align-items:center; gap:8px; margin-bottom:4px;">
        <span>💰</span> Emergency Relief Funds Dashboard
    </div>
    <div style="font-size:13px; color:#cbd5e1; margin-bottom:14px;">
        Demonstrates how configured wind and surge values could be compared with example thresholds and mapped to example payout tiers. This is not an active insurance policy, a payment, or a fund-release workflow.
    </div>
    """, unsafe_allow_html=True)

    if evaluate_parametric_trigger and compute_district_parametric_matrix and get_aggregate_payout_summary:
        ins_result = evaluate_parametric_trigger(
            wind_kts=peak_wind,
            surge_m=calc_surge_m,
            state_name=selected_state
        )

        # State-level trigger card
        ins_border = ins_result.color
        ins_badge = "SCENARIO THRESHOLD MET" if ins_result.is_triggered else "SCENARIO THRESHOLD NOT MET"
        render_html(f"""
        <div class="situation-card" style="border-left-color:{ins_border};">
            <div style="display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap; gap:12px;">
                <div>
                    <div style="font-size:12px; font-weight:700; color:{ins_border}; text-transform:uppercase; letter-spacing:0.8px;">💰 ILLUSTRATIVE SCENARIO THRESHOLD</div>
                    <h2 style="margin:4px 0 6px 0; font-size:22px; font-weight:800; color:#f8fafc;">{ins_result.tier_label}</h2>
                    <div style="font-size:13.5px; color:#cbd5e1; line-height:1.6;">
                        🌪️ <b>Wind</b>: {ins_result.wind_kts:.0f} kts ({ins_result.wind_kts*1.852:.0f} km/h) &nbsp;|&nbsp;
                        🌊 <b>Seawater Rise</b>: {ins_result.surge_m:.2f} m &nbsp;|&nbsp;
                        🎯 <b>Scenario input</b>: {ins_result.trigger_source.upper()}<br>
                        📋 {ins_result.description}
                    </div>
                </div>
                <div style="text-align:right;">
                    <div style="font-size:30px; font-weight:900; color:{ins_border};">
                        ₹ {ins_result.payout_amount_cr:.0f} Cr
                    </div>
                    <div style="font-size:12px; color:#94a3b8;">Example payout timing assumption: {ins_result.time_to_payout_hours}h after trigger confirmation</div>
                    <div style="font-size:11px; color:{ins_border}; font-weight:700; margin-top:4px;">{ins_badge}</div>
                </div>
            </div>
            <div class="directive-box" style="margin-top:12px; margin-bottom:0;">
                <div style="font-size:11px; font-weight:800; color:#ef4444; text-transform:uppercase;">🚨 POSSIBLE ACTION FOR AUTHORIZED REVIEW:</div>
                <div style="font-size:13px; color:#f1f5f9; margin-top:2px;">{ins_result.ndrf_implication}</div>
            </div>
        </div>
        """)

        # Tier waterfall visualization
        st.markdown("<div style='font-size:14px; font-weight:700; color:#38bdf8; margin:12px 0 8px;'>📊 Trigger Tier Waterfall — All Thresholds</div>", unsafe_allow_html=True)
        tier_cols = st.columns(4)
        for i, tier in enumerate(ins_result.all_tiers_status):
            with tier_cols[i % 4]:
                is_active = tier["is_triggered"]
                bg = f"background:rgba({','.join(str(int(tier['color'].lstrip('#')[j:j+2], 16)) for j in (0,2,4))}, 0.18);"
                border = f"border:2px solid {tier['color']};" if is_active else "border:1px solid rgba(148,163,184,0.2);"
                st.markdown(f"""
                <div style="{bg}{border}border-radius:10px;padding:12px;text-align:center;margin-bottom:8px;">
                    <div style="font-size:11px; font-weight:700; color:{tier['color']}; text-transform:uppercase;">{tier['tier_name']}</div>
                    <div style="font-size:18px; font-weight:900; color:#f8fafc; margin:4px 0;">₹ {STATE_DEFAULT_SUM_INSURED_CR.get(selected_state,500)*tier['payout_pct']:.0f} Cr</div>
                    <div style="font-size:11px; color:#94a3b8;">Wind ≥ {tier['wind_threshold']:.0f} kts<br>OR Surge ≥ {tier['surge_threshold']:.1f} m</div>
                    <div style="font-size:12px; font-weight:700; color:{'#10b981' if is_active else '#64748b'}; margin-top:6px;">{'✅ SCENARIO THRESHOLD MET' if is_active else '⭕ NOT MET'}</div>
                </div>
                """, unsafe_allow_html=True)

        # District-level parametric matrix
        st.markdown("<div style='font-size:14px; font-weight:700; color:#38bdf8; margin:14px 0 8px;'>🏘️ District-Level Parametric Payout Matrix</div>", unsafe_allow_html=True)
        st.caption("Each district receives a proportional payout based on its exposure to the cyclone core. More exposed districts receive higher effective wind/surge values and trigger higher tiers.")

        if not state_vuln_df.empty:
            district_ins = compute_district_parametric_matrix(
                district_rows=state_vuln_df.to_dict(orient="records"),
                base_wind_kts=peak_wind,
                base_surge_m=calc_surge_m,
                state_name=selected_state,
                sum_insured_cr_per_district=50.0
            )
            summary = get_aggregate_payout_summary(district_ins, selected_state)

            ins_df = pd.DataFrame(district_ins)[[
                "district_name", "population", "effective_wind_kts", "effective_surge_m",
                "insurance_tier_name", "payout_pct", "payout_amount_cr", "ndrf_implication"
            ]]
            ins_df.columns = ["District", "Population", "Wind (km/h)", "Seawater Rise (m)",
                              "Example Tier", "Example Payout %", "Example Amount (₹ Cr)", "Possible Action (Review)"]
            ins_df["Example Payout %"] = (ins_df["Example Payout %"] * 100).apply(lambda x: f"{x:.0f}%")
            st.dataframe(ins_df, use_container_width=True, hide_index=True)

            # Aggregate summary ribbon
            s1, s2, s3, s4 = st.columns(4)
            s1.metric("Example Total Payout", f"₹ {summary['total_payout_cr']:.0f} Cr")
            s2.metric("Scenario Thresholds Met", f"{summary['triggered_districts']} / {summary['total_districts']}")
            s3.metric("Illustrative SDRF Share", f"{summary['sdrf_utilization_pct']:.1f}%")
            s4.metric("Illustrative Balance", "✅ Within reference" if summary['is_sdrf_sufficient'] else f"⚠️ Example gap: ₹{summary['sdrf_gap_cr']:.0f} Cr")

            ins_csv = ins_df.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="📥 Download Parametric Insurance Matrix CSV",
                data=ins_csv,
                file_name=f"parametric_insurance_{selected_state.lower().replace(' ', '_')}_{selected_storm_name.lower()}.csv",
                mime="text/csv"
            )

            # Illustrative capital-allocation scenario section
            st.markdown("<div style='height:14px;'></div>", unsafe_allow_html=True)
            ins_audit_col1, ins_audit_col2 = st.columns([1.8, 1.0])
            with ins_audit_col1:
                st.markdown("""
                <div style='font-size:15px; font-weight:800; color:#38bdf8; display:flex; align-items:center; gap:8px;'>
                    <span>💰</span> Example Liquidity Allocation — Decision Support
                </div>
                """, unsafe_allow_html=True)
            with ins_audit_col2:
                st.markdown("<div style='text-align:right;'><span class='badge-google' title='Optional advisory-generation integration; displayed calculations are examples and do not release funds.'>Illustrative calculation</span></div>", unsafe_allow_html=True)

            ins_cache_key = f"ins_audit_{selected_state}_{peak_wind}_{calc_surge_m}"
            if st.button("💰 Generate Example Allocation for Review", type="primary", use_container_width=True):
                with st.spinner("Preparing an illustrative allocation for review..."):
                    if generate_parametric_liquidity_audit:
                        audit_res = generate_parametric_liquidity_audit(
                            ins_result=ins_result,
                            district_matrix=state_vuln_df.to_dict(orient="records"),
                            state_name=selected_state,
                            api_key=active_gemini_key
                        )
                        st.session_state[ins_cache_key] = audit_res

            active_audit = st.session_state.get(ins_cache_key)
            if not active_audit and generate_parametric_liquidity_audit:
                active_audit = generate_parametric_liquidity_audit(
                    ins_result=ins_result,
                    district_matrix=state_vuln_df.to_dict(orient="records"),
                    state_name=selected_state,
                    api_key=None
                )

            if active_audit:
                a_badge = active_audit.get("engine", "Google Gemini")
                is_live_a = active_audit.get("is_live_gemini", False)
                a_badge_cls = "badge-google-live" if is_live_a else "badge-google-fallback"
                audit_tooltip = (
                    "Live Google Gemini response for this request; calculated amounts remain illustrative and do not authorize payments."
                    if is_live_a else
                    "Built-in fallback example; amounts are illustrative and do not authorize payments."
                )

                render_html(f"""
                <div class="google-card" style="border-left: 5px solid #10b981;">
                    <div style="display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap; gap:8px;">
                        <div>
                            <span style="background:rgba(16,185,129,0.18); color:#6ee7b7; border:1px solid #10b981; padding:2px 8px; border-radius:4px; font-size:11px; font-weight:800;">ILLUSTRATIVE ALLOCATION SCENARIO — FOR REVIEW</span>
                            <h3 style="margin:6px 0 4px 0; font-size:18px; font-weight:800; color:#f8fafc;">Example allocation: ₹ {active_audit.get('total_payout_cr', 0):.0f} Crore for {selected_state}</h3>
                            <div style="font-size:13px; color:#cbd5e1; line-height:1.5;">{active_audit.get('executive_summary', '')}</div>
                        </div>
                        <div>
                            <span class="{a_badge_cls}" title="{audit_tooltip}">{a_badge}</span>
                        </div>
                    </div>
                </div>
                """)

                aud_c1, aud_c2 = st.columns([1.1, 1.0], gap="medium")
                with aud_c1:
                    st.markdown("**📋 Example district allocation (not a fund release):**")
                    if active_audit.get("district_allocations"):
                        alloc_df = pd.DataFrame(active_audit["district_allocations"])
                        if "allocated_cr" in alloc_df.columns:
                            alloc_df = alloc_df.rename(columns={
                                "district_name": "District",
                                "allocated_cr": "Allocated (₹ Cr)",
                                "percentage": "Share %",
                                "priority_need": "Operational Procurement Priority"
                            })
                            st.dataframe(alloc_df, use_container_width=True, hide_index=True)
                with aud_c2:
                    st.markdown("**📊 Example expenditure breakdown:**")
                    if active_audit.get("budget_line_breakdown"):
                        bl_df = pd.DataFrame(active_audit["budget_line_breakdown"])
                        bl_df = bl_df.rename(columns={
                            "category": "Expenditure Line",
                            "amount_cr": "Budget (₹ Cr)",
                            "percentage": "Share %"
                        })
                        st.dataframe(bl_df, use_container_width=True, hide_index=True)

                    render_html(f"""
                    <div style="background:rgba(15,23,42,0.7); border:1px solid rgba(16,185,129,0.3); border-radius:8px; padding:10px 14px; margin-top:8px;">
                        <div style="font-size:11.5px; font-weight:800; color:#10b981; text-transform:uppercase;">FAST-TRACK GOVERNANCE AUDIT PROTOCOL</div>
                        <div style="font-size:12.5px; color:#cbd5e1; margin-top:4px; line-height:1.4;">{active_audit.get('governance_audit_protocol','')}</div>
                    </div>
                    """)
            else:
                st.info("Parametric insurance module not loaded. Ensure `parametric_insurance.py` is present in the project folder.")

    render_explanation(
        "How are parametric triggers and payouts calculated?",
        {
            "what": "Illustrates how a pre-agreed, measurable trigger (wind speed and/or surge height) could be checked against scenario values and mapped to example payout tiers — showing the concept of parametric insurance for faster disaster finance.",
            "how": [
                "Read the current scenario's wind and surge values from the selected cyclone.",
                "Compare against configured trigger tiers (each with wind/surge thresholds and a payout percentage).",
                "Display the state-level trigger status, example payout amount, and a tier waterfall showing which thresholds are met.",
                "Show a district-level matrix where each district receives a proportional payout based on its exposure to the cyclone core.",
                "Optionally generate an illustrative liquidity allocation breakdown (when Gemini is available) with example district allocations and expenditure lines for officer review."
            ],
            "benefit": "During an actual cyclone, a parametric trigger checked against measured wind/surge could immediately show which districts qualify and the expected payout size — instead of waiting weeks for damage surveys — helping officials plan relief funding and procurement faster.",
            "tech": [
                "Configured wind/surge threshold tiers — define trigger levels and payout percentages for demonstration.",
                "District exposure weighting — adjusts effective wind/surge per district based on distance from cyclone core.",
                "Reference funding values (sum insured, SDRF corpus) — provide context only; not actual funds or approvals.",
                "Optional Google Gemini advisory — generates an illustrative allocation narrative when a live response is confirmed; otherwise uses prepared fallback."
            ],
            "limitations": "This is a calculation prototype only — not an active insurance policy, verified trigger, or payment. No insurer, contractual policy, or payment service is connected. Trigger assessment uses scenario values, not live measured data. All payout amounts are illustrative examples for review.",
            "note": "Real-world deployment would require authorised live data feeds (IMD bulletins, verified observations), scheduled recalculation, threshold alerting for decision-makers, cloud-scale infrastructure, and formal governance agreements with insurers/fund managers."
        },
        icon="💰"
    )


# ==============================================================================
# TAB 7: Real-Time Meteorological Feed (Open-Meteo — Free, No API Key)
# ==============================================================================
with tab_met:
    st.markdown("""
    <div style="font-size:18px; font-weight:800; color:#38bdf8; display:flex; align-items:center; gap:8px; margin-bottom:4px;">
        <span>🌤️</span> Real-Time Meteorological Feed
    </div>
    <div style="font-size:13px; color:#cbd5e1; margin-bottom:14px;">
    Requests wind, rain, and pressure forecasts from <b>Open-Meteo ECMWF IFS</b> when available. Check the source/status badge and retrieval time to confirm a live response; fallback values are estimates. This is not an official IMD forecast.
    </div>
    """, unsafe_allow_html=True)

    # Determine best landfall coordinates for met query
    state_coords = {
        "West Bengal": (21.9, 88.1),
        "Odisha": (20.3, 86.2),
        "Andhra Pradesh": (16.5, 81.8),
        "Tamil Nadu": (11.8, 79.8),
        "Gujarat": (22.3, 70.0)
    }
    if is_custom_track and active_track_df is not None and not active_track_df.empty:
        met_lat = float(active_track_df["lat"].iloc[-1])
        met_lon = float(active_track_df["lon"].iloc[-1])
    else:
        met_lat, met_lon = state_coords.get(selected_state, (20.5, 85.0))

    met_c1, met_c2 = st.columns([1.2, 1.0], gap="large")

    with met_c1:
        st.markdown("<div style='font-size:14px; font-weight:700; color:#38bdf8; margin-bottom:8px;'>⚡ 72-Hour Weather Forecast for Scenario Location (Open-Meteo)</div>", unsafe_allow_html=True)
        with st.spinner("Fetching live Open-Meteo ECMWF data..."):
            if fetch_landfall_forecast:
                met_data = fetch_landfall_forecast(met_lat, met_lon, hours_ahead=72)
            else:
                met_data = {"status": "offline", "source_badge": "🔵 ESTIMATED",
                            "peak_wind_kmh": peak_wind * 1.852, "peak_gust_kmh": peak_wind * 2.2,
                            "total_rain_mm": 180.0, "min_pressure_hpa": min_pres,
                            "imd_category": "Severe Cyclonic Storm",
                            "source_label": "Fallback estimate", "hours_covered": 0}

        status_badge = met_data.get("source_badge", "🔵 ESTIMATED")
        st.markdown(f"""
        <div style="background:rgba(30,41,59,0.7); border:1px solid rgba(56,189,248,0.25); border-radius:8px;
                    padding:10px 14px; font-size:12px; color:#94a3b8; margin-bottom:10px;">
            {status_badge} &nbsp; <b style="color:#f8fafc;">{met_data.get('source_label','Open-Meteo ECMWF IFS')}</b>
            &nbsp;|&nbsp; Retrieved: {met_data.get('retrieved_at','—')}
            &nbsp;|&nbsp; Coverage: {met_data.get('hours_covered',0)}h
        </div>
        """, unsafe_allow_html=True)

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Peak Wind", f"{met_data.get('peak_wind_kmh', 0):.0f} km/h",
                  f"{met_data.get('peak_wind_kts', 0):.0f} kts")
        m2.metric("Peak Gust", f"{met_data.get('peak_gust_kmh', 0):.0f} km/h")
        m3.metric("72h Rainfall", f"{met_data.get('total_rain_mm', 0):.0f} mm")
        m4.metric("Min Pressure", f"{met_data.get('min_pressure_hpa', 1013):.0f} hPa")

        st.markdown(f"""
        <div style="background:rgba(15,23,42,0.7); border-left:4px solid #38bdf8;
                    border-radius:8px; padding:10px 14px; margin-top:10px;">
            <div style="font-size:11px; color:#94a3b8; text-transform:uppercase; font-weight:700;">Indicative Category (Derived from Feed)</div>
            <div style="font-size:18px; font-weight:800; color:#38bdf8; margin-top:4px;">
                {met_data.get('imd_category', '—')}
            </div>
        </div>
        """, unsafe_allow_html=True)

        if met_data.get("hourly_times") and len(met_data["hourly_times"]) > 0:
            import pandas as _pd_met
            chart_df = _pd_met.DataFrame({
                "Hour": met_data["hourly_times"][:72:3],
                "Wind (km/h)": met_data["hourly_wind_kmh"][:72:3],
                "Rain (mm)": met_data["hourly_rain_mm"][:72:3],
            })
            st.markdown("**Wind Forecast (hourly sample):**")
            st.bar_chart(chart_df.set_index("Hour")[["Wind (km/h)"]].head(24), height=160)

    with met_c2:
        st.markdown("<div style='font-size:14px; font-weight:700; color:#38bdf8; margin-bottom:8px;'>🌊 Offshore Marine Wave & Swell Forecast</div>", unsafe_allow_html=True)
        with st.spinner("Fetching marine conditions..."):
            if fetch_marine_conditions:
                marine = fetch_marine_conditions(met_lat - 1.0, met_lon, hours_ahead=48)
            else:
                marine = {"status": "offline", "source_badge": "🔵 ESTIMATED",
                          "peak_wave_m": 4.5, "peak_swell_m": 2.8,
                          "avg_wave_period_s": 10.0, "surge_amplification_factor": 1.34,
                          "source_label": "Bay of Bengal Climatology Estimate"}

        st.markdown(f"""
        <div style="background:rgba(30,41,59,0.7); border:1px solid rgba(56,189,248,0.25); border-radius:8px;
                    padding:10px 14px; font-size:12px; color:#94a3b8; margin-bottom:10px;">
            {marine.get('source_badge','🔵')} &nbsp; <b style="color:#f8fafc;">{marine.get('source_label','Marine API')}</b>
        </div>
        """, unsafe_allow_html=True)

        wv1, wv2, wv3 = st.columns(3)
        wv1.metric("Peak Wave", f"{marine.get('peak_wave_m', 0):.1f} m")
        wv2.metric("Peak Swell", f"{marine.get('peak_swell_m', 0):.1f} m")
        wv3.metric("Wave Period", f"{marine.get('avg_wave_period_s', 8):.0f} sec")

        amp_factor = marine.get("surge_amplification_factor", 1.0)
        amp_pct = round((amp_factor - 1.0) * 100, 1)
        amplified_surge = round(calc_surge_m * amp_factor, 2)
        render_html(f"""
        <div style="background:rgba(15,23,42,0.7); border-left:4px solid #7c3aed;
                    border-radius:8px; padding:10px 14px; margin-top:10px;">
            <div style="font-size:11px; color:#94a3b8; text-transform:uppercase; font-weight:700;">Swell Surge Amplification</div>
            <div style="font-size:22px; font-weight:900; color:#7c3aed;">+{amp_pct:.0f}%</div>
            <div style="font-size:12.5px; color:#cbd5e1; margin-top:2px;">
                Base surge {calc_surge_m:.2f}m → <b style="color:#f8fafc;">Amplified: {amplified_surge:.2f}m</b><br>
                <span style="font-size:11px; color:#94a3b8;">Offshore swell pushes additional water onto coast during landfall window.</span>
            </div>
        </div>
        """)

        # District-level live snapshot for selected district
        st.markdown("<div style='font-size:14px; font-weight:700; color:#38bdf8; margin:14px 0 8px;'>📍 Live Conditions at Selected District</div>", unsafe_allow_html=True)
        if not state_vuln_df.empty:
            d_lat_met = float(state_vuln_df.iloc[0].get("lat", met_lat))
            d_lon_met = float(state_vuln_df.iloc[0].get("lon", met_lon))
            d_name_met = state_vuln_df.iloc[0].get("district_name", sel_dist)
            with st.spinner(f"Fetching live conditions for {d_name_met}..."):
                if fetch_district_met_snapshot:
                    snap = fetch_district_met_snapshot(d_lat_met, d_lon_met, d_name_met)
                else:
                    snap = {"status": "offline", "source_badge": "🔵 ESTIMATED",
                            "current_wind_kmh": 0.0, "current_gust_kmh": 0.0,
                            "current_rain_mmph": 0.0, "current_pressure_hpa": 1013.0,
                            "next_6h_rain_mm": 0.0, "next_6h_max_wind_kmh": 0.0,
                            "imd_category": "No active data", "retrieved_at": "—"}

            st.markdown(f"""
            <div style="background:rgba(15,23,42,0.7); border:1px solid rgba(148,163,184,0.2); border-radius:8px; padding:10px 14px;">
                <div style="font-size:11px; color:#94a3b8;">{snap.get('source_badge','—')} · {d_name_met} · {snap.get('retrieved_at','—')}</div>
                <div style="display:grid; grid-template-columns:1fr 1fr; gap:8px; margin-top:8px;">
                    <div><div style="font-size:10px;color:#94a3b8;">CURRENT WIND</div><div style="font-size:16px;font-weight:700;color:#f8fafc;">{snap.get('current_wind_kmh',0):.0f} km/h</div></div>
                    <div><div style="font-size:10px;color:#94a3b8;">GUST</div><div style="font-size:16px;font-weight:700;color:#ef4444;">{snap.get('current_gust_kmh',0):.0f} km/h</div></div>
                    <div><div style="font-size:10px;color:#94a3b8;">RAIN NOW</div><div style="font-size:16px;font-weight:700;color:#38bdf8;">{snap.get('current_rain_mmph',0):.1f} mm/h</div></div>
                    <div><div style="font-size:10px;color:#94a3b8;">NEXT 6H RAIN</div><div style="font-size:16px;font-weight:700;color:#818cf8;">{snap.get('next_6h_rain_mm',0):.0f} mm</div></div>
                </div>
                <div style="font-size:12px;color:#f59e0b;margin-top:8px;font-weight:700;">{snap.get('imd_category','—')}</div>
            </div>
            """, unsafe_allow_html=True)

    # Google Gemini Compound Hazard & Estuarine Risk Synthesis Section
    st.markdown("<div style='height:14px;'></div>", unsafe_allow_html=True)
    met_syn_col1, met_syn_col2 = st.columns([1.8, 1.0])
    with met_syn_col1:
        st.markdown("""
        <div style='font-size:15px; font-weight:800; color:#38bdf8; display:flex; align-items:center; gap:8px;'>
            <span>🌊</span> Google Gemini — Compound Hydro-Meteorological Hazard Briefing
        </div>
        """, unsafe_allow_html=True)
    with met_syn_col2:
        st.markdown("<div style='text-align:right;'><span class='badge-google' title='Google Gemini AI: Warns if heavy rains and huge sea waves will block river mouths and cause severe overflow into nearby coastal towns.'>✨ Google Gemini 2.5 Flash</span></div>", unsafe_allow_html=True)

    d_target_met = state_vuln_df.iloc[0].get("district_name", selected_state) if not state_vuln_df.empty else selected_state
    met_cache_key = f"compound_briefing_{d_target_met}_{met_data.get('peak_wind_kmh',0)}"
    if st.button("🌊 Generate Compound Threat Assessment (Google Gemini)", type="primary", use_container_width=True):
        with st.spinner("Synthesizing compound surge, swell, and estuarine damming with Google Gemini..."):
            if generate_compound_hazard_briefing:
                briefing_res = generate_compound_hazard_briefing(
                    met_snapshot=met_data,
                    marine_snapshot=marine,
                    district_name=d_target_met,
                    api_key=active_gemini_key
                )
                st.session_state[met_cache_key] = briefing_res

    active_briefing = st.session_state.get(met_cache_key)
    if not active_briefing and generate_compound_hazard_briefing:
        active_briefing = generate_compound_hazard_briefing(
            met_snapshot=met_data,
            marine_snapshot=marine,
            district_name=d_target_met,
            api_key=None
        )

    if active_briefing:
        b_badge = active_briefing.get("engine", "Google Gemini")
        is_live_b = active_briefing.get("is_live_gemini", False)
        b_badge_cls = "badge-google-live" if is_live_b else "badge-google-fallback"
        briefing_tooltip = (
            "Live Google Gemini AI: Actively analyzed live sea waves, wind, and rain to spot river overflow risks."
            if is_live_b else
            "Built-in River & Wave Model: Calculated river overflow risk using weather and tide formulas (no internet or API key needed)."
        )
        c_tier = active_briefing.get("compound_threat_tier", "CRITICAL RISK")
        c_col = "#ef4444" if "CRITICAL" in c_tier else ("#f97316" if "HIGH" in c_tier else "#38bdf8")

        render_html(f"""
        <div class="google-card" style="border-left: 5px solid {c_col};">
            <div style="display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap; gap:8px;">
                <div>
                    <span style="background:{c_col}22; color:{c_col}; border:1px solid {c_col}; padding:2px 8px; border-radius:4px; font-size:11px; font-weight:800;">● {c_tier}</span>
                    <h3 style="margin:6px 0 4px 0; font-size:18px; font-weight:800; color:#f8fafc;">River & Sea Threat Assessment: {d_target_met}</h3>
                    <div style="font-size:12.5px; color:#94a3b8;"><b>Peak danger window</b>: <span style="color:#f8fafc;">{active_briefing.get('peak_danger_window_ist','Landfall Window')}</span></div>
                </div>
                <div>
                    <span class="{b_badge_cls}" title="{briefing_tooltip}">{b_badge}</span>
                </div>
            </div>
            <div style="font-size:13px; color:#cbd5e1; margin-top:10px; line-height:1.5;">
                🌊 <b>Will heavy rain and huge sea waves block the river?</b>: {active_briefing.get('estuary_damming_assessment','')}<br>
                ⚓ <b>What ports and ships should do</b>: {active_briefing.get('marine_port_directive','')}<br>
                🚨 <b>What ground teams should do</b>: {active_briefing.get('ground_commander_action','')}
            </div>
        </div>
        """)

    render_explanation(
        "How are real-time weather and offshore marine conditions fetched?",
        {
            "what": "Displays a 72-hour landfall-area weather forecast (wind, gusts, rainfall, pressure), offshore wave/swell conditions with surge amplification, and a district-level snapshot — all with clear source badges and retrieval timestamps.",
            "how": [
                "Determine forecast location — uses the active storm track's last waypoint when available, otherwise a default coastal coordinate for the selected state.",
                "Request forecast data from Open-Meteo (ECMWF IFS) — fetches wind, gusts, rainfall, pressure, and derived IMD-style category when the service is reachable.",
                "Retrieve marine conditions — shows peak wave height, swell height, wave period, and calculates a surge amplification factor from swell.",
                "Fetch district-level snapshot — current wind, gust, rain rate, pressure, and next-6-hour forecasts for the selected district.",
                "Check source/status badge and retrieval time on every panel — confirms whether values are from a live API response or a labeled fallback estimate."
            ],
            "benefit": "Officials can review expected wind, rain, wave, and surge conditions for the landfall area in one place with clear source attribution, helping them judge when conditions may become dangerous for rescue operations, port activity, and evacuation movement.",
            "tech": [
                "Open-Meteo forecast API (ECMWF IFS) — supplies weather values when reachable; clearly labeled fallback estimates when unavailable.",
                "Marine forecast data — provides offshore wave, swell, and period data for surge amplification calculation.",
                "Google Gemini (optional) — generates a compound hydro-meteorological hazard briefing when a live response is confirmed; otherwise uses a built-in river/wave model fallback.",
                "Explicit source badges and timestamps — every panel shows data provenance (live API, estimate, or fallback)."
            ],
            "limitations": "This panel is not an official IMD cyclone-track forecast or warning. When live data is unavailable, the app shows clearly labeled estimates — check the source badge and retrieval time. No automatic refresh interval is implemented; no end-to-end data sharing between tabs or continuous real-time tracking unless verified in code. The Gemini compound briefing is optional and only runs on user click.",
            "note": "Real-time scaling would require scheduled forecast refreshes, additional sources (IMD products, coastal observations), district-level coverage for all monitored areas, and automated threshold alerting."
        },
        icon="🌤️"
    )


# ==============================================================================
# TAB 8: Technical Architecture & Evaluator Audit (Collapsed for Judges)
# ==============================================================================
with tab_tech:
    render_explanation(
        "Technical Architecture & Evaluator Audit",
        {
            "what": "This section documents the actual architecture, data flow, model performance, deployment recipes, and Google service integrations used in CycloneShield. It distinguishes between what runs live, what is configured for future deployment, and what remains a prototype demonstration.",
            "how": [
                "Model Performance — Internal benchmark metrics for the synthetic-training scenario model (ROC-AUC, Brier Score, feature importance).",
                "Deployment Recipe — Vertex AI and Cloud Run deployment blueprints (not the current hosting configuration).",
                "Historical Storm Data — Optional BigQuery query path for NOAA IBTrACS records (the app may use its bundled cache instead).",
                "How to Deploy — Dockerfile for Cloud Run deployment; capacity and cost depend on actual deployment settings.",
                "Google Services Used — Inventory of each Google service integration, its role in the app, primary engine, and zero-key fallback."
            ],
            "benefit": "Judges and reviewers can verify what is genuinely implemented vs. what is a configured future integration, understand the synthetic-data limitations, and see the evidence needed before production deployment.",
            "tech": [
                "Python + Streamlit — Core application framework.",
                "Folium + OpenStreetMap — Interactive geospatial mapping.",
                "Scikit-learn (Gradient Boosting) — Local ML model for scenario-based lifeline screening.",
                "Google Gemini (optional) — Multimodal vision, advisory generation, translation, bulletin parsing when live API succeeds.",
                "Open-Meteo (ECMWF IFS) — Weather and marine forecast feed when reachable.",
                "Google Earth Engine (optional) — Elevation/geospatial processing when authenticated.",
                "Google BigQuery (optional) — Historical cyclone record queries.",
                "Google Cloud Run / Vertex AI — Deployment blueprints; not the current runtime unless separately deployed."
            ],
            "limitations": "The ML model is trained and tested on synthetic physics-inspired scenarios only — metrics do not establish accuracy on real cyclone impacts. Vertex AI and Cloud Run are deployment recipes, not active managed services. Gemini features run only on explicit user action when a live response is confirmed; otherwise prepared fallbacks are shown. Earth Engine does not predict cyclones. BigQuery queries historical data only. No live alert delivery, fund release, or operational dispatch is implemented."
        },
        icon="⚙️",
        expanded=False
    )

    tech_sub1, tech_sub2, tech_sub3, tech_sub4, tech_sub5 = st.tabs([
        "🔬 Model Performance",
        "☁️ Deployment Recipe",
        "🛰️ Historical Storm Data",
        "🐳 How to Deploy",
        "🌟 Google Services Used"
    ])

    with tech_sub1:
        st.caption("📊 **What this shows:** Internal benchmark metrics for a model trained and tested on synthetic physics-inspired scenarios. These scores do not establish accuracy on real cyclone impacts or field-calibrated probabilities. **ROC-AUC** and **Brier Score** describe performance on this synthetic test split only.")
        st.markdown("**AI Model Accuracy Benchmark:**")
        st.markdown("""
        - **Train / Test Split**: A held-out split from the synthetic scenario dataset; not past observed disaster outcomes.
        - **Confidence Calibration**: Calibration describes scores against this synthetic dataset only, not observed real-world event frequencies.
        - **Accuracy Leaderboard** *(ROC-AUC: higher = better ↑ · Brier Score: lower = better ↓)*:
        """)
        if os.path.exists(METRICS_JSON_PATH):
            with open(METRICS_JSON_PATH, "r", encoding="utf-8") as f:
                saved_m = json.load(f)
            road_bench = saved_m.get("highway_cutoff", {})
            st.dataframe(pd.DataFrame([
                {"Model": k, "Accuracy (ROC-AUC ↑)": v["roc_auc"], "Precision-Recall Score (↑)": v["pr_auc"], "Confidence Error (Brier ↓)": v["brier_score"]}
                for k, v in road_bench.items()
            ]), hide_index=True)

        if os.path.exists(EVAL_PLOT_PATH):
            st.image(EVAL_PLOT_PATH, caption="CycloneShield Model Benchmark: (A) ROC Curves — how well the model separates flood vs. safe districts; (B) Precision-Recall — accuracy when predicting actual flood events; (C) Feature Importances — which inputs the model relies on most; (D) Reliability Diagram — does '70% confidence' really mean 70%?", use_container_width=True)

    with tech_sub2:
        st.caption("☁️ **What this shows:** A deployment recipe for Google Vertex AI. The model currently runs locally on CPU; no Vertex AI service or national-scale live inference is implied.")
        st.markdown("**Google Vertex AI Cloud Deployment Recipe:**")
        st.markdown("""
        The trained prediction model is saved as `lifeline_risk_model.joblib` and packaged with this schema. A production Vertex AI deployment would require separate provisioning, validation, monitoring, and an operational data pipeline.
        """)
        if os.path.exists(VERTEX_MANIFEST_PATH):
            with open(VERTEX_MANIFEST_PATH, "r", encoding="utf-8") as f:
                st.json(json.load(f))

    with tech_sub3:
        st.caption("🛰️ **What this shows:** The optional BigQuery query path for historical cyclone data. The application may use its bundled cache instead; historical records do not provide live cyclone forecasts.")
        st.markdown("**Google BigQuery: Historical Cyclone Data Query (NOAA Global Hurricane Database):**")
        if get_bigquery_pipeline:
            pipeline_inst = get_bigquery_pipeline()
            sql_text = pipeline_inst.generate_sql_query(selected_storm_name)
            st.code(sql_text, language="sql")
            st.caption("Filtered to the North Indian Ocean only (Bay of Bengal + Arabian Sea) — reduces data scanned to under 1% of the full global dataset, costing a fraction of a cent per query.")

    with tech_sub4:
        st.caption("🐳 **What this shows:** A Docker deployment recipe for Google Cloud Run. It is a blueprint, not the current hosting configuration; capacity and charges depend on deployment settings and usage.")
        st.markdown("**Google Cloud Run Deployment Recipe (Dockerfile):**")
        st.code("""FROM python:3.11-slim
ENV PYTHONUNBUFFERED=1 PORT=8080
RUN apt-get update && apt-get install -y libgdal-dev libgeos-dev curl
RUN useradd -m -u 10001 appuser
WORKDIR /app
COPY cycloneshield/requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app
RUN chown -R appuser:appuser /app
USER appuser
EXPOSE 8080
ENTRYPOINT ["sh", "-c", "streamlit run cycloneshield/app.py --server.port=${PORT:-8080} --server.address=0.0.0.0"]""", language="dockerfile")

    with tech_sub5:
        st.caption("🌟 **What this shows:** An inventory of optional Google-service integration paths and prepared fallbacks. Fallback output is not a live service response or an operational decision.")
        st.markdown("**Google Services Used & Fallbacks:**")

        google_matrix_data = [
            {
                "Google Product": "Local scikit-learn model",
                "App Location": "Tab 5: Landfall Scenario Modeler",
                "Operational Decision Made": "Scenario-based lifeline screening and possible resource actions for officer review; no units are dispatched.",
                "Primary Engine": "Local scikit-learn what-if model",
                "Zero-Key Fallback": "Configured scenario rules"
            },
            {
                "Google Product": "Local insurance calculation",
                "App Location": "Tab 6: Emergency Relief Funds",
                "Operational Decision Made": "Illustrative trigger and payout calculations; not an active policy or fund release.",
                "Primary Engine": "Configured threshold rules",
                "Zero-Key Fallback": "Example allocation model"
            },
            {
                "Google Product": "Open-Meteo weather feed",
                "App Location": "Tab 7: Real-Time Weather & Sea Conditions",
                "Operational Decision Made": "Optional forecast request; confirm the source/status badge. Not an official IMD forecast or the risk model input.",
                "Primary Engine": "Connected forecast API when available",
                "Zero-Key Fallback": "Clearly labeled scenario estimate"
            },
            {
                "Google Product": "✨ Google Gemini 2.5 Flash",
                "App Location": "Sidebar: IMD Bulletin Ingestion",
                "Operational Decision Made": "User-provided or fetched bulletin parsing; verify source and parsed track before use.",
                "Primary Engine": "Bulletin ingestion/parser path",
                "Zero-Key Fallback": "Configured historical examples"
            },
            {
                "Google Product": "✨ Google Gemini 2.5 Flash",
                "App Location": "Tab 1 & Tab 2: Broadcast Hub",
                "Operational Decision Made": "Prepared multilingual draft messages and voice workflow; not live Gemini translation or public alert delivery.",
                "Primary Engine": "Templates and optional speech services",
                "Zero-Key Fallback": "Prepared text/audio examples"
            },
            {
                "Google Product": "📸 Gemini Multimodal Vision",
                "App Location": "Tab 3: Ground Damage Triage",
                "Operational Decision Made": "User-triggered photo analysis only when a live Gemini response is confirmed; otherwise a prepared offline benchmark.",
                "Primary Engine": "Optional Gemini Vision API",
                "Zero-Key Fallback": "Prepared benchmark scene profile"
            },
            {
                "Google Product": "🌍 Google Earth Engine (GEE)",
                "App Location": "Tab 1: Situation & Hazard Maps",
                "Operational Decision Made": "Geospatial data: Can provide or process elevation layers for screening; does not predict cyclones or confirm flooding.",
                "Primary Engine": "earthengine-api (SRTM90_V4 / 30m)",
                "Zero-Key Fallback": "OpenTopodata / Local GeoJSON Cache"
            },
            {
                "Google Product": "🛰️ Google BigQuery",
                "App Location": "Tab 8 & Data Pipeline",
                "Operational Decision Made": "Storm Database: Searches historical records in seconds to compare the current cyclone with past major Indian storms.",
                "Primary Engine": "BigQuery Python API with Dry-Run Validator",
                "Zero-Key Fallback": "Curated 13-Cyclone Offline JSON Cache"
            },
            {
                "Google Product": "☁️ Google Cloud Run",
                "App Location": "Deployment Architecture",
                "Operational Decision Made": "Deployment option: Cloud Run can host the application when separately deployed; capacity and cost depend on configuration.",
                "Primary Engine": "Google Cloud Run (gcloud run deploy)",
                "Zero-Key Fallback": "Docker local runtime / Streamlit Cloud"
            },
            {
                "Google Product": "🧪 Google Colab",
                "App Location": "Submission Package",
                "Operational Decision Made": "1-Click Testing: Lets anyone run and test the complete project in Google Cloud without installing anything.",
                "Primary Engine": "Google Colab Free GPU/CPU Runtime",
                "Zero-Key Fallback": "Local Jupyter Notebook (.ipynb)"
            }
        ]

        st.dataframe(pd.DataFrame(google_matrix_data), use_container_width=True, hide_index=True)

        render_html("""
        <div style="background:rgba(66,133,244,0.1); border:1px solid rgba(66,133,244,0.3); border-radius:8px; padding:12px 16px; margin-top:10px;">
            <div style="font-weight:700; color:#93c5fd; font-size:13.5px;">🛡️ Demo Fallbacks & Service Status:</div>
            <div style="font-size:12.5px; color:#cbd5e1; margin-top:4px; line-height:1.5;">
                Some workflows have prepared fallback examples for demonstration. These are not interchangeable with live service responses; check each panel's status and source labels. Network requests and external services may fail or be unavailable.
            </div>
        </div>
        """)


# ==============================================================================
# 7. Data Transparency & State Pilot Rollout Footer
# ==============================================================================
st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

foot_c1, foot_c2 = st.columns([1.2, 1.0], gap="large")

with foot_c1:
    st.markdown("""
    <div style="background:rgba(15,23,42,0.85); border:1px solid rgba(148,163,184,0.2); border-radius:10px; padding:16px;">
        <div style="font-size:13px; font-weight:800; color:#38bdf8; margin-bottom:8px;">
            🛡️ WHERE THE NUMBERS COME FROM (DATA PROVENANCE)
        </div>
        <div style="font-size:12px; color:#cbd5e1; line-height:1.6;">
            • <span class="source-badge-real" title="Historical/configured inputs and live service responses are distinct. Check the active source and status before calling a result live.">Historical / configured inputs</span>: Bundled NOAA-derived tracks, configured district profiles, Census-era references, and open-data-derived geospatial baselines. Optional IMD/RSMC, BigQuery, and Open-Meteo requests are live only when confirmed for the current request.<br>
            • <span class="source-badge-est" title="Scenario estimates are not official forecasts or measured impacts.">Screening estimates</span>: Seawater rise and risk outputs are scenario estimates. Earth Engine can provide or process geospatial layers when authenticated; it does not predict cyclones. Live forecasts require a connected meteorological source.<br>
            • <span class="source-badge-sim" title="Practice Simulation: Realistic test scenarios based on historic storms to train disaster response teams.">Simulated Data</span>: NDRF tactical dispatch logs and ML training dataset are physics-calibrated synthetic models simulating Bay of Bengal & Arabian Sea coastal profiles.<br>
            • <b>Vertex AI Status</b>: Pre-configured and packaged as Vertex AI-Ready; inference runs locally on CPU for zero-cost reproduction.<br>
            • <b>Insurance demonstration</b>: Illustrative trigger and payout calculations only — not an active policy, verified trigger, or payment.
        </div>
    </div>
    """, unsafe_allow_html=True)

with foot_c2:
    st.markdown("""
    <div style="background:rgba(15,23,42,0.85); border:1px solid rgba(16,185,129,0.3); border-radius:10px; padding:16px;">
        <div style="font-size:13px; font-weight:800; color:#10b981; margin-bottom:8px;">
            🏛️ PILOT IN YOUR STATE (4-STEP SDMA ROLLOUT)
        </div>
        <div style="font-size:12px; color:#cbd5e1; line-height:1.6;">
            1. <b>Ingest Local Geospatial Layers</b> (Week 1): Provide district shelter GeoJSON & hospital shapefiles.<br>
            2. <b>Configure Radio & SMS Endpoints</b> (Week 2): Link regional AIR radio frequency & SDMA SMS gateway.<br>
            3. <b>Control Room Training</b> (2 Hours): Onboard district duty officers on the 5-step operational workflow.<br>
            4. <b>Optional deployment</b>: Cloud Run is a deployment path requiring separate configuration, validation, and operating-cost review.
        </div>
    </div>
    """, unsafe_allow_html=True)
