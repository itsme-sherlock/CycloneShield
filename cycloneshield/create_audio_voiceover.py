"""
Create Audio Voiceover for CycloneShield Hackathon Demo Video
Generates synchronized narration using gTTS and splices authentic regional emergency voice broadcasts.
Strictly calibrated for: 3:30 to 4:00 minutes (210s - 240s) satisfying the 3-5 minute requirement.
Aligned 100% with the latest app.py code and UI layout.
"""

import os
import subprocess
import json
import imageio_ffmpeg
from gtts import gTTS

FFMPEG_EXE = imageio_ffmpeg.get_ffmpeg_exe()
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AUDIO_DIR = os.path.join(BASE_DIR, "cycloneshield", "outputs", "audio")
TEMP_DIR = os.path.join(BASE_DIR, "cycloneshield", "outputs", "voiceover_parts")
os.makedirs(TEMP_DIR, exist_ok=True)

SCRIPTS = {
    "act1_hook": (
        "Namaste judges. Over 188 million Indian citizens live along our 7,500-kilometer coastline, "
        "facing recurring severe cyclonic storms in the Bay of Bengal and Arabian Sea. "
        "While agencies like the IMD forecast cyclone trajectories with remarkable precision, "
        "disaster commanders hit a fatal Last-Mile Disaster Gap: "
        "synoptic wind isobars do not tell a District Magistrate which evacuation highways will drown under coastal surge, "
        "which rural hospitals will lose backup power, "
        "or how to alert fishing communities when cellular networks collapse. "
        "This is CycloneShield: an end-to-end, multi-state disaster operations command center "
        "converting cyclone tracks into street-level lifeline actions before landfall."
    ),
    "act2_top_controls_imd": (
        "CycloneShield is built for all of India—scaling across our vulnerable eastern and western coastlines. "
        "In the three selectors at the top of the home page, duty officers can switch between major coastal states—"
        "West Bengal, Odisha, Andhra Pradesh, Tamil Nadu, and Gujarat—"
        "choose from 13 historical cyclones or select custom live IMD CSV track ingestion directly from the Cyclone Event dropdown, "
        "and switch the broadcast language across seven Indian languages. "
        "For Cyclone Remal in West Bengal, our spatial engine dynamically projects multi-tier wind swaths "
        "and applies NASA SRTM 30-meter elevation screening across 32.6 million citizens, "
        "flagging 73 kilometers of flooded highways and seven inundated hospitals in under three seconds."
    ),
    "act3_tab1_spatial_xai": (
        "Under disaster pressure, duty officers need instant clarity without black-box ambiguity. "
        "In Tab 1, our geospatial viewport renders five operational map layers—"
        "intersecting coastal bathtub surge with OpenStreetMap lifelines over NASA SRTM 30-meter terrain. "
        "On the right, our District AI Inspector evaluates South 24 Parganas—home to 81.6 lakh citizens—"
        "at a critical 84.0 out of 100, "
        "pinpointing four of eight hospitals at flood risk, six of eighteen shelters inundated, "
        "39.9 kilometers of district roads cut off, and six electrical substations facing blackout risk."
    ),
    "act4_part1_voice_intro": (
        "When cyclones make landfall, power grids fail and cellular towers go dark. "
        "Battery radios and community sirens become the only life-saving communication channels. "
        "CycloneShield is voice-first and multilingual. "
        "Right inside the District Inspector, officers can stream spoken emergency radio bulletins "
        "across seven Indian languages. Listen to our live voice broadcast in Bengali:"
    ),
    "act4_part2_cap": (
        "Switching to Tab 2—our Voice Alerts and Broadcast Hub—commanders get copy-ready 160-character SMS, "
        "WhatsApp, and public address scripts, alongside a one-click OASIS Common Alerting Protocol "
        "CAP version 1.2 XML export that feeds directly into India's national NDMA SACHET alert gateway."
    ),
    "act5_tab3_gemini_vision": (
        "Post-landfall, emergency response pivots to field reconnaissance. "
        "In Tab 3, we deploy Google Gemini Multimodal Vision for ground damage photo triage. "
        "NDRF drone operators and citizens can upload field photos or evaluate benchmark incident scenes. "
        "Analyzing this flooded arterial corridor on National Highway 117, "
        "Gemini detects standing floodwaters, estimates water level at 1.2 meters, "
        "flags road access as impassable with a sub-two-hour response window, "
        "and recommends immediate NDRF deployment of high-capacity dewatering pumps and inflatable motor boats—"
        "complete with machine-parsable JSON telemetry."
    ),
    "act6_tab4_tab5_sim_ml": (
        "In Tab 4, our Multi-District Risk Matrix ranks all coastal districts by Census population exposure and lifeline impact, "
        "with one-click CSV export for state control rooms. "
        "In Tab 5, our What-If Landfall Simulator enables proactive scenario planning. "
        "Duty officers can click the Spring Tide plus 1.5-meter or Super Cyclone plus 2.5-meter presets, "
        "or drag the surge, wind, and 48-hour rainfall sliders. "
        "In sub-5 milliseconds, our calibrated Scikit-Learn HistGradientBoosting model—"
        "achieving a 0.941 ROC-AUC—recalculates road-blockage and hospital-flooding probabilities across every coastal district."
    ),
    "act7_tab6_close": (
        "Finally, Tab 6 provides complete evaluator audit transparency—"
        "displaying our ROC-AUC benchmark curves, Google Vertex AI Model Registry manifest, "
        "BigQuery NOAA SQL queries costing a fraction of a cent, "
        "and our scale-to-zero Cloud Run Dockerfile. "
        "Backed by transparent data provenance and a four-step State Disaster Management rollout plan, "
        "CycloneShield transforms meteorological forecasts into saved Indian lives. Thank you."
    )
}

