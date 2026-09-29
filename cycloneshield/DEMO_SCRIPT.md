# 🎬 CycloneShield — Official Hackathon Video Walkthrough Demo Script
> **Target Event**: Google DevFest / Google AI Hackathon  
> **Format**: 3 to 5 Minute Working End-to-End Walkthrough Video (Target Runtime: ~3:45 to 4:15)  
> **Speaker Role**: Lead Solutions Architect & Disaster AI Specialist  
> **Target Audience**: Google DevFest Judges, Disaster Response Authorities, Technical Evaluators  
> **Repository**: [https://github.com/itsme-sherlock/CycloneShield](https://github.com/itsme-sherlock/CycloneShield)  
> **Interactive Colab**: [Open in Google Colab](https://colab.research.google.com/github/itsme-sherlock/CycloneShield/blob/main/CycloneShield_Colab.ipynb)  

---

## ⏱️ Video Structure & Timing Overview (3–5 Minutes)

| Timestamp | Segment Title | Visual Display | Focus Rubric |
| :---: | :--- | :--- | :--- |
| **0:00 – 0:35** | The Hook & India's Last-Mile Gap | Speaker + Title Slide / Satellite Image | Problem Statement & Societal Need (20%) |
| **0:35 – 1:15** | Geospatial Engine & Dual View Mode | Dashboard Header, Dual Mode Switcher & Tab 1 Map | UI Polish & Geospatial GEE (20%) |
| **1:15 – 1:55** | Explainable AI & Trilingual Voice Audio | District Scorecard, XAI Factors & Bengali Audio Player | Gemini 2.5 Flash & Cloud TTS (25%) |
| **1:55 – 2:35** | Gemini Multimodal Drone Damage Triage | Tab 2: Ground Damage Scenes, Flood Depth & Pumps | Gemini Multimodal Vision (25%) |
| **2:35 – 3:15** | Predictive Lifeline ML & Vertex AI | Tab 3: Landfall Scenario Sliders & ROC Curves | Calibrated Scikit-Learn & Vertex AI (25%) |
| **3:15 – 3:55** | BigQuery NOAA Public Pipeline & FinOps | Tab 4: NOAA Track Explorer & Dry-Run Estimator | Google BigQuery & Free Tier (25%) |
| **3:55 – 4:25** | Built for India & 1-Click Colab CTA | Tab 5: All-District Matrix, Colab Badge & Cloud Run | National Reach (20%) & Deployability (20%) |

---

## 🎙️ Word-for-Word Walkthrough Script

### 🎬 ACT 1: The Hook, India's Coastline & The "Last-Mile Gap" (0:00 – 0:35)

**[VISUAL CUE]**:  
*Start with camera on speaker or split-screen showing a satellite image of Cyclone Remal spinning over the Bay of Bengal, transitioning to the CycloneShield title screen.*

**[SPOKEN DIALOGUE]**:  
> *"Hello, judges! India has over 7,500 kilometers of coastline and 250 million citizens living in the direct path of tropical cyclones. The Bay of Bengal historically accounts for 80% of global cyclone-related deaths.  
> 
> Today, meteorological agencies like the IMD can predict storm trajectories with remarkable accuracy. But when district magistrates and the National Disaster Response Force (NDRF) prepare for landfall, they face the classic **'Last-Mile Disaster Gap'**: they don't know which state highways will be cut off by storm surge, which rural hospitals will lose power, or how to alert fishing communities once cell towers collapse.  
> 
> This is **CycloneShield**—an end-to-end Track-Based Cyclone Impact & Infrastructure Forecaster built for India and powered 100% by Google Cloud's free tier ecosystem."*

---

### 🎬 ACT 2: Interactive Command Center & Dual View Mode (0:35 – 1:15)

**[VISUAL CUE]**:  
*Screen switch to the live Streamlit Command Center at `http://localhost:8501`. Highlight the new **Dual View Mode Switcher** at the top. Point to the **3-Step Quick Guide**. Then inspect **Tab 1: 🗺️ Multi-Hazard Command & Voice Alerts** showing the interactive Folium map centered on the Bengal delta.*

**[SPOKEN DIALOGUE]**:  
> *"Here is CycloneShield running live on localhost. To prevent cognitive overload, we designed a **Dual View Mode**: emergency coordinators get an intuitive, human-first **Disaster Operations Command**, while technical evaluators can toggle to **Hackathon Evaluator Mode** to audit underlying ROC curves, BigQuery queries, and Docker manifests.  
> 
> In Tab 1, rather than relying on crude static radius circles, our spatial engine projects **dynamic multi-tier wind swaths** directly onto UTM 45N: core hurricane winds in red, gale winds in amber, and squalls in blue.  
> 
> Next, using our empirical central pressure deficit model and **Google Earth Engine's NASA SRTM 30-meter Digital Elevation Model**, CycloneShield calculates a peak storm surge of **3.56 meters**—instantly generating a high-precision coastal bathtub flood zone. Intersecting this with OpenStreetMap lifelines pinpoints **39.6 kilometers of cut-off state highways** and **5 flooded hospitals** up to 48 hours before landfall."*

---

### 🎬 ACT 3: Explainable AI & Trilingual Voice Broadcasts (1:15 – 1:55)

**[VISUAL CUE]**:  
*In the right column of Tab 1, select **South 24 Parganas**. Point out the **Explainable AI (XAI)** factor breakdown (Health 35%, Shelters 25%, Roads 25%, Grid 15%). Switch to the **📢 Broadcast Advisories** tab and click the **▶️ Play** button on the Bengali audio player (`remal_south_24_parganas_bn.mp3`).*

**[SPOKEN DIALOGUE]**:  
> *"Instead of an untrustworthy 'black-box' score, CycloneShield provides an **Explainable AI Risk Index** from 0 to 100, showing district magistrates the exact contribution of clinic density, road cutoffs, wind, and storm surge. Here, South 24 Parganas ranks at a critical 88.4 out of 100.  
> 
> In the sidebar, **Google Gemini 2.5 Flash** ingests this spatial telemetry to generate structured emergency advisories in **English**, **Hindi**, and **Bengali**, alongside simulated **NDRF Battalion Tactical Dispatch Orders**.  
> 
> But when coastal power fails and cellular towers go dark, emergency battery radios are the only lifeline. Listen to our **Voice-First Audio Engine** broadcasting the localized Bengali emergency alert synthesized directly from Gemini's output:*  
> 
> `[Audio clip plays 3-4 seconds of authentic Bengali emergency broadcast: "ঘূর্ণিঝড় রিমাল সুন্দরবন উপকূলে আছড়ে পড়তে চলেছে..."]`  
> 
> *"Every single district alert is pre-synthesized and ready for zero-latency radio relay."*

---

### 🎬 ACT 4: Gemini Multimodal Drone & Field Damage Triage (1:55 – 2:35)

**[VISUAL CUE]**:  
*Click to switch to **Tab 2: 📸 Ground Damage AI Triage (Gemini Vision)**. Select the first benchmark scene: **NH-117 Arterial Highway Submersion**. Show the extracted visual observations, estimated water depth pill, and tactical action directive.*

**[SPOKEN DIALOGUE]**:  
> *"As the storm makes landfall, field reconnaissance begins. In Tab 2, our **Gemini Multimodal Vision Engine** triages ground-truth disaster photographs captured by citizens and NDRF drone teams.  
> 
> Let's inspect this flooded highway scene. Gemini 2.5 Flash analyzes the image, detects deep floodwaters, estimates the water depth at **1.2 meters**, classifies it as **Threat Tier: CRITICAL (Severity 5/5)**, and issues an immediate tactical recovery order: deploying high-capacity submersible dewatering pumps and establishing an alternate emergency evacuation corridor along NH-12.  
> 
> It even detects non-hazard baseline photos, ensuring relief battalions aren't dispatched to false alarms."*

---

### 🎬 ACT 5: Predictive Lifeline ML Simulator & Vertex AI (2:35 – 3:15)

**[VISUAL CUE]**:  
*Click to switch to **Tab 4: 🤖 Predictive Lifeline ML Simulator**. Slide the **Storm Surge Shift** slider from `0.0m` to `+1.5m` (Spring Tide Surge) and show the failure probability table update dynamically. Then expand the **🔬 View Model Benchmark Metrics & Vertex AI Specification** expander to show the ROC-AUC curves and Vertex manifest.*

**[SPOKEN DIALOGUE]**:  
> *"In Tab 4, we move from reactive assessment to proactive simulation. We trained a calibrated machine learning pipeline using **Scikit-Learn CalibratedClassifierCV** on over 3,500 historical storm observations.  
> 
> With an **ROC-AUC of 0.941** on highway cutoffs and **0.938** on hospital inundation, disaster commanders can adjust sliders—simulating a spring tide surge amplification of +1.5 meters or sudden eye intensification—to get calibrated, real-time lifeline cut-off probabilities in sub-5 milliseconds.  
> 
> Under the hood, this model is 100% packaged for **Google Cloud Vertex AI Model Registry** with standard sklearn container deployment specs."*

---

### 🎬 ACT 6: BigQuery NOAA Pipeline & FinOps Free Tier Audit (3:15 – 3:55)

**[VISUAL CUE]**:  
*Click to switch to **Tab 5: 🛰️ Cloud Architecture & BigQuery**. Click **Estimate BigQuery Cost** to show the dry-run cost box ($0.0002 / Free Tier Eligible). Select **AMPHAN (2020)** in the storm dropdown and show the historic synoptic intensity line chart.*

**[SPOKEN DIALOGUE]**:  
> *"In Tab 5, CycloneShield connects directly to **Google Cloud BigQuery**, querying `bigquery-public-data.noaa_hurricanes.ibtracs_all` with built-in FinOps dry-run cost controls—scanning 40 megabytes at a cost of just $0.0002, 100% covered by GCP's 1 Terabyte monthly free tier.  
> 
> Disaster commanders can load any historical Bay of Bengal super cyclone—from Super Cyclone Amphan to Fani or Dana—to evaluate historical analogues and calibrate relief operations.  
> 
> Our FinOps audit confirms that the entire platform—from BigQuery queries and Gemini API calls to Cloud Run container hosting—operates at **exactly $0.00 recurring cloud expense**."*

---

### 🎬 ACT 7: Built for India, Cloud Run & 1-Click Colab Call to Action (3:55 – 4:25)

**[VISUAL CUE]**:  
*Quick screen split: Left side showing the `CycloneShield_Colab.ipynb` notebook with the "Open in Colab" badge; Right side showing `deploy_cloud_run.sh` terminal and the GitHub repository.*

**[SPOKEN DIALOGUE]**:  
> *"CycloneShield is built for all of India. While validated on Cyclone Remal in West Bengal, the system is architected to scale instantly across all **9 coastal states**—from Odisha and Andhra Pradesh to Gujarat and Maharashtra—and supports regional languages from Bengali to Hindi, Odia, and Telugu.  
> 
> It is containerized for **Google Cloud Run** with a hardened, multi-stage Dockerfile and automated Cloud Build CI/CD pipelines.  
> 
> And best of all, anyone can test CycloneShield right now: click the **'Open in Colab'** badge in our GitHub repository to execute the entire 12-section pipeline end-to-end with a single click—no API key or GCP credentials required.  
> 
> CycloneShield transforms meteorological predictions into saving Indian lives. Thank you!"*

---

## 🛠️ Recording & Production Checklist

1. **Local Setup Verification**:
   - Ensure Streamlit is running: `http://localhost:8501`
   - Test audio playback in browser: verify your system audio output is captured by OBS / screen recorder.
   - Browser zoom set to 100% or 110% for crisp text readability on 1080p / 4K.
2. **Audio Levels**:
   - Mic: -6 dB to -12 dB (clear, crisp voice, no echo).
   - Desktop Audio (for Bengali broadcast clip): -15 dB (audible without clipping).
3. **Pacing & Energy**:
   - Speak with energetic, clear, professional articulation.
   - Pace yourself comfortably across the 7 acts to stay within **3:45 to 4:15**.
4. **Colab Test**:
   - Have `CycloneShield_Colab.ipynb` open in a separate Chrome tab so you can switch instantly without loading delay.
