import os
import requests
import time
import logging
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import google.generativeai as genai

# استيراد النواة السيادية
from dominator_brain import strategic_intelligence_core, alchemy_fusion_core, WPIL_DOMINATOR_SYSTEM

app = Flask(__name__, template_folder="templates", static_folder="static")
CORS(app)
logger = logging.getLogger(__name__)

# ========= ترسانة موديلات 2025 المختارة من قائمتك المتاحة =========
MODELS_POOL = [
    "gemini-2.5-flash",
    "gemini-2.5-flash-lite",
    "gemini-2.0-flash-lite-001",
    "gemini-flash-latest",
    "gemini-pro-latest"
]

GENAI_KEY = os.getenv("GEMINI_API_KEY")
APIFY_KEY = os.getenv("APIFY_API_KEY")

if GENAI_KEY:
    genai.configure(api_key=GENAI_KEY)

def get_ai_response_nebula(prompt: str) -> str:
    """
    بروتوكول Nebula: التبديل التلقائي القسري بين الموديلات في حال انتهاء الحصة (Quota)
    """
    last_error = ""
    for model_name in MODELS_POOL:
        try:
            print(f"📡 [COMMAND] Deploying model: {model_name}")
            model = genai.GenerativeModel(model_name)
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            last_error = str(e)
            print(f"⚠️ [WARNING] Model {model_name} failed. Error: {last_error[:50]}...")
            # إذا كان الخطأ متعلق بالحصة (429) أو عدم التوفر (404/500)، ننتقل فوراً
            continue
            
    return f"🚨 كافة خطوط الاتصال العصبية مشغولة. آخر إشعار: {last_error}"

def fetch_real_gold_posts(niche):
    if APIFY_KEY:
        try:
            url = f"https://api.apify.com/v2/acts/apidojo~tweet-scraper/run-sync-get-dataset-items?token={APIFY_KEY}"
            res = requests.post(url, json={"searchTerms": [niche], "maxTweets": 5, "searchMode": "top"}, timeout=15)
            if res.status_code in [200, 201]:
                return [{"text": i.get("full_text") or i.get("text", "DNA"), "engagement": f"{i.get('favorite_count', 0)} Likes"} for i in res.json()]
        except: pass
    
    return [
        {"text": f"المعادلة الذهبية للهيمنة في {niche} لعام 2026", "engagement": "150K+"},
        {"text": f"لماذا يكتسح القادة سوق {niche}؟ إليك السر الخفي", "engagement": "90K+"}
    ]

@app.route("/")
def home(): return render_template("index.html")

@app.route("/alchemy/discover", methods=["POST"])
def discover():
    data = request.get_json(silent=True) or {}
    niche = data.get("niche", "القيادة")
    posts = fetch_real_gold_posts(niche)
    fusion = alchemy_fusion_core(posts, niche)
    # تشغيل Nebula لضمان التخليق
    output = get_ai_response_nebula(f"{WPIL_DOMINATOR_SYSTEM}\n{fusion['synthesis_task']}")
    return jsonify({"super_post": output, "sources": posts, "trace": fusion["logic_trace"]}), 200

@app.route("/generate_all", methods=["POST"])
def generate_all():
    data = request.get_json(silent=True) or {}
    idea = data.get('text') or "السيادة العالمية"
    prompt = f"{WPIL_DOMINATOR_SYSTEM}\nالمهمة: توليد 3 نسخ (LinkedIn, X, TikTok) لهذه الفكرة: {idea}\nالناتج يجب أن يكون منسقاً بفخامة."
    # تشغيل Nebula لضمان التوليد العابر للمنصات
    output = get_ai_response_nebula(prompt)
    brain = strategic_intelligence_core(idea)
    return jsonify({"combined_text": output, "trace": brain["logic_trace"], "video_prompt": brain["video_segments"]}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
