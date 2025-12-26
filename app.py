import os
import re
import random
import urllib.parse
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import google.generativeai as genai

from dominator_brain import WPIL_DOMINATOR_SYSTEM, alchemy_fusion_core

app = Flask(__name__, template_folder="templates", static_folder="static")
CORS(app)

# مصفوفة النماذج للتبديل التلقائي (Failover System)
MODELS_POOL = ["gemini-2.0-flash-lite-001", "gemini-1.5-flash", "gemini-1.5-pro"]
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def get_ai_response_nebula(prompt: str) -> str:
    """نظام التبديل التلقائي لضمان استقرار 100%"""
    last_error = ""
    for model_name in MODELS_POOL:
        try:
            model = genai.GenerativeModel(model_name)
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            last_error = str(e)
            continue
    return f"🚨 خطأ في كافة النماذج: {last_error}"

def generate_visual_identity(idea: str) -> str:
    """استخدام Gemini لابتكار وصف بصري احترافي"""
    prompt = f"Create a short, highly detailed English image prompt for: {idea}. Focus on: professional lighting, 8k, cinematic, business environment. No text in image. Max 20 words."
    visual_description = get_ai_response_nebula(prompt)
    # تنظيف النص من أي زيادات
    clean_prompt = re.sub(r'[^a-zA-Z0-9\s,]', '', visual_description)
    return clean_prompt

@app.route("/")
def home(): return render_template("index.html")

@app.route("/alchemy/discover", methods=["POST"])
def discover():
    try:
        data = request.get_json(silent=True) or {}
        niche = data.get("niche", "السيادة")
        target = data.get("target_data", "")
        posts = [{"text": target if target else f"ترند {niche} 2026"}]
        fusion = alchemy_fusion_core(posts, niche)
        output = get_ai_response_nebula(f"{WPIL_DOMINATOR_SYSTEM}\n{fusion['synthesis_task']}")
        return jsonify({"super_post": output, "status": "success"}), 200
    except Exception as e: return jsonify({"error": str(e)}), 500

@app.route("/generate_all", methods=["POST"])
def generate():
    try:
        data = request.get_json(silent=True) or {}
        idea = data.get("text", "Business Success")
        
        # 1. توليد النصوص
        prompt = f"{WPIL_DOMINATOR_SYSTEM}\nتوليد حزمة سيادية (LinkedIn, X, TikTok) للفكرة: {idea}\nأنهِ الرد بـ [VISUAL_PROMPT] يصف الصورة المناسبة بالإنجليزية."
        raw_text = get_ai_response_nebula(prompt)
        
        # 2. تحليل النصوص
        parts = {"linkedin": "", "twitter": "", "tiktok": "", "visual": ""}
        ln = re.search(r"\[LINKEDIN\](.*?)(?=\[TWITTER\]|\[TIKTOK\]|\[VISUAL_PROMPT\]|$)", raw_text, re.S | re.I)
        tw = re.search(r"\[TWITTER\](.*?)(?=\[LINKEDIN\]|\[TIKTOK\]|\[VISUAL_PROMPT\]|$)", raw_text, re.S | re.I)
        tk = re.search(r"\[TIKTOK\](.*?)(?=\[LINKEDIN\]|\[TWITTER\]|\[VISUAL_PROMPT\]|$)", raw_text, re.S | re.I)
        vs = re.search(r"\[VISUAL_PROMPT\](.*?)$", raw_text, re.S | re.I)
        
        parts["linkedin"] = ln.group(1).strip() if ln else raw_text
        parts["twitter"] = tw.group(1).strip() if tw else ""
        parts["tiktok"] = tk.group(1).strip() if tk else ""
        
        # 3. توليد الصورة عبر محرك Nebula (Gemini + High-Res Renderer)
        visual_idea = vs.group(1).strip() if vs else idea
        refined_visual_prompt = generate_visual_identity(visual_idea)
        
        seed = random.randint(1, 99999)
        encoded_prompt = urllib.parse.quote(refined_visual_prompt)
        # استخدام نظام توزيع الحمل (Load Balancing) للصور
        image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?seed={seed}&width=1080&height=1350&nologo=true"
        
        return jsonify({**parts, "image_url": image_url}), 200
    except Exception as e: return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
