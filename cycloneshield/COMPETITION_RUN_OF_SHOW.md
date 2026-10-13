# CycloneShield Competition Run-of-Show

**Format:** 5-minute presentation + 5-minute jury Q&A  
**Rule:** Keep the application open and demonstrate it live. Use slides only to orient the jury; do not spend the slot reading the existing 12-slide deck.

## Readiness gate

Checked on 2026-10-12:

- In the prior deployment check, the public Streamlit app loaded. Reopen it before the slot and verify the current eight tabs and deployed revision; do not assume the hosted copy matches un-deployed source.
- The deployed vision panel reported **Zero-Key Calibrated Vision Mode**. The deployed model selector also differed from the current working tree. Do not describe that hosted page as a live Gemini analysis until the updated app is deployed and verified.
- No Gemini key was configured in the local `.env`. Do not put an API key in source control, slides, screen shares, or terminal output.
- The working tree's vision UI now distinguishes a successful live Gemini response from its offline fallback. This change is not live until it is deployed.

Before the slot, in Streamlit Community Cloud open the app's **Settings → Secrets** and add the key in TOML format:

```toml
GEMINI_API_KEY = "your-key"
```

Save the secret, publish the current source to the branch connected to the app, and let Streamlit redeploy (or reboot the app). Run the photo-triage action. Proceed with live Gemini claims only if the result confirms a live response; a configured key alone is not proof that the API call succeeded. Do not put the real key in the repository or presentation. Also verify the Cloud Text-to-Speech voice separately if you plan to present it as live.

If live API access cannot be confirmed, use the offline mode as a deliberate reliability demo and say that the example is a calibrated benchmark/fallback, not model-generated image analysis. The currently hosted app is on Streamlit Community Cloud; the repository's Cloud Run scripts describe a deployment path, not proof that the current public app runs on Cloud Run.

## Five-minute presentation

| Time | Live action |
| --- | --- |
| 0:00–0:25 | Open on West Bengal / REMAL. State the problem and frame 188M+ as a Census-era population-scale reference, not people already protected. |
| 0:25–0:55 | Show state and storm choices; clarify that switching state selects configured data and does not fetch a new state-agency feed. |
| 0:55–1:10 | Show the seven language choices and explain that broadcasts use fixed templates. |
| 1:10–1:55 | Tab 1: point to the map layers and district inspector; call risk/counts scenario rules and surge a screening estimate. |
| 1:55–2:20 | Tab 2: preview copy-ready alerts and CAP export; do not claim live delivery or Gemini-generated translation. |
| 2:20–2:55 | Tab 3: show the triage path. Claim Gemini only after a successful live-response indicator; otherwise present the offline benchmark honestly. |
| 2:55–3:12 | Tab 4: show the deterministic district risk matrix and CSV export. |
| 3:12–3:35 | Tab 5: show a what-if change; identify the local model and synthetic training data. |
| 3:35–3:52 | Tab 6: identify insurance thresholds and amounts as illustrative, not an active policy. |
| 3:52–4:15 | Tab 7: read the live/estimated badge and timestamp; clarify it is not an official IMD bulletin and does not drive other tabs. |
| 4:15–4:40 | Tab 8: show the Google/GCP integration paths and distinguish deployed services from blueprints. |
| 4:40–4:52 | State the five-state/seven-language scale-out path and 188M+ context. |
| 4:52–5:00 | Make one pilot ask and stop. |

For the **verbatim spoken script**, live/offline alternatives, and detailed click cues, use [DETAILED_PRESENTATION_SCRIPT.md](./DETAILED_PRESENTATION_SCRIPT.md). For likely component-specific questions, use [JUDGE_QA_BY_COMPONENT.md](./JUDGE_QA_BY_COMPONENT.md). The two linked documents are the source of truth if this quick timing table is shortened further during rehearsal.

### Spoken script

**0:00–0:35 — The problem**

> “When a cyclone approaches, knowing its track is only the start. District teams need to know which roads may be cut off, which hospitals and shelters are exposed, and how to communicate when networks fail. Census 2011 data put the population of India’s coastal districts at over 188 million. CycloneShield is a decision-support prototype for closing that last-mile information gap.”

**0:35–1:55 — Live product**

> “Here is the working command view. I’ll use the West Bengal Remal scenario, then inspect its district-level exposure and hazard layers. These numbers are screening estimates for a historical scenario, not an official forecast or evacuation order. The state selector covers West Bengal, Odisha, Andhra Pradesh, Tamil Nadu, and Gujarat. I can also change the broadcast language so an officer can prepare a locally understandable message.”

*(Show the map and inspector; change the language. Keep the cursor moving and do not read every metric.)*

**1:55–2:25 — From analysis to action**

