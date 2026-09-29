# CycloneShield - Comprehensive Hackathon & UX Audit Report
**Date**: September 29, 2026  
**Auditor**: Senior Full-Stack Engineer & UX Reviewer  
**Target Application**: CycloneShield (`cycloneshield/app.py` and supporting modules)  
**Hackathon Context**: Google AI Hackathon (India Edition)  
**Evaluation Criteria**: AI/Technical Execution (25%), Problem-Solution Fit (20%), Depth & Reach Across India (20%), Deployability (20%), Impact (15%)

---

## EXECUTIVE SUMMARY

CycloneShield is an ambitious disaster management decision-support prototype built for District Magistrates, State Disaster Management Authorities (SDMAs), and National Disaster Response Force (NDRF) duty officers. It combines Google Gemini 2.5/1.5 Flash (bilingual emergency advisories & multimodal damage photo triage), NOAA IBTrACS historical tracks, SRTM 30m elevation contours, speech synthesis (Cloud TTS / gTTS), and a scikit-learn predictive classifier.

**Key Finding**: While the technical components individually possess high merit, the prototype currently suffers from **severe geographical over-specialization (hardcoded to Cyclone REMAL and the West Bengal/Bangladesh Sundarbans)**, **jargon-heavy data science interfaces unsuited for stressful emergency operations**, **overstated cloud claims (Vertex AI & Earth Engine claims are largely local manifests or offline fallbacks rather than live managed endpoints)**, and **a critical deployment bug where Streamlit Community Cloud `st.secrets` are ignored**, breaking cold-start deployments.

This audit provides an unsparing analysis across the 6 Hackathon Rules, evaluates every screen from the perspective of an Indian district officer under time pressure, and defines a prioritized P0/P1 implementation blueprint.

---

## PART A: RULE-ALIGNMENT AUDIT

| Hackathon Rule | Status | Primary Evidence (File + Function) | Gap Analysis |
| :--- | :---: | :--- | :--- |
| **1. Working end-to-end prototype** | **PARTIAL** | `app.py`: `load_map_html()` (L439), ML presets (L1487-1490) | Core flow only functions for pre-baked Cyclone REMAL. Quick scenario buttons in Tab 3 are dead placeholders (`st.info` string only). Custom live tracks cannot be simulated without developer terminal intervention. |
| **2. Mandatory, meaningful Google AI** | **MET (Gemini) / PARTIAL (Cloud Ecosystem)** | `gemini_advisory.py`: `call_gemini_api()` (L235)<br>`multimodal_damage.py`: `analyze_damage_image()` (L458) | Gemini text generation and multimodal photo triage perform authentic, mission-critical work. However, Vertex AI is only an offline scikit-learn joblib model + JSON manifest; Earth Engine is an unauthenticated fallback; Translation is missing for regional Indian languages. |
| **3. Real or realistic data with clear labeling** | **PARTIAL** | `predictive_model.py`: `generate_calibrated_dataset()` (L108)<br>`surge_rain.py`: `generate_coastal_inundation_contours()` (L251) | NOAA tracks and OSM infrastructure are authentic. However, NDRF dispatch logs and ML training datasets are 100% synthetic/rule-derived, and surge inundation is an empirical proxy. **None of this synthetic/proxy nature is explicitly disclosed in the UI.** |
| **4. Built for India (multi-state & multi-community)** | **MISSING** | `data/coastal_districts.geojson`<br>`app.py` (L453, L727)<br>`surge_rain.py` (L328-346) | **The entire pipeline is hardcoded to West Bengal and Bangladesh.** Bounding boxes, latitudes (hardcoded `21.55°N`), and district lists exclude Odisha, Andhra Pradesh, Tamil Nadu, and Gujarat. |
| **5. Multilingual & voice support** | **PARTIAL** | `voice_engine.py`: `LANGUAGE_CONFIGS` (L112)<br>`app.py`: `subtab_en, subtab_hi, subtab_bn` (L885) | Only English, Hindi, and Bengali are supported. Major disaster-prone Indian states (Odisha, Andhra Pradesh, Tamil Nadu, Gujarat) lack their regional languages (Odia, Telugu, Tamil, Gujarati). UI labels do not translate. Voice playback is nested 3 tabs deep. |
| **6. Deployable by a state agency in weeks** | **PARTIAL** | `deploy_cloud_run.sh`<br>`cycloneshield/.env`<br>`app.py` (L36-47, L1054) | Container specs exist, but the application relies strictly on local `.env` files and **completely ignores `st.secrets`**. A zero-setup deployment on Streamlit Community Cloud silently drops to offline mode. No Common Alerting Protocol (CAP) or state onboarding workflow exists. |

