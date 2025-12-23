import os
import time
import requests
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import google.generativeai as genai
from dominator_brain import strategic_intelligence_core, alchemy_fusion_core, WPIL_DOMINATOR_SYSTEM

app = Flask(__name__, template_folder="templates", static_folder="static")
CORS(app)

# إعداد AI مع مصفوفة ذكية
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
APIFY_API_KEY = os.getenv("APIFY_API_KEY")

def get_ai_response_final(prompt: str) -> str:
    # نستخدم الموديل المستقر أولاً لتفادي الـ 429
    models = ["gemini-1.5-flash", "gemini-2.0-flash-lite", "gemini-flash-latest"]
    for m in models:
        try:
            model = genai.GenerativeModel(m)
            return model.generate_content(prompt).text
        except Exception as e:
            if "429" in str(e): time.sleep(2) # انتظار ذكي في حال الزحام
            continue
    return "⚠️ المحرك مشغول حالياً، يرجى المحاولة بعد لحظات."

@app.route("/")
def home(): return render_template("index.html")

@app.route("/alchemy/discover", methods=["POST"])
def discover():
    data = request.get_json(silent=True) or {}
    niche = data.get("niche", "القيادة")
    
    # جلب البيانات مع fallback ذكي
    gold_posts = []
    if APIFY_API_KEY:
        try:
            res = requests.post("https://api.apify.com/v2/acts/apidojo~tweet-scraper/run-sync-get-dataset-items?token="+APIFY_API_KEY, 
                                json={"searchTerms": [niche], "maxTweets": 5, "searchMode": "top"}, timeout=30)
            if res.status_code in [200, 201]:
                gold_posts = [{"text": i.get("full_text") or i.get("text"), "engagement": f"{i.get('favorite_count',0)} Likes"} for i in res.json() if i.get("text")]
        except: pass

    if not gold_posts:
        gold_posts = [{"text": f"المعادلة الاستراتيجية للنجاح في {niche}", "engagement": "100K+"}]

    fusion = alchemy_fusion_core(gold_posts, niche)
    output = get_ai_response_final(f"{WPIL_DOMINATOR_SYSTEM}\n{fusion['synthesis_task']}")
    return jsonify({"super_post": output, "sources": gold_posts, "trace": fusion["logic_trace"]}), 200

@app.route("/generate/<platform>", methods=["POST"])
def generate(platform):
    data = request.get_json(silent=True) or {}
    idea = data.get('text') or data.get('idea') or "استراتيجية هيمنة"
    brain = strategic_intelligence_core(idea, platform)
    output = get_ai_response_final(f"{WPIL_DOMINATOR_SYSTEM}\nالمنصة: {platform}\nالمهمة: {brain['transformed_input']}")
    return jsonify({"text": f"{output}{brain.get('viral_signature','')}", "trace": brain["logic_trace"], "video_prompt": brain.get("video_segments")}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
