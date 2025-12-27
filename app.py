import os
import re
import requests
import urllib.parse
import random
import time
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import google.generativeai as genai

# استيراد النواة السيادية
from dominator_brain import strategic_intelligence_core, alchemy_fusion_core, WPIL_DOMINATOR_SYSTEM

app = Flask(__name__, template_folder="templates", static_folder="static")
CORS(app)

# ========= ترسانة Nebula v14.1 الموسعة (7 موديلات) =========
MODELS_POOL = [
    "gemini-2.0-flash-lite-001", # الأسرع والأكثر توفراً
    "gemini-2.5-flash-lite",     # حصانة عالية ضد الضغط
    "gemini-2.0-flash",          # توازن ذكاء
    "gemini-2.5-flash",          # القمة الاستراتيجية
    "gemini-flash-latest",       # المحرك المستقر 1.5
    "gemini-pro-latest",         # الملاذ الأخير
    "gemini-1.5-flash"           # النسخة الاحتياطية
]

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
APIFY_KEY = os.getenv("APIFY_API_KEY")

def get_ai_response_nebula_v14(prompt: str) -> str:
    """بروتوكول Nebula المطور: جولة قسرية عبر 7 محركات لضمان الاستجابة"""
    for model_name in MODELS_POOL:
        try:
            print(f"📡 [COMMAND] Deploying Intelligence on: {model_name}")
            model = genai.GenerativeModel(model_name)
            response = model.generate_content(prompt)
            if response and response.text:
                return response.text
        except Exception as e:
            print(f"⚠️ [RETRY] {model_name} bypassed. Logic: {str(e)[:40]}")
            time.sleep(0.5) # انتظار تقني بسيط لمنع الحظر اللحظي
            continue
    return "🚨 كافة الشبكات العصبية مشغولة حالياً، يرجى المحاولة بعد 10 ثوانٍ."

def parse_v14(text):
    parts = {"linkedin": "", "twitter": "", "tiktok": "", "visual": "High-end professional business photography, realistic"}
    patterns = {
        "linkedin": r"\[LINKEDIN\](.*?)(?=\[TWITTER\]|\[TIKTOK\]|\[VISUAL_PROMPT\]|$)",
        "twitter": r"\[TWITTER\](.*?)(?=\[LINKEDIN\]|\[TIKTOK\]|\[VISUAL_PROMPT\]|$)",
        "tiktok": r"\[TIKTOK\](.*?)(?=\[LINKEDIN\]|\[TWITTER\]|\[VISUAL_PROMPT\]|$)",
        "visual": r"\[VISUAL_PROMPT\](.*?)$"
    }
    for key, pat in patterns.items():
        match = re.search(pat, text, re.S | re.I)
        if match: parts[key] = match.group(1).strip()
    if not parts["linkedin"]: parts["linkedin"] = text
    return parts

@app.route("/")
def home(): return render_template("index.html")

@app.route("/alchemy/discover", methods=["POST"])
def discover():
    try:
        data = request.get_json(silent=True) or {}
        target = data.get("target_data", "")
        niche = data.get("niche", "السيادة")
        posts = [{"text": target if target else f"Trend in {niche}", "engagement": "Confirmed", "author": "Target"}]
        fusion = alchemy_fusion_core(posts, niche)
        # استخدام Nebula لتخليق المختبر
        output = get_ai_response_nebula_v14(f"{WPIL_DOMINATOR_SYSTEM}\n{fusion['synthesis_task']}")
        return jsonify({"super_post": output, "sources": posts}), 200
    except Exception as e: return jsonify({"error": str(e)}), 500

@app.route("/generate_all", methods=["POST"])
def generate():
    try:
        data = request.get_json(silent=True) or {}
        idea = data.get("text", "السيادة")
        prompt = f"{WPIL_DOMINATOR_SYSTEM}\nتوليد حزمة سيادية كاملة متوافقة حرفياً مع الموضوع: {idea}\nأنهِ بـ [VISUAL_PROMPT]."
        raw = get_ai_response_nebula_v14(prompt)
        parsed = parse_v14(raw)
        
        seed = random.randint(1, 99999)
        quoted_v = urllib.parse.quote(parsed['visual'])
        image_url = f"https://image.pollinations.ai/prompt/{quoted_v}?seed={seed}&width=1024&height=1024&model=flux&nologo=true"
        
        brain = strategic_intelligence_core(idea)
        return jsonify({**parsed, "image_url": image_url, "video_blueprint": brain["video_segments"]}), 200
    except Exception as e: return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
