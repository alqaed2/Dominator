import os
import re
import requests
import logging
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import google.generativeai as genai
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
    if APIFY_KEY:
        try:
            url = f"https://api.apify.com/v2/acts/apidojo~tweet-scraper/run-sync-get-dataset-items?token={APIFY_KEY}"
            res = requests.post(url, json={"searchTerms": [niche], "maxTweets": 4, "searchMode": "top"}, timeout=20)
            if res.status_code in [200, 201]:
                return [{
                    "text": i.get("text", "DNA"), 
                    "engagement": f"{i.get('favorite_count', 0)}",
                    "author": i.get("user", {}).get("screen_name", "Elite_User"),
                    "url": i.get("url") or f"https://twitter.com/i/web/status/{i.get('id_str')}",
                    "score": 85 + (i.get('favorite_count', 0) % 15)
                } for i in res.json()]
        except: pass
    return [{"text": f"استراتيجية {niche} لعام 2026", "engagement": "120K", "author": "Strategic_AI", "url": "#", "score": 95}]

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
    niche = request.get_json().get("niche", "القيادة")
    posts = fetch_live_dna(niche)
    fusion = alchemy_fusion_core(posts, niche)
    output = get_ai_response_nebula(f"{WPIL_DOMINATOR_SYSTEM}\n{fusion['synthesis_task']}")
    return jsonify({"super_post": output, "sources": posts}), 200

@app.route("/generate_all", methods=["POST"])
def generate():
    idea = request.get_json().get("text", "الهيمنة")
    prompt = f"{WPIL_DOMINATOR_SYSTEM}\nتوليد محتوى لـ [LINKEDIN], [TWITTER], [TIKTOK] للفكرة: {idea}"
    raw = get_ai_response_nebula(prompt)
    parsed = parse_output(raw)
    brain = strategic_intelligence_core(idea)
    return jsonify({**parsed, "video_prompt": brain["video_segments"]}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
