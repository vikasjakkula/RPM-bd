from flask import Blueprint, jsonify, request

from services.emergency_workflow import emergency_workflow

emergency_bp = Blueprint("emergency", __name__, url_prefix="/api/emergency")


@emergency_bp.route("/trigger", methods=["POST"])
def trigger():
    data = request.get_json(silent=True) or {}
    alert = data.get("alert")
    source = data.get("source", "manual")
    result = emergency_workflow.trigger(alert=alert, source=source)
    return jsonify(result)
