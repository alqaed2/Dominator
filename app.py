import os
import sys
import requests
import time
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import google.generativeai as genai

# استيراد صارم
from dominator_brain import strategic_intelligence_core, alchemy_fusion_core, WPIL_DOMINATOR_SYSTEM

app = Flask(__name__, template_folder="templates", static_folder="static")
CORS(app)

# إعداد AI
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
APIFY_API_KEY = os.getenv("APIFY_API_KEY")

def get_ai_response_safe(prompt: str) -> str:
    try:
        model = genai.GenerativeModel("gemini-1.5-flash") # الأكثر استقراراً للعمليات المتعددة
        return model.generate_content(prompt).text
    except Exception as e:
        return f"⚠️ المحرك مستعد، أعد المحاولة. (Error: {str(e)[:50]})"

def fetch_real_gold_posts(niche):
    # نظام السحب مع حماية التوقف
    if APIFY_API_KEY:
        try:
            actor_url = f"https://api.apify.com/v2/acts/apidojo~tweet-scraper/run-sync-get-dataset-items?token={APIFY_API_KEY}"
            res = requests.post(actor_url, json={"searchTerms": [niche], "maxTweets": 4, "searchMode": "top"}, timeout=15)
            if res.status_code in [200, 201]:
                return [{"text": i.get("text", "DNA"), "engagement": i.get('favorite_count', 0), "score": 90} for i in res.json()]
        except: pass
    return [{"text": f"المعادلة الاستراتيجية في {niche}", "engagement": "100K+", "score": 95}]

@app.route("/")
def home(): return render_template("index.html")

@app.route("/alchemy/discover", methods=["POST"])
def discover():
    data = request.get_json(silent=True) or {}
    niche = data.get("niche", "القيادة")
    posts = fetch_real_gold_posts(niche)
    fusion = alchemy_fusion_core(posts, niche)
    output = get_ai_response_safe(f"{WPIL_DOMINATOR_SYSTEM}\n{fusion['synthesis_task']}")
    return jsonify({"super_post": output, "sources": posts, "trace": fusion["logic_trace"]}), 200

@app.route("/generate_all", methods=["POST"])
def generate_all():
    data = request.get_json(silent=True) or {}
    idea = data.get('text') or "الهيمنة"
    prompt = f"{WPIL_DOMINATOR_SYSTEM}\nالمهمة: توليد 3 نسخ (LinkedIn, X, TikTok) لهذه الفكرة: {idea}\nنسق المخرجات بفخامة."
    output = get_ai_response_safe(prompt)
    brain = strategic_intelligence_core(idea)
    return jsonify({"combined_text": output, "trace": brain["logic_trace"], "video_prompt": brain["video_segments"]}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
