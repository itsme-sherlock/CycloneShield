"""
CycloneShield - Evidence storage in Google Cloud Storage.

Saves the damage photo and its triage JSON to:

    gs://<BUCKET>/<state>/<district>/<incident_id>/<timestamp>_photo.<ext>
    gs://<BUCKET>/<state>/<district>/<incident_id>/<timestamp>_triage.json

Unverified-location incidents go under ``_unverified/``; points outside every
district polygon go under ``_outside_coverage/``.

Configuration (Streamlit secrets first, then environment variables):
    GCS_BUCKET                       bucket name (required)
    gcp_service_account              secrets table with a service-account key (optional)
    GOOGLE_APPLICATION_CREDENTIALS   path to a key file / Application Default Credentials

Everything here fails soft: missing config or credentials returns a result with
``ok=False`` and a message; nothing raises into the UI.
"""

import json
import mimetypes
import os
import re
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, Optional

UNVERIFIED_PREFIX = "_unverified"
OUTSIDE_PREFIX = "_outside_coverage"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
try:
    from dotenv import load_dotenv
    for _env_path in [
        os.path.join(BASE_DIR, ".env"),
        os.path.join(os.path.dirname(BASE_DIR), ".env"),
    ]:
        if os.path.exists(_env_path):
            load_dotenv(_env_path)
except ImportError:
    pass


@dataclass
class StoreResult:
    """Outcome of an evidence upload."""

    ok: bool
    message: str
    photo_uri: Optional[str] = None
    triage_uri: Optional[str] = None


def get_setting(name: str) -> Optional[str]:
    """Return a setting from st.secrets, then os.environ, else None."""
    try:
        import streamlit as st
        if name in st.secrets:
            return str(st.secrets[name])
    except Exception:
        pass
    return os.environ.get(name) or None


def get_credentials() -> Any:
    """
    Service-account credentials from the ``gcp_service_account`` secrets table,
    or None to let Google libraries use Application Default Credentials.
    """
    try:
        import streamlit as st
        if "gcp_service_account" in st.secrets:
            from google.oauth2 import service_account
            return service_account.Credentials.from_service_account_info(
                dict(st.secrets["gcp_service_account"])
            )
    except Exception:
        pass
    return None


def new_incident_id() -> str:
    """Unique incident id, e.g. INC-20261018T033000Z-a1b2c3."""
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    return f"INC-{stamp}-{uuid.uuid4().hex[:6]}"


def _safe_segment(value: Optional[str]) -> str:
    """Make a string safe for use as one object-path segment."""
    cleaned = re.sub(r"[^A-Za-z0-9._-]+", "_", (value or "").strip()).strip("._")
    return cleaned or "unknown"


def build_prefix(location: Dict[str, Any], incident_id: str) -> str:
    """Object-path prefix for an incident, based on its location block."""
    district = location.get("district")
    state = location.get("state")
    if location.get("location_source") == "unverified" or not district:
        head = UNVERIFIED_PREFIX
    elif district == "outside coverage area":
        head = OUTSIDE_PREFIX
    else:
        head = f"{_safe_segment(state)}/{_safe_segment(district)}"
    return f"{head}/{_safe_segment(incident_id)}"


def save_incident(
    image_bytes: bytes,
    filename: str,
    triage: Dict[str, Any],
    location: Dict[str, Any],
    incident_id: str,
) -> StoreResult:
    """
    Upload the photo and triage JSON to Cloud Storage.
    Never raises; returns ``StoreResult(ok=False, ...)`` when not configured or on error.
    """
    bucket_name = get_setting("GCS_BUCKET")
    if not bucket_name:
        return StoreResult(False, "GCS_BUCKET is not configured.")
    try:
        from google.cloud import storage

        client = storage.Client(
            project=get_setting("GCP_PROJECT"), credentials=get_credentials()
        )
        bucket = client.bucket(bucket_name)

        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        prefix = build_prefix(location, incident_id)
        ext = os.path.splitext(filename or "")[1].lower() or ".jpg"
        content_type = mimetypes.guess_type(f"x{ext}")[0] or "image/jpeg"

        photo_blob = bucket.blob(f"{prefix}/{stamp}_photo{ext}")
        photo_blob.upload_from_string(image_bytes, content_type=content_type)
        photo_uri = f"gs://{bucket_name}/{photo_blob.name}"

        record = dict(triage)
        record["incident_id"] = incident_id
        record["location"] = location
        record["photo_uri"] = photo_uri
        record["stored_at"] = stamp
        triage_blob = bucket.blob(f"{prefix}/{stamp}_triage.json")
        triage_blob.upload_from_string(
            json.dumps(record, indent=2, default=str), content_type="application/json"
        )
        return StoreResult(
            True, "Stored in Cloud Storage.", photo_uri,
            f"gs://{bucket_name}/{triage_blob.name}",
        )
    except Exception as exc:
        return StoreResult(False, f"Cloud Storage upload failed ({type(exc).__name__}).")
