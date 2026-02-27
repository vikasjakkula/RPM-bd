"""
Threshold-based alert detection. Evaluates each vital reading against
configurable thresholds and maintains a list of recent alerts.
"""
from collections import deque
from threading import Lock
import time

DEFAULT_THRESHOLDS = {
    "heartRateHigh": 120,
    "heartRateLow": 50,
    "systolicHigh": 180,
    "diastolicHigh": 120,
    "diastolicLow": 60,
}

ALERTS_BUFFER_SIZE = 50
ALERTS_MAX_AGE_MS = 60 * 1000  # 1 minute


def detect_alerts(reading: dict, thresholds: dict) -> list:
    """Compare one reading to thresholds; return list of alert dicts."""
    alerts = []
    ts = int(time.time() * 1000)
    hr_high = thresholds.get("heartRateHigh", DEFAULT_THRESHOLDS["heartRateHigh"])
    hr_low = thresholds.get("heartRateLow", DEFAULT_THRESHOLDS["heartRateLow"])
    sys_high = thresholds.get("systolicHigh", DEFAULT_THRESHOLDS["systolicHigh"])
    dia_high = thresholds.get("diastolicHigh", DEFAULT_THRESHOLDS["diastolicHigh"])
    dia_low = thresholds.get("diastolicLow", DEFAULT_THRESHOLDS["diastolicLow"])

    hr = reading.get("heartRate")
    if hr is not None:
        if hr >= hr_high:
            alerts.append({
                "type": "heartRate",
                "message": f"High heart rate: {hr} BPM",
                "severity": "critical",
                "timestamp": ts,
                "value": hr,
                "threshold": hr_high,
            })
        if hr <= hr_low:
            alerts.append({
                "type": "heartRate",
                "message": f"Low heart rate: {hr} BPM",
                "severity": "critical",
                "timestamp": ts,
                "value": hr,
                "threshold": hr_low,
            })

    systolic = reading.get("systolic")
    if systolic is not None and systolic >= sys_high:
        alerts.append({
            "type": "bloodPressure",
            "message": f"High systolic: {systolic} mmHg",
            "severity": "critical",
            "timestamp": ts,
            "value": systolic,
            "threshold": sys_high,
        })

    diastolic = reading.get("diastolic")
    if diastolic is not None:
        if diastolic >= dia_high:
            alerts.append({
                "type": "bloodPressure",
                "message": f"High diastolic: {diastolic} mmHg",
                "severity": "critical",
                "timestamp": ts,
                "value": diastolic,
                "threshold": dia_high,
            })
        if dia_low and diastolic <= dia_low:
            alerts.append({
                "type": "bloodPressure",
                "message": f"Low diastolic: {diastolic} mmHg",
                "severity": "warning",
                "timestamp": ts,
                "value": diastolic,
                "threshold": dia_low,
            })

    spo2 = reading.get("bloodOxygen")
    if spo2 is not None and spo2 < 92:
        alerts.append({
            "type": "bloodOxygen",
            "message": f"Low SpO2: {spo2}%",
            "severity": "critical",
            "timestamp": ts,
            "value": spo2,
            "threshold": 92,
        })

    return alerts


class AlertEngine:
    def __init__(self, buffer_size: int = ALERTS_BUFFER_SIZE, max_age_ms: int = ALERTS_MAX_AGE_MS):
        self._alerts: deque = deque(maxlen=buffer_size)
        self._lock = Lock()
        self._max_age_ms = max_age_ms
        self._thresholds = dict(DEFAULT_THRESHOLDS)
        self._on_critical = None  # optional callback for auto emergency trigger

    def set_thresholds(self, thresholds: dict):
        with self._lock:
            self._thresholds.update(thresholds)

    def get_thresholds(self) -> dict:
        with self._lock:
            return dict(self._thresholds)

    def set_on_critical(self, callback):
        """Set callback(alert) when a critical alert is added (e.g. trigger emergency)."""
        self._on_critical = callback

    def evaluate(self, reading: dict) -> list:
        """Evaluate reading, append new alerts, return new alerts."""
        with self._lock:
            th = dict(self._thresholds)
        new_alerts = detect_alerts(reading, th)
        if not new_alerts:
            return []
        now = int(time.time() * 1000)
        with self._lock:
            for a in new_alerts:
                self._alerts.append(a)
                if a.get("severity") == "critical" and self._on_critical:
                    try:
                        self._on_critical(a)
                    except Exception:
                        pass
            # drop too-old alerts
            while self._alerts and (now - self._alerts[0]["timestamp"]) > self._max_age_ms:
                self._alerts.popleft()
        return new_alerts

    def get_recent(self, limit: int = 20) -> list:
        with self._lock:
            return list(self._alerts)[-limit:]


alert_engine = AlertEngine()
