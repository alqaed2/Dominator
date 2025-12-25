import os
import re
import requests
import json
import urllib.parse
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import google.generativeai as genai

# استيراد النواة السيادية
from dominator_brain import strategic_intelligence_core, alchemy_fusion_core, WPIL_DOMINATOR_SYSTEM

app = Flask(__name__, template_folder="templates", static_folder="static")
CORS(app)

# ========= ترسانة Nebula لعام 2025 =========
MODELS_POOL = ["gemini-2.0-flash-lite-001", "gemini-2.5-flash-lite", "gemini-1.5-flash"]
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
APIFY_KEY = os.getenv("APIFY_API_KEY")

def get_ai_response_nebula(prompt: str) -> str:
    for model_name in MODELS_POOL:
        try:
            model = genai.GenerativeModel(model_name)
            return model.generate_content(prompt).text
        except: continue
    return "🚨 كافة محركات الذكاء مشغولة حالياً."

def fetch_live_dna(niche, target_data=None):
    """منطق مزدوج: إذا وُجد هدف يدوياً نستخدمه، وإلا نبحث تلقائياً"""
    search_url = f"https://x.com/search?q={urllib.parse.quote(niche)}&f=live"
    
    # الخيار الأول: إذا قام المستخدم بلصق رابط أو نص
    if target_data and len(target_data.strip()) > 10:
        return [{
            "text": target_data,
            "engagement": "Target Confirmed",
            "author": "Target_Source",
            "url": target_data if "http" in target_data else search_url,
            "is_live": True,
            "score": 100
        }]

    # الخيار الثاني: البحث التلقائي عبر Apify
    if APIFY_KEY:
        try:
            url = f"https://api.apify.com/v2/acts/apidojo~tweet-scraper/run-sync-get-dataset-items?token={APIFY_KEY}"
            payload = {"searchTerms": [niche], "maxTweets": 4, "searchMode": "latest"}
            res = requests.post(url, json=payload, timeout=28)
            if res.status_code in [200, 201]:
                data = res.json()
                if data:
                    return [{
                        "text": i.get("full_text") or i.get("text", "DNA"),
                        "engagement": f"{i.get('favorite_count', 0)}",
                        "author": i.get("user", {}).get("screen_name", "user"),
                        "url": f"https://x.com/i/web/status/{i.get('id_str')}",
                        "is_live": True,
                        "score": 90
                    } for i in data if i.get("text")]
        except: pass

    # الملاذ الأخير (بيانات بديلة)
    return [{"text": f"تحليل سيادي لترندات {niche}", "engagement": "Simulated", "author": "Dominator_SIC", "url": search_url, "is_live": False, "score": 95}]

@app.route("/")
def home(): return render_template("index.html")

@app.route("/alchemy/discover", methods=["POST"])
def discover():
    data = request.get_json(silent=True) or {}
    niche = data.get("niche", "ريادة الأعمال")
    target = data.get("target_data", "") # الحقل الجديد
    
    posts = fetch_live_dna(niche, target)
    fusion = alchemy_fusion_core(posts, niche)
    output = get_ai_response_nebula(f"{WPIL_DOMINATOR_SYSTEM}\n{fusion['synthesis_task']}")
    return jsonify({"super_post": output, "sources": posts}), 200

@app.route("/generate_all", methods=["POST"])
def generate():
    data = request.get_json(silent=True) or {}
    idea = data.get("text", "السيادة")
    prompt = f"{WPIL_DOMINATOR_SYSTEM}\nتوليد حزمة سيادية لـ [LINKEDIN], [TWITTER], [TIKTOK] للفكرة: {idea}"
    raw = get_ai_response_nebula(prompt)
    
    parts = {"linkedin": "", "twitter": "", "tiktok": ""}
    for p in parts:
        match = re.search(rf"\[{p.upper()}\](.*?)(\[|$)", raw, re.S | re.I)
        parts[p] = match.group(1).strip() if match else "فشل استخراج القسم"
    
    brain = strategic_intelligence_core(idea)
    return jsonify({**parts, "video_prompt": brain["video_segments"]}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