---

### Detailed Technical Findings for Section A

#### 1. Every Hardcoded Assumption Identified
1. **Single Cyclone Locking**:
   - `app.py:L453`: `selected_storm = "remal"` hardcoded in global state.
   - `app.py:L477`: HTML banner hardcoded to `"CYCLONE REMAL (MAY 2024)"`.
   - `app.py:L558-614`: Top KPI ribbon numbers (`60 kts`, `977 mb`, `3.56 m`, `39.6 km`, `5 Hosp / 6 Shlt`) are static constants for Remal.
   - `app.py:L397, L415, L430`: Loaders directly load `remal_vulnerability_scores.csv`, `remal_advisories.json`, and `remal_district_exposure.json`.
   - `app.py:L665-678`: Map dropdown hardcodes `remal_vulnerability_map.html`, `remal_infrastructure_map.html`, etc.
2. **Geographical & Coordinate Locking**:
   - `surge_rain.py:L328-346`: Bathtub flood polygon generation hardcodes latitude vertices `(c_lon - lateral_spread, 21.55)` through `21.98` (Bengal Delta). If run for Chennai (lat 13°N) or Gujarat (lat 22°N, lon 69°E), the flood polygon generates in the ocean or Bengal!
   - `wind_swath.py:L99`: UTM projection defaults to Zone 45N (EPSG:32645). While `get_utm_epsg()` exists, several downstream modules assume Zone 45N.
   - `data/coastal_districts.geojson`: Contains only 10 administrative units (5 in West Bengal, 5 in Bangladesh). No coverage of Odisha (Puri, Ganjam, Balasore), Andhra Pradesh (Vizag, Krishna), Tamil Nadu (Chennai, Nagapattinam), or Gujarat (Kutch, Dwarka).
   - `data/osm_infrastructure_baseline.geojson`: Only contains 86 features, strictly limited to West Bengal and Khulna/Barisal.

#### 2. Supported States, Cyclones, and Languages in Current UI
- **States/Regions**: West Bengal (India) and Khulna/Barisal Divisions (Bangladesh).
- **Cyclones**: REMAL (May 2024) on the active dashboard. (Other cyclones—Amphan, Yaas, Fani, Mocha, Dana, Sidr—are listed only in the BigQuery CSV download tab).
- **Languages**: English (`en-IN`), Hindi (`hi-IN`), Bengali (`bn-IN/bn-BD`). Missing: Odia, Telugu, Tamil, Gujarati, Malayalam.

#### 3. Silent Fallbacks to Mock/Cached Data
- **Earth Engine DEM**: `surge_rain.py` advertises live GEE SRTM ingestion. In runtime, GEE credentials are absent, and the engine silently switches to pre-computed coordinate contours without user notification.
- **Overpass OSM API**: `infra_exposure.py:L123-143` attempts a 6-second live query. If rate-limited, it silently reverts to `osm_infrastructure_baseline.geojson` without displaying an "Offline Baseline" badge in the UI.
- **Gemini Advisory Generation**: In Tab 1, initial view displays pre-baked JSON (`remal_advisories.json`) without indicating whether it was live-generated or pre-computed.
- **Predictive ML Simulator**: In Tab 1 (L841-860), a pill states `"Calibrated ML Failure Risk (Vertex AI Model)"`, but inference executes purely on a local scikit-learn `.joblib` model.

