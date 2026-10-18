# 🌀 CycloneShield — Multi-Hazard Cyclone Impact & Infrastructure Vulnerability Forecaster

> **CycloneShield is an interactive cyclone decision-support prototype for Indian coastal states. It combines historical NOAA cyclone tracks with an on-demand fetch of the latest dated India Meteorological Department (IMD / RSMC New Delhi) cyclone outlook/bulletin. It loads a live track only when the downloaded official document contains at least two complete, explicit waypoint rows; it does not infer a track from an outlook or fall back to synthetic demo data. Other views use scenario-based hazard screening, a local what-if model, multilingual message templates, optional Gemini Vision triage, and an optional weather feed. It is not an official forecast, field-validated impact model, or operational alerting system.**

[![Live Demo](https://img.shields.io/badge/Streamlit%20App-Live%20Demo-FF4B4B?logo=streamlit&logoColor=white)](https://cycloneshield-vawrqbhtbgu8i6cafhbf3q.streamlit.app/)
[![IMD / RSMC](https://img.shields.io/badge/IMD%20%2F%20RSMC-Live%20Bulletin%20Fetch-FF6F00)](https://rsmcnewdelhi.imd.gov.in/)
[![Google Cloud Run](https://img.shields.io/badge/Google%20Cloud-Run%20Ready-4285F4?logo=googlecloud&logoColor=white)](https://cloud.google.com/run)
[![Google BigQuery](https://img.shields.io/badge/Google%20BigQuery-Public%20Dataset-009688?logo=googlebigquery&logoColor=white)](https://cloud.google.com/bigquery)
[![Gemini 2.5 Flash](https://img.shields.io/badge/Google%20Gemini-2.5%20Flash-8E75C4?logo=googlegemini&logoColor=white)](https://aistudio.google.com/)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/itsme-sherlock/CycloneShield/blob/main/CycloneShield_Colab.ipynb)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-green.svg)](https://opensource.org/licenses/Apache-2.0)

**[🌐 Live Streamlit App](https://cycloneshield-vawrqbhtbgu8i6cafhbf3q.streamlit.app/) • [🎥 Master Demo Video (MP4)](../CycloneShield_Demo_Walkthrough.mp4) • [🎥 WebM Video](../cycloneshield_demo_walkthrough.webm) • [🎙️ Audio Voiceover](../cycloneshield_demo_voiceover.mp3) • [🚀 1-Click Google Colab](https://colab.research.google.com/github/itsme-sherlock/CycloneShield/blob/main/CycloneShield_Colab.ipynb) • [📊 Executive Pitch Deck](../PITCH_DECK.md) • [🎬 Video Demo Script](./DEMO_SCRIPT.md) • [📝 Audit Report](../AUDIT_REPORT.md)**

**Competition prep:** [Detailed 5-minute spoken script](./DETAILED_PRESENTATION_SCRIPT.md) • [Judge Q&A by component](./JUDGE_QA_BY_COMPONENT.md) • [5-minute run-of-show](./COMPETITION_RUN_OF_SHOW.md)

---

## 📍 Geo-Evidence & Alerts (Photo Triage)

Gemini judges **damage type and severity only**. Location never comes from the model.

```
photo ─► geo_locate.py ──► district (point-in-polygon, coastal_districts.geojson)
          EXIF GPS > device > manual > "unverified"
photo ─► Gemini (damage + severity) ─┐
                                     ├─► evidence_store.py ─► gs://BUCKET/<state>/<district>/<incident_id>/
                                     └─► alerts.py (CRITICAL/HIGH) ─► Pub/Sub topic ─► scripts/alert_subscriber.py
```

- Unverified locations are filed under `_unverified/`; points outside all polygons under `_outside_coverage/`.
- The bundled district polygons are coarse, overlapping rectangles: the smallest containing polygon is returned and flagged `ambiguous`.
- Storage and alerts are optional. Without credentials the app shows "Cloud features not configured" and keeps working.
- Run tests: `python -m pytest tests`

**Setup** (replace `PROJECT`, `BUCKET`):

```bash
# 1. (Optional) Link billing account if creating new GCS buckets or deploying Cloud Run
gcloud billing projects link PROJECT --billing-account=ACCOUNT_ID

# 2. Enable Cloud Storage and Pub/Sub APIs
gcloud services enable storage.googleapis.com pubsub.googleapis.com --project PROJECT

# 3. Create GCS Evidence Bucket & Pub/Sub Alert Topic
gcloud storage buckets create gs://BUCKET --project PROJECT --location asia-south1
gcloud pubsub topics create cyclone-alerts --project PROJECT
gcloud pubsub subscriptions create cs-alerts-all --topic cyclone-alerts --project PROJECT

# 4. (Optional) District-filtered subscription demo
gcloud pubsub subscriptions create cs-puri --topic cyclone-alerts --project PROJECT \
  --message-filter='attributes.district = "Puri"'
```

Grant the app's service account `roles/storage.objectCreator` on the bucket and `roles/pubsub.publisher` on the topic. Then provide settings in `.streamlit/secrets.toml` or `.env` (never commit real secrets):

```toml
GCS_BUCKET = "BUCKET"
PUBSUB_TOPIC = "cyclone-alerts"
GCP_PROJECT = "PROJECT"

[gcp_service_account]   # optional; otherwise Application Default Credentials (ADC) are used
# paste the service-account JSON key fields here
```

Demo the alerts live: `python scripts/alert_subscriber.py --project PROJECT --subscription cs-alerts-all`, then run a CRITICAL/HIGH triage in Tab 3.

**Deploy to Google Cloud Run:**

- **1-Click Script Deployment**: Run `./deploy_cloud_run.sh` (POSIX/Cloud Shell) or `.\deploy_cloud_run.ps1` (Windows PowerShell). Both scripts automatically detect your active project, package the container via the root `Dockerfile`, bind port 8080, and forward `GCS_BUCKET`, `PUBSUB_TOPIC`, `GCP_PROJECT`, and `GEMINI_API_KEY` into Cloud Run environment variables.
- **Production Deployment with Service Account & Secret Manager**:

```bash
# service account used by the Cloud Run service (no key file needed)
gcloud iam service-accounts create cycloneshield-run --project PROJECT
SA=cycloneshield-run@PROJECT.iam.gserviceaccount.com
gcloud storage buckets add-iam-policy-binding gs://BUCKET --member=serviceAccount:$SA --role=roles/storage.objectCreator
gcloud pubsub topics add-iam-policy-binding cyclone-alerts --project PROJECT --member=serviceAccount:$SA --role=roles/pubsub.publisher

# store the Gemini key securely in Secret Manager
printf '%s' "$GEMINI_API_KEY" | gcloud secrets create gemini-api-key --data-file=- --project PROJECT
gcloud secrets add-iam-policy-binding gemini-api-key --project PROJECT --member=serviceAccount:$SA --role=roles/secretmanager.secretAccessor

# Deploy to Cloud Run
gcloud run deploy cycloneshield --source . --region asia-south1 --project PROJECT \
  --service-account $SA --allow-unauthenticated --port 8080 --memory 2Gi --cpu 2 \
  --set-env-vars GCS_BUCKET=BUCKET,PUBSUB_TOPIC=cyclone-alerts,GCP_PROJECT=PROJECT \
  --set-secrets GEMINI_API_KEY=gemini-api-key:latest
```

Notes: On Cloud Run the app reads these from environment variables (no `secrets.toml` needed) and authenticates as the attached service account. Browser "device location" requires HTTPS, which Cloud Run natively provides. Pub/Sub delivers to subscribers, so run `scripts/alert_subscriber.py` from your laptop or Cloud Shell to monitor alerts live.

**Google Colab Notebook:**
[`CycloneShield_Colab.ipynb`](./CycloneShield_Colab.ipynb) includes a dedicated **Section 9.1: Location-Aware Evidence & Alerts** cell. It demonstrates:
1. EXIF GPS extraction from geotagged field photos
2. Device coordinate simulation
3. Manual operator district override
4. Out-of-coverage boundary protection (no nearest guess)
5. Live Pub/Sub alert dispatch and Cloud Storage persistence with graceful zero-key / unconfigured fallback. To run against live GCP in Colab, authenticate via `google.colab.auth.authenticate_user()`.

---

## 📦 Hackathon Submission Package (Judge Quick-Links)

| Submission Deliverable | Direct Repository Link / URL | Description |
| :--- | :--- | :--- |
| **1. Deployed Working Prototype** | **[🌐 Launch Live Streamlit App](https://cycloneshield-vawrqbhtbgu8i6cafhbf3q.streamlit.app/)** | Hosted interactive command center (works out-of-the-box with zero API keys required). |
| **2. Demo Video (3–5 Minutes)** | **[🎥 `CycloneShield_Demo_Walkthrough.mp4`](../CycloneShield_Demo_Walkthrough.mp4)** *(H.264/AAC)*<br>**[🎥 `cycloneshield_demo_walkthrough.webm`](../cycloneshield_demo_walkthrough.webm)** | 3m 28s end-to-end working walkthrough with studio narration ([`cycloneshield_demo_voiceover.mp3`](../cycloneshield_demo_voiceover.mp3)) and live Bengali radio broadcast. |
| **3. Pitch Deck (PPTX & Markdown)** | **[📊 `CycloneShield_Pitch_Deck.pptx`](./CycloneShield_Pitch_Deck.pptx)**<br>**[📄 `PITCH_DECK.md`](../PITCH_DECK.md)** | 12-slide executive presentation covering problem, Google AI architecture, validation, and 4-week state rollout. |
| **4. Source Code & 1-Click Colab** | **[💻 `cycloneshield/app.py`](./app.py)**<br>**[🚀 `CycloneShield_Colab.ipynb`](../CycloneShield_Colab.ipynb)** | Modular Python codebase, trained ML artifacts, Dockerfile, and reproducible Google Colab notebook. |
| **5. Demo Script & Recording Guide** | **[🎬 `DEMO_SCRIPT.md`](./DEMO_SCRIPT.md)**<br>**[🧭 `DEMO_VIDEO_RECORDING_GUIDE.md`](./DEMO_VIDEO_RECORDING_GUIDE.md)** | Recording storyboard for the current eight-tab app; verify the deployed revision and visible tabs before presenting. |
