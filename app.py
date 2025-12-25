import os
import re
import requests
import json
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
    "gemini-flash-latest"
]

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
APIFY_KEY = os.getenv("APIFY_API_KEY")

def get_ai_response_nebula(prompt: str) -> str:
    """بروتوكول Nebula للتبديل التلقائي القسري"""
    for model_name in MODELS_POOL:
        try:
            model = genai.GenerativeModel(model_name)
            response = model.generate_content(prompt)
            return response.text
        except: continue
    return "🚨 كافة خطوط الاتصال مشغولة حالياً."

def fetch_live_dna(niche):
    """بروتوكول السحب الحي المطور لاستخراج الروابط المباشرة لـ x.com"""
    if APIFY_KEY:
        try:
            url = f"https://api.apify.com/v2/acts/apidojo~tweet-scraper/run-sync-get-dataset-items?token={APIFY_KEY}"
            payload = {
                "searchTerms": [niche],
                "maxTweets": 5,
                "searchMode": "top",
                "addUserInfo": True
            }
            res = requests.post(url, json=payload, timeout=30)
            if res.status_code in [200, 201]:
                data = res.json()
                if data:
                    refined = []
                    for i in data:
                        user = i.get("user", {}).get("screen_name", "user")
                        tid = i.get("id_str") or i.get("id")
                        # بناء رابط X المباشر
                        link = f"https://x.com/{user}/status/{tid}" if tid else f"https://x.com/search?q={niche}"
                        refined.append({
                            "text": i.get("full_text") or i.get("text", "DNA"),
                            "engagement": f"{i.get('favorite_count', 0)}",
                            "author": user,
                            "url": link,
                            "score": 85 + (int(i.get('favorite_count', 0)) % 15)
                        })
                    return refined
        except: pass
    
    # Fallback Data
    return [{"text": f"استراتيجية {niche} لعام 2026", "engagement": "150K", "author": "Dominator_AI", "url": f"https://x.com/search?q={niche}", "score": 98}]

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
        niche = data.get("niche", "ريادة الأعمال")
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
        idea = data.get("text", "السيادة")
        prompt = f"{WPIL_DOMINATOR_SYSTEM}\nتوليد محتوى لـ [LINKEDIN], [TWITTER], [TIKTOK] للفكرة: {idea}"
        raw = get_ai_response_nebula(prompt)
        parsed = parse_output(raw)
        brain = strategic_intelligence_core(idea)
        return jsonify({**parsed, "video_prompt": brain["video_segments"]}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