#### 4. Vertex AI and Earth Engine Reality Check
- **Vertex AI**: **Not live at runtime.** The repository contains a static metadata file `outputs/models/vertex_model_config.json` and a Python script snippet showing how one *would* upload to Vertex AI. The app executes a local `HistGradientBoostingClassifier` on CPU. It should be transparently labeled as **"Vertex AI-Ready"**.
- **Google Earth Engine**: **Not live at runtime.** The app uses pre-rendered Folium HTML maps or local geometric polygon clipping.

#### 5. ML Labels & Training Disclosure
- **Reality**: The training dataset in `predictive_model.py:L108` (`generate_calibrated_dataset`) generates 3,600 synthetic rows using parametric physics equations (exponential surge decay, pluvial ponding formulas). Road cutoff and hospital inundation labels are rule-derived binary thresholds (`water > 0.3m`, `surge > 0.5m`).
- **UI Disclosure**: **Zero disclosure.** The dashboard presents "ROC-AUC: 0.975" and "Confidence: 97.5%", creating a false impression of empirical historical validation.

#### 6. Error Handling & Rate Limiting (Gemini, Earth Engine, TTS)
- **Gemini Missing Key**: Gracefully intercepted in Tab 1 and Tab 2, showing a blue "Zero-Key Calibrated Engine" banner.
- **Gemini Rate Limiting (15 RPM / 429)**: `multimodal_damage.py:L406` catches HTTP errors and logs to terminal, falling back to calibrated heuristics, but fails to show an informative alert to the user in the UI (e.g., "Free tier rate limit reached; using verified benchmark scenario").
- **TTS Failure**: Falls back to gTTS, and if gTTS fails, generates a synthetic WAV tone alert. This is robust, but the user is not informed which tier synthesized the audio.

#### 7. Cold Start on Streamlit Community Cloud
- **Failure Condition**: `app.py:L36-47` only searches for local `.env` files. `os.environ.get("GEMINI_API_KEY")` does not automatically populate from `st.secrets["GEMINI_API_KEY"]` on Streamlit Cloud unless explicitly bound.
- **Result**: A cold start on Streamlit Cloud will run in offline mode even if the user correctly enters their API keys in the Streamlit Cloud dashboard.

---

## PART B: UX & PLAIN-LANGUAGE AUDIT

### Target Persona
**District Magistrate (DM) / Collector / SDMA Duty Officer**:
- Operating under high stress during cyclone alert phase (Landfall -24h to Landfall +6h).
- Non-technical background (Administrative service, civil protection).
- Needs to answer three questions in **5 seconds**:
  1. *What is happening and where will it hit?*
  2. *Which evacuation corridors and hospitals will drown first?*
  3. *What concrete directive must I issue to NDRF/police right now?*

---

### Screen-by-Screen Review & Scoring (Scale 1–5)

#### 1. Header & Landing View
- **Current State**: Shows "DEV-FEST DEMO", "Synoptic intensity timeline", a Persona radio toggle ("Disaster Operations" vs "Hackathon Evaluator"), and an expander with 3 steps.
- **Jargon Flagged**: "Synoptic intensity timeline", "Hackathon Evaluator & Architecture Audit Mode", "ROC-AUC, BigQuery & Vertex Specs Visible".
- **UX Defect**: High visual clutter. No instant "Situation at a Glance" card answering landfall ETA, primary impact zone, or total lives at risk.
- **Score**: **2.5 / 5**  
  *Justification*: Too much meta-commentary about the hackathon. A real commander would be confused by a "Hackathon Evaluator Mode" switch.

#### 2. Strategic KPI Metrics Ribbon (6 Cards)
- **Current State**: Wind (60 kts), Pressure (977 mb), Peak Surge (3.56 m), Cut-Off Highways (39.6 km), Submerged Facilities (5 Hosp / 6 Shlt), Priority Districts (2 Districts).
- **Jargon Flagged**: "Eye Wall Pressure: 977 mb", "Eye Deficit ΔP = 36 mb", "SRTM 30m Bathtub via GEE", "Overpass Spatial Intersect", "XAI Vulnerability > 80.0".
- **UX Defect**: Technical units like "977 mb" or "60 kts" lack immediate real-world severity context for a civilian administrator.
- **Score**: **2.5 / 5**  
  *Justification*: Good data, but needs plain-language equivalence (e.g., "60 kts (~111 km/h) • Cat 1 / Severe").

