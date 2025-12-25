import os
import re
import requests
import json
import logging
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import google.generativeai as genai

# استيراد النواة السيادية
from dominator_brain import strategic_intelligence_core, alchemy_fusion_core, WPIL_DOMINATOR_SYSTEM

app = Flask(__name__, template_folder="templates", static_folder="static")
CORS(app)

# ========= ترسانة Nebula لعام 2025 =========
MODELS_POOL = [
    "gemini-2.0-flash-lite", 
    "gemini-1.5-flash", 
    "gemini-flash-latest"
]

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
APIFY_KEY = os.getenv("APIFY_API_KEY")

def get_ai_response_nebula(prompt: str) -> str:
    for model_name in MODELS_POOL:
        try:
            model = genai.GenerativeModel(model_name)
            response = model.generate_content(prompt)
            return response.text
        except: continue
    return "🚨 كافة خطوط الذكاء مشغولة حالياً."

def fetch_live_dna(niche):
    """بروتوكول الاقتناص المباشر: يجبر النظام على جلب روابط x.com حقيقية"""
    fallback_url = f"https://x.com/search?q={niche}&f=live"
    
    if APIFY_KEY:
        try:
            # زيادة المهلة لـ 45 ثانية لضمان انتهاء سكرابر X من عمله
            actor_url = f"https://api.apify.com/v2/acts/apidojo~tweet-scraper/run-sync-get-dataset-items?token={APIFY_KEY}"
            payload = {
                "searchTerms": [niche],
                "maxTweets": 5,
                "searchMode": "top",
                "addUserInfo": True
            }
            res = requests.post(actor_url, json=payload, timeout=45)
            
            if res.status_code in [200, 201]:
                data = res.json()
                if data and len(data) > 0:
                    refined = []
                    for i in data:
                        text = i.get("full_text") or i.get("text")
                        if not text: continue
                        
                        # بناء الرابط المباشر قسرياً باستخدام ID التغريدة
                        user = i.get("user", {}).get("screen_name") or "user"
                        tid = i.get("id_str") or i.get("id")
                        direct_link = f"https://x.com/{user}/status/{tid}" if tid else fallback_url
                        
                        refined.append({
                            "text": text,
                            "engagement": f"{i.get('favorite_count', '10K+')}",
                            "author": user,
                            "url": direct_link,
                            "is_live": True if tid else False, # علامة للحقيقة
                            "score": 85 + (hash(text) % 15)
                        })
                    if refined: return refined
        except Exception as e:
            logging.error(f"Apify Nerve Error: {e}")

    # Fallback Data (Synthetic DNA)
    return [
        {"text": f"استراتيجية اختراق {niche} لعام 2026", "engagement": "التحليل الاستراتيجي", "author": "Dominator_SIC", "url": fallback_url, "is_live": False, "score": 98},
        {"text": f"لماذا يسيطر القادة على سوق {niche}؟", "engagement": "النبض العالمي", "author": "Market_Oracle", "url": fallback_url, "is_live": False, "score": 92}
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
    niche = data.get("niche", "السيادة الرقمية")
    posts = fetch_live_dna(niche)
    fusion = alchemy_fusion_core(posts, niche)
    output = get_ai_response_nebula(f"{WPIL_DOMINATOR_SYSTEM}\n{fusion['synthesis_task']}")
    return jsonify({"super_post": output, "sources": posts}), 200

@app.route("/generate_all", methods=["POST"])
def generate():
    data = request.get_json(silent=True) or {}
    idea = data.get("text", "الهيمنة")
    prompt = f"{WPIL_DOMINATOR_SYSTEM}\nتوليد حزمة سيادية لـ [LINKEDIN], [TWITTER], [TIKTOK] للفكرة: {idea}"
    raw = get_ai_response_nebula(prompt)
    parsed = parse_output(raw)
    brain = strategic_intelligence_core(idea)
    return jsonify({**parsed, "video_prompt": brain["video_segments"]}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
