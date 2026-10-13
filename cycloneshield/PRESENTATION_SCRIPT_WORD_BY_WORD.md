# CycloneShield — Word-by-Word Presentation Script (5 Minutes)

Read this verbatim. Keep it under 5 minutes. Do NOT ad-lib beyond this.

---

## 0:00–0:25 — Opening

"Good morning. During a cyclone, the storm track is only the beginning. A district operations team needs to decide, quickly: which roads may become impassable, which hospitals and shelters need contingencies, and how warnings can reach people even if cellular service fails. Census-era data put India's coastal-district population at over 188 million. CycloneShield is a decision-support prototype that connects a storm scenario to district lifelines and preparedness actions."

---

## 0:25–0:55 — State & Cyclone Selectors

"The prototype is parameterized for five Indian coastal states: West Bengal, Odisha, Andhra Pradesh, Tamil Nadu, and Gujarat. Switching state changes the configured cyclone choices, the district records, the regional-language default, and the state-specific simulator profile. It does not connect to that state's control room or fetch its current data. Historical tracks use a bundled NOAA-derived catalog first. The BigQuery module can query the public NOAA IBTrACS table when Google Cloud credentials and a project are configured; otherwise it falls back to its local cache."

---

## 0:55–1:10 — Language Selection

"The interface offers seven languages — English, Hindi, Bengali, Odia, Telugu, Tamil, and Gujarati — with a regional default by state. Broadcasts use prepared language templates and an audio-synthesis path. Every safety message must be reviewed by agencies and local speakers before use."

---

## 1:10–1:55 — Tab 1: Situation & Hazard Maps

"This interactive map plots a selected storm against configured district profiles. It is not a live satellite feed. Tracks may come from the historical bundle. Risk rows and facility counts use scenario rules, not a fresh live overlay of assets. The surge value is a screening estimate based on pressure deficit. Population figures are Census-era references. These results do not replace an IMD forecast or an official decision."

---

## 1:55–2:20 — Tab 2: Voice Alerts & CAP Export

"Here the scenario becomes copy-ready messages for SMS, WhatsApp, and community radio, plus a CAP 1.2 XML export for State Disaster Management Authorities. This demo does not send alerts to SACHET, carriers, or the public. Voice has a Google Cloud Text-to-Speech path and fallback paths; I claim a live voice service only if verified in this run."

---

## 2:20–2:55 — Tab 3: Photo Triage

[If live Gemini confirmed:]
"This is the post-impact workflow. Gemini Vision returned this image's structured observations, severity, access implications, and equipment suggestions. The live confirmation verifies this request reached Gemini. These are not ground truth — a responder must verify them."

[If offline fallback:]
"This is an offline benchmark reference, not Gemini analysis of the image. It demonstrates the workflow without credentials. I am not claiming live image understanding."

---

## 2:55–3:12 — Tab 4: Multi-District Risk Matrix

"The matrix compares configured districts and exports CSV. Its risk rows use deterministic rules based on district ordering and storm intensity — not a live incident feed or a fresh asset-by-asset analysis. A state partner must validate its boundaries, assets, population, and thresholds before operational use."

---

## 3:12–3:35 — Tab 5: What-If Landfall Simulator

"This is sensitivity analysis. Vary surge, wind, or rainfall, and a local scikit-learn model recalculates screening scores for a configured state profile. Training used a 3,600-row synthetic, physics-inspired dataset — not verified damage records. This compares scenarios; it is not a validated forecast."

---

## 3:35–3:52 — Tab 6: Parametric Insurance

"This demonstrates illustrative wind and surge thresholds mapped to payout tiers. They are assumptions — not an insurance contract, a live financial product, or a money transfer."

---

## 3:52–4:15 — Tab 7: Real-Time Met Feed

"This tab requests a 72-hour Open-Meteo forecast and marine data for configured state coordinates. The badge and retrieval time distinguish live responses from fallback estimates. This is not an official IMD forecast, and this separate feed does not currently drive the risk KPIs or the simulator."

---

## 4:15–4:40 — Tab 8: Architecture

"The application is Python and Streamlit. It includes an optional Gemini Vision path for explicit photo triage, a BigQuery path for NOAA history, and optional Google Cloud Text-to-Speech. The simulator runs locally. This demo is hosted on Streamlit Community Cloud. Cloud Run and Vertex AI are deployment blueprints, not its current runtime."

---

## 4:40–4:52 — Scale & Impact

"Scaling means state-by-state data and workflow validation, not just a dropdown. The five configurations and seven language choices are a starting point. The 188 million figure describes the population scale of the problem — it is not active users, deployed coverage, or measured impact from this prototype."

---

## 4:52–5:00 — Close

"We are seeking one state partner for a controlled data-validation and tabletop pilot. Thank you."

---

**STOP at five minutes.** Do not open a second demo while the jury waits for Q&A.