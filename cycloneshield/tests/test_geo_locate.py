"""Point-in-polygon tests for geo_locate against data/coastal_districts.geojson."""

import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from geo_locate import OUTSIDE_COVERAGE, load_districts, lookup_district  # noqa: E402

# (district, state/division, lat, lon): one point per district polygon. The polygons
# overlap; each point sits outside every other polygon, except Kolkata and Barguna,
# which are fully covered by others and resolve via the smallest-polygon rule.
KNOWN_POINTS = [
    ("South 24 Parganas", "West Bengal", 21.9, 88.5),
    ("North 24 Parganas", "West Bengal", 22.9, 88.7),
    ("Purba Medinipur", "West Bengal", 22.05, 87.7),
    ("Kolkata", "West Bengal", 22.55, 88.35),
    ("Howrah", "West Bengal", 22.45, 87.9),
    ("Puri", "Odisha", 19.95, 85.55),
    ("Jagatsinghpur", "Odisha", 20.05, 86.55),
    ("Kendrapara", "Odisha", 20.55, 86.6),
    ("Bhadrak", "Odisha", 21.0, 86.7),
    ("Balasore", "Odisha", 21.4, 86.95),
    ("Ganjam", "Odisha", 19.4, 84.75),
    ("Visakhapatnam", "Andhra Pradesh", 17.65, 83.2),
    ("Srikakulam", "Andhra Pradesh", 18.45, 84.3),
    ("Vizianagaram", "Andhra Pradesh", 18.5, 83.3),
    ("East Godavari", "Andhra Pradesh", 17.1, 82.15),
    ("Krishna", "Andhra Pradesh", 16.5, 81.0),
    ("Bapatla", "Andhra Pradesh", 16.0, 80.3),
    ("SPSR Nellore", "Andhra Pradesh", 14.5, 80.0),
    ("Chennai", "Tamil Nadu", 13.1, 80.25),
    ("Chengalpattu", "Tamil Nadu", 12.65, 80.05),
    ("Cuddalore", "Tamil Nadu", 11.65, 79.6),
    ("Nagapattinam", "Tamil Nadu", 10.65, 79.9),
    ("Thiruvarur", "Tamil Nadu", 10.65, 79.5),
    ("Ramanathapuram", "Tamil Nadu", 9.45, 78.8),
    ("Kutch", "Gujarat", 23.65, 69.55),
    ("Devbhumi Dwarka", "Gujarat", 22.35, 69.25),
    ("Jamnagar", "Gujarat", 22.35, 70.3),
    ("Porbandar", "Gujarat", 21.5, 69.65),
    ("Gir Somnath", "Gujarat", 20.9, 70.6),
    ("Bhavnagar", "Gujarat", 21.75, 72.0),
    ("Satkhira", "Khulna", 21.7, 89.25),
    ("Khulna", "Khulna", 22.3, 89.45),
    ("Bagerhat", "Khulna", 22.15, 89.7),
    ("Patuakhali", "Barisal", 22.15, 90.55),
    ("Barguna", "Barisal", 22.2, 90.2),
]


def test_known_points_cover_every_district() -> None:
    """The table above must list every polygon in the data file."""
    assert {p[0] for p in KNOWN_POINTS} == set(load_districts()["district_name"])


@pytest.mark.parametrize("district,state,lat,lon", KNOWN_POINTS)
def test_known_coordinate_maps_to_district(district: str, state: str, lat: float, lon: float) -> None:
    """Each sample coordinate resolves to its district and state."""
    result = lookup_district(lat, lon)
    assert result["district"] == district
    assert result["state"] == state


def test_outside_coverage_is_not_a_nearest_guess() -> None:
    """New Delhi is inland and far from every polygon."""
    result = lookup_district(28.6139, 77.2090)
    assert result["district"] == OUTSIDE_COVERAGE
    assert result["state"] is None
    assert result["candidates"] == []


def test_overlap_is_flagged_ambiguous() -> None:
    """A point in overlapping polygons reports every candidate."""
    result = lookup_district(22.55, 88.35)
    assert result["ambiguous"] is True
    assert "Kolkata" in result["candidates"]
