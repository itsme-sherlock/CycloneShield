# 📑 CycloneShield — Technical Appendix & Methodology Backup

This document provides the mathematical formulas, validation metrics, Google Cloud deployment specifications, FinOps calculations, and data source attributions supporting the CycloneShield 12-slide pitch deck.

---

## 1. Physical & Mathematical Formulations

### 1.1 Empirical Storm Surge Model (Central Pressure Deficit)
CycloneShield calculates the peak coastal storm surge head ($S_{\text{surge}}$ in meters) derived from the central pressure deficit relative to ambient atmospheric pressure:

$$\Delta P = P_{\text{ambient}} - P_{\text{eye}}$$

$$S_{\text{surge}} = \max\left(0.5, \frac{\Delta P}{10.0} \times \mu_{\text{shelf}}\right)$$

Where:
* $P_{\text{ambient}} = 1013.25\text{ mb}$ (standard regional sea-level pressure).
* $P_{\text{eye}}$ is the minimum central barometric pressure reported in the storm track (e.g., $977.0\text{ mb}$ for Cyclone Remal, yielding $\Delta P = 36.25\text{ mb}$).
* $\mu_{\text{shelf}} \approx 0.98$ is the shallow bathymetric shelf amplification coefficient for the northern Bay of Bengal delta.
* *Example (Cyclone Remal)*: $S_{\text{surge}} = \frac{36.25}{10} \times 0.98 \approx 3.56\text{ meters}$.

### 1.2 Inland Surge Attenuation & Pluvial Ponding
Surge height decays exponentially as water travels inland across delta channels and mangrove belts:

$$S_{\text{local}}(d) = S_{\text{surge}} \cdot \exp(-k_{\text{decay}} \cdot d_{\text{coast}})$$

Where $k_{\text{decay}} = 0.026\text{ km}^{-1}$ represents hydrodynamic drag and mangrove attenuation (~50% energy drop every 26 km).

Pluvial rainwater ponding ($P_{\text{ponding}}$ in meters) is modeled as a function of 24–48hr precipitation, antecedent soil moisture, and localized drainage capacity:

$$P_{\text{ponding}} = \left(\frac{R_{\text{accum}}}{1000}\right) \cdot \sigma_{\text{soil}} \cdot (1.35 - 0.65 \cdot C_{\text{drain}})$$

Where $R_{\text{accum}}$ is cumulative rainfall in mm, $\sigma_{\text{soil}} \in [0, 1]$ is soil saturation index, and $C_{\text{drain}} \in [0, 1]$ is sluice gate/drainage capacity.

### 1.3 Composite Vulnerability Scoring Formulation
The district-level composite risk score ($V_{\text{district}} \in [0, 100]$) combines four normalized lifeline infrastructure exposure indices multiplied by storm hazard intensity:

$$V_{\text{district}} = \min\left(100.0, \; \left( \sum_{i=1}^{4} w_i \cdot I_i \right) \times M_{\text{hazard}} \right)$$

#### Dimension Weights ($w_i$):
* **Healthcare Vulnerability Index ($I_{\text{health}}$)**: $w_1 = 0.35$ (35% weight) — Flooded hospitals, rural PHCs, and generator basement submergence.
* **Road Severance Index ($I_{\text{road}}$)**: $w_2 = 0.25$ (25% weight) — Submerged arterial highway kilometers (e.g. State Highway 3).
* **Shelter Deficit Index ($I_{\text{shelter}}$)**: $w_3 = 0.25$ (25% weight) — Capacity shortfall relative to vulnerable population.
* **Power Grid Fragility Index ($I_{\text{power}}$)**: $w_4 = 0.15$ (15% weight) — Substation inundation and feeder vulnerability.

#### Hazard Intensity Multiplier ($M_{\text{hazard}}$):
$$M_{\text{hazard}} = 1.0 + 0.30 \cdot \left(\frac{V_{\text{wind}} - 34}{85}\right) + 0.25 \cdot \left(\frac{S_{\text{surge}}}{5.0}\right)$$

---

## 2. Machine Learning Benchmark & Validation Suite

