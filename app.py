from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os
import google.generativeai as genai

# استيراد المحرك المصلح
from dominator_brain import strategic_intelligence_core, WPIL_DOMINATOR_SYSTEM

# استيراد الذاكرة مع معالجة حالة عدم الوجود
try:
    from sic_memory import record_success, record_failure
except ImportError:
    def record_success(p): pass
    def record_failure(p): pass

app = Flask(__name__, template_folder="templates", static_folder="static")
CORS(app)

# ========= الإعدادات التقنية =========
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
# استخدام فلاش 2.0 للسرعة القصوى والاكتساح
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")

if not GEMINI_API_KEY:
    print("CRITICAL ERROR: GEMINI_API_KEY IS MISSING!")
else:
    genai.configure(api_key=GEMINI_API_KEY)

def get_ai_response(prompt: str) -> str:
    try:
        model = genai.GenerativeModel(GEMINI_MODEL)
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"خطأ في الاتصال بالمحرك الذكي: {str(e)}"

# ========= المسارات الاستراتيجية (Endpoints) =========

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "active", "engine": "AI Dominator V2.0"}), 200

@app.route("/generate/<platform>", methods=["POST"])
def generate_content(platform):
    data = request.get_json(silent=True) or {}
    idea = data.get("idea", "").strip()
    style = data.get("style", "default").strip()

    if not idea:
        return jsonify({"error": "الفكرة مطلوبة للبدء"}), 400

    try:
        # 1. تشغيل الدماغ الاستراتيجي (SIC)
        brain_result = strategic_intelligence_core(idea=idea, platform=platform, style=style)
        
        # 2. بناء الأمر النهائي للذكاء الاصطناعي
        final_prompt = f"""
        {WPIL_DOMINATOR_SYSTEM}
        
        الهدف: توليد محتوى مهيمن لمنصة {platform}.
        الأسلوب المطلوب: {style}
        النص بعد المعالجة الاستراتيجية: {brain_result['transformed_input']}
        
        المطلوب:
        - نص احترافي باللغة العربية.
        - هيكلية قوية (Hook, Value, CTA).
        - إذا كانت المنصة TikTok، اجعل النص سكريبت مقسم بلقطات.
        """

        generated_text = get_ai_response(final_prompt)

        # 3. تجهيز النتائج للبصريات (إذا لزم الأمر)
        payload = {
            "platform": platform,
            "text": generated_text,
            "trace": brain_result['logic_trace']
        }

        if platform == "tiktok":
            payload["video_prompt"] = get_ai_response(f"Convert this script to a cinematic video generation prompt (English): {generated_text}")

        record_success(platform)
        return jsonify(payload), 200

    except Exception as e:
        record_failure(platform)
        return jsonify({"error": f"انهيار في النظام: {str(e)}"}), 500

@app.route("/remix", methods=["POST"])
def remix():
    data = request.get_json(silent=True) or {}
    niche = data.get("niche", "")
    seed = data.get("seed", "")
    
    prompt = f"{WPIL_DOMINATOR_SYSTEM}\nأعد صياغة هذه الفكرة (Seed: {seed}) لمجال ({niche}) بأسلوب رابح ومؤثر."
    result = get_ai_response(prompt)
    return jsonify({"text": result}), 200

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
