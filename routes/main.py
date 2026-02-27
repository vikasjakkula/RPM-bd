from flask import Blueprint, jsonify

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    return jsonify({
        "status": "online",
        "service": "RPM Backend",
        "documentation": "/health, /api/health, /predict, /api/vitals/latest"
    })


@main_bp.route("/health")
@main_bp.route("/api/health")
def health():
    from services.predict_service import LATEST_RESULT
    return jsonify(ok=True, message="RPM Backend is running", port=5000, last_prediction=LATEST_RESULT)


@main_bp.route("/api/hello")
def hello():
    return jsonify(message="Hello from API!")


@main_bp.route("/api/ping")
def ping():
    import time
    return jsonify(pong=int(time.time() * 1000))
