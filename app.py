import os
import json
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import google.generativeai as genai
from dominator_brain import strategic_intelligence_core, WPIL_DOMINATOR_SYSTEM

app = Flask(__name__, template_folder="templates", static_folder="static")
CORS(app)

# إعداد AI
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def get_ai_response(prompt: str) -> str:
    try:
        model = genai.GenerativeModel("gemini-2.0-flash")
        return model.generate_content(prompt).text
    except Exception as e:
        return f"AI Error: {str(e)}"

# ========= مستخرج البيانات العبقري (The Omni-Scanner) =========
def extract_data():
    """يبحث في كل ثقب في الطلب (Request) عن البيانات"""
    data = {}
    
    # 1. محاولة قراءة JSON (حتى لو كان Content-Type خاطئاً)
    try:
        data = request.get_json(force=True, silent=True) or {}
    except:
        data = {}

    # 2. دمج بيانات النماذج (Form Data)
    if request.form:
        data.update(request.form.to_dict())

    # 3. دمج بيانات الروابط (Query Args)
    if request.args:
        data.update(request.args.to_dict())

    # 4. البحث في البيانات الخام (Raw Body) إذا كان كل ما سبق فارغاً
    if not data and request.data:
        try:
            raw_json = json.loads(request.data)
            data.update(raw_json)
        except:
            pass

    # الخرائط الذهنية للمسميات (Mapping)
    # الواجهة قد ترسل 'topic' أو 'idea' أو 'content'
    idea = data.get("idea") or data.get("topic") or data.get("content") or ""
    # الواجهة قد ترسل 'seed' أو 'winning_post' أو 'reference'
    seed = data.get("seed") or data.get("winning_post") or data.get("reference") or ""
    # الأسلوب والنيش
    style = data.get("style") or "Professional"
    niche = data.get("niche") or ""

    return str(idea).strip(), str(seed).strip(), str(style).strip(), str(niche).strip()

# ========= المسارات المهيمنة =========

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/generate/<platform>", methods=["POST", "GET"])
@app.route("/remix", methods=["POST", "GET"])
def execute(platform="linkedin"):
    # إذا تم استدعاء /remix نعتبر المنصة افتراضياً LinkedIn
    if request.path == "/remix":
        platform = "linkedin"

    idea, seed, style, niche = extract_data()

    # محاولة الإنقاذ: إذا كان أحد الحقلين ممتلئاً، نعتبره هو المحتوى الأساسي
    actual_input = idea if idea else seed
    
    if not actual_input:
        return jsonify({
            "error": "فشل التشغيل: لم تصل أي بيانات للسيرفر. تأكد من الكتابة في الصناديق.",
            "debug_received_keys": list(request.form.keys()) if request.form else "None"
        }), 400

    try:
        # 1. تشغيل الدماغ (SIC)
        brain = strategic_intelligence_core(idea, platform, style, seed)
        
        # 2. توليد المحتوى
        final_prompt = f"{WPIL_DOMINATOR_SYSTEM}\nالمهمة: {brain['transformed_input']}\nالمنصة: {platform}\nالأسلوب: {style}"
        text = get_ai_response(final_prompt)

        return jsonify({
            "platform": platform,
            "text": text,
            "trace": brain["logic_trace"],
            "video_prompt": brain.get("visual_prompt") if platform == "tiktok" else "",
            "niche": niche
        }), 200

    except Exception as e:
        return jsonify({"error": f"Internal Server Crash: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
