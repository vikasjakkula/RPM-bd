"""
Heart attack risk prediction: score from clinical + lifestyle factors, optional LLM summary.
"""
import logging
import os
from typing import Any

logger = logging.getLogger(__name__)

# Optional: set OPENAI_API_KEY (or OPENAI_BASE_URL for compatible APIs) in .env for LLM summary
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
OPENAI_BASE_URL = os.environ.get("OPENAI_BASE_URL")  # e.g. Azure or local proxy


def _float(value: Any, default: float = 0.0) -> float:
    if value is None or value == "":
        return default
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _int(value: Any, default: int = 0) -> int:
    if value is None or value == "":
        return default
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _bool(value: Any) -> bool:
    return bool(value)


def compute_risk_score(payload: dict) -> float:
    """
    Compute a 0–1 heart attack risk score from form inputs.
    Weights are heuristic and for demo; replace with a trained model in production.
    """
    age = _float(payload.get("age"), 50)
    sex = _int(payload.get("sex"), 0)  # 1 = male, 0 = female
    cholesterol = _float(payload.get("cholesterol"), 200)
    bp = _float(payload.get("bp"), 120)
    fbs = _bool(payload.get("fbs"))
    thalachh = _float(payload.get("thalachh"), 150)  # max heart rate

    diabetes = _bool(payload.get("diabetes"))
    obesity = _bool(payload.get("obesity"))
    shortness_of_breath = _bool(payload.get("shortness_of_breath"))
    chest_pain = _bool(payload.get("chest_pain"))
    sweating = _bool(payload.get("sweating"))
    stress = _bool(payload.get("stress"))
    poor_sleep = _bool(payload.get("poor_sleep"))
    smoking = _bool(payload.get("smoking"))

    score = 0.0

    # Age: 30–80 → ~0–0.25
    score += min(1.0, (age - 30) / 200) * 0.25

    # Sex: male adds a small amount
    if sex == 1:
        score += 0.05

    # Cholesterol: >200 adds risk
    if cholesterol >= 240:
        score += 0.15
    elif cholesterol >= 200:
        score += 0.08

    # Blood pressure: high adds risk
    if bp >= 160:
        score += 0.15
    elif bp >= 140:
        score += 0.10
    elif bp >= 130:
        score += 0.05

    # FBS (fasting blood sugar > 120)
    if fbs:
        score += 0.08

    # Max heart rate: lower can indicate stress/risk (normal ~220-age)
    if thalachh > 0 and thalachh < 120:
        score += 0.10
    elif thalachh > 0 and thalachh < 140:
        score += 0.04

    # Conditions and symptoms
    if diabetes:
        score += 0.10
    if obesity:
        score += 0.08
    if chest_pain:
        score += 0.12
    if shortness_of_breath:
        score += 0.06
    if sweating:
        score += 0.05
    if stress:
        score += 0.05
    if poor_sleep:
        score += 0.04
    if smoking:
        score += 0.10

    return min(1.0, max(0.0, score))


def get_llm_summary(
    risk_percentage: float,
    prediction: int,
    payload: dict,
) -> str | None:
    """
    Call an LLM to generate a short, non-diagnostic summary of the risk result.
    Returns None if no API key or on error.
    """
    if not OPENAI_API_KEY:
        return None

    try:
        import openai
        client = openai.OpenAI(
            api_key=OPENAI_API_KEY,
            base_url=OPENAI_BASE_URL or None,
        )
        risk_label = "elevated" if prediction == 1 else "lower"
        prompt = (
            "You are a health assistant. In one or two short, clear sentences, "
            "summarize this heart risk result in a supportive, non-alarming way. "
            "Do not diagnose or give medical advice. "
            f"Risk score: {risk_percentage:.1f}% ({risk_label} risk). "
            "Mention that the user should discuss with a doctor for any health decisions."
        )
        response = client.chat.completions.create(
            model=os.environ.get("OPENAI_MODEL", "gpt-4o-mini"),
            messages=[{"role": "user", "content": prompt}],
            max_tokens=120,
        )
        text = response.choices[0].message.content
        return text.strip() if text else None
    except Exception as e:
        logger.warning("LLM summary failed: %s", e)
        return None


def predict(payload: dict) -> dict:
    """
    Run heart risk prediction and optional LLM summary.
    Returns dict with prediction (0/1), probability, health_status, risk_percentage, llm_summary (if available).
    """
    probability = compute_risk_score(payload)
    threshold = 0.45
    prediction = 1 if probability >= threshold else 0
    risk_percentage = probability * 100

    if risk_percentage >= 60:
        health_status = "High Risk"
    elif risk_percentage >= 40:
        health_status = "Moderate Risk"
    else:
        health_status = "Low Risk"

    llm_summary = get_llm_summary(risk_percentage, prediction, payload)

    out = {
        "prediction": prediction,
        "probability": round(probability, 4),
        "health_status": health_status,
        "risk_percentage": round(risk_percentage, 2),
    }
    if llm_summary:
        out["llm_summary"] = llm_summary
    return out
