from flask import Blueprint, jsonify, request

from services.predict_service import predict as run_predict

predict_bp = Blueprint("predict", __name__)


@predict_bp.route("/predict", methods=["POST"])
def predict():
    """Heart attack risk prediction from form data. Returns prediction, probability, health_status, risk_percentage, optional llm_summary."""
    if not request.is_json:
        return jsonify(error="Content-Type must be application/json"), 400
    payload = request.get_json() or {}
    try:
        result = run_predict(payload)
        return jsonify(result)
    except Exception as e:
        return jsonify(error=str(e)), 500
