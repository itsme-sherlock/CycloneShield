"""
Record End-to-End Walkthrough Video of CycloneShield with Playwright
Strictly aligned with the latest app.py code and UI layout.
Synchronized to the 3:45 master audio voiceover.
Outputs:
  - CycloneShield_Demo_Walkthrough.mp4 (H.264 + AAC, 1080p)
  - cycloneshield_demo_walkthrough.webm
"""

import os
import time
import subprocess
import json
import imageio_ffmpeg
from playwright.sync_api import sync_playwright

FFMPEG_EXE = imageio_ffmpeg.get_ffmpeg_exe()
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RECORD_DIR = os.path.join(BASE_DIR, "cycloneshield", "outputs", "recordings")
VOICEOVER_PATH = os.path.join(BASE_DIR, "cycloneshield_demo_voiceover.mp3")
OUTPUT_MP4 = os.path.join(BASE_DIR, "CycloneShield_Demo_Walkthrough.mp4")
OUTPUT_WEBM = os.path.join(BASE_DIR, "cycloneshield_demo_walkthrough.webm")
OUTPUT_WEBM_COPY = os.path.join(BASE_DIR, "cycloneshield", "outputs", "cycloneshield_demo_walkthrough.webm")
OUTPUT_MP4_COPY = os.path.join(BASE_DIR, "cycloneshield", "outputs", "CycloneShield_Demo_Walkthrough.mp4")

os.makedirs(RECORD_DIR, exist_ok=True)

def smooth_scroll(page, target_y, steps=25, delay=0.03):
    """Smoothly scroll the page to target_y position."""
    current_y = page.evaluate("window.scrollY")
    diff = target_y - current_y
    for i in range(1, steps + 1):
        y = current_y + diff * (i / steps)
        page.evaluate(f"window.scrollTo(0, {y})")
        time.sleep(delay)

