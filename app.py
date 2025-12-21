import os
import sys
import json
import logging
import time
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import google.generativeai as genai
from dominator_brain import strategic_intelligence_core, WPIL_DOMINATOR_SYSTEM

app = Flask(__name__, template_folder="templates", static_folder="static")
CORS(app)
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger(__name__)

# ========= إعداد محركات AI (بروتوكول الاستمرارية 2025) =========
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

# مصفوفة الهيمنة المحدثة: تعطي الأولوية للموديلات ذات الحدود العالية (High Quota)
MODELS_PRIORITY = [
    "gemini-2.0-flash-lite",   # الأسرع والأعلى في حدود الطلبات (Quota)
    "gemini-flash-latest",     # الموديل المستقر (1.5 Flash) - حدود عالية جداً
    "gemini-2.0-flash",       # توازن بين الذكاء والسرعة
    "gemini-2.5-flash-lite",  # موديل القمة بنسخة Lite
    "gemini-2.5-flash"        # الخيار الأخير (قيود صارمة)
]

def get_ai_response_with_failover(prompt: str) -> str:
    last_error = ""
    for model_name in MODELS_PRIORITY:
        try:
            logger.info(f"🚀 Deploying on: {model_name}")
            model = genai.GenerativeModel(model_name)
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            last_error = str(e)
            logger.warning(f"⚠️ {model_name} busy or limited. Error: {last_error[:50]}...")
            # إذا كان الخطأ 429 (الحد المتجاوز)، ننتقل فوراً للتالي
            if "429" in last_error or "Quota" in last_error:
                continue
            # إذا كان خطأ 404 (موديل غير موجود)، ننتقل للتالي
            if "404" in last_error:
                continue
            return f"Strategic Engine Error: {last_error}"
    
    return f"⚠️ جميع الشبكات العصبية مشغولة بالطلبات حالياً. يرجى الانتظار 30 ثانية والمحاولة مجدداً لفتح مسار جديد."

# ========= مستخرج البيانات ذكياً =========
def extract_ui_data():
    data = {}
    try:
        data = request.get_json(force=True, silent=True) or {}
    except: data = {}
    if request.form: data.update(request.form.to_dict())

    idea = data.get('text') or data.get('idea') or data.get('topic') or ""
    seed = data.get('winning_post') or data.get('seed') or ""
    style = data.get('style_dna') or data.get('style') or "Professional"
    
    return str(idea).strip(), str(seed).strip(), str(style).strip()

# ========= المسارات الاستراتيجية =========

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/generate/<platform>", methods=["POST", "GET"])
@app.route("/remix", methods=["POST", "GET"])
def handle_execution(platform="linkedin"):
    if request.method == "GET":
        return jsonify({"status": "ready"}), 200

    if request.path == "/remix": platform = "linkedin"

    idea, seed, style = extract_ui_data()
    actual_content = idea if idea else seed
    
    if not actual_content:
        return jsonify({"error": "يرجى إدخال بيانات للتحليل"}), 400

    try:
        # 1. تشغيل الدماغ
        brain = strategic_intelligence_core(idea, platform, style, seed)
        
        # 2. توليد المحتوى بنظام الـ Failover الذكي
        final_prompt = f"{WPIL_DOMINATOR_SYSTEM}\nالمنصة: {platform}\nالمهمة: {brain['transformed_input']}\nالأسلوب: {style}"
        generated_text = get_ai_response_with_failover(final_prompt)

        payload = {
            "platform": platform,
            "text": generated_text,
            "trace": brain["logic_trace"],
            "remixed_seed": idea if idea else seed,
            "sic_transformed_input": brain['transformed_input']
        }

        # 3. برومبت الفيديو لتيك توك
        if platform == "tiktok" and "video_segments" in brain:
            formatted_prompts = "🎥 **SUPREME ADVISOR VIDEO BLUEPRINT (9:16)**\n\n"
            for seg in brain["video_segments"]:
                formatted_prompts += f"### Scene: {seg['time']}\n```text\n{seg['prompt']}\n```\n\n"
            payload["video_prompt"] = formatted_prompts
        else:
            payload["video_prompt"] = brain.get("visual_prompt", "")

        return jsonify(payload), 200

    except Exception as e:
        logger.error(f"CRITICAL CRASH: {str(e)}")
        return jsonify({"error": f"Internal Error: {str(e)}"}), 500

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
