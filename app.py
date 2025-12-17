from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import os
import re

# 🧠 Strategic Intelligence Core
from dominator_brain import strategic_intelligence_core

app = Flask(__name__)

# -------------------------------------------------
# Environment Configuration
# -------------------------------------------------
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
GEMINI_MODEL = os.environ.get("GEMINI_MODEL")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY missing")

if not GEMINI_MODEL:
    raise ValueError("GEMINI_MODEL missing")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel(GEMINI_MODEL)

# -------------------------------------------------
# Helpers
# -------------------------------------------------
def extract(text, start, end):
    if not text:
        return ""
    m = re.search(re.escape(start) + r"(.*?)" + re.escape(end), text, re.DOTALL)
    return m.group(1).strip() if m else ""

def get_safe_response(prompt: str) -> str:
    response = model.generate_content(prompt)
    if hasattr(response, "text") and response.text:
        return response.text
    return response.candidates[0].content.parts[0].text

# -------------------------------------------------
# Brain Payload Builder
# -------------------------------------------------
def build_brain_payload(topic: str, style_dna: str):
    return {
        "content_signal": {
            "topic": topic,
            "raw_text": topic,
            "intent": "dominate"
        },
        "style_signal": {
            "style_dna": style_dna,
            "confidence_level": 0.9
        },
        "context_signal": {
            "platforms_available": ["linkedin", "twitter", "tiktok"],
            "time_context": "now"
        },
        "system_memory": {}
    }

# -------------------------------------------------
# Routes
# -------------------------------------------------
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/generate/linkedin", methods=["POST"])
def generate_linkedin():
    return execute_with_brain("linkedin")

@app.route("/generate/twitter", methods=["POST"])
def generate_twitter():
    return execute_with_brain("twitter")

@app.route("/generate/tiktok", methods=["POST"])
def generate_tiktok():
    return execute_with_brain("tiktok")

# -------------------------------------------------
# 🧠 Unified Execution Gate
# -------------------------------------------------
def execute_with_brain(requested_platform: str):
    try:
        data = request.get_json(silent=True)
        if not data or "text" not in data:
            return jsonify({"error": "No data provided"}), 400

        topic = data["text"]
        style = data.get("style_dna", "Professional")
        image_style = data.get("image_style", "Default")

        decision = strategic_intelligence_core(
            build_brain_payload(topic, style)
        )

        if not decision.get("execute"):
            return jsonify({
                "error": "Blocked by Strategic Intelligence Core",
                "reason": decision.get("decision_reason")
            }), 403

        if decision.get("primary_platform") != requested_platform:
            return jsonify({
                "error": "Platform overridden by SIC",
                "approved": decision.get("primary_platform")
            }), 409

        if requested_platform == "linkedin":
            prompt = (
                f"Act as a LinkedIn Expert.\n"
                f"Write a viral post about: {topic}\n"
                f"Style: {style}\n"
                f"Image Style: {image_style}\n\n"
                f"---LINKEDIN_START---\n"
                f"(Content)\n"
                f"---LINKEDIN_END---\n"
                f"---IMAGE_MAIN_START---\n"
                f"(Image Prompt)\n"
                f"---IMAGE_MAIN_END---"
            )

            text = get_safe_response(prompt)
            return jsonify({
                "text": extract(text, "---LINKEDIN_START---", "---LINKEDIN_END---"),
                "image": extract(text, "---IMAGE_MAIN_START---", "---IMAGE_MAIN_END---")
            })

        if requested_platform == "twitter":
            prompt = (
                f"Act as a Twitter Expert.\n"
                f"Write a 5-tweet thread about: {topic}\n"
                f"Style: {style}\n\n"
                f"---TWITTER_START---\n"
                f"(Thread)\n"
                f"---TWITTER_END---"
            )

            text = get_safe_response(prompt)
            return jsonify({
                "text": extract(text, "---TWITTER_START---", "---TWITTER_END---")
            })

        if requested_platform == "tiktok":
            prompt = (
                f"Act as a TikTok Director.\n"
                f"Write a script for: {topic}\n"
                f"Style: {style}\n"
                f"Image Style: {image_style}\n\n"
                f"---TIKTOK_START---\n"
                f"(Script)\n"
                f"---TIKTOK_END---\n"
                f"---VIDEO_PROMPT_START---\n"
                f"(Video Prompt)\n"
                f"---VIDEO_PROMPT_END---"
            )

            text = get_safe_response(prompt)
            return jsonify({
                "text": extract(text, "---TIKTOK_START---", "---TIKTOK_END---"),
                "video_prompt": extract(text, "---VIDEO_PROMPT_START---", "---VIDEO_PROMPT_END---")
            })

        return jsonify({"error": "Unsupported platform"}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
