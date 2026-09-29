"""
CycloneShield - 12-Slide Pitch Deck Generator
Builds a high-impact, clean, 16:9 widescreen presentation using python-pptx.
Grounded strictly in repo reality and verified facts.
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
    # Category tag
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

    # Main takeaway title
    title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.75), Inches(11.7), Inches(0.9))
    tf_title = title_box.text_frame
    tf_title.word_wrap = True
    tf_title.margin_left = tf_title.margin_right = tf_title.margin_top = tf_title.margin_bottom = 0
    p_title = tf_title.paragraphs[0]
    p_title.text = title
    p_title.font.size = Pt(22)
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
    # SLIDE 1: Title + Core Promise + Live Demo
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    apply_slide_bg(s1)

    # Accent pill
    pill = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.0), Inches(4.5), Inches(0.45))
    pill.fill.solid()
    pill.fill.fore_color.rgb = CARD_BG
    pill.line.color.rgb = ACCENT_CYAN
    p = pill.text_frame.paragraphs[0]
    p.text = "GOOGLE AI HACKATHON • DISASTER RESILIENCE"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = ACCENT_CYAN
    p.alignment = PP_ALIGN.CENTER

    # Title & Subtitle
    t_box = s1.shapes.add_textbox(Inches(0.8), Inches(1.7), Inches(11.7), Inches(2.2))
    tf = t_box.text_frame
    tf.word_wrap = True
    p1 = tf.paragraphs[0]
    p1.text = "CycloneShield"
    p1.font.size = Pt(44)
    p1.font.bold = True
    p1.font.color.rgb = TEXT_WHITE
    p1.font.name = "Arial"

    p2 = tf.add_paragraph()
    p2.text = "Predicting Cut-Off Evacuation Roads & Flooded Lifelines 48 Hours Before Landfall"
    p2.font.size = Pt(20)
    p2.font.bold = True
    p2.font.color.rgb = ACCENT_CYAN
    p2.font.name = "Arial"

    p3 = tf.add_paragraph()
    p3.text = "A district-level operational decision layer that converts cyclone tracks into specific infrastructure intelligence."
    p3.font.size = Pt(14)
    p3.font.color.rgb = TEXT_MUTED
    p3.font.name = "Arial"

    # 3 Info Cards at bottom
    c1 = add_card(s1, Inches(0.8), Inches(4.3), Inches(3.6), Inches(2.3), ACCENT_CYAN)
    tf1 = c1.text_frame
    tf1.word_wrap = True
    p = tf1.paragraphs[0]
    p.text = "🌐 LIVE WORKING DEMO"
    p.font.bold = True
    p.font.size = Pt(12)
    p.font.color.rgb = ACCENT_CYAN
    p = tf1.add_paragraph()
    p.text = "cycloneshield-vawrqbhtbgu8i6cafhbf3q.streamlit.app"
    p.font.size = Pt(11)
    p.font.color.rgb = TEXT_WHITE
    p = tf1.add_paragraph()
    p.text = "Interactive Command Center with full spatial hazard and district ranking."
    p.font.size = Pt(10)
    p.font.color.rgb = TEXT_MUTED

    c2 = add_card(s1, Inches(4.7), Inches(4.3), Inches(3.6), Inches(2.3), BORDER_COLOR)
    tf2 = c2.text_frame
    tf2.word_wrap = True
    p = tf2.paragraphs[0]
    p.text = "📂 OPEN REPOSITORY"
    p.font.bold = True
    p.font.size = Pt(12)
    p.font.color.rgb = ACCENT_CYAN
    p = tf2.add_paragraph()
    p.text = "github.com/itsme-sherlock/CycloneShield"
    p.font.size = Pt(11)
    p.font.color.rgb = TEXT_WHITE
    p = tf2.add_paragraph()
    p.text = "Full pipeline code, Jupyter Colab notebook, and reproducible ML benchmarks."
    p.font.size = Pt(10)
    p.font.color.rgb = TEXT_MUTED

    c3 = add_card(s1, Inches(8.6), Inches(4.3), Inches(3.9), Inches(2.3), BORDER_COLOR)
    tf3 = c3.text_frame
    tf3.word_wrap = True
    p = tf3.paragraphs[0]
    p.text = "👥 TEAM & EVENT"
    p.font.bold = True
    p.font.size = Pt(12)
    p.font.color.rgb = ACCENT_CYAN
    p = tf3.add_paragraph()
    p.text = "Team: [TEAM NAME: TO VERIFY]"
    p.font.size = Pt(11)
    p.font.color.rgb = TEXT_WHITE
    p = tf3.add_paragraph()
    p.text = "Members: [TEAM MEMBERS: TO VERIFY]\nEvent: [HACKATHON NAME: TO VERIFY]"
    p.font.size = Pt(10)
    p.font.color.rgb = TEXT_MUTED

    add_speaker_note(s1, (
        "Good morning, judges. When a tropical cyclone forms in the Bay of Bengal, meteorologists can track where it is headed. "
        "However, district authorities still face a critical blind spot: which state highways will submerge, and which hospitals will lose power? "
        "CycloneShield bridges this last-mile gap by converting raw storm forecasts into specific, lifeline-level infrastructure risk predictions 48 hours before landfall."
    ))

    # =========================================================================
    # SLIDE 2: Problem: The Last-Mile Gap
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    apply_slide_bg(s2)
    add_header(s2, "The Problem: The Last-Mile Operational Gap",
               "Weather forecasts track the storm, but field teams still lack road and hospital impact data.")

    # 3 Problem Cards
    card_w = Inches(3.7)
    card_h = Inches(4.8)

    p_card1 = add_card(s2, Inches(0.8), Inches(1.8), card_w, card_h)
    tf = p_card1.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "🌊 Coastal Scale & Risk"
    p.font.bold = True
    p.font.size = Pt(15)
    p.font.color.rgb = ACCENT_ORANGE
    p = tf.add_paragraph()
    p.text = "\n• 188M+ coastal citizens live across India's coastal districts (Census 2011)."
    p.font.size = Pt(12.5)
    p.font.color.rgb = TEXT_WHITE
    p = tf.add_paragraph()
    p.text = "\n• ~250M people reside within 50 km of the coast (UNDP/NDMA Studies)."
    p.font.size = Pt(12.5)
    p.font.color.rgb = TEXT_WHITE
    p = tf.add_paragraph()
    p.text = "\n• The Bay of Bengal historically accounts for severe surge mortality due to shallow coastal deltas."
    p.font.size = Pt(12)
    p.font.color.rgb = TEXT_MUTED

    p_card2 = add_card(s2, Inches(4.8), Inches(1.8), card_w, card_h)
    tf = p_card2.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "📡 The Information Disconnect"
    p.font.bold = True
    p.font.size = Pt(15)
    p.font.color.rgb = ACCENT_RED
    p = tf.add_paragraph()
    p.text = "\n• Synoptic warnings provide wind speeds and isobar tracks, not road cut-offs."
    p.font.size = Pt(12.5)
    p.font.color.rgb = TEXT_WHITE
    p = tf.add_paragraph()
    p.text = "\n• Compound hazards—surge plus pluvial rain—are computed in separate silos."
    p.font.size = Pt(12.5)
    p.font.color.rgb = TEXT_WHITE
    p = tf.add_paragraph()
    p.text = "\n• Text bulletins fail to reach fishing hamlets once cell towers lose grid power."
    p.font.size = Pt(12)
    p.font.color.rgb = TEXT_MUTED

    p_card3 = add_card(s2, Inches(8.8), Inches(1.8), card_w, card_h)
    tf = p_card3.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "🚨 The Field Responder's Dilemma"
    p.font.bold = True
    p.font.size = Pt(15)
    p.font.color.rgb = ACCENT_CYAN
    p = tf.add_paragraph()
    p.text = "\n• District Magistrate (DM) / SDMA Duty Officer must stage rescue boats blindly."
    p.font.size = Pt(12.5)
    p.font.color.rgb = TEXT_WHITE
    p = tf.add_paragraph()
    p.text = "\n• Critical questions unanswered: Will State Highway 3 remain passable for ambulances?"
    p.font.size = Pt(12.5)
    p.font.color.rgb = TEXT_WHITE
    p = tf.add_paragraph()
    p.text = "\n• Which primary health centers will lose basement power before landfall?"
    p.font.size = Pt(12)
    p.font.color.rgb = TEXT_MUTED

    add_speaker_note(s2, (
        "India's coastal districts house over 188 million citizens according to the 2011 Census. When a cyclone develops, the India Meteorological Department provides accurate weather forecasts. "
        "However, a District Magistrate or State Disaster Management officer cannot deploy ambulances based solely on wind speed isobars. "
        "They need to know if State Highway 3 will be cut off, whether rural clinics will flood, and how to broadcast alerts when cell networks fail. That is the critical last-mile operational gap."
    ))

    # =========================================================================
    # SLIDE 3: Solution: 5-Step Flow
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    apply_slide_bg(s3)
    add_header(s3, "The Solution: End-to-End Decision Pipeline",
               "CycloneShield converts raw track forecasts into field directives through five automated steps.")

    steps = [
        ("1. Ingest Track", "NOAA IBTrACS live ingest (IMD-compatible format planned).\nWind, pressure, position.", "[Real data]"),
        ("2. Compute Hazards", "Hydrodynamic surge formula + 30m SRTM satellite elevation.\nCoastal bathtub flood zone.", "[Real data]"),
        ("3. Intersect Lifelines", "Spatial overlay against OpenStreetMap:\nState highways, hospitals, and relief shelters.", "[Real data]"),
        ("4. Explainable Scoring", "Transparent 0–100 district vulnerability score.\nIdentifies primary local risk drivers.", "[Simulated risk]"),
        ("5. Google AI Action", "Gemini operational advisories & trilingual broadcast audio.\nEnglish, Hindi, and Bengali.", "[Live / Cached]")
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
        p.text = f"{stag}\n"
        p.font.size = Pt(9.5)
        p.font.bold = True
        p.font.color.rgb = ACCENT_ORANGE if "Simulated" in stag else (ACCENT_GREEN if "Real" in stag else ACCENT_CYAN)
        p = tf.add_paragraph()
        p.text = sdesc
        p.font.size = Pt(11)
        p.font.color.rgb = TEXT_WHITE

    add_speaker_note(s3, (
        "CycloneShield operates as an end-to-end decision pipeline in five automated steps. "
        "First, it ingests storm coordinates and central pressure. Second, it models coastal storm surge against 30-meter satellite elevation data. "
        "Third, it spatially intersects predicted flood zones with OpenStreetMap lifelines. "
        "Fourth, it scores district vulnerability from 0 to 100 with clear explainability. "
        "Finally, Google Gemini generates operational field directives and multilingual broadcast alerts."
    ))

    # =========================================================================
    # SLIDE 4: Live Prototype: Cyclone Remal End-to-End
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    apply_slide_bg(s4)
    add_header(s4, "Live Working Prototype: Cyclone Remal Scenario",
               "Tested end-to-end on Cyclone Remal across the Bengal delta in the live deployed app.")

    # Left: 3 concise bullet cards
    c_left = add_card(s4, Inches(0.8), Inches(1.8), Inches(4.8), Inches(4.8))
    tf = c_left.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "🎯 Operational Highlights (Remal Scenario)"
    p.font.bold = True
    p.font.size = Pt(14)
    p.font.color.rgb = ACCENT_CYAN
    p = tf.add_paragraph()
    p.text = "\n• 39.6 km Exposed Highways: Pinpointed critical submersion along State Highway 3 [Real OSM data]."
    p.font.size = Pt(11.5)
    p.font.color.rgb = TEXT_WHITE
    p = tf.add_paragraph()
    p.text = "\n• 5 Clinics at Risk: Flagged 5 high-risk health facilities out of 47 evaluated along the coastal belt [Simulated risk]."
    p.font.size = Pt(11.5)
    p.font.color.rgb = TEXT_WHITE
    p = tf.add_paragraph()
    p.text = "\n• South 24 Parganas Ranked #1: Priority 1 evacuation tier (Vulnerability: 82.4/100; Population: ~8.16M, Census 2011)."
    p.font.size = Pt(11.5)
    p.font.color.rgb = TEXT_WHITE
    p = tf.add_paragraph()
    p.text = "\n• Rapid Execution: Full spatial hazard mapping and scoring executes in seconds."
    p.font.size = Pt(11)
    p.font.color.rgb = TEXT_MUTED

    # Right: Dashboard Screenshot
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
        "Here is our working prototype executing on Cyclone Remal. In the Bengal delta, CycloneShield evaluated 47 coastal health facilities and flagged 5 at critical inundation risk. "
        "It identified exactly 39.6 kilometers of cut-off roadway along the State Highway 3 corridor, and ranked South 24 Parganas as Priority 1 for immediate asset staging. "
        "The live application is running online today, proving the end-to-end concept works."
    ))

    # =========================================================================
    # SLIDE 5: Google AI at Work
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    apply_slide_bg(s5)
    add_header(s5, "Google AI at Work: Multimodal Intelligence",
               "Google AI bridges raw data into plain-language directives and aerial damage triage.")

    # Left: 3 short bullets
    c_left = add_card(s5, Inches(0.8), Inches(1.8), Inches(5.2), Inches(4.8))
    tf = c_left.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "🤖 Three Google AI Integrations"
    p.font.bold = True
    p.font.size = Pt(14)
    p.font.color.rgb = ACCENT_CYAN
    p = tf.add_paragraph()
    p.text = "\n1. Gemini 1.5 Pro Advisories [Live]: Generates district-specific resource staging recommendations for SDRF and medical officers."
    p.font.size = Pt(11.5)
    p.font.color.rgb = TEXT_WHITE
    p = tf.add_paragraph()
    p.text = "\n2. Gemini Multimodal Vision [Live Prototype]: Triages post-landfall drone photos to detect breached embankments and flooded roadways."
    p.font.size = Pt(11.5)
    p.font.color.rgb = TEXT_WHITE
    p = tf.add_paragraph()
    p.text = "\n3. Multilingual Speech [30 Cached Clips]: Google Cloud TTS & gTTS pipeline delivers spoken radio alerts in Bengali, Hindi, & English."
    p.font.size = Pt(11.5)
    p.font.color.rgb = TEXT_WHITE
    p = tf.add_paragraph()
    p.text = "\nWithout AI: Responders face raw coordinate tables, English-only text PDFs, and manual photo inspection bottlenecks."
    p.font.size = Pt(11)
    p.font.color.rgb = ACCENT_ORANGE

    # Right: Multimodal Damage Triage Image
    img_path2 = os.path.join(SCREENSHOTS_DIR, "02_ground_damage_triage.png")
    if os.path.exists(img_path2):
        s5.shapes.add_picture(img_path2, Inches(6.3), Inches(1.8), Inches(6.2), Inches(4.8))
    else:
        c_right = add_card(s5, Inches(6.3), Inches(1.8), Inches(6.2), Inches(4.8))
        tf_r = c_right.text_frame
        p = tf_r.paragraphs[0]
        p.text = "[Drone Triage Screenshot: outputs/screenshots/02_ground_damage_triage.png]"
        p.font.color.rgb = TEXT_MUTED

    add_speaker_note(s5, (
        "We harness Google AI across three distinct operational layers. Gemini 1.5 Pro synthesizes complex geospatial data into plain-language field directives for emergency managers. "
        "Gemini Vision triages post-disaster drone imagery in real-time to detect breached embankments. "
        "And our multilingual voice architecture ensures spoken warnings reach vulnerable communities in Bengali and Hindi over battery-powered radios."
    ))

    # =========================================================================
    # SLIDE 6: Explainable Risk Score
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    apply_slide_bg(s6)
    add_header(s6, "Explainable Risk Scoring: Built for Field Trust",
               "A transparent 0–100 composite score that tells duty officers exactly why a district is at risk.")

    # 4 Dimension cards
    dims = [
        ("🏥 Healthcare Vulnerability (35%)", "Flooded hospitals, primary health centers (PHCs), and loss of backup generator power.", ACCENT_RED),
        ("🛣️ Road Cut-Off Risk (25%)", "Submerged arterial routes (e.g. SH-3) blocking ambulance and evacuation convoys.", ACCENT_ORANGE),
        ("🏕️ Shelter Deficit Risk (25%)", "Severe cyclone shelter capacity shortfall relative to vulnerable coastal population.", ACCENT_CYAN),
        ("⚡ Power Grid Fragility (15%)", "Inundated electrical substations and high-wind feeder line failure exposure.", ACCENT_GREEN)
    ]

    for i, (dtitle, ddesc, dcol) in enumerate(dims):
        col_idx = i % 2
        row_idx = i // 2
        card = add_card(s6, Inches(0.8 + col_idx * 5.9), Inches(1.8 + row_idx * 2.1), Inches(5.6), Inches(1.8))
        tf = card.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = dtitle
        p.font.bold = True
        p.font.size = Pt(13)
        p.font.color.rgb = dcol
        p = tf.add_paragraph()
        p.text = ddesc
        p.font.size = Pt(11.5)
        p.font.color.rgb = TEXT_WHITE

    # Bottom summary banner
    banner = add_card(s6, Inches(0.8), Inches(6.0), Inches(11.7), Inches(0.85), ACCENT_CYAN)
    tf_b = banner.text_frame
    tf_b.word_wrap = True
    p = tf_b.paragraphs[0]
    p.text = "🔍 Audit-Ready Transparency: Composite Score = [Base Lifelines] × [Hazard Multiplier]"
    p.font.bold = True
    p.font.size = Pt(11.5)
    p.font.color.rgb = ACCENT_CYAN
    p = tf_b.add_paragraph()
    p.text = "Every district score decomposes into a plain-language explanation, eliminating black-box distrust during emergency evacuations."
    p.font.size = Pt(10.5)
    p.font.color.rgb = TEXT_MUTED

    add_speaker_note(s6, (
        "In life-or-death emergency operations, black-box AI cannot be trusted. Our 0 to 100 vulnerability score is completely transparent. "
        "It weights four critical lifelines: healthcare facilities at 35%, road severance at 25%, shelter deficits at 25%, and power substations at 15%. "
        "Duty officers see not just a number, but the exact primary driver behind it, allowing them to justify evacuation orders with confidence."
    ))

    # =========================================================================
    # SLIDE 7: Predictive ML & Validation (Honest Version)
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    apply_slide_bg(s7)
    add_header(s7, "Predictive ML & Validation: Honest Methodology",
               "Calibrated Gradient Boosting predicts lifeline failure risks ahead of landfall.")

    # Left: ML Details Card
    c_left = add_card(s7, Inches(0.8), Inches(1.8), Inches(5.4), Inches(4.8))
    tf = c_left.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "📊 Model Architecture & Results"
    p.font.bold = True
    p.font.size = Pt(13.5)
    p.font.color.rgb = ACCENT_CYAN
    p = tf.add_paragraph()
    p.text = "\n• Targets: Highway Submersion Cut-Off Risk & Hospital Inundation Risk."
    p.font.size = Pt(11)
    p.font.color.rgb = TEXT_WHITE
    p = tf.add_paragraph()
    p.text = "\n• Internal Consistency Metrics [Simulated Dataset, n=3,600]:\n  - Highway Cut-Off: ROC-AUC 0.9739 | PR-AUC 0.9042 | Brier 0.0497\n  - Hospital Inundation: ROC-AUC 0.9758 | PR-AUC 0.8877 | Brier 0.0457"
    p.font.size = Pt(11)
    p.font.color.rgb = TEXT_WHITE
    p = tf.add_paragraph()
    p.text = "\n• Methodology: Stratified random 80/20 train/test split. Pre-split scaling and Platt probability calibration."
    p.font.size = Pt(10.5)
    p.font.color.rgb = TEXT_MUTED
    p = tf.add_paragraph()
    p.text = "\n• Next Validation Steps: Leave-one-storm-out cross-validation and empirical benchmarking against observed NDRF post-disaster damage logs."
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = ACCENT_ORANGE

    # Right: ML Evaluation Plot
    img_path3 = os.path.join(MODELS_DIR, "lifeline_model_evaluation.png")
    if not os.path.exists(img_path3):
        img_path3 = os.path.join(SCREENSHOTS_DIR, "03_predictive_lifeline_ml.png")

    if os.path.exists(img_path3):
        s7.shapes.add_picture(img_path3, Inches(6.5), Inches(1.8), Inches(6.0), Inches(4.8))
    else:
        c_right = add_card(s7, Inches(6.5), Inches(1.8), Inches(6.0), Inches(4.8))
        tf_r = c_right.text_frame
        p = tf_r.paragraphs[0]
        p.text = "[Model Evaluation Plot: outputs/models/lifeline_model_evaluation.png]"
        p.font.color.rgb = TEXT_MUTED

    add_speaker_note(s7, (
        "To forecast lifeline failures before landfall, we developed Calibrated Gradient Boosting models. "
        "On our physically calibrated dataset of 3,600 coastal records, the models achieved strong internal consistency, with ROC-AUCs exceeding 0.97. "
        "Crucially, we must be completely honest: these labels are physics-simulated, not historical damage logs. "
        "Our immediate next engineering step is leave-one-storm-out cross-validation against verified post-disaster field damage reports."
    ))

    # =========================================================================
    # SLIDE 8: Who It Serves: Three Personas
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    apply_slide_bg(s8)
    add_header(s8, "Who It Serves: Actionable Decisions by Persona",
               "Delivering the exact operational decision each disaster responder needs to make differently.")

    personas = [
        ("🚒 NDRF / SDRF Battalions", "Pre-stage Rescue Assets Ahead of Time",
         "• Stages inflatable rescue boats and tree-clearing saws along unflooded bypass routes.\n• Avoids deploying heavy convoys into doomed bottlenecks on State Highway 3.\n• Decision impact: Zero stranded rescue vehicles; faster post-landfall access.",
         ACCENT_ORANGE),
        ("🏛️ District Magistrates & SDMA", "Targeted Evacuation & Medical Protection",
         "• Orders prioritized village evacuations in South 24 Parganas 24 hours earlier.\n• Protects rural PHC backup generators and moves ICUs to elevated structures.\n• Decision impact: Proactive resource allocation instead of reactive triage.",
         ACCENT_CYAN),
        ("📻 Coastal Delta Communities", "Life-Saving Warnings in Mother Tongue",
         "• Listens to clear, localized voice bulletins in Bengali and Hindi on battery radios.\n• Receives specific guidance on which local high-ground cyclone shelters have space.\n• Decision impact: Actionable evacuation for non-English, low-literacy citizens.",
         ACCENT_GREEN)
    ]

    pw = Inches(3.7)
    ph = Inches(4.8)
    for i, (pname, psub, pbody, pcolor) in enumerate(personas):
        card = add_card(s8, Inches(0.8 + i * 4.0), Inches(1.8), pw, ph)
        tf = card.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = pname
        p.font.bold = True
        p.font.size = Pt(14)
        p.font.color.rgb = pcolor
        p = tf.add_paragraph()
        p.text = f"{psub}\n"
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = TEXT_WHITE
        p = tf.add_paragraph()
        p.text = pbody
        p.font.size = Pt(11)
        p.font.color.rgb = TEXT_MUTED

    add_speaker_note(s8, (
        "CycloneShield delivers distinct decisions for three key stakeholders. "
        "NDRF rescue battalions pre-stage inflatable boats outside predicted inundation zones. "
        "District Magistrates order targeted evacuations and protect vulnerable hospital backup generators 24 hours earlier. "
        "And coastal fishing communities receive clear spoken advisories in Bengali and Hindi over battery-powered radios."
    ))

    # =========================================================================
    # SLIDE 9: Built for India: Current vs Planned
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    apply_slide_bg(s9)
    add_header(s9, "Built for India: Operational Scope vs Roadmap",
               "Tested in West Bengal today, architected to scale across all 13 coastal states and UTs.")

    # Two clear comparison cards
    cw = Inches(5.6)
    ch = Inches(4.8)

    # Left: Operational Today
    c_today = add_card(s9, Inches(0.8), Inches(1.8), cw, ch, ACCENT_GREEN)
    tf = c_today.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "✅ OPERATIONAL TODAY (TESTED)"
    p.font.bold = True
    p.font.size = Pt(14)
    p.font.color.rgb = ACCENT_GREEN
    p = tf.add_paragraph()
    p.text = "\n• Active Storm Scenario: Cyclone Remal (May 2024) fully operational end-to-end; Dana & Yaas tracks ingested [Dana/Yaas app UI to verify]."
    p.font.size = Pt(11.5)
    p.font.color.rgb = TEXT_WHITE
    p = tf.add_paragraph()
    p.text = "\n• Operational Geography: West Bengal coastal districts (South 24 Parganas, Purba Medinipur); cross-border Satkhira as regional context."
    p.font.size = Pt(11.5)
    p.font.color.rgb = TEXT_WHITE
    p = tf.add_paragraph()
    p.text = "\n• Working Languages: English, Hindi, and Bengali (30 cached broadcast audio alert files in repo)."
    p.font.size = Pt(11.5)
    p.font.color.rgb = TEXT_WHITE
    p = tf.add_paragraph()
    p.text = "\n• Live Ingestion: NOAA IBTrACS v4 North Indian Ocean dataset."
    p.font.size = Pt(11)
    p.font.color.rgb = TEXT_MUTED

    # Right: Planned Expansion
    c_plan = add_card(s9, Inches(6.9), Inches(1.8), cw, ch, ACCENT_CYAN)
    tf = c_plan.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "🚀 PLANNED PAN-INDIA EXPANSION"
    p.font.bold = True
    p.font.size = Pt(14)
    p.font.color.rgb = ACCENT_CYAN
    p = tf.add_paragraph()
    p.text = "\n• Regional States (Phase 2): Odisha, Andhra Pradesh, Tamil Nadu, Kerala, Maharashtra, and Gujarat."
    p.font.size = Pt(11.5)
    p.font.color.rgb = TEXT_WHITE
    p = tf.add_paragraph()
    p.text = "\n• Multilingual Extension: Spoken audio in Odia, Telugu, Tamil, Malayalam, and Marathi."
    p.font.size = Pt(11.5)
    p.font.color.rgb = TEXT_WHITE
    p = tf.add_paragraph()
    p.text = "\n• Official Data Feeds: Direct IMD cyclone bulletin API ingestion (IMD-compatible schema ready)."
    p.font.size = Pt(11.5)
    p.font.color.rgb = TEXT_WHITE
    p = tf.add_paragraph()
    p.text = "\n• Core Scalability: Standard GeoPandas geospatial projection (EPSG:3857/4326) covers all 7,516 km of Indian coastline."
    p.font.size = Pt(11)
    p.font.color.rgb = TEXT_MUTED

    add_speaker_note(s9, (
        "CycloneShield is proven today on Cyclone Remal across West Bengal's coastal districts, with full trilingual audio in English, Hindi, and Bengali. "
        "Because our architecture uses global satellite elevation and open-source infrastructure grids, scaling to Odisha, Andhra Pradesh, and Gujarat requires configuring state boundary polygons and regional language TTS. "
        "Expanding to all thirteen coastal states and integrating direct IMD feeds forms our immediate Phase 2 roadmap."
    ))

    # =========================================================================
    # SLIDE 10: Deployability: 4-Week SDMA Pilot
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    apply_slide_bg(s10)
    add_header(s10, "Deployability: A 4-Week State Authority Pilot",
               "A non-disruptive pilot plan designed to integrate alongside existing SDMA workflows.")

    weeks = [
        ("Week 1: Data Integration", "• Ingest state GIS layers: PHC locations, district roads, shelter capacities.\n• Configure state-specific boundary polygons.\n• Operator: SDMA GIS cell with 1 data engineer."),
        ("Week 2: IMD Feed Hookup", "• Connect IMD bulletin ingestion parser.\n• Validate real-time wind swath contours against IMD warning zones.\n• Operator: State Emergency Operations Centre (SEOC)."),
        ("Week 3: Alert Channels", "• Connect Common Alerting Protocol (CAP) XML export.\n• Setup WhatsApp bot for district duty officers.\n• Pre-cache regional audio alerts for community radio."),
        ("Week 4: Tabletop Exercise", "• Simulate historical storm scenario with NDRF/SDRF officers.\n• Measure end-to-end dispatch timeline.\n• Finalize standard operating procedure (SOP).")
    ]

    ww = Inches(2.7)
    wh = Inches(3.6)
    for i, (wtitle, wdesc) in enumerate(weeks):
        card = add_card(s10, Inches(0.8 + i * 2.95), Inches(1.8), ww, wh)
        tf = card.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = wtitle
        p.font.bold = True
        p.font.size = Pt(12.5)
        p.font.color.rgb = ACCENT_CYAN
        p = tf.add_paragraph()
        p.text = f"\n{wdesc}"
        p.font.size = Pt(10.5)
        p.font.color.rgb = TEXT_WHITE

    # Bottom Cost & Licensing note card
    cost_card = add_card(s10, Inches(0.8), Inches(5.7), Inches(11.7), Inches(1.1), BORDER_COLOR)
    tf_c = cost_card.text_frame
    tf_c.word_wrap = True
    p = tf_c.paragraphs[0]
    p.text = "💰 Cost & Licensing Note"
    p.font.bold = True
    p.font.size = Pt(11)
    p.font.color.rgb = ACCENT_ORANGE
    p = tf_c.add_paragraph()
    p.text = "• Prototype runs within Google Cloud free-tier quotas during testing.\n• Production SDMA deployment utilizes low-cost serverless container hosting (Cloud Run / Vertex AI spec); production Earth Engine requires commercial licensing."
    p.font.size = Pt(10)
    p.font.color.rgb = TEXT_MUTED

    add_speaker_note(s10, (
        "We do not ask disaster authorities to overhaul their existing operations. "
        "We propose a practical four-week pilot with a State Disaster Management Authority. "
        "In weeks one and two, we ingest state GIS assets and connect bulletin feeds. "
        "In weeks three and four, we link Common Alerting Protocol feeds and run a tabletop exercise with NDRF commanders. "
        "The prototype runs serverless and incurs minimal compute overhead during readiness."
    ))

    # =========================================================================
    # SLIDE 11: Impact, Limitations, and Roadmap
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    apply_slide_bg(s11)
    add_header(s11, "Impact, Limitations, & Technical Roadmap",
               "Credible disaster impact demands absolute transparency about technical boundaries.")

    cw3 = Inches(3.7)
    ch3 = Inches(4.8)

    # Col 1: Quantified Potential Impact
    c_imp = add_card(s11, Inches(0.8), Inches(1.8), cw3, ch3, ACCENT_GREEN)
    tf = c_imp.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "📈 Quantified Potential Impact"
    p.font.bold = True
    p.font.size = Pt(13.5)
    p.font.color.rgb = ACCENT_GREEN
    p = tf.add_paragraph()
    p.text = "\n• 2 Priority Districts Covered: South 24 Parganas (~8.16M) & Purba Medinipur (~5.10M) [Census 2011]."
    p.font.size = Pt(11)
    p.font.color.rgb = TEXT_WHITE
    p = tf.add_paragraph()
    p.text = "\n• 47 Facilities Evaluated: 5 high-risk health clinics prioritized for backup generator flood protection [Estimate]."
    p.font.size = Pt(11)
    p.font.color.rgb = TEXT_WHITE
    p = tf.add_paragraph()
    p.text = "\n• 48h Evacuation Window: Enables advance road clearance and bypass logistics before storm landfall."
    p.font.size = Pt(11)
    p.font.color.rgb = TEXT_WHITE

    # Col 2: Known Current Limitations
    c_lim = add_card(s11, Inches(4.8), Inches(1.8), cw3, ch3, ACCENT_RED)
    tf = c_lim.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "⚠️ Known Technical Limitations"
    p.font.bold = True
    p.font.size = Pt(13.5)
    p.font.color.rgb = ACCENT_RED
    p = tf.add_paragraph()
    p.text = "\n• Bathtub Flood Model: Uses 30m SRTM satellite elevation; does not currently model dynamic hydrodynamic tides."
    p.font.size = Pt(11)
    p.font.color.rgb = TEXT_WHITE
    p = tf.add_paragraph()
    p.text = "\n• Simulated ML Labels: Models trained on rule-based physics synthetic data; not verified against historical damage logs."
    p.font.size = Pt(11)
    p.font.color.rgb = TEXT_WHITE
    p = tf.add_paragraph()
    p.text = "\n• Single Storm Active: Only Cyclone Remal fully tested end-to-end in the live dashboard today."
    p.font.size = Pt(11)
    p.font.color.rgb = TEXT_WHITE

    # Col 3: Responsible Roadmap
    c_rdm = add_card(s11, Inches(8.8), Inches(1.8), cw3, ch3, ACCENT_CYAN)
    tf = c_rdm.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "🎯 Immediate Next Milestones"
    p.font.bold = True
    p.font.size = Pt(13.5)
    p.font.color.rgb = ACCENT_CYAN
    p = tf.add_paragraph()
    p.text = "\n• ML Validation: Leave-one-storm-out cross-validation against official post-disaster damage reports."
    p.font.size = Pt(11)
    p.font.color.rgb = TEXT_WHITE
    p = tf.add_paragraph()
    p.text = "\n• Dynamic Surge Modeling: Integrate INCOIS coastal tide gauge telemetry into inundation depth."
    p.font.size = Pt(11)
    p.font.color.rgb = TEXT_WHITE
    p = tf.add_paragraph()
    p.text = "\n• Pan-India Storm Ingestion: Automate parsing for all upcoming North Indian Ocean cyclonic disturbances."
    p.font.size = Pt(11)
    p.font.color.rgb = TEXT_WHITE

    add_speaker_note(s11, (
        "Responsible disaster technology requires total honesty about limitations. "
        "Our surge model currently uses a static bathtub method on 30-meter SRTM elevation, and our ML models are trained on simulated physics data. "
        "We do not claim real-world damage validation today. "
        "Instead, we present a credible roadmap: integrating hydrodynamic tide telemetry and validating models against verified post-disaster field reports in partnership with disaster authorities."
    ))

    # =========================================================================
    # SLIDE 12: Team & Call to Action
    # =========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    apply_slide_bg(s12)
    add_header(s12, "Team & Call to Action: Moving from Forecast to Action",
               "Partner with us to pilot CycloneShield for India's vulnerable coastal communities.")

    # Left: Team details card
    c_team = add_card(s12, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.8))
    tf = c_team.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "👥 Project Team & Submission"
    p.font.bold = True
    p.font.size = Pt(14)
    p.font.color.rgb = ACCENT_CYAN
    p = tf.add_paragraph()
    p.text = "\n• Team Name: [TEAM NAME: TO VERIFY]"
    p.font.size = Pt(12)
    p.font.color.rgb = TEXT_WHITE
    p = tf.add_paragraph()
    p.text = "\n• Team Members: [TEAM MEMBERS: TO VERIFY]"
    p.font.size = Pt(12)
    p.font.color.rgb = TEXT_WHITE
    p = tf.add_paragraph()
    p.text = "\n• Hackathon Event: [HACKATHON NAME: TO VERIFY]"
    p.font.size = Pt(12)
    p.font.color.rgb = TEXT_WHITE
    p = tf.add_paragraph()
    p.text = "\n• Track / Focus: AI for Social Impact & Disaster Resilience"
    p.font.size = Pt(12)
    p.font.color.rgb = TEXT_MUTED

    # Right: Call to action & links card
    c_cta = add_card(s12, Inches(6.9), Inches(1.8), Inches(5.6), Inches(4.8), ACCENT_CYAN)
    tf = c_cta.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "🔗 Live Artifacts & Evaluation Links"
    p.font.bold = True
    p.font.size = Pt(14)
    p.font.color.rgb = ACCENT_CYAN
    p = tf.add_paragraph()
    p.text = "\n🌐 Live Streamlit Command Center:\ncycloneshield-vawrqbhtbgu8i6cafhbf3q.streamlit.app"
    p.font.size = Pt(11.5)
    p.font.color.rgb = TEXT_WHITE
    p = tf.add_paragraph()
    p.text = "\n📂 GitHub Code Repository:\ngithub.com/itsme-sherlock/CycloneShield"
    p.font.size = Pt(11.5)
    p.font.color.rgb = TEXT_WHITE
    p = tf.add_paragraph()
    p.text = "\n📓 Interactive Google Colab:\ncolab.research.google.com/github/itsme-sherlock/CycloneShield/blob/main/CycloneShield_Colab.ipynb"
    p.font.size = Pt(11)
    p.font.color.rgb = TEXT_MUTED
    p = tf.add_paragraph()
    p.text = "\n🤝 Next Step: Ready for state-level SDMA pilot onboarding."
    p.font.size = Pt(11.5)
    p.font.bold = True
    p.font.color.rgb = ACCENT_GREEN

    add_speaker_note(s12, (
        "CycloneShield proves that modern AI can transform passive weather bulletins into proactive, life-saving infrastructure intelligence. "
        "Our working prototype is live online, fully reproducible via GitHub and Google Colab, and designed specifically for Indian disaster management. "
        "We invite the judges to test the live dashboard, and we look forward to collaborating with disaster authorities on our upcoming coastal pilot. Thank you."
    ))

    # Save presentation
    prs.save(OUTPUT_PPTX)
    print(f"Presentation successfully created at {OUTPUT_PPTX}")

if __name__ == "__main__":
    build_deck()
