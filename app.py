import os
import re
import requests
import json
import urllib.parse
import random
import logging
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import google.generativeai as genai

# استيراد النواة السيادية
from dominator_brain import strategic_intelligence_core, alchemy_fusion_core, WPIL_DOMINATOR_SYSTEM

app = Flask(__name__, template_folder="templates", static_folder="static")
CORS(app)
logging.basicConfig(level=logging.INFO)

# ========= إعدادات AI و Apify =========
GENAI_KEY = os.getenv("GEMINI_API_KEY")
APIFY_KEY = os.getenv("APIFY_API_KEY")

if GENAI_KEY:
    genai.configure(api_key=GENAI_KEY)

MODELS_POOL = ["gemini-1.5-flash", "gemini-2.0-flash-lite-001", "gemini-flash-latest"]

def get_ai_response_nebula(prompt: str) -> str:
    """بروتوكول التبديل التلقائي لضمان خروج النتائج"""
    for model_name in MODELS_POOL:
        try:
            model = genai.GenerativeModel(model_name)
            response = model.generate_content(prompt)
            return response.text
        except: continue
    return "🚨 كافة خطوط الاتصال مشغولة حالياً."

def fetch_live_dna(niche, target_data=None):
    """بروتوكول السحب المزدوج المطور"""
    search_url = f"https://x.com/search?q={urllib.parse.quote(niche)}&f=live"
    if target_data and len(target_data.strip()) > 10:
        return [{"text": target_data, "engagement": "Confirmed", "author": "Target", "url": target_data, "is_live": True, "score": 100}]
    
    if APIFY_KEY:
        try:
            url = f"https://api.apify.com/v2/acts/apidojo~tweet-scraper/run-sync-get-dataset-items?token={APIFY_KEY}"
            res = requests.post(url, json={"searchTerms": [niche], "maxTweets": 3, "searchMode": "latest"}, timeout=25)
            if res.status_code in [200, 201]:
                data = res.json()
                return [{"text": i.get("full_text") or i.get("text"), "engagement": i.get("favorite_count", 0), "author": i.get("user", {}).get("screen_name", "user"), "url": f"https://x.com/i/status/{i.get('id_str')}", "is_live": True, "score": 90} for i in data if i.get("text")]
        except: pass
    return [{"text": f"تحليل استراتيجي لـ {niche}", "engagement": "100K", "author": "Dominator_AI", "url": search_url, "is_live": False, "score": 95}]

def robust_parse(text):
    """مفكك نصوص حصين يمنع خطأ 500 حتى لو فشل الـ AI في التنسيق"""
    parts = {"linkedin": "", "twitter": "", "tiktok": "", "visual": "Luxurious professional modern office, cinematic lighting"}
    
    # محاولة اقتناص الأقسام باستخدام Regex مرن
    ln = re.search(r"\[LINKEDIN\](.*?)(?=\[TWITTER\]|\[TIKTOK\]|\[VISUAL_PROMPT\]|$)", text, re.S | re.I)
    tw = re.search(r"\[TWITTER\](.*?)(?=\[LINKEDIN\]|\[TIKTOK\]|\[VISUAL_PROMPT\]|$)", text, re.S | re.I)
    tk = re.search(r"\[TIKTOK\](.*?)(?=\[LINKEDIN\]|\[TWITTER\]|\[VISUAL_PROMPT\]|$)", text, re.S | re.I)
    vs = re.search(r"\[VISUAL_PROMPT\](.*?)$", text, re.S | re.I)
    
    if ln: parts["linkedin"] = ln.group(1).strip()
    if tw: parts["twitter"] = tw.group(1).strip()
    if tk: parts["tiktok"] = tk.group(1).strip()
    if vs: parts["visual"] = vs.group(1).strip()
    
    # في حال فشل التقسيم، نضع النص الكامل في LinkedIn كخيار بديل
    if not parts["linkedin"]: parts["linkedin"] = text
    return parts

@app.route("/")
def home(): return render_template("index.html")

@app.route("/alchemy/discover", methods=["POST"])
def discover():
    try:
        data = request.get_json(silent=True) or {}
        posts = fetch_live_dna(data.get("niche", "القيادة"), data.get("target_data", ""))
        fusion = alchemy_fusion_core(posts, data.get("niche", "السيادة"))
        output = get_ai_response_nebula(f"{WPIL_DOMINATOR_SYSTEM}\n{fusion['synthesis_task']}")
        return jsonify({"super_post": output, "sources": posts}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/generate_all", methods=["POST"])
def generate():
    try:
        data = request.get_json(silent=True) or {}
        idea = data.get("text", "السيادة")
        prompt = f"{WPIL_DOMINATOR_SYSTEM}\nتوليد حزمة سيادية كاملة (LinkedIn, X, TikTok) وصورة واقعية للفكرة: {idea}"
        raw = get_ai_response_nebula(prompt)
        parsed = robust_parse(raw)
        
        # محرك الصور السيادي
        seed = random.randint(1, 99999)
        quoted_prompt = urllib.parse.quote(parsed['visual'])
        image_url = f"https://image.pollinations.ai/prompt/{quoted_prompt}?width=1080&height=1350&model=flux&seed={seed}&nologo=true"
        
        brain = strategic_intelligence_core(idea)
        return jsonify({**parsed, "image_url": image_url, "video_prompt": brain["video_segments"]}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
