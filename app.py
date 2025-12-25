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
MODELS_POOL = [
    "gemini-2.0-flash-lite-001",
    "gemini-2.5-flash-lite",
    "gemini-1.5-flash",
    "gemini-flash-latest"
]

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
APIFY_KEY = os.getenv("APIFY_API_KEY")

def get_ai_response_nebula(prompt: str) -> str:
    """بروتوكول Nebula للتبديل التلقائي"""
    for model_name in MODELS_POOL:
        try:
            model = genai.GenerativeModel(model_name)
            response = model.generate_content(prompt)
            return response.text
        except: continue
    return "🚨 كافة محركات الذكاء مشغولة حالياً."

@app.route("/test_apify")
def test_apify():
    if not APIFY_KEY: return jsonify({"status": "error", "message": "Key missing"}), 400
    try:
        res = requests.get(f"https://api.apify.com/v2/users/me?token={APIFY_KEY}", timeout=10)
        return jsonify({"status": "success", "apify_user": res.json()}), 200
    except Exception as e:
        return jsonify({"status": "failed", "error": str(e)}), 500

def fetch_live_dna(niche):
    """بروتوكول السحب المطور مع تصحيح التشفير البايثوني"""
    encoded_niche = urllib.parse.quote(niche)
    search_url = f"https://x.com/search?q={encoded_niche}&f=live"
    
    if APIFY_KEY:
        try:
            url = f"https://api.apify.com/v2/acts/apidojo~tweet-scraper/run-sync-get-dataset-items?token={APIFY_KEY}"
            payload = {"searchTerms": [niche], "maxTweets": 5, "searchMode": "latest", "addUserInfo": True}
            # تقليص المهلة لـ 28 ثانية لضمان استجابة Gunicorn قبل التوقف
            res = requests.post(url, json=payload, timeout=28)
            if res.status_code in [200, 201]:
                data = res.json()
                if data:
                    refined = []
                    for i in data:
                        user = i.get("user", {}).get("screen_name", "user")
                        tid = i.get("id_str") or i.get("id")
                        link = f"https://x.com/{user}/status/{tid}" if tid else search_url
                        refined.append({
                            "text": i.get("full_text") or i.get("text") or "DNA",
                            "engagement": f"{int(i.get('favorite_count', 0)) + int(i.get('retweet_count', 0))}",
                            "author": user,
                            "url": link,
                            "is_live": True if tid else False,
                            "score": 85 + (len(str(tid)) % 15 if tid else 10)
                        })
                    return refined
        except: pass
    return [{"text": f"تحليل استراتيجي لترندات {niche}", "engagement": "Simulated", "author": "Dominator_AI", "url": search_url, "is_live": False, "score": 98}]

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
    try:
        data = request.get_json(silent=True) or {}
        niche = data.get("niche", "السيادة الرقمية")
        posts = fetch_live_dna(niche)
        fusion = alchemy_fusion_core(posts, niche)
        output = get_ai_response_nebula(f"{WPIL_DOMINATOR_SYSTEM}\n{fusion['synthesis_task']}")
        return jsonify({"super_post": output, "sources": posts}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/generate_all", methods=["POST"])
def generate():
    try:
        data = request.get_json(silent=True) or {}
        idea = data.get("text", "الهيمنة")
        prompt = f"{WPIL_DOMINATOR_SYSTEM}\nتوليد حزمة سيادية لـ [LINKEDIN], [TWITTER], [TIKTOK] للفكرة: {idea}"
        raw = get_ai_response_nebula(prompt)
        parsed = parse_output(raw)
        brain = strategic_intelligence_core(idea)
        return jsonify({**parsed, "video_prompt": brain["video_segments"]}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
