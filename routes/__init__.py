from .main import main_bp
from .vitals import vitals_bp
from .alerts import alerts_bp
from .thresholds import thresholds_bp
from .emergency import emergency_bp
from .predict import predict_bp
from .diet import diet_bp

__all__ = ["main_bp", "vitals_bp", "alerts_bp", "thresholds_bp", "emergency_bp", "predict_bp", "diet_bp"]
