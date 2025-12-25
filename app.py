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

MODELS_POOL = ["gemini-2.0-flash-lite-001", "gemini-2.5-flash-lite", "gemini-flash-latest"]
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def get_ai_response_nebula(prompt: str) -> str:
    for model_name in MODELS_POOL:
        try:
            model = genai.GenerativeModel(model_name)
            return model.generate_content(prompt).text
        except: continue
    return "🚨 كافة المحركات مشغولة."

def parse_v12_5(text):
    parts = {"linkedin": "", "twitter": "", "tiktok": "", "visual": "Professional high-end business corporate photography"}
    # تقسيم النص الموحد بدقة أكبر
    ln = re.search(r"\[LINKEDIN\](.*?)(\[TWITTER\]|\[TIKTOK\]|\[VISUAL_PROMPT\]|$)", text, re.S | re.I)
    tw = re.search(r"\[TWITTER\](.*?)(\[LINKEDIN\]|\[TIKTOK\]|\[VISUAL_PROMPT\]|$)", text, re.S | re.I)
    tk = re.search(r"\[TIKTOK\](.*?)(\[LINKEDIN\]|\[TWITTER\]|\[VISUAL_PROMPT\]|$)", text, re.S | re.I)
    vs = re.search(r"\[VISUAL_PROMPT\](.*?)$", text, re.S | re.I)
    
    if ln: parts["linkedin"] = ln.group(1).strip()
    if tw: parts["twitter"] = tw.group(1).strip()
    if tk: parts["tiktok"] = tk.group(1).strip()
    if vs: parts["visual"] = "High-end professional photography, " + vs.group(1).strip().replace("magic", "").replace("fantasy", "")
    return parts

@app.route("/")
def home(): return render_template("index.html")

@app.route("/alchemy/discover", methods=["POST"])
def discover():
    data = request.get_json(silent=True) or {}
    niche = data.get("niche", "السيادة الرقمية")
    # بيانات بديلة احترافية
    posts = [{"text": f"المعادلة الاستراتيجية في {niche}", "engagement": "150K", "author": "Dominator_AI"}]
    fusion = alchemy_fusion_core(posts, niche)
    output = get_ai_response_nebula(f"{WPIL_DOMINATOR_SYSTEM}\n{fusion['synthesis_task']}")
    return jsonify({"super_post": output, "sources": posts}), 200

@app.route("/generate_all", methods=["POST"])
def generate():
    idea = request.get_json().get("text", "الهيمنة")
    prompt = f"{WPIL_DOMINATOR_SYSTEM}\nتوليد حزمة سيادية (نص + وصف بصري احترافي واقعي) للفكرة: {idea}\nيجب إنهاء الرد بـ [VISUAL_PROMPT]."
    raw = get_ai_response_nebula(prompt)
    parsed = parse_
