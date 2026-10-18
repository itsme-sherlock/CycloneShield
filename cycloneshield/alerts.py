"""
CycloneShield - Pub/Sub alerts for CRITICAL / HIGH damage triage results.

Message body is JSON; message attributes (filterable by subscriptions) are:
    district, state, severity, location_source, photo_uri, assessment_source

Configuration (Streamlit secrets first, then environment variables):
    PUBSUB_TOPIC   topic id, or a full path ``projects/<p>/topics/<t>``
    GCP_PROJECT    project id (not needed with a full topic path)
    gcp_service_account / GOOGLE_APPLICATION_CREDENTIALS   as in evidence_store

Fails soft: missing config or credentials returns ``AlertResult(published=False, ...)``.
"""

import json
from dataclasses import dataclass
from typing import Any, Dict, Optional

from evidence_store import get_credentials, get_setting

ALERT_SEVERITIES = ("CRITICAL", "HIGH")


@dataclass
class AlertResult:
    """Outcome of an alert publish attempt."""

    published: bool
    message: str
    message_id: Optional[str] = None


def get_severity(triage: Dict[str, Any]) -> str:
    """Return the upper-cased threat tier, derived from severity_score if the tier is missing."""
    tier = str(triage.get("threat_tier") or "").strip().upper()
    if tier:
        return tier
    try:
        score = int(triage.get("severity_score", 0))
    except (TypeError, ValueError):
        return "UNKNOWN"
    return "CRITICAL" if score >= 5 else "HIGH" if score == 4 else "MODERATE" if score == 3 else "LOW"


def should_alert(triage: Dict[str, Any]) -> bool:
    """True for CRITICAL and HIGH results."""
    return get_severity(triage) in ALERT_SEVERITIES


def build_attributes(
    triage: Dict[str, Any], location: Dict[str, Any], photo_uri: Optional[str]
) -> Dict[str, str]:
    """Pub/Sub attributes (all strings, never empty)."""
    return {
        "district": str(location.get("district") or "unverified"),
        "state": str(location.get("state") or "unknown"),
        "severity": get_severity(triage),
        "location_source": str(location.get("location_source") or "unverified"),
        "photo_uri": photo_uri or "not_stored",
        "assessment_source": "gemini_live" if triage.get("is_live_api") else "offline_fallback",
    }


def _topic_path(topic: str) -> Optional[str]:
    """Resolve a topic id to a full path using GCP_PROJECT when needed."""
    if topic.startswith("projects/"):
        return topic
    project = get_setting("GCP_PROJECT")
    return f"projects/{project}/topics/{topic}" if project else None


def publish_alert(
    triage: Dict[str, Any], location: Dict[str, Any], photo_uri: Optional[str]
) -> AlertResult:
    """
    Publish an alert if severity is CRITICAL or HIGH.
    Never raises; returns ``AlertResult(published=False, ...)`` when skipped or failed.
    """
    if not should_alert(triage):
        return AlertResult(False, "Severity below alert threshold.")
    topic = get_setting("PUBSUB_TOPIC")
    if not topic:
        return AlertResult(False, "PUBSUB_TOPIC is not configured.")
    path = _topic_path(topic)
    if not path:
        return AlertResult(False, "GCP_PROJECT is not configured.")
    try:
        from google.cloud import pubsub_v1

        publisher = pubsub_v1.PublisherClient(credentials=get_credentials())
        attributes = build_attributes(triage, location, photo_uri)
        body = {
            "incident_id": triage.get("incident_id"),
            "damage_type": triage.get("damage_type"),
            "severity": attributes["severity"],
            "severity_score": triage.get("severity_score"),
            "confidence_score": triage.get("confidence_score"),
            "needs_human_confirmation": attributes["severity"] == "CRITICAL",
            "location": location,
            "photo_uri": photo_uri,
            "assessment_source": attributes["assessment_source"],
        }
        future = publisher.publish(
            path, json.dumps(body, default=str).encode("utf-8"), **attributes
        )
        return AlertResult(True, "Alert published.", future.result(timeout=10))
    except Exception as exc:
        return AlertResult(False, f"Pub/Sub publish failed ({type(exc).__name__}).")
