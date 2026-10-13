"""
CycloneShield - Parametric Insurance Trigger & Payout Engine
=============================================================
Models parametric (trigger-based) insurance instruments for coastal India.
Unlike traditional indemnity insurance (which requires post-event damage assessment),
parametric insurance pays out automatically when measurable physical thresholds are
crossed — enabling IMMEDIATE pre-landfall or at-landfall liquidity deployment.

This module is 100% free-tier: pure Python + NumPy. No external API, no cloud billing.

Trigger Architecture:
  - Tier 1 (Watch):    Wind >= 34 kts   OR  Surge >= 0.5m   → Advisory payout: 10% of sum insured
  - Tier 2 (Alert):    Wind >= 48 kts   OR  Surge >= 1.0m   → Partial payout:   30% of sum insured
  - Tier 3 (Warning):  Wind >= 64 kts   OR  Surge >= 2.0m   → Major payout:     60% of sum insured
  - Tier 4 (Disaster): Wind >= 90 kts   OR  Surge >= 3.0m   → Full payout:     100% of sum insured

Reference:
  - World Bank PCRIC (Pacific Catastrophe Risk Insurance Company) parametric model
  - UNDP India Disaster Risk Financing framework for coastal states
  - Swiss Re Corporate Solutions: Agriculture & Coastal Parametric Products (South Asia)
"""

from __future__ import annotations
import math
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, field


# ---------------------------------------------------------------------------
# Parametric Trigger Thresholds
# ---------------------------------------------------------------------------

TRIGGER_TIERS: List[Dict[str, Any]] = [
    {
        "tier_id": 4,
        "tier_name": "DISASTER",
        "label": "Tier 4 — Full Payout Trigger",
        "wind_kts_threshold": 90.0,
        "surge_m_threshold": 3.0,
        "payout_pct": 1.00,
        "color": "#ef4444",
        "badge_class": "badge-critical",
        "description": "Super Cyclonic Storm / Extremely Severe. Catastrophic surge. Full 100% sum-insured payout.",
        "ndrf_implication": "All SDRF/NDRF reserves deployed. Mutual aid from neighbouring states triggered."
    },
    {
        "tier_id": 3,
        "tier_name": "WARNING",
        "label": "Tier 3 — Major Payout Trigger",
        "wind_kts_threshold": 64.0,
        "surge_m_threshold": 2.0,
        "payout_pct": 0.60,
        "color": "#f97316",
        "badge_class": "badge-high",
        "description": "Very Severe Cyclonic Storm. Structural damage to kachha dwellings. 60% payout triggers.",
        "ndrf_implication": "Pre-positioned NDRF battalions activated. District Collector declares Section 144."
    },
    {
        "tier_id": 2,
        "tier_name": "ALERT",
        "label": "Tier 2 — Partial Payout Trigger",
        "wind_kts_threshold": 48.0,
        "surge_m_threshold": 1.0,
        "payout_pct": 0.30,
        "color": "#f59e0b",
        "badge_class": "badge-moderate",
        "description": "Severe Cyclonic Storm. Coastal embankment overtopping expected. 30% payout triggers.",
        "ndrf_implication": "State Disaster Response Force (SDRF) mobilised. Highway toll plazas placed on standby."
    },
    {
        "tier_id": 1,
        "tier_name": "WATCH",
        "label": "Tier 1 — Advisory Payout Trigger",
        "wind_kts_threshold": 34.0,
        "surge_m_threshold": 0.5,
        "payout_pct": 0.10,
        "color": "#38bdf8",
        "badge_class": "badge-low",
        "description": "Cyclonic Storm. Gale-force winds and minor coastal flooding. Advisory 10% payout triggers.",
        "ndrf_implication": "SDMA issues Yellow Alert. Port closures and fishing boat harbour advisory."
    },
]

# Default sum insured (INR crore) per district for state disaster insurance pools
STATE_DEFAULT_SUM_INSURED_CR: Dict[str, float] = {
    "West Bengal": 500.0,
    "Odisha": 600.0,
    "Andhra Pradesh": 750.0,
    "Tamil Nadu": 800.0,
    "Gujarat": 700.0,
}

