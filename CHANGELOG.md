# CycloneShield — Changelog & Optimization History

All notable changes and technical optimizations made to CycloneShield for the Google AI Hackathon are documented in this file.

---

## [2.0.0] - Phase 1 & Phase 2 Hackathon Overhaul (September 2026)

### 🚨 Critical Fixes & Cold Start Robustness (P0)

- **Fixed Streamlit Secrets Resolution (`st.secrets`)**:
  - Implemented `get_resolved_api_key()` across `app.py`, `voice_engine.py`, `gemini_advisory.py`, and `multimodal_damage.py`.
  - Replaced hardcoded `os.environ.get("GEMINI_API_KEY")` with a priority cascade: `st.secrets["GEMINI_API_KEY"]` $\to$ `st.secrets["GOOGLE_API_KEY"]` $\to$ OS environment $\to$ `.env`.
  - Fixes Streamlit Community Cloud cold start crash where API keys stored in secrets were ignored.
- **Removed Single-State Bengal Delta Hardcoding**:
  - Expanded `coastal_districts.geojson` from 10 districts (West Bengal / Bangladesh only) to **35 coastal districts** across **5 key Indian states**: West Bengal, Odisha, Andhra Pradesh, Tamil Nadu, and Gujarat.
  - Added authentic Census 2011/projected population figures, coastal area metadata, and representative district coordinates.
- **Dynamic Inundation Coordinates**:
  - Refactored `surge_rain.py` bathtub inundation generator from hardcoded Bengal Delta coordinates (`21.55°N, 88.5°E`) to dynamically anchor against actual cyclone landfall coordinates `(c_lat, c_lon)`.
  - Generates realistic coastal sea flood hazard polygons for Odisha (Puri/Paradip), Andhra Pradesh (Visakhapatnam), Tamil Nadu (Chennai/Nagapattinam), and Gujarat (Saurashtra/Kutch).
- **Graceful API Fallbacks (No Stack Traces)**:
  - Wrapped all Gemini 2.5 Flash, Cloud Translation, Cloud TTS, and BigQuery calls in defensive exception handlers.
  - Added pre-computed zero-config fallbacks for every supported district, ensuring the app functions seamlessly even when offline, unauthenticated, or rate-limited (15 RPM free tier).
  - Replaced raw runtime errors with friendly, actionable warning toasts and status badges in the UI.

---

### 🇮🇳 Multi-State & National Reach Enhancements (P0 / P1)

- **State & Storm Dynamic Selectors**:
  - Added State Selector in the sidebar: **West Bengal**, **Odisha**, **Andhra Pradesh**, **Tamil Nadu**, and **Gujarat**.
  - Dynamically filters storm list by coast and state:
    - *West Bengal*: Remal (2024), Amphan (2020), Yaas (2021)
    - *Odisha*: Fani (2019), Dana (2024), Phailin (2013)
    - *Andhra Pradesh*: Hudhud (2014), Michaung (2023)
    - *Tamil Nadu*: Vardah (2016), Gaja (2018), Michaung (2023)
    - *Gujarat*: Biparjoy (2023), Tauktae (2021)
- **Live IMD / Custom Track Ingestion**:
  - Added custom track ingestion mode in sidebar allowing disaster managers to upload custom CSV tracks (`time, lat, lon, wind_kts, pressure_hpa`).
  - Added a 1-click **"Load Sample IMD Bulletin"** button simulating live IMD synoptic warnings without requiring manual file uploads.
- **Comprehensive Historical NOAA Dataset (`noaa_sample_tracks.json`)**:
  - Enriched sample tracks from 7 storms to **13 major historical Indian cyclones** using verified NOAA IBTrACS data.
- **Dynamic UTM Projection**:
  - Parameterized spatial wind swath generator to dynamically calculate the correct UTM EPSG zone based on cyclone longitude (`EPSG:32642` for Gujarat, `EPSG:32644` for AP/TN/Odisha, `EPSG:32645` for Bengal).

---

### 🗣️ Multilingual & Voice-First Engine (P1)

