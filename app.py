import os
import sys
import json
import logging
import requests  # نحتاج هذه المكتبة للاتصال بـ Apify
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import google.generativeai as genai
from dominator_brain import strategic_intelligence_core, alchemy_fusion_core, WPIL_DOMINATOR_SYSTEM

app = Flask(__name__, template_folder="templates", static_folder="static")
CORS(app)
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger(__name__)

# إعداد AI
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
MODELS_PRIORITY = ["gemini-2.0-flash-lite", "gemini-flash-latest"]

# ========= إعدادات Apify للربط الحي =========
APIFY_API_KEY = os.getenv("APIFY_API_KEY")

def fetch_real_gold_posts(niche):
    """
    بروتوكول السحب الحي: يتصل بـ Apify لسحب أفضل المنشورات.
    """
    if not APIFY_API_KEY:
        logger.warning("APIFY_API_KEY missing. Falling back to internal DNA storage.")
        return get_mock_gold_posts(niche)

    try:
        # استخدام Actor متخصص في سحب ترندات X (كمثال قوي للانتشار)
        # هذا الـ Actor يبحث عن الكلمات المفتاحية للنيش ويجلب الأعلى تفاعلاً
        actor_url = "https://api.apify.com/v2/acts/apidojo~tweet-scraper/run-sync-get-dataset-items"
        payload = {
            "searchMode": "top",
            "searchTerms": [niche],
            "maxTweets": 5,
            "addUserInfo": True
        }
        
        response = requests.post(
            f"{actor_url}?token={APIFY_API_KEY}", 
            json=payload, 
            timeout=45 # مهلة كافية للسحب
        )
        
        if response.status_code == 201 or response.status_code == 200:
            raw_data = response.json()
            gold_posts = []
            for item in raw_data:
                gold_posts.append({
                    "text": item.get("full_text") or item.get("text", ""),
                    "engagement": f"{item.get('retweet_count', 0) + item.get('favorite_count', 0)} Interactions",
                    "platform": "X (Twitter)"
                })
            return gold_posts if gold_posts else get_mock_gold_posts(niche)
        
        return get_mock_gold_posts(niche)
    except Exception as e:
        logger.error(f"Apify Connection Error: {e}")
        return get_mock_gold_posts(niche)

def get_mock_gold_posts(niche):
    """الذاكرة الاحتياطية في حال تعطل الربط الخارجي"""
    return [
        {"text": f"المعادلة الخفية للسيطرة على {niche} في 2026...", "engagement": "الذاكرة الاستراتيجية", "platform": "Deep Logic"},
        {"text": f"لماذا ينهار المنافسون في مجال {niche}؟ التحليل الكامل.", "engagement": "الذاكرة الاستراتيجية", "platform": "Deep Logic"}
    ]

def get_ai_response(prompt: str) -> str:
    for model_name in MODELS_PRIORITY:
        try:
            model = genai.GenerativeModel(model_name)
            return model.generate_content(prompt).text
        except: continue
    return "Error: AI Engines Busy."

@app.route("/")
def home(): return render_template("index.html")

@app.route("/alchemy/discover", methods=["POST"])
def discover_gold():
    data = request.get_json(silent=True) or {}
    niche = data.get("niche", "القيادة الاستراتيجية")
    
    # 1. السحب الحي من الإنترنت عبر Apify
    gold_posts = fetch_real_gold_posts(niche)
    
    # 2. تشغيل مفاعل الاندماج (Synthesis)
    fusion_data = alchemy_fusion_core(gold_posts, niche)
    
    # 3. تخليق المنشور الخارق بواسطة المحرك الذكي
    super_post_text = get_ai_response(f"{WPIL_DOMINATOR_SYSTEM}\n{fusion_data['synthesis_task']}")
    
    return jsonify({
        "super_post": super_post_text,
        "score": fusion_data["dominance_score"],
        "sources": gold_posts,
        "trace": fusion_data["logic_trace"]
    }), 200

@app.route("/generate/<platform>", methods=["POST", "GET"])
def handle_execution(platform="linkedin"):
    # (نفس منطق التوليد السابق لضمان استقرار المهام العادية)
    data = request.get_json(force=True, silent=True) or {}
    idea = data.get('text') or data.get('idea') or ""
    seed = data.get('winning_post') or ""
    brain = strategic_intelligence_core(idea, platform, "default", seed)
    prompt = f"{WPIL_DOMINATOR_SYSTEM}\nالمهمة: {brain['transformed_input']}\nالمنصة: {platform}"
    text_raw = get_ai_response(prompt)
    
    payload = {
        "platform": platform, 
        "text": f"{text_raw}{brain.get('viral_signature','')}",
        "trace": brain["logic_trace"]
    }
    if platform == "tiktok":
        v_prompt = "🚀 **VERTICAL 9:16 PROMPTS**\n\n"
        for seg in brain["video_segments"]:
            v_prompt += f"### {seg['time']}\n```text\n{seg['prompt']}\n```\n\n"
        payload["video_prompt"] = v_prompt
    return jsonify(payload), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
