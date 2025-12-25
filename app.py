import os
import re
import requests
import json
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import google.generativeai as genai

from dominator_brain import strategic_intelligence_core, alchemy_fusion_core, WPIL_DOMINATOR_SYSTEM

app = Flask(__name__, template_folder="templates", static_folder="static")
CORS(app)

# ========= ترسانة الموديلات =========
MODELS_POOL = ["gemini-2.0-flash-lite", "gemini-1.5-flash", "gemini-flash-latest"]
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
APIFY_KEY = os.getenv("APIFY_API_KEY")

def get_ai_response_nebula(prompt: str) -> str:
    for model_name in MODELS_POOL:
        try:
            model = genai.GenerativeModel(model_name)
            return model.generate_content(prompt).text
        except: continue
    return "🚨 المحركات مشغولة."

@app.route("/test_apify")
def test_apify():
    """مسار تشخيصي للتأكد من صحة مفتاح Apify"""
    if not APIFY_KEY:
        return jsonify({"status": "error", "message": "Key is missing in Render Settings!"}), 400
    try:
        res = requests.get(f"https://api.apify.com/v2/users/me?token={APIFY_KEY}")
        return jsonify({"status": "success", "data": res.json()}), 200
    except Exception as e:
        return jsonify({"status": "failed", "error": str(e)}), 500

def fetch_live_dna(niche):
    """بروتوكول الاقتناص مع توثيق حالة الربط"""
    if APIFY_KEY:
        try:
            url = f"https://api.apify.com/v2/acts/apidojo~tweet-scraper/run-sync-get-dataset-items?token={APIFY_KEY}"
            # تقليص المهلة لسرعة الاستجابة وطلب منشورات أقل لضمان النجاح
            res = requests.post(url, json={"searchTerms": [niche], "maxTweets": 3, "searchMode": "top"}, timeout=35)
            if res.status_code in [200, 201]:
                data = res.json()
                if data and len(data) > 0:
                    refined = []
                    for i in data:
                        user = i.get("user", {}).get("screen_name", "user")
                        tid = i.get("id_str") or i.get("id")
                        # بناء الرابط المباشر
                        link = f"https://x.com/{user}/status/{tid}" if tid else f"https://x.com/search?q={niche}"
                        refined.append({
                            "text": i.get("full_text") or i.get("text", "DNA"),
                            "engagement": f"{i.get('favorite_count', '10K+')}",
                            "author": user,
                            "url": link,
                            "is_live": True, # تأكيد أن البيانات حقيقية
                            "score": 90
                        })
                    return refined
        except: pass

    # إذا وصلنا هنا، يعني الـ API فشل. نرجع بيانات بديلة مع روابط "بحث حقيقي" وليس #
    search_url = f"https://x.com/search?q={niche}&f=live"
    return [
        {"text": f"تحليل سيادي لترندات {niche} لعام 2026", "engagement": "AI Simulated", "author": "Dominator_SIC", "url": search_url, "is_live": False, "score": 98},
        {"text": f"المعادلة الذهبية للهيمنة في {niche}", "engagement": "AI Simulated", "author": "Market_Oracle", "url": search_url, "is_live": False, "score": 95}
    ]

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
    brain = strategic_intelligence_core(idea)
    
    parts = {"linkedin": "", "twitter": "", "tiktok": ""}
    for p in parts:
        match = re.search(rf"\[{p.upper()}\](.*?)(\[|$)", raw, re.S | re.I)
        parts[p] = match.group(1).strip() if match else "فشل استخراج القسم"
        
    return jsonify({**parts, "video_prompt": brain["video_segments"]}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
