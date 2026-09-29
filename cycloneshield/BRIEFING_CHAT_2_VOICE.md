# Prompt & Briefing for Next Chat: Chat 2 (Enhancement E2 — Voice-First Multilingual Audio Engine)

> **Copy and paste the prompt below into the new chat window to immediately begin Enhancement 2.**

---

```markdown
Hello! We are working on **CycloneShield** (Track-Based Cyclone Impact & Infrastructure Vulnerability Forecaster for Google DevFest / AI Hackathon).

### Current Project State:
- Chapters 1 through 7 are 100% COMPLETED and VERIFIED.
- Enhancement 1 (E1: Gemini Multimodal Ground Damage Vision) is 100% COMPLETED and VERIFIED:
  - `multimodal_damage.py` - Core vision triage engine with Google Gemini 2.5 Flash / 1.5 Flash + calibrated zero-key fallback
  - Curated test damage photos in `data/sample_damage/`
  - Integrated into Streamlit Command Center (`app.py`) under "📸 Ground Damage AI Triage (Gemini Multimodal)"
- Master Roadmap: `cycloneshield/ROADMAP_ENHANCEMENTS.md`

### Your Task for THIS Chat: Enhancement 2 (E2) — Voice-First Multilingual Audio Engine
We need to close the "Language & Voice" hackathon track gap by implementing an automated Text-to-Speech (TTS) broadcast audio generation system for emergency cyclone advisories across English, Hindi, and Bengali.

### Requirements:
1. **Create `cycloneshield/voice_engine.py`**:
   - Ingest generated multilingual bulletins from Chapter 6 (`outputs/remal_advisories.json`).
   - Synthesize spoken voice alerts for each district in 3 languages:
     - English (`en`): Clear national broadcast voice
     - Hindi (`hi`): Regional Doordarshan / Akashvani alert voice
     - Bengali (`bn`): Coastal Sundarbans delta radio broadcast voice
   - Support Google Cloud Text-to-Speech / `gTTS` / edge-tts with pre-cached audio output so judges hear instant crystal-clear audio with zero delay.
   - Save synthesized audio MP3s into `outputs/audio/` (e.g., `remal_south_24_parganas_en.mp3`, `remal_south_24_parganas_hi.mp3`, `remal_south_24_parganas_bn.mp3`).
2. **Integrate Audio Players into Streamlit (`cycloneshield/app.py`)**:
   - In the district advisory tabs ("📢 Broadcast Advisories"), embed audio player widgets (`st.audio`) alongside the English, Hindi, and Bengali bulletins.
   - Allow instant 1-click playback for field responders and coastal communities.
3. **Verification**:
   - Run standalone generator: `python cycloneshield/voice_engine.py`
   - Verify audio files are created in `outputs/audio/` and playable.
   - Verify Streamlit app renders audio players cleanly.
   - Generate `HANDOVER_ENHANCEMENT_2.md` and briefing for Chat 3.

Please inspect `cycloneshield/ROADMAP_ENHANCEMENTS.md` and start building Enhancement 2.
```