def get_audio_duration(filepath: str) -> float:
    cmd = [FFMPEG_EXE, "-i", filepath, "-f", "null", "-"]
    res = subprocess.run(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE, text=True, errors="ignore")
    for line in res.stderr.splitlines():
        if "Duration:" in line:
            parts = line.split("Duration:")[1].split(",")[0].strip().split(":")
            return float(parts[0]) * 3600 + float(parts[1]) * 60 + float(parts[2])
    return 0.0

def generate_voiceover():
    print("=" * 60)
    print("Generating Calibrated Voiceover Parts for Latest Layout...")
    print("=" * 60)
    
    part_files = {}
    for key, text in SCRIPTS.items():
        raw_path = os.path.join(TEMP_DIR, f"{key}_raw.mp3")
        tuned_path = os.path.join(TEMP_DIR, f"{key}.mp3")
        tts = gTTS(text=text, lang="en", tld="co.in", slow=False)
        tts.save(raw_path)
        
        # Apply atempo=1.14 for natural, crisp, energetic cadence
        cmd_tempo = [
            FFMPEG_EXE, "-y", "-i", raw_path,
            "-filter:a", "atempo=1.14",
            tuned_path
        ]
        subprocess.run(cmd_tempo, capture_output=True)
        dur = get_audio_duration(tuned_path)
        part_files[key] = (tuned_path, dur)
        print(f"  -> {key}: {dur:.2f}s ({len(text.split())} words)")
        
    # Bengali live alert clip
    bengali_source = os.path.join(AUDIO_DIR, "remal_south_24_parganas_bn.mp3")
    bengali_clip = os.path.join(TEMP_DIR, "bengali_clip.mp3")
    if os.path.exists(bengali_source):
        cmd = [
            FFMPEG_EXE, "-y", "-ss", "00:00:01", "-to", "00:00:05",
            "-i", bengali_source, "-c", "copy", bengali_clip
        ]
        subprocess.run(cmd, capture_output=True)
        bengali_dur = get_audio_duration(bengali_clip)
        print(f"  -> Bengali live audio clip: {bengali_dur:.2f}s")
    else:
        bengali_dur = 0.0
        bengali_clip = None

    concat_list_file = os.path.join(TEMP_DIR, "concat_list.txt")
    ordered_files = [
        part_files["act1_hook"][0],
        part_files["act2_top_controls_imd"][0],
        part_files["act3_tab1_spatial_xai"][0],
        part_files["act4_part1_voice_intro"][0],
    ]
    if bengali_clip and os.path.exists(bengali_clip):
        ordered_files.append(bengali_clip)
    ordered_files.extend([
        part_files["act4_part2_cap"][0],
        part_files["act5_tab3_gemini_vision"][0],
        part_files["act6_tab4_tab5_sim_ml"][0],
        part_files["act7_tab6_close"][0]
    ])

    with open(concat_list_file, "w", encoding="utf-8") as f:
        for p in ordered_files:
            escaped_p = p.replace("\\", "/")
            f.write(f"file '{escaped_p}'\n")

    master_audio_raw = os.path.join(TEMP_DIR, "master_voiceover_raw.mp3")
    master_audio_mp3 = os.path.join(BASE_DIR, "cycloneshield_demo_voiceover.mp3")
    
    cmd_concat = [
        FFMPEG_EXE, "-y", "-f", "concat", "-safe", "0",
        "-i", concat_list_file, "-c:a", "libmp3lame", "-b:a", "192k", master_audio_raw
    ]
    subprocess.run(cmd_concat, capture_output=True)

    # Apply global tempo 1.40 for 3:45 target
    cmd_final = [
        FFMPEG_EXE, "-y", "-i", master_audio_raw,
        "-filter:a", "atempo=1.40",
        master_audio_mp3
    ]
    subprocess.run(cmd_final, capture_output=True)

    total_dur = get_audio_duration(master_audio_mp3)
    mins = int(total_dur // 60)
    secs = int(total_dur % 60)
    print("=" * 60)
    print(f"MASTER VOICEOVER COMPLETED!")
    print(f"Location: {master_audio_mp3}")
    print(f"Total Runtime: {mins}:{secs:02d} ({total_dur:.2f} seconds)")
    print(f"Satisfies Hackathon '3–5 minutes' requirement: {'YES' if 180 <= total_dur <= 300 else 'NO'}")
    print("=" * 60)

    timings = {
        "act1_hook": round(part_files["act1_hook"][1] / 1.40, 2),
        "act2_top_controls_imd": round(part_files["act2_top_controls_imd"][1] / 1.40, 2),
        "act3_tab1_spatial_xai": round(part_files["act3_tab1_spatial_xai"][1] / 1.40, 2),
        "act4_voice_cap": round((part_files["act4_part1_voice_intro"][1] + bengali_dur + part_files["act4_part2_cap"][1]) / 1.40, 2),
        "act5_gemini_vision": round(part_files["act5_tab3_gemini_vision"][1] / 1.40, 2),
        "act6_sim_ml": round(part_files["act6_tab4_tab5_sim_ml"][1] / 1.40, 2),
        "act7_close": round(part_files["act7_tab6_close"][1] / 1.40, 2),
        "total_duration": total_dur
    }
    
    timing_file = os.path.join(TEMP_DIR, "timings.json")
    with open(timing_file, "w") as f:
        json.dump(timings, f, indent=2)
    print(f"Timings saved to: {timing_file}")
    return timings

if __name__ == "__main__":
    generate_voiceover()
