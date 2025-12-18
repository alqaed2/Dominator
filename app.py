from flask import Flask, render_template, request, jsonify
import os
import re
import json
from typing import Dict, Any

import google.generativeai as genai

from dominator_brain import strategic_intelligence_core
from sic_memory import record_success, record_failure

# WPIL runtime (إن لم يكن موجودًا لن نكسر التشغيل)
try:
    from wpil_runtime import invoke_wpil
except Exception:
    invoke_wpil = None


app = Flask(__name__)

# ----------------------------
# Gemini Config
# ----------------------------
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
GEMINI_MODEL = os.environ.get("GEMINI_MODEL")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY missing")
if not GEMINI_MODEL:
    raise ValueError("GEMINI_MODEL missing")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel(GEMINI_MODEL)

# آخر تتبع WPIL (لعرضه في الواجهة)
_LAST_WPIL_TRACE: Dict[str, Any] = {
    "mode": "direct",
    "niche": None,
    "platform": None,
    "applied": False,
    "constraints": {},
    "notes": "No runs yet"
}


@app.get("/")
def home():
    return render_template("index.html")


@app.get("/health")
def health():
    return jsonify({"ok": True})


# ============================
# WPIL Trace Endpoint (Fix 404)
# ============================
@app.get("/wpil/trace")
def wpil_trace():
    return jsonify(_LAST_WPIL_TRACE)


# ============================
# Helpers
# ============================
def _safe_json() -> Dict[str, Any]:
    try:
        return request.get_json(force=True) or {}
    except Exception:
        return {}


def _extract_image_prompt(text: str) -> str:
    """
    لو رجع الموديل سطر IMAGE: ... نلتقطه.
    """
    if not text:
        return ""
    m = re.search(r"(?:IMAGE_PROMPT|IMAGE)\s*:\s*(.+)", text, re.IGNORECASE)
    return (m.group(1).strip() if m else "")


def _clean_model_text(text: str) -> str:
    if not text:
        return ""
    # نحذف سطر image prompt من العرض إن وجد
    text = re.sub(r"(?:IMAGE_PROMPT|IMAGE)\s*:\s*.+", "", text, flags=re.IGNORECASE).strip()
    return text


def _call_gemini(prompt: str) -> str:
    resp = model.generate_content(prompt)
    # مكتبة google-generativeai غالبًا توفر resp.text
    out = getattr(resp, "text", None)
    return out if out else str(resp)


def _build_wpil(platform: str, niche: str, winning_post: str, topic: str) -> Dict[str, Any]:
    """
    WPIL لا يقيّم ولا يرفض.
    فقط يطلع قيود Winning Constraints.
    """
    global _LAST_WPIL_TRACE

    if not invoke_wpil:
        _LAST_WPIL_TRACE = {
            "mode": "direct",
            "niche": niche,
            "platform": platform,
            "applied": False,
            "constraints": {},
            "notes": "WPIL runtime not available"
        }
        return {"constraints": {}, "mode": "direct"}

    content_signal = {
        "platform": platform,
        "niche": niche,
        "intent": "authority",
        "topic": topic,
        "winning_post": winning_post
    }

    result = invoke_wpil(content_signal) or {}
    constraints = result.get("constraints", {}) or {}
    mode = result.get("mode", "direct")

    _LAST_WPIL_TRACE = {
        "mode": mode,
        "niche": niche,
        "platform": platform,
        "applied": bool(constraints),
        "constraints": constraints,
        "notes": result.get("notes", "ok")
    }

    return {"constraints": constraints, "mode": mode}


