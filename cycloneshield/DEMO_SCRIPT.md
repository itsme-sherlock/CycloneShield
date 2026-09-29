# 🎬 CycloneShield — Official 3-to-5 Minute Hackathon Video Demo Script

> **Target Event**: Google DevFest / Google AI Hackathon India  
> **Format**: 3 to 5 Minute Live Working Walkthrough (Target Runtime: 3:30 to 4:15)  
> **Presenter**: Lead Solutions Architect & Disaster Management AI Engineer  
> **Deployed Web App**: [https://cycloneshield-vawrqbhtbgu8i6cafhbf3q.streamlit.app/](https://cycloneshield-vawrqbhtbgu8i6cafhbf3q.streamlit.app/)  
> **GitHub Repository**: [https://github.com/itsme-sherlock/CycloneShield](https://github.com/itsme-sherlock/CycloneShield)  

---

## ⏱️ Video Rundown & Step-by-Step Sequence

| Step | Duration | Screen Action | Narrative Focus |
| :---: | :---: | :--- | :--- |
| **1. Hook & Problem** | `0:00 - 0:35` | Camera on speaker / Satellite Cyclone map | The Last-Mile Disaster Gap: 188M coastal Indians, synoptic tracks vs lifeline reality |
| **2. State & Cyclone Select** | `0:35 - 1:10` | Sidebar: Pick State (Odisha / WB) & Cyclone (Fani / Remal) or Custom IMD Track | Multi-state coverage across India's coastline; dynamic track processing |
| **3. Read Plain-Language Risk** | `1:10 - 1:50` | Executive "Situation at a Glance" card & Tab 1 Flood Risk Map | Plain language risk (0-100), cut-off state highways, hospitals at flood risk |
| **4. Regional Voice Alerts** | `1:50 - 2:30` | Top Language picker $\to$ Bengali / Odia / Hindi; Click "▶️ Play Voice Alert" | Cloud TTS / Voice-First broadcast for battery radios before power grids fail |
| **5. Drone Photo Damage Triage** | `2:30 - 3:15` | Tab 3: Upload / Select Drone Damage Photo | Google Gemini 2.5 Flash Multimodal Vision extracts damage tier, water depth, and pumps |
| **6. Tactical Dispatch & CAP Alert** | `3:15 - 3:50` | Tab 4 & Tab 2: Show NDRF Dispatch Plan & Download OASIS CAP v1.2 XML | Interoperable national alerting, SMS/WhatsApp scripts, and 4-week state pilot |
| **7. Close & Call to Action** | `3:50 - 4:15` | Colab 1-Click Badge, GitHub repo, Free-Tier FinOps | 100% Free Tier, zero-barrier deployment, live link |

---

## 🎙️ Word-for-Word Walkthrough Script

### 🎬 ACT 1: The Hook & India's "Last-Mile Disaster Gap" (0:00 – 0:35)

**[VISUAL CUE]**:  
*Show title slide or satellite imagery of a cyclonic storm brewing in the Bay of Bengal, transitioning to the live CycloneShield command center.*

**[SPOKEN DIALOGUE]**:  
> *"Namaste, judges! Over 188 million Indian citizens live along our 7,500 kilometers of coastline, facing recurring severe cyclonic storms in the Bay of Bengal and Arabian Sea.  
> 
> Meteorological agencies like the IMD forecast cyclone trajectories with remarkable precision. But when a District Magistrate or NDRF Battalion Commander prepares for landfall, they hit the **'Last-Mile Disaster Gap'**:  
> A wind isobar doesn't tell a duty officer which evacuation road will submerge under storm surge, which sub-divisional hospital will lose generator access, or how to alert fishing villages when mobile towers go dark.  
> 
> This is **CycloneShield**—an end-to-end multi-state disaster intelligence platform converting cyclone tracks into lifeline-level actions before landfall."*

---

### 🎬 ACT 2: Step 1 — Pick State, Cyclone & Live IMD Track (0:35 – 1:10)

**[VISUAL CUE]**:  
*In the left sidebar, show the **State Selector**. Switch between **Odisha**, **Andhra Pradesh**, **West Bengal**, and **Gujarat**. Select **Odisha** $\to$ **Cyclone Fani**, or show **West Bengal** $\to$ **Cyclone Remal**. Briefly show the **'Upload / Enter Custom Track'** toggle with the 1-click **'Load Sample IMD Bulletin'** button.*

**[SPOKEN DIALOGUE]**:  
> *"CycloneShield is built for all of India—not just one city. In the sidebar, disaster managers can select any coastal state—from West Bengal and Odisha to Andhra Pradesh, Tamil Nadu, and Gujarat.  
> 
> The platform dynamically pulls authentic NOAA IBTrACS tracks for 13 historic cyclones, or ingests live synoptic IMD bulletins via CSV upload.  
> 
> Watch how seamlessly it processes the cyclone: our spatial engine dynamically calculates the local UTM projection zone, projects multi-tier gale and hurricane wind swaths, and queries NASA SRTM elevation data—loading the entire regional risk profile in under three seconds."*

---

### 🎬 ACT 3: Step 2 — Read Plain-Language Risk at a Glance (1:10 – 1:50)

**[VISUAL CUE]**:  
*Highlight the top **'Situation at a Glance'** card. Point to the **Extreme Risk** badge, Landfall ETA, Population Exposed (~16.3M), and the **Top 3 Recommended Actions**. Then scroll to Tab 1 showing the **Ranked District Priority** table and the interactive Folium map.*

**[SPOKEN DIALOGUE]**:  
> *"Under disaster pressure, duty officers don't have time to decipher complex data science jargon.  
> 
> Right at the top, our **'Situation at a Glance'** card provides immediate situational clarity in five seconds: storm category, expected landfall window, overall risk level—here rated **EXTREME**—and the top three immediate directives: evacuate low-lying coastal polders, close coastal state highways, and activate hospital backup generators.  
> 
> In Tab 1, our Explainable Risk Index ranks districts with plain-language rationales: South 24 Parganas is flagged at 88 out of 100 primarily due to 39.6 kilometers of highway cutoffs and coastal surge inundation, while Purba Medinipur follows with critical hospital exposure. The interactive map renders exact sea flood zones and flags at-risk healthcare centers."*

---

### 🎬 ACT 4: Step 3 — Multilingual Spoken Voice Alerts (1:50 – 2:30)

**[VISUAL CUE]**:  
*Navigate to the top language picker. Switch from English to **Bengali (`বাংলা`)** or **Odia (`ଓଡ଼ିଆ`)**. Point to the translated alert card. Click the **'▶️ Play Voice Alert'** button to play the synthesized audio.*

**[SPOKEN DIALOGUE]**:  
> *"When a super cyclone makes landfall, power grids collapse and cellular bandwidth vanishes. Battery-powered community radios and loudspeaker sirens become the only life-saving communication channels.  
> 
> CycloneShield is voice-first and multilingual. Using Google Gemini and Cloud Translation, it instantly translates emergency advisories into seven Indian languages: Bengali, Hindi, Odia, Telugu, Tamil, Gujarati, and English.  
> 
> Listen to our Voice Engine broadcasting an urgent Bengali coastal advisory via Google Cloud TTS:*  
> 
> `[Audio plays 3-4 seconds of authentic emergency Bengali broadcast]`  
> 
> *"Every coastal district officer can play, download, or broadcast these spoken warnings with zero latency."*

---

### 🎬 ACT 5: Step 4 — Google Gemini Multimodal Drone Damage Triage (2:30 – 3:15)

**[VISUAL CUE]**:  
*Switch to **Tab 3: 📸 Field Damage Reconnaissance**. Select the benchmark scene: **Flooded Arterial Highway** or upload a drone image. Show the visual reconnaissance cards: **Damage Level 5/5 (Critical)**, **What is Blocked**, **What is Needed**, and the **Next Step**.*

**[SPOKEN DIALOGUE]**:  
> *"As the storm passes, the response shifts to rescue and recovery. In Tab 3, we harness **Google Gemini 2.5 Flash Multimodal Vision** for field reconnaissance.  
> 
> NDRF drone operators and ground citizens upload damage photographs directly from the field. Within seconds, Gemini analyzes the image: detecting breached river embankments, estimating flood water depth at **1.2 meters**, rating damage at **Severity 5/5 (Critical)**, and recommending immediate tactical recovery orders: deploying high-capacity submersible dewatering pumps and rerouting ambulances along an alternate bypass corridor.  
> 
> Crucially, it detects and ignores non-hazard photos, preventing false alarms from wasting relief assets."*

---

### 🎬 ACT 6: Step 5 — Tactical Dispatch & OASIS CAP Alert Export (3:15 – 3:50)

**[VISUAL CUE]**:  
*Switch to **Tab 4: 🚨 Disaster Response Plan & NDRF Staging**. Show the resource breakdown (NDRF Battalions, Inflatable Boats, Dewatering Pumps). Then show the **Download CAP v1.2 XML** button and the copy-ready WhatsApp/SMS message boxes.*

**[SPOKEN DIALOGUE]**:  
> *"In Tab 4, CycloneShield generates a complete **NDRF Tactical Resource Staging Plan**: calculating exactly how many rescue battalions, inflatable motorized boats, and high-output pumps must be pre-positioned outside the flood zone.  
> 
> To integrate seamlessly into national workflows, duty officers can export standardized **OASIS Common Alerting Protocol (CAP v1.2) XML** with one click, or copy ready-to-send emergency broadcasts formatted specifically for district WhatsApp groups and SMS relays.  
> 
> A state disaster authority can pilot this platform within 4 weeks simply by uploading their district shelter and hospital coordinates."*

---

### 🎬 ACT 7: Close, Free-Tier FinOps & Call to Action (3:50 – 4:15)

**[VISUAL CUE]**:  
*Scroll down to reveal the collapsed **'🔬 For Technical Reviewers & Judges'** section showing the Vertex AI model manifest, scikit-learn ROC curves (0.94+), and BigQuery FinOps summary ($0.00 cost). End on the GitHub repository and 1-Click Colab badge.*

**[SPOKEN DIALOGUE]**:  
> *"For technical evaluators, CycloneShield includes a calibrated Scikit-Learn ML engine with a Vertex AI Model Registry manifest, and connects directly to NOAA BigQuery Public Data—processing queries for under $0.0002, operating 100% within Google Cloud's free-tier quotas.  
> 
> You can test CycloneShield right now: visit our live deployed Streamlit app, or click the **'Open in Colab'** badge on GitHub to run the complete end-to-end pipeline in one click.  
> 
> CycloneShield transforms meteorological predictions into saved Indian lives. Thank you!"*

---

## 📋 Presenter's Pre-Flight Checklist

1. **Browser Setup**:
   - Open [https://cycloneshield-vawrqbhtbgu8i6cafhbf3q.streamlit.app/](https://cycloneshield-vawrqbhtbgu8i6cafhbf3q.streamlit.app/) in Chrome (clean tab, bookmarks bar hidden, 100% zoom).
   - Have GitHub repository tab open in background.
2. **Audio Setup**:
   - Verify desktop audio recording in OBS / screen recorder so the Bengali voice alert plays clearly.
   - Microphone levels set between -6 dB and -12 dB.
3. **Execution Pacing**:
   - Keep transitions brisk: 30 seconds per act ensures a crisp 3-minute 45-second total presentation.
