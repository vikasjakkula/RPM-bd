from flask import Blueprint, jsonify

main_bp = Blueprint("main", __name__)


@main_bp.route("/health")
def health():
    return jsonify(ok=True, message="API is running")


@main_bp.route("/api/hello")
def hello():
    return jsonify(message="Hello from API!")


@main_bp.route("/api/ping")
def ping():
    import time
    return jsonify(pong=int(time.time() * 1000))
