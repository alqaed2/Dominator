import os
import re
import requests
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import google.generativeai as genai

# استيراد النواة السيادية
from dominator_brain import strategic_intelligence_core, alchemy_fusion_core, WPIL_DOMINATOR_SYSTEM

app = Flask(__name__, template_folder="templates", static_folder="static")
CORS(app)

# ========= ترسانة Nebula لعام 2025 =========
MODELS_POOL = [
    "gemini-2.5-flash",
    "gemini-2.5-flash-lite",
    "gemini-2.0-flash-lite-001",
    "gemini-flash-latest",
    "gemini-pro-latest"
]

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
APIFY_KEY = os.getenv("APIFY_API_KEY")

def get_ai_response_nebula(prompt: str) -> str:
    for model_name in MODELS_POOL:
        try:
            model = genai.GenerativeModel(model_name)
            return model.generate_content(prompt).text
        except: continue
    return "🚨 كافة المحركات مشغولة حالياً."

def fetch_live_dna(niche):
    # رابط البحث الافتراضي لضمان عدم توجيه المستخدم للرئيسية أبداً
    fallback_url = f"https://twitter.com/search?q={niche}&f=live"
    
    if APIFY_KEY:
        try:
            url = f"https://api.apify.com/v2/acts/apidojo~tweet-scraper/run-sync-get-dataset-items?token={APIFY_KEY}"
            res = requests.post(url, json={"searchTerms": [niche], "maxTweets": 5, "searchMode": "top"}, timeout=20)
            if res.status_code in [200, 201]:
                data = res.json()
                if data:
                    return [{
                        "text": i.get("text", "DNA Sample"), 
                        "engagement": f"{i.get('favorite_count', 0)}",
                        "author": i.get("user", {}).get("screen_name", "Elite_Insight"),
                        "url": i.get("url") or f"https://twitter.com/i/web/status/{i.get('id_str')}",
                        "score": 85 + (i.get('favorite_count', 0) % 15)
                    } for i in data if i.get("text")]
        except: pass
    
    # بيانات بديلة احترافية مع روابط بحث حقيقية في النيش
    return [
        {"text": f"تحليل استراتيجي لاكتساح {niche} في 2026", "engagement": "120K", "author": "Dominator_AI", "url": fallback_url, "score": 95},
        {"text": f"لماذا يسيطر القادة على سوق {niche}؟", "engagement": "85K", "author": "Market_Oracle", "url": fallback_url, "score": 90}
    ]

def parse_output(text):
    parts = {"linkedin": "", "twitter": "", "tiktok": ""}
    for p in parts:
        match = re.search(rf"\[{p.upper()}\](.*?)(\[|$)", text, re.S | re.I)
        parts[p] = match.group(1).strip() if match else "فشل استخراج القسم"
    return parts

@app.route("/")
def home(): return render_template("index.html")

@app.route("/alchemy/discover", methods=["POST"])
def discover():
    data = request.get_json(silent=True) or {}
    niche = data.get("niche", "ريادة الأعمال")
    posts = fetch_live_dna(niche)
    fusion = alchemy_fusion_core(posts, niche)
    output = get_ai_response_nebula(f"{WPIL_DOMINATOR_SYSTEM}\n{fusion['synthesis_task']}")
    return jsonify({"super_post": output, "sources": posts}), 200

@app.route("/generate_all", methods=["POST"])
def generate():
    idea = request.get_json().get("text", "السيادة")
    prompt = f"{WPIL_DOMINATOR_SYSTEM}\nتوليد محتوى لـ [LINKEDIN], [TWITTER], [TIKTOK] لهذه الفكرة: {idea}"
    raw = get_ai_response_nebula(prompt)
    parsed = parse_output(raw)
    brain = strategic_intelligence_core(idea)
    return jsonify({**parsed, "video_prompt": brain["video_segments"]}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
