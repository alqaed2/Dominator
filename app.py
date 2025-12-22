import os
import sys
import json
import logging
import requests
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
APIFY_API_KEY = os.getenv("APIFY_API_KEY")

def get_ai_response(prompt: str) -> str:
    try:
        model = genai.GenerativeModel("gemini-2.0-flash-lite")
        return model.generate_content(prompt).text
    except:
        return "⚠️ المحرك مشغولي حالياً، لكن الاستراتيجية قيد التحضير."

def fetch_real_gold_posts(niche):
    if not APIFY_API_KEY:
        return get_mock_gold_posts(niche)
    try:
        # بروتوكول السحب السريع (Timeout 30s)
        actor_url = "https://api.apify.com/v2/acts/apidojo~tweet-scraper/run-sync-get-dataset-items"
        res = requests.post(f"{actor_url}?token={APIFY_API_KEY}", 
                            json={"searchTerms": [niche], "maxTweets": 5, "searchMode": "top"}, 
                            timeout=30)
        if res.status_code in [200, 201]:
            data = res.json()
            return [{"text": i.get("full_text") or i.get("text", "DNA Sample"), "engagement": f"{i.get('favorite_count', 0)} Likes"} for i in data]
        return get_mock_gold_posts(niche)
    except:
        return get_mock_gold_posts(niche)

def get_mock_gold_posts(niche):
    return [{"text": f"تحليل سيادي لترندات {niche} في 2026", "engagement": "100K+"}]

@app.route("/")
def home(): return render_template("index.html")

@app.route("/alchemy/discover", methods=["POST"])
def discover():
    try:
        data = request.get_json(silent=True) or {}
        niche = data.get("niche", "الذكاء الاصطناعي")
        
        # 1. جلب البيانات (الحي أو الذاكرة)
        gold_posts = fetch_real_gold_posts(niche)
        
        # 2. تشغيل مفاعل الاندماج
        fusion = alchemy_fusion_core(gold_posts, niche)
        
        # 3. تخليق المنشور الخارق
        prompt = f"{WPIL_DOMINATOR_SYSTEM}\nالمهمة: {fusion['synthesis_task']}"
        output = get_ai_response(prompt)
        
        return jsonify({
            "super_post": output,
            "sources": gold_posts,
            "trace": fusion["logic_trace"]
        }), 200
    except Exception as e:
        logger.error(f"Alchemy Discovery Error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/generate/<platform>", methods=["POST"])
def generate(platform):
    try:
        data = request.get_json(force=True, silent=True) or {}
        idea = data.get('text') or data.get('idea') or "استراتيجية هيمنة"
        brain = strategic_intelligence_core(idea, platform)
        prompt = f"{WPIL_DOMINATOR_SYSTEM}\nالمنصة: {platform}\nالمهمة: {brain['transformed_input']}"
        output = get_ai_response(prompt)
        return jsonify({"text": output, "trace": brain["logic_trace"], "video_prompt": brain.get("video_segments")}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
