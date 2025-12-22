import os
import sys
import json
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import google.generativeai as genai
from dominator_brain import strategic_intelligence_core, alchemy_fusion_core, WPIL_DOMINATOR_SYSTEM

app = Flask(__name__, template_folder="templates", static_folder="static")
CORS(app)

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
MODELS = ["gemini-2.0-flash-lite", "gemini-flash-latest"]

def get_ai_response(prompt: str) -> str:
    for model_name in MODELS:
        try:
            model = genai.GenerativeModel(model_name)
            return model.generate_content(prompt).text
        except: continue
    return "Error: AI Engines Busy."

# ========= نظام المقترحات الذهبية المحاكي (Ready for Apify) =========
def get_mock_gold_posts(niche):
    # هذه البيانات ستحل محلها بيانات Apify لاحقاً
    return [
        {"id": 1, "text": "السر في النجاح ليس العمل الجاد بل العمل الذكي...", "engagement": "150K", "time": "24h"},
        {"id": 2, "text": "لماذا فشلت 90% من الشركات الناشئة في 2025؟ إليكم الحقيقة...", "engagement": "80K", "time": "12h"}
    ]

# ========= المسارات الجديدة =========

@app.route("/")
def home(): return render_template("index.html")

@app.route("/alchemy/discover", methods=["POST"])
def discover_gold():
    data = request.get_json(silent=True) or {}
    niche = data.get("niche", "القيادة")
    
    # 1. سحب المنشورات الذهبية (محاكاة Apify)
    gold_posts = get_mock_gold_posts(niche)
    
    # 2. تشغيل مفاعل الاندماج
    fusion_data = alchemy_fusion_core(gold_posts, niche)
    
    # 3. تخليق المنشور الخارق
    super_post_text = get_ai_response(f"{WPIL_DOMINATOR_SYSTEM}\n{fusion_data['synthesis_task']}")
    
    return jsonify({
        "super_post": super_post_text,
        "score": fusion_data["dominance_score"],
        "sources": gold_posts,
        "trace": fusion_data["logic_trace"]
    }), 200

@app.route("/generate/<platform>", methods=["POST"])
def generate(platform):
    # ... (منطق التوليد العادي المصلح سابقاً لضمان الاستمرارية) ...
    data = request.get_json(force=True, silent=True) or {}
    idea = data.get('text') or data.get('idea') or ""
    brain = strategic_intelligence_core(idea, platform)
    output = get_ai_response(f"{WPIL_DOMINATOR_SYSTEM}\nالمهمة: {brain['transformed_input']}")
    return jsonify({"text": output, "trace": brain["logic_trace"]}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