# SDRF (State Disaster Response Fund) allocation per state (INR crore, approximate 2023-24 values)
SDRF_CORPUS_CR: Dict[str, float] = {
    "West Bengal": 1242.0,
    "Odisha": 1056.0,
    "Andhra Pradesh": 1330.0,
    "Tamil Nadu": 1580.0,
    "Gujarat": 1445.0,
}


# ---------------------------------------------------------------------------
# Core Engine
# ---------------------------------------------------------------------------

@dataclass
class ParametricTriggerResult:
    """Result of a parametric insurance trigger evaluation."""
    active_tier: int
    tier_name: str
    tier_label: str
    trigger_source: str            # "wind" | "surge" | "combined" | "none"
    wind_kts: float
    surge_m: float
    payout_pct: float
    payout_amount_cr: float
    sum_insured_cr: float
    sdrf_corpus_cr: float
    sdrf_utilization_pct: float
    color: str
    badge_class: str
    description: str
    ndrf_implication: str
    is_triggered: bool
    time_to_payout_hours: int
    all_tiers_status: List[Dict[str, Any]] = field(default_factory=list)


def evaluate_parametric_trigger(
    wind_kts: float,
    surge_m: float,
    state_name: str = "Odisha",
    sum_insured_cr: Optional[float] = None,
    manual_payout_hours: int = 6
) -> ParametricTriggerResult:
    """
    Evaluate which parametric trigger tier is active based on current
    wind speed and storm surge measurements.

    Args:
        wind_kts: Current peak sustained wind speed in knots.
        surge_m: Predicted peak storm surge in metres.
        state_name: Indian coastal state (determines sum insured and SDRF corpus).
        sum_insured_cr: Override for sum insured in INR crore. If None, uses state default.
        manual_payout_hours: Hours from trigger confirmation to first payout transfer.

    Returns:
        ParametricTriggerResult dataclass with all trigger details.
    """
    si_cr = sum_insured_cr or STATE_DEFAULT_SUM_INSURED_CR.get(state_name, 500.0)
    sdrf_cr = SDRF_CORPUS_CR.get(state_name, 1000.0)

    # Evaluate tiers from highest to lowest
    active_tier_data = None
    trigger_source = "none"
    all_status = []

    for t in TRIGGER_TIERS:
        wind_triggered = wind_kts >= t["wind_kts_threshold"]
        surge_triggered = surge_m >= t["surge_m_threshold"]
        both_triggered = wind_triggered and surge_triggered

        if both_triggered:
            src = "combined"
        elif wind_triggered:
            src = "wind"
        elif surge_triggered:
            src = "surge"
        else:
            src = "none"

        is_met = (wind_triggered or surge_triggered)

        all_status.append({
            "tier_id": t["tier_id"],
            "tier_name": t["tier_name"],
            "label": t["label"],
            "wind_threshold": t["wind_kts_threshold"],
            "surge_threshold": t["surge_m_threshold"],
            "payout_pct": t["payout_pct"],
            "is_triggered": is_met,
            "trigger_source": src,
            "color": t["color"],
        })

        if is_met and active_tier_data is None:
            active_tier_data = t
            trigger_source = src

    if active_tier_data is None:
        # No trigger met — below Tier 1
        payout_pct = 0.0
        payout_cr = 0.0
        return ParametricTriggerResult(
            active_tier=0,
            tier_name="NO TRIGGER",
            tier_label="Below Tier 1 — No Payout",
            trigger_source="none",
            wind_kts=wind_kts,
            surge_m=surge_m,
            payout_pct=0.0,
            payout_amount_cr=0.0,
            sum_insured_cr=si_cr,
            sdrf_corpus_cr=sdrf_cr,
            sdrf_utilization_pct=0.0,
            color="#3b82f6",
            badge_class="badge-low",
            description="Storm below parametric trigger thresholds. Standard administrative watch level.",
            ndrf_implication="Normal administrative readiness. No special NDRF deployment required.",
            is_triggered=False,
            time_to_payout_hours=0,
            all_tiers_status=list(reversed(all_status))
        )

    payout_pct = active_tier_data["payout_pct"]
    payout_cr = round(si_cr * payout_pct, 2)
    sdrf_util_pct = round((payout_cr / sdrf_cr) * 100.0, 1) if sdrf_cr > 0 else 0.0

    return ParametricTriggerResult(
        active_tier=active_tier_data["tier_id"],
        tier_name=active_tier_data["tier_name"],
        tier_label=active_tier_data["label"],
        trigger_source=trigger_source,
        wind_kts=wind_kts,
        surge_m=surge_m,
        payout_pct=payout_pct,
        payout_amount_cr=payout_cr,
        sum_insured_cr=si_cr,
        sdrf_corpus_cr=sdrf_cr,
        sdrf_utilization_pct=sdrf_util_pct,
        color=active_tier_data["color"],
        badge_class=active_tier_data["badge_class"],
        description=active_tier_data["description"],
        ndrf_implication=active_tier_data["ndrf_implication"],
        is_triggered=True,
        time_to_payout_hours=manual_payout_hours,
        all_tiers_status=list(reversed(all_status))
    )