#### 3. Tab 1: Multi-Hazard Geospatial Viewer & District AI Inspector
- **Current State**: Folium map on left with layer selector; District score card, 4 lifeline pills, ML risk telemetry pill, XAI attribution breakdown, and 3 nested tabs (Broadcast, Dispatch, Live Gemini) on right.
- **Jargon Flagged**: "Cartographic Layer", "Dynamic Multi-Tier Wind Swaths (Core / Gale / Squall)", "UTM 45N (EPSG:32645)", "Explainable AI (XAI) Risk Attribution Breakdown", "Platt scaling".
- **UX Defect**: Massive cognitive overload. Finding the audio broadcast requires clicking through *Tab 1 → Subtab 1 → Language Sub-subtab → Generate Audio*. That is 4 clicks to hear an emergency warning!
- **Score**: **2.0 / 5**  
  *Justification*: The maps and advisories are high quality, but buried under academic layout and nested tabs.

#### 4. Tab 2: Citizen & NDRF Ground Damage AI Photo Triage (Gemini Vision)
- **Current State**: Benchmark radio selector, photo preview, 4 metric pills (Water depth, Access status, Urgency, Confidence), Gemini visual observations, NDRF directive box, required equipment pills, raw JSON expander.
- **Jargon Flagged**: "INC-TRIAGE-01", "Access Impediment", "Urgency Window Hours", "Machine-Parsable Structured JSON Payload".
- **UX Defect**: Raw technical JSON is prominent. Water depth is presented as a raw float.
- **Score**: **3.5 / 5**  
  *Justification*: Visually compelling and actionable. Needs plain English ("Damage Level: 4/5 - Severe", "Road Cut: Yes", "Rescue Gear Needed").

#### 5. Tab 3: Predictive Lifeline ML Engine & Dynamic Risk Simulator
- **Current State**: Slider lab for surge/wind/rain delta, 10-district prediction table, single-facility risk profiler, model benchmark leaderboard, 4-panel ROC/PR evaluation curves, Vertex AI Python deployment code.
- **Jargon Flagged**: "Hist-GB", "ROC-AUC: 0.975", "Brier Score", "PR-AUC", "Platt Sigmoidal Calibration", "Soil Saturation Index", "Drainage Sluice Capacity", `us-docker.pkg.dev/vertex-ai/...`.
- **UX Defect**: This is a pure machine learning research dashboard, completely impenetrable to an emergency officer.
- **Score**: **1.5 / 5**  
  *Justification*: High technical quality for AI judges, but in the default ops mode it alienates disaster managers. Must be packaged as an intuitive "What-If Landfall Scenario Modeler", with technical metrics collapsed into a Technical Review section.

#### 6. Tab 4: BigQuery NOAA Ingestion & Serverless Cloud Run
- **Current State**: BigQuery connection status ribbon, dry-run cost estimation, historical storm selector, SQL query code box, historical leaderboard, Cloud Run container specs, Dockerfile, and shell scripts.
- **Jargon Flagged**: "Dry-Run Cost Estimation", "Partition Pruning", "Bytes Scanned: 40.0 MB", "Scale-to-Zero", "Port 8080".
- **UX Defect**: Completely irrelevant to disaster management operations.
- **Score**: **1.0 / 5 (For Ops) / 4.5 / 5 (For Architecture Judges)**  
  *Justification*: Must be moved into a dedicated "Technical Architecture & Audit" container so emergency managers never see raw SQL or Dockerfiles during a cyclone.

#### 7. Tab 5: Multi-District Vulnerability & Lifeline Risk Matrix
- **Current State**: Table of 10 districts with scores, threat tier, evacuation priority, flooded hospitals, shelters, road cut km, and hazard multiplier.
- **Jargon Flagged**: "Hazard Intensity Multiplier", "Attribution Healthcare Pct".
- **UX Defect**: Missing total population exposed, number of people needing shelter, and copy-ready dispatch directives.
- **Score**: **3.0 / 5**  
  *Justification*: Clean table, but lacks population grounding and immediate operational action hooks.

