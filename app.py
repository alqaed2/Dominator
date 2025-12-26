import os
import re
import requests
import json
import urllib.parse
import random
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import google.generativeai as genai

from dominator_brain import strategic_intelligence_core, alchemy_fusion_core, WPIL_DOMINATOR_SYSTEM

app = Flask(__name__, template_folder="templates", static_folder="static")
CORS(app)

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
MODELS = ["gemini-1.5-flash", "gemini-2.0-flash-lite", "gemini-flash-latest"]

def get_ai_response_nebula(prompt: str) -> str:
    for m in MODELS:
        try:
            return genai.GenerativeModel(m).generate_content(prompt).text
        except: continue
    return "🚨 كافة المحركات مشغولة."

def robust_parse(text):
    parts = {"linkedin": "", "twitter": "", "tiktok": "", "visual": "Professional business office, realistic, 8k"}
    ln = re.search(r"\[LINKEDIN\](.*?)(?=\[TWITTER\]|\[TIKTOK\]|\[VISUAL_PROMPT\]|$)", text, re.S | re.I)
    tw = re.search(r"\[TWITTER\](.*?)(?=\[LINKEDIN\]|\[TIKTOK\]|\[VISUAL_PROMPT\]|$)", text, re.S | re.I)
    tk = re.search(r"\[TIKTOK\](.*?)(?=\[LINKEDIN\]|\[TWITTER\]|\[VISUAL_PROMPT\]|$)", text, re.S | re.I)
    vs = re.search(r"\[VISUAL_PROMPT\](.*?)$", text, re.S | re.I)
    
    if ln: parts["linkedin"] = ln.group(1).strip()
    if tw: parts["twitter"] = tw.group(1).strip()
    if tk: parts["tiktok"] = tk.group(1).strip()
    if vs: parts["visual"] = "High-end business photography, " + vs.group(1).strip()[:300]
    if not parts["linkedin"]: parts["linkedin"] = text
    return parts

@app.route("/")
def home(): return render_template("index.html")

@app.route("/alchemy/discover", methods=["POST"])
def discover():
    data = request.get_json(silent=True) or {}
    posts = [{"text": data.get("target_data", "تحليل سيادي"), "engagement": "Confirmed", "author": "Target"}]
    fusion = alchemy_fusion_core(posts, data.get("niche", "القيادة"))
    output = get_ai_response_nebula(f"{WPIL_DOMINATOR_SYSTEM}\n{fusion['synthesis_task']}")
    return jsonify({"super_post": output, "sources": posts}), 200

@app.route("/generate_all", methods=["POST"])
def generate():
    try:
        data = request.get_json(silent=True) or {}
        idea = data.get("text", "السيادة")
        prompt = f"{WPIL_DOMINATOR_SYSTEM}\nتوليد حزمة سيادية كاملة للفكرة: {idea}\nيجب إنهاء الرد بـ [VISUAL_PROMPT]."
        raw = get_ai_response_nebula(prompt)
        parsed = robust_parse(raw)
        
        # توليد الصورة
        seed = random.randint(1, 9999)
        image_url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(parsed['visual'])}?seed={seed}&nologo=true"
        
        # استدعاء مخطط الفيديو من الدماغ
        brain = strategic_intelligence_core(idea)
        
        return jsonify({
            **parsed, 
            "image_url": image_url, 
            "video_blueprint": brain["video_segments"]
        }), 200
    except Exception as e: return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
