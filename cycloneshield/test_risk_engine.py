import json
import os

import pandas as pd
import pytest

from risk_engine import (
    classify_imd_wind,
    colour_band,
    composite_score,
    compute_district_risk,
    load_facilities,
    surge_score,
    wind_score,
)

BASE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(BASE, "data")


def _load():
    with open(os.path.join(DATA, "noaa_sample_tracks.json"), encoding="utf-8") as f:
        tracks = json.load(f)
    with open(os.path.join(DATA, "coastal_districts.geojson"), encoding="utf-8") as f:
        dists = [ft["properties"] for ft in json.load(f)["features"]]
    return tracks, dists, load_facilities(os.path.join(DATA, "osm_infrastructure_baseline.geojson"))


def _run(storm, state):
    tracks, dists, fac = _load()
    m = tracks[storm]
    return compute_district_risk(
        [d for d in dists if d["state_or_division"] == state],
        pd.DataFrame(m["track"]), state, m["peak_wind_kts"], m["min_pressure_mb"], fac,
    )


@pytest.mark.parametrize("kts,name", [
    (16, "Low Pressure Area"), (17, "Depression"), (28, "Deep Depression"),
    (34, "Cyclonic Storm"), (48, "Severe Cyclonic Storm"), (64, "Very Severe Cyclonic Storm"),
    (90, "Extremely Severe Cyclonic Storm"), (120, "Super Cyclonic Storm"),
])
def test_imd_wind_classes(kts, name):
    assert classify_imd_wind(kts) == name


@pytest.mark.parametrize("score,colour", [
    (0, "Green"), (29.9, "Green"), (30, "Yellow"), (49.9, "Yellow"),
    (50, "Orange"), (69.9, "Orange"), (70, "Red"), (100, "Red"),
])
def test_colour_bands(score, colour):
    assert colour_band(score)["colour"] == colour


def test_subscores_monotonic_and_bounded():
    winds = [wind_score(w) for w in range(0, 200, 5)]
    surges = [surge_score(s / 10) for s in range(0, 80)]
    assert winds == sorted(winds) and surges == sorted(surges)
    assert 0 <= min(winds) and max(winds) == 100 and max(surges) == 100
    assert composite_score(100, 100) == 100.0


def test_tier_matches_score_and_sorted():
    df = _run("REMAL", "West Bengal")
    assert df["vulnerability_score"].is_monotonic_decreasing
    for _, r in df.iterrows():
        assert r["imd_colour"] == colour_band(r["vulnerability_score"])["colour"]
        assert r["threat_tier"] == colour_band(r["vulnerability_score"])["tier"]


def test_nearer_track_scores_higher():
    df = _run("REMAL", "West Bengal").sort_values("closest_approach_km")
    assert df.iloc[0]["vulnerability_score"] >= df.iloc[-1]["vulnerability_score"]


def test_output_depends_on_storm_not_list_position():
    a = _run("REMAL", "West Bengal")
    b = _run("FANI", "Odisha")
    assert b["vulnerability_score"].max() > a["vulnerability_score"].max()
    g1, g2 = _run("TAUKTAE", "Gujarat"), _run("BIPARJOY", "Gujarat")
    assert g1.iloc[0]["district_name"] != g2.iloc[0]["district_name"]


def test_no_hardcoded_directive_text():
    for storm, state in [("REMAL", "West Bengal"), ("FANI", "Odisha")]:
        text = " ".join(_run(storm, state)["action_directive"])
        assert "NDRF boat teams" not in text and "within 6 hours" not in text


def test_facility_flags():
    wb = _run("REMAL", "West Bengal")
    assert wb["facility_data_available"].any()
    gj = _run("TAUKTAE", "Gujarat")
    assert not gj["facility_data_available"].any()
    assert (gj["flooded_hospitals"] == 0).all()


def test_missing_track_falls_back():
    _, dists, _ = _load()
    df = compute_district_risk(
        [d for d in dists if d["state_or_division"] == "Odisha"], pd.DataFrame(), "Odisha", 80.0, 960.0,
    )
    assert len(df) > 0 and df["vulnerability_score"].between(0, 100).all()
