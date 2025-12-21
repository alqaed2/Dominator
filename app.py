import os
import json
import logging
import sys
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import google.generativeai as genai
from dominator_brain import strategic_intelligence_core, WPIL_DOMINATOR_SYSTEM

# إعداد السجلات لرؤية الحقيقة في Render Logs
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__, template_folder="templates", static_folder="static")
CORS(app)

# إعداد AI مع نظام التبديل التلقائي (Failover)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

MODELS = ["gemini-2.0-flash", "gemini-1.5-flash", "gemini-flash-latest"]

def get_ai_response(prompt):
    for model_name in MODELS:
        try:
            logger.info(f"Using Model: {model_name}")
            model = genai.GenerativeModel(model_name)
            return model.generate_content(prompt).text
        except Exception as e:
            logger.error(f"Model {model_name} failed: {e}")
            continue
    return "Error: All AI engines are currently unavailable."

# ========= الرادار الشامل لاستقبال البيانات (The Omni-Ingestor) =========
def extract_data_from_anywhere():
    """
    يستخرج البيانات حتى لو أرسلتها الواجهة بشكل خاطئ تماماً.
    """
    final_payload = {}
    
    # 1. محاولة JSON
    try:
        json_data = request.get_json(force=True, silent=True)
        if json_data: final_payload.update(json_data)
    except: pass
    
    # 2. محاولة Form Data
    if request.form: final_payload.update(request.form.to_dict())
    
    # 3. محاولة Query Args
    if request.args: final_payload.update(request.args.to_dict())
    
    # 4. محاولة البيانات الخام (Raw Body) - إذا أرسلها المتصفح كنص عادي
    raw_body = request.get_data(as_text=True)
    if raw_body and not final_payload:
        try:
            final_payload.update(json.loads(raw_body))
        except:
            final_payload['idea'] = raw_body # اعتباره فكرة مباشرة

    # طباعة البيانات المستلمة في Logs للتشخيص
    logger.debug(f"RECEIVED DATA: {final_payload}")

    # توحيد المسميات (Mapping)
    idea = final_payload.get('idea') or final_payload.get('topic') or final_payload.get('content') or ""
    seed = final_payload.get('seed') or final_payload.get('winning_post') or final_payload.get('reference') or ""
    style = final_payload.get('style') or "Professional"
    
    return str(idea).strip(), str(seed).strip(), str(style).strip()

# ========= المسارات المهيمنة =========

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/generate/<platform>", methods=["POST", "GET"])
@app.route("/remix", methods=["POST", "GET"])
def handle_request(platform="linkedin"):
    if request.path == "/remix": platform = "linkedin"
    
    idea, seed, style = extract_data_from_anywhere()
    
    # الفحص النهائي قبل الرفض
    if not idea and not seed:
        logger.error("400 Error: No text found in any part of the request.")
        return jsonify({
            "error": "السيرفر لم يجد أي نصوص. تأكد أن الواجهة ترسل البيانات بشكل صحيح.",
            "debug_keys": list(request.form.keys()) if request.form else "None"
        }), 400

    try:
        brain = strategic_intelligence_core(idea, platform, style, seed)
        prompt = f"{WPIL_DOMINATOR_SYSTEM}\nالمنصة: {platform}\nالمهمة: {brain['transformed_input']}\nالأسلوب: {style}"
        
        output = get_ai_response(prompt)
        
        return jsonify({
            "text": output,
            "platform": platform,
            "trace": brain["logic_trace"],
            "video_prompt": brain.get("visual_prompt") if platform == "tiktok" else ""
        }), 200
    except Exception as e:
        return jsonify({"error": f"Internal Crash: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
