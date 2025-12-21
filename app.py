from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os
import google.generativeai as genai
from dominator_brain import strategic_intelligence_core, WPIL_DOMINATOR_SYSTEM

app = Flask(__name__, template_folder="templates", static_folder="static")
CORS(app)

# ========= إعداد المحرك =========
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

def get_ai_response(prompt: str) -> str:
    try:
        model = genai.GenerativeModel("gemini-2.0-flash")
        return model.generate_content(prompt).text
    except Exception as e:
        return f"خطأ في المحرك الذكي: {str(e)}"

def extract_all_data():
    """
    مستخرج بيانات ذكي: يبحث في JSON و Form و Args عن أي محتوى.
    """
    # 1. محاولة جلب البيانات من JSON
    data = request.get_json(silent=True) or {}
    # 2. دمجها مع بيانات Form (إذا وجدت)
    form_data = request.form.to_dict()
    data.update(form_data)
    
    # البحث عن الفكرة بكل المسميات الممكنة
    idea = data.get("idea") or data.get("topic") or data.get("content") or ""
    # البحث عن المنشور المرجعي (Seed)
    seed = data.get("seed") or data.get("reference") or data.get("winning_post") or ""
    # البحث عن النيش والأسلوب
    niche = data.get("niche") or ""
    style = data.get("style") or "Professional"
    
    return str(idea).strip(), str(seed).strip(), str(niche).strip(), str(style).strip()

# ========= المسارات الاستراتيجية =========

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/generate/<platform>", methods=["POST", "GET"])
def generate_content(platform):
    # دعم GET فقط لإرجاع رسالة توضيحية، العمل الحقيقي في POST
    if request.method == "GET":
        return jsonify({"info": f"Endpoint for {platform} is active. Use POST."}), 200

    # استخراج البيانات بذكاء
    idea, seed, niche, style = extract_all_data()

    # إذا كان كلاهما فارغاً، نقوم بمحاولة أخيرة من الـ URL Parameters
    if not idea and not seed:
        idea = request.args.get("idea", "")
        seed = request.args.get("seed", "")

    # فحص القبول النهائي
    actual_content = idea if idea else seed
    if not actual_content:
        return jsonify({"error": "فشل التشغيل: يرجى إدخال فكرة أو منشور مرجعي للبدء"}), 400

    try:
        # تشغيل الدماغ بمنطق الاندماج
        brain = strategic_intelligence_core(idea=idea, platform=platform, style=style, reference_post=seed)
        
        final_prompt = f"""
        {WPIL_DOMINATOR_SYSTEM}
        المهمة: {brain['transformed_input']}
        المنصة: {platform}
        الأسلوب: {style}
        """
        
        generated_text = get_ai_response(final_prompt)

        return jsonify({
            "platform": platform,
            "text": generated_text,
            "trace": brain["logic_trace"]
        }), 200

    except Exception as e:
        return jsonify({"error": f"Internal Crash: {str(e)}"}), 500

@app.route("/remix", methods=["POST", "GET"])
def remix():
    # توحيد مسار الريمكس مع المحرك الرئيسي لضمان القوة
    return generate_content("linkedin")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
