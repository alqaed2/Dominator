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
    for model_name in MODELS_POOL:
        try:
            model = genai.GenerativeModel(model_name)
            return model.generate_content(prompt).text
        except: continue
    return "🚨 كافة خطوط الاتصال مشغولة حالياً."

def fetch_live_dna(niche):
    """بروتوكول السحب الحي المطور لاستf"https://twitter.com/{user_name}/status/{tweet_id}" if tweet_id else None)
                        
                        results.append({
                            "text": i.get("full_text") or i.get("text") or "DNA Sample",
                            "engagement": f"{i.get('favorite_count', 0)}",
                            "author": user_name,
                            "url": actual_url, # الرابط الحقيقي
                            "is_live": True,
                            "score": 85 + (int(i.get('favorite_count', 0)) % 15)
                        })
                    return results
        except Exception as e:
            print(f"Apify Error: {e}")
            
    # إذا لم يجد روابط حقيقية، يعطي جينات استراتيجية واضحة
    return [
        {
            "text": f"استراتيجية السيادة في {niche} لعام 2026", 
            "engagement": "التحليل الاستراتيجي", 
            "author": "Dominator_AI", 
            "url": f"https://twitter.com/search?q={niche}&f=live",
            "is_live": False,
            "score": 98
        }
    ]

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
    idea = request.getخراج الروابط المباشرة"""
    if APIFY_KEY:
        try:
            # استخدام Actor السحب المتقدم مع مهلة أطول قليلاً لضمان الدقة
            url = f"https://api.apify.com/v2/acts/apidojo~tweet-scraper/run-sync-get-dataset-items?token={APIFY_KEY}"
            payload = {
                "searchTerms": [niche],
                "maxTweets": 5,
                "searchMode": "top",
                "addUserInfo": True
            }
            res = requests.post(url, json=payload, timeout=40)
            if res.status_code in [200, 201]:
                data = res.json()
                if data and len(data) > 0:
                    refined_posts = []
                    for i in data:
                        text = i.get("full_text") or i.get("text")
                        if not text: continue
                        
                        # بناء رابط المنشور المباشر قسرياً
                        username = i.get("user", {}).get("screen_name") or "user"
                        tweet_id = i.get("id_str") or i.get("id")
                        direct_url = f"https://x.com/{username}/status/{tweet_id}" if tweet_id else f"https://x.com/search?q={niche}"
                        
                        refined_posts.append({
                            "text": text,
                            "engagement": f"{int(i.get('favorite_count', 0)) + int(i.get('retweet_count', 0))}",
                            "author": username,
                            "url": direct_url,
                            "score": 85 + (int(i.get('favorite_count', 0)) % 15)
                        })
                    if refined_posts: return refined_posts_json().get("text", "السيادة")
    prompt = f"{WPIL_DOMINATOR_SYSTEM}\nتوليد محتوى لـ [LINKEDIN], [TWITTER], [TIKTOK] للفكرة: {idea}"
    raw = get_ai_response_nebula(prompt)
    brain = strategic_intelligence_core(idea)
    
    parts = {"linkedin": "", "twitter": "", "tiktok": ""}
    for p in parts:
        match = re.search(rf"\[{p.upper()}\](.*?)(\[|$)", raw, re.S | re.I)
        parts[p] = match.group(1).strip() if match else "فشل استخراج القسم"
        
    return jsonify({**parts, "video_prompt": brain["video_segments"]}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
