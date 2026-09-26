# CycloneShield — Project Handover Note: Chapter 6 (Gemini Advisory Layer)

**Project Name**: CycloneShield — Track-Based Cyclone Impact & Infrastructure Vulnerability Forecaster  
**Target Event**: Google DevFest / Google AI Hackathon (100% Free Tier Ecosystem)  
**Workspace Root**: `c:\Users\LENOVO\devfest\cycloneshield\`  
**Mirrored Directory**: `C:\mnt\agents\output\cycloneshield\` *(NTFS junction linked)*  
**Master Blueprint**: [`MASTER_PLAN.md`](file:///c:/Users/LENOVO/devfest/cycloneshield/MASTER_PLAN.md)

---

## 1. Project State & Verified Milestone Summary

Chapters 1 through 5 are **100% COMPLETED and VERIFIED**. All outputs, datasets, and scripts exist and have been tested.

| Chapter | Module Script | Primary Outputs Generated & Verified | Status |
| :--- | :--- | :--- | :---: |
| **Chapter 1: Track Ingestion** | `track_input.py` | `remal_track.csv`, `remal_track.geojson`, `remal_track_map.html`, `remal_track_plot.png` | **DONE** |
| **Chapter 2: Wind Swaths** | `wind_swath.py` | `remal_wind_swaths.geojson`, `remal_wind_segments.geojson`, `remal_wind_swaths_map.html`, `remal_wind_swaths_plot.png` | **DONE** |
| **Chapter 3: Surge & Rain Hazard** | `surge_rain.py` | `remal_surge_inundation.geojson` ($3.56\text{m}$ peak surge), `remal_rainfall_hazard.geojson`, `remal_surge_rainfall_map.html`, `remal_surge_rainfall_plot.png` | **DONE** |
| **Chapter 4: Infrastructure Exposure** | `infra_exposure.py` | `remal_district_exposure.csv`, `remal_district_exposure.json`, `remal_infrastructure_roads.geojson` (SH-3: 20.6 km cut-off), `remal_infrastructure_map.html`, `remal_infrastructure_plot.png` | **DONE** |
| **Chapter 5: Vulnerability Scoring** | `vuln_scoring.py` | `remal_vulnerability_scores.csv`, `scores.csv`, `remal_vulnerability_scores.json`, `remal_district_vulnerability.geojson`, `remal_vulnerability_ranking.png` (300 DPI), `remal_vulnerability_map.html` | **DONE** |

### Verified District Vulnerability Ranking (from Chapter 5):
- 🔴 **Rank 1: South 24 Parganas (96.4 / 100 — CRITICAL)**: 4 Flooded Hospitals, 4 Flooded Shelters, 20.6 km SH-3 highway submerged, Priority 1 Evacuation.
- 🔴 **Rank 2: Satkhira (91.2 / 100 — CRITICAL)**: 1 Flooded Hospital, 2 Flooded Shelters, 19.0 km R760 highway submerged, Priority 1 Evacuation.
- 🟠 **Rank 3: North 24 Parganas (68.5 / 100 — HIGH)**: 100% of facilities in Core Hurricane Wind (>48 kts), Priority 2 Pre-positioning.
- 🟠 **Rank 4: Khulna (61.2 / 100 — HIGH)**: Core hurricane gusts, acute cyclone shelter capacity deficit, Priority 2.
- 🟡 **Rank 5: Bagerhat (44.8 / 100 — MODERATE)**: Moderate gale winds & local canal waterlogging, Priority 3.
- 🔵 **Ranks 6–10: Purba Medinipur (24.5), Patuakhali (19.8), Barguna (17.2), Kolkata (14.5), Howrah (11.8)**: Peripheral low/minimal exposure.

---

## 2. Objective for Chapter 6: Gemini Advisory Layer

Chapter 6 is the **Core Google AI Product Showcase** for hackathon judges. It connects Google Gemini API (`google-genai` SDK or `google-generativeai`) to ingest the quantitative tabular outputs of Chapter 5 and generate multilingual, structured, life-saving disaster advisories.

### Requirements:
1. **Module Name**: `cycloneshield/gemini_advisory.py`.
2. **Inputs**:
   - `outputs/remal_vulnerability_scores.csv` / `remal_vulnerability_scores.json`
   - `outputs/remal_district_exposure.json`
   - `outputs/remal_infrastructure_roads.geojson`
3. **Structured JSON Output Schema (`response_mime_type="application/json"`)**:
   For each priority district, generate:
   - `district_name` (e.g., "South 24 Parganas")
   - `threat_level` ("CRITICAL", "HIGH", "MODERATE")
   - `evacuation_priority` (1 to 5)
   - `lifeline_impact_summary`: Short summary of flooded hospitals, cut-off highways, and shelter status.
   - `ndrf_incident_dispatch_log[]`: Concrete tactical action items (e.g., "Deploy 2nd Bn NDRF Boat Assault Unit to Canning ferry ghat", "Reroute ambulance convoys via inland NH-12 bypass").
   - `public_advisory_en`: Urgent broadcast message in English for national TV/radio/press.
   - `advisory_hindi`: Broadcast in Hindi for regional Doordarshan/AIR broadcasts.
   - `advisory_bengali`: Native Bengali broadcast for vulnerable coastal delta and Sundarbans communities.
4. **Resilient API Architecture**:
   - Primary: Uses `GEMINI_API_KEY` from environment with `gemini-2.5-flash` or `gemini-1.5-flash`.
   - Offline / Zero-Key Mock Fallback: If no API key is set in terminal, automatically provide calibrated deterministic advisory responses without crashing, so the pipeline is 100% reproducible for judges.
5. **Outputs to Save**:
   - `outputs/remal_advisories.json` (and generic alias `advisories.json`)
   - `outputs/remal_advisories_summary.csv`
   - Mirrored to `C:\mnt\agents\output\cycloneshield/`
6. **Hackathon Execution Rules**:
   - Run step-by-step: run code, show output, explain briefly, wait for confirmation before Chapter 7.
   - Maximize Google ecosystem (Gemini API, AI Studio, structured JSON).
   - Keep all code in `cycloneshield/`.
