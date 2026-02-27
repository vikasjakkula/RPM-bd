"""
Heart attack risk prediction: scikit-learn LogisticRegression + optional LLM summary.
"""
import logging
import os

from services.heart_risk_model import predict_proba as model_predict_proba

logger = logging.getLogger(__name__)
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
OPENAI_BASE_URL = os.environ.get("OPENAI_BASE_URL")

# Global to store the most recent prediction for health check/monitoring
LATEST_RESULT = {"status": "No prediction yet"}


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
    Run heart risk prediction (scikit-learn) and optional LLM summary.
    Returns dict with prediction (0/1), probability, health_status, risk_percentage, llm_summary (if available).
    """
    probability = model_predict_proba(payload)
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
    
    global LATEST_RESULT
    LATEST_RESULT = out
    
    return out