---

### Cross-Cutting Accessibility & Usability Issues
1. **Color-Only Severity**: In several tables and metric pills, severity is signaled by color alone (e.g. red/amber borders) without an explicit text indicator (`CRITICAL`, `HIGH`). This fails WCAG AA accessibility for color-blind duty officers.
2. **Micro Font Sizes**: Sub-labels frequently use `9.5px` or `10px` font sizes, rendering them unreadable on mobile tablets or ruggedized laptops in field command vehicles.
3. **Contrast Ratios**: Muted gray `#94a3b8` on dark blue `#0b1120` gives a 3.8:1 contrast ratio, failing WCAG AA (requires 4.5:1 for normal text).
4. **No Step-by-Step Workflow**: The app currently presents 5 sprawling tabs simultaneously. An emergency manager needs a linear flow: **1. Choose Location → 2. See Risk → 3. Broadcast Alert → 4. Assess Damage → 5. Dispatch Units**.

---

## PART C: PRIORITIZED FIX LIST & EFFORT ESTIMATES

### Priority P0: Must-Fix (Critical Hackathon Alignment & Disqualification Risks)

| ID | Issue & Action Item | Target Files | Effort |
| :--- | :--- | :--- | :---: |
| **P0-1** | **Multi-State & Multi-Cyclone Pipeline Architecture**<br>• Add State selector: West Bengal, Odisha, Andhra Pradesh, Tamil Nadu, Gujarat.<br>• Filter cyclones by coast/state (e.g., FANI/YAAS for Odisha, HUDHUD/MICHAUNG for AP, VARDAH/GAJA for TN, BIPARJOY for Gujarat).<br>• Expand `coastal_districts.geojson` to include all coastal districts across these 5 states with Census populations.<br>• Parameterize dynamic UTM zones (`get_utm_epsg`) and remove hardcoded Bengal coordinates (`21.55°N`) from `surge_rain.py`. | `app.py`<br>`data/coastal_districts.geojson`<br>`surge_rain.py`<br>`track_input.py` | 3.5 hrs |
| **P0-2** | **Live IMD / Custom Track Ingestion & Scenario Builder**<br>• Add "Upload / Enter Custom Track" mode (CSV: time, lat, lon, wind_kts, pressure_mb) enabling duty officers to ingest live IMD bulletins during active storms.<br>• Compute dynamic wind swaths, surge estimates, and district impact on demand. | `app.py`<br>`track_input.py`<br>`bigquery_pipeline.py` | 2.0 hrs |
| **P0-3** | **Regional Languages & One-Click Voice Broadcast Expansion**<br>• Expand `LANGUAGE_CONFIGS` in `voice_engine.py` to include Odia (`or-IN`), Telugu (`te-IN`), Tamil (`ta-IN`), and Gujarati (`gu-IN`) alongside English, Hindi, and Bengali.<br>• Add top-level Language Picker translating core UI headings and alert banners.<br>• Add direct 1-click "🔊 Play Spoken Broadcast Alert" button on every district advisory card without nested tabs. | `voice_engine.py`<br>`gemini_advisory.py`<br>`app.py` | 2.5 hrs |
| **P0-4** | **Streamlit Cloud `st.secrets` & Rate-Limit Graceful Degradation**<br>• Explicitly inspect `st.secrets` in `app.py`, `gemini_advisory.py`, `multimodal_damage.py`, and `voice_engine.py` so cloud deployments with secrets never fail.<br>• Add friendly, visible banners when Gemini API hits 15 RPM rate limits or runs in calibrated offline mode.<br>• Add `@st.cache_data` wrappers around all expensive data transformations. | `app.py`<br>`gemini_advisory.py`<br>`multimodal_damage.py` | 1.5 hrs |
| **P0-5** | **Executive "Situation at a Glance" Command Card**<br>• Replace current jargon header with an urgent Situation Card: Cyclone Name, Category, Landfall ETA & Location, Overall Risk Level (Color + Icon + Text), Total Population at Risk, and Top 3 Immediate Directives. | `app.py` | 1.5 hrs |
| **P0-6** | **Transparency, Data Provenance & Honest AI Claims**<br>• Clearly badge all data: Real (NOAA IBTrACS, SRTM, OSM) vs Simulated (NDRF logs, synthetic ML dataset).<br>• Disclose in plain language that ML models are trained on physics-simulated coastal profiles.<br>• Rebrand all Vertex AI mentions to **"Vertex AI-Ready"** and clarify that GEE bathtub inundation is an empirical screening model. | `app.py`<br>`predictive_model.py`<br>`README.md` | 1.0 hrs |

