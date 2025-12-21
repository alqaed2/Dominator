import os
import sys
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import google.generativeai as genai

# استيراد الدماغ
from dominator_brain import strategic_intelligence_core, WPIL_DOMINATOR_SYSTEM

app = Flask(__name__, template_folder="templates", static_folder="static")
CORS(app)

# ========= إعداد المحرك =========
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

def get_ai_response(prompt: str) -> str:
    try:
        model = genai.GenerativeModel("gemini-2.0-flash")
        return model.generate_content(prompt).text
    except Exception as e:
        return f"Engine Error: {str(e)}"

# ========= مستخرج البيانات النووي (The Ingestor) =========
def extract_universal_data():
    """يبحث عن البيانات في كل مكان وبأي مسمى محتمل من الواجهة"""
    data = {}
    
    # 1. البحث في JSON
    json_data = request.get_json(silent=True)
    if json_data: data.update(json_data)
    
    # 2. البحث في Form (بيانات النموذج)
    if request.form: data.update(request.form.to_dict())
    
    # 3. البحث في الروابط (URL Args)
    if request.args: data.update(request.args.to_dict())

    # 4. استخراج الحقول بكل المسميات الممكنة (Mapping)
    # حقل الفكرة (المربع العلوي)
    idea = data.get("idea") or data.get("topic") or data.get("content") or ""
    # حقل المنشور المرجعي (المربع السفلي)
    seed = data.get("seed") or data.get("reference") or data.get("winning_post") or ""
    # حقل الأسلوب والنيش
    style = data.get("style") or "Professional"
    niche = data.get("niche") or ""

    # طباعة في سجلات Render للتحقق (Debug)
    print(f"[DEBUG] Incoming Payload: {data}", file=sys.stderr)
    
    return str(idea).strip(), str(seed).strip(), str(style).strip(), str(niche).strip()

# ========= المسارات التلقائية =========

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/generate/<platform>", methods=["POST", "GET"])
def handle_generation(platform):
    # استخراج البيانات مهما كان مصدرها
    idea, seed, style, niche = extract_universal_data()

    # محاولة توحيد المدخلات إذا كان أحدهما فارغاً
    target_content = idea if idea else seed
    
    if not target_content:
        # إذا كان كل شيء فارغاً حقاً، نرجع الخطأ 400 مع شرح
        return jsonify({"error": "فشل: لم تصل أي بيانات للسيرفر. تأكد من الكتابة في الصناديق."}), 400

    try:
        # تشغيل الدماغ بمنطق الاندماج الفائق (Fusion)
        brain = strategic_intelligence_core(idea=idea, platform=platform, style=style, reference_post=seed)
        
        # بناء الأمر النهائي
        final_prompt = f"""
        {WPIL_DOMINATOR_SYSTEM}
        المهمة الاستراتيجية: {brain['transformed_input']}
        المنصة المستهدفة: {platform}
        الأسلوب: {style}
        """
        
        generated_text = get_ai_response(final_prompt)

        return jsonify({
            "platform": platform,
            "text": generated_text,
            "trace": brain["logic_trace"],
            "video_prompt": brain.get("visual_prompt", "") if platform == "tiktok" else ""
        }), 200

    except Exception as e:
        return jsonify({"error": f"Internal Crash: {str(e)}"}), 500

@app.route("/remix", methods=["POST", "GET"])
def handle_remix():
    # توحيد الريمكس مع المحرك الرئيسي لضمان القوة
    return handle_generation("linkedin")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
