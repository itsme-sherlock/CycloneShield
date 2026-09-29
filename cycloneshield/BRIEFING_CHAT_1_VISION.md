# Prompt & Briefing for Next Chat: Chat 1 (Enhancement E1 — Gemini Multimodal Damage Vision)

> **Copy and paste the prompt below into the new chat window to immediately begin Enhancement 1.**

---

```markdown
Hello! We are working on **CycloneShield** (Track-Based Cyclone Impact & Infrastructure Vulnerability Forecaster for Google DevFest / AI Hackathon).

### Current Project State:
- Chapters 1 through 7 are 100% COMPLETED and VERIFIED:
  - Track Ingestion (`track_input.py`) - DONE
  - Wind Swaths (`wind_swath.py`) - DONE
  - Surge & Rain Hazard with GEE SRTM DEM (`surge_rain.py`) - DONE
  - Infrastructure Exposure (`infra_exposure.py`) - DONE
  - XAI Vulnerability Scoring (`vuln_scoring.py`) - DONE
  - Gemini Structured Advisory Layer (`gemini_advisory.py`) - DONE
  - Interactive Streamlit Dashboard (`app.py`) - DONE & verified on http://localhost:8501
- Master Roadmap: `cycloneshield/ROADMAP_ENHANCEMENTS.md`

### Your Task for THIS Chat: Enhancement 1 (E1) — Gemini Multimodal Damage Vision
We need to close the "Vision & Multimodal" hackathon track gap by implementing a Citizen & NDRF Ground Damage Photo Triage system powered by **Google Gemini 1.5 / 2.5 Flash Multimodal Vision**.

### Requirements:
1. **Create `cycloneshield/multimodal_damage.py`**:
   - Ingest an image file (JPEG/PNG) of cyclone/flood damage (e.g. flooded hospital road, breach in saline embankment, collapsed bridge, downed power line).
   - Call Gemini API (`gemini-2.5-flash` or `gemini-1.5-flash`) using base64 image encoding with structured prompt.
   - Structured JSON response schema:
     - `damage_type`: e.g. "Road Submersion", "Embankment Breach", "Structural Collapse", "Electrical Grid Hazard"
     - `severity_score`: Integer 1 to 5 (5 being Critical Life Threat)
     - `estimated_water_depth_m`: Estimated flood depth in meters or null
     - `access_impediment`: "Complete Blockage | Partial Passage | Normal"
     - `recommended_ndrf_action`: Concrete action directive (e.g. "Deploy inflatable assault boat & dewatering pump")
     - `confidence_score`: Float 0.0 to 1.0
   - Resilient Fallback: Provide calibrated deterministic fallback responses if no API key is present or when offline.
2. **Add Sample Test Images**:
   - Generate / curate realistic demo sample damage images or synthetic SVG/PNG damage scenes in `cycloneshield/data/sample_damage/` (e.g. `flooded_highway.png`, `broken_embankment.png`, `submerged_clinic.png`).
3. **Integrate into Streamlit Command Center (`cycloneshield/app.py`)**:
   - Add a new tab or section: "📸 Ground Damage AI Triage (Gemini Multimodal)".
   - Allow user to either upload their own photo or select from pre-loaded field incident samples.
   - Display the image alongside the live Gemini Multimodal breakdown (threat badge, severity gauge, recommended response equipment, and dispatch status).
4. **Verification**:
   - Test standalone CLI: `python cycloneshield/multimodal_damage.py`
   - Verify in Streamlit: Ensure `app.py` runs without errors and renders the vision triage interface smoothly.
   - Create `HANDOVER_ENHANCEMENT_1.md` when completed.

Please inspect `cycloneshield/ROADMAP_ENHANCEMENTS.md` and start building Enhancement 1.
```
