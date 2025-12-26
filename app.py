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

MODELS_POOL = ["gemini-1.5-flash", "gemini-2.0-flash-lite-001", "gemini-flash-latest"]
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def get_ai_response_nebula(prompt: str) -> str:
    for model_name in MODELS_POOL:
        try:
            model = genai.GenerativeModel(model_name)
            return model.generate_content(prompt).text
        except: continue
    return "🚨 المحرك مشغول."

def sanitize_visual_prompt(text):
    """تحويل البرومبت الطويل إلى كلمات مفتاحية قصيرة جداً لضمان عمل الرابط"""
    # استخراج الأسماء والصفات الأساسية فقط وحذف الكلمات الشائعة
    clean = re.sub(r'\[.*?\]', '', text) # حذف أي تاغات
    clean = clean.replace("Professional", "Pro").replace("Photography", "Photo")
    keywords = clean.split()[:15] # الاكتفاء بأول 15 كلمة فقط
    return " ".join(keywords)

def robust_parse_v12_8(text):
    parts = {"linkedin": "", "twitter": "", "tiktok": "", "visual": "Professional business office, 8k, realistic"}
    ln = re.search(r"\[LINKEDIN\](.*?)(?=\[TWITTER\]|\[TIKTOK\]|\[VISUAL_PROMPT\]|$)", text, re.S | re.I)
    tw = re.search(r"\[TWITTER\](.*?)(?=\[LINKEDIN\]|\[TIKTOK\]|\[VISUAL_PROMPT\]|$)", text, re.S | re.I)
    tk = re.search(r"\[TIKTOK\](.*?)(?=\[LINKEDIN\]|\[TWITTER\]|\[VISUAL_PROMPT\]|$)", text, re.S | re.I)
    vs = re.search(r"\[VISUAL_PROMPT\](.*?)$", text, re.S | re.I)
    
    if ln: parts["linkedin"] = ln.group(1).strip()
    if tw: parts["twitter"] = tw.group(1).strip()
    if tk: parts["tiktok"] = tk.group(1).strip()
    if vs: parts["visual"] = sanitize_visual_prompt(vs.group(1).strip())
    
    if not parts["linkedin"]: parts["linkedin"] = text
    return parts

@app.route("/")
def home(): return render_template("index.html")

@app.route("/alchemy/discover", methods=["POST"])
def discover():
    try:
        data = request.get_json(silent=True) or {}
        niche = data.get("niche", "السيادة")
        target = data.get("target_data", "")
        posts = [{"text": target if target else f"ترند {niche} 2026", "engagement": "Confirmed", "author": "Dominator"}]
        fusion = alchemy_fusion_core(posts, niche)
        output = get_ai_response_nebula(f"{WPIL_DOMINATOR_SYSTEM}\n{fusion['synthesis_task']}")
        return jsonify({"super_post": output, "sources": posts}), 200
    except Exception as e: return jsonify({"error": str(e)}), 500

@app.route("/generate_all", methods=["POST"])
def generate():
    try:
        data = request.get_json(silent=True) or {}
        idea = data.get("text", "الهيمنة")
        prompt = f"{WPIL_DOMINATOR_SYSTEM}\nتوليد حزمة سيادية (LinkedIn, X, TikTok) + وصف بصري احترافي قصير للفكرة: {idea}\nيجب إنهاء الرد بـ [VISUAL_PROMPT]."
        raw = get_ai_response_nebula(prompt)
        parsed = robust_parse_v12_8(raw)
        
        # إنشاء رابط الصورة المختصر (v12.8)
        seed = random.randint(1, 9999)
        clean_prompt = urllib.parse.quote(parsed['visual'])
        # استخدام رابط أبسط بدون معطيات معقدة لضمان التحميل
        image_url = f"https://image.pollinations.ai/prompt/{clean_prompt}?seed={seed}&nologo=true"
        
        return jsonify({**parsed, "image_url": image_url}), 200
    except Exception as e: return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
