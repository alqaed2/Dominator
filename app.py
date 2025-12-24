import os
import requests
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import google.generativeai as genai
from dominator_brain import strategic_intelligence_core, alchemy_fusion_core, WPIL_DOMINATOR_SYSTEM

app = Flask(__name__, template_folder="templates", static_folder="static")
CORS(app)

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
APIFY_API_KEY = os.getenv("APIFY_API_KEY")

def get_ai_response_unified(prompt: str) -> str:
    # الطلقة الواحدة لضمان عدم حظر الطلبات المتكررة
    model = genai.GenerativeModel("gemini-2.0-flash-lite")
    try:
        return model.generate_content(prompt).text
    except:
        return "⚠️ المحرك مشغول، حاول بعد لحظات."

def fetch_real_gold_posts(niche):
    if APIFY_API_KEY:
        try:
            actor_url = "https://api.apify.com/v2/acts/apidojo~tweet-scraper/run-sync-get-dataset-items?token="+APIFY_API_KEY
            res = requests.post(actor_url, json={"searchTerms": [niche], "maxTweets": 4, "searchMode": "top"}, timeout=20)
            if res.status_code in [200, 201]:
                return [{"text": i.get("full_text") or i.get("text"), "engagement": i.get('favorite_count', 0), "score": 80 + (i.get('favorite_count',0)%20)} for i in res.json() if i.get("text")]
        except: pass
    return [{"text": f"المعادلة الاستراتيجية في {niche}", "engagement": 12000, "score": 95}]

@app.route("/")
def home(): return render_template("index.html")

@app.route("/alchemy/discover", methods=["POST"])
def discover():
    data = request.get_json(silent=True) or {}
    niche = data.get("niche", "القيادة")
    gold_posts = fetch_real_gold_posts(niche)
    fusion = alchemy_fusion_core(gold_posts, niche)
    output = get_ai_response_unified(f"{WPIL_DOMINATOR_SYSTEM}\n{fusion['synthesis_task']}")
    return jsonify({"super_post": output, "sources": gold_posts, "trace": fusion["logic_trace"]}), 200

@app.route("/generate_all", methods=["POST"])
def generate_all():
    data = request.get_json(silent=True) or {}
    idea = data.get('text') or "الهيمنة السوقية"
    brain = strategic_intelligence_core(idea)
    
    prompt = f"{WPIL_DOMINATOR_SYSTEM}\nالمهمة: توليد 3 نسخ (LinkedIn, X, TikTok) لهذه الفكرة: {idea}\nاجعل النتائج منسقة جداً."
    output = get_ai_response_unified(prompt)
    
    return jsonify({"combined_text": output, "trace": brain["logic_trace"], "video_prompt": brain["video_segments"]}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
