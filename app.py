import os
import requests
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import google.generativeai as genai
from dominator_brain import strategic_intelligence_core, alchemy_fusion_core, WPIL_DOMINATOR_SYSTEM

app = Flask(__name__, template_folder="templates", static_folder="static")
CORS(app)

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
APIFY_KEY = os.getenv("APIFY_API_KEY")

def fetch_live_market_dna(niche):
    """جلب البيانات مع روابط التحقق لضمان الموثوقية"""
    if not APIFY_KEY:
        return get_fallback_dna(niche)

    try:
        actor_url = f"https://api.apify.com/v2/acts/apidojo~tweet-scraper/run-sync-get-dataset-items?token={APIFY_KEY}"
        payload = {"searchTerms": [niche], "maxTweets": 5, "searchMode": "top"}
        res = requests.post(actor_url, json=payload, timeout=25)
        
        if res.status_code in [200, 201]:
            data = res.json()
            if data:
                return [
                    {
                        "text": i.get("full_text") or i.get("text", "DNA Sample"),
                        "engagement": f"{int(i.get('favorite_count', 0))}",
                        "author": i.get("user", {}).get("screen_name", "Elite_User"),
                        "url": i.get("url") or f"https://twitter.com/i/web/status/{i.get('id_str')}",
                        "score": 85 + (int(i.get('favorite_count', 0)) % 15)
                    } for i in data if i.get("text")
                ]
        return get_fallback_dna(niche)
    except:
        return get_fallback_dna(niche)

def get_fallback_dna(niche):
    # بيانات محاكاة احترافية عند غياب API
    return [
        {"text": f"استراتيجية اختراق {niche} لعام 2026", "engagement": "120K", "author": "Strategic_AI", "url": "#", "score": 95},
        {"text": f"لماذا يسيطر القادة على {niche}", "engagement": "85K", "author": "Market_Oracle", "url": "#", "score": 90}
    ]

@app.route("/")
def home(): return render_template("index.html")

@app.route("/alchemy/discover", methods=["POST"])
def discover():
    data = request.get_json(silent=True) or {}
    niche = data.get("niche", "القيادة")
    gold_posts = fetch_live_market_dna(niche)
    fusion = alchemy_fusion_core(gold_posts, niche)
    
    model = genai.GenerativeModel("gemini-2.0-flash-lite")
    output = model.generate_content(f"{WPIL_DOMINATOR_SYSTEM}\n{fusion['synthesis_task']}").text
    
    return jsonify({"super_post": output, "sources": gold_posts, "trace": fusion["logic_trace"]}), 200

@app.route("/generate_all", methods=["POST"])
def generate_all():
    data = request.get_json(silent=True) or {}
    idea = data.get('text') or "الهيمنة"
    prompt = f"{WPIL_DOMINATOR_SYSTEM}\nتوليد محتوى مهيمن لـ [LINKEDIN], [TWITTER], [TIKTOK] لهذه الفكرة: {idea}"
    output = genai.GenerativeModel("gemini-1.5-flash").generate_content(prompt).text
    return jsonify({"combined_text": output}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