### 2.1 Experimental Protocol
* **Dataset**: 3,600 physically calibrated coastal lifeline records synthesized across Bay of Bengal geographical distributions.
* **Split**: Stratified random 80/20 train/test split ($n_{\text{train}} = 2,880$, $n_{\text{test}} = 720$), stratified by target class.
* **Pre-processing**: Pre-split StandardScaler fitted exclusively on training splits to prevent data leakage.
* **Calibration**: 5-fold cross-validated Platt scaling (sigmoid calibration) applied via `CalibratedClassifierCV`.

### 2.2 Complete Metrics Comparison Table
Reproduced directly from [`outputs/models/model_metrics.json`](file:///c:/Users/LENOVO/devfest/cycloneshield/outputs/models/model_metrics.json):

#### Target A: Highway Submersion Cut-Off Risk
| Model Candidate | ROC-AUC | PR-AUC | F1-Score | Accuracy | Precision | Recall | Brier Score |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Baseline (Logistic Regression)** | 0.9798 | 0.9211 | 0.8514 | 94.86% | 0.8983 | 0.8092 | 0.0430 |
| **Random Forest Classifier** | 0.9746 | 0.9081 | 0.7256 | 91.81% | 0.9286 | 0.5954 | 0.0596 |
| **HistGradientBoosting (Calibrated)** | **0.9739** | **0.9042** | **0.7984** | **93.06%** | **0.8879** | **0.7252** | **0.0497** |

#### Target B: Healthcare Facility Inundation Risk
| Model Candidate | ROC-AUC | PR-AUC | F1-Score | Accuracy | Precision | Recall | Brier Score |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Baseline (Logistic Regression)** | 0.9774 | 0.8875 | 0.8267 | 94.58% | 0.8857 | 0.7750 | 0.0381 |
| **Random Forest Classifier** | 0.9760 | 0.8875 | 0.7419 | 93.33% | 0.9583 | 0.6053 | 0.0527 |
| **HistGradientBoosting (Calibrated)** | **0.9758** | **0.8877** | **0.8000** | **93.47%** | **0.8824** | **0.7317** | **0.0457** |

> **Honesty & Validation Note**: These metrics demonstrate high mathematical consistency against the non-linear rules of the calibrated physical simulation. They do **not** represent empirical validation against unobserved real-world disaster damage logs. Next validation phase: leave-one-storm-out cross-validation across historical storms and benchmarking against official post-disaster field reports.

### 2.3 Permutation Feature Importance (Top Drivers)
1. **Storm Surge Height ($S_{\text{surge}}$)**: Importance = 0.182 (Highway), 0.210 (Hospital).
2. **DEM Ground Elevation ($E_{\text{dem}}$)**: Importance = 0.118 (Highway), 0.162 (Hospital).
3. **Distance to Active Shoreline ($d_{\text{coast}}$)**: Importance = 0.145 (Highway), 0.124 (Hospital).
4. **Sustained Wind Speed ($V_{\text{wind}}$)**: Importance = 0.082 (Highway obstruction via fallen utility lines/trees).

---

## 3. Google Cloud Architecture & Vertex AI Specification

### 3.1 Vertex AI Model Registry Configuration
Generated manifest specification at [`outputs/models/vertex_model_config.json`](file:///c:/Users/LENOVO/devfest/cycloneshield/outputs/models/vertex_model_config.json):
* **Serving Container**: `us-docker.pkg.dev/vertex-ai/prediction/sklearn-cpu.1-4:latest`
* **Target Hardware Spec**: `n1-standard-2` (2 vCPU, 7.5 GB RAM)
* **Estimated Prediction Latency**: 4.2 ms estimated serving latency on target hardware; local measured CPU inference ~140 ms mean.
* **Batch Sizing**: Max batch size 256 instances per request.
* **Status**: "Vertex AI-ready" specification; export bundle stored at `outputs/models/lifeline_risk_model.joblib`.

### 3.2 Google Cloud Text-to-Speech Engine
* **Synthesis Cascade**:
  1. *Tier 1*: Google Cloud Text-to-Speech REST API (`Wavenet` / `Neural2` voices).
  2. *Tier 2*: Google Translate Text-to-Speech (`gTTS`) — free tier native fallback.
  3. *Tier 3*: Offline Emergency Chime Generator (dual-tone 853 Hz + 960 Hz broadcast warning chime).
* **Repo Implementation Status**: 30 broadcast audio files pre-generated and cached in `outputs/audio/` across English (`en-IN`), Hindi (`hi-IN`), and Bengali (`bn-IN/bn-BD`), indexed via `audio_manifest.json`.

---

## 4. Financial & Cloud FinOps Breakdown

### 4.1 Prototype & Hackathon Evaluation Tier ($0/month)
* **Compute (Cloud Run / Streamlit Community)**: 0 cost within free allowance (2 million requests/month, 360,000 vCPU-seconds).
* **Storage (Artifact Registry & GCS)**: < 1 GB storage within Google Cloud 5 GB free tier.
* **Speech Synthesis**: gTTS (free tier) + Google Cloud TTS free tier quota (1 million characters/month for WaveNet).

### 4.2 State Disaster Authority (SDMA) Production Pilot Estimate
For an operational 6-month deployment covering an active cyclone season across 1 coastal state:

| Component | Usage / Volume | Monthly Cost (USD) | Monthly Cost (INR) |
| :--- | :--- | :---: | :---: |
| **Cloud Run (Command Center API)** | 2 vCPU, 4GB RAM, auto-scaled to 0 | ~$12.00 | ~₹1,000 |
| **Google Cloud TTS (Regional Alerts)** | ~250,000 chars per storm event | ~$4.00 | ~₹330 |
| **Gemini 1.5 Pro (Advisories & Vision)** | ~500 prompt runs + 200 drone images | ~$8.50 | ~₹700 |
| **Cloud Storage (GeoJSON & Audio)** | 50 GB multi-region storage | ~$1.30 | ~₹110 |
| **Total Estimated Cloud Footprint** | Standby readiness + active storm | **~$25.80 / mo** | **~₹2,140 / mo** |

> **Licensing Caveat**: Google Earth Engine API is provided free of charge strictly for non-commercial research, education, and non-profit evaluation. Transitioning to a production deployment within an operational state government IT infrastructure may require an enterprise Earth Engine commercial license or migration to open-source self-hosted elevation rasters (e.g., Copernicus / Cartosat-1 DEM via GeoPandas).

---

## 5. Authoritative Data Sources & Attributions

1. **NOAA IBTrACS v4 (North Indian Ocean)**:
   * Source: National Oceanic and Atmospheric Administration (NOAA) / NCEI.
   * Dataset: `ibtracs.NI.list.v04r01.csv`.
   * Role: Historical and real-time storm tracks, coordinates, central pressure, and 1-minute sustained wind speed.
2. **NASA SRTM 30m Digital Elevation Model**:
   * Source: NASA Jet Propulsion Laboratory / USGS via Google Earth Engine.
   * Dataset: `USGS/SRTMGL1_003`.
   * Role: 30-meter ground elevation above mean sea level used for coastal inundation bathtub intersections.
3. **OpenStreetMap (OSM) via Overpass API**:
   * Source: OpenStreetMap contributors (ODbL).
   * Assets: Hospital polygons/nodes (`amenity=hospital/clinic`), road centerlines (`highway=trunk/primary/secondary`), and educational shelters.
   * Role: Ground-truth infrastructure lifelines in the Bengal delta.
4. **Census of India 2011**:
   * Source: Office of the Registrar General & Census Commissioner, India.
   * Population figures: South 24 Parganas (~8,161,961), Purba Medinipur (~5,095,875).
   * Role: District population baselines for shelter deficit and risk weighting.
5. **UNDP / NDMA Coastal Risk Assessment Studies**:
   * Source: National Disaster Management Authority (NDMA) & Ministry of Earth Sciences (MoES) / NCCR.
   * Reference: 188M+ coastal district population; ~250M citizens within 50 km of Indian coastlines.
