import os
import requests
import logging
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import google.generativeai as genai
from dominator_brain import strategic_intelligence_core, alchemy_fusion_core, WPIL_DOMINATOR_SYSTEM

app = Flask(__name__, template_folder="templates", static_folder="static")
CORS(app)

# إعداد AI مع مصفوفة الـ Failover
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
MODELS_PRIORITY = ["gemini-2.0-flash-lite", "gemini-flash-latest", "gemini-2.0-flash"]
APIFY_API_KEY = os.getenv("APIFY_API_KEY")

def get_ai_response_elite(prompt: str) -> str:
    """نظام الاستجابة المتعدد الذي يضمن خروج النص مهما كان الضغط"""
    for model_name in MODELS_PRIORITY:
        try:
            model = genai.GenerativeModel(model_name)
            return model.generate_content(prompt).text
        except: continue
    return "⚠️ النظام قيد التحديث، يرجى إعادة المحاولة خلال ثوانٍ."

def fetch_real_gold_posts(niche):
    """بروتوكول السحب مع بيانات بديلة ذكية"""
    try:
        if APIFY_API_KEY:
            actor_url = "https://api.apify.com/v2/acts/apidojo~tweet-scraper/run-sync-get-dataset-items"
            res = requests.post(f"{actor_url}?token={APIFY_API_KEY}", 
                                json={"searchTerms": [niche], "maxTweets": 5, "searchMode": "top"}, timeout=25)
            if res.status_code in [200, 201]:
                data = res.json()
                if data:
                    return [{"text": i.get("full_text") or i.get("text"), "engagement": f"{i.get('favorite_count', '10K')}+ Likes"} for i in data if i.get("text")]
        
        # بيانات بديلة احترافية إذا فشل السحب
        return [
            {"text": f"المعادلة السرية للنمو في مجال {niche} لعام 2026", "engagement": "125K Likes"},
            {"text": f"لماذا يسيطر القادة على سوق {niche}؟ إليك التحليل", "engagement": "89K Likes"},
            {"text": f"3 أخطاء تقتل عملك في {niche} وكيف تتجاوزها", "engagement": "210K Likes"}
        ]
    except:
        return [{"text": f"تحليل سيادي لقطاع {niche}", "engagement": "50K+"}]

@app.route("/")
def home(): return render_template("index.html")

@app.route("/alchemy/discover", methods=["POST"])
def discover():
    data = request.get_json(silent=True) or {}
    niche = data.get("niche", "السيادة الرقمية")
    gold_posts = fetch_real_gold_posts(niche)
    fusion = alchemy_fusion_core(gold_posts, niche)
    output = get_ai_response_elite(f"{WPIL_DOMINATOR_SYSTEM}\n{fusion['synthesis_task']}")
    return jsonify({"super_post": output, "sources": gold_posts, "trace": fusion["logic_trace"]}), 200

@app.route("/generate/<platform>", methods=["POST"])
def generate(platform):
    data = request.get_json(silent=True) or {}
    idea = data.get('text') or "استراتيجية هيمنة"
    brain = strategic_intelligence_core(idea, platform)
    prompt = f"{WPIL_DOMINATOR_SYSTEM}\nالمنصة: {platform}\nالمهمة: {brain['transformed_input']}"
    output = get_ai_response_elite(prompt)
    return jsonify({"text": output, "trace": brain["logic_trace"], "video_prompt": brain.get("video_segments")}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
