# 🌀 CycloneShield — 12-Slide Executive Pitch Deck Outline

> **Turning Storm Scenarios into Clearer District Priorities**
> **Hosted Interactive Prototype**: [https://cycloneshield-vawrqbhtbgu8i6cafhbf3q.streamlit.app/](https://cycloneshield-vawrqbhtbgu8i6cafhbf3q.streamlit.app/) (verify the deployed revision and each live data source before presenting)
> **Source Repository**: [https://github.com/itsme-sherlock/CycloneShield](https://github.com/itsme-sherlock/CycloneShield)  
> **Interactive Google Colab**: [Open in Colab](https://colab.research.google.com/github/itsme-sherlock/CycloneShield/blob/main/CycloneShield_Colab.ipynb)  
> **Event**: Google DevFest / Google AI Hackathon India  

---

## Slide 1: Title & Core Promise
### CycloneShield: Turning Storm Scenarios into Clearer District Priorities

* **The Goal**: Help district teams turn storm scenarios and configured lifeline data into clearer priorities and possible preparedness actions.
* **Interactive Prototype**: The hosted Streamlit interface demonstrates the workflow; individual data feeds and AI services are live only when the app confirms a successful request.
* **Configured Scope**: Five state profiles and seven language choices illustrate a path toward broader, agency-validated coverage.

**Speaker Notes (20s)**:  
*"Good morning, judges. Weather agencies track cyclones, and response officers make operational decisions. CycloneShield is not a replacement for either. It is a decision-support prototype designed to turn a selected storm scenario and configured district information into clearer lifeline priorities and possible actions for people to review."*

---

## Slide 2: The Problem: The Last-Mile Operational Gap
### Weather forecasts track the storm, but field teams still lack road and hospital impact data.

* **188M+ Coastal Citizens**: Over 188 million people live in India's coastal districts (Census 2011), with ~250 million within 50 km of the sea.
* **The Information Disconnect**: Synoptic bulletins provide wind speeds, isobar charts, and landfall points, but not which arterial highway segments could face flooding or which hospital ICUs may need backup planning.
* **The Duty Officer's Dilemma**: District Magistrates and NDRF commanders must stage rescue convoys without knowing which bridges submerge first or how to reach offline communities.

**Speaker Notes (25s)**:  
*"India's coastal districts are home to over 188 million citizens, based on Census 2011—not a count of people currently protected by this prototype. Weather agencies issue forecasts, while local officers make operational decisions. CycloneShield is designed to help those officers compare storm scenarios and configured lifeline information when considering preparedness options."*

---

## Slide 3: The Solution: An End-to-End Decision Pipeline
### CycloneShield demonstrates a decision-support workflow; it does not generate official forecasts or dispatch responders.

* **1. Select a scenario**: Start with the bundled historical storm catalog, or provide a track file; describe external queries as live only after confirming them in the running app.
* **2. Review hazard context**: Surge and rainfall outputs are screening estimates. Earth Engine, when connected, can supply or process geospatial layers such as elevation; it does not predict cyclones.
* **3. Examine configured lifelines**: District profiles and open-data-derived baselines inform the displayed map and risk matrix; state changes do not guarantee fresh agency or asset data.
* **4. Compare priorities**: Rules and local ML produce scenario-based screening scores and recommend possible actions for qualified officers to review.
* **5. Inspect a photo**: The user-requested vision workflow calls Gemini only when configured and a successful live response is confirmed; otherwise the prepared offline benchmark is a demonstration, not model analysis.

**Speaker Notes (25s)**:  
*"CycloneShield demonstrates how selected storm scenarios and configured district profiles can be organized into a map, screening scores, and possible preparedness actions. Live forecasts require a connected weather source; the prototype does not replace official forecasts or automatically dispatch responders."*

---

## Slide 4: Demo Flow: Multi-State Scenarios in Action
### Configured scenarios illustrate a multi-state workflow; they are not live state-agency integrations.

* **West Bengal (Remal / Amphan)**: A configured scenario displays district rankings and lifeline screening results; these are not observed impacts or a validated forecast.
* **Other state profiles**: Odisha, Andhra Pradesh, Tamil Nadu, and Gujarat provide configured examples whose local data and thresholds need partner validation.
* **Track input**: A user can select a bundled historical track or provide a compatible track file; neither action implies a live IMD connection.
* **Prepared photo triage**: Offline benchmark scenes demonstrate the workflow. Call the result Gemini analysis only when the UI confirms a successful live Gemini response.
* **Weather and maps**: The map visualizes the selected scenario and configured geospatial baselines. Show weather as live only when its source/status badge confirms a successful current response.

**Speaker Notes (25s)**:  
*"This is a configured Cyclone Remal scenario in our interactive prototype. The map and risk matrix help compare modeled priorities; they are screening outputs, not confirmed road closures or clinic flooding. The five state profiles are a starting point for local validation, not live integrations with those agencies."*

---

## Slide 5: Google Tools at Work: Distinct Roles
### Each tool has a bounded role; AI outputs and messages remain subject to human review.

* **Gemini Vision**: Optional, explicitly requested image analysis when a configured API returns successfully. Otherwise the prepared offline benchmark demonstrates the interaction; it is not Gemini output.
* **Gemini advisory code**: An integration path exists in the repository, but displayed dashboard broadcasts use prepared templates rather than live Gemini-generated advisories.
* **Earth Engine**: Optional geospatial/elevation data processing when authenticated; it does not provide live cyclone forecasts or predictions.
* **Weather sources**: A separate Open-Meteo feed may return current forecast data. Verify its status badge and retrieval time; it is not an official IMD forecast and does not currently drive the risk KPIs or simulator.
* **BigQuery**: Optional path for historical NOAA IBTrACS queries; the bundled historical catalog is used unless a live query is confirmed.

**Speaker Notes (25s)**:  
*"Each service has a specific role. Gemini Vision can analyze a submitted photo only when configured and a successful live response is confirmed; otherwise the displayed result is a prepared offline benchmark. The dashboard's displayed broadcasts are prepared templates, not live Gemini output. Earth Engine can support geospatial analysis, while live forecasts require a connected weather source. CycloneShield recommends possible actions for human review; it does not deploy resources or send alerts."*

---

## Slide 6: Data Transparency: Real vs. Simulated Grounding
### Honest labeling of data provenance ensures operational credibility and trust.

* **Historical/configured inputs**: Bundled NOAA-derived storm tracks, configured district profiles, open-data-derived geospatial baselines, and Census-era population references. These are not all live queries.
* **Conditional live services**: Open-Meteo weather and Gemini Vision are live only when the running app confirms a successful response. Earth Engine and BigQuery are optional data/processing paths, not forecast engines.
* **Screening outputs**: Surge, risk scores, and the what-if model are scenario estimates; the model was trained on synthetic physics-inspired data and lacks field validation.
* **Prepared demonstration**: Offline photo-triage benchmark results and simulated dispatch examples are not live AI analysis or actual operations.

**Speaker Notes (25s)**:  
*"We distinguish historical and configured inputs, conditional live service responses, screening estimates, and prepared demonstrations. A visible service badge and retrieval time—not the presence of integration code—determine whether we call a response live."*

---

## Slide 7: Predictive ML & Vertex AI Readiness
### A prototype model compares scenarios; it is not a validated operational forecast.

* **Synthetic-task benchmarks**: Internal ROC-AUC / PR-AUC metrics are from synthetic test scenarios only; they do not establish real-world predictive accuracy.
* **Synthetic training data**: The model was trained/evaluated on physics-inspired synthetic scenarios, not verified historical damage records; its displayed scores are not calibrated probabilities of real-world failure.
* **Vertex AI deployment blueprint**: The model artifact (`joblib`), schema manifest (`vertex_model_config.json`), and serving container specs are packaging artifacts; inference in this demo runs locally.

**Speaker Notes (25s)**:  
*"The what-if view compares model outputs as scenario inputs change. Its training and test data are synthetic, so benchmark metrics show internal performance on those scenarios—not real-world predictive accuracy. Field validation with verified damage records is a necessary next step."*

---

## Slide 8: Who It Serves: Actionable Decisions by Persona
### Helping officers consider options—without replacing their judgment or authority.

* **NDRF / SDRF Battalions**: Review possible staging locations for boats, pumps, and access routes against scenario-based risk information.
* **District Magistrates & SDMA Officers**: Consider possible evacuation, facility-continuity, and resource-prioritization actions using validated local data.
* **Coastal Communities**: Could receive agency-approved, locally reviewed voice warnings through established channels; this prototype does not transmit public alerts.

**Speaker Notes (20s)**:  
*"CycloneShield does not replace weather agencies or rescue officers. It is designed to help them turn complex information into clearer priorities, compare possible actions, and make faster decisions. Any deployment, evacuation, or public warning remains with authorized people and agencies."*

---

## Slide 9: Built for India: National Reach Across 5 States
### Five configured state profiles are a starting point for validation, not proof of national operational coverage.

* **Configured Profiles**: West Bengal, Odisha, Andhra Pradesh, Tamil Nadu, and Gujarat.
* **Dynamic Coordinate Projections**: Automatically adapts UTM coordinate reference systems (`EPSG:32642` to `EPSG:32645`) based on cyclone longitude.
* **7 Language Choices**: Prepared text templates and a multi-tier audio path; verify the voice service used in the current run and obtain local review before any public use.
* **Track Input**: Compatible user-supplied track files can be explored; this does not establish a live IMD connection or forecast service.

**Speaker Notes (25s)**:  
*"The prototype is configured with five state profiles and seven language choices. Scaling responsibly requires state partners to validate the underlying boundaries, assets, thresholds, and message workflows—and to connect appropriate live weather sources."*

---

## Slide 10: Deployability: A 4-Week State Agency Pilot
### A proposed pilot would validate data and workflows before any operational use.

* **Week 1 (State GIS Onboarding)**: Ingest state health clinic coordinates, primary shelter capacities, and local road shapefiles into the spatial engine.
* **Week 2 (Telecommunications & Radio Integration)**: Connect OASIS CAP v1.2 XML output to the national alerting portal (Sachet / NDMA) and district WhatsApp bots.
* **Week 3 (Field Testing & Tabletop Drill)**: Run a simulated pre-landfall exercise with District Emergency Operation Centers (DEOCs) and NDRF battalions.
* **Week 4 (Tabletop & Review)**: Run a controlled exercise, evaluate limitations, and agree next steps. Any operational deployment would require separate approval and integration work.

**Speaker Notes (25s)**:  
*"Our proposed next step is a controlled pilot with a state partner: validate local data, review draft outputs, and run a tabletop exercise. Connecting alert channels or deploying to production would require agency approval, technical integration, and operational safeguards."*

---

## Slide 11: Impact, Limitations, & Technical Roadmap
### Delivering measurable societal impact with a clear, honest path toward operational deployment.

* **Potential Impact**: Could help teams prioritize lifeline review for communities in cyclone-prone areas; the 188 million figure describes population scale, not people currently protected by CycloneShield.
* **Current Limitations (Disclosed)**:
  - Planar bathtub surge model does not capture dynamic astronomical tidal harmonics.
  - SRTM 30m elevation lacks micro-drainage culvert resolution.
  - ML models trained on simulated disaster physics, pending live disaster damage log validation.
* **Phase 3 Roadmap**:
  - Couple hydrodynamic tide models (ADCIRC / SLOSH) with IMD coastal storm surge models.
  - Conduct leave-one-storm-out validation against verified NDRF post-disaster damage logs.
  - Partner with State Remote Sensing Centers for high-resolution 1m LiDAR/drone elevation data.

**Speaker Notes (25s)**:  
*"Responsible AI requires transparency about limitations. Our surge model uses an empirical bathtub elevation method without dynamic tidal coupling, and our ML models are trained on simulated physics data. By acknowledging these boundaries, we establish a credible roadmap: coupling hydrodynamic surge models, ingesting high-resolution drone elevation grids, and validating against verified post-disaster damage logs."*

---

## Slide 12: Team & Call to Action: From Forecast to Action
### Partner with us to pilot CycloneShield for India's most vulnerable coastal communities.

* **Team Details**: CycloneShield Disaster AI Research & Engineering Team
* **Hosted Interactive Prototype**: [https://cycloneshield-vawrqbhtbgu8i6cafhbf3q.streamlit.app/](https://cycloneshield-vawrqbhtbgu8i6cafhbf3q.streamlit.app/)
* **Reproducible Code & Colab**: [github.com/itsme-sherlock/CycloneShield](https://github.com/itsme-sherlock/CycloneShield)
* **The Ask**: We are seeking a state partner for controlled data validation and tabletop evaluation before considering operational integration.

**Speaker Notes (20s)**:  
*"CycloneShield is not trying to replace weather agencies or rescue officers. It is designed to help them turn complex information into clearer priorities and faster decisions. We are seeking a partner to validate the data and test the workflow in a controlled tabletop pilot. Thank you."*
