import os
import sys
import re
import time
import requests
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import google.generativeai as genai

# استيراد النواة السيادية
from dominator_brain import strategic_intelligence_core, alchemy_fusion_core, WPIL_DOMINATOR_SYSTEM

app = Flask(__name__, template_folder="templates", static_folder="static")
CORS(app)

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
    """بروتوكول Nebula: التبديل التلقائي القسري بين الموديلات لتجاوز Quota"""
    last_error = ""
    for model_name in MODELS_POOL:
        try:
            print(f"📡 [COMMAND] Deploying model: {model_name}")
            model = genai.GenerativeModel(model_name)
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            last_error = str(e)
            print(f"⚠️ [WARNING] Model {model_name} failed. Switching...")
            continue
    return f"[ERROR] كافة الخطوط مشغولة حالياً. {last_error}"

def parse_unified_output(raw_text: str) -> dict:
    """تفكيك النص الموحد إلى أقسام المنصات برمجياً"""
    parts = {"linkedin": "فشل استخراج النص", "twitter": "فشل استخراج النص", "tiktok": "فشل استخراج النص"}
    ln = re.search(r"\[LINKEDIN\](.*?)(\[TWITTER\]|\[TIKTOK\]|$)", raw_text, re.S | re.I)
    tw = re.search(r"\[TWITTER\](.*?)(\[LINKEDIN\]|\[TIKTOK\]|$)", raw_text, re.S | re.I)
    tk = re.search(r"\[TIKTOK\](.*?)(\[LINKEDIN\]|\[TWITTER\]|$)", raw_text, re.S | re.I)
    if ln: parts["linkedin"] = ln.group(1).strip()
    if tw: parts["twitter"] = tw.group(1).strip()
    if tk: parts["tiktok"] = tk.group(1).strip()
    return parts

def fetch_real_gold_posts(niche):
    if APIFY_KEY:
        try:
            url = f"https://api.apify.com/v2/acts/apidojo~tweet-scraper/run-sync-get-dataset-items?token={APIFY_KEY}"
            res = requests.post(url, json={"searchTerms": [niche], "maxTweets": 4, "searchMode": "top"}, timeout=15)
            if res.status_code in [200, 201]:
                return [{"text": i.get("text", "DNA"), "engagement": i.get('favorite_count', 0), "score": 90} for i in res.json()]
        except: pass
    return [{"text": f"المعادلة الاستراتيجية في {niche}", "engagement": "100K+", "score": 95}]

@app.route("/")
def home(): return render_template("index.html")

@app.route("/alchemy/discover", methods=["POST"])
def discover():
    data = request.get_json(silent=True) or {}
    niche = data.get("niche", "القيادة")
    posts = fetch_real_gold_posts(niche)
    fusion = alchemy_fusion_core(posts, niche)
    output = get_ai_response_nebula(f"{WPIL_DOMINATOR_SYSTEM}\n{fusion['synthesis_task']}")
    return jsonify({"super_post": output, "sources": posts}), 200

@app.route("/generate_all", methods=["POST"])
def generate_all():
    data = request.get_json(silent=True) or {}
    idea = data.get('text') or "الهيمنة"
    prompt = f"{WPIL_DOMINATOR_SYSTEM}\nالمهمة: توليد محتوى لـ [LINKEDIN] و [TWITTER] و [TIKTOK] للفكرة: {idea}"
    raw_output = get_ai_response_nebula(prompt)
    parsed = parse_unified_output(raw_output)
    brain = strategic_intelligence_core(idea)
    return jsonify({
        "linkedin": parsed["linkedin"], "twitter": parsed["twitter"], "tiktok": parsed["tiktok"],
        "video_prompt": brain["video_segments"], "trace": brain["logic_trace"]
    }), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
