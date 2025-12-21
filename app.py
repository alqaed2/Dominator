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

# ========= إعداد محركات AI 2025 =========
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

# مصفوفة الهيمنة لتجاوز خطأ 429 (التحميل الزائد)
MODELS_PRIORITY = [
    "gemini-2.0-flash",       # التوازن المثالي
    "gemini-1.5-flash",       # سرعة فائقة وحدود عالية
    "gemini-flash-latest"     # الملاذ الأخير للاستقرار
]

def get_ai_response_with_failover(prompt: str) -> str:
    last_error = ""
    for model_name in MODELS_PRIORITY:
        try:
            logger.info(f"Attempting execution with: {model_name}")
            model = genai.GenerativeModel(model_name)
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            last_error = str(e)
            if "429" in last_error:
                logger.warning(f"Model {model_name} rate limited. Switching...")
                continue
            return f"Critical Engine Error: {last_error}"
    return f"⚠️ عذراً، جميع المحركات مشغولة حالياً. يرجى الانتظار دقيقة واحدة. الخطأ: {last_error}"

# ========= مستخرج البيانات المطابق لـ index.html =========
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

# ========= المسارات المهيمنة =========

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/health")
def health():
    return jsonify({"status": "online", "system": "AI DOMINATOR V3.0"}), 200

@app.route("/generate/<platform>", methods=["POST", "GET"])
@app.route("/remix", methods=["POST", "GET"])
def handle_execution(platform="linkedin"):
    if request.method == "GET":
        return jsonify({"info": "POST expected"}), 200

    if request.path == "/remix": platform = "linkedin"

    # 1. استخراج البيانات
    idea, seed, style = extract_ui_data()
    actual_content = idea if idea else seed
    
    if not actual_content:
        return jsonify({"error": "يرجى إدخال فكرة أو منشور مرجعي للبدء"}), 400

    try:
        # 2. تشغيل الدماغ بمنطق المقاطع السينمائية
        brain = strategic_intelligence_core(idea, platform, style, seed)
        
        # 3. بناء الأمر وتوليد النص
        final_prompt = f"{WPIL_DOMINATOR_SYSTEM}\nالمنصة: {platform}\nالمهمة: {brain['transformed_input']}\nالأسلوب: {style}"
        generated_text = get_ai_response_with_failover(final_prompt)

        payload = {
            "platform": platform,
            "text": generated_text,
            "trace": brain["logic_trace"],
            "remixed_seed": idea if idea else seed,
            "sic_transformed_input": brain['transformed_input']
        }

        # 4. معالجة مقاطع الفيديو لتيك توك (بصيغة كود)
        if platform == "tiktok" and "video_segments" in brain:
            formatted_prompts = "🚀 **SUPREME ADVISOR VIDEO BLUEPRINT (9:16)**\n\n"
            for seg in brain["video_segments"]:
                formatted_prompts += f"### Scene: {seg['time']}\n```text\n{seg['prompt']}\n```\n\n"
            payload["video_prompt"] = formatted_prompts
        else:
            payload["video_prompt"] = brain.get("visual_prompt", "")

        return jsonify(payload), 200

    except Exception as e:
        logger.error(f"DEPLOYMENT CRASH: {str(e)}")
        return jsonify({"error": f"Internal Crash: {str(e)}"}), 500

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
