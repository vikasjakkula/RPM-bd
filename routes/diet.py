from flask import Blueprint, jsonify, request

diet_bp = Blueprint("diet", __name__)

DIET_RECOMMENDATIONS = {
    "Low Risk": {
        "summary": "Maintain your healthy lifestyle with a balanced diet.",
        "items": [
            "Keep consuming whole grains and lean proteins.",
            "Maintain moderate sodium intake.",
            "Stay hydrated with 8+ glasses of water daily.",
            "Incorporate a variety of colorful vegetables."
        ]
    },
    "Moderate Risk": {
        "summary": "Focus on heart-healthy adjustments to reduce your risk factors.",
        "items": [
            "Increase fiber intake through legumes and oats.",
            "Replace saturated fats with healthy fats (nuts, avocado, olive oil).",
            "Reduce processed sugar and refined carbohydrates.",
            "Limit sodium to less than 2,300mg per day."
        ]
    },
    "High Risk": {
        "summary": "Strict cardiovascular-focused diet is recommended. Consult a specialist.",
        "items": [
            "Strict low-sodium (DASH) diet: < 1,500mg per day.",
            "Eliminate trans fats and highly processed meats.",
            "Focus on Omega-3 rich foods like salmon or flaxseeds.",
            "Prioritize plant-based meals multiple times a week."
        ]
    }
}

@diet_bp.route("/api/diet", methods=["POST"])
def get_diet():
    """Returns diet recommendations based on health_status or risk_percentage."""
    data = request.get_json() or {}
    health_status = data.get("health_status", "Low Risk")
    
    # Fallback/Mapping if risk_percentage is provided instead
    if "risk_percentage" in data and "health_status" not in data:
        try:
            risk = float(data["risk_percentage"])
            if risk >= 60: health_status = "High Risk"
            elif risk >= 40: health_status = "Moderate Risk"
            else: health_status = "Low Risk"
        except (ValueError, TypeError):
            health_status = "Low Risk"

    recommendation = DIET_RECOMMENDATIONS.get(health_status, DIET_RECOMMENDATIONS["Low Risk"])
    return jsonify({
        "status": "success",
        "health_status": health_status,
        "diet_plan": recommendation
    })