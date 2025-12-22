import os
import sys
import json
import logging
import requests
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import google.generativeai as genai

# استيراد المكونات الثلاثة يقيناً
from dominator_brain import strategic_intelligence_core, alchemy_fusion_core, WPIL_DOMINATOR_SYSTEM

app = Flask(__name__, template_folder="templates", static_folder="static")
CORS(app)
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger(__name__)

# إعداد AI
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
MODELS_PRIORITY = ["gemini-2.0-flash-lite", "gemini-flash-latest"]
APIFY_API_KEY = os.getenv("APIFY_API_KEY")

def get_ai_response(prompt: str) -> str:
    for model_name in MODELS_PRIORITY:
        try:
            model = genai.GenerativeModel(model_name)
            return model.generate_content(prompt).text
        except: continue
    return "Error: AI Engines Busy."

def fetch_real_gold_posts(niche):
    if not APIFY_API_KEY: return get_mock_gold_posts(niche)
    try:
        actor_url = "https://api.apify.com/v2/acts/apidojo~tweet-scraper/run-sync-get-dataset-items"
        payload = {"searchMode": "top", "searchTerms": [niche], "maxTweets": 5}
        res = requests.post(f"{actor_url}?token={APIFY_API_KEY}", json=payload, timeout=40)
        if res.status_code in [200, 201]:
            data = res.json()
            return [{"text": i.get("full_text") or i.get("text", ""), "engagement": f"{i.get('favorite_count',0)} Likes", "platform": "X"} for i in data]
        return get_mock_gold_posts(niche)
    except: return get_mock_gold_posts(niche)

def get_mock_gold_posts(niche):
    return [{"text": f"استراتيجية الهيمنة في {niche}...", "engagement": "100K+", "platform": "Deep Logic"}]

@app.route("/")
def home(): return render_template("index.html")

@app.route("/alchemy/discover", methods=["POST"])
def discover():
    data = request.get_json(silent=True) or {}
    niche = data.get("niche", "القيادة")
    gold_posts = fetch_real_gold_posts(niche)
    fusion = alchemy_fusion_core(gold_posts, niche)
    output = get_ai_response(f"{WPIL_DOMINATOR_SYSTEM}\n{fusion['synthesis_task']}")
    return jsonify({"super_post": output, "sources": gold_posts, "trace": fusion["logic_trace"]}), 200

@app.route("/generate/<platform>", methods=["POST", "GET"])
def generate(platform):
    if request.method == "GET": return jsonify({"status": "ready"}), 200
    data = request.get_json(force=True, silent=True) or {}
    idea = data.get('text') or data.get('idea') or ""
    brain = strategic_intelligence_core(idea, platform)
    output = get_ai_response(f"{WPIL_DOMINATOR_SYSTEM}\nالمهمة: {brain['transformed_input']}\nالمنصة: {platform}")
    
    payload = {"platform": platform, "text": f"{output}{brain.get('viral_signature','')}", "trace": brain["logic_trace"]}
    if platform == "tiktok":
        v_prompt = "🚀 **VERTICAL 9:16 PROMPTS**\n\n"
        for seg in brain["video_segments"]:
            v_prompt += f"### {seg['time']}\n```text\n{seg['prompt']}\n```\n\n"
        payload["video_prompt"] = v_prompt
    return jsonify(payload), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
