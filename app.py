from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os
import google.generativeai as genai
from dominator_brain import strategic_intelligence_core, WPIL_DOMINATOR_SYSTEM

app = Flask(__name__, template_folder="templates", static_folder="static")
CORS(app)

# ========= الإعدادات =========
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

def get_ai_response(prompt: str) -> str:
    try:
        model = genai.GenerativeModel(GEMINI_MODEL)
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

# ========= المسارات المصلحة =========

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/remix", methods=["POST"])
def remix():
    data = request.get_json(silent=True) or {}
    niche = data.get("niche", "Business Strategy")
    seed = data.get("seed", "").strip()
    
    # إذا كان الـ Seed مفقوداً، نقوم بصناعة فكرة رابحة تلقائياً بناءً على النيش
    if not seed:
        seed = f"أفضل طريقة للسيطرة على سوق الـ {niche} في 2025"
        trace_msg = "MODE: WINNING POSTS REMIX | STATUS: SEED AUTO-GENERATED"
    else:
        trace_msg = "MODE: WINNING POSTS REMIX | STATUS: SUCCESS"

    prompt = f"{WPIL_DOMINATOR_SYSTEM}\nTask: Remix this idea into a viral high-authority post.\nNiche: {niche}\nSeed: {seed}"
    result = get_ai_response(prompt)
    
    return jsonify({
        "text": result, 
        "trace": trace_msg
    }), 200

@app.route("/generate/<platform>", methods=["POST"])
def generate_content(platform):
    data = request.get_json(silent=True) or {}
    idea = data.get("idea", "").strip()
    style = data.get("style", "cinematic").strip()

    if not idea:
        return jsonify({"error": "Idea missing"}), 400

    # 1. تشغيل الدماغ
    brain = strategic_intelligence_core(idea, platform, style)
    
    # 2. توليد المحتوى النصي
    final_prompt = f"{WPIL_DOMINATOR_SYSTEM}\nGenerate {platform} content for: {brain['transformed_input']}\nStyle: {style}"
    generated_text = get_ai_response(final_prompt)

    # 3. بناء البايلود
    payload = {
        "platform": platform,
        "text": generated_text,
        "trace": brain["logic_trace"]
    }

    # تخصيص تيك توك ببرومبت فخم جداً
    if platform == "tiktok":
        payload["video_prompt"] = brain["visual_prompt"]
        payload["script_details"] = "Luxury Cinematic Style - Supreme Advisor Character"

    return jsonify(payload), 200

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
