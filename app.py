from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os
import google.generativeai as genai
from dominator_brain import strategic_intelligence_core, WPIL_DOMINATOR_SYSTEM
from sic_memory import record_success, record_failure

app = Flask(__name__, template_folder="templates", static_folder="static")
CORS(app)

# ========= Environment =========
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")

if not GEMINI_API_KEY:
    print("WARNING: GEMINI_API_KEY is missing.")
else:
    genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel(GEMINI_MODEL)


def get_safe_response(prompt: str) -> str:
    """
    Wrapper to call Gemini with a single prompt and return text safely.
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception:
        # Fallback (some SDK response shapes differ)
        try:
            return response.candidates[0].content.parts[0].text
        except Exception as e:
            return f"ERROR: Gemini call failed: {e}"


def normalize_platform(p: str) -> str:
    if not p:
        return ""
    p = p.strip().lower()
    # Common aliases from UI labels
    if p in {"x", "twitter"}:
        return "twitter"
    if p in {"ln", "linkedin"}:
        return "linkedin"
    if p in {"tt", "tiktok"}:
        return "tiktok"
    return p


def extract_from_request():
    """
    Reads JSON from request body safely:
    - idea: required
    - style: optional
    """
    data = request.get_json(silent=True) or {}
    idea = (data.get("idea") or "").strip()
    style = (data.get("style") or "").strip()
    return idea, style


def remix_winning_post(niche: str, seed: str):
    """
    Uses SIC to remix a 'winning post' using a niche + seed phrase.
    """
    niche = (niche or "").strip()
    seed = (seed or "").strip()

    if not niche or not seed:
        return jsonify({"error": "niche and seed are required"}), 400

    prompt = f"""
{WPIL_DOMINATOR_SYSTEM}

Task: Remix a proven "winning post" into a new post in Arabic with the same structure and persuasion.

Niche: {niche}
Seed (winning post idea/text): {seed}

Return:
1) LinkedIn post
2) X post
3) TikTok short script
"""
    # You already have strategic_intelligence_core; keep it in the loop
    # but here we directly generate output text; adjust as you prefer.
    out = get_safe_response(prompt).strip()

    return jsonify({"text": out, "niche": niche}), 200


# ========= UI =========
@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")


# ========= Diagnostics =========
@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "model": GEMINI_MODEL}), 200


@app.route("/__routes", methods=["GET"])
def __routes():
    """
    If this endpoint returns 404, you are NOT running Flask on Render
    (likely a Static Site or wrong start command/module).
    """
    rules = sorted([str(r) for r in app.url_map.iter_rules()])
    return jsonify({"routes": rules}), 200


# ========= API =========
@app.route("/remix", methods=["POST", "GET"], strict_slashes=False)
def remix_endpoint():
    if request.method == "GET":
        return jsonify({"error": "API endpoint", "hint": "Send POST with JSON: {niche, seed}"}), 400

    data = request.get_json(silent=True) or {}
    niche = data.get("niche", "")
    seed = data.get("seed", "")
    return remix_winning_post(niche, seed)


@app.route("/generate/<platform>", methods=["POST", "GET"], strict_slashes=False)
def generate_platform(platform):
    return execute_with_brain(platform)


@app.route("/generate/linkedin", methods=["POST", "GET"], strict_slashes=False)
def generate_linkedin():
    return execute_with_brain("linkedin")


@app.route("/generate/twitter", methods=["POST", "GET"], strict_slashes=False)
def generate_twitter():
    return execute_with_brain("twitter")


@app.route("/generate/tiktok", methods=["POST", "GET"], strict_slashes=False)
def generate_tiktok():
    return execute_with_brain("tiktok")


def execute_with_brain(requested_platform):
    requested_platform = normalize_platform(requested_platform)

    if request.method == "GET":
        return jsonify({"error": "API endpoint", "hint": "Send POST with JSON: {idea, style(optional)}"}), 400

    idea, style = extract_from_request()
    if not idea:
        return jsonify({"error": "Idea is required"}), 400

    try:
        # SIC builds the structured content
        result = strategic_intelligence_core(idea=idea, platform=requested_platform, style=style)

        # Build prompt for Gemini generation (text + optional video prompt)
        base_prompt = f"""
{WPIL_DOMINATOR_SYSTEM}

You are generating content in Arabic.

Platform: {requested_platform}
Style: {style or "default"}
Core idea: {idea}

SIC Output (use as guidance, do not dump raw unless appropriate):
{result}

Return the final content only.
"""

        generated_text = get_safe_response(base_prompt).strip()

        payload = {
            "platform": requested_platform,
            "idea": idea,
            "style": style,
            "text": generated_text
        }

        # TikTok extra: generate "video prompt" + "image prompt" if your UI expects it
        if requested_platform == "tiktok":
            video_prompt = get_safe_response(
                base_prompt + "\nAdditionally: Provide a concise cinematic video prompt for this script."
            ).strip()
            image_prompt = get_safe_response(
                base_prompt + "\nAdditionally: Provide a concise cinematic image prompt for the thumbnail."
            ).strip()
            payload["video_prompt"] = video_prompt
            payload["image_prompt"] = image_prompt

        record_success(requested_platform)
        return jsonify(payload), 200

    except Exception as e:
        record_failure(requested_platform)
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    # Local dev only. On Render use gunicorn.
    port = int(os.getenv("PORT", "5000"))
    app.run(host="0.0.0.0", port=port, debug=True)
