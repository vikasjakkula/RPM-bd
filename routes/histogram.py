from flask import Blueprint, request, Response, jsonify

from services.histogram_service import build_histogram

histogram_bp = Blueprint("histogram", __name__)


@histogram_bp.route("/api/histogram", methods=["POST"])
def histogram():
    """
    Accept JSON: { "numbers": [1, 2, 3, ...], "title": "...", "xlabel": "...", "bins": 10 }.
    Returns PNG image of the histogram.
    """
    if not request.is_json:
        return jsonify(error="Content-Type must be application/json"), 400
    payload = request.get_json() or {}
    numbers = payload.get("numbers")
    if numbers is None:
        return jsonify(error="Missing 'numbers' array"), 400
    if not isinstance(numbers, (list, tuple)):
        return jsonify(error="'numbers' must be an array"), 400
    try:
        nums = [float(n) for n in numbers]
    except (TypeError, ValueError):
        return jsonify(error="All items in 'numbers' must be numeric"), 400
    if not nums:
        return jsonify(error="At least one number is required"), 400
    title = payload.get("title", "Distribution")
    xlabel = payload.get("xlabel", "Value")
    ylabel = payload.get("ylabel", "Frequency")
    bins = payload.get("bins")
    if bins is not None:
        try:
            bins = int(bins)
            bins = max(2, min(100, bins))
        except (TypeError, ValueError):
            bins = None
    try:
        png_bytes = build_histogram(
            nums,
            title=str(title),
            xlabel=str(xlabel),
            ylabel=str(ylabel),
            bins=bins,
        )
    except ValueError as e:
        return jsonify(error=str(e)), 400
    return Response(png_bytes, mimetype="image/png")
