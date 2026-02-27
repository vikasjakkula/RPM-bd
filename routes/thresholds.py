from flask import Blueprint, jsonify, request

from services.alert_engine import alert_engine

thresholds_bp = Blueprint("thresholds", __name__, url_prefix="/api/thresholds")


@thresholds_bp.route("", methods=["GET"])
def get_thresholds():
    return jsonify(alert_engine.get_thresholds())


@thresholds_bp.route("", methods=["PUT"])
def put_thresholds():
    data = request.get_json(silent=True) or {}
    allowed = {
        "heartRateHigh", "heartRateLow",
        "systolicHigh", "diastolicHigh", "diastolicLow",
    }
    updates = {k: int(v) for k, v in data.items() if k in allowed and isinstance(v, (int, float))}
    if not updates:
        return jsonify(alert_engine.get_thresholds())
    alert_engine.set_thresholds(updates)
    return jsonify(alert_engine.get_thresholds())
