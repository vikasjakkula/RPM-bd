"""
Heart risk classification using scikit-learn LogisticRegression.
Trained on synthetic data aligned with form features (suitable for scatter/feature analysis).
"""
import logging
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler

logger = logging.getLogger(__name__)

# Feature order for model (must match payload keys used in predict_service)
FEATURE_NAMES = [
    "age",
    "sex",
    "cholesterol",
    "bp",
    "fbs",
    "thalachh",
    "diabetes",
    "obesity",
    "shortness_of_breath",
    "chest_pain",
    "sweating",
    "stress",
    "poor_sleep",
    "smoking",
]

_model = None
_scaler = None


def _synthetic_label(row: np.ndarray) -> int:
    """Synthetic risk rule so the dataset has a learnable structure (for scatter/ML)."""
    age, sex, chol, bp, fbs, thalach, diab, obe, sob, cp, sw, stress, sleep, smoke = row
    score = 0.0
    if age >= 55:
        score += 0.25
    elif age >= 45:
        score += 0.12
    if sex == 1:
        score += 0.05
    if chol >= 240:
        score += 0.2
    elif chol >= 200:
        score += 0.1
    if bp >= 160:
        score += 0.2
    elif bp >= 140:
        score += 0.12
    if fbs:
        score += 0.1
    if thalach > 0 and thalach < 120:
        score += 0.15
    elif thalach > 0 and thalach < 140:
        score += 0.05
    if diab:
        score += 0.12
    if obe:
        score += 0.08
    if cp:
        score += 0.15
    if sob:
        score += 0.06
    if sw:
        score += 0.05
    if stress:
        score += 0.04
    if sleep:
        score += 0.03
    if smoke:
        score += 0.12
    return 1 if score >= 0.45 else 0


def _build_synthetic_data(n_samples: int = 800, seed: int = 42) -> tuple[np.ndarray, np.ndarray]:
    rng = np.random.default_rng(seed)
    X = np.zeros((n_samples, len(FEATURE_NAMES)))
    X[:, 0] = rng.integers(25, 85, size=n_samples)  # age
    X[:, 1] = rng.integers(0, 2, size=n_samples)  # sex
    X[:, 2] = rng.integers(150, 320, size=n_samples)  # cholesterol
    X[:, 3] = rng.integers(100, 180, size=n_samples)  # bp (systolic proxy)
    X[:, 4] = rng.integers(0, 2, size=n_samples)  # fbs
    X[:, 5] = rng.integers(90, 200, size=n_samples)  # thalachh
    for j in range(6, 14):
        X[:, j] = rng.integers(0, 2, size=n_samples)
    y = np.array([_synthetic_label(X[i]) for i in range(n_samples)])
    return X, y


def _get_model():
    global _model, _scaler
    if _model is not None:
        return _model, _scaler
    X, y = _build_synthetic_data()
    _scaler = StandardScaler()
    X_scaled = _scaler.fit_transform(X)
    _model = LogisticRegression(max_iter=500, random_state=42)
    _model.fit(X_scaled, y)
    logger.info("Heart risk LogisticRegression model fitted on synthetic data.")
    return _model, _scaler


def payload_to_features(payload: dict) -> np.ndarray:
    """Convert API payload to feature vector in FEATURE_NAMES order."""
    def _float(k, default=0.0):
        v = payload.get(k, default)
        if v is None or v == "":
            return default
        try:
            return float(v)
        except (TypeError, ValueError):
            return default

    def _int(k, default=0):
        v = payload.get(k, default)
        if v is None or v == "":
            return default
        try:
            return int(v)
        except (TypeError, ValueError):
            return default

    def _bool(k):
        v = payload.get(k)
        return 1.0 if v else 0.0

    return np.array([
        _float("age", 50),
        _float("sex", 0),
        _float("cholesterol", 200),
        _float("bp", 120),
        _bool("fbs"),
        _float("thalachh", 150),
        _bool("diabetes"),
        _bool("obesity"),
        _bool("shortness_of_breath"),
        _bool("chest_pain"),
        _bool("sweating"),
        _bool("stress"),
        _bool("poor_sleep"),
        _bool("smoking"),
    ], dtype=np.float64).reshape(1, -1)


def predict_proba(payload: dict) -> float:
    """Return P(risk=1) in [0, 1]."""
    model, scaler = _get_model()
    x = payload_to_features(payload)
    x_scaled = scaler.transform(x)
    return float(model.predict_proba(x_scaled)[0, 1])
