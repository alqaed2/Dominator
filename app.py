import os
import json
import logging
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import google.generativeai as genai
from dominator_brain import strategic_intelligence_core, WPIL_DOMINATOR_SYSTEM

app = Flask(__name__, template_folder="templates", static_folder="static")
CORS(app)

# إعدادات الـ AI
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def get_ai_response(prompt: str) -> str:
    try:
        model = genai.GenerativeModel("gemini-2.0-flash")
        return model.generate_content(prompt).text
    except Exception as e:
        return f"AI Error: {str(e)}"

# ========= مستخرج البيانات الخارق (The Absolute Ingestor) =========
def extract_data_no_matter_what():
    """
    هذا التابع مصمم للامتصاص المطلق للبيانات مهما كان خطأ الواجهة.
    """
    data = {}
    
    # 1. محاولة جلب JSON (بشكل قسري)
    try:
        data = request.get_json(force=True, silent=True) or {}
    except:
        data = {}

    # 2. دمج بيانات Form
    if request.form:
        data.update(request.form.to_dict())

    # 3. دمج بيانات الروابط
    if request.args:
        data.update(request.args.to_dict())

    # 4. الملاذ الأخير: البحث في الجسم الخام (Raw Body)
    if not data and request.data:
        try:
            # محاولة فك تشفير البيانات إذا كانت مرسلة كـ String
            raw_text = request.data.decode('utf-8')
            data = json.loads(raw_text)
        except:
            # إذا لم تكن JSON، نضعها في حقل 'idea' كافتراض
            data = {"idea": request.data.decode('utf-8')}

    # استخراج القيم مع دعم كافة المسميات الممكنة (Mapping)
    idea = data.get("idea") or data.get("topic") or data.get("content") or data.get("text") or ""
    seed = data.get("seed") or data.get("winning_post") or data.get("reference") or ""
    style = data.get("style") or "Professional"
    
    return str(idea).strip(), str(seed).strip(), str(style).strip()

# ========= المسارات الاستراتيجية =========

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/generate/<platform>", methods=["POST", "GET"])
@app.route("/remix", methods=["POST", "GET"])
def universal_handler(platform="linkedin"):
    if request.path == "/remix":
        platform = "linkedin"

    # استخراج البيانات بالبروتوكول الشامل
    idea, seed, style = extract_data_no_matter_what()

    # التحقق النهائي للتشغيل
    actual_content = idea if idea else seed
    
    if not actual_content:
        # رسالة خطأ ذكية تخبرنا ماذا وصل للسيرفر فعلياً للمساعدة في التشخيص
        debug_info = {
            "received_keys": list(request.form.keys()) if request.form else "None",
            "has_json": bool(request.get_json(silent=True)),
            "raw_data_length": len(request.data) if request.data else 0
        }
        return jsonify({
            "error": "فشل التشغيل: لم تصل بيانات. السيرفر مستعد ولكن الواجهة أرسلت طلباً فارغاً.",
            "debug": debug_info
        }), 400

    try:
        # تشغيل الدماغ (SIC)
        brain = strategic_intelligence_core(idea, platform, style, seed)
        
        # بناء الأمر النهائي للهيمنة
        final_prompt = f"{WPIL_DOMINATOR_SYSTEM}\nالمنصة: {platform}\nالمهمة: {brain['transformed_input']}\nالأسلوب: {style}"
        
        text = get_ai_response(final_prompt)

        return jsonify({
            "platform": platform,
            "text": text,
            "trace": brain["logic_trace"],
            "video_prompt": brain.get("visual_prompt", "") if platform == "tiktok" else ""
        }), 200

    except Exception as e:
        return jsonify({"error": f"Internal Crash: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
