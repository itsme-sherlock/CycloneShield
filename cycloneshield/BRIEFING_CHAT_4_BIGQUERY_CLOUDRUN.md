# Prompt & Briefing for Next Chat: Chat 4 (Enhancement E4 — BigQuery & Cloud Run)

> **Copy and paste the prompt below into the next chat session to immediately begin Enhancement 4.**

---

```markdown
Hello! We are continuing work on **CycloneShield** (Track-Based Cyclone Impact & Infrastructure Vulnerability Forecaster for Google DevFest / AI Hackathon).

### Current Project State:
- Chapters 1 through 7 are 100% COMPLETED and VERIFIED.
- Enhancement 1 (E1: Gemini Multimodal Vision Ground Damage Triage) is 100% COMPLETED and VERIFIED.
- Enhancement 2 (E2: Voice-First Multilingual Audio Engine) is 100% COMPLETED and VERIFIED.
- Enhancement 3 (E3: Predictive Lifeline ML Model — Vertex AI Ready) is 100% COMPLETED and VERIFIED:
  - `predictive_model.py`: 5-fold calibrated Gradient Boosting pipeline (ROC-AUC > 0.975, Brier < 0.049)
  - Serialized model artifact: `outputs/models/lifeline_risk_model.joblib` (4.8 MB)
  - 4-panel evaluation figure: `outputs/models/lifeline_model_evaluation.png`
  - Vertex AI Model Registry manifest: `outputs/models/vertex_model_config.json`
  - Streamlit Command Center (`app.py`): Tab 3 Dynamic "What-If" Scenario Simulator with live meteorological sliders
- Master Roadmap: `cycloneshield/ROADMAP_ENHANCEMENTS.md`
- Previous Handover: `cycloneshield/HANDOVER_ENHANCEMENT_3.md`

### Your Task for THIS Chat: Enhancement 4 (E4) — Google BigQuery Connector & Cloud Run Containerization
We need to close the "Data Engineering, GCP Native Integrations & Cloud Deployment" hackathon rubric gap (jumping from 65% -> 95%) by connecting the ingestion layer to Google BigQuery's public NOAA Hurricane dataset and containerizing the entire production stack for Google Cloud Run.

### Requirements:
1. **Create `cycloneshield/bigquery_pipeline.py`**:
   - Google BigQuery client querying `bigquery-public-data.noaa_hurricanes.ibtracs_all` (or regional tables).
   - Ingest archived and active North Indian Ocean cyclones (Bay of Bengal / Arabian Sea).
   - Fallback offline cache for zero-key evaluator access (`data/noaa_sample_tracks.json`).
   - Function to query track coordinates, central pressure, maximum wind speed, and forward velocity.
2. **Production Containerization & Cloud Deployment Configuration**:
   - Production `Dockerfile` optimized for Google Cloud Run (lightweight Python runtime, dependencies cached, non-root user, Streamlit headless port 8080 configuration).
   - `.dockerignore` ignoring virtualenvs, cache files, and git history.
   - `cloudbuild.yaml` for Google Cloud Build automated CI/CD container build & deployment.
   - Shell/PowerShell 1-click deployment scripts (`deploy_cloud_run.sh` / `deploy_cloud_run.ps1`).
3. **Streamlit UI Integration (`cycloneshield/app.py`)**:
   - In sidebar or data tab: BigQuery Live Track Explorer letting judges query real historical Bay of Bengal cyclones (Amphan, Fani, Remal, Yaas, Sidr) directly from NOAA BigQuery.
4. **Verification**:
   - Test `bigquery_pipeline.py` standalone execution.
   - Validate Dockerfile syntax and build requirements.
   - Update `ROADMAP_ENHANCEMENTS.md`, generate `HANDOVER_ENHANCEMENT_4.md`, and briefing for Chat 5.

Please inspect `cycloneshield/ROADMAP_ENHANCEMENTS.md` and begin Enhancement 4.
```