- **Expanded to 7 Regional Indian Languages**:
  - Added native voice and text support for:
    - **English** (`en-IN`, Neural2-D / Indian Accent)
    - **Hindi** (`hi-IN`, Swara / Neural2-D)
    - **Bengali** (`bn-IN`, Bashkar / Neural2-A)
    - **Odia** (`or-IN`, Google Cloud TTS / Gemini Translation)
    - **Telugu** (`te-IN`, Mohan / Neural2-A)
    - **Tamil** (`ta-IN`, Pallavi / Neural2-A)
    - **Gujarati** (`gu-IN`, Dhwani / Neural2-A)
- **Top-Level Regional Language Selector**:
  - Embedded language selector at the very top of the application.
  - Automatically translates primary UI section headers, metrics, and broadcast alerts.
- **One-Click Audio Playback**:
  - Added an audio **"Play Voice Alert"** button directly adjacent to every district emergency bulletin.
  - Fallback pipeline cascades: Google Cloud TTS $\to$ gTTS $\to$ pre-cached audio generator.

---

### 🎨 Plain-Language UX & Decision-Maker Ergonomics (P1)

- **"Situation at a Glance" Executive Card**:
  - Replaced dense technical charts on initial load with a high-impact summary card:
    - Cyclone Name & Category
    - Landfall Location & Estimated Landfall Time (ETA)
    - Overall Risk Level (`LOW`, `MODERATE`, `HIGH`, `EXTREME`) with visual badge and color-coding
    - Total Exposed Population & Number of Districts in Path
    - **Top 3 Immediate Directives** (e.g., Evacuation window, Highway closure, Shelter opening)
- **Elimination of Technical Jargon**:
  - Replaced "XAI Composite Vulnerability Score (0-100)" with **"District Risk Level (0-100)"**.
  - Replaced "UTM 45N Wind Swath Polygon" with **"Areas Hit by Strong Winds"**.
  - Replaced "Bathtub Inundation Model (SRTM 30m DEM)" with **"Areas Likely to Flood from Sea Water"**.
  - Replaced "Lifeline Infrastructure Spatial Join" with **"Hospitals, Roads & Shelters at Risk"**.
- **Intuitive Visual Hierarchy**:
  - Added *"What does this mean?"* tooltips and expanders across every score and map layer.
  - Formatted district priorities into a clear actionable table: `District | Risk Level | Why (One sentence) | Recommended Action`.
  - Streamlined Photo Damage Triage into plain-language cards: `Damage Tier (1-5)`, `What is Blocked`, `What is Needed`, `Next Step` (raw JSON hidden by default).
- **Consolidated Technical Inspector**:
  - Moved scikit-learn ROC-AUC curves, Vertex AI manifests, BigQuery FinOps dry-run estimators, and raw JSON schemas into a collapsed **"🔬 For Technical Reviewers & Judges"** section at the bottom.

---

### 🛡️ Transparency, Trust & Data Provenance (P1)

- **Visible Provenance Badges**:
  - Marked every data component with an explicit origin tag:
    - 🟢 `REAL`: NOAA IBTrACS tracks, USGS/NASA SRTM 30m elevation, OpenStreetMap hospital/road locations, Census 2011 populations.
    - 🟡 `SCREENING MODEL`: Coastal bathtub surge model and empirical barometric pressure deficit formula (labeled as screening-level estimates).
    - 🔵 `SIMULATED`: NDRF tactical incident dispatch logs and synthetic damage verification labels.
- **Honest AI & ML Disclosures**:
  - Disclosed that the predictive lifeline ML model was trained on 3,600 physics-simulated disaster scenarios with calibrated probabilities, with real-world validation on the roadmap.
  - Clarified Vertex AI status as **"Vertex AI-Ready"** (manifest and serving schema provided) rather than claiming an active paid cloud endpoint.
- **Interoperability & Dissemination**:
  - Added **OASIS Common Alerting Protocol (CAP v1.2) XML export** download.
  - Added copy-ready broadcast snippets formatted for SMS, WhatsApp Emergency Groups, and All India Radio / Community Radio broadcasts.
