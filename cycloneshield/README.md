# 🌀 CycloneShield — Multi-Hazard Cyclone Impact & Infrastructure Vulnerability Forecaster

> **CycloneShield is an interactive cyclone decision-support prototype for Indian coastal states. It combines historical NOAA cyclone tracks and real-time India Meteorological Department (IMD / RSMC New Delhi) bulletin ingestion with scenario-based hazard screening, a local what-if model, multilingual message templates, optional Gemini Vision triage, and an optional real-time weather feed. It demonstrates workflows for prioritizing critical lifelines and preparing messages; it is not an official forecast, field-validated impact model, or operational alerting system.**

[![Live Demo](https://img.shields.io/badge/Streamlit%20App-Live%20Demo-FF4B4B?logo=streamlit&logoColor=white)](https://cycloneshield-vawrqbhtbgu8i6cafhbf3q.streamlit.app/)
[![IMD / RSMC](https://img.shields.io/badge/IMD%20%2F%20RSMC-Live%20Ingestion-FF6F00)](https://rsmcnewdelhi.imd.gov.in/)
[![Google Cloud Run](https://img.shields.io/badge/Google%20Cloud-Run%20Ready-4285F4?logo=googlecloud&logoColor=white)](https://cloud.google.com/run)
[![Google BigQuery](https://img.shields.io/badge/Google%20BigQuery-Public%20Dataset-009688?logo=googlebigquery&logoColor=white)](https://cloud.google.com/bigquery)
[![Gemini 2.5 Flash](https://img.shields.io/badge/Google%20Gemini-2.5%20Flash-8E75C4?logo=googlegemini&logoColor=white)](https://aistudio.google.com/)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/itsme-sherlock/CycloneShield/blob/main/CycloneShield_Colab.ipynb)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-green.svg)](https://opensource.org/licenses/Apache-2.0)

**[🌐 Live Streamlit App](https://cycloneshield-vawrqbhtbgu8i6cafhbf3q.streamlit.app/) • [🎥 Master Demo Video (MP4)](../CycloneShield_Demo_Walkthrough.mp4) • [🎥 WebM Video](../cycloneshield_demo_walkthrough.webm) • [🎙️ Audio Voiceover](../cycloneshield_demo_voiceover.mp3) • [🚀 1-Click Google Colab](https://colab.research.google.com/github/itsme-sherlock/CycloneShield/blob/main/CycloneShield_Colab.ipynb) • [📊 Executive Pitch Deck](../PITCH_DECK.md) • [🎬 Video Demo Script](./DEMO_SCRIPT.md) • [📝 Audit Report](../AUDIT_REPORT.md)**

**Competition prep:** [Detailed 5-minute spoken script](./DETAILED_PRESENTATION_SCRIPT.md) • [Judge Q&A by component](./JUDGE_QA_BY_COMPONENT.md) • [5-minute run-of-show](./COMPETITION_RUN_OF_SHOW.md)

---

## 📦 Hackathon Submission Package (Judge Quick-Links)

| Submission Deliverable | Direct Repository Link / URL | Description |
| :--- | :--- | :--- |
| **1. Deployed Working Prototype** | **[🌐 Launch Live Streamlit App](https://cycloneshield-vawrqbhtbgu8i6cafhbf3q.streamlit.app/)** | Hosted interactive command center (works out-of-the-box with zero API keys required). |
| **2. Demo Video (3–5 Minutes)** | **[🎥 `CycloneShield_Demo_Walkthrough.mp4`](../CycloneShield_Demo_Walkthrough.mp4)** *(H.264/AAC)*<br>**[🎥 `cycloneshield_demo_walkthrough.webm`](../cycloneshield_demo_walkthrough.webm)** | 3m 28s end-to-end working walkthrough with studio narration ([`cycloneshield_demo_voiceover.mp3`](../cycloneshield_demo_voiceover.mp3)) and live Bengali radio broadcast. |
| **3. Pitch Deck (PPTX & Markdown)** | **[📊 `CycloneShield_Pitch_Deck.pptx`](./CycloneShield_Pitch_Deck.pptx)**<br>**[📄 `PITCH_DECK.md`](../PITCH_DECK.md)** | 12-slide executive presentation covering problem, Google AI architecture, validation, and 4-week state rollout. |
| **4. Source Code & 1-Click Colab** | **[💻 `cycloneshield/app.py`](./app.py)**<br>**[🚀 `CycloneShield_Colab.ipynb`](../CycloneShield_Colab.ipynb)** | Modular Python codebase, trained ML artifacts, Dockerfile, and reproducible Google Colab notebook. |
| **5. Demo Script & Recording Guide** | **[🎬 `DEMO_SCRIPT.md`](./DEMO_SCRIPT.md)**<br>**[🧭 `DEMO_VIDEO_RECORDING_GUIDE.md`](./DEMO_VIDEO_RECORDING_GUIDE.md)** | Recording storyboard for the current eight-tab app; verify the deployed revision and visible tabs before presenting. |
