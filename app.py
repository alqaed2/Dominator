import os
import sys
import json
import logging
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import google.generativeai as genai

# استيراد الدماغ المطور
from dominator_brain import strategic_intelligence_core, WPIL_DOMINATOR_SYSTEM

# إعداد التطبيق والسجلات
app = Flask(__name__, template_folder="templates", static_folder="static")
CORS(app)
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger(__name__)

# ========= إعداد محركات AI (تحديث 21 ديسمبر 2025) =========
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

# مصفوفة الهيمنة - تم اختيار الأسماء بناءً على قائمتك "المتاحة" يقيناً
MODELS_PRIORITY = [
    "gemini-2.5-flash",       # طراز القمة لعام 2025 (متاح في قائمتك)
    "gemini-2.0-flash",       # الطراز المستقر فائق السرعة (متاح في قائمتك)
    "gemini-flash-latest"     # البديل الشامل لضمان التشغيل (متاح في قائمتك)
]

def get_ai_response_with_failover(prompt: str) -> str:
    last_error = ""
    for model_name in MODELS_PRIORITY:
        try:
            logger.info(f"Deploying Brain on: {model_name}")
            # نستخدم التسمية الكاملة للتأكد من الموثوقية
            model = genai.GenerativeModel(model_name)
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            last_error = str(e)
            logger.error(f"Execution failed on {model_name}: {last_error}")
            # إذا كان الخطأ 404 أو 429، ننتقل للموديل التالي فوراً
            if "404" in last_error or "429" in last_error:
                continue
            return f"Strategic Engine Error: {last_error}"
    
    return f"⚠️ انقطاع في الاتصال بالشبكة العصبية العالمية. يرجى المحاولة لاحقاً. الخطأ الأخير: {last_error}"

# ========= مستخرج البيانات ذكياً =========
def extract_ui_data():
    data = {}
    try:
        data = request.get_json(force=True, silent=True) or {}
    except: data = {}
    
    if request.form: data.update(request.form.to_dict())

    # المطابقة مع مسميات JavaScript في index.html
    idea = data.get('text') or data.get('idea') or data.get('topic') or ""
    seed = data.get('winning_post') or data.get('seed') or ""
    style = data.get('style_dna') or data.get('style') or "Professional"
    
    return str(idea).strip(), str(seed).strip(), str(style).strip()

# ========= المسارات الاستراتيجية المهيمنة =========

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
        return jsonify({"error": "يرجى إدخال مادة خام للعمل عليها"}), 400

    try:
        # 1. تشغيل الدماغ الاستراتيجي
        brain = strategic_intelligence_core(idea, platform, style, seed)
        
        # 2. بناء الميثاق وتوليد النتائج عبر نظام الـ Failover
        final_prompt = f"{WPIL_DOMINATOR_SYSTEM}\nالمنصة المستهدفة: {platform}\nالمهمة: {brain['transformed_input']}\nالأسلوب: {style}"
        generated_text = get_ai_response_with_failover(final_prompt)

        payload = {
            "platform": platform,
            "text": generated_text,
            "trace": brain["logic_trace"],
            "remixed_seed": idea if idea else seed,
            "sic_transformed_input": brain['transformed_input']
        }

        # 3. معالجة الفيديو لمنصة TikTok
        if platform == "tiktok" and "video_segments" in brain:
            formatted_prompts = "🎥 **SUPREME ADVISOR VIDEO BLUEPRINT (9:16)**\n\n"
            for seg in brain["video_segments"]:
                formatted_prompts += f"### Scene: {seg['time']}\n```text\n{seg['prompt']}\n```\n\n"
            payload["video_prompt"] = formatted_prompts
        else:
            payload["video_prompt"] = brain.get("visual_prompt", "")

        return jsonify(payload), 200

    except Exception as e:
        logger.error(f"SYSTEM CRITICAL CRASH: {str(e)}")
        return jsonify({"error": f"Internal Crash: {str(e)}"}), 500

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
