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
    # SLIDE 1: Title + Core Promise + Hosted Prototype
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
    p2.text = "Turning Storm Scenarios into Clearer District Priorities"
    p2.font.size = Pt(20)
    p2.font.bold = True
    p2.font.color.rgb = ACCENT_CYAN
    p2.font.name = "Arial"

    p3 = tf.add_paragraph()
    p3.text = "A decision-support prototype for reviewing configured storm scenarios and possible preparedness actions."
    p3.font.size = Pt(14)
    p3.font.color.rgb = TEXT_MUTED
    p3.font.name = "Arial"

    # 3 Info Cards at bottom
    c1 = add_card(s1, Inches(0.8), Inches(4.3), Inches(3.6), Inches(2.3), ACCENT_CYAN)
    tf1 = c1.text_frame
    tf1.word_wrap = True
    p = tf1.paragraphs[0]
    p.text = "🌐 INTERACTIVE PROTOTYPE"
    p.font.bold = True
    p.font.size = Pt(12)
    p.font.color.rgb = ACCENT_CYAN
    p = tf1.add_paragraph()
    p.text = "cycloneshield-vawrqbhtbgu8i6cafhbf3q.streamlit.app"
    p.font.size = Pt(11)
    p.font.color.rgb = TEXT_WHITE
    p = tf1.add_paragraph()
    p.text = "Interactive view of configured scenarios, screening outputs, and district priorities."
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
        "Good morning, judges. Weather agencies track cyclones, and response officers make operational decisions. "
        "CycloneShield is not a replacement for either. It is a decision-support prototype designed to turn a selected storm scenario and configured district information "
        "into clearer lifeline priorities and possible actions for people to review."
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
    p.text = "\n• Critical questions unanswered: Could State Highway 3 remain passable for ambulances?"
    p.font.size = Pt(12.5)
    p.font.color.rgb = TEXT_WHITE
    p = tf.add_paragraph()
    p.text = "\n• Which primary health centers may need backup power before landfall?"
    p.font.size = Pt(12)
    p.font.color.rgb = TEXT_MUTED

    add_speaker_note(s2, (
        "India's coastal districts house over 188 million citizens according to the 2011 Census. When a cyclone develops, the India Meteorological Department provides official weather forecasts. "
        "However, a District Magistrate or State Disaster Management officer cannot deploy ambulances based solely on wind speed isobars. "
        "They need to assess whether State Highway 3 could be cut off, which rural clinics may face flooding, and how to prepare alerts when cell networks fail. That is the critical last-mile operational gap."
    ))

    # =========================================================================
    # SLIDE 3: Solution: 5-Step Flow
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    apply_slide_bg(s3)
    add_header(s3, "The Solution: Decision-Support Workflow",
               "Configured scenarios and data become screening outputs for human review—not official forecasts or dispatches.")

    steps = [
        ("1. Select Scenario", "Bundled historical track or user-supplied file.\nConfirm any live query in the app.", "[Cached / Input]"),
        ("2. Review Hazards", "Surge and rainfall screening estimates.\nEarth Engine can process geospatial layers.", "[Estimate / Optional]"),
        ("3. View Lifelines", "Configured district profiles and open-data-derived baselines.\nNot a fresh live asset overlay.", "[Configured]"),
        ("4. Compare Priorities", "Rules and local ML produce screening scores.\nPossible actions are for officer review.", "[Scenario output]"),
        ("5. Inspect a Photo", "Explicit Gemini Vision request if configured and confirmed.\nOtherwise prepared offline benchmark.", "[Live / Benchmark]")
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
        "CycloneShield demonstrates how a selected storm scenario and configured district profiles can be organized into maps, screening scores, and possible preparedness actions. "
        "Live forecasts require a connected weather source. Earth Engine helps with geospatial data; it does not predict cyclones. "
        "The prototype does not replace official forecasts or automatically dispatch responders."
    ))

    # =========================================================================
    # SLIDE 4: Live Prototype: Cyclone Remal End-to-End
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    apply_slide_bg(s4)
    add_header(s4, "Prepared Demonstration: Cyclone Remal Scenario",
               "Configured screening outputs—not observed impacts or a validated forecast.")

    # Left: 3 concise bullet cards
    c_left = add_card(s4, Inches(0.8), Inches(1.8), Inches(4.8), Inches(4.8))
    tf = c_left.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "🎯 Scenario Highlights (Remal)"
    p.font.bold = True
    p.font.size = Pt(14)
    p.font.color.rgb = ACCENT_CYAN
    p = tf.add_paragraph()
    p.text = "\n• District rankings and lifeline screening help compare possible priorities; they do not confirm road closures."
    p.font.size = Pt(11.5)
    p.font.color.rgb = TEXT_WHITE
    p = tf.add_paragraph()
    p.text = "\n• Facility results use configured profiles and scenario rules, not live asset-by-asset analysis."
    p.font.size = Pt(11.5)
    p.font.color.rgb = TEXT_WHITE
    p = tf.add_paragraph()
    p.text = "\n• Population figures are Census-era references; scores are screening outputs for review."
    p.font.size = Pt(11.5)
    p.font.color.rgb = TEXT_WHITE
    p = tf.add_paragraph()
    p.text = "\n• The map is a scenario view, not a live satellite feed or official warning."
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
        "This is a configured Cyclone Remal scenario in our interactive prototype. "
        "The map and risk matrix help compare modeled priorities; they are not confirmed road closures or clinic flooding. "
        "State profiles and thresholds need local validation before operational use."
    ))

    # =========================================================================
    # SLIDE 5: Google AI at Work
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    apply_slide_bg(s5)
    add_header(s5, "Google Tools: Defined Roles",
               "Connected services are used only for their specific data or analysis tasks.")

    # Left: 3 short bullets
    c_left = add_card(s5, Inches(0.8), Inches(1.8), Inches(5.2), Inches(4.8))
    tf = c_left.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "🤖 Bounded Roles & Demo Modes"
    p.font.bold = True
    p.font.size = Pt(14)
    p.font.color.rgb = ACCENT_CYAN
    p = tf.add_paragraph()
    p.text = "\n1. Gemini advisory code exists; displayed broadcasts use prepared templates, not live Gemini."
    p.font.size = Pt(11.5)
    p.font.color.rgb = TEXT_WHITE
    p = tf.add_paragraph()
    p.text = "\n2. Gemini Vision is optional and user-triggered; offline benchmark output is not model analysis."
    p.font.size = Pt(11.5)
    p.font.color.rgb = TEXT_WHITE
    p = tf.add_paragraph()
    p.text = "\n3. Earth Engine can supply/process geospatial layers; it does not forecast cyclones. Weather must come from a connected source."
    p.font.size = Pt(11.5)
    p.font.color.rgb = TEXT_WHITE
    p = tf.add_paragraph()
    p.text = "\nAll generated messages are drafts for review; the demo does not issue alerts or dispatch resources."
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
        "Gemini Vision can analyze an explicitly submitted image when a live request succeeds; otherwise the displayed photo result is a prepared offline benchmark. "
        "Earth Engine supports geospatial data work, not cyclone prediction. Weather forecasts require a connected meteorological source. "
        "These tools support analysis and presentation; people and agencies remain responsible for decisions and alerts."
    ))

    # =========================================================================
    # SLIDE 6: Explainable Risk Score
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    apply_slide_bg(s6)
    add_header(s6, "Risk Screening: Explainable, Not Validated",
               "Scenario scores help organize review; they are not field-validated impact probabilities.")

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
    p.text = "Configured profiles and synthetic training data limit real-world interpretation; local validation and officer review are required."
    p.font.size = Pt(10.5)
    p.font.color.rgb = TEXT_MUTED

    add_speaker_note(s6, (
        "The dashboard displays scenario-based screening scores and configured profiles. "
        "The underlying model uses synthetic physics-inspired training data, so these outputs are not field-validated probabilities. "
        "They can help structure review but cannot justify or issue an evacuation decision on their own."
    ))

    # =========================================================================
    # SLIDE 7: Predictive ML & Validation (Honest Version)
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    apply_slide_bg(s7)
    add_header(s7, "Predictive ML & Validation: Honest Methodology",
               "The prototype compares scenarios; it does not provide a validated operational forecast.")

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
    p.text = "\n• Benchmark metrics use synthetic scenarios (n=3,600); they do not establish real-world predictive accuracy."
    p.font.size = Pt(11)
    p.font.color.rgb = TEXT_WHITE
    p = tf.add_paragraph()
    p.text = "\n• Outputs are screening scores under configured inputs, not calibrated probabilities of real-world failure."
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
        "The what-if view compares model outputs as scenario inputs change. "
        "Training and test data are synthetic, so benchmark metrics show internal performance on those scenarios—not real-world predictive accuracy. "
        "Field validation against verified damage records is required."
    ))

    # =========================================================================
    # SLIDE 8: Who It Serves: Three Personas
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    apply_slide_bg(s8)
    add_header(s8, "Who It Serves: Actionable Decisions by Persona",
               "Helping officers consider options—without replacing their judgment or authority.")

    personas = [
        ("🚒 NDRF / SDRF Battalions", "Review Possible Staging Options",
         "• Compare possible boat, pump, and access-route staging locations against scenario risks.\n• Validate roads and local conditions before use.\n• No rescue units are automatically deployed.",
         ACCENT_ORANGE),
        ("🏛️ District Magistrates & SDMA", "Consider Preparedness Actions",
         "• Review possible evacuation, facility-continuity, and resource-prioritization actions.\n• Validate local data and thresholds.\n• Authorized officers retain all decision authority.",
         ACCENT_CYAN),
        ("📻 Coastal Delta Communities", "Agency-Approved Warnings",
         "• Draft messages and voice workflows can be reviewed for local use.\n• Public alerts require agency approval and connected delivery channels.\n• The prototype does not send alerts.",
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
        "CycloneShield does not replace weather agencies or rescue officers. "
        "It is designed to help them turn complex information into clearer priorities and faster decisions. "
        "It recommends possible actions for review; it does not deploy resources, issue evacuations, or send public warnings."
    ))

    # =========================================================================
    # SLIDE 9: Built for India: Current vs Planned
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    apply_slide_bg(s9)
    add_header(s9, "Built for India: Operational Scope vs Roadmap",
               "Five configured state profiles are a starting point for validation—not national operational coverage.")

    # Two clear comparison cards
    cw = Inches(5.6)
    ch = Inches(4.8)

    # Left: Operational Today
    c_today = add_card(s9, Inches(0.8), Inches(1.8), cw, ch, ACCENT_GREEN)
    tf = c_today.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "✅ CONFIGURED DEMONSTRATION"
    p.font.bold = True
    p.font.size = Pt(14)
    p.font.color.rgb = ACCENT_GREEN
    p = tf.add_paragraph()
    p.text = "\n• Historical storm examples are selected from a bundled catalog; confirm any live query separately."
    p.font.size = Pt(11.5)
    p.font.color.rgb = TEXT_WHITE
    p = tf.add_paragraph()
    p.text = "\n• Five state profiles use configured districts and scenario data; they are not agency integrations."
    p.font.size = Pt(11.5)
    p.font.color.rgb = TEXT_WHITE
    p = tf.add_paragraph()
    p.text = "\n• Seven language choices; messages and audio paths require review and per-run verification."
    p.font.size = Pt(11.5)
    p.font.color.rgb = TEXT_WHITE
    p = tf.add_paragraph()
    p.text = "\n• Compatible user-supplied track files can be explored; no live IMD feed is implied."
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
    p.text = "\n• State partners must validate local boundaries, assets, populations, and thresholds."
    p.font.size = Pt(11.5)
    p.font.color.rgb = TEXT_WHITE
    p = tf.add_paragraph()
    p.text = "\n• Multilingual Extension: Spoken audio in Odia, Telugu, Tamil, Malayalam, and Marathi."
    p.font.size = Pt(11.5)
    p.font.color.rgb = TEXT_WHITE
    p = tf.add_paragraph()
    p.text = "\n• Live forecast and official bulletin sources require separate connection and validation."
    p.font.size = Pt(11.5)
    p.font.color.rgb = TEXT_WHITE
    p = tf.add_paragraph()
    p.text = "\n• Core Scalability: Standard GeoPandas geospatial projection (EPSG:3857/4326) covers all 7,516 km of Indian coastline."
    p.font.size = Pt(11)
    p.font.color.rgb = TEXT_MUTED

    add_speaker_note(s9, (
        "The prototype includes five configured state profiles and language choices. "
        "Operational scaling requires local data validation, appropriate connected weather sources, and agency-approved workflows."
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
        ("Week 4: Tabletop Exercise", "• Review a historical scenario with agency partners.\n• Evaluate outputs and limitations.\n• Agree next steps before any production deployment.")
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
    p.text = "• Service quotas, hosting costs, and licensing depend on the configured deployment.\n• Cloud Run / Vertex AI are deployment options; production Earth Engine access and operational integrations require separate review."
    p.font.size = Pt(10)
    p.font.color.rgb = TEXT_MUTED

    add_speaker_note(s10, (
        "We propose a controlled pilot with a state partner: validate local data, review draft outputs, and run a tabletop exercise. "
        "Production hosting, live alert channels, and operational use would require separate approval, integration, and safeguards."
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
    p.text = "\n• Potential use: support review of priorities; no claim of people currently protected or actions already taken."
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
    p.text = "\n• Insurance trigger amounts are illustrative calculations, not an active policy or payment."
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
        "CycloneShield is not trying to replace weather agencies or rescue officers. "
        "It is designed to help them turn complex information into clearer priorities and faster decisions. "
        "We are seeking a partner to validate the data and test the workflow in a controlled tabletop pilot. Thank you."
    ))

    # Save presentation
    prs.save(OUTPUT_PPTX)
    print(f"Presentation successfully created at {OUTPUT_PPTX}")

if __name__ == "__main__":
    build_deck()
