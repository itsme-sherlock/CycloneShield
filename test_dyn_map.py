import os, sys
sys.path.insert(0, "cycloneshield")
import pandas as pd
import folium
from app import render_dynamic_folium_map, compute_state_district_vulnerability, load_cyclone_track_data

dists = compute_state_district_vulnerability('Tamil Nadu', 'VARDAH', 85.0, 2.5)
track, meta = load_cyclone_track_data('VARDAH', 'Tamil Nadu')
html = render_dynamic_folium_map(dists, track, '🏥 District Risk & Critical Lifelines (Recommended)', 'Tamil Nadu')

print("Generated HTML Length:", len(html))
with open("test_dyn_map.html", "w", encoding="utf-8") as f:
    f.write(html)
print("Saved test_dyn_map.html successfully")
