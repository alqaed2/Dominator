import os
import sys
import json
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import google.generativeai as genai
from dominator_brain import strategic_intelligence_core, WPIL_DOMINATOR_SYSTEM

app = Flask(__name__, template_folder="templates", static_folder="static")
CORS(app)

# إعداد AI
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def get_ai_response(prompt):
    # تجربة الموديلات بالترتيب لتجنب خطأ 429
    for model_name in ["gemini-1.5-flash", "gemini-flash-latest"]:
        try:
            model = genai.GenerativeModel(model_name)
            return model.generate_content(prompt).text
        except: continue
    return "Error: AI engine busy."

# ========= مستخرج البيانات المطابق لـ index.html =========
def extract_ui_data():
    """هذه الدالة تطابق تماماً مسميات JavaScript في ملف index.html الخاص بك"""
    data = {}
    try:
        data = request.get_json(force=True, silent=True) or {}
    except: data = {}
    
    if request.form: data.update(request.form.to_dict())

    # المطابقة مع index.html:
    # 1. الفكرة تأتي في مفتاح 'text' (في generate) أو 'idea'
    idea = data.get('text') or data.get('idea') or ""
    
    # 2. المنشور المرجعي يأتي في 'winning_post' (في remix) أو 'seed'
    seed = data.get('winning_post') or data.get('seed') or ""
    
    # 3. الأسلوب يأتي في 'style_dna'
    style = data.get('style_dna') or data.get('style') or "Professional"
    
    return str(idea).strip(), str(seed).strip(), str(style).strip()

# ========= المسارات المهيمنة =========

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/generate/<platform>", methods=["POST", "GET"])
@app.route("/remix", methods=["POST", "GET"])
def handle_all(platform="linkedin"):
    if request.path == "/remix": platform = "linkedin"

    idea, seed, style = extract_ui_data()

    # التحقق: إذا وصل أي نص في أي حقل، سنعمل
    actual_content = idea if idea else seed
    
    if not actual_content:
        # إذا فشل كل شيء، سنرجع معلومات تقنية للمساعدة
        return jsonify({
            "error": "السيرفر لم يجد نصوصاً. تأكد من الكتابة في الصناديق.",
            "trace": "Check if index.html sends 'text' or 'winning_post'"
        }), 400

    try:
        # تشغيل الدماغ
        brain = strategic_intelligence_core(idea, platform, style, seed)
        
        prompt = f"{WPIL_DOMINATOR_SYSTEM}\nالمنصة: {platform}\nالمهمة: {brain['transformed_input']}\nالأسلوب: {style}"
        output = get_ai_response(prompt)

        return jsonify({
            "text": output,
            "platform": platform,
            "trace": brain["logic_trace"],
            "video_prompt": brain.get("visual_prompt") if platform == "tiktok" else "",
            "remixed_seed": idea if idea else seed, # لإرجاع البيانات للـ UI
            "sic_transformed_input": brain['transformed_input']
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