> “The broadcast hub turns that context into SMS, WhatsApp, and public-address text, and exports a Common Alerting Protocol 1.2 XML payload. Today this is a standards-based export for integration—not a direct connection to SACHET or a live public alert.”

*(Preview the XML and click Download only if the download is useful in the room.)*

**2:25–2:55 — AI / fallback**

If live Gemini is verified:

> “For field triage, the configured Gemini Vision model can analyze an uploaded image and return structured observations and response suggestions. The live-result status here confirms this request reached Gemini. A human responder remains responsible for validating the evidence and acting.”

If live Gemini is not verified:

> “This deployment is in calibrated offline mode, so this benchmark result is not a Gemini image analysis. The workflow remains demonstrable without credentials; I’m not claiming live Google AI for this run.”

**2:55–3:40 — Google technology**

> “The application is Python and Streamlit. It includes an optional Gemini Vision path for explicit photo triage, a BigQuery path for NOAA history, and optional Google Cloud Text-to-Speech. The district inspector and broadcast use deterministic rules and fixed templates, not live Gemini generation. The current public demo is hosted on Streamlit Community Cloud; Cloud Run and Vertex AI are deployment blueprints, not its current runtime.”

**3:40–4:20 — Scale**

> “The prototype exposes five coastal states and seven languages: English, Hindi, Bengali, Odia, Telugu, Tamil, and Gujarati. Scaling means onboarding state-verified roads, hospitals, shelters, and local alert procedures—not merely copying the interface. We would pilot with one state control room, validate its asset data and language workflows, then repeat the integration pattern state by state.”

**4:20–4:50 — Impact and trust**

> “The opportunity is better prioritization for communities and critical lifelines across a coastal population measured at over 188 million in Census 2011. The surge layer is a screening estimate, and the current lifeline model is not field-validated; it is not a replacement for IMD forecasts or official authority. Our next step is agency-led validation against verified event and infrastructure data.”

**4:50–5:00 — The ask**

> “We’re seeking a state disaster-management partner for a measured pilot: validate the data, test the workflow in a tabletop exercise, and define the safety and integration gates for operational use. Thank you.”

## Five-minute jury Q&A

Keep answers to about 20–30 seconds. If asked for more detail, offer it after the slot.

**Is this live Google AI or a simulation?**  
“The app has both paths. The status on the triage result tells us whether that specific request returned from Gemini. If it says offline, the displayed benchmark is a deterministic fallback—not a live model result. I only claim live AI when that request is confirmed.”

**What does the 188M+ figure mean?**  
“It is a Census 2011-based estimate of people living in India’s coastal districts. It describes the scale of the population the problem concerns; it is not a measured number of users protected by this prototype.”

**How accurate are the flood and failure predictions?**  
“The surge layer is a screening approximation, and current model benchmarks use simulated disaster physics. They are not field validation. Before operational use, we need holdout-storm evaluation and agency-verified damage and asset records.”

**Does CycloneShield send alerts directly to SACHET or the public?**  
“No. It produces copy-ready messages and a CAP 1.2 XML export. A verified agency integration, approval workflow, and operational safeguards would be required before any public alerting.”

**What does Google add?**  
“The repository includes a Gemini Vision path, a BigQuery path for NOAA historical data, and an optional Google Cloud Text-to-Speech path. The displayed district inspector and broadcasts use configured rules and fixed templates, not live Gemini generation. Cloud Run and Vertex AI are deployment blueprints here; the public demo is on Streamlit Community Cloud and the simulator runs locally.”

**How do five states and seven languages scale?**  
“The interface already has those state and language choices. A real rollout still needs each state’s authoritative asset data, terminology review, voice checks, alert protocol integration, and field validation. The architecture is repeatable; operational readiness must be earned state by state.”

**What happens if the key, network, or model is unavailable?**  
“The prototype falls back to a clearly labeled offline benchmark path. We never treat that result as proof that a cloud model ran. Production would also require key rotation, monitoring, rate limits, audit logs, and a tested human approval workflow.”

**Is this production-ready?**  
“No. It is a working decision-support prototype. It demonstrates the workflow and integration points; it still needs validation with disaster agencies, stronger hydrodynamic modeling, reliable state data, security review, and operational exercises.”

## Final operator checklist

- Open the deployed URL in the exact browser and network you will use; wait for the app to finish loading.
- Confirm the deployed revision matches the current source and the model selector is the expected Gemini model.
- Confirm the secret is configured without displaying or sharing its value; perform one real Gemini request and verify the live-result indicator.
- Test the intended photo, language, audio, and CAP export in advance; keep the offline demo video available as backup.
- Keep the default scenario selected, pre-open the tabs, disable notifications, and rehearse the timed sequence with a visible five-minute timer.
- Do not claim live SACHET integration, field-validated model accuracy, or Cloud Run hosting unless each has actually been verified.
