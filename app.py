import os
import sys
import json
import logging
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import google.generativeai as genai

# استيراد الدماغ
from dominator_brain import strategic_intelligence_core, WPIL_DOMINATOR_SYSTEM

app = Flask(__name__, template_folder="templates", static_folder="static")
CORS(app)
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger(__name__)

# إعداد AI مع مصفوفة التبديل (Failover)
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
MODELS = ["gemini-2.0-flash-lite", "gemini-flash-latest", "gemini-2.0-flash"]

def get_ai_response(prompt: str) -> str:
    for model_name in MODELS:
        try:
            model = genai.GenerativeModel(model_name)
            return model.generate_content(prompt).text
        except: continue
    return "⚠️ محرك الذكاء مشغولي حالياً. حاول بعد 30 ثانية."

def extract_ui_data():
    data = request.get_json(force=True, silent=True) or {}
    if request.form: data.update(request.form.to_dict())
    idea = data.get('text') or data.get('idea') or ""
    seed = data.get('winning_post') or data.get('seed') or ""
    style = data.get('style_dna') or "Professional"
    return str(idea).strip(), str(seed).strip(), str(style).strip()

@app.route("/")
def home(): return render_template("index.html")

@app.route("/generate/<platform>", methods=["POST", "GET"])
@app.route("/remix", methods=["POST", "GET"])
def handle_execution(platform="linkedin"):
    if request.method == "GET": return jsonify({"status": "ready"}), 200
    if request.path == "/remix": platform = "linkedin"

    idea, seed, style = extract_ui_data()
    if not (idea or seed): return jsonify({"error": "No input"}), 400

    try:
        brain = strategic_intelligence_core(idea, platform, style, seed)
        
        # التوليد النصي
        final_prompt = f"{WPIL_DOMINATOR_SYSTEM}\nالمهمة: {brain['transformed_input']}\nالمنصة: {platform}"
        text_raw = get_ai_response(final_prompt)
        
        # دمج التوقيع الفيروسي (تم إصلاح السطر المكسور هنا)
        signature = brain.get('viral_signature', '')
        final_text = f"{text_raw}{signature}"

        payload = {
            "platform": platform,
            "text": final_text,
            "trace": brain["logic_trace"],
            "remixed_seed": idea if idea else seed,
            "sic_transformed_input": brain['transformed_input']
        }

        if platform == "tiktok":
            v_prompt = "🚀 **VERTICAL 9:16 PROMPTS**\n\n"
            for seg in brain["video_segments"]:
                v_prompt += f"### {seg['time']}\n```text\n{seg['prompt']}\n```\n\n"
            payload["video_prompt"] = v_prompt

        return jsonify(payload), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