---

### Priority P1: Should-Fix (Substantially Boosts Problem-Solution Fit & Deployability)

| ID | Issue & Action Item | Target Files | Effort |
| :--- | :--- | :--- | :---: |
| **P1-1** | **Plain-Language UX Rewrite & Jargon Removal**<br>• Replace technical jargon: "Vulnerability Score" → "Risk Level (0-100)", "Wind Swath" → "Areas Hit by Damaging Winds", "Bathtub Inundation" → "Areas at Risk of Sea Water Flooding", "Lifeline Exposure" → "Hospitals, Roads & Shelters at Risk".<br>• Add "What does this mean?" tooltips to every score and map layer.<br>• Move all developer/judge technical deep-dives (ROC-AUC curves, Brier scores, BigQuery dry-run bytes, Dockerfile, shell scripts) into a collapsed "Technical & Architecture Review" section. | `app.py` | 2.0 hrs |
| **P1-2** | **Ranked District Priority & Action Directive List**<br>• Provide a simple priority card list: District Name, Risk Tier, Primary Hazard, and Action Directive (e.g. "Order immediate evacuation of Sagar Island before 18:00"). | `app.py` | 1.0 hrs |
| **P1-3** | **Multi-Channel Alert Delivery & CAP Export**<br>• Add "Alert Delivery" panel with pre-formatted, copy-ready emergency broadcast messages for SMS (160 char limit), WhatsApp, and Community Radio.<br>• Add one-click download for Common Alerting Protocol (CAP 1.2 XML / JSON) format for direct SDMA ingestion. | `app.py`<br>`gemini_advisory.py` | 1.5 hrs |
| **P1-4** | **Population & Human Impact Metrics Panel**<br>• Add exposed human population estimates per district (grounded in Census data), operational cyclone shelter capacity, and hospital bed shortfall. | `app.py`<br>`vuln_scoring.py` | 1.0 hrs |
| **P1-5** | **"Pilot in Your State" 4-Step Rollout Guide**<br>• Add an actionable 4-step onboarding plan for state agencies: 1. Upload shelter/hospital shapefile → 2. Configure regional radio frequencies → 3. Train control room operators (2 hours) → 4. Go live on Cloud Run. | `app.py`<br>`README.md` | 1.0 hrs |

---

### Priority P2: Nice-to-Have (Polish & Presentation)

| ID | Issue & Action Item | Target Files | Effort |
| :--- | :--- | :--- | :---: |
| **P2-1** | **Repository Documentation & Submission Polish**<br>• Update `README.md` with multi-state support, live demo link, architecture diagram, and honest data source breakdown.<br>• Update `DEMO_SCRIPT.md` to a tight 3-5 minute presentation walkthrough.<br>• Add 10-12 slide Pitch Deck outline in `PITCH_DECK.md`. | `README.md`<br>`DEMO_SCRIPT.md`<br>`PITCH_DECK.md` | 1.5 hrs |
| **P2-2** | **Mobile Responsiveness & WCAG AA Contrast Polish**<br>• Enforce minimum 14px font size for all data captions and 16px for body text.<br>• Ensure all severity cues combine color, icon, and text badges. | `app.py` | 1.0 hrs |

**Total Estimated Implementation Effort**: ~18.5 hours.

---

## NEXT STEPS: PROCEEDING TO PHASE 2 (IMPLEMENTATION)

With the audit complete and every finding substantiated with file lines and evidence, we proceed immediately to Phase 2:
1. Implement all **P0** and **P1** items.
2. Deliver code changes, `CHANGELOG.md`, UI copy before/after table, and a 5-minute verification test checklist.
