from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import os
import json
from typing import Any, Dict

# SIC
from dominator_brain import strategic_intelligence_core

# Memory
from sic_memory import record_success, record_failure

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WPIL_PATTERNS_FILE = os.path.join(BASE_DIR, "wpil_patterns.json")

app = Flask(__name__)

# ----------------------------
# Environment
# ----------------------------
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
GEMINI_MODEL = os.environ.get("GEMINI_MODEL", "gemini-1.5-flash")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY missing")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel(GEMINI_MODEL)


# ----------------------------
# Utilities
# ----------------------------
def _read_patterns() -> Any:
    if not os.path.exists(WPIL_PATTERNS_FILE):
        with open(WPIL_PATTERNS_FILE, "w", encoding="utf-8") as f:
            json.dump([], f, ensure_ascii=False, indent=2)
        return []
    try:
        with open(WPIL_PATTERNS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []


def _write_patterns(data: Any) -> None:
    try:
        with open(WPIL_PATTERNS_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception:
        pass


def _build_prompt(sic: Dict[str, Any], user_style_text: str = "") -> str:
    """
    يبني Prompt نهائي للموديل بالاعتماد على:
    - SIC transformed_input
    - WPIL constraints
    - platform + content_mode
    """
    mode = sic.get("mode", "DIRECT")
    platform = sic.get("primary_platform", "linkedin")
    content_mode = sic.get("content_mode", "post")
    style = sic.get("style_override", "Professional")
    rules = sic.get("rules", {})
    wpil_trace = sic.get("wpil_trace", {}) or {}
    constraints = (wpil_trace.get("constraints") or {})

    hook_type = rules.get("hook_type", "bold_claim")
    hook_max_words = rules.get("hook_max_words", 12)
    cta_type = rules.get("cta_type", "curiosity")
    cta_position = rules.get("cta_position", "end")

    extra_style = user_style_text.strip()

    return f"""
أنت كاتب محتوى عربي محترف متخصص في صناعة منشورات تنتشر.
هدفك: إنتاج محتوى عالي الجاذبية دون نسخ حرفي أو اقتباس مباشر.

# OUTPUT TARGET
- platform: {platform}
- content_mode: {content_mode}
- mode: {mode}

# STYLE DNA
- default_style: {style}
- user_style_sample (if any): {extra_style}

# WPIL CONSTRAINTS (NON-NEGOTIABLE)
- hook.type = {hook_type}
- hook.max_words = {hook_max_words}
- cta.type = {cta_type}
- cta.position = {cta_position}
- structure = {constraints.get("structure", {})}

# HARD RULES
- لا نسخ حرفي إطلاقًا.
- إذا كان mode = WINNING_POSTS_REMIX: أعد هندسة الفكرة والهيكل لتبدو جديدة 100% مع نفس القوة البنيوية.
- اكتب عربي طبيعي، سهل القراءة، بفواصل وأسطر قصيرة عند الحاجة.
- اختم بنداء فعل قوي مناسب.

# INPUT (SIC TRANSFORMED)
{sic.get("transformed_input","")}
""".strip()


# ----------------------------
# Pages
# ----------------------------
@app.get("/")
def home():
    return render_template("index.html")


# ----------------------------
# Core Generate
# ----------------------------
@app.post("/generate")
def generate():
    """
    مولد موحد:
    - Direct: raw_text
    - Remix: winning_post
    """
    try:
        payload = request.get_json(force=True) or {}

        raw_text = (payload.get("raw_text") or payload.get("text") or "").strip()
        winning_post = (payload.get("winning_post") or "").strip()

        platform = (payload.get("platform") or "linkedin").lower()
        niche = (payload.get("niche") or "general").lower()
        intent = (payload.get("intent") or "educational").lower()

        style_text = (payload.get("style_text") or "").strip()

        remix = bool(payload.get("remix")) or bool(winning_post)

        sic = strategic_intelligence_core({
            "remix": remix,
            "platform": platform,
            "niche": niche,
            "intent": intent,
            "content_signal": {
                "raw_text": raw_text,
                "winning_post": winning_post,
                "platform": platform,
                "niche": niche,
                "intent": intent
            },
            "style_signal": {
                "style_dna": payload.get("style_dna", "Professional")
            },
            "context_signal": {
                "platforms_available": ["linkedin", "twitter", "tiktok"],
                "platform": platform,
                "niche": niche,
                "intent": intent
            }
        })

        prompt = _build_prompt(sic, user_style_text=style_text)
        resp = model.generate_content(prompt)
        out_text = (resp.text or "").strip()

        record_success(sic.get("primary_platform", platform), {"mode": sic.get("mode")})

        return jsonify({
            "ok": True,
            "mode": sic.get("mode", "DIRECT"),
            "primary_platform": sic.get("primary_platform"),
            "secondary_platforms": sic.get("secondary_platforms", []),
            "content_mode": sic.get("content_mode"),
            "rules": sic.get("rules", {}),
            "wpil_trace": sic.get("wpil_trace", {}),
            "output": out_text
        })

    except Exception as e:
        record_failure("unknown", str(e))
        return jsonify({"ok": False, "error": str(e)}), 500


# ----------------------------
# WPIL Remix Routes (Fix 404)
# ----------------------------
def _remix_handler():
    """
    Handler واحد + عدة Routes لتفادي اختلاف اسم endpoint في الواجهة.
    """
    payload = request.get_json(force=True) or {}
    winning_post = (payload.get("winning_post") or payload.get("text") or "").strip()
    if not winning_post:
        return jsonify({"ok": False, "error": "winning_post missing"}), 400

    platform = (payload.get("platform") or "linkedin").lower()
    niche = (payload.get("niche") or "general").lower()
    intent = (payload.get("intent") or "educational").lower()
    style_text = (payload.get("style_text") or "").strip()

    sic = strategic_intelligence_core({
        "remix": True,
        "platform": platform,
        "niche": niche,
        "intent": intent,
        "content_signal": {
            "winning_post": winning_post,
            "platform": platform,
            "niche": niche,
            "intent": intent
        },
        "style_signal": {
            "style_dna": payload.get("style_dna", "Professional")
        },
        "context_signal": {
            "platforms_available": ["linkedin", "twitter", "tiktok"],
            "platform": platform,
            "niche": niche,
            "intent": intent
        }
    })

    prompt = _build_prompt(sic, user_style_text=style_text)
    resp = model.generate_content(prompt)
    out_text = (resp.text or "").strip()

    return jsonify({
        "ok": True,
        "mode": sic.get("mode", "WINNING_POSTS_REMIX"),
        "primary_platform": sic.get("primary_platform"),
        "content_mode": sic.get("content_mode"),
        "rules": sic.get("rules", {}),
        "wpil_trace": sic.get("wpil_trace", {}),
        "output": out_text
    })


@app.post("/wpil/remix")
def wpil_remix():
    return _remix_handler()

@app.post("/api/wpil/remix")
def api_wpil_remix():
    return _remix_handler()

@app.post("/remix")
def remix_alias():
    return _remix_handler()

@app.post("/winning-posts/remix")
def remix_alias2():
    return _remix_handler()


# ----------------------------
# WPIL Ingest (Optional)
# ----------------------------
def _ingest_handler():
    """
    إدخال بيانات Winning Posts للتجارب:
    يقبل:
      { "posts": ["text1","text2", ...] }
    أو:
      { "posts": [ { "text": "...", "platform":"x", "niche":"..." }, ... ] }
    """
    payload = request.get_json(force=True) or {}
    posts = payload.get("posts", [])
    if not isinstance(posts, list) or len(posts) == 0:
        return jsonify({"ok": False, "error": "posts must be a non-empty list"}), 400

    existing = _read_patterns()
    if not isinstance(existing, list):
        existing = []

    # خزّنها كبساطة (التحليل البنيوي المتقدم لاحقاً)
    for p in posts:
        if isinstance(p, str):
            existing.append({"text": p})
        elif isinstance(p, dict) and p.get("text"):
            existing.append({
                "text": p.get("text", ""),
                "platform": (p.get("platform") or "").lower(),
                "niche": (p.get("niche") or "").lower(),
                "meta": p.get("meta", {})
            })

    _write_patterns(existing)

    return jsonify({"ok": True, "count": len(existing)})


@app.post("/wpil/ingest")
def wpil_ingest():
    return _ingest_handler()

@app.post("/api/wpil/ingest")
def api_wpil_ingest():
    return _ingest_handler()


@app.get("/wpil/health")
def wpil_health():
    patterns = _read_patterns()
    return jsonify({"ok": True, "patterns_count": len(patterns) if isinstance(patterns, list) else 0})
