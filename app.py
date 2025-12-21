from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os
import google.generativeai as genai
from dominator_brain import strategic_intelligence_core, WPIL_DOMINATOR_SYSTEM

app = Flask(__name__, template_folder="templates", static_folder="static")
CORS(app)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

def get_ai_response(prompt: str) -> str:
    try:
        model = genai.GenerativeModel("gemini-2.0-flash")
        return model.generate_content(prompt).text
    except Exception as e:
        return f"Error: {str(e)}"

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/generate/<platform>", methods=["POST"])
def generate_content(platform):
    data = request.get_json(silent=True) or {}
    
    # سحب البيانات من "كل" المصادر الممكنة في الواجهة
    idea = data.get("idea", "").strip()
    seed = data.get("seed", "").strip() # المنشور المرجعي من Winning Posts
    style = data.get("style", "Professional").strip()

    # ضمان عدم الانهيار: إذا كانت الفكرة فارغة، نستخدم المنشور المرجعي كفكرة
    actual_idea = idea if idea else seed
    
    if not actual_idea:
        return jsonify({"error": "يرجى إدخال فكرة أو منشور مرجعي للبدء"}), 400

    # 1. تشغيل الدماغ بمنطق الاندماج
    brain = strategic_intelligence_core(idea=idea, platform=platform, style=style, reference_post=seed)
    
    # 2. بناء الأمر النهائي للـ AI
    final_prompt = f"""
    {WPIL_DOMINATOR_SYSTEM}
    المهمة: {brain['transformed_input']}
    المنصة: {platform}
    الأسلوب: {style}
    
    المطلوب: توليد محتوى مهيمن وقوي جداً باللغة العربية.
    """
    
    generated_text = get_ai_response(final_prompt)

    payload = {
        "platform": platform,
        "text": generated_text,
        "trace": brain["logic_trace"]
    }

    if platform == "tiktok":
        payload["video_prompt"] = brain["visual_prompt"]

    return jsonify(payload), 200

# مسار الـ Remix للإبقاء على التوافق مع الأزرار القديمة
@app.route("/remix", methods=["POST"])
def remix():
    return generate_content("linkedin") # تحويله تلقائياً للمسار الشامل

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