def record_walkthrough():
    print("=" * 60)
    print("Starting Playwright Video Recording (Latest app.py Layout)...")
    print("=" * 60)

    # Clean previous recordings
    for f in os.listdir(RECORD_DIR):
        if f.endswith(".webm"):
            try:
                os.remove(os.path.join(RECORD_DIR, f))
            except Exception:
                pass

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=[
                "--disable-gpu",
                "--no-sandbox",
                "--disable-setuid-sandbox",
                "--hide-scrollbars"
            ]
        )
        context = browser.new_context(
            record_video_dir=RECORD_DIR,
            record_video_size={"width": 1920, "height": 1080},
            viewport={"width": 1920, "height": 1080}
        )
        page = context.new_page()

        print("Navigating to http://localhost:8501 ...")
        page.goto("http://localhost:8501", wait_until="networkidle", timeout=45000)
        page.wait_for_timeout(4000)

        # -------------------------------------------------------------
        # ACT 1: Hook & Last-Mile Gap (~32 seconds)
        # -------------------------------------------------------------
        print(">> Act 1: The Hook & India's Last-Mile Gap (~32s)...")
        # Hover over top hero area
        page.mouse.move(960, 80)
        page.wait_for_timeout(2500)
        
        # Scroll gently to Executive Situation Card
        smooth_scroll(page, 180, steps=15, delay=0.03)
        page.mouse.move(700, 240)
        page.wait_for_timeout(4000)
        page.mouse.move(1400, 240) # Overall threat badge: CRITICAL
        page.wait_for_timeout(3500)

        # Move to the Strategic 6 KPI Ribbon
        smooth_scroll(page, 320, steps=15, delay=0.03)
        kpi_x_coords = [320, 580, 840, 1100, 1360, 1620]
        for x in kpi_x_coords:
            page.mouse.move(x, 430)
            page.wait_for_timeout(1800)

        page.wait_for_timeout(3000)

        # -------------------------------------------------------------
        # ACT 2: Top Control Bar & Multi-State Cyclone Selection (~33 seconds)
        # -------------------------------------------------------------
        print(">> Act 2: Top Control Bar & Multi-State Cyclone Selection (~33s)...")
        smooth_scroll(page, 0, steps=20, delay=0.03)
        page.wait_for_timeout(2000)

        # Hover & open State Selector (Dropdown 1)
        page.mouse.move(300, 120)
        page.wait_for_timeout(2500)
        try:
            sels = page.locator("div[data-testid='stSelectbox']")
            if sels.count() >= 3:
                # Open Dropdown 1 (State) briefly to show all 5 states
                sels.nth(0).click()
                page.wait_for_timeout(2500)
                page.keyboard.press("Escape")
                page.wait_for_timeout(1500)

                # Open Dropdown 2 (Cyclone Event) to show REMAL, AMPHAN, and Custom IMD option
                page.mouse.move(750, 120)
                sels.nth(1).click()
                page.wait_for_timeout(3000)
                page.keyboard.press("Escape")
                page.wait_for_timeout(1500)

                # Open Dropdown 3 (App & Broadcast Language) to show 7 Indian languages
                page.mouse.move(1200, 120)
                sels.nth(2).click()
                page.wait_for_timeout(2500)
                page.keyboard.press("Escape")
                page.wait_for_timeout(1500)
        except Exception as e:
            print(f"Top selector note: {e}")

        # Pan across Situation Card & 6 KPI cards while Remal metrics are narrated
        smooth_scroll(page, 220, steps=15, delay=0.03)
        page.mouse.move(650, 260)
        page.wait_for_timeout(4000)
        page.mouse.move(1100, 420)
        page.wait_for_timeout(4000)

        # -------------------------------------------------------------
        # ACT 3: Tab 1 — Hazard Maps, Layer Selector & District AI Inspector (~37 seconds)
        # -------------------------------------------------------------
        print(">> Act 3: Tab 1 — Hazard Maps, Layer Selector & District AI Inspector (~37s)...")
        smooth_scroll(page, 480, steps=20, delay=0.03)
        page.wait_for_timeout(1500)

        # Ensure Tab 1 is active
        tab1 = page.get_by_text("Situation & Hazard Maps", exact=False).first
        if tab1.count() > 0:
            tab1.click()
            page.wait_for_timeout(2000)

        # Left Column: Layer Selector dropdown
        page.mouse.move(450, 560)
        page.wait_for_timeout(2000)

        # Move mouse across the Folium map
        page.mouse.move(600, 750)
        page.wait_for_timeout(3500)
        page.mouse.move(750, 850)
        page.wait_for_timeout(3000)

        # Right Column: District AI Inspector
        page.mouse.move(1450, 580)
        page.wait_for_timeout(2500)
        # Hover over the glass panel with 88.4 / 100 score
        page.mouse.move(1450, 680)
        page.wait_for_timeout(4000)

        # Hover over the 4 Lifeline boxes: HOSPITALS, SHELTERS, ROADS CUT OFF, POWER GRID
        for x_box in [1280, 1400, 1520, 1640]:
            page.mouse.move(x_box, 820)
            page.wait_for_timeout(1500)

        page.wait_for_timeout(4000)

        # -------------------------------------------------------------
        # ACT 4: Tab 2 — Voice Alerts & Broadcast Hub (~36 seconds)
        # -------------------------------------------------------------
        print(">> Act 4: Tab 2 — Voice Alerts & Broadcast Hub (~36s)...")
        # In right panel, show the Voice tabs: English, Hindi, Bengali
        smooth_scroll(page, 780, steps=15, delay=0.03)
        page.wait_for_timeout(1500)
        bengali_subtab = page.get_by_text("Bengali (বাংলা)", exact=False)
        if bengali_subtab.count() > 0:
            try:
                bengali_subtab.first.click()
                page.wait_for_timeout(2000)
            except Exception:
                pass

        # Hover over audio player during the 4s Bengali broadcast
        page.mouse.move(1450, 950)
        page.wait_for_timeout(6000)

        # Now click Tab 2 (Voice Alerts & Broadcast Hub)
        smooth_scroll(page, 440, steps=15, delay=0.03)
        page.wait_for_timeout(1000)
        tab2 = page.get_by_text("Voice Alerts & Broadcast Hub", exact=False).first
        if tab2.count() > 0:
            tab2.click()
            page.wait_for_timeout(2500)

        # Left Column: SMS, WhatsApp, Community Radio
        page.mouse.move(550, 620)
        page.wait_for_timeout(4000)
        page.mouse.move(550, 780)
        page.wait_for_timeout(4000)

        # Right Column: OASIS CAP v1.2 XML preview & Download Button
        page.mouse.move(1350, 650)
        page.wait_for_timeout(3000)
        page.mouse.move(1350, 880) # Hover near download button
        page.wait_for_timeout(4000)

        # -------------------------------------------------------------
        # ACT 5: Tab 3 — Google Gemini Multimodal Drone Photo Triage (~34 seconds)
        # -------------------------------------------------------------
        print(">> Act 5: Tab 3 — Google Gemini Multimodal Ground Damage Photo Triage (~34s)...")
        smooth_scroll(page, 440, steps=15, delay=0.03)
        page.wait_for_timeout(1000)

        tab3 = page.get_by_text("Ground Damage Photo Triage", exact=False).first
        if tab3.count() > 0:
            tab3.click()
            page.wait_for_timeout(3000)

        # Show the top API Connected badge
        page.mouse.move(1550, 520)
        page.wait_for_timeout(2500)

        # Hover over benchmark scene selector
        page.mouse.move(500, 620)
        page.wait_for_timeout(3000)

        # Click Run Gemini Damage Triage button
        triage_btn = page.get_by_text("Run Gemini Damage Triage", exact=False)
        if triage_btn.count() > 0:
            try:
                triage_btn.first.click()
                page.wait_for_timeout(2500)
            except Exception:
                pass

        # Scroll to damage image and AI telemetry cards
        smooth_scroll(page, 720, steps=15, delay=0.03)
        page.wait_for_timeout(2000)

        # Hover over Water Depth (1.2m) and Severity 5/5
        page.mouse.move(600, 750)
        page.wait_for_timeout(3500)
        page.mouse.move(1200, 750)
        page.wait_for_timeout(4000)

        # Hover over Tactical Equipment Directives (pumps and boats)
        page.mouse.move(960, 920)
        page.wait_for_timeout(5000)

        # -------------------------------------------------------------
        # ACT 6: Tab 4 & Tab 5 — District Risk Matrix & What-If Landfall Simulator (~32 seconds)
        # -------------------------------------------------------------
        print(">> Act 6: Tab 4 & 5 — District Risk Matrix & What-If Simulator (~32s)...")
        smooth_scroll(page, 440, steps=15, delay=0.03)
        page.wait_for_timeout(1000)

        # Tab 4: Multi-District Risk Matrix
        tab4 = page.get_by_text("Multi-District Risk Matrix", exact=False).first
        if tab4.count() > 0:
            tab4.click()
            page.wait_for_timeout(2500)
            smooth_scroll(page, 650, steps=15, delay=0.03)
            page.wait_for_timeout(3500)
            # Hover over CSV download button
            page.mouse.move(400, 850)
            page.wait_for_timeout(2500)

        # Tab 5: What-If Landfall Simulator
        smooth_scroll(page, 440, steps=15, delay=0.03)
        page.wait_for_timeout(1000)
        tab5 = page.get_by_text("What-If Landfall Simulator", exact=False).first
        if tab5.count() > 0:
            tab5.click()
            page.wait_for_timeout(2500)

        # Click Spring Tide Preset button (+1.5m)
        spring_btn = page.get_by_text("Spring Tide (+1.5m)", exact=False)
        if spring_btn.count() > 0:
            try:
                spring_btn.first.click()
                page.wait_for_timeout(2500)
            except Exception:
                pass

        # Hover over sliders (left) and predicted failure table (right)
        page.mouse.move(500, 680)
        page.wait_for_timeout(3000)
        page.mouse.move(1350, 680)
        page.wait_for_timeout(5000)

        # -------------------------------------------------------------
        # ACT 7: Tab 6 — Architecture, FinOps, Pilot Footer & Conclusion (~21 seconds)
        # -------------------------------------------------------------
        print(">> Act 7: Tab 6 — Architecture, FinOps & State Pilot Footer (~21s)...")
        smooth_scroll(page, 440, steps=15, delay=0.03)
        page.wait_for_timeout(1000)

        tab6 = page.get_by_text("Technical Architecture", exact=False).first
        if tab6.count() > 0:
            tab6.click()
            page.wait_for_timeout(2500)

        # Switch across the subtabs: BigQuery SQL & Cloud Run
        bq_sub = page.get_by_text("BigQuery NOAA Ingestion", exact=False)
        if bq_sub.count() > 0:
            try:
                bq_sub.first.click()
                page.wait_for_timeout(2500)
            except Exception:
                pass

        docker_sub = page.get_by_text("Google Cloud Run Container Spec", exact=False)
        if docker_sub.count() > 0:
            try:
                docker_sub.first.click()
                page.wait_for_timeout(2500)
            except Exception:
                pass

        # Scroll down to Footer: Data Provenance & 4-Step State Pilot Rollout
        smooth_scroll(page, 950, steps=20, delay=0.03)
        page.mouse.move(500, 980) # Provenance notice
        page.wait_for_timeout(3000)
        page.mouse.move(1400, 980) # 4-Week State Pilot Rollout
        page.wait_for_timeout(3000)

        # Smooth scroll back to top hero title and Google Colab badge
        smooth_scroll(page, 0, steps=25, delay=0.03)
        page.mouse.move(960, 150)
        page.wait_for_timeout(4000)

        print("Walkthrough recording completed! Finalizing video stream...")
        context.close()
        browser.close()

    # Locate the recorded .webm file
    recorded_webms = [f for f in os.listdir(RECORD_DIR) if f.endswith(".webm")]
    if not recorded_webms:
        raise RuntimeError("No .webm recorded file found in RECORD_DIR!")
    
    raw_video = os.path.join(RECORD_DIR, recorded_webms[0])
    print(f"Raw recorded video: {raw_video} ({os.path.getsize(raw_video):,} bytes)")

    # -------------------------------------------------------------
    # Mux Audio and Video with FFmpeg
    # -------------------------------------------------------------
    print("=" * 60)
    print("Muxing Video with Synchronized Audio Voiceover...")
    print("=" * 60)

    # 1. Produce high-quality MP4 (H.264 + AAC, faststart)
    cmd_mp4 = [
        FFMPEG_EXE, "-y",
        "-i", raw_video,
        "-i", VOICEOVER_PATH,
        "-c:v", "libx264",
        "-preset", "medium",
        "-crf", "22",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        "-movflags", "+faststart",
        OUTPUT_MP4
    ]
    print(f"Rendering MP4: {OUTPUT_MP4} ...")
    res_mp4 = subprocess.run(cmd_mp4, capture_output=True, text=True, errors="ignore")
    if res_mp4.returncode != 0:
        print("MP4 Mux error:", res_mp4.stderr[-500:])
    else:
        print(f"MP4 created successfully! ({os.path.getsize(OUTPUT_MP4):,} bytes)")

    # 2. Produce high-quality WebM (VP9/VP8 + Opus)
    cmd_webm = [
        FFMPEG_EXE, "-y",
        "-i", raw_video,
        "-i", VOICEOVER_PATH,
        "-c:v", "copy",
        "-c:a", "libopus",
        "-shortest",
        OUTPUT_WEBM
    ]
    print(f"Rendering WebM: {OUTPUT_WEBM} ...")
    subprocess.run(cmd_webm, capture_output=True)

    # Copy files to cycloneshield/outputs/
    if os.path.exists(OUTPUT_MP4):
        import shutil
        shutil.copyfile(OUTPUT_MP4, OUTPUT_MP4_COPY)
    if os.path.exists(OUTPUT_WEBM):
        import shutil
        shutil.copyfile(OUTPUT_WEBM, OUTPUT_WEBM_COPY)

    print("=" * 60)
    print("ALL PRODUCTION DELIVERABLES UPDATED AND READY!")
    print(f"1. Master MP4 Video: {OUTPUT_MP4}")
    print(f"2. Master WebM Video: {OUTPUT_WEBM}")
    print(f"3. Master Audio Track: {VOICEOVER_PATH}")
    print("=" * 60)

if __name__ == "__main__":
    record_walkthrough()
