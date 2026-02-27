from flask import Blueprint, jsonify, request

from services.alert_engine import alert_engine

alerts_bp = Blueprint("alerts", __name__, url_prefix="/api/alerts")


@alerts_bp.route("")
def list_alerts():
    limit = request.args.get("limit", 20, type=int)
    limit = min(max(1, limit), 50)
    data = alert_engine.get_recent(limit=limit)
    return jsonify(data)
