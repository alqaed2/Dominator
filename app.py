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
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
GEMINI_MODEL = os.environ.get('GEMINI_MODEL')

if not GEMINI_API_KEY:
    raise ValueError("❌ CRITICAL ERROR: GEMINI_API_KEY is missing.")

if not GEMINI_MODEL:
    raise ValueError("❌ CRITICAL ERROR: GEMINI_MODEL is missing.")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel(GEMINI_MODEL)

# -------------------------------------------------
# Helpers
# -------------------------------------------------
def extract(text, start, end):
    try:
        if not text:
            return ""
        p = re.escape(start) + r"(.*?)" + re.escape(end)
        m = re.search(p, text, re.DOTALL)
        return m.group(1).strip() if m else ""
    except:
        return ""

def get_safe_response(prompt):
    response = model.generate_content(prompt)
    if hasattr(response, 'text') and response.text:
        return response.text
    return response.candidates[0].content.parts[0].text

# -------------------------------------------------
# 🧠 Brain Payload Builder
# -------------------------------------------------
def build_brain_payload(topic, style_dna):
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
        "system_memory": {
            "historical_scores": {
                "linkedin": 0.7,
                "twitter": 0.8,
                "tiktok": 0.9
            }
        }
    }

# -------------------------------------------------
# Routes
# -------------------------------------------------
@app.route('/')
def home():
    return render_template('index.html')

# -------------------------------------------------
# LinkedIn (🧠 Controlled)
# -------------------------------------------------
@app.route('/generate/linkedin', methods=['POST'])
def generate_linkedin():
    return _execute_with_brain("linkedin")

# -------------------------------------------------
# Twitter (🧠 Controlled)
# -------------------------------------------------
@app.route('/generate/twitter', methods=['POST'])
def generate_twitter():
    return _execute_with_brain("twitter")

# -------------------------------------------------
# TikTok (🧠 Controlled)
# -------------------------------------------------
@app.route('/generate/tiktok', methods=['POST'])
def generate_tiktok():
    return _execute_with_brain("tiktok")

# -------------------------------------------------
# 🧠 Unified Execution Gate
# -------------------------------------------------
def _execute_with_brain(requested_platform):
    try:
        data = request.get_json(silent=True)
        if not data or 'text' not in data:
            return jsonify({"error": "No data provided"}), 400

        topic = data['text']
        style = data.get('style_dna', 'Professional')
        image_style = data.get('image_style', 'Default')

        # 🧠 Brain Decision
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
                "error": "Platform overridden by Strategic Intelligence Core",
                "requested": requested_platform,
                "approved": decision.get("primary_platform")
            }), 409

        # -------------------------------------------------
        # Prompt Routing
        # -------------------------------------------------
        if requested_platform == "linkedin":
            prompt = f"""
            Act as a LinkedIn Expert. Write a viral post about: {topic}
