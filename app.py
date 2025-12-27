import os
import re
import requests
import urllib.parse
import random
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import google.generativeai as genai

from dominator_brain import strategic_intelligence_core, alchemy_fusion_core, WPIL_DOMINATOR_SYSTEM

app = Flask(__name__, template_folder="templates", static_folder="static")
CORS(app)

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
MODELS = ["gemini-1.5-flash", "gemini-2.0-flash-lite-001"]

def get_ai_response_v14(prompt: str) -> str:
    for m in MODELS:
        try:
            return genai.GenerativeModel(m).generate_content(prompt).text
        except: continue
    return "🚨 المحرك مشغول."

def parse_v14(text):
    # نظام تقسيم فائق الدقة لضمان عدم ضياع التبويبات
    parts = {"linkedin": "", "twitter": "", "tiktok": "", "visual": "Professional business dashboard, 8k"}
    patterns = {
        "linkedin": r"\[LINKEDIN\](.*?)(?=\[TWITTER\]|\[TIKTOK\]|\[VISUAL_PROMPT\]|$)",
        "twitter": r"\[TWITTER\](.*?)(?=\[LINKEDIN\]|\[TIKTOK\]|\[VISUAL_PROMPT\]|$)",
        "tiktok": r"\[TIKTOK\](.*?)(?=\[LINKEDIN\]|\[TWITTER\]|\[VISUAL_PROMPT\]|$)",
        "visual": r"\[VISUAL_PROMPT\](.*?)$"
    }
    for key, pat in patterns.items():
        match = re.search(pat, text, re.S | re.I)
        if match: parts[key] = match.group(1).strip()
    
    if not parts["linkedin"]: parts["linkedin"] = text # Fallback
    return parts

@app.route("/")
def home(): return render_template("index.html")

@app.route("/alchemy/discover", methods=["POST"])
def discover():
    data = request.get_json(silent=True) or {}
    target = data.get("target_data", "")
    niche = data.get("niche", "Business")
    
    # استخدام الهدف المباشر كمرجع سياقي قسري
    posts = [{"text": target if target else f"Trend in {niche}", "engagement": "Direct Target", "author": "Target"}]
    fusion = alchemy_fusion_core(posts, niche)
    output = get_ai_response_v14(f"{WPIL_DOMINATOR_SYSTEM}\n{fusion['synthesis_task']}")
    return jsonify({"super_post": output, "sources": posts}), 200

@app.route("/generate_all", methods=["POST"])
def generate():
    data = request.get_json(silent=True) or {}
    idea = data.get("text", "السيادة")
    prompt = f"{WPIL_DOMINATOR_SYSTEM}\nالمهمة: ارفع مستوى هذا النص ليكون احترافياً ونخبوياً ومطابقاً للموضوع: {idea}\nيجب تقسيم الرد بوضوح تام."
    raw = get_ai_response_v14(prompt)
    parsed = parse_v14(raw)
    
    # توليد صورة واقعية مطابقة
    seed = random.randint(1, 9999)
    image_url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(parsed['visual'])}?seed={seed}&width=1080&height=1080&model=flux&nologo=true"
    
    brain = strategic_intelligence_core(idea)
    return jsonify({**parsed, "image_url": image_url, "video_blueprint": brain["video_segments"]}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
