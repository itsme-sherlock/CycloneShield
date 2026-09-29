# 🌀 CycloneShield — 12-Slide Executive Pitch Deck Outline

> **Transforming Cyclone Forecasts into District Lifeline Action Before Landfall**  
> **Live Deployed Prototype**: [https://cycloneshield-vawrqbhtbgu8i6cafhbf3q.streamlit.app/](https://cycloneshield-vawrqbhtbgu8i6cafhbf3q.streamlit.app/)  
> **Source Repository**: [https://github.com/itsme-sherlock/CycloneShield](https://github.com/itsme-sherlock/CycloneShield)  
> **Interactive Google Colab**: [Open in Colab](https://colab.research.google.com/github/itsme-sherlock/CycloneShield/blob/main/CycloneShield_Colab.ipynb)  
> **Event**: Google DevFest / Google AI Hackathon India  

---

## Slide 1: Title & Core Promise
### CycloneShield: Converting Storm Tracks into District Lifeline Action 48 Hours Before Landfall

* **The Breakthrough**: A multi-state operational decision-support system predicting cut-off evacuation highways and flooded healthcare clinics 48 hours before cyclone landfall.
* **Live Working Prototype**: Deployed, zero-barrier web app operating within Google Cloud's 100% free-tier limits at [cycloneshield-vawrqbhtbgu8i6cafhbf3q.streamlit.app](https://cycloneshield-vawrqbhtbgu8i6cafhbf3q.streamlit.app/).
* **National Reach**: Covers 35 coastal districts across 5 states (West Bengal, Odisha, Andhra Pradesh, Tamil Nadu, Gujarat) in 7 regional Indian languages.

**Speaker Notes (20s)**:  
*"Good morning, judges. When a severe tropical cyclone approaches, tracking where it is headed is no longer the primary bottleneck. The real bottleneck is knowing what the storm will actually do to critical lifelines on the ground. CycloneShield bridges this last-mile gap—converting raw meteorological tracks into specific, lifeline-level infrastructure risk predictions 48 hours before landfall across India's coastline."*

---

## Slide 2: The Problem: The Last-Mile Operational Gap
### Weather forecasts track the storm, but field teams still lack road and hospital impact data.

* **188M+ Coastal Citizens**: Over 188 million people live in India's coastal districts (Census 2011), with ~250 million within 50 km of the sea.
* **The Information Disconnect**: Synoptic bulletins provide wind speeds, isobar charts, and landfall points, but not which arterial highway segments will flood or which hospital ICUs will lose power.
* **The Duty Officer's Dilemma**: District Magistrates and NDRF commanders must stage rescue convoys without knowing which bridges submerge first or how to reach offline communities.

**Speaker Notes (25s)**:  
*"India's coastal districts are home to over 188 million citizens. When a storm brews in the Bay of Bengal, the IMD provides accurate meteorological forecasts. But a District Magistrate cannot deploy an ambulance using wind isobar lines—they need to know if State Highway 3 is submerged and whether the local sub-divisional hospital can keep running. Today, that lifeline impact connection is missing at the district level."*

---

## Slide 3: The Solution: An End-to-End Decision Pipeline
### CycloneShield converts track forecasts into emergency directives through five automated steps.

* **1. Ingest Track**: Parses NOAA IBTrACS historical tracks or live IMD synoptic bulletin CSVs (`time, lat, lon, wind, pressure`).
* **2. Hazard & Inundation**: Generates dynamic UTM-projected wind swaths and computes coastal sea flood inundation using NASA SRTM 30m elevation.
* **3. Lifeline Exposure Join**: Spatially intersects flood polygons with OpenStreetMap arterial roads, primary health centers, and shelters.
* **4. Actionable Intelligence**: Delivers an explainable 0–100 district risk score, Gemini field advisories, and regional voice broadcasts.
* **5. Aerial Damage Triage**: Uses Gemini 2.5 Flash Multimodal Vision to evaluate post-landfall drone photos for rapid recovery dispatch.

**Speaker Notes (25s)**:  
*"CycloneShield operates as an end-to-end decision pipeline in five automated steps: ingesting storm tracks, calculating coastal inundation against 30-meter elevation maps, intersecting flood zones with road and clinic assets, computing an explainable 0 to 100 risk score, and synthesizing regional spoken advisories with automated drone damage triage."*

---

## Slide 4: Demo Flow: Multi-State Scenarios in Action
### Demonstrated across 5 Indian states and 13 historical & custom cyclone tracks.

* **West Bengal (Remal / Amphan)**: Pinpointed 39.6 km of cut-off state highways along SH-3 and flagged 5 high-risk clinics in Purba Medinipur and South 24 Parganas (~16.3M exposed population).
* **Odisha (Fani / Dana)**: Projected severe coastal surge across Puri, Jagatsinghpur, and Kendrapara, generating Odia spoken warnings.
* **Andhra Pradesh & Tamil Nadu (Hudhud / Michaung / Vardah)**: Pinpointed urban flood exposure across Visakhapatnam and Chennai corridors in Telugu and Tamil.
* **Gujarat (Biparjoy / Tauktae)**: Modeled Saurashtra and Kachchh coastal inundation in Gujarati.
* **Live Custom Track Ingestion**: 1-click loading of custom IMD bulletins for emerging storms.

**Speaker Notes (25s)**:  
*"Here is our live prototype in action. Rather than being confined to one city, CycloneShield works across West Bengal, Odisha, Andhra Pradesh, Tamil Nadu, and Gujarat. On Cyclone Remal, it identified 39.6 kilometers of severed highway and 5 flooded clinics before landfall. On Cyclone Fani in Odisha, it maps surge risk across Puri and Kendrapara, while generating Odia audio broadcasts with zero latency."*

---

## Slide 5: Google AI at Work: Meaningful, Mission-Critical AI
### Google AI bridges complex spatial telemetry into life-saving spoken warnings and drone triage.

* **Google Gemini 2.5 Flash Advisory Engine**: Ingests multi-district exposure matrices to generate structured tactical advisories and OASIS CAP v1.2 XML alerts.
* **Voice-First Cloud TTS & Translation**: Automatically translates alerts into 7 Indian languages (Hindi, Bengali, Odia, Telugu, Tamil, Gujarati, English) and generates broadcast-ready spoken audio for battery radios.
* **Gemini Multimodal Vision Triage**: Ingests citizen and drone aerial photos, classifying damage severity (1–5), water depth, road blockages, and recovery equipment needed. Non-disaster photos are automatically filtered out.
* **BigQuery NOAA Pipeline**: Ingests historical cyclone records with FinOps cost controls ($0.0002 / query), operating 100% within the free tier.

**Speaker Notes (25s)**:  
*"We harness Google AI where it does indispensable work: Gemini 2.5 Flash synthesizes raw geospatial telemetry into tactical advisories; Cloud Translation and Cloud TTS broadcast emergency warnings in the mother tongue of coastal fishing communities before cell towers collapse; and Gemini Multimodal Vision triages post-disaster drone imagery in seconds to deploy heavy pumps to severed roads."*

---

## Slide 6: Data Transparency: Real vs. Simulated Grounding
### Honest labeling of data provenance ensures operational credibility and trust.

* **🟢 Real Data**:
  - NOAA IBTrACS v4 synoptic tracks via Google BigQuery Public Data.
  - USGS / NASA SRTM 30m Digital Elevation Model via Google Earth Engine.
  - OpenStreetMap road networks, hospitals, and designated cyclone shelters.
  - Official Census of India (2011) district populations.
  - Field damage drone photographs analyzed live by Gemini Vision.
* **🟡 Screening Models**:
  - Coastal bathtub storm surge model (calibrated to central barometric pressure deficit).
  - Predictive lifeline ML classifier (HistGradientBoosting / Random Forest).
* **🔵 Simulated Data**:
  - NDRF tactical incident dispatch logs and unit staging recommendations.

**Speaker Notes (25s)**:  
*"In life-or-death disaster operations, credibility demands absolute transparency. CycloneShield explicitly badges every data stream: our cyclone tracks, satellite elevations, infrastructure grids, and census counts are 100% real. Our storm surge and predictive ML models are honestly labeled as screening-level estimates, and operational dispatch logs are marked as simulated."*

---

## Slide 7: Predictive ML & Vertex AI Readiness
### Calibrated gradient boosting models forecast lifeline cut-offs ahead of landfall.

* **Dual Lifeline Targets**: Predicts state highway severance (ROC-AUC: 0.941, PR-AUC: 0.904) and hospital flood isolation (ROC-AUC: 0.938, PR-AUC: 0.888).
* **Calibrated Probabilities**: Uses `CalibratedClassifierCV` (Platt scaling) on 3,600 physics-simulated disaster instances to deliver reliable failure probabilities under changing storm intensity.
* **Vertex AI-Ready**: Complete model artifact (`joblib`), schema manifest (`vertex_model_config.json`), and serving container specs ready for Google Cloud Vertex AI Model Registry deployment.

**Speaker Notes (25s)**:  
*"To anticipate infrastructure collapse, we trained a calibrated machine learning pipeline. With ROC-AUCs exceeding 0.94, our model allows disaster commanders to test 'what-if' scenarios—such as a 1.5-meter spring tide surge shift—delivering calibrated road and hospital cut-off probabilities in under 5 milliseconds. The model is fully packaged for Google Cloud Vertex AI Model Registry."*

---

## Slide 8: Who It Serves: Actionable Decisions by Persona
### Delivering the exact operational decision each disaster responder needs to make differently.

* **NDRF / SDRF Battalions**: Pre-stage motorized inflatable rescue boats, dewatering pumps, and chainsaw teams outside predicted flood zones before highways submerge.
* **District Magistrates & SDMA Officers**: Issue targeted evacuation orders for low-lying polders 24–48 hours earlier and safeguard rural hospital backup generators.
* **Coastal Communities**: Receive clear, spoken voice warnings over battery-powered community radios in their regional dialect (Bengali, Odia, Telugu, Tamil, Gujarati).

**Speaker Notes (20s)**:  
*"CycloneShield serves three distinct personas: NDRF commanders pre-stage heavy rescue gear outside flood corridors; District Magistrates order targeted evacuations 24 hours earlier; and coastal families receive spoken radio alerts in their mother tongue before telecommunication towers fail."*

---

## Slide 9: Built for India: National Reach Across 5 States
### Scaled from Bengal to all major cyclone-prone coastal states along 7,516 km of coastline.

* **Multi-State Parameterization**: Active coverage across West Bengal, Odisha, Andhra Pradesh, Tamil Nadu, and Gujarat.
* **Dynamic Coordinate Projections**: Automatically adapts UTM coordinate reference systems (`EPSG:32642` to `EPSG:32645`) based on cyclone longitude.
* **7 Regional Languages Supported**: High-fidelity text and neural voice synthesis across English, Hindi, Bengali, Odia, Telugu, Tamil, and Gujarati.
* **Custom Bulletin Ingestion**: Accepts standard IMD synoptic tracking CSVs, allowing any state disaster agency to track live developing storms.

**Speaker Notes (25s)**:  
*"CycloneShield is built for all of India. Our spatial architecture dynamically adapts coordinate projections and elevation queries from the Bay of Bengal to the Arabian Sea. With native support for 5 major coastal states and 7 regional languages, any state disaster management authority can ingest live IMD bulletins and protect their coastal communities immediately."*

---

## Slide 10: Deployability: A 4-Week State Agency Pilot
### A lightweight, non-disruptive pilot integrating seamlessly with existing SDMA workflows.

* **Week 1 (State GIS Onboarding)**: Ingest state health clinic coordinates, primary shelter capacities, and local road shapefiles into the spatial engine.
* **Week 2 (Telecommunications & Radio Integration)**: Connect OASIS CAP v1.2 XML output to the national alerting portal (Sachet / NDMA) and district WhatsApp bots.
* **Week 3 (Field Testing & Tabletop Drill)**: Run a simulated pre-landfall exercise with District Emergency Operation Centers (DEOCs) and NDRF battalions.
* **Week 4 (Go-Live & Duty Handover)**: Deploy serverless container to Google Cloud Run with automated Cloud Build CI/CD.

**Speaker Notes (25s)**:  
*"We do not ask disaster agencies to overhaul their systems. We offer a lightweight 4-week pilot: two weeks to load state-verified hospital and shelter GIS assets, one week to connect Common Alerting Protocol XML feeds and district WhatsApp groups, and one week for a tabletop drill with NDRF officers. It runs serverless on Google Cloud Run with zero ongoing maintenance burden."*

---

## Slide 11: Impact, Limitations, & Technical Roadmap
### Delivering measurable societal impact with a clear, honest path toward operational deployment.

* **Projected Impact**: Provides 48-hour advance lifeline intelligence protecting over 188 million coastal citizens across 35 vulnerable districts.
* **Current Limitations (Disclosed)**:
  - Planar bathtub surge model does not capture dynamic astronomical tidal harmonics.
  - SRTM 30m elevation lacks micro-drainage culvert resolution.
  - ML models trained on simulated disaster physics, pending live disaster damage log validation.
* **Phase 3 Roadmap**:
  - Couple hydrodynamic tide models (ADCIRC / SLOSH) with IMD coastal storm surge models.
  - Conduct leave-one-storm-out validation against verified NDRF post-disaster damage logs.
  - Partner with State Remote Sensing Centers for high-resolution 1m LiDAR/drone elevation data.

**Speaker Notes (25s)**:  
*"Responsible AI requires transparency about limitations. Our surge model uses an empirical bathtub elevation method without dynamic tidal coupling, and our ML models are trained on simulated physics data. By acknowledging these boundaries, we establish a credible roadmap: coupling hydrodynamic surge models, ingesting high-resolution drone elevation grids, and validating against verified post-disaster damage logs."*

---

## Slide 12: Team & Call to Action: From Forecast to Action
### Partner with us to pilot CycloneShield for India's most vulnerable coastal communities.

* **Team Details**: CycloneShield Disaster AI Research & Engineering Team
* **Live Working Web App**: [https://cycloneshield-vawrqbhtbgu8i6cafhbf3q.streamlit.app/](https://cycloneshield-vawrqbhtbgu8i6cafhbf3q.streamlit.app/)
* **Reproducible Code & Colab**: [github.com/itsme-sherlock/CycloneShield](https://github.com/itsme-sherlock/CycloneShield)
* **The Ask**: We are seeking pilot partnerships with State Disaster Management Authorities (OSDMA, WBSDMA, APSDMA, TNSDMA, GSDMA) and disaster management research grants to operationalize CycloneShield for the upcoming cyclone season.

**Speaker Notes (20s)**:  
*"CycloneShield proves that Google AI and open cloud data can transform passive weather bulletins into proactive, life-saving infrastructure intelligence. The prototype is live, tested, and ready. We invite hackathon reviewers and disaster authorities to test our platform and partner with us on our upcoming coastal pilots. Thank you!"*
