"""
Emergency workflow: triggered manually (demo) or by critical alerts.
Logs the event and returns a demo payload; can be extended with webhooks, DB, etc.
"""
import time
import logging

logger = logging.getLogger(__name__)


def trigger_emergency(alert: dict = None, source: str = "manual") -> dict:
    """
    Run emergency workflow. Optional alert dict when auto-triggered by critical event.
    Returns a demo payload for the API.
    """
    ts = int(time.time() * 1000)
    payload = {
        "triggered_at": ts,
        "source": source,
        "status": "triggered",
        "message": "Emergency workflow triggered",
        "alert": alert,
    }
    logger.warning("EMERGENCY WORKFLOW TRIGGERED: source=%s alert=%s", source, alert)
    # Extend here: call webhook, persist to DB, notify clinician, etc.
    return payload


emergency_workflow = type("EmergencyWorkflow", (), {"trigger": trigger_emergency})()
