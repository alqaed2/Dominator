import os
import sys
import json
import logging
import time
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import google.generativeai as genai

# استيراد الدماغ الاستراتيجي المطور (v4.0)
from dominator_brain import strategic_intelligence_core, WPIL_DOMINATOR_SYSTEM

# إعداد التطبيق والسجلات
app = Flask(__name__, template_folder="templates", static_folder="static")
CORS(app)
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger(__name__)

# ========= إعداد محركات AI (بروتوكول الاستقرار 2025) =========
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

# مصفوفة الهيمنة المحدثة لضمان أعلى Quota متاح
MODELS_PRIORITY = [
    "gemini-2.0-flash-lite",   # الأعلى استقراراً في عدد الطلبات
    "gemini-flash-latest",     # الموديل المستقر (1.5 Flash)
    "gemini-2.0-flash",       # توازن ذكاء عالي
    "gemini-2.5-flash-lite",  # موديل القمة (نسخة لايت)
    "gemini-2.5-flash"        # موديل القمة (نسخة برو)
]

def get_ai_response_with_failover(prompt: str) -> str:
    last_error = ""
    for model_name in MODELS_PRIORITY:
        try:
            logger.info(f"🚀 Deploying Brain on: {model_name}")
            model = genai.GenerativeModel(model_name)
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            last_error = str(e)
            logger.warning(f"⚠️ Model {model_name} rate limited or unavailable.")
            if "429" in last_error or "Quota" in last_error or "404" in last_error:
                continue
            return f"Strategic Engine Error: {last_error}"
    return f"⚠️ جميع الشبكات العصبية مشغولة حالياً. يرجى الانتظار 30 ثانية والمحاولة مجدداً."

# ========= مستخرج البيانات المطابق لـ index.html =========
def extract_ui_data():
    """هذه الدالة تطابق تماماً مسميات JavaScript في ملف index.html الخاص بك"""
    data = {}
    try:
        data = request.get_json(force=True, silent=True) or {}
    except: data = {}
    
    if request.form: data.update(request.form.to_dict())

    # المطابقة مع مسميات JavaScript: 'text' للفكرة و 'winning_post' للريمكس
    idea = data.get('text') or data.get('idea') or data.get('topic') or ""
    seed = data.get('winning_post') or data.get('seed') or ""
    style = data.get('style_dna') or data.get('style') or "Professional"
    
    return str(idea).strip(), str(seed).strip(), str(style).strip()

# ========= المسارات الاستراتيجية المهيمنة =========

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/health")
def health():
    return jsonify({"status": "active", "version": "4.0.0"}), 200

@app.route("/generate/<platform>", methods=["POST", "GET"])
@app.route("/remix", methods=["POST", "GET"])
def handle_execution(platform="linkedin"):
    if request.method == "GET":
        return jsonify({"status": "ready"}), 200

    if request.path == "/remix": platform = "linkedin"

    # 1. استخراج البيانات بالبروتوكول الشامل
    idea, seed, style = extract_ui_data()
    actual_content = idea if idea else seed
    
    if not actual_content:
        return jsonify({"error": "يرجى إدخال مادة خام للعمل عليها"}), 400

    try:
        # 2. تشغيل الدماغ الاستراتيجي (v4.0 Vertical Optimized)
        brain = strategic_intelligence_core(idea, platform, style, seed)
        
        # 3. بناء الميثاق وتوليد النتائج
        final_prompt = f"{WPIL_DOMINATOR_SYSTEM}\nالمنصة: {platform}\nالمهمة: {brain['transformed_input']}\nالأسلوب: {style}"
        generated_text = get_ai_response_with_failover(final_prompt)

        # دمج البصمة الفيروسية
        final_output = f"{generated_text}{brain.get('viral
