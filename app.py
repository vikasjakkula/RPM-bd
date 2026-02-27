"""
Remote Patient Monitoring (RPM) IoT Agent – Flask backend.
Mock IoT stream, threshold-based alerts, emergency workflow.
"""
import logging
from flask import Flask
from flask_cors import CORS

from config import Config
from routes import main_bp, vitals_bp, alerts_bp, thresholds_bp, emergency_bp, predict_bp
from services.mock_stream import mock_stream_service
from services.alert_engine import alert_engine
from services.emergency_workflow import emergency_workflow

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def _on_reading(reading):
    alert_engine.evaluate(reading)


def _on_critical(alert):
    emergency_workflow.trigger(alert=alert, source="critical_alert")


def create_app(config=None):
    app = Flask(__name__)
    app.config.from_object(config or Config)
    CORS(app, origins=app.config.get("CORS_ORIGINS") if isinstance(app.config.get("CORS_ORIGINS"), list) else "*")
    app.register_blueprint(main_bp)
    app.register_blueprint(vitals_bp)
    app.register_blueprint(alerts_bp)
    app.register_blueprint(thresholds_bp)
    app.register_blueprint(emergency_bp)
    app.register_blueprint(predict_bp)
    return app


app = create_app()


@app.before_request
def ensure_stream_started():
    if not mock_stream_service._running:
        alert_engine.set_on_critical(_on_critical)
        mock_stream_service.start(on_reading=_on_reading)
        logger.info("Mock IoT vitals stream started.")


if __name__ == "__main__":
    port = Config.PORT
    app.run(host="0.0.0.0", port=port, debug=Config.DEBUG, threaded=True)
