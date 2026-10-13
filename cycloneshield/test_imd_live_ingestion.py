from unittest.mock import Mock, patch

import pandas as pd

from imd_live_ingestion import (
    _find_latest_imd_product,
    fetch_latest_imd_bulletin,
    parse_imd_published_track,
)


def test_find_latest_imd_product_uses_newest_dated_official_link():
    index_html = """
    <a href="download.php?path=uploads/archive/1/Tropical_Weather_Outlook_based_on_0300_UTC_of_12.10.2026.pdf">Old outlook</a>
    <a href="download.php?path=uploads/archive/2/Tropical_Weather_Outlook_based_on_0300_UTC_of_13.10.2026.pdf">Latest outlook</a>
    <a href="https://example.com/National_Bulletin_14.10.2026.pdf">Untrusted link</a>
    """

    product = _find_latest_imd_product(index_html)

    assert product is not None
    assert product["issued_at"] == "2026-10-13"
    assert product["product_type"] == "Tropical Weather Outlook"
    assert product["url"].startswith("https://rsmcnewdelhi.imd.gov.in/")
    assert "13.10.2026" in product["title"]


def test_parse_imd_published_track_keeps_explicit_waypoint_values():
    bulletin = """
    14.10.2026/1130 | 17.8 / 84.6 | 70 KNOTS | 978 HPA
    14.10.2026/1730 | 18.3 / 84.9 | 80 KNOTS | 970 HPA
    """

    track, meta = parse_imd_published_track(bulletin)

    assert track is not None
    assert len(track) == 2
    assert track.iloc[0]["time"] == pd.Timestamp("2026-10-14 11:30:00")
    assert track.iloc[1]["lat"] == 18.3
    assert track.iloc[1]["wind_kts"] == 80
    assert track.iloc[1]["pressure_mb"] == 970
    assert meta["total_observations"] == 2


def test_parse_imd_published_track_refuses_incomplete_or_single_waypoint():
    one_point = "14.10.2026/1130 | 17.8 / 84.6 | 70 KNOTS | 978 HPA"
    incomplete_points = """
    14.10.2026/1130 | 17.8 / 84.6 | 70 KNOTS
    14.10.2026/1730 | 18.3 / 84.9 | 80 KNOTS
    """

    track, _ = parse_imd_published_track(one_point)
    assert track is None

    track, meta = parse_imd_published_track(incomplete_points)
    assert track is None
    assert "dashboard track was not changed" in meta["track_status"]


def test_fetch_latest_imd_bulletin_loads_only_parsed_official_waypoints():
    product = {
        "title": "Tropical Weather Outlook 14.10.2026",
        "url": "https://rsmcnewdelhi.imd.gov.in/download.php?path=outlook.pdf",
        "issued_at": "2026-10-14",
        "product_type": "Tropical Weather Outlook",
    }
    response = Mock()
    response.content = b"%PDF-test"
    response.raise_for_status.return_value = None
    page = Mock()
    page.extract_text.return_value = """
    14.10.2026/1130 | 17.8 / 84.6 | 70 KNOTS | 978 HPA
    14.10.2026/1730 | 18.3 / 84.9 | 80 KNOTS | 970 HPA
    """

    with patch("imd_live_ingestion._fetch_latest_imd_product", return_value=product), patch(
        "imd_live_ingestion.requests.get", return_value=response
    ), patch("imd_live_ingestion.PdfReader") as pdf_reader:
        pdf_reader.return_value.pages = [page]
        track, meta = fetch_latest_imd_bulletin()

    assert track is not None
    assert len(track) == 2
    assert meta["source_url"] == product["url"]
    assert meta["data_source"].startswith("RSMC New Delhi")


def test_fetch_latest_imd_bulletin_leaves_track_empty_without_waypoints():
    product = {
        "title": "Tropical Weather Outlook 14.10.2026",
        "url": "https://rsmcnewdelhi.imd.gov.in/download.php?path=outlook.pdf",
        "issued_at": "2026-10-14",
        "product_type": "Tropical Weather Outlook",
    }
    response = Mock()
    response.content = b"%PDF-test"
    response.raise_for_status.return_value = None
    page = Mock()
    page.extract_text.return_value = "No complete forecast track is present in this outlook."

    with patch("imd_live_ingestion._fetch_latest_imd_product", return_value=product), patch(
        "imd_live_ingestion.requests.get", return_value=response
    ), patch("imd_live_ingestion.PdfReader") as pdf_reader:
        pdf_reader.return_value.pages = [page]
        track, meta = fetch_latest_imd_bulletin()

    assert track is None
    assert "dashboard track was not changed" in meta["track_status"]
