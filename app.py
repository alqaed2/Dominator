import os
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import google.generativeai as genai

# استيراد الدماغ المصلح
from dominator_brain import strategic_intelligence_core, WPIL_DOMINATOR_SYSTEM

app = Flask(__name__, template_folder="templates", static_folder="static")
CORS(app)

# ========= إعدادات المحرك الذكي =========
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

def get_ai_response(prompt: str) -> str:
    try:
        # استخدام موديل الفلاش لسرعة الاستجابة والاكتساح
        model = genai.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"فشل المحرك الذكي: {str(e)}"

# ========= مركز استخراج البيانات ذكياً =========
def extract_data():
    """يجلب البيانات من JSON أو Form بكل مرونة"""
    data = request.get_json(silent=True) or {}
    form = request.form.to_dict()
    data.update(form)
    
    idea = data.get("idea") or data.get("topic") or ""
    seed = data.get("seed") or data.get("reference") or ""
    style = data.get("style") or "Professional"
    
    return str(idea).strip(), str(seed).strip(), str(style).strip()

# ========= المسارات الاستراتيجية =========

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/generate/<platform>", methods=["POST", "GET"])
def generate(platform):
    if request.method == "GET":
        return jsonify({"status": "active"}), 200

    idea, seed, style = extract_data()
    
    # التحقق من وجود أي مدخل للعمل عليه
    actual_input = idea if idea else seed
    if not actual_input:
        return jsonify({"error": "يرجى إدخال فكرة أو منشور مرجعي"}), 400

    try:
        # 1. تشغيل الدماغ بمنطق الاندماج (Fusion)
        brain = strategic_intelligence_core(idea=idea, platform=platform, style=style, reference_post=seed)
        
        # 2. بناء الأمر النهائي للذكاء الاصطناعي
        final_prompt = f"""
        {WPIL_DOMINATOR_SYSTEM}
        المهمة المطلوبة: {brain['transformed_input']}
        المنصة: {platform}
        الأسلوب البصري واللفظي: {style}
        
        المطلوب: توليد محتوى مهيمن باللغة العربية بجودة استشارية عليا.
        """
        
        generated_text = get_ai_response(final_prompt)

        return jsonify({
            "platform": platform,
            "text": generated_text,
            "trace": brain["logic_trace"],
            "video_prompt": brain.get("visual_prompt", "") if platform == "tiktok" else ""
        }), 200

    except Exception as e:
        return jsonify({"error": f"Internal Error: {str(e)}"}), 500

@app.route("/remix", methods=["POST", "GET"])
def remix_legacy():
    # توجيد مسار الريمكس القديم مع المحرك الجديد
    return generate("linkedin")

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
