import os
import re
import requests
import json
import logging
import time
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import google.generativeai as genai

# استيراد النواة السيادية
from dominator_brain import strategic_intelligence_core, alchemy_fusion_core, WPIL_DOMINATOR_SYSTEM

app = Flask(__name__, template_folder="templates", static_folder="static")
CORS(app)

# ========= ترسانة Nebula لعام 2025 =========
MODELS_POOL = ["gemini-2.0-flash-lite", "gemini-1.5-flash", "gemini-flash-latest"]
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
APIFY_KEY = os.getenv("APIFY_API_KEY")

def get_ai_response_nebula(prompt: str) -> str:
    for model_name in MODELS_POOL:
        try:
            model = genai.GenerativeModel(model_name)
            return model.generate_content(prompt).text
        except: continue
    return "🚨 المحركات مشغولة حالياً."

@app.route("/test_apify")
def test_apify():
    if not APIFY_KEY: return jsonify({"status": "error", "message": "Key missing"}), 400
    try:
        res = requests.get(f"https://api.apify.com/v2/users/me?token={APIFY_KEY}", timeout=10)
        return jsonify({"status": "success", "apify_user": res.json()}), 200
    except Exception as e:
        return jsonify({"status": "failed", "error": str(e)}), 500

def fetch_live_dna(niche):
    """بروتوكول Stealth Hunter: اقتناص المنشورات الحقيقية بروابط مباشرة"""
    search_url = f"https://x.com/search?q={niche}&f=live"
    
    if APIFY_KEY:
        try:
            # استخدام إعدادات بحث أكثر دقة لضمان العثور على نتائج
            url = f"https://api.apify.com/v2/acts/apidojo~tweet-scraper/run-sync-get-dataset-items?token={APIFY_KEY}"
            payload = {
                "searchTerms": [niche],
                "maxTweets": 5,
                "searchMode": "latest", # البحث في الأحدث يضمن روابط حية أكثر من 'top'
                "addUserInfo": True
            }
            # زيادة المهلة لـ 50 ثانية لإعطاء السكرابر وقتاً لتجاوز الحماية
            res = requests.post(url, json=payload, timeout=50)
            
            if res.status_code in [200, 201]:
                data = res.json()
                if data and len(data) > 0:
                    refined = []
                    for i in data:
                        text = i.get("full_text") or i.get("text")
                        if not text: continue
                        user = i.get("user", {}).get("screen_name") or "user"
                        tid = i.get("id_str") or i.get("id")
                        # بناء الرابط المباشر القهري
                        direct_link = f"https://x.com/{user}/status/{tid}" if tid else search_url
                        
                        refined.append({
                            "text": text,
                            "engagement": f"{i.get('favorite_count', 0) + i.get('retweet_count', 0)} Interactions",
                            "author": user,
                            "url": direct_link,
                            "is_live": True if tid else False,
                            "score": 85 + (len(text) % 15)
                        })
                    if refined: return refined
        except Exception as e:
            print(f"Extraction Log: {e}")

    # السقوط الآمن (Synthetic DNA) في حال فشل الإنترنت
    return [
        {"text": f"المعادلة السيادية للاكتساح في {niche} لعام 2026", "engagement": "AI Simulated", "author": "Dominator_SIC", "url": search_url, "is_live": False, "score": 98},
        {"text": f"لماذا ينهار المنافسون في سوق {niche}؟", "engagement": "AI Simulated", "author": "Market_Oracle", "url": search_url, "is_live": False, "score": 95}
    ]

@app.route("/")
def home(): return render_template("index.html")

@app.route("/alchemy/discover", methods=["POST"])
def discover():
    data = request.get_json(silent=True) or {}
    niche = data.get("niche", "القيادة")
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
    
    parts = {"linkedin": "", "twitter": "", "tiktok": ""}
    for p in parts:
        match = re.search(rf"\[{p.upper()}\](.*?)(\[|$)", raw, re.S | re.I)
        parts[p] = match.group(1).strip() if match else "فشل استخراج القسم"
    
    brain = strategic_intelligence_core(idea)
    return jsonify({**parts, "video_prompt": brain["video_segments"]}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