def _prompt_for(platform: str, topic: str, style_dna: str, image_style: str, wpil_constraints: Dict[str, Any], winning_post: str) -> str:
    """
    Prompt واحد “حاكم” يضمن:
    - عربي
    - مخرجات منصة محددة
    - WPIL (قيود بنيوية) إن وجدت
    - Remix لو Winning Post موجود
    """
    wpil_block = ""
    if wpil_constraints:
        wpil_block = f"""
[WPIL_CONSTRAINTS - بنيوية فقط]
{json.dumps(wpil_constraints, ensure_ascii=False)}
"""

    remix_block = ""
    if winning_post and len(winning_post.strip()) > 20:
        remix_block = f"""
[WINNING_POST_INPUT]
{winning_post.strip()}

[INSTRUCTION]
أعد كتابة المنشور أعلاه (Remix) ليبدو جديدًا 100% بدون نسخ حرفي.
حافظ فقط على "الفكرة البنيوية" (Hook/Structure/CTA) ولا تنقل نفس الجُمل.
"""

    if platform == "linkedin":
        format_block = """
[OUTPUT FORMAT - LINKEDIN]
- Hook قوي في أول سطر (جملة واحدة)
- فقرات قصيرة + أسطر منفصلة
- قيمة عملية واضحة
- CTA في النهاية (سؤال أو دعوة للتعليق)
- الطول: 120 إلى 220 كلمة تقريبًا
"""
    elif platform == "twitter":
        format_block = """
[OUTPUT FORMAT - X/TWITTER THREAD]
- اكتب Thread من 5 إلى 7 تغريدات
- كل تغريدة سطرين إلى 4 أسطر كحد أقصى
- ابدأ بـ Hook قوي
- اختم CTA واضح
"""
    else:  # tiktok
        format_block = """
[OUTPUT FORMAT - TIKTOK]
أرجع مخرجين:
1) SCRIPT: سكريبت فيديو من 45 إلى 70 ثانية (مقسّم لقطات)
2) VIDEO_PROMPT: وصف مشهد سينمائي للفيديو
وأضف في النهاية سطر:
IMAGE_PROMPT: <وصف لصورة الغلاف بأسلوب مناسب>
"""

    return f"""
أنت محرر نمو/انتشار عالمي (Growth) متخصص في صناعة محتوى عربي عالي الأداء.
أسلوب العميل (Style DNA): {style_dna}
أسلوب الصور المطلوب: {image_style}

{wpil_block}
{remix_block}

[TOPIC / INPUT]
{topic}

{format_block}

[NON-NEGOTIABLE]
- اكتب بالعربية.
- لا تذكر أنك نموذج ذكاء اصطناعي.
- لا تقيّم الفكرة ولا ترفضها. فقط أخرج المحتوى الجاهز للنشر.
""".strip()


def _handle_generate(platform: str):
    try:
        payload = _safe_json()

        text = (payload.get("text") or payload.get("topic") or "").strip()
        style_dna = (payload.get("style_dna") or "Professional").strip()
        image_style = (payload.get("image_style") or "Cinematic").strip()

        # Winning Posts inputs (اختياري)
        niche = (payload.get("niche") or payload.get("winning_niche") or "").strip() or "general"
        winning_post = (payload.get("winning_post") or payload.get("winning_text") or "").strip()

        # قرار SIC (بدون رفض)
        decision = strategic_intelligence_core({
            "text": text,
            "content_signal": {"raw_text": text},
            "style_signal": {"style_dna": style_dna},
            "context_signal": {"platforms_available": [platform]},
        })

        topic = decision.get("transformed_input", text)

        # WPIL (يفرض قيود بنيوية فقط)
        wpil = _build_wpil(platform=platform, niche=niche, winning_post=winning_post, topic=topic)
        wpil_constraints = wpil.get("constraints", {}) or {}
        wpil_mode = wpil.get("mode", "direct")

        # إعادة تمرير قيود WPIL داخل SIC (للشفافية)
        decision = strategic_intelligence_core({
            "text": topic,
            "content_signal": {"raw_text": topic},
            "style_signal": {"style_dna": style_dna},
            "context_signal": {"platforms_available": [platform]},
            "wpil_constraints": wpil_constraints,
            "wpil_mode": wpil_mode
        })

        prompt = _prompt_for(
            platform=platform,
            topic=decision.get("transformed_input", topic),
            style_dna=style_dna,
            image_style=image_style,
            wpil_constraints=wpil_constraints,
            winning_post=winning_post
        )

        out = _call_gemini(prompt)

        # TikTok: استخراج VIDEO_PROMPT لو موجود
        video_prompt = ""
        if platform == "tiktok":
            m = re.search(r"VIDEO_PROMPT\s*:\s*(.+)", out, re.IGNORECASE)
            video_prompt = (m.group(1).strip() if m else "")

        image_prompt = _extract_image_prompt(out)
        clean_text = _clean_model_text(out)

        record_success(platform, meta={"wpil": bool(wpil_constraints), "niche": niche})

        return jsonify({
            "text": clean_text,
            "image": image_prompt,
            "video_prompt": video_prompt,
            "wpil_trace": _LAST_WPIL_TRACE
        })

    except Exception as e:
        record_failure(platform, reason=str(e))
        return jsonify({"error": str(e)}), 500


# ============================
# Generate Routes
# ============================
@app.post("/generate/linkedin")
def gen_linkedin():
    return _handle_generate("linkedin")


@app.post("/generate/twitter")
def gen_twitter():
    return _handle_generate("twitter")


@app.post("/generate/tiktok")
def gen_tiktok():
    return _handle_generate("tiktok")
