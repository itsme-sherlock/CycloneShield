"""
CycloneShield - 12-Slide Pitch Deck Generator (Updated with Complete Google Cloud & AI Stack)
Builds a high-impact, clean, 16:9 widescreen presentation using python-pptx.
Grounded strictly in repo reality, verified facts, and comprehensive Google Cloud services.
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_PPTX = os.path.join(BASE_DIR, "CycloneShield_Pitch_Deck.pptx")
SCREENSHOTS_DIR = os.path.join(BASE_DIR, "outputs", "screenshots")
MODELS_DIR = os.path.join(BASE_DIR, "outputs", "models")

# Palette
BG_DARK = RGBColor(11, 17, 32)        # #0B1120 deep navy
CARD_BG = RGBColor(26, 36, 56)        # #1A2438 card dark slate
TEXT_WHITE = RGBColor(248, 250, 252)  # #F8FAFC crisp white
TEXT_MUTED = RGBColor(148, 163, 184)  # #94A3B8 light slate
ACCENT_CYAN = RGBColor(56, 189, 248)  # #38BDF8 primary accent
ACCENT_ORANGE = RGBColor(249, 115, 22)# #F97316 warning/hazard
ACCENT_RED = RGBColor(239, 68, 68)    # #EF4444 critical
ACCENT_GREEN = RGBColor(16, 185, 129) # #10B981 success/validation
BORDER_COLOR = RGBColor(51, 65, 85)   # #334155 subtle border

def apply_slide_bg(slide):
    """Sets a solid deep navy background."""
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = BG_DARK

def add_header(slide, category: str, title: str):
    """Adds standard clean header with tag and takeaway sentence."""
    tag_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(0.4))
    tf_tag = tag_box.text_frame
    tf_tag.word_wrap = True
    tf_tag.margin_left = tf_tag.margin_right = tf_tag.margin_top = tf_tag.margin_bottom = 0
    p_tag = tf_tag.paragraphs[0]
    p_tag.text = category.upper()
    p_tag.font.size = Pt(11)
    p_tag.font.bold = True
    p_tag.font.color.rgb = ACCENT_CYAN
    p_tag.font.name = "Arial"

    title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.75), Inches(11.7), Inches(0.9))
    tf_title = title_box.text_frame
    tf_title.word_wrap = True
    tf_title.margin_left = tf_title.margin_right = tf_title.margin_top = tf_title.margin_bottom = 0
    p_title = tf_title.paragraphs[0]
    p_title.text = title
    p_title.font.size = Pt(21)
    p_title.font.bold = True
    p_title.font.color.rgb = TEXT_WHITE
    p_title.font.name = "Arial"

def add_speaker_note(slide, note_text: str):
    """Adds speaker notes to slide."""
    notes_slide = slide.notes_slide
    text_frame = notes_slide.notes_text_frame
    text_frame.text = note_text.strip()

def add_card(slide, left, top, width, height, border_color=BORDER_COLOR):
    """Adds a dark slate rounded card shape."""
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = CARD_BG
    shape.line.color.rgb = border_color
    shape.line.width = Pt(1)
    return shape

def build_deck():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # =========================================================================
    # SLIDE 1: Title + Core Promise + Hosted Prototype
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    apply_slide_bg(s1)

    pill = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.9), Inches(5.8), Inches(0.45))
    pill.fill.solid()
    pill.fill.fore_color.rgb = CARD_BG
    pill.line.color.rgb = ACCENT_CYAN
    p = pill.text_frame.paragraphs[0]
    p.text = "GOOGLE AI HACKATHON • DISASTER RESILIENCE & CLOUD AI"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = ACCENT_CYAN
    p.alignment = PP_ALIGN.CENTER

    t_box = s1.shapes.add_textbox(Inches(0.8), Inches(1.6), Inches(11.7), Inches(2.3))
    tf = t_box.text_frame
    tf.word_wrap = True
    p1 = tf.paragraphs[0]
    p1.text = "CycloneShield"
    p1.font.size = Pt(44)
    p1.font.bold = True
    p1.font.color.rgb = TEXT_WHITE
    p1.font.name = "Arial"

    p2 = tf.add_paragraph()
    p2.text = "Turning Storm Scenarios into Clearer District Priorities"
    p2.font.size = Pt(20)
    p2.font.bold = True
    p2.font.color.rgb = ACCENT_CYAN
    p2.font.name = "Arial"

    p3 = tf.add_paragraph()
    p3.text = "Powered by Google Cloud Run, BigQuery, Gemini 2.5 Flash, Pub/Sub, Cloud Storage, Vertex AI & Cloud TTS."
    p3.font.size = Pt(13)
    p3.font.color.rgb = TEXT_MUTED
    p3.font.name = "Arial"

    # 3 Info Cards at bottom
    c1 = add_card(s1, Inches(0.8), Inches(4.3), Inches(3.6), Inches(2.3), ACCENT_CYAN)
    tf1 = c1.text_frame
    tf1.word_wrap = True
    p = tf1.paragraphs[0]
    p.text = "🌐 LIVE STREAMLIT PROTOTYPE"
    p.font.bold = True
    p.font.size = Pt(11.5)
    p.font.color.rgb = ACCENT_CYAN
    p = tf1.add_paragraph()
    p.text = "cycloneshield-vawrqbhtbgu8i6cafhbf3q.streamlit.app"
    p.font.size = Pt(10.5)
    p.font.color.rgb = TEXT_WHITE
    p = tf1.add_paragraph()
    p.text = "\nInteractive command center: 5 coastal states, 7 Indian languages, and zero-key evaluator fallback."
    p.font.size = Pt(9.5)
    p.font.color.rgb = TEXT_MUTED

    c2 = add_card(s1, Inches(4.7), Inches(4.3), Inches(3.6), Inches(2.3), BORDER_COLOR)
    tf2 = c2.text_frame
    tf2.word_wrap = True
    p = tf2.paragraphs[0]
    p.text = "📂 OPEN SOURCE REPOSITORY"
    p.font.bold = True
    p.font.size = Pt(11.5)
    p.font.color.rgb = ACCENT_CYAN
    p = tf2.add_paragraph()
    p.text = "github.com/itsme-sherlock/CycloneShield"
    p.font.size = Pt(10.5)
    p.font.color.rgb = TEXT_WHITE
    p = tf2.add_paragraph()
    p.text = "\nProduction Dockerfile, Cloud Build CI/CD, Vertex AI manifest, and Apache 2.0 open-source code."
    p.font.size = Pt(9.5)
    p.font.color.rgb = TEXT_MUTED

    c3 = add_card(s1, Inches(8.6), Inches(4.3), Inches(3.9), Inches(2.3), BORDER_COLOR)
    tf3 = c3.text_frame
    tf3.word_wrap = True
    p = tf3.paragraphs[0]
    p.text = "🚀 REPRODUCIBLE GOOGLE COLAB"
    p.font.bold = True
    p.font.size = Pt(11.5)
    p.font.color.rgb = ACCENT_CYAN
    p = tf3.add_paragraph()
    p.text = "CycloneShield_Colab.ipynb"
    p.font.size = Pt(10.5)
    p.font.color.rgb = TEXT_WHITE
    p = tf3.add_paragraph()
    p.text = "\n1-Click interactive execution of BigQuery queries, ML training, Pub/Sub alerts & GCS evidence vault."
    p.font.size = Pt(9.5)
    p.font.color.rgb = TEXT_MUTED

    add_speaker_note(s1, (
        "Good morning, judges. Weather agencies track cyclones, and disaster response officers make operational decisions. "
        "CycloneShield bridges that critical operational gap. It is an end-to-end decision-support prototype powered by 11 Google Cloud "
        "and AI services—including Gemini 2.5 Flash, BigQuery, Cloud Storage, Pub/Sub, Cloud Run, Vertex AI, and Cloud Text-to-Speech—designed "
        "to translate raw storm scenarios into clear district lifeline priorities, road cut-off forecasts, and targeted alerts."
    ))

    # =========================================================================
    # SLIDE 2: Problem: The Last-Mile Gap
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    apply_slide_bg(s2)
    add_header(s2, "The Problem: The Last-Mile Operational Gap",
               "Weather forecasts track the storm, but field teams still lack road and hospital impact data.")

    card_w = Inches(3.7)
    card_h = Inches(4.8)

    p_card1 = add_card(s2, Inches(0.8), Inches(1.8), card_w, card_h)
    tf = p_card1.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "🌊 Coastal Scale & Risk"
    p.font.bold = True
    p.font.size = Pt(14)
    p.font.color.rgb = ACCENT_ORANGE
    p = tf.add_paragraph()
    p.text = "\n• 188M+ coastal citizens reside across India's maritime districts (Census 2011)."
    p.font.size = Pt(12)
    p.font.color.rgb = TEXT_WHITE
    p = tf.add_paragraph()
    p.text = "\n• ~250M people live within 50 km of the sea (UNDP/NDMA Studies)."
    p.font.size = Pt(12)
    p.font.color.rgb = TEXT_WHITE
    p = tf.add_paragraph()
    p.text = "\n• The Bay of Bengal historically accounts for catastrophic storm surges due to shallow shelf bathymetry."
    p.font.size = Pt(11.5)
    p.font.color.rgb = TEXT_MUTED

    p_card2 = add_card(s2, Inches(4.8), Inches(1.8), card_w, card_h)
    tf = p_card2.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "📡 The Information Disconnect"
    p.font.bold = True
    p.font.size = Pt(14)
    p.font.color.rgb = ACCENT_RED
    p = tf.add_paragraph()
    p.text = "\n• Synoptic bulletins provide wind speeds, isobar charts, and landfall points—not infrastructure impact."
    p.font.size = Pt(12)
    p.font.color.rgb = TEXT_WHITE
    p = tf.add_paragraph()
    p.text = "\n• Compound hazards—surge plus extreme pluvial rainfall—are modeled in isolated silos."
    p.font.size = Pt(12)
    p.font.color.rgb = TEXT_WHITE
    p = tf.add_paragraph()
    p.text = "\n• Text bulletins fail to reach vulnerable fishing hamlets once cell towers lose grid power."
    p.font.size = Pt(11.5)
    p.font.color.rgb = TEXT_MUTED

    p_card3 = add_card(s2, Inches(8.8), Inches(1.8), card_w, card_h)
    tf = p_card3.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "🚨 The Field Responder's Dilemma"
    p.font.bold = True
    p.font.size = Pt(14)
    p.font.color.rgb = ACCENT_CYAN
    p = tf.add_paragraph()
    p.text = "\n• District Magistrates (DMs) & NDRF commanders must stage rescue convoys without knowing which bridges fail first."
    p.font.size = Pt(12)
    p.font.color.rgb = TEXT_WHITE
    p = tf.add_paragraph()
    p.text = "\n• Critical questions unanswered: Will State Highway 3 submerge? Which rural clinics lose backup power?"
    p.font.size = Pt(12)
    p.font.color.rgb = TEXT_WHITE
    p = tf.add_paragraph()
    p.text = "\n• How can duty officers issue targeted, voice-based directives in local dialects before landfall?"
    p.font.size = Pt(11.5)
    p.font.color.rgb = TEXT_MUTED

    add_speaker_note(s2, (
        "India's coastal districts house over 188 million citizens according to the 2011 Census. When a cyclone develops, the India Meteorological Department provides official weather forecasts. "
        "However, a District Magistrate or State Disaster Management officer cannot deploy ambulances based solely on wind speed isobars. "
        "They need to know whether State Highway 3 will be cut off, which rural clinics may face flooding, and how to reach offline communities in their native language. That is the critical last-mile gap."
    ))

    # =========================================================================
    # SLIDE 3: Solution: 5-Stage Decision Pipeline
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    apply_slide_bg(s3)
    add_header(s3, "The Solution: 5-Stage Decision Pipeline",
               "An integrated workflow powered by Google services—from planetary data to edge alerting.")

    steps = [
        ("1. Track Ingestion", "Google BigQuery NOAA IBTrACS & IMD Bulletin Parser.\nIngest coordinates, central pressure & winds.", "BigQuery / NOAA"),
        ("2. Geospatial Hazard", "Google Earth Engine SRTM 30m DEM & Bathymetry.\nDynamic inundation & wind swath modeling.", "Earth Engine / DEM"),
        ("3. Lifeline ML", "Vertex AI-Ready Calibrated Gradient Boosting.\nForecasts road cut-offs & hospital flood risks.", "Vertex AI / ML"),
        ("4. Ground Triage", "Gemini 2.5 Flash Vision & Cloud Storage Vault.\nDamage grading decoupled from location.", "Gemini & GCS"),
        ("5. Actionable Alerts", "Google Cloud Pub/Sub & Cloud TTS in 7 Languages.\nTargeted district alerts & audio broadcasts.", "Pub/Sub & TTS")
    ]

    sw = Inches(2.25)
    sh = Inches(4.8)
    for i, (stitle, sdesc, stag) in enumerate(steps):
        scard = add_card(s3, Inches(0.8 + i * 2.4), Inches(1.8), sw, sh)
        tf = scard.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = stitle
        p.font.bold = True
        p.font.size = Pt(13)
        p.font.color.rgb = ACCENT_CYAN
        p = tf.add_paragraph()
        p.text = f"[{stag}]\n"
        p.font.size = Pt(9.5)
        p.font.bold = True
        p.font.color.rgb = ACCENT_GREEN
        p = tf.add_paragraph()
        p.text = sdesc
        p.font.size = Pt(11)
        p.font.color.rgb = TEXT_WHITE

    add_speaker_note(s3, (
        "CycloneShield structures disaster decision-making into 5 connected stages: "
        "First, storm tracks are ingested via Google BigQuery and official IMD bulletins. "
        "Second, Google Earth Engine topography powers compound surge and flood hazard screening. "
        "Third, our Vertex AI-ready predictive ML model scores road and hospital lifeline failure. "
        "Fourth, post-storm damage photos are triaged via Gemini 2.5 Flash and archived in Google Cloud Storage. "
        "Fifth, life-safety warnings are dispatched via Google Cloud Pub/Sub and broadcast via Cloud Text-to-Speech in 7 languages."
    ))

    # =========================================================================
    # SLIDE 4: Prepared Demonstration: Cyclone Remal Scenario
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    apply_slide_bg(s4)
    add_header(s4, "Prepared Demonstration: Cyclone Remal Scenario",
               "Configured multi-hazard screening outputs—turning complex data into actionable district priorities.")

    c_left = add_card(s4, Inches(0.8), Inches(1.8), Inches(4.8), Inches(4.8))
    tf = c_left.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "🎯 Scenario Highlights (Cyclone Remal)"
    p.font.bold = True
    p.font.size = Pt(14)
    p.font.color.rgb = ACCENT_CYAN
    p = tf.add_paragraph()
    p.text = "\n• Track & Wind Swath: 110 km/h landfall wind envelope modeled across South 24 Parganas and Purba Medinipur."
    p.font.size = Pt(11.5)
    p.font.color.rgb = TEXT_WHITE
    p = tf.add_paragraph()
    p.text = "\n• Coastal Sea Surge: 3.56m storm surge head calculated from 977 mb central pressure deficit."
    p.font.size = Pt(11.5)
    p.font.color.rgb = TEXT_WHITE
    p = tf.add_paragraph()
    p.text = "\n• District Prioritization: South 24 Parganas (Risk: 88.4/100, EXTREME) prioritized for 12,000-person evacuation window."
    p.font.size = Pt(11.5)
    p.font.color.rgb = TEXT_WHITE
    p = tf.add_paragraph()
    p.text = "\n• Lifeline Infrastructure: 5 rural primary health centers identified for immediate generator flood protection."
    p.font.size = Pt(11)
    p.font.color.rgb = TEXT_MUTED

    img_path1 = os.path.join(SCREENSHOTS_DIR, "01_spatial_hazard_core.png")
    if os.path.exists(img_path1):
        s4.shapes.add_picture(img_path1, Inches(5.9), Inches(1.8), Inches(6.6), Inches(4.8))
    else:
        c_right = add_card(s4, Inches(5.9), Inches(1.8), Inches(6.6), Inches(4.8))
        tf_r = c_right.text_frame
        p = tf_r.paragraphs[0]
        p.text = "[Dashboard Screenshot: outputs/screenshots/01_spatial_hazard_core.png]"
        p.font.color.rgb = TEXT_MUTED

    add_speaker_note(s4, (
        "Here you see the interactive prototype running Cyclone Remal. "
        "The system calculates a 3.56-meter storm surge from barometric pressure, maps the 110 km/h wind swath, and overlays 47 critical facilities. "
        "Instead of wading through raw numbers, the District Magistrate immediately sees that South 24 Parganas is at extreme risk (88.4) and State Highway 3 faces a 78% probability of submersion, allowing pre-emptive staging."
    ))

    # =========================================================================
    # SLIDE 5: Google Cloud & AI Architecture: 11 Connected Services
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    apply_slide_bg(s5)
    add_header(s5, "Google Cloud & AI Architecture: 11 Connected Services",
               "A resilient, enterprise-grade cloud architecture spanning perception, data, and edge alerting.")

    cw3 = Inches(3.7)
    ch3 = Inches(4.8)

    # Pillar 1: Generative AI & Perception
    c_p1 = add_card(s5, Inches(0.8), Inches(1.8), cw3, ch3, ACCENT_CYAN)
    tf1 = c_p1.text_frame
    tf1.word_wrap = True
    p = tf1.paragraphs[0]
    p.text = "🧠 Perception & GenAI"
    p.font.bold = True
    p.font.size = Pt(13.5)
    p.font.color.rgb = ACCENT_CYAN
    p = tf1.add_paragraph()
    p.text = "\n• Google Gemini 2.5 Flash:"
    p.font.size = Pt(11.5)
    p.font.bold = True
    p.font.color.rgb = TEXT_WHITE
    p = tf1.add_paragraph()
    p.text = "Multimodal visual triage of ground & drone damage photos. Grades structural severity (1-5) and identifies critical relief needs without hallucinating location."
    p.font.size = Pt(10.5)
    p.font.color.rgb = TEXT_MUTED
    p = tf1.add_paragraph()
    p.text = "\n• Google Cloud Text-to-Speech:"
    p.font.size = Pt(11.5)
    p.font.bold = True
    p.font.color.rgb = TEXT_WHITE
    p = tf1.add_paragraph()
    p.text = "High-fidelity Neural2 voice synthesis across 7 regional Indian languages (Bengali, Hindi, Odia, Telugu, Tamil, Gujarati, English) for voice-first alerts."
    p.font.size = Pt(10.5)
    p.font.color.rgb = TEXT_MUTED

    # Pillar 2: Planetary Data & Machine Learning
    c_p2 = add_card(s5, Inches(4.8), Inches(1.8), cw3, ch3, ACCENT_GREEN)
    tf2 = c_p2.text_frame
    tf2.word_wrap = True
    p = tf2.paragraphs[0]
    p.text = "🌍 Planetary Data & ML"
    p.font.bold = True
    p.font.size = Pt(13.5)
    p.font.color.rgb = ACCENT_GREEN
    p = tf2.add_paragraph()
    p.text = "\n• Google BigQuery:"
    p.font.size = Pt(11.5)
    p.font.bold = True
    p.font.color.rgb = TEXT_WHITE
    p = tf2.add_paragraph()
    p.text = "Ingests NOAA IBTrACS historical hurricane warehouse (Bay of Bengal & Arabian Sea). Built-in FinOps dry-run cost estimators safeguard cloud budgets."
    p.font.size = Pt(10.5)
    p.font.color.rgb = TEXT_MUTED
    p = tf2.add_paragraph()
    p.text = "\n• Google Earth Engine (GEE):"
    p.font.size = Pt(11.5)
    p.font.bold = True
    p.font.color.rgb = TEXT_WHITE
    p = tf2.add_paragraph()
    p.text = "Processes NASA SRTM 30m digital elevation models and coastal topography for surge inundation screening."
    p.font.size = Pt(10.5)
    p.font.color.rgb = TEXT_MUTED
    p = tf2.add_paragraph()
    p.text = "\n• Google Vertex AI (Ready):"
    p.font.size = Pt(11.5)
    p.font.bold = True
    p.font.color.rgb = TEXT_WHITE
    p = tf2.add_paragraph()
    p.text = "Model Registry deployment manifest and custom container serving specifications for lifeline risk forecasting."
    p.font.size = Pt(10.5)
    p.font.color.rgb = TEXT_MUTED

    # Pillar 3: Serverless Cloud & Real-Time Alerting
    c_p3 = add_card(s5, Inches(8.8), Inches(1.8), cw3, ch3, ACCENT_ORANGE)
    tf3 = c_p3.text_frame
    tf3.word_wrap = True
    p = tf3.paragraphs[0]
    p.text = "⚡ Serverless & Alerts"
    p.font.bold = True
    p.font.size = Pt(13.5)
    p.font.color.rgb = ACCENT_ORANGE
    p = tf3.add_paragraph()
    p.text = "\n• Google Cloud Run:"
    p.font.size = Pt(11.5)
    p.font.bold = True
    p.font.color.rgb = TEXT_WHITE
    p = tf3.add_paragraph()
    p.text = "Production containerized Streamlit command center on port 8080. Autoscales 0-to-N; native HTTPS enables Web Geolocation API."
    p.font.size = Pt(10.5)
    p.font.color.rgb = TEXT_MUTED
    p = tf3.add_paragraph()
    p.text = "\n• Google Cloud Pub/Sub:"
    p.font.size = Pt(11.5)
    p.font.bold = True
    p.font.color.rgb = TEXT_WHITE
    p = tf3.add_paragraph()
    p.text = "Event-driven disaster bus dispatching CRITICAL/HIGH alerts with district attribute filtering (e.g. attributes.district = 'Puri')."
    p.font.size = Pt(10.5)
    p.font.color.rgb = TEXT_MUTED
    p = tf3.add_paragraph()
    p.text = "\n• Cloud Storage & Secret Manager:"
    p.font.size = Pt(11.5)
    p.font.bold = True
    p.font.color.rgb = TEXT_WHITE
    p = tf3.add_paragraph()
    p.text = "Tamper-evident incident vault (gs://BUCKET/state/district/) and keyless IAM security with Cloud Build CI/CD."
    p.font.size = Pt(10.5)
    p.font.color.rgb = TEXT_MUTED

    add_speaker_note(s5, (
        "CycloneShield leverages a comprehensive suite of 11 Google Cloud services organized across three distinct pillars: "
        "Perception & Generative AI uses Gemini 2.5 Flash for multimodal visual damage triage and Cloud Text-to-Speech for voice alerts in 7 Indian languages. "
        "Planetary Data & ML utilizes BigQuery for NOAA storm tracks, Google Earth Engine for elevation models, and Vertex AI for model registry readiness. "
        "Serverless Cloud & Alerts leverages Cloud Run for autoscaling, Cloud Pub/Sub for attribute-filtered emergency alerts, Cloud Storage for incident evidence, and Secret Manager with Cloud Build for zero-trust security."
    ))

    # =========================================================================
    # SLIDE 6: Gemini 2.5 Flash & Cloud Storage: Responsible Triage
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    apply_slide_bg(s6)
    add_header(s6, "Google Gemini 2.5 Flash & Cloud Storage: Incident Triage",
               "Multimodal damage assessment with strict geospatial decoupling and tamper-evident evidence storage.")

    c_left = add_card(s6, Inches(0.8), Inches(1.8), Inches(5.2), Inches(4.8))
    tf = c_left.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "🛡️ Responsible AI: Decoupled Architecture"
    p.font.bold = True
    p.font.size = Pt(13.5)
    p.font.color.rgb = ACCENT_CYAN
    p = tf.add_paragraph()
    p.text = "\n1. Gemini 2.5 Flash Multimodal Vision:"
    p.font.size = Pt(11.5)
    p.font.bold = True
    p.font.color.rgb = TEXT_WHITE
    p = tf.add_paragraph()
    p.text = "• Evaluates damage type (culvert blowout, fallen trees, embankment breach), severity tier (1-5), and required equipment (earthmovers, dewatering pumps)."
    p.font.size = Pt(10.5)
    p.font.color.rgb = TEXT_MUTED
    p = tf.add_paragraph()
    p.text = "\n2. Anti-Hallucination Design Decision:"
    p.font.size = Pt(11.5)
    p.font.bold = True
    p.font.color.rgb = ACCENT_ORANGE
    p = tf.add_paragraph()
    p.text = "• Gemini NEVER infers location from imagery. Coordinates come strictly from EXIF GPS, browser HTML5 location, or operator point-in-polygon verification."
    p.font.size = Pt(10.5)
    p.font.color.rgb = TEXT_WHITE
    p = tf.add_paragraph()
    p.text = "\n3. Google Cloud Storage Evidence Vault:"
    p.font.size = Pt(11.5)
    p.font.bold = True
    p.font.color.rgb = ACCENT_GREEN
    p = tf.add_paragraph()
    p.text = "• Persists photo and audit JSON to gs://<BUCKET>/<state>/<district>/<incident_id>/. Unverified photos are quarantined under _unverified/."
    p.font.size = Pt(10.5)
    p.font.color.rgb = TEXT_MUTED

    img_path2 = os.path.join(SCREENSHOTS_DIR, "02_ground_damage_triage.png")
    if os.path.exists(img_path2):
        s6.shapes.add_picture(img_path2, Inches(6.3), Inches(1.8), Inches(6.2), Inches(4.8))
    else:
        c_right = add_card(s6, Inches(6.3), Inches(1.8), Inches(6.2), Inches(4.8))
        tf_r = c_right.text_frame
        p = tf_r.paragraphs[0]
        p.text = "[Drone Triage Screenshot: outputs/screenshots/02_ground_damage_triage.png]"
        p.font.color.rgb = TEXT_MUTED

    add_speaker_note(s6, (
        "In disaster management, AI hallucination costs lives. We made a deliberate engineering decision: Gemini 2.5 Flash only evaluates damage type, severity, and needed rescue machinery. "
        "It is strictly forbidden from guessing location. Coordinates are determined deterministically from EXIF metadata, browser GPS, or operator district polygon lookup. "
        "Each incident is permanently archived in Google Cloud Storage with structured JSON metadata for auditability."
    ))

    # =========================================================================
    # SLIDE 7: Google Cloud Pub/Sub & Cloud Run: Event Bus & Serverless Edge
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    apply_slide_bg(s7)
    add_header(s7, "Google Cloud Pub/Sub & Cloud Run: Alerting & Serverless Edge",
               "Low-latency, attribute-filtered disaster alerts and scalable containerized deployment.")

    c_left = add_card(s7, Inches(0.8), Inches(1.8), Inches(5.2), Inches(4.8))
    tf = c_left.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "📡 Real-Time Alert Bus & Container Edge"
    p.font.bold = True
    p.font.size = Pt(13.5)
    p.font.color.rgb = ACCENT_CYAN
    p = tf.add_paragraph()
    p.text = "\n1. Google Cloud Pub/Sub Emergency Topic:"
    p.font.size = Pt(11.5)
    p.font.bold = True
    p.font.color.rgb = TEXT_WHITE
    p = tf.add_paragraph()
    p.text = "• When damage severity is CRITICAL or HIGH, a message is published to 'cyclone-alerts' with attributes: district, state, severity, and GCS URI."
    p.font.size = Pt(10.5)
    p.font.color.rgb = TEXT_MUTED
    p = tf.add_paragraph()
    p.text = "\n2. District-Filtered Subscriptions:"
    p.font.size = Pt(11.5)
    p.font.bold = True
    p.font.color.rgb = ACCENT_GREEN
    p = tf.add_paragraph()
    p.text = "• Local duty officers subscribe with filters like attributes.district = 'Puri', receiving only relevant alerts and preventing alert fatigue."
    p.font.size = Pt(10.5)
    p.font.color.rgb = TEXT_WHITE
    p = tf.add_paragraph()
    p.text = "\n3. Google Cloud Run Serverless Deployment:"
    p.font.size = Pt(11.5)
    p.font.bold = True
    p.font.color.rgb = ACCENT_ORANGE
    p = tf.add_paragraph()
    p.text = "• Containerized Streamlit on port 8080 (Dockerfile). Autoscales 0-to-N; native HTTPS enables browser device GPS; zero-secret posture via Secret Manager."
    p.font.size = Pt(10.5)
    p.font.color.rgb = TEXT_MUTED

    img_path4 = os.path.join(SCREENSHOTS_DIR, "04_bigquery_cloudrun.png")
    if os.path.exists(img_path4):
        s7.shapes.add_picture(img_path4, Inches(6.3), Inches(1.8), Inches(6.2), Inches(4.8))
    else:
        c_right = add_card(s7, Inches(6.3), Inches(1.8), Inches(6.2), Inches(4.8))
        tf_r = c_right.text_frame
        p = tf_r.paragraphs[0]
        p.text = "[Cloud Run & BigQuery Screenshot: outputs/screenshots/04_bigquery_cloudrun.png]"
        p.font.color.rgb = TEXT_MUTED

    add_speaker_note(s7, (
        "When an incident is classified as CRITICAL or HIGH, CycloneShield automatically fires an event to Google Cloud Pub/Sub. "
        "Because each message contains district metadata, downstream responders like the Puri District Control Room can use subscription filters to receive only alerts for their jurisdiction. "
        "The entire command center runs on Google Cloud Run, scaling automatically during landfall traffic surges, while Google Cloud Build and Secret Manager provide a zero-secret deployment."
    ))

    # =========================================================================
    # SLIDE 8: Google BigQuery & Predictive ML (Vertex AI Ready)
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    apply_slide_bg(s8)
    add_header(s8, "Google BigQuery & Predictive ML: Vertex AI Blueprint",
               "Planetary historical cyclone data warehouse and calibrated lifeline vulnerability forecasting.")

    c_left = add_card(s8, Inches(0.8), Inches(1.8), Inches(5.4), Inches(4.8))
    tf = c_left.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "📊 BigQuery Data Engine & Vertex AI ML"
    p.font.bold = True
    p.font.size = Pt(13.5)
    p.font.color.rgb = ACCENT_CYAN
    p = tf.add_paragraph()
    p.text = "\n1. Google BigQuery Public NOAA Dataset:"
    p.font.size = Pt(11.5)
    p.font.bold = True
    p.font.color.rgb = TEXT_WHITE
    p = tf.add_paragraph()
    p.text = "• Connects to bigquery-public-data.noaa_hurricanes.ibtracs_all. Ingests 13 major Bay of Bengal and Arabian Sea cyclones with FinOps dry-run cost control."
    p.font.size = Pt(10.5)
    p.font.color.rgb = TEXT_MUTED
    p = tf.add_paragraph()
    p.text = "\n2. Calibrated Predictive Lifeline ML:"
    p.font.size = Pt(11.5)
    p.font.bold = True
    p.font.color.rgb = ACCENT_GREEN
    p = tf.add_paragraph()
    p.text = "• HistGradientBoosting classifier predicts Highway Submersion Cut-Off Risk and Hospital ICU Inundation (ROC-AUC > 0.975, Brier Score < 0.049)."
    p.font.size = Pt(10.5)
    p.font.color.rgb = TEXT_WHITE
    p = tf.add_paragraph()
    p.text = "\n3. Vertex AI Model Registry Specification:"
    p.font.size = Pt(11.5)
    p.font.bold = True
    p.font.color.rgb = ACCENT_ORANGE
    p = tf.add_paragraph()
    p.text = "• Serialized model artifact (lifeline_risk_model.joblib), serving schema (vertex_model_config.json), and custom container specs ready for managed cloud endpoints."
    p.font.size = Pt(10.5)
    p.font.color.rgb = TEXT_MUTED

    img_path3 = os.path.join(MODELS_DIR, "lifeline_model_evaluation.png")
    if not os.path.exists(img_path3):
        img_path3 = os.path.join(SCREENSHOTS_DIR, "03_predictive_lifeline_ml.png")

    if os.path.exists(img_path3):
        s8.shapes.add_picture(img_path3, Inches(6.5), Inches(1.8), Inches(6.0), Inches(4.8))
    else:
        c_right = add_card(s8, Inches(6.5), Inches(1.8), Inches(6.0), Inches(4.8))
        tf_r = c_right.text_frame
        p = tf_r.paragraphs[0]
        p.text = "[Model Evaluation Plot: outputs/models/lifeline_model_evaluation.png]"
        p.font.color.rgb = TEXT_MUTED

    add_speaker_note(s8, (
        "CycloneShield integrates with Google BigQuery to access NOAA's planetary hurricane database, including built-in dry-run queries to prevent unexpected costs. "
        "Our calibrated machine learning pipeline predicts arterial highway cut-offs and hospital ICU flooding with an ROC-AUC above 0.975. "
        "We've packaged this model with a complete Vertex AI Model Registry manifest and container spec, making it production-ready for deployment."
    ))

    # =========================================================================
    # SLIDE 9: Google Cloud Text-to-Speech: Voice-First in 7 Indian Languages
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    apply_slide_bg(s9)
    add_header(s9, "Google Cloud Text-to-Speech: Voice-First in 7 Languages",
               "Bridging the last-mile digital and literacy divide with high-fidelity Neural2 speech synthesis.")

    pw = Inches(3.7)
    ph = Inches(4.8)

    c_v1 = add_card(s9, Inches(0.8), Inches(1.8), pw, ph, ACCENT_CYAN)
    tf1 = c_v1.text_frame
    tf1.word_wrap = True
    p = tf1.paragraphs[0]
    p.text = "🗣️ 7 Regional Indian Languages"
    p.font.bold = True
    p.font.size = Pt(13.5)
    p.font.color.rgb = ACCENT_CYAN
    p = tf1.add_paragraph()
    p.text = "\n• Native Speech Synthesis:"
    p.font.size = Pt(11.5)
    p.font.bold = True
    p.font.color.rgb = TEXT_WHITE
    p = tf1.add_paragraph()
    p.text = "• Bengali (bn-IN, Bashkar/Neural2-A)\n• Hindi (hi-IN, Swara/Neural2-D)\n• Odia (or-IN, Cloud TTS)\n• Telugu (te-IN, Mohan/Neural2-A)\n• Tamil (ta-IN, Pallavi/Neural2-A)\n• Gujarati (gu-IN, Dhwani/Neural2-A)\n• English (en-IN, Neural2-D)"
    p.font.size = Pt(10.5)
    p.font.color.rgb = TEXT_WHITE
    p = tf1.add_paragraph()
    p.text = "\n• Top-level language switcher dynamically translates UI alerts and synthesized audio."
    p.font.size = Pt(10)
    p.font.color.rgb = TEXT_MUTED

    c_v2 = add_card(s9, Inches(4.8), Inches(1.8), pw, ph, ACCENT_GREEN)
    tf2 = c_v2.text_frame
    tf2.word_wrap = True
    p = tf2.paragraphs[0]
    p.text = "⚡ 3-Tier Synthesis Resilience"
    p.font.bold = True
    p.font.size = Pt(13.5)
    p.font.color.rgb = ACCENT_GREEN
    p = tf2.add_paragraph()
    p.text = "\n• Tier 1: Google Cloud TTS"
    p.font.size = Pt(11.5)
    p.font.bold = True
    p.font.color.rgb = TEXT_WHITE
    p = tf2.add_paragraph()
    p.text = "High-definition Neural2 natural speech with customized rate and pitch for megaphone audio."
    p.font.size = Pt(10.5)
    p.font.color.rgb = TEXT_MUTED
    p = tf2.add_paragraph()
    p.text = "\n• Tier 2: gTTS Free Fallback"
    p.font.size = Pt(11.5)
    p.font.bold = True
    p.font.color.rgb = TEXT_WHITE
    p = tf2.add_paragraph()
    p.text = "Graceful zero-cost fallback when API quotas or internet connectivity are constrained."
    p.font.size = Pt(10.5)
    p.font.color.rgb = TEXT_MUTED
    p = tf2.add_paragraph()
    p.text = "\n• Tier 3: Pre-Rendered Audio"
    p.font.size = Pt(11.5)
    p.font.bold = True
    p.font.color.rgb = TEXT_WHITE
    p = tf2.add_paragraph()
    p.text = "30 pre-rendered studio warning bulletins with emergency siren chimes ready for offline playback."
    p.font.size = Pt(10.5)
    p.font.color.rgb = TEXT_MUTED

    c_v3 = add_card(s9, Inches(8.8), Inches(1.8), pw, ph, ACCENT_ORANGE)
    tf3 = c_v3.text_frame
    tf3.word_wrap = True
    p = tf3.paragraphs[0]
    p.text = "📻 Reaching the Last Mile"
    p.font.bold = True
    p.font.size = Pt(13.5)
    p.font.color.rgb = ACCENT_ORANGE
    p = tf3.add_paragraph()
    p.text = "\n• Accessible Disaster Alerting:"
    p.font.size = Pt(11.5)
    p.font.bold = True
    p.font.color.rgb = TEXT_WHITE
    p = tf3.add_paragraph()
    p.text = "SMS text alerts fail illiterate citizens, elderly populations, and families who lose electricity."
    p.font.size = Pt(10.5)
    p.font.color.rgb = TEXT_MUTED
    p = tf3.add_paragraph()
    p.text = "\n• Direct Community Audio:"
    p.font.size = Pt(11.5)
    p.font.bold = True
    p.font.color.rgb = TEXT_WHITE
    p = tf3.add_paragraph()
    p.text = "Generates downloadable, broadcast-ready MP3s for local community radio, police loudspeaker vans, and boat siren systems."
    p.font.size = Pt(10.5)
    p.font.color.rgb = TEXT_WHITE
    p = tf3.add_paragraph()
    p.text = "\n• 1-Click Playback: Play voice alerts directly in the browser with zero external player required."
    p.font.size = Pt(10)
    p.font.color.rgb = TEXT_MUTED

    add_speaker_note(s9, (
        "During a severe cyclone, cell towers go dark, power lines snap, and text messages fail to reach vulnerable fishing hamlets. "
        "CycloneShield implements a voice-first alerting engine powered by Google Cloud Text-to-Speech, delivering lifelike Neural2 broadcasts across 7 Indian languages. "
        "With a three-tier fallback architecture—from Cloud TTS to gTTS and pre-rendered emergency broadcasts—the system ensures that life-saving warnings reach citizens even in full blackout conditions."
    ))

    # =========================================================================
    # SLIDE 10: Explainable Risk Scoring: 4-Pillar Index & What-If Simulator
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    apply_slide_bg(s10)
    add_header(s10, "Explainable Risk Scoring: 4-Pillar Index & What-If Simulator",
               "Transparent vulnerability formulation backed by an interactive meteorological simulator.")

    dims = [
        ("🏥 Healthcare Vulnerability (35%)", "Flooded hospitals, primary health centers (PHCs), ICU generator basements, and oxygen reserves.", ACCENT_RED),
        ("🛣️ Road Cut-Off Risk (25%)", "Submerged arterial routes (e.g. State Highway 3) blocking ambulance convoys and evacuation corridors.", ACCENT_ORANGE),
        ("🏕️ Shelter Deficit Risk (25%)", "Severe cyclone shelter capacity shortfall relative to vulnerable coastal population (Census 2011).", ACCENT_CYAN),
        ("⚡ Power Grid Fragility (15%)", "Inundated electrical substations and high-wind transmission feeder failure exposure.", ACCENT_GREEN)
    ]

    for i, (dtitle, ddesc, dcol) in enumerate(dims):
        col_idx = i % 2
        row_idx = i // 2
        card = add_card(s10, Inches(0.8 + col_idx * 5.9), Inches(1.8 + row_idx * 1.95), Inches(5.6), Inches(1.75))
        tf = card.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = dtitle
        p.font.bold = True
        p.font.size = Pt(13)
        p.font.color.rgb = dcol
        p = tf.add_paragraph()
        p.text = ddesc
        p.font.size = Pt(11)
        p.font.color.rgb = TEXT_WHITE

    banner = add_card(s10, Inches(0.8), Inches(5.8), Inches(11.7), Inches(1.1), ACCENT_CYAN)
    tf_b = banner.text_frame
    tf_b.word_wrap = True
    p = tf_b.paragraphs[0]
    p.text = "🔍 Dynamic 'What-If' Scenario Simulator (Tab 3):"
    p.font.bold = True
    p.font.size = Pt(11.5)
    p.font.color.rgb = ACCENT_CYAN
    p = tf_b.add_paragraph()
    p.text = "Duty officers can adjust live meteorological sliders (central pressure, wind speed, forward velocity, rainfall) to evaluate counterfactual scenarios: 'What if Remal slows down by 5 km/h?' or 'What if central pressure drops 10 mb?'"
    p.font.size = Pt(10.5)
    p.font.color.rgb = TEXT_WHITE

    add_speaker_note(s10, (
        "Unlike black-box models, CycloneShield's composite risk score is 100% transparent and explainable. "
        "It balances healthcare exposure at 35%, road severed risk at 25%, shelter deficits at 25%, and power grid vulnerability at 15%. "
        "In Tab 3 of our app, disaster managers can test 'what-if' scenarios using interactive meteorological sliders to see how an intensifying storm alters lifeline priorities in real time."
    ))

    # =========================================================================
    # SLIDE 11: Built for India: Scope vs 4-Week SDMA Pilot Plan
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    apply_slide_bg(s11)
    add_header(s11, "Built for India: Scope vs 4-Week SDMA Pilot Plan",
               "Five configured coastal state profiles and a structured 4-week rollout for state disaster authorities.")

    cw = Inches(5.6)
    ch = Inches(4.8)

    c_today = add_card(s11, Inches(0.8), Inches(1.8), cw, ch, ACCENT_GREEN)
    tf = c_today.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "🇮🇳 PAN-INDIA SCOPE TODAY"
    p.font.bold = True
    p.font.size = Pt(14)
    p.font.color.rgb = ACCENT_GREEN
    p = tf.add_paragraph()
    p.text = "\n• 5 Configured Maritime State Profiles:"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = TEXT_WHITE
    p = tf.add_paragraph()
    p.text = "West Bengal, Odisha, Andhra Pradesh, Tamil Nadu, and Gujarat covering 35 coastal districts."
    p.font.size = Pt(11)
    p.font.color.rgb = TEXT_MUTED
    p = tf.add_paragraph()
    p.text = "\n• Dynamic UTM Coordinate System:"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = TEXT_WHITE
    p = tf.add_paragraph()
    p.text = "Automatically switches projection zones (EPSG:32642 to EPSG:32645) across all 7,516 km of Indian coastline."
    p.font.size = Pt(11)
    p.font.color.rgb = TEXT_MUTED
    p = tf.add_paragraph()
    p.text = "\n• Zero-Key Evaluator Guarantee:"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = TEXT_WHITE
    p = tf.add_paragraph()
    p.text = "Functions seamlessly offline with pre-cached NOAA tracks, synthetic ML models, and audio fallbacks."
    p.font.size = Pt(11)
    p.font.color.rgb = TEXT_MUTED

    c_plan = add_card(s11, Inches(6.9), Inches(1.8), cw, ch, ACCENT_CYAN)
    tf = c_plan.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "🚀 4-WEEK SDMA PILOT BLUEPRINT"
    p.font.bold = True
    p.font.size = Pt(14)
    p.font.color.rgb = ACCENT_CYAN
    p = tf.add_paragraph()
    p.text = "\n• Week 1: State GIS Asset Onboarding"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = TEXT_WHITE
    p = tf.add_paragraph()
    p.text = "Ingest local health clinic coordinates, road shapefiles, and shelter capacities into the spatial engine."
    p.font.size = Pt(10.5)
    p.font.color.rgb = TEXT_MUTED
    p = tf.add_paragraph()
    p.text = "\n• Week 2: IMD Real-Time Feed Hookup"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = TEXT_WHITE
    p = tf.add_paragraph()
    p.text = "Connect live IMD RSMC bulletin parser and calibrate local wind swath thresholds with SEOC duty officers."
    p.font.size = Pt(10.5)
    p.font.color.rgb = TEXT_MUTED
    p = tf.add_paragraph()
    p.text = "\n• Week 3: CAP Alerting & Voice Bots"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = TEXT_WHITE
    p = tf.add_paragraph()
    p.text = "Integrate OASIS CAP v1.2 XML with NDMA Sachet portal, WhatsApp alerts, and community radio broadcasts."
    p.font.size = Pt(10.5)
    p.font.color.rgb = TEXT_MUTED
    p = tf.add_paragraph()
    p.text = "\n• Week 4: Tabletop Simulation & Review"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = TEXT_WHITE
    p = tf.add_paragraph()
    p.text = "Execute end-to-end simulated pre-landfall drill with District Emergency Operation Centers (DEOCs) and NDRF."
    p.font.size = Pt(10.5)
    p.font.color.rgb = TEXT_MUTED

    add_speaker_note(s11, (
        "CycloneShield is built specifically for India, supporting 5 maritime states with automated UTM coordinate projections. "
        "We have designed a structured 4-week pilot blueprint for State Disaster Management Authorities: "
        "starting with local GIS asset ingestion in Week 1, real-time IMD feed integration in Week 2, multi-channel alerting via CAP XML and WhatsApp in Week 3, "
        "and culminating in a full pre-landfall tabletop exercise with NDRF battalions in Week 4."
    ))

    # =========================================================================
    # SLIDE 12: Impact, Limitations, & Call to Action
    # =========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    apply_slide_bg(s12)
    add_header(s12, "Impact, Responsible AI, & Call to Action",
               "Measurable societal resilience grounded in complete technical honesty and cloud excellence.")

    cw3 = Inches(3.7)
    ch3 = Inches(4.8)

    c_imp = add_card(s12, Inches(0.8), Inches(1.8), cw3, ch3, ACCENT_GREEN)
    tf = c_imp.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "📈 Quantified Potential Impact"
    p.font.bold = True
    p.font.size = Pt(13.5)
    p.font.color.rgb = ACCENT_GREEN
    p = tf.add_paragraph()
    p.text = "\n• 188M+ Coastal Citizens:"
    p.font.size = Pt(11.5)
    p.font.bold = True
    p.font.color.rgb = TEXT_WHITE
    p = tf.add_paragraph()
    p.text = "Decision support framework covering 35 vulnerable coastal districts across 5 maritime states."
    p.font.size = Pt(10.5)
    p.font.color.rgb = TEXT_MUTED
    p = tf.add_paragraph()
    p.text = "\n• Pre-Emptive Evacuation Window:"
    p.font.size = Pt(11.5)
    p.font.bold = True
    p.font.color.rgb = TEXT_WHITE
    p = tf.add_paragraph()
    p.text = "Identifies high-risk submersion corridors 24-48 hours before landfall to stage emergency convoys."
    p.font.size = Pt(10.5)
    p.font.color.rgb = TEXT_MUTED
    p = tf.add_paragraph()
    p.text = "\n• Critical Hospital Continuity:"
    p.font.size = Pt(11.5)
    p.font.bold = True
    p.font.color.rgb = TEXT_WHITE
    p = tf.add_paragraph()
    p.text = "Early alert for backup generator flood barriers protects patient ICUs and oxygen supplies."
    p.font.size = Pt(10.5)
    p.font.color.rgb = TEXT_MUTED

    c_lim = add_card(s12, Inches(4.8), Inches(1.8), cw3, ch3, ACCENT_RED)
    tf = c_lim.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "⚠️ Responsible AI Disclosures"
    p.font.bold = True
    p.font.size = Pt(13.5)
    p.font.color.rgb = ACCENT_RED
    p = tf.add_paragraph()
    p.text = "\n• Bathymetric Surge Model:"
    p.font.size = Pt(11.5)
    p.font.bold = True
    p.font.color.rgb = TEXT_WHITE
    p = tf.add_paragraph()
    p.text = "Empirical bathtub screening model based on SRTM 30m DEM; does not yet capture dynamic astronomical tidal harmonics."
    p.font.size = Pt(10.5)
    p.font.color.rgb = TEXT_MUTED
    p = tf.add_paragraph()
    p.text = "\n• Synthetic Physics ML Training:"
    p.font.size = Pt(11.5)
    p.font.bold = True
    p.font.color.rgb = TEXT_WHITE
    p = tf.add_paragraph()
    p.text = "Predictive model trained on 3,600 physics-simulated disaster scenarios; real-world NDRF damage log benchmarking is next."
    p.font.size = Pt(10.5)
    p.font.color.rgb = TEXT_MUTED
    p = tf.add_paragraph()
    p.text = "\n• Human-in-the-Loop Safeguard:"
    p.font.size = Pt(11.5)
    p.font.bold = True
    p.font.color.rgb = TEXT_WHITE
    p = tf.add_paragraph()
    p.text = "All AI-generated advisories and triage results require authorized human officer verification before public alert dispatch."
    p.font.size = Pt(10.5)
    p.font.color.rgb = TEXT_MUTED

    c_cta = add_card(s12, Inches(8.8), Inches(1.8), cw3, ch3, ACCENT_CYAN)
    tf = c_cta.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "🔗 Live Artifacts & Call to Action"
    p.font.bold = True
    p.font.size = Pt(13.5)
    p.font.color.rgb = ACCENT_CYAN
    p = tf.add_paragraph()
    p.text = "\n🌐 Live Streamlit Command Center:"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = TEXT_WHITE
    p = tf.add_paragraph()
    p.text = "cycloneshield-vawrqbhtbgu8i6cafhbf3q.streamlit.app"
    p.font.size = Pt(9.5)
    p.font.color.rgb = ACCENT_CYAN
    p = tf.add_paragraph()
    p.text = "\n📂 Open Source Repository:"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = TEXT_WHITE
    p = tf.add_paragraph()
    p.text = "github.com/itsme-sherlock/CycloneShield"
    p.font.size = Pt(9.5)
    p.font.color.rgb = ACCENT_CYAN
    p = tf.add_paragraph()
    p.text = "\n📓 1-Click Reproducible Colab:"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = TEXT_WHITE
    p = tf.add_paragraph()
    p.text = "CycloneShield_Colab.ipynb"
    p.font.size = Pt(9.5)
    p.font.color.rgb = ACCENT_CYAN
    p = tf.add_paragraph()
    p.text = "\n🤝 The Ask: Partner with us to pilot CycloneShield with state disaster management authorities."
    p.font.size = Pt(10.5)
    p.font.bold = True
    p.font.color.rgb = ACCENT_GREEN

    add_speaker_note(s12, (
        "CycloneShield demonstrates how Google Cloud and AI technologies can solve the hardest last-mile challenges in disaster resilience. "
        "We are honest about our current limitations: our surge model uses bathtub elevation screening, and our ML models are trained on simulated physics awaiting field damage calibration. "
        "All code, container configs, and Colab notebooks are open and reproducible. We invite you to test our live prototype and partner with us on an SDMA pilot. Thank you."
    ))

    # Save presentation
    prs.save(OUTPUT_PPTX)
    print(f"Presentation successfully created at {OUTPUT_PPTX}")

if __name__ == "__main__":
    build_deck()
