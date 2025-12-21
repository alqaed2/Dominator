import os
import json
import logging
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import google.generativeai as genai
from dominator_brain import strategic_intelligence_core, WPIL_DOMINATOR_SYSTEM

app = Flask(__name__, template_folder="templates", static_folder="static")
CORS(app)

# ========= مركز القيادة للموديلات 2025 =========
# مصفوفة الهيمنة: المحرك سيجرب هذه الموديلات بالترتيب في حال فشل أحدهما
MODELS_PRIORITY = [
    "gemini-2.5-flash",       # الأعلى ذكاءً
    "gemini-2.5-flash-lite",  # الأعلى في حدود الطلبات (Quota)
    "gemini-flash-latest"     # الأكثر استقراراً (Legacy)
]

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

def get_ai_response_with_failover(prompt: str) -> str:
    """
    نظام استجابة حصين: يجرب الموديلات بالترتيب لتجاوز خطأ 429.
    """
    last_error = ""
    for model_name in MODELS_PRIORITY:
        try:
            print(f"[SYSTEM] Attempting with model: {model_name}")
            model = genai.GenerativeModel(model_name)
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            last_error = str(e)
            if "429" in last_error:
                print(f"[WARNING] Model {model_name} reached limit. Switching to next...")
                continue # جرب الموديل التالي
            else:
                return f"Critical Engine Error: {last_error}"
    
    return f"⚠️ جميع المحركات مشغولة حالياً (خطأ 429). يرجى المحاولة بعد دقيقة واحدة. آخر خطأ: {last_error}"

# ========= مستخرج البيانات الشامل =========
def extract_universal_data():
    data = {}
    try:
        data = request.get_json(force=True, silent=True) or {}
    except: pass
    if request.form: data.update(request.form.to_dict())
    
    idea = data.get("idea") or data.get("topic") or data.get("content") or ""
    seed = data.get("seed") or data.get("winning_post") or data.get("reference") or ""
    style = data.get("style") or "Professional"
    
    return str(idea).strip(), str(seed).strip(), str(style).strip()

# ========= المسارات الاستراتيجية =========

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/generate/<platform>", methods=["POST", "GET"])
@app.route("/remix", methods=["POST", "GET"])
def execute(platform="linkedin"):
    if request.path == "/remix": platform = "linkedin"

    idea, seed, style = extract_universal_data()
    actual_input = idea if idea else seed
    
    if not actual_input:
        return jsonify({"error": "يرجى إدخال فكرة أو منشور مرجعي"}), 400

    try:
        # 1. تشغيل الدماغ (SIC)
        brain = strategic_intelligence_core(idea, platform, style, seed)
        
        # 2. توليد المحتوى بنظام الـ Failover
        final_prompt = f"""
        {WPIL_DOMINATOR_SYSTEM}
        المنصة: {platform}
        المهمة الاستراتيجية: {brain['transformed_input']}
        الأسلوب: {style}
        """
        
        text = get_ai_response_with_failover(final_prompt)

        return jsonify({
            "platform": platform,
            "text": text,
            "trace": brain["logic_trace"],
            "video_prompt": brain.get("visual_prompt") if platform == "tiktok" else ""
        }), 200

    except Exception as e:
        return jsonify({"error": f"Internal Crash: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