def compute_district_parametric_matrix(
    district_rows: list,
    base_wind_kts: float,
    base_surge_m: float,
    state_name: str,
    sum_insured_cr_per_district: float = 50.0
) -> List[Dict[str, Any]]:
    """
    Compute parametric insurance trigger status for every district in the vulnerability matrix.

    Args:
        district_rows: List of district dicts (from state_vuln_df).
        base_wind_kts: Cyclone peak wind speed (knots).
        base_surge_m: Peak predicted storm surge (metres).
        state_name: State for SDRF reference.
        sum_insured_cr_per_district: Sum insured (INR crore) per district.

    Returns:
        List of district parametric result dicts.
    """
    results = []
    for d in district_rows:
        # Adjust wind/surge based on district vulnerability score
        dist_score = float(d.get("vulnerability_score", 50.0))
        # Districts farther from core eyewall experience attenuated conditions
        attenuation = 0.5 + (dist_score / 200.0)  # 0.5 to 1.0 scaling
        eff_wind = round(base_wind_kts * attenuation, 1)
        eff_surge = round(base_surge_m * attenuation, 2)

        result = evaluate_parametric_trigger(
            wind_kts=eff_wind,
            surge_m=eff_surge,
            state_name=state_name,
            sum_insured_cr=sum_insured_cr_per_district
        )

        results.append({
            "district_name": d.get("district_name", "Unknown"),
            "population": d.get("population", 1000000),
            "threat_tier": d.get("threat_tier", "MODERATE"),
            "vulnerability_score": dist_score,
            "effective_wind_kts": eff_wind,
            "effective_surge_m": eff_surge,
            "insurance_trigger_tier": result.active_tier,
            "insurance_tier_name": result.tier_name,
            "payout_pct": result.payout_pct,
            "payout_amount_cr": result.payout_amount_cr,
            "trigger_source": result.trigger_source,
            "is_triggered": result.is_triggered,
            "ndrf_implication": result.ndrf_implication,
            "color": result.color,
        })
    return results


def get_aggregate_payout_summary(
    district_results: List[Dict[str, Any]],
    state_name: str
) -> Dict[str, Any]:
    """
    Compute state-level aggregate parametric insurance payout summary.
    """
    total_payout = sum(d["payout_amount_cr"] for d in district_results)
    triggered_count = sum(1 for d in district_results if d["is_triggered"])
    sdrf_cr = SDRF_CORPUS_CR.get(state_name, 1000.0)
    sdrf_util = round((total_payout / sdrf_cr) * 100.0, 1) if sdrf_cr > 0 else 0.0
    max_tier = max((d["insurance_trigger_tier"] for d in district_results), default=0)
    total_pop_triggered = sum(
        d["population"] for d in district_results if d["is_triggered"]
    )
    per_capita_cr = total_payout / (total_pop_triggered / 1e5) if total_pop_triggered > 0 else 0.0

    return {
        "state_name": state_name,
        "total_payout_cr": round(total_payout, 2),
        "total_payout_inr_bn": round(total_payout * 10, 2),   # INR crore → INR million
        "triggered_districts": triggered_count,
        "total_districts": len(district_results),
        "sdrf_corpus_cr": sdrf_cr,
        "sdrf_utilization_pct": sdrf_util,
        "max_active_tier": max_tier,
        "total_population_covered": total_pop_triggered,
        "payout_per_lakh_population_cr": round(per_capita_cr, 3),
        "is_sdrf_sufficient": total_payout <= sdrf_cr,
        "sdrf_gap_cr": max(0.0, round(total_payout - sdrf_cr, 2)),
    }
