import os
import sys
import re
import time
import requests
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import google.generativeai as genai

# استيراد النواة السيادية
from dominator_brain import strategic_intelligence_core, alchemy_fusion_core, WPIL_DOMINATOR_SYSTEM

app = Flask(__name__, template_folder="templates", static_folder="static")
CORS(app)

# ========= ترسانة موديلات 2025 - حماية Nebula الموحدة =========
MODELS_POOL = [
    "gemini-2.5-flash",
    "gemini-2.5-flash-lite",
    "gemini-2.0-flash-lite-001",
    "gemini-flash-latest",
    "gemini-pro-latest"
]

GENAI_KEY = os.getenv("GEMINI_API_KEY")
APIFY_KEY = os.getenv("APIFY_API_KEY")

if GENAI_KEY:
    genai.configure(api_key=GENAI_KEY)

def get_ai_response_nebula(prompt: str) -> str:
    """بروتوكول Nebula: التبديل التلقائي القسري لضمان استمرارية التوليد"""
    for model_name in MODELS_POOL:
        try:
            model = genai.GenerativeModel(model_name)
            response = model.generate_content(prompt)
            return response.text
        except Exception:
            continue
    return "[CRITICAL ERROR] كافة المحركات مشغولة حالياً."

def fetch_live_market_dna(niche):
    """الربط الحي مع Apify لسحب ترندات X (Twitter) الحقيقية لحظياً"""
    if not APIFY_KEY:
        return get_fallback_dna(niche)

    try:
        # تشغيل Actor السحب الحي (Tweet Scraper)
        # هذا الـ Actor يجلب التغريدات الأعلى تفاعلاً في هذه اللحظة للنيش المطلوب
        actor_url = f"https://api.apify.com/v2/acts/apidojo~tweet-scraper/run-sync-get-dataset-items?token={APIFY_KEY}"
        payload = {
            "searchTerms": [niche],
            "maxTweets": 5,
            "searchMode": "top",
            "lang": "ar"
        }
        
        # مهلة انتظار قسرية (Timeout) لضمان عدم تجمد النظام
        res = requests.post(actor_url, json=payload, timeout=25)
        
        if res.status_code in [200, 201]:
            data = res.json()
            if data and len(data) > 0:
                return [
                    {
                        "text": i.get("full_text") or i.get("text", "DNA Fragment"),
                        "engagement": f"{int(i.get('favorite_count', 0)) + int(i.get('retweet_count', 0))}",
                        "score": 85 + (int(i.get('favorite_count', 0)) % 15)
                    } for i in data if (i.get("full_text") or i.get("text"))
                ]
        return get_fallback_dna(niche)
    except Exception:
        return get_fallback_dna(niche)

def get_fallback_dna(niche):
    """نظام الحصانة: توليد جينات ذكية في حال تعذر الاتصال بالرادار الخارجي"""
    return [
        {"text": f"المعادلة الاستراتيجية للاكتساح في {niche} لعام 2026", "engagement": "140K+", "score": 98},
        {"text": f"لماذا تفشل 99% من محاولات السيطرة على {niche}؟ التحليل الكامل", "engagement": "85K+", "score": 92}
    ]

def parse_unified_output(raw_text: str) -> dict:
    """تفكيك المخرجات الموحدة لضمان عمل التبويبات بنسبة 100%"""
    parts = {"linkedin": "فشل التفكيك", "twitter": "فشل التفكيك", "tiktok": "فشل التفكيك"}
    patterns = {
        "linkedin": r"\[LINKEDIN\](.*?)(\[TWITTER\]|\[TIKTOK\]|$)",
        "twitter": r"\[TWITTER\](.*?)(\[LINKEDIN\]|\[TIKTOK\]|$)",
        "tiktok": r"\[TIKTOK\](.*?)(\[LINKEDIN\]|\[TWITTER\]|$)"
    }
    for p, pattern in patterns.items():
        match = re.search(pattern, raw_text, re.S | re.I)
        if match: parts[p] = match.group(1).strip()
    return parts

@app.route("/")
def home(): return render_template("index.html")

@app.route("/alchemy/discover", methods=["POST"])
def discover():
    data = request.get_json(silent=True) or {}
    niche = data.get("niche", "القيادة")
    
    # 1. سحب النبض الحي من الإنترنت
    gold_posts = fetch_live_market_dna(niche)
    
    # 2. تشغيل مفاعل الاندماج (Synthesis)
    fusion = alchemy_fusion_core(gold_posts, niche)
    
    # 3. تخليق المنشور الخارق عبر Nebula
    output = get_ai_response_nebula(f"{WPIL_DOMINATOR_SYSTEM}\nالمهمة: ادمج هذه الجينات الحية وصغ مرسوماً خارقاً لنيش {niche}:\n{fusion['synthesis_task']}")
    
    return jsonify({
        "super_post": output,
        "sources": gold_posts,
        "trace": fusion["logic_trace"]
    }), 200

@app.route("/generate_all", methods=["POST"])
def generate_all():
    data = request.get_json(silent=True) or {}
    idea = data.get('text') or "الهيمنة السوقية"
    
    prompt = f"""
    {WPIL_DOMINATOR_SYSTEM}
    المهمة: توليد 3 نسخ محتوى لهذه الفكرة: {idea}
    يجب تقسيم الرد بالعلامات الصارمة: [LINKEDIN], [TWITTER], [TIKTOK].
    اجعل المخرجات قمة في الفخامة والاستراتيجية.
    """
    
    raw_output = get_ai_response_nebula(prompt)
    parsed = parse_unified_output(raw_output)
    brain = strategic_intelligence_core(idea)
    
    return jsonify({
        "linkedin": parsed["linkedin"],
        "twitter": parsed["twitter"],
        "tiktok": parsed["tiktok"],
        "video_prompt": brain["video_segments"],
        "trace": brain["logic_trace"]
    }), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
