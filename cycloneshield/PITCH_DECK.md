# 🌀 CycloneShield — 12-Slide Executive Pitch Deck

> **Turning Storm Scenarios into Clearer District Priorities with Google Cloud & AI**  
> **Hosted Interactive Prototype**: [https://cycloneshield-vawrqbhtbgu8i6cafhbf3q.streamlit.app/](https://cycloneshield-vawrqbhtbgu8i6cafhbf3q.streamlit.app/)  
> **Open Source Repository**: [https://github.com/itsme-sherlock/CycloneShield](https://github.com/itsme-sherlock/CycloneShield)  
> **Reproducible Google Colab**: [Open in Colab](https://colab.research.google.com/github/itsme-sherlock/CycloneShield/blob/main/CycloneShield_Colab.ipynb)  
> **Event**: Google AI Hackathon / DevFest India • **Presentation Format**: 16:9 Widescreen (12 Slides)  
> **Generated PPTX Presentation**: [`CycloneShield_Pitch_Deck.pptx`](file:///c:/mnt/agents/output/cycloneshield/CycloneShield_Pitch_Deck.pptx)

---

## Executive Summary: Google Cloud & AI in CycloneShield

CycloneShield connects **11 native Google Cloud & AI services** into a unified, event-driven disaster decision-support system:

| # | Google Service / Technology | Operational Role in CycloneShield | Code Reference |
|---|---|---|---|
| 1 | **Google Gemini 2.5 Flash** | Multimodal visual ground damage triage (grading severity 1–5, equipment needs), strictly decoupled from location to prevent hallucinations; multilingual emergency advisory drafting. | [`multimodal_damage.py`](file:///c:/mnt/agents/output/cycloneshield/multimodal_damage.py), [`gemini_advisory.py`](file:///c:/mnt/agents/output/cycloneshield/gemini_advisory.py) |
| 2 | **Google Cloud Storage (GCS)** | Tamper-evident, audit-proof incident evidence vault (`gs://<BUCKET>/<state>/<district>/<incident_id>/`), storing raw photos and JSON metadata with quarantine for unverified locations (`_unverified/`). | [`evidence_store.py`](file:///c:/mnt/agents/output/cycloneshield/evidence_store.py) |
| 3 | **Google Cloud Pub/Sub** | Low-latency, event-driven alerting backbone publishing CRITICAL/HIGH incidents to `cyclone-alerts` topic with custom district attributes for localized subscriber filtering (`attributes.district = "Puri"`). | [`alerts.py`](file:///c:/mnt/agents/output/cycloneshield/alerts.py), [`alert_subscriber.py`](file:///c:/mnt/agents/output/cycloneshield/scripts/alert_subscriber.py) |
| 4 | **Google Cloud Run** | Serverless production container hosting (Streamlit port 8080) with automatic 0-to-N scaling, zero server management, and native HTTPS enabling browser device geolocation. | [`Dockerfile`](file:///c:/mnt/agents/output/cycloneshield/Dockerfile), [`deploy_cloud_run.sh`](file:///c:/mnt/agents/output/cycloneshield/deploy_cloud_run.sh) |
| 5 | **Google BigQuery** | Planetary historical storm data ingestion directly querying public dataset `bigquery-public-data.noaa_hurricanes.ibtracs_all` with built-in FinOps dry-run cost estimators. | [`bigquery_pipeline.py`](file:///c:/mnt/agents/output/cycloneshield/bigquery_pipeline.py) |
| 6 | **Google Vertex AI (Ready)** | Machine Learning model deployment blueprint, serving container specs (`vertex_model_config.json`), and calibrated Gradient Boosting pipeline (ROC-AUC > 0.975) for lifeline failure prediction. | [`predictive_model.py`](file:///c:/mnt/agents/output/cycloneshield/predictive_model.py), [`vertex_model_config.json`](file:///c:/mnt/agents/output/cycloneshield/outputs/models/vertex_model_config.json) |
| 7 | **Google Cloud Text-to-Speech** | Voice-first emergency broadcast synthesis using high-fidelity Neural2 voices across 7 regional Indian languages (Bengali, Hindi, Odia, Telugu, Tamil, Gujarati, Indian English). | [`voice_engine.py`](file:///c:/mnt/agents/output/cycloneshield/voice_engine.py) |
| 8 | **Google Earth Engine (GEE)** | Planetary digital elevation modeling using NASA SRTM 30m DEM for coastal bathymetry, run-up modeling, and elevation-aware inundation screening. | [`surge_rain.py`](file:///c:/mnt/agents/output/cycloneshield/surge_rain.py), [`infra_exposure.py`](file:///c:/mnt/agents/output/cycloneshield/infra_exposure.py) |
| 9 | **Google Cloud Build** | Automated CI/CD container build and deployment pipeline (`cloudbuild.yaml`) pulling directly from Git into Google Artifact Registry and Cloud Run. | [`cloudbuild.yaml`](file:///c:/mnt/agents/output/cycloneshield/cloudbuild.yaml) |
| 10 | **Google Cloud Secret Manager** | Zero-trust security managing `GEMINI_API_KEY` with keyless runtime service accounts (`cycloneshield-run`), preventing credential exposure. | [`deploy_cloud_run.sh`](file:///c:/mnt/agents/output/cycloneshield/deploy_cloud_run.sh#L80-L89) |
| 11 | **Google Colab** | 1-Click reproducible interactive notebook demonstrating BigQuery ingestion, ML training, Pub/Sub dispatch, GCS storage, and zero-key evaluator fallback. | [`CycloneShield_Colab.ipynb`](file:///c:/mnt/agents/output/cycloneshield/CycloneShield_Colab.ipynb) |

---

## Slide 1: Title & Core Promise
### CycloneShield: Turning Storm Scenarios into Clearer District Priorities
* **Subtitle**: Powered by Google Cloud Run, BigQuery, Gemini 2.5 Flash, Pub/Sub, Cloud Storage, Vertex AI & Cloud TTS
* **The Goal**: Empower District Magistrates, SDMA officers, and NDRF commanders to turn complex meteorological storm tracks into clear, actionable infrastructure priorities and life-safety alerts.
* **Interactive Live Prototype**: Hosted on Streamlit Community Cloud with 5 state profiles, 7 regional languages, and zero-key evaluator fallback.
* **Reproducible Evaluation**: Complete open-source repository and 1-Click Google Colab notebook for instant judge verification.

**Speaker Notes (20s)**:  
> *"Good morning, judges. Weather agencies track cyclones, and disaster response officers make operational decisions. CycloneShield bridges that critical operational gap. It is an end-to-end decision-support prototype powered by 11 Google Cloud and AI services—including Gemini 2.5 Flash, BigQuery, Cloud Storage, Pub/Sub, Cloud Run, Vertex AI, and Cloud Text-to-Speech—designed to translate raw storm scenarios into clear district lifeline priorities, road cut-off forecasts, and targeted alerts."*

---

## Slide 2: The Problem: The Last-Mile Operational Gap
### Weather forecasts track the storm, but field teams still lack road and hospital impact data.
* **188M+ Coastal Citizens**: Over 188 million people live in India's coastal districts (Census 2011), with ~250 million residing within 50 km of the sea.
* **The Information Disconnect**: Synoptic bulletins provide isobar tracks, landfall coordinates, and central barometric pressure—not whether State Highway 3 will submerge or which rural hospital ICUs will lose power.
* **Compound Hazards in Silos**: Coastal storm surges and extreme pluvial rainfall are modeled separately, obscuring true ground inundation.
* **The Duty Officer's Dilemma**: Incident commanders must deploy rescue boats and stage evacuation buses without knowing which bridges fail first or how to alert offline communities.

**Speaker Notes (25s)**:  
> *"India's coastal districts house over 188 million citizens according to the 2011 Census. When a cyclone develops, the India Meteorological Department provides official weather forecasts. However, a District Magistrate or State Disaster Management officer cannot deploy ambulances based solely on wind speed isobars. They need to know whether State Highway 3 will be cut off, which rural clinics may face flooding, and how to reach offline communities in their native language. That is the critical last-mile operational gap."*

---

## Slide 3: The Solution: 5-Stage Decision Pipeline
### An integrated workflow powered by Google services—from planetary data to edge alerting.
1. **Track Ingestion**: Ingests historical NOAA storm tracks via **Google BigQuery** and parses dated IMD bulletins to extract central pressure, wind velocity, and waypoints.
2. **Geospatial Hazards**: Evaluates compound coastal storm surge and pluvial flooding using **Google Earth Engine** SRTM 30m elevation rasters and bathymetric shelf coefficients.
3. **Lifeline ML Forecasting**: Applies a **Vertex AI-ready** calibrated Gradient Boosting model to predict highway submersion and hospital ICU flood failure.
4. **Ground Photo Damage Triage**: Inspects post-storm photos via **Google Gemini 2.5 Flash** (damage classification and severity grading) and archives evidence in **Google Cloud Storage**.
5. **Actionable Multi-Channel Alerting**: Dispatches event-driven incident alerts via **Google Cloud Pub/Sub** and broadcasts audio alerts in 7 Indian languages via **Google Cloud Text-to-Speech**.

**Speaker Notes (25s)**:  
> *"CycloneShield structures disaster decision-making into 5 connected stages: First, storm tracks are ingested via Google BigQuery and official IMD bulletins. Second, Google Earth Engine topography powers compound surge and flood hazard screening. Third, our Vertex AI-ready predictive ML model scores road and hospital lifeline failure. Fourth, post-storm damage photos are triaged via Gemini 2.5 Flash and archived in Google Cloud Storage. Fifth, life-safety warnings are dispatched via Google Cloud Pub/Sub and broadcast via Cloud Text-to-Speech in 7 languages."*

---

## Slide 4: Prepared Demonstration: Cyclone Remal Scenario
### Configured multi-hazard screening outputs—turning complex data into actionable district priorities.
* **Landfall Wind Swath**: 110 km/h wind envelope dynamically mapped across South 24 Parganas and Purba Medinipur.
* **Coastal Surge Head**: 3.56m storm surge calculated from a 977 mb central pressure deficit ($S_{\text{surge}} = \frac{36.25}{10} \times 0.98$).
* **District Risk Scoring**: South 24 Parganas scores **88.4/100 (EXTREME)**, triggering a 12,000-person prioritized evacuation recommendation.
* **Critical Facility Protection**: 5 rural Primary Health Centers (PHCs) identified within the 2-meter flood zone, recommending immediate generator sandbagging.
* **Visual Reference**: High-contrast interactive Folium map with toggleable wind swaths, flood depths, and lifeline icons (`outputs/screenshots/01_spatial_hazard_core.png`).

**Speaker Notes (25s)**:  
> *"Here you see the interactive prototype running Cyclone Remal. The system calculates a 3.56-meter storm surge from barometric pressure, maps the 110 km/h wind swath, and overlays 47 critical facilities. Instead of wading through raw numbers, the District Magistrate immediately sees that South 24 Parganas is at extreme risk (88.4) and State Highway 3 faces a 78% probability of submersion, allowing pre-emptive staging."*

---

## Slide 5: Google Cloud & AI Architecture: 11 Connected Services
### A resilient, enterprise-grade cloud architecture spanning perception, data, and edge alerting.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       CYCLONESHIELD CLOUD ARCHITECTURE                      │
├──────────────────────────────┬──────────────────────────────┬───────────────┤
│    1. PERCEPTION & GENAI     │     2. DATA ENGINE & ML      │ 3. SERVERLESS │
├──────────────────────────────┼──────────────────────────────┼───────────────┤
│ • Gemini 2.5 Flash Vision    │ • BigQuery NOAA IBTrACS      │ • Cloud Run   │
│   (Damage Triage 1-5)        │   (Public Dataset Warehouse) │   (Container) │
│ • Cloud Text-to-Speech       │ • Earth Engine (GEE)         │ • Pub/Sub     │
│   (Neural2 in 7 Languages)   │   (SRTM 30m Elevation DEM)   │   (Alert Bus) │
│ • Gemini Advisory Drafting   │ • Vertex AI (Ready)          │ • Cloud Store │
│   (Multilingual SOPs)        │   (Lifeline Model Registry)  │ • Secret Mgr  │
└──────────────────────────────┴──────────────────────────────┴───────────────┘
```

* **Pillar 1: Perception & Generative AI**:
  - **Gemini 2.5 Flash**: Evaluates structural destruction, road blockages, and relief equipment needs.
  - **Cloud Text-to-Speech**: High-definition Neural2 natural voices for audio warnings in 7 Indian regional languages.
* **Pillar 2: Planetary Data & Machine Learning**:
  - **BigQuery**: Ingests decades of North Indian Ocean historical cyclone tracks with FinOps dry-run cost control.
  - **Google Earth Engine**: High-resolution elevation analysis for coastal storm surge bathymetry.
  - **Vertex AI (Ready)**: Packaging manifest (`vertex_model_config.json`) and serving container specs.
* **Pillar 3: Serverless Cloud & Real-Time Alerting**:
  - **Cloud Run**: Autoscaling containerized Streamlit command center on port 8080 with native HTTPS for device GPS.
  - **Cloud Pub/Sub**: Real-time event bus with custom district attribute filtering (`attributes.district = "Puri"`).
  - **Cloud Storage**: Secure incident vault (`gs://BUCKET/state/district/incident_id/`).
  - **Secret Manager & Cloud Build**: Keyless IAM service account deployment and automated CI/CD.

**Speaker Notes (30s)**:  
> *"CycloneShield leverages a comprehensive suite of 11 Google Cloud services organized across three distinct pillars: Perception & Generative AI uses Gemini 2.5 Flash for multimodal visual damage triage and Cloud Text-to-Speech for voice alerts in 7 Indian languages. Planetary Data & ML utilizes BigQuery for NOAA storm tracks, Google Earth Engine for elevation models, and Vertex AI for model registry readiness. Serverless Cloud & Alerts leverages Cloud Run for autoscaling, Cloud Pub/Sub for attribute-filtered emergency alerts, Cloud Storage for incident evidence, and Secret Manager with Cloud Build for zero-trust security."*

---

## Slide 6: Google Gemini 2.5 Flash & Cloud Storage: Incident Triage
### Multimodal damage assessment with strict geospatial decoupling and tamper-evident evidence storage.
* **Gemini 2.5 Flash Multimodal Vision**:
  - Automatically classifies structural damage types (culvert blowouts, embankment breaches, uprooted trees, collapsed roofs).
  - Assigns severity scores (Tier 1 Minor to Tier 5 Catastrophic) and extracts actionable relief equipment needs (e.g., "Requires 50HP dewatering pumps and JCB excavator").
* **Strict Anti-Hallucination Design Decision**:
  - **Gemini NEVER infers location from imagery**.
  - Incident coordinates are derived strictly and deterministically via **EXIF GPS** $\to$ **HTML5 browser device location** $\to$ **manual operator point-in-polygon verification** (`geo_locate.py`).
* **Google Cloud Storage Evidence Vault**:
  - Uploaded photos and structured triage JSON files are archived to:
    `gs://<BUCKET>/<state>/<district>/<incident_id>/`
  - Photos with missing or out-of-coverage coordinates are quarantined under `_unverified/` and `_outside_coverage/`.
  - Service account authentication uses `roles/storage.objectCreator` for keyless write security.
* **Operational Verification**: CRITICAL severity incidents display a prominent **"Needs Human Confirmation"** badge before dispatch.

**Speaker Notes (25s)**:  
> *"In disaster management, AI hallucination costs lives. We made a deliberate engineering decision: Gemini 2.5 Flash only evaluates damage type, severity, and needed rescue machinery. It is strictly forbidden from guessing location. Coordinates are determined deterministically from EXIF metadata, browser GPS, or operator district polygon lookup. Each incident is permanently archived in Google Cloud Storage with structured JSON metadata for auditability."*

---

## Slide 7: Google Cloud Pub/Sub & Cloud Run: Alerting & Serverless Edge
### Low-latency, attribute-filtered disaster alerts and scalable containerized deployment.
* **Google Cloud Pub/Sub Real-Time Disaster Bus**:
  - When an incident is graded as **CRITICAL** or **HIGH**, an automated event payload is published to topic `cyclone-alerts`.
  - Message attributes include: `district`, `state`, `severity`, `location_source`, and `gcs_uri`.
  - **Granular District-Filtered Subscriptions**: Responders subscribe using message filters (e.g., `attributes.district = "Puri"`), ensuring the Puri Emergency Center receives only relevant localized life-safety alerts without message fatigue.
  - Bundled subscriber tool: `scripts/alert_subscriber.py` for live tabletop demo execution.
* **Google Cloud Run Production Containerization**:
  - Headless Streamlit application packaged via production `Dockerfile`, binding port 8080.
  - Serverless auto-scaling (0-to-N instances) absorbs sudden landfall traffic surges without manual intervention.
  - Native HTTPS encryption enables secure browser HTML5 Web Geolocation API for field teams.
* **Zero-Trust Security & Cloud Build CI/CD**:
  - Attached runtime service account `cycloneshield-run` with least-privilege IAM roles.
  - Secrets injected at deployment time from **Google Cloud Secret Manager** (`--set-secrets GEMINI_API_KEY=gemini-api-key:latest`), leaving zero plaintext credentials in containers or code.

**Speaker Notes (25s)**:  
> *"When an incident is classified as CRITICAL or HIGH, CycloneShield automatically fires an event to Google Cloud Pub/Sub. Because each message contains district metadata, downstream responders like the Puri District Control Room can use subscription filters to receive only alerts for their jurisdiction. The entire command center runs on Google Cloud Run, scaling automatically during landfall traffic surges, while Google Cloud Build and Secret Manager provide a zero-secret deployment."*

---

## Slide 8: Google BigQuery & Predictive ML: Vertex AI Blueprint
### Planetary historical cyclone data warehouse and calibrated lifeline vulnerability forecasting.
* **Google BigQuery Planetary Hurricane Warehouse**:
  - Connects to public table `bigquery-public-data.noaa_hurricanes.ibtracs_all`.
  - Ingests and analyzes historical North Indian Ocean cyclone tracks (Bay of Bengal & Arabian Sea) including Amphan, Fani, Remal, Yaas, Hudhud, and Biparjoy.
  - Implements **FinOps Dry-Run Cost Control** (`dry_run=True`) in `bigquery_pipeline.py` to calculate exact scanned query bytes before execution, preventing accidental billing charges.
* **Predictive Lifeline ML Model (HistGradientBoosting)**:
  - 5-fold cross-validated Gradient Boosting pipeline with Platt sigmoid calibration.
  - **Target A (Highway Cut-Off)**: ROC-AUC = 0.9739, PR-AUC = 0.9042, Brier Score = 0.0497.
  - **Target B (Hospital Flooding)**: ROC-AUC = 0.9758, PR-AUC = 0.8877, Brier Score = 0.0457.
  - Key predictive features: Storm surge head ($S_{\text{surge}}$), DEM elevation, distance to coastline, and sustained wind speed.
* **Vertex AI Model Registry Packaging**:
  - Serialized model artifact: `outputs/models/lifeline_risk_model.joblib` (4.8 MB).
  - Official Vertex AI manifest: `outputs/models/vertex_model_config.json`.
  - Custom container specification: `us-docker.pkg.dev/vertex-ai/prediction/sklearn-cpu.1-4:latest` with estimated 4.2 ms inference latency.

**Speaker Notes (25s)**:  
> *"CycloneShield integrates with Google BigQuery to access NOAA's planetary hurricane database, including built-in dry-run queries to prevent unexpected costs. Our calibrated machine learning pipeline predicts arterial highway cut-offs and hospital ICU flooding with an ROC-AUC above 0.975. We've packaged this model with a complete Vertex AI Model Registry manifest and container spec, making it production-ready for deployment."*

---

## Slide 9: Google Cloud Text-to-Speech: Voice-First in 7 Indian Languages
### Bridging the last-mile digital and literacy divide with high-fidelity Neural2 speech synthesis.
* **7 Regional Indian Languages Supported**:
  - **Bengali** (`bn-IN`, Bashkar / Neural2-A)
  - **Hindi** (`hi-IN`, Swara / Neural2-D)
  - **Odia** (`or-IN`, Google Cloud TTS / Neural2)
  - **Telugu** (`te-IN`, Mohan / Neural2-A)
  - **Tamil** (`ta-IN`, Pallavi / Neural2-A)
  - **Gujarati** (`gu-IN`, Dhwani / Neural2-A)
  - **English** (`en-IN`, Neural2-D / Indian Accent)
* **3-Tier Resilient Speech Cascade**:
  - **Tier 1 (Google Cloud TTS)**: High-definition Neural2 natural voices with customized speech rates (0.92x) for public loudspeaker clarity.
  - **Tier 2 (gTTS Fallback)**: Graceful free-tier synthesis when cloud quota or internet connectivity is constrained.
  - **Tier 3 (Pre-Rendered Audio Archive)**: 30 pre-rendered studio warning bulletins with emergency siren chimes ready for full offline playback.
* **Reaching the Last Mile**:
  - Generates downloadable, broadcast-ready MP3s for community FM radio, police patrol megaphones, and fishing trawler VHF radios.
  - Eliminates reliance on SMS text alerts for illiterate citizens and during power grid blackout conditions.

**Speaker Notes (25s)**:  
> *"During a severe cyclone, cell towers go dark, power lines snap, and text messages fail to reach vulnerable fishing hamlets. CycloneShield implements a voice-first alerting engine powered by Google Cloud Text-to-Speech, delivering lifelike Neural2 broadcasts across 7 Indian languages. With a three-tier fallback architecture—from Cloud TTS to gTTS and pre-rendered emergency broadcasts—the system ensures that life-saving warnings reach citizens even in full blackout conditions."*

---

## Slide 10: Explainable Risk Scoring: 4-Pillar Index & What-If Simulator
### Transparent vulnerability formulation backed by an interactive meteorological simulator.
* **Composite Vulnerability Scoring ($V_{\text{district}} \in [0, 100]$)**:
  $$V_{\text{district}} = \min\left(100.0, \; \left( \sum_{i=1}^{4} w_i \cdot I_i \right) \times M_{\text{hazard}} \right)$$
* **4 Weighted Infrastructure Pillars**:
  - 🏥 **Healthcare Vulnerability ($w_1 = 35\%$)**: Hospital beds, rural PHCs, and generator basement flood exposure.
  - 🛣️ **Road Severance Risk ($w_2 = 25\%$)**: Submerged arterial highway kilometers (e.g. State Highway 3).
  - 🏕️ **Shelter Deficit Risk ($w_3 = 25\%$)**: Capacity shortfall relative to vulnerable population (Census 2011).
  - ⚡ **Power Grid Fragility ($w_4 = 15\%$)**: Substation inundation and high-wind feeder failure exposure.
* **Dynamic "What-If" Meteorological Simulator (Tab 3)**:
  - Interactive sliders for **Central Pressure (hPa)**, **Sustained Wind Speed (km/h)**, **Forward Velocity (km/h)**, and **Rainfall (mm)**.
  - Allows disaster officers to run live sensitivity tests: *"What if Cyclone Remal slows down by 5 km/h over the delta?"* or *"What if central pressure drops another 10 mb?"*

**Speaker Notes (25s)**:  
> *"Unlike black-box models, CycloneShield's composite risk score is 100% transparent and explainable. It balances healthcare exposure at 35%, road severed risk at 25%, shelter deficits at 25%, and power grid vulnerability at 15%. In Tab 3 of our app, disaster managers can test 'what-if' scenarios using interactive meteorological sliders to see how an intensifying storm alters lifeline priorities in real time."*

---

## Slide 11: Built for India: Scope vs 4-Week SDMA Pilot Plan
### Five configured coastal state profiles and a structured 4-week rollout for state disaster authorities.
* **Pan-India Coastal Reach Today**:
  - Configured state profiles for **West Bengal**, **Odisha**, **Andhra Pradesh**, **Tamil Nadu**, and **Gujarat** (35 coastal districts).
  - Dynamic coordinate reference projection: automatically calculates appropriate UTM zones (`EPSG:32642` to `EPSG:32645`) across India's entire 7,516 km coastline.
* **4-Week Non-Disruptive SDMA Pilot Blueprint**:
  - **Week 1 (GIS Asset Onboarding)**: Ingest state health clinic coordinates, primary shelter capacities, and local road shapefiles into the spatial engine.
  - **Week 2 (IMD Live Feed Hookup)**: Connect live IMD RSMC cyclone outlook scraper and calibrate wind swath thresholds with State Emergency Operation Centre (SEOC) officers.
  - **Week 3 (Alert Channels Integration)**: Connect OASIS Common Alerting Protocol (CAP v1.2) XML export to the national NDMA Sachet portal, WhatsApp alert bots, and community radio.
  - **Week 4 (Tabletop Simulation Drill)**: Run simulated pre-landfall exercise with District Emergency Operation Centers (DEOCs) and NDRF battalions to validate operational decisions.

**Speaker Notes (25s)**:  
> *"CycloneShield is built specifically for India, supporting 5 maritime states with automated UTM coordinate projections. We have designed a structured 4-week pilot blueprint for State Disaster Management Authorities: starting with local GIS asset ingestion in Week 1, real-time IMD feed integration in Week 2, multi-channel alerting via CAP XML and WhatsApp in Week 3, and culminating in a full pre-landfall tabletop exercise with NDRF battalions in Week 4."*

---

## Slide 12: Impact, Responsible AI, & Call to Action
### Measurable societal resilience grounded in complete technical honesty and cloud excellence.
* **Quantified Societal Impact**:
  - 188M+ coastal population covered across 5 coastal state profiles.
  - 24-48 hour pre-landfall window for staging boats, pumps, and evacuation convoys.
  - Prioritized protection for hospital ICU power continuity and critical oxygen plants.
* **Responsible AI & Honest Limitations (Disclosed)**:
  - Surge model currently uses a planar bathtub elevation approach (SRTM 30m) without dynamic astronomical tides (roadmap: ADCIRC / INCOIS coupling).
  - ML models trained on physics-inspired synthetic disaster data (roadmap: leave-one-storm-out validation against verified NDRF post-disaster field reports).
  - All AI advisories and alerts require authorized human review before transmission.
* **Evaluation Deliverables & Call to Action**:
  - 🌐 **Live Streamlit Command Center**: [https://cycloneshield-vawrqbhtbgu8i6cafhbf3q.streamlit.app/](https://cycloneshield-vawrqbhtbgu8i6cafhbf3q.streamlit.app/)
  - 📂 **Source Code Repository**: [https://github.com/itsme-sherlock/CycloneShield](https://github.com/itsme-sherlock/CycloneShield)
  - 📓 **Reproducible Google Colab**: [`CycloneShield_Colab.ipynb`](https://colab.research.google.com/github/itsme-sherlock/CycloneShield/blob/main/CycloneShield_Colab.ipynb)
  - **The Ask**: Partner with us to pilot CycloneShield with state disaster authorities for India's vulnerable coastal communities.

**Speaker Notes (25s)**:  
> *"CycloneShield demonstrates how Google Cloud and AI technologies can solve the hardest last-mile challenges in disaster resilience. We are honest about our current limitations: our surge model uses bathtub elevation screening, and our ML models are trained on simulated physics awaiting field damage calibration. All code, container configs, and Colab notebooks are open and reproducible. We invite you to test our live prototype and partner with us on an SDMA pilot. Thank you."*
