# Prompt & Briefing for Next Chat: Chat 3 (Enhancement E3 — Predictive Lifeline ML Model)

> **Copy and paste the prompt below into the next chat session to immediately begin Enhancement 3.**

---

```markdown
Hello! We are continuing work on **CycloneShield** (Track-Based Cyclone Impact & Infrastructure Vulnerability Forecaster for Google DevFest / AI Hackathon).

### Current Project State:
- Chapters 1 through 7 are 100% COMPLETED and VERIFIED.
- Enhancement 1 (E1: Gemini Multimodal Ground Damage Vision) is 100% COMPLETED and VERIFIED.
- Enhancement 2 (E2: Voice-First Multilingual Audio Engine) is 100% COMPLETED and VERIFIED:
  - `voice_engine.py` - Multi-tier TTS engine (Google Cloud TTS + gTTS + offline emergency chime)
  - 30 pre-cached MP3 audio broadcasts cataloged in `outputs/audio/audio_manifest.json`
  - Integrated into Streamlit Command Center (`app.py`) with native `st.audio` players across English, Hindi, and Bengali
- Master Roadmap: `cycloneshield/ROADMAP_ENHANCEMENTS.md`
- Previous Handover: `cycloneshield/HANDOVER_ENHANCEMENT_2.md`

### Your Task for THIS Chat: Enhancement 3 (E3) — Predictive Lifeline ML Model (Vertex AI Ready)
We need to close the "Predictive Modeling & Advanced ML" hackathon rubric gap (jumping from 40% -> 90%) by training and deploying a dedicated Machine Learning model that predicts infrastructure submergence risk and lifeline failure probabilities.

### Requirements:
1. **Create `cycloneshield/predictive_model.py`**:
   - Synthesize calibrated coastal storm exposure dataset representing Bay of Bengal cyclonic history (incorporating features: elevation, distance_to_coastline_km, storm_surge_m, max_wind_speed_kts, accumulated_rain_mm, soil_saturation_idx).
   - Train a Scikit-Learn Gradient Boosting / Random Forest Classifier with calibrated probabilities:
     - Target 1: Highway Submersion Cut-off Risk (0.0 to 1.0)
     - Target 2: Healthcare Facility Inundation Risk (0.0 to 1.0)
   - Evaluate model metrics: ROC-AUC score, Precision-Recall curve, Confusion Matrix, and Permutation Feature Importances.
   - Export saved model artifact (`cycloneshield/outputs/models/lifeline_risk_model.joblib` or `.pkl`) and ROC plot (`cycloneshield/outputs/models/lifeline_model_evaluation.png`).
   - Export Google Cloud Vertex AI Model Registry deployment manifest (`cycloneshield/outputs/models/vertex_model_config.json`).
2. **Integrate Predictive ML Risk Inspector into Streamlit (`cycloneshield/app.py`)**:
   - In Tab 1 or dedicated ML sidebar inspector: display live ML-predicted cutoff probability vs. actual inundation.
   - Add interactive scenario sliders (e.g., "What if surge increases by +1.5m?") allowing ground commanders to simulate dynamic risk shifts.
3. **Verification**:
   - Run standalone model training: `python cycloneshield/predictive_model.py`
   - Verify model artifact and evaluation plots are saved in `outputs/models/`.
   - Verify Streamlit app hot-reloads cleanly with interactive ML simulation widgets.
   - Generate `HANDOVER_ENHANCEMENT_3.md` and briefing for Chat 4.

Please inspect `cycloneshield/ROADMAP_ENHANCEMENTS.md` and begin Enhancement 3.
```
