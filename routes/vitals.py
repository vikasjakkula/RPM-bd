from flask import Blueprint, jsonify, request

from services.mock_stream import mock_stream_service

vitals_bp = Blueprint("vitals", __name__, url_prefix="/api/vitals")


@vitals_bp.route("/latest")
def latest():
    reading = mock_stream_service.get_latest()
    if reading is None:
        return jsonify(error="No vitals yet"), 404
    return jsonify(reading)


@vitals_bp.route("/history")
def history():
    limit = request.args.get("limit", 50, type=int)
    limit = min(max(1, limit), 100)
    data = mock_stream_service.get_history(limit=limit)
    return jsonify(data)
