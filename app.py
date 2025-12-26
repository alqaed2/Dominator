import os
import re
import requests
import json
import urllib.parse
import random
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import google.generativeai as genai

# استيراد النواة السيادية
from dominator_brain import strategic_intelligence_core, alchemy_fusion_core, WPIL_DOMINATOR_SYSTEM

app = Flask(__name__, template_folder="templates", static_folder="static")
CORS(app)

# إعداد AI
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
APIFY_KEY = os.getenv("APIFY_API_KEY")
MODELS = ["gemini-1.5-flash", "gemini-2.0-flash-lite-001", "gemini-flash-latest"]

def get_ai_response_nebula(prompt: str) -> str:
    for m in MODELS:
        try:
            return genai.GenerativeModel(m).generate_content(prompt).text
        except: continue
    return "🚨 كافة المحركات مشغولة حالياً."

def fetch_live_dna(niche, target_data=None):
    search_url = f"https://x.com/search?q={urllib.parse.quote(niche)}&f=live"
    if target_data and len(target_data.strip()) > 10:
        return [{"text": target_data, "engagement": "Confirmed", "author": "Target", "url": target_data, "is_live": True}]
    
    if APIFY_KEY:
        try:
            url = f"https://api.apify.com/v2/acts/apidojo~tweet-scraper/run-sync-get-dataset-items?token={APIFY_KEY}"
            res = requests.post(url, json={"searchTerms": [niche], "maxTweets": 3, "searchMode": "latest"}, timeout=28)
            if res.status_code in [200, 201]:
                data = res.json()
                return [{"text": i.get("full_text") or i.get("text"), "engagement": i.get("favorite_count", 0), "author": i.get("user", {}).get("screen_name", "user"), "url": f"https://x.com/i/status/{i.get('id_str')}"} for i in data if i.get("text")]
        except: pass
    return [{"text": f"تحليل سيادي لـ {niche}", "engagement": "100K", "author": "Dominator_AI", "url": search_url}]

def robust_parse(text):
    parts = {"linkedin": "", "twitter": "", "tiktok": "", "visual": "Professional business office, 8k, realistic"}
    ln = re.search(r"\[LINKEDIN\](.*?)(?=\[TWITTER\]|\[TIKTOK\]|\[VISUAL_PROMPT\]|$)", text, re.S | re.I)
    tw = re.search(r"\[TWITTER\](.*?)(?=\[LINKEDIN\]|\[TIKTOK\]|\[VISUAL_PROMPT\]|$)", text, re.S | re.I)
    tk = re.search(r"\[TIKTOK\](.*?)(?=\[LINKEDIN\]|\[TWITTER\]|\[VISUAL_PROMPT\]|$)", text, re.S | re.I)
    vs = re.search(r"\[VISUAL_PROMPT\](.*?)$", text, re.S | re.I)
    if ln: parts["linkedin"] = ln.group(1).strip()
    if tw: parts["twitter"] = tw.group(1).strip()
    if tk: parts["tiktok"] = tk.group(1).strip()
    if vs: parts["visual"] = "Professional business photography, " + vs.group(1).strip()[:200]
    if not parts["linkedin"]: parts["linkedin"] = text
    return parts

@app.route("/")
def home(): return render_template("index.html")

@app.route("/alchemy/discover", methods=["POST"])
def discover():
    try:
        data = request.get_json(silent=True) or {}
        posts = fetch_live_dna(data.get("niche", "السيادة"), data.get("target_data", ""))
        fusion = alchemy_fusion_core(posts, data.get("niche", "السيادة"))
        output = get_ai_response_nebula(f"{WPIL_DOMINATOR_SYSTEM}\n{fusion['synthesis_task']}")
        return jsonify({"super_post": output, "sources": posts}), 200
    except Exception as e: return jsonify({"error": str(e)}), 500

@app.route("/generate_all", methods=["POST"])
def generate():
    try:
        data = request.get_json(silent=True) or {}
        idea = data.get("text", "السيادة")
        prompt = f"{WPIL_DOMINATOR_SYSTEM}\nتوليد حزمة سيادية كاملة (نص + صورة) للفكرة: {idea}\nيجب إنهاء الرد بـ [VISUAL_PROMPT]."
        raw = get_ai_response_nebula(prompt)
        parsed = robust_parse(raw)
        seed = random.randint(1, 9999)
        image_url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(parsed['visual'])}?seed={seed}&nologo=true"
        brain = strategic_intelligence_core(idea)
        return jsonify({**parsed, "image_url": image_url, "video_blueprint": brain["video_segments"]}), 200
    except Exception as e: return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
