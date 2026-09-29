# 🎬 CycloneShield — Official 2–3 Minute Demo Video Recording & Voiceover Guide

> **Live Production Website**: [https://cycloneshield-vawrqbhtbgu8i6cafhbf3q.streamlit.app](https://cycloneshield-vawrqbhtbgu8i6cafhbf3q.streamlit.app)  
> **Local Backup Mirror**: `http://localhost:8501`  
> **Target Video Runtime**: **2 Minutes 30 Seconds** (Strictly within the 2:00 – 3:00 minute hackathon requirement)  
> **Total Word Count**: **358 Words** (~140 words/min presentation pace + 15s visual & audio pauses)  
> **Pitch Deck Alignment**: 100% mapped to the 12 slides in [`PITCH_DECK.md`](file:///c:/Users/LENOVO/devfest/PITCH_DECK.md)  
> **Pre-Generated Audio Voiceover**: [`cycloneshield_2min_demo_voiceover.mp3`](file:///c:/Users/LENOVO/devfest/cycloneshield_2min_demo_voiceover.mp3) (Ready to use in the project root)

---

## 🧭 Executive Video Architecture (Deck to Screen Mapping)

| Timestamp | Act Title | Pitch Deck Slide | Live Website Action (`streamlit.app`) | Google Tech Highlight |
| :---: | :--- | :---: | :--- | :--- |
| **0:00 – 0:25** | **The Hook & Last-Mile Gap** | Slides 1 & 2 | Landing View, Hero Title & Top KPI Ribbon | Google Material 3 UI & Cloud Run |
| **0:25 – 0:50** | **Geospatial Surge & Hazard Intersect** | Slides 3 & 4 | Tab 1: Folium Map, Wind Swaths & Inundation | Google Earth Engine (SRTM 30m DEM) |
| **0:50 – 1:20** | **Explainable AI & Trilingual Voice** | Slides 3 & 6 | Tab 1: South 24 Parganas, XAI Chart & Play Audio | Gemini 2.5 Flash & Google Cloud TTS |
| **1:20 – 1:45** | **Gemini Multimodal Damage Triage** | Slide 5 | Tab 2: Flooded Highway Scene, Water Depth & Pumps | Gemini Multimodal Vision (Flash) |
| **1:45 – 2:10** | **Predictive Lifeline ML Simulator** | Slide 7 | Tab 4: Surge Shift Slider (`+1.5m`) & Vertex Specs | Scikit-Learn Calibrated & Vertex AI |
| **2:10 – 2:30** | **BigQuery NOAA FinOps & Call to Action**| Slides 8, 10, 12 | Tab 5: BigQuery Cost Estimator ($0.0002) & Colab Badge | BigQuery Public Data & 100% Free Tier |

---

## 🎙️ Master Second-by-Second Storyboard & Teleprompter Script

### 🎬 ACT 1: The Hook & India's Last-Mile Gap (0:00 – 0:25)
- **Deck Slide**: Slide 1 (*Vision & Executive Summary*) & Slide 2 (*The Problem: India's 7,516 km Coastline*)
- **Visual Action on Screen**:
  1. Open [cycloneshield-vawrqbhtbgu8i6cafhbf3q.streamlit.app](https://cycloneshield-vawrqbhtbgu8i6cafhbf3q.streamlit.app) in 1080p full-screen browser.
  2. Cursor gently hovers across the top hero title: **CycloneShield | AI Disaster Command Center**.
  3. Mouse moves across the **6 KPI cards** in the ribbon: highlighting **Sustained Wind (60 kts)**, **Peak Storm Surge (3.56m)**, and **Cut-Off Highways (39.6 km)**.
- **Spoken Script (Word-for-Word)**:
  > *"Every year, severe cyclones strike India's 7,500-kilometer coastline, threatening over 250 million citizens. While modern meteorology tracks storms accurately, disaster commanders face a fatal **Last-Mile Gap**: they do not know which state highways will drown, which rural hospitals will lose power, or how to alert delta fishermen once cell towers collapse.  
  > 
  > This is **CycloneShield**—an end-to-end disaster impact and infrastructure vulnerability forecaster powered 100% by Google Cloud's free tier."*

---

### 🎬 ACT 2: Interactive Geospatial Hazard & Lifeline Intersect (0:25 – 0:50)
- **Deck Slide**: Slide 3 (*Track-Based Multi-Hazard Spatial Engine*) & Slide 4 (*Google AI Ecosystem*)
- **Visual Action on Screen**:
  1. Under **Tab 1: 🗺️ 1. Multi-Hazard Command & Voice Alerts**, look at the interactive map.
  2. Move cursor along the storm track: point to the **dynamic wind swaths** (Red Core Hurricane Swath >48 kts, Orange Gale Swath >34 kts).
  3. Zoom in slightly (+1 scroll wheel) over the Sundarbans coastal edge: point to the **blue coastal storm surge bathtub flood zone**.
  4. Hover over the red medical cross icons (submerged clinics) and orange severed highway lines (State Highway SH-3).
- **Spoken Script (Word-for-Word)**:
  > *"Here on our live command center, rather than static circles, CycloneShield projects **dynamic multi-tier wind swaths** along the storm track.  
  > 
  > By integrating central pressure deficit with **Google Earth Engine's 30-meter NASA SRTM elevation data**, we simulate a peak coastal storm surge of **3.56 meters**.  
  > 
  > Intersecting this flood zone with OpenStreetMap lifelines pinpoints **39.6 kilometers of submerged highways** and flooded health centers up to 48 hours before landfall."*

---

### 🎬 ACT 3: Explainable AI & Trilingual Emergency Radio Alerts (0:50 – 1:20)
- **Deck Slide**: Slide 3 (*Explainable AI Formula*) & Slide 6 (*Voice-First Trilingual Radio Engine*)
- **Visual Action on Screen**:
  1. On the right-side panel of Tab 1, click the **Select Target District** dropdown and select **South 24 Parganas**.
  2. Point cursor to the **Explainable AI (XAI)** factor breakdown bar chart (showing exact drivers: Wind 35%, Surge 25%, Roads 25%, Grid 15% -> Vulnerability Score **88.4 / 100**).
  3. Click the **📢 Broadcast Advisories** tab right below the chart.
  4. Select the **Bengali (বাংলা)** language tab.
  5. Click **▶️ Play** on the embedded audio player (`remal_south_24_parganas_bn.mp3`).
  6. **PAUSE 4 SECONDS** and let the authentic regional emergency radio broadcast play clearly out loud:
     *(Sound: "ঘূর্ণিঝড় রিমাল সুন্দরবন উপকূলে আছড়ে পড়তে চলেছে...")*
- **Spoken Script (Word-for-Word)**:
  > *"Zero black-box ambiguity: our **Explainable AI score** shows commanders exactly why South 24 Parganas reaches a critical 88.4 risk index.  
  > 
  > In real-time, **Google Gemini 2.5 Flash** synthesizes targeted emergency advisories in English, Hindi, and Bengali. When coastal power grids fail and cellular towers go dark, our **Cloud TTS Voice Engine** broadcasts life-saving radio alerts directly to local fishermen:*  
  > 
  > `[Pause 4 seconds for Bengali Audio Playback]`  
  > 
  > *Every district alert is pre-synthesized for instant zero-latency broadcast."*

---

### 🎬 ACT 4: Gemini Multimodal Drone Damage Triage (1:20 – 1:45)
- **Deck Slide**: Slide 5 (*Ground Damage AI Triage — Gemini Multimodal Vision*)
- **Visual Action on Screen**:
  1. Click to switch to **Tab 2: 📸 2. Ground Damage AI Triage (Gemini Vision)**.
  2. In the benchmark scenes selector, click the first card: **NH-117 Arterial Highway Submersion**.
  3. The image of the flooded road appears with immediate AI Telemetry below it.
  4. Hover mouse over:
     - Badge: **Estimated Water Depth: 1.2 m**
     - Badge: **Threat Tier: CRITICAL (Severity 5/5)**
     - Box: **Tactical Action Directives**: point cursor to *"Deploy high-capacity submersible dewatering pumps and motorized rescue rafts."*
- **Spoken Script (Word-for-Word)**:
  > *"Post-landfall, field reconnaissance begins. In Tab 2, our **Gemini Multimodal Vision Engine** triages ground-truth drone and citizen photos in real time.  
  > 
  > Analyzing this flooded highway, Gemini detects deep standing floodwaters, estimates the water depth at **1.2 meters**, flags a critical severity threat, and generates actionable NDRF directives—instructing response teams to deploy submersible dewatering pumps and reroute relief convoys."*

---

### 🎬 ACT 5: Predictive Lifeline ML Simulator & Vertex AI (1:45 – 2:10)
- **Deck Slide**: Slide 7 (*Predictive Lifeline ML & Vertex AI Architecture*)
- **Visual Action on Screen**:
  1. Click to switch to **Tab 4: 🤖 4. Predictive Lifeline ML Simulator**.
  2. Locate the slider: **Storm Surge Shift (meters)**.
  3. Drag the slider from `0.0m` to **`+1.5m`** (simulating Spring Tide Surge).
  4. Point to the Failure Probability Table updating dynamically in sub-5 milliseconds (probabilities surging into deep red >85%).
  5. Click the accordion: **🔬 View Model Benchmark Metrics & Vertex AI Specification**.
  6. Show the ROC-AUC evaluation curves (ROC 0.941) and the Vertex AI Model Registry container configuration json.
- **Spoken Script (Word-for-Word)**:
  > *"In Tab 4, we transition to predictive foresight. Trained on over 3,500 historical storm observations with a **0.94 ROC-AUC**, our calibrated machine learning model simulates what-if scenarios in under 5 milliseconds.  
  > 
  > Shifting the surge slider by plus 1.5 meters recalculates highway and hospital failure probabilities instantly. Under the hood, it is fully packaged for **Google Cloud Vertex AI**."*

---

### 🎬 ACT 6: BigQuery NOAA FinOps & Call to Action (2:10 – 2:30)
- **Deck Slide**: Slide 8 (*BigQuery NOAA Pipeline & FinOps*), Slide 10 (*1-Click Interactive Colab*), & Slide 12 (*Call to Action*)
- **Visual Action on Screen**:
  1. Click to switch to **Tab 5: 🛰️ 5. Cloud Architecture & BigQuery (Judges)**.
  2. Click the blue button: **⚡ Estimate BigQuery Query Cost (Dry Run)**.
  3. Show the green success callout: **Estimated Cost: $0.0002 / 100% Free Tier Eligible**.
  4. Point cursor to the top-right header / repository link and highlight the **Open in Google Colab** badge.
- **Spoken Script (Word-for-Word)**:
  > *"In Tab 5, CycloneShield queries NOAA’s IBTrACS public dataset on **Google BigQuery** with built-in FinOps controls, costing just two-hundredths of a cent.  
  > 
  > The entire platform runs within **Google's Free Tier**, scales across all 9 Indian coastal states, and is executable with a single click in Google Colab.  
  > 
  > CycloneShield transforms forecasts into lives saved. Thank you!"*

---

## 🛠️ Step-by-Step Recording Instructions

### Step 1: Prepare Your Browser
1. Open Google Chrome or Microsoft Edge.
2. Navigate to: `https://cycloneshield-vawrqbhtbgu8i6cafhbf3q.streamlit.app`
3. Press **F11** (Full Screen) or press **Ctrl + Shift + B** to hide bookmarks for a distraction-free view.
4. Set Zoom level to **100%** (or **90%** if on a smaller laptop display so all KPI cards fit comfortably).
5. Pre-test audio: In Tab 1, click the Bengali audio player once to verify it plays through your speakers or headphones.

### Step 2: Choose Your Recording Method

#### Option A: Quick Screen Recording via Windows Game Bar (Built-in, Zero Install)
- Press **Win + G** on Windows 11 / 10.
- Click the **Capture** widget -> Click **Record** (or press **Win + Alt + R**).
- Ensure the microphone toggle is **ON** if you are speaking live.
- Perform the actions according to the Storyboard above.
- Press **Win + Alt + R** again to finish recording. Video saves automatically to `C:\Users\LENOVO\Videos\Captures`.

#### Option B: Studio Recording via OBS Studio or Loom
- Screen Canvas: **1920x1080 (1080p, 60fps or 30fps)**.
- Sources to add:
  1. **Window Capture / Screen Capture** -> CycloneShield browser window.
  2. **Desktop Audio** -> Captures the Streamlit Bengali emergency radio playback.
  3. **Microphone (Auxiliary)** -> Your voice (if speaking live).
- Click **Start Recording**, perform the walkthrough, click **Stop Recording**.

### Step 3: Audio Voiceover Options

#### Choice 1: Speak Live Using the Teleprompter
- Place this document on a secondary monitor or your phone next to the screen.
- Read with confident, energetic, and steady pacing.

#### Choice 2: Use the Pre-Generated Studio AI Narration
- We have already generated the complete synchronized narration audio for you:  
  📁 [`c:\Users\LENOVO\devfest\cycloneshield_2min_demo_voiceover.mp3`](file:///c:/Users/LENOVO/devfest/cycloneshield_2min_demo_voiceover.mp3)
- Drop your recorded screen video (`.mp4`/`.webm`) and `cycloneshield_2min_demo_voiceover.mp3` into **Clipchamp** (free on Windows), **CapCut**, or **Canva**.
- Align the speech with the tab switches as timed in the table above.
- Export as `CycloneShield_Demo_Final_2min.mp4`.

---

## 📋 Pre-Flight Submission Checklist

- [ ] **Duration**: Video is between **2:15 and 2:45 minutes** (under 3:00 min limit).
- [ ] **Visual Clarity**: Text and map labels are crisp at 1080p.
- [ ] **Google Tech Visible**:
  - [ ] Google Earth Engine (SRTM 30m DEM) mentioned in Tab 1
  - [ ] Google Gemini 2.5 Flash advisories and Cloud TTS audio played in Tab 1
  - [ ] Gemini Multimodal Vision demonstrated in Tab 2
  - [ ] Google Cloud Vertex AI & Scikit-Learn demonstrated in Tab 4
  - [ ] Google BigQuery public data & FinOps dry-run demonstrated in Tab 5
- [ ] **National Impact**: Mentions India's 7,516 km coastline and 9 coastal states.
- [ ] **Links in Video Description / Submission Form**:
  - Live Demo App: `https://cycloneshield-vawrqbhtbgu8i6cafhbf3q.streamlit.app`
  - GitHub Repository: `https://github.com/itsme-sherlock/CycloneShield`
  - Google Colab 1-Click: `https://colab.research.google.com/github/itsme-sherlock/CycloneShield/blob/main/CycloneShield_Colab.ipynb`
