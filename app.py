import os
import re
import requests
import json
import urllib.parse
import random
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import google.generativeai as genai

from dominator_brain import strategic_intelligence_core, alchemy_fusion_core, WPIL_DOMINATOR_SYSTEM

app = Flask(__name__, template_folder="templates", static_folder="static")
CORS(app)

MODELS_POOL = ["gemini-2.0-flash-lite-001", "gemini-2.5-flash-lite", "gemini-flash-latest"]
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
APIFY_KEY = os.getenv("APIFY_API_KEY")

def get_ai_response_nebula(prompt: str) -> str:
    for model_name in MODELS_POOL:
        try:
            model = genai.GenerativeModel(model_name)
            return model.generate_content(prompt).text
        except: continue
    return "🚨 كافة المحركات مشغولة."

def fetch_live_dna(niche, target_data=None):
    encoded_niche = urllib.parse.quote(niche)
    search_url = f"https://x.com/search?q={encoded_niche}&f=live"
    
    if target_data and len(target_data.strip()) > 10:
        return [{"text": target_data, "engagement": "Target Confirmed", "author": "Target_Source", "url": target_data if "http" in target_data else search_url, "is_live": True, "score": 100}]

    if APIFY_KEY:
        try:
            url = f"https://api.apify.com/v2/acts/apidojo~tweet-scraper/run-sync-get-dataset-items?token={APIFY_KEY}"
            res = requests.post(url, json={"searchTerms": [niche], "maxTweets": 3, "searchMode": "latest"}, timeout=28)
            if res.status_code in [200, 201]:
                data = res.json()
                return [{"text": i.get("full_text") or i.get("text", "DNA"), "engagement": f"{i.get('favorite_count', 0)}", "author": i.get("user", {}).get("screen_name", "user"), "url": f"https://x.com/i/web/status/{i.get('id_str')}", "is_live": True, "score": 90} for i in data if i.get("text")]
        except: pass
    return [{"text": f"تحليل استراتيجي لـ {niche}", "engagement": "Simulated", "author": "Dominator_SIC", "url": search_url, "is_live": False, "score": 95}]

def parse_unified_v12(text):
    parts = {"linkedin": "", "twitter": "", "tiktok": "", "visual": "Luxurious cinematic professional business background"}
    ln = re.search(r"\[LINKEDIN\](.*?)(\[TWITTER\]|\[TIKTOK\]|\[VISUAL_PROMPT\]|$)", text, re.S | re.I)
    tw = re.search(r"\[TWITTER\](.*?)(\[LINKEDIN\]|\[TIKTOK\]|\[VISUAL_PROMPT\]|$)", text, re.S | re.I)
    tk = re.search(r"\[TIKTOK\](.*?)(\[LINKEDIN\]|\[TWITTER\]|\[VISUAL_PROMPT\]|$)", text, re.S | re.I)
    vs = re.search(r"\[VISUAL_PROMPT\](.*?)$", text, re.S | re.I)
    
    if ln: parts["linkedin"] = ln.group(1).strip()
    if tw: parts["twitter"] = tw.group(1).strip()
    if tk: parts["tiktok"] = tk.group(1).strip()
    if vs: parts["visual"] = vs.group(1).strip()
    return parts

@app.route("/")
def home(): return render_template("index.html")

@app.route("/alchemy/discover", methods=["POST"])
def discover():
    data = request.get_json(silent=True) or {}
    posts = fetch_live_dna(data.get("niche", "القيادة"), data.get("target_data", ""))
    fusion = alchemy_fusion_core(posts, data.get("niche"))
    output = get_ai_response_nebula(f"{WPIL_DOMINATOR_SYSTEM}\n{fusion['synthesis_task']}")
    return jsonify({"super_post": output, "sources": posts}), 200

@app.route("/generate_all", methods=["POST"])
def generate():
    idea = request.get_json().get("text", "الهيمنة")
    prompt = f"{WPIL_DOMINATOR_SYSTEM}\nتوليد حزمة سيادية كاملة (نص + وصف بصري) للفكرة: {idea}\nيجب إنهاء الرد بـ [VISUAL_PROMPT] يصف صورة فخمة."
    raw = get_ai_response_nebula(prompt)
    parsed = parse_unified_v12(raw)
    
    # محرك توليد الصور الفوري (Pollinations Integration)
    seed = random.randint(1, 99999)
    image_url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(parsed['visual'])}?width=1080&height=1350&model=flux&seed={seed}&nologo=true"
    
    brain = strategic_intelligence_core(idea)
    return jsonify({**parsed, "image_url": image_url, "video_prompt": brain["video_segments"]}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
