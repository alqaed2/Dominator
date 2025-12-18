from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import os
import re

# 🧠 Strategic Intelligence Core
from dominator_brain import strategic_intelligence_core

# 🧠 Memory
from sic_memory import record_success, record_failure

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
# Brain Payload Builder (WPIL ENABLED)
# -------------------------------------------------
def build_brain_payload(raw_text: str, style_dna: str, wpil_signal: dict | None = None):
    return {
        "content_signal": {
            "topic": raw_text,
            "raw_text": raw_text,
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
        "wpil_signal": wpil_signal or {},
        "system_memory": {}
    }

# -------------------------------------------------
# Routes
# -------------------------------------------------
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/generate/<platform>", methods=["POST"])
def generate(platform):
    try:
        data = request.get_json(silent=True) or {}

        user_text = (data.get("text") or "").strip()
        if not user_text:
            return jsonify({"error": "text is required"}), 400

        style = data.get("style_dna", "Professional")
        image_style = data.get("image_style", "Default")

        # 🧠 WPIL INPUT (OPTIONAL)
        winning_posts = data.get("winning_posts", [])
        niche = data.get("niche", "general")

        wpil_signal = {
            "winning_posts": winning_posts,
            "niche": niche,
            "voice_profile": style
        } if winning_posts else {}

        # 1) SIC Decision
        decision = strategic_intelligence_core(
            build_brain_payload(
                raw_text=user_text,
                style_dna=style,
                wpil_signal=wpil_signal
            )
        )

        final_input = decision.get("transformed_input", user_text)

        # 2) Platform Generation
        if platform == "linkedin":
            prompt = (
                f"اكتب منشور LinkedIn احترافي عالي الانتشار.\n"
                f"الفكرة: {final_input}\n"
                f"الأسلوب: {style}\n"
                f"قيود: {decision['rules']}\n\n"
                f"---POST---\n"
                f"(النص)\n"
                f"---IMAGE---\n"
                f"(وصف صورة)"
            )

            txt = get_safe_response(prompt)
            record_success("linkedin")
            return jsonify({
                "text": extract(txt, "---POST---", "---IMAGE---"),
                "image": extract(txt, "---IMAGE---", ""),
                "meta": decision
            })

        if platform == "twitter":
            prompt = (
                f"اكتب Thread على X.\n"
                f"الفكرة: {final_input}\n"
                f"الأسلوب: {style}\n"
                f"قيود: {decision['rules']}\n\n"
                f"---THREAD---\n"
                f"(Thread)"
            )

            txt = get_safe_response(prompt)
            record_success("twitter")
            return jsonify({
                "text": extract(txt, "---THREAD---", ""),
                "meta": decision
            })

        if platform == "tiktok":
            prompt = (
                f"اكتب سكربت TikTok جذاب.\n"
                f"الفكرة: {final_input}\n"
                f"الأسلوب: {style}\n"
                f"قيود: {decision['rules']}\n\n"
                f"---SCRIPT---\n"
                f"(سكربت)\n"
                f"---COVER---\n"
                f"(صورة)"
            )

            txt = get_safe_response(prompt)
            record_success("tiktok")
            return jsonify({
                "text": extract(txt, "---SCRIPT---", "---COVER---"),
                "image": extract(txt, "---COVER---", ""),
                "meta": decision
            })

        record_failure(platform)
        return jsonify({"error": "Unsupported platform"}), 400

    except Exception as e:
        record_failure(platform)
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
