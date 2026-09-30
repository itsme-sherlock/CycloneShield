# 🎬 CycloneShield — Master Demo Video Recording & Voiceover Guide

> **Live Production Website**: [https://cycloneshield-vawrqbhtbgu8i6cafhbf3q.streamlit.app](https://cycloneshield-vawrqbhtbgu8i6cafhbf3q.streamlit.app)  
> **Local Backup Mirror**: `http://localhost:8501`  
> **Master Demo Video (MP4)**: [`CycloneShield_Demo_Walkthrough.mp4`](./CycloneShield_Demo_Walkthrough.mp4) (H.264 + AAC, 1080p, Universal Playback)  
> **Master Demo Video (WebM)**: [`cycloneshield_demo_walkthrough.webm`](./cycloneshield_demo_walkthrough.webm)  
> **Master Video Runtime**: **3 Minutes 45 Seconds (225 Seconds)** (Strictly within the 3:00 – 5:00 minute hackathon submission requirement)  
> **Synchronized Studio Audio**: [`cycloneshield_demo_voiceover.mp3`](./cycloneshield_demo_voiceover.mp3)  
> **Pitch Deck Alignment**: 100% mapped to the 12 slides in [`PITCH_DECK.md`](./PITCH_DECK.md) and [`CycloneShield_Pitch_Deck.pptx`](./cycloneshield/CycloneShield_Pitch_Deck.pptx)  

---

## 🧭 Executive Video Architecture (100% Verified Against Current `app.py` Home Page & Tabs)

| Timestamp | Act Title | Pitch Deck Slide | Live Web App Action (`app.py` Exact Home Page & Tabs) | Google Tech Highlight |
| :---: | :--- | :---: | :--- | :--- |
| **0:00 – 0:32** | **The Hook & Last-Mile Gap** | Slides 1 & 2 | Home Page: `🚨 SITUATION AT A GLANCE` Card (`32.6M Citizens`, `73.0 km Cut-Off Roads`) & 6 KPI Metric Cards | Google Material Dark UI & Cloud Run |
| **0:32 – 1:05** | **Top Control Bar & Multi-State Catalog** | Slides 3 & 4 | Top 3 Dropdowns (`📍 State`, `🌀 Cyclone Event`, `🌐 Language`) + Optional Custom IMD CSV inside Dropdown 2 | Dynamic UTM Projection & NOAA IBTrACS |
| **1:05 – 1:42** | **Spatial Hazard & District AI** | Slides 3 & 6 | Tab 1: Map Layer Dropdown (5 Views), Folium Map & Right-Side `🤖 District AI Inspector` (`84.0 / 100`) | NASA SRTM 30m DEM & Explainable AI |
| **1:42 – 2:18** | **Voice Alerts & CAP Export** | Slides 4 & 6 | Tab 1 Bottom Audio Player (`Bengali`) + Tab 2: SMS/WhatsApp/Radio & `📥 Download CAP 1.2 XML Alert` | Gemini 2.5 Flash & Google Cloud TTS |
| **2:18 – 2:52** | **Gemini Multimodal Photo Triage** | Slide 5 | Tab 3: `Choose Benchmark Field Scene` (`NH-117`), `🔍 Run Gemini Damage Triage`, 4 KPI Cards & Equipment Pills | Gemini Multimodal Vision |
| **2:52 – 3:24** | **Risk Matrix & What-If Simulator** | Slide 7 | Tab 4: District Matrix & CSV Download; Tab 5: `🌊 Spring Tide (+1.5m)` Preset, 3 Sliders & Sub-5ms ML Table | Scikit-Learn (ROC 0.941) & Vertex AI |
| **3:24 – 3:45** | **Architecture, FinOps & Close** | Slides 8, 10, 12 | Tab 6: 4 Audit Sub-Tabs (ROC, Vertex AI, BigQuery SQL, Cloud Run Dockerfile) & Bottom Provenance/Pilot Cards | BigQuery Public Data & 100% Free Tier |

---

## 🎙️ Master Second-by-Second Storyboard & Teleprompter Script

### 🎬 ACT 1: The Hook & India's "Last-Mile Disaster Gap" (0:00 – 0:32)
- **Deck Slide**: Slide 1 (*Vision & Executive Summary*) & Slide 2 (*The Problem: India's 7,516 km Coastline*)
- **Exact Screen Action on `app.py` Home Page**:
  1. Full-screen browser open at 1080p displaying [cycloneshield-vawrqbhtbgu8i6cafhbf3q.streamlit.app](https://cycloneshield-vawrqbhtbgu8i6cafhbf3q.streamlit.app).
  2. Cursor hovers across the **`🚨 SITUATION AT A GLANCE • EXECUTIVE ACTION DIRECTIVE`** card at the top of the home page:
     - Heading: `Cyclone REMAL • WEST BENGAL`
     - `📍 Expected Landfall: West Bengal / Bangladesh Coast (2024-05-28 06:00:00)`
     - `👥 Citizens at Risk: 32.6 Million across 5 Coastal Districts`
     - Red threat badge on the right: `● CRITICAL / CATASTROPHIC` (`Max Winds: 60 kts (111 km/h) • Surge: 3.56 m`)
     - Red directive box inside the card: `⚠️ TOP PRIORITY IMMEDIATE OPERATIONAL ACTIONS (NEXT 6 HOURS)` (1. Immediate Evacuation of Sundarbans Estuary, 2. Arterial Route Protection for 73.0 km cut-off, 3. Healthcare Contingency 125 kVA generators).
  3. Cursor moves across the **6 KPI Metric Cards** directly below the Situation card:
     - `PEAK SUSTAINED WIND`: `60 kts` (`≈ 111 km/h · Very Severe Cyclonic Storm`)
     - `STORM EYE PRESSURE`: `977 hPa` (`↓ 36 hPa below normal sea-level pressure`)
     - `PEAK COASTAL SURGE`: `3.56 m` (`Seawater rise above normal tide` · `Estimated`)
     - `FLOODED & CUT-OFF ROADS`: `73.0 km` (`Main roads impassable for emergency vehicles`)
     - `FLOODED HOSPITALS & SHELTERS`: `7 Hospitals / 10 Shelters` (`Facilities at risk of flood inundation`)
     - `MANDATORY EVACUATION ZONES`: `1 Districts` (`Highest life-threat — evacuate immediately`)
- **Spoken Script (Word-for-Word)**:
  > *"Namaste judges. Over 188 million Indian citizens live along our 7,500-kilometer coastline, facing recurring severe cyclonic storms in the Bay of Bengal and Arabian Sea.  
  > While agencies like the IMD forecast cyclone trajectories with remarkable precision, disaster commanders hit a fatal **'Last-Mile Disaster Gap'**:  
  > synoptic wind isobars do not tell a District Magistrate which evacuation highways will drown under coastal surge, which rural hospitals will lose backup power, or how to alert fishing communities when cellular networks collapse.  
  > This is **CycloneShield**—an end-to-end, multi-state disaster operations command center converting cyclone tracks into street-level lifeline actions before landfall."*

---

### 🎬 ACT 2: Top Control Bar & Multi-State Cyclone Selection (0:32 – 1:05)
- **Deck Slide**: Slide 3 (*Track-Based Multi-Hazard Spatial Engine*) & Slide 4 (*Multi-State Demo Scenarios*)
- **Exact Screen Action on `app.py` Home Page**:
  1. Cursor moves to the very top of the Home Page, where the **3 Top Control Bar Dropdowns** sit side-by-side:
     - **Dropdown 1 — `📍 Select Vulnerable Coastal State:`** (Currently `West Bengal`; click to show the 5 supported states: `West Bengal`, `Odisha`, `Andhra Pradesh`, `Tamil Nadu`, `Gujarat`).
     - **Dropdown 2 — `🌀 Select Cyclone Event:`** (Currently `REMAL (2024) — Very Severe Cyclonic Storm`; click to show historical cyclones for the selected state plus the bottom option `➕ Enter / Upload Custom Live IMD Track (CSV)`).
     - **Dropdown 3 — `🌐 App & Broadcast Language:`** (Currently `Bengali (বাংলা)`; click to show the 7 languages: `English`, `Hindi (हिंदी)`, `Bengali (বাংলা)`, `Odia (ଓଡ଼ିଆ)`, `Telugu (తెలుగు)`, `Tamil (தமிழ்)`, `Gujarati (ગુજરાતી)`).
  2. *(Note on Custom Live IMD Track)*: The `📥 Live IMD Bulletin Ingestion / Custom Cyclone Track Builder` expander is hidden by default so the home page stays clean. It **only appears** if you open Dropdown 2 (`🌀 Select Cyclone Event:`) and select the last item `➕ Enter / Upload Custom Live IMD Track (CSV)`. During the live demo, you can either just open Dropdown 2 to show that option in the menu, or keep `REMAL (2024)` selected.
- **Spoken Script (Word-for-Word)**:
  > *"CycloneShield is built for all of India—scaling across our vulnerable eastern and western coastlines. In the three selectors at the top of the home page, duty officers can switch between major coastal states—West Bengal, Odisha, Andhra Pradesh, Tamil Nadu, and Gujarat—choose from 13 historical cyclones or select custom live IMD CSV track ingestion directly from the Cyclone Event dropdown, and switch the broadcast language across seven Indian languages.  
  > For Cyclone Remal in West Bengal, our spatial engine dynamically projects multi-tier wind swaths and applies NASA SRTM 30-meter elevation screening across 32.6 million citizens, flagging 73 kilometers of flooded highways and seven inundated hospitals in under three seconds."*

---

### 🎬 ACT 3: Tab 1 — Hazard Maps, Layer Selector & District AI Inspector (1:05 – 1:42)
- **Deck Slide**: Slide 3 (*Explainable AI Formula*) & Slide 4 (*Geospatial Hazard Intersect*)
- **Exact Screen Action on `app.py` Home Page (Tab 1 is open by default)**:
  1. Look at **Tab 1: `🗺️ 1. Situation & Hazard Maps`** (active by default on the home page).
  2. Point to the left column: **`🗺️ Interactive Multi-Hazard Geospatial Intelligence Viewport`** (`Google Satellite & Carto Hybrid Basemaps`).
  3. Click the layer selector dropdown directly above the map (currently showing `🏥 District Risk & Critical Lifelines (Recommended)`) to display the 5 map views:
     - `🏥 District Risk & Critical Lifelines (Recommended)`
     - `🛣️ Severed Highways & Evacuation Corridors`
     - `🌊 Coastal Surge Inundation & Sea Water Ingress`
     - `🌪️ Damaging Wind Swaths (Core / Gale / Squall)`
     - `🛰️ Cyclone Track & Landfall Eye Timeline`
  4. Hover across the interactive Folium dark-mode map and the 3-item cartographic bar below it (`🗺️ Terrain Data: NASA SRTM 30-m Satellite Elevation`, `🌪️ Storm Tracks: NOAA Global Historical Cyclone Archive`, `🏥 Infrastructure: OpenStreetMap`).
  5. Move cursor to the right column: **`🤖 District AI Inspector & Directives`** (`Google Gemini 2.5 Flash`).
  6. Under `Select Coastal District to Inspect:`, keep `South 24 Parganas` selected and point to the glass panel:
     - `South 24 Parganas` (`West Bengal, India • Pop: 81.6 Lakh (8,161,961)`)
     - Badge: `● CRITICAL` | Score: **`84.0 / 100`**
     - `⚠️ Primary Risk Factor: Core Eyewall Winds & Catastrophic Storm Surge`
     - `🚨 Evacuation Directive: Priority 1 (Order mandatory evacuation of Sundarbans Estuary within 6 hours. Pre-position 4 NDRF boat teams.)`
  7. Point to the **4 Lifeline Metric Boxes** directly below the South 24 Parganas card:
     - `HOSPITALS`: **`4/8`** (`At Flood Risk`)
     - `SHELTERS`: **`6/18`** (`At Flood Risk`)
     - `ROADS CUT OFF`: **`39.9 km`** (`Flooded & Impassable`)
     - `POWER GRID`: **`6 Substations`** (`Blackout Risk`)
- **Spoken Script (Word-for-Word)**:
  > *"Under disaster pressure, duty officers need instant clarity without black-box ambiguity.  
  > In Tab 1, our geospatial viewport renders five operational map layers—intersecting coastal bathtub surge with OpenStreetMap lifelines over NASA SRTM 30-meter terrain.  
  > On the right, our **District AI Inspector** evaluates South 24 Parganas—home to 81.6 lakh citizens—at a critical **84.0 out of 100**, pinpointing four of eight hospitals at flood risk, six of eighteen shelters inundated, 39.9 kilometers of district roads cut off, and six electrical substations facing blackout risk."*

---

### 🎬 ACT 4: Tab 1 Audio Console & Tab 2 — Voice Alerts & CAP v1.2 Export (1:42 – 2:18)
- **Deck Slide**: Slide 5 (*Voice-First Regional Alerts*) & Slide 9 (*Target Users & NDRF Relay*)
- **Exact Screen Action on `app.py`**:
  1. Look at the bottom half of the right column in Tab 1: **`📢 Official Disaster Voice Broadcast Alert`** with 3 language sub-tabs (`🇬🇧 English`, `🇮🇳 Hindi (हिंदी)`, `🏛️ Bengali (বাংলা)`).
  2. Click the `🏛️ Bengali (বাংলা)` sub-tab and click Play on the embedded `<audio>` player (or click `🔊 Synthesize Voice`), playing 4 seconds of authentic emergency radio broadcast:  
     *(Sound: "ঘূর্ণিঝড় রিমাল সুন্দরবন উপকূলে আছড়ে পড়তে চলেছে...")*
  3. Now click **Tab 2: `📢 2. Voice Alerts & Broadcast Hub`** in the main tab bar.
  4. Point to the left column (`📱 Copy-Ready Multi-Channel Emergency Broadcasts`):
     - `1. Emergency SMS (160 Characters Max)`
     - `2. WhatsApp Emergency Message (Formatted)`
     - `3. Community Radio / Public Address Announcement`
  5. Point to the right column (`🏛️ Machine-Readable Emergency Alert File (International CAP Standard)`):
     - Show the XML preview block and hover over the download button: **`📥 Download CAP 1.2 XML Alert for South 24 Parganas`**.
- **Spoken Script (Word-for-Word)**:
  > *"When cyclones make landfall, power grids fail and cellular towers go dark. Battery radios and community sirens become the only life-saving communication channels.  
  > CycloneShield is voice-first and multilingual. Right inside the District Inspector, officers can stream spoken emergency radio bulletins across seven Indian languages. Listen to our live voice broadcast in Bengali:*  
  > 
  > `[Authentic Bengali Audio Plays 4 Seconds: "ঘূর্ণিঝড় রিমাল সুন্দরবন উপকূলে আছড়ে পড়তে চলেছে..."]`  
  > 
  > *Switching to Tab 2—our Voice Alerts and Broadcast Hub—commanders get copy-ready 160-character SMS, WhatsApp, and public address scripts, alongside a one-click **OASIS Common Alerting Protocol CAP version 1.2 XML** export that feeds directly into India's national NDMA SACHET alert gateway."*

---

### 🎬 ACT 5: Tab 3 — Google Gemini Multimodal Ground Damage Photo Triage (2:18 – 2:52)
- **Deck Slide**: Slide 5 (*Ground Damage AI Triage — Gemini Multimodal Vision*)
- **Exact Screen Action on `app.py`**:
  1. Click **Tab 3: `📸 3. Ground Damage Photo Triage`**.
  2. Point to the header `📸 Field Ground Damage AI Photo Triage` and the top-right status badge (`⚡ Gemini Vision API Connected` / `🛡️ Zero-Key Calibrated Vision Mode`).
  3. Show the two top controls:
     - Left radio: `Select Disaster Photo Source:` (`Benchmark Field Incident Scenes (4 Scenarios)` vs. `Upload Custom Field Photo (JPEG / PNG)`)
     - Right dropdown: `Gemini Vision Model:` (`gemini-3.1-flash-lite`, `gemini-3.7-flash`, `gemini-3.5-flash`)
  4. In `Choose Benchmark Field Scene:`, keep `Flooded Highway: Arterial Highway Flooded (NH-117)` selected and click the primary button: **`🔍 Run Gemini Damage Triage`**.
  5. Point to the left evidence photo (`📸 Field Incident Evidence Photo`) and the right telemetry panel:
     - Incident Header Card: `Severe Highway Inundation & Embankment Washout`, `● LEVEL 4 / 5` (or `5 / 5`), `Threat: CRITICAL`
     - **4 Key Emergency Indicator Cards**: `Water Level` (`1.2 m`), `Road Access` (`IMPASSABLE — Flooded`), `Response Window` (`< 2 Hours`), `AI Confidence` (`94%`)
     - `🔍 What Gemini Vision Detected:` bullet list
     - `🚨 RECOMMENDED NDRF TACTICAL ACTION:` red box + `📦` equipment pills (`📦 High-Capacity Dewatering Pumps`, `📦 Inflatable Motor Boats`) + `📄 View Machine-Parsable JSON (Collapsed)`.
- **Spoken Script (Word-for-Word)**:
  > *"Post-landfall, emergency response pivots to field reconnaissance. In Tab 3, we deploy **Google Gemini Multimodal Vision** for ground damage photo triage.  
  > NDRF drone operators and citizens can upload field photos or evaluate benchmark incident scenes. Analyzing this flooded arterial corridor on National Highway 117, Gemini detects standing floodwaters, estimates water level at 1.2 meters, flags road access as impassable with a sub-two-hour response window, and recommends immediate NDRF deployment of high-capacity dewatering pumps and inflatable motor boats—complete with machine-parsable JSON telemetry."*

---

### 🎬 ACT 6: Tab 4 & Tab 5 — District Risk Matrix & What-If Landfall Simulator (2:52 – 3:24)
- **Deck Slide**: Slide 7 (*Predictive Lifeline ML & Vertex AI Architecture*)
- **Exact Screen Action on `app.py`**:
  1. Click **Tab 4: `📊 4. Multi-District Risk Matrix`**.
  2. Show the heading `📊 West Bengal Coastal District Vulnerability & Impact Matrix` and the interactive table with columns: `Rank`, `District`, `Population`, `Risk Score (0-100)`, `Threat Level`, `Evac Priority`, `Flooded Hosp`, `Flooded Shelters`, `Cutoff Road (km)`, and `Action Directive`.
  3. Hover over the button: **`📥 Download West Bengal Risk Matrix CSV`**.
  4. Click **Tab 5: `🌪️ 5. What-If Landfall Simulator`**.
  5. In the left column (`🎛️ Meteorological Scenario Sliders`), point to the two preset buttons—**`🌊 Spring Tide (+1.5m)`** and **`🌀 Super Cyclone (+2.5m)`**—and click **`🌊 Spring Tide (+1.5m)`**.
  6. Show the 3 sliders below them: `🌊 Surge Shift (metres)`, `💨 Wind Speed Shift (knots)`, and `🌧️ 48-hour Rainfall Shift (mm)`.
  7. Point to the right column (`📊 Predicted Lifeline Failures Under Your Scenario`), showing the table (`District`, `Surge (m)`, `Road Blocked %`, `Road Status`, `Hospital Flooded %`, `Hospital Status`, `Recommended Action`) updating in sub-5 milliseconds.
- **Spoken Script (Word-for-Word)**:
  > *"In Tab 4, our Multi-District Risk Matrix ranks all coastal districts by Census population exposure and lifeline impact, with one-click CSV export for state control rooms.  
  > In Tab 5, our What-If Landfall Simulator enables proactive scenario planning.  
  > Duty officers can click the **Spring Tide +1.5-meter** or **Super Cyclone +2.5-meter** presets, or drag the surge, wind, and 48-hour rainfall sliders. In sub-5 milliseconds, our calibrated Scikit-Learn HistGradientBoosting model—achieving a 0.941 ROC-AUC—recalculates road-blockage and hospital-flooding probabilities across every coastal district."*

---

### 🎬 ACT 7: Tab 6 — Architecture, Evaluator Audit & State Pilot Footer (3:24 – 3:45)
- **Deck Slide**: Slide 8 (*BigQuery NOAA Pipeline & FinOps*), Slide 10 (*4-Week State Pilot*), & Slide 12 (*Call to Action*)
- **Exact Screen Action on `app.py`**:
  1. Click **Tab 6: `🛰️ 6. Technical Architecture & Evaluator Audit`**.
  2. Click through the 4 audit sub-tabs:
     - `🔬 ML Model Benchmark & ROC-AUC Curves` (Shows Accuracy Leaderboard dataframe and 4-panel evaluation chart)
     - `☁️ Vertex AI-Ready Model Registry` (Shows `vertex_ai_model_manifest.json` blueprint)
     - `🛰️ BigQuery NOAA Ingestion & SQL Query` (Shows SQL query targeting `bigquery-public-data.noaa_historic_severe_storms`)
     - `🐳 Google Cloud Run Container Spec` (Shows the production `Dockerfile`)
  3. Scroll down to the two footer cards visible at the bottom of the page:
     - Left card: **`🛡️ DATA PROVENANCE & TRANSPARENCY NOTICE`** (`Real Data`, `Screening Model`, `Simulated Data` badges)
     - Right card: **`🏛️ PILOT IN YOUR STATE (4-STEP SDMA ROLLOUT)`**
  4. Scroll smoothly back to the top `🚨 SITUATION AT A GLANCE` card to conclude.
- **Spoken Script (Word-for-Word)**:
  > *"Finally, Tab 6 provides complete evaluator audit transparency—displaying our ROC-AUC benchmark curves, Google Vertex AI Model Registry manifest, BigQuery NOAA SQL queries costing a fraction of a cent, and our scale-to-zero Cloud Run Dockerfile.  
  > Backed by transparent data provenance and a four-step State Disaster Management rollout plan, CycloneShield transforms meteorological forecasts into saved Indian lives. Thank you."*

---

## 🛠️ Video Production & Delivery Verification

Both production-ready video files are generated, synchronized, and pre-packaged in the repository root:
- 📁 **Master MP4 Video (H.264 / AAC)**: [`CycloneShield_Demo_Walkthrough.mp4`](./CycloneShield_Demo_Walkthrough.mp4)
- 📁 **Master WebM Video (VP8/9 / Opus)**: [`cycloneshield_demo_walkthrough.webm`](./cycloneshield_demo_walkthrough.webm)
- 📁 **Master Audio Narration Track (MP3)**: [`cycloneshield_demo_voiceover.mp3`](./cycloneshield_demo_voiceover.mp3)
