from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os
import google.generativeai as genai

# استيراد المكونات المحدثة
from dominator_brain import strategic_intelligence_core, WPIL_DOMINATOR_SYSTEM

app = Flask(__name__, template_folder="templates", static_folder="static")
CORS(app)

# ========= الإعدادات الذكية =========
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")

if not GEMINI_API_KEY:
    print("CRITICAL: MISSING API KEY")
else:
    genai.configure(api_key=GEMINI_API_KEY)

def get_ai_response(prompt: str) -> str:
    """استدعاء المحرك مع معالجة الأخطاء"""
    try:
        model = genai.GenerativeModel(GEMINI_MODEL)
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"System Error: {str(e)}"

# ========= المسارات (Endpoints) =========

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "online", "system": "AI DOMINATOR V2"}), 200

@app.route("/generate/<platform>", methods=["POST", "GET"])
@app.route("/generate/linkedin", methods=["POST", "GET"])
@app.route("/generate/twitter", methods=["POST", "GET"])
@app.route("/generate/tiktok", methods=["POST", "GET"])
def handle_generation(platform=None):
    # إذا نسي النظام تمرير المنصة من الرابط، نحاول استنتاجها
    target_platform = platform or request.path.split('/')[-1] or "linkedin"
    
    if request.method == "GET":
        return jsonify({"error": "Method not allowed. Use POST"}), 405

    # دالة صائد البيانات الجريئة
    data = request.get_json(silent=True) or {}
    idea = (data.get("idea") or data.get("text") or data.get("content") or "").strip()
    style = data.get("style", "professional").strip()

    if not idea:
        return jsonify({"error": "فشل التشغيل: الفكرة مطلوبة للبدء"}), 400

    try:
        # 1. المعالجة عبر الدماغ (SIC)
        brain = strategic_intelligence_core(idea=idea, platform=target_platform, style=style)
        
        # 2. توليد المحتوى النهائي
        prompt = f"""
        {WPIL_DOMINATOR_SYSTEM}
        
        Platform: {brain['primary_platform']}
        Style Context: {style}
        Strategic Input: {brain['transformed_input']}
        
        المطلوب: توليد منشور كامل، احترافي، وجاهز للنشر فوراً بالعربية.
        """
        
        final_text = get_ai_response(prompt)

        # 3. تجهيز الرد
        response_payload = {
            "platform": brain['primary_platform'],
            "text": final_text,
            "trace": brain['logic_trace']
        }

        # ميزة إضافية للـ TikTok
        if brain['primary_platform'] == "tiktok":
            response_payload["video_prompt"] = get_ai_response(f"Create a 1-sentence cinematic AI video prompt for this: {final_text}")

        return jsonify(response_payload), 200

    except Exception as e:
        return jsonify({"error": f"Internal Crash: {str(e)}"}), 500

@app.route("/remix", methods=["POST"])
def remix():
    data = request.get_json(silent=True) or {}
    niche = data.get("niche", "General")
    seed = data.get("seed", "")
    
    if not seed: return jsonify({"error": "Seed missing"}), 400

    prompt = f"{WPIL_DOMINATOR_SYSTEM}\nRemix this idea for the ({niche}) niche in Arabic: {seed}"
    return jsonify({"text": get_ai_response(prompt)}), 200

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
