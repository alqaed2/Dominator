import os
import sys
import json
import logging
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import google.generativeai as genai
from dominator_brain import strategic_intelligence_core, alchemy_fusion_core, WPIL_DOMINATOR_SYSTEM

app = Flask(__name__, template_folder="templates", static_folder="static")
CORS(app)
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger(__name__)

# إعداد AI مع مصفوفة التبديل لتفادي خطأ 429
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

MODELS_PRIORITY = ["gemini-2.0-flash-lite", "gemini-flash-latest", "gemini-2.0-flash"]

def get_ai_response(prompt: str) -> str:
    for model_name in MODELS_PRIORITY:
        try:
            model = genai.GenerativeModel(model_name)
            return model.generate_content(prompt).text
        except Exception as e:
            logger.warning(f"Model {model_name} failed. Trying next...")
            continue
    return "⚠️ جميع المحركات مشغولة حالياً. حاول بعد قليل."

def extract_ui_data():
    data = request.get_json(force=True, silent=True) or {}
    if request.form: data.update(request.form.to_dict())
    idea = data.get('text') or data.get('idea') or ""
    seed = data.get('winning_post') or data.get('seed') or ""
    style = data.get('style_dna') or "Professional"
    return str(idea).strip(), str(seed).strip(), str(style).strip()

# محاكاة لبيانات Apify (سيتم ربط الـ API الحقيقي هنا بمجرد إضافة المفتاح لـ Render)
def get_gold_posts_logic(niche):
    return [
        {"text": f"لماذا يسيطر الـ AI على مجال {niche}؟ إليك 5 أسباب صادمة.", "engagement": "120K", "platform": "X"},
        {"text": f"دليل الهيمنة الشامل في {niche} لعام 2026. لا تغلق الفيديو.", "engagement": "250K", "platform": "TikTok"}
    ]

@app.route("/")
def home(): return render_template("index.html")

@app.route("/alchemy/discover", methods=["POST"])
def discover_gold():
    data = request.get_json(silent=True) or {}
    niche = data.get("niche", "القيادة")
    gold_posts = get_gold_posts_logic(niche)
    fusion_data = alchemy_fusion_core(gold_posts, niche)
    super_post_text = get_ai_response(f"{WPIL_DOMINATOR_SYSTEM}\n{fusion_data['synthesis_task']}")
    return jsonify({
        "super_post": super_post_text,
        "score": fusion_data["dominance_score"],
        "sources": gold_posts,
        "trace": fusion_data["logic_trace"]
    }), 200

@app.route("/generate/<platform>", methods=["POST", "GET"])
@app.route("/remix", methods=["POST", "GET"])
def handle_execution(platform="linkedin"):
    if request.path == "/remix": platform = "linkedin"
    idea, seed, style = extract_ui_data()
    if not (idea or seed): return jsonify({"error": "No input"}), 400
    try:
        brain = strategic_intelligence_core(idea, platform, style, seed)
        final_prompt = f"{WPIL_DOMINATOR_SYSTEM}\nالمنصة: {platform}\nالمهمة: {brain['transformed_input']}"
        text_raw = get_ai_response(final_prompt)
        final_text = f"{text_raw}{brain.get('viral_signature', '')}"
        
        payload = {
            "platform": platform, "text": final_text, "trace": brain["logic_trace"],
            "remixed_seed": idea if idea else seed,
            "sic_transformed_input": brain['transformed_input']
        }
        if platform == "tiktok":
            v_prompt = "🚀 **VERTICAL 9:16 CINEMATIC PROMPTS**\n\n"
            for seg in brain["video_segments"]:
                v_prompt += f"### {seg['time']}\n```text\n{seg['prompt']}\n```\n\n"
            payload["video_prompt"] = v_prompt
        return jsonify(payload), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
