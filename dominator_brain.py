# =========================================================
# Strategic Intelligence Core (SIC) - AI DOMINATOR V2.0
# Optimized for Supreme Leadership Mode
# =========================================================

from __future__ import annotations
from typing import Dict, Any, List, Tuple
try:
    from sic_memory import get_platform_score
except ImportError:
    # Fallback if memory module is missing
    def get_platform_score(p): return 1.0

# الميثاق الأعلى للنظام - هذا ما كان يفتقده app.py
WPIL_DOMINATOR_SYSTEM = """
أنت محرك الهيمنة الاستراتيجية (AI DOMINATOR). 
مهمتك: تحويل الأفكار العادية إلى محتوى عابر للمنصات يمتلك "سلطة معرفية" وقدرة عالية على الانتشار.
القواعد الصارمة:
1. التفكير الاستراتيجي أولاً: حلل الفكرة من زاوية غير متوقعة.
2. هندسة الخطاف (Hook): أول جملة يجب أن توقف التمرير (Scroll-stopping).
3. التكيف مع المنصة: LinkedIn (مهني/عميق)، X (حاد/موجز)، TikTok (بصري/سريع).
4. لغة قوية: استخدم لغة عربية حديثة، واثقة، ومباشرة.
5. مخرجات جاهزة للنشر: لا فلسفة زائدة، اعطِ النتائج فوراً.
"""

_ALLOWED_PLATFORMS = ("linkedin", "twitter", "tiktok")

def strategic_intelligence_core(idea: str, platform: str = "linkedin", style: str = "default") -> Dict[str, Any]:
    """
    النسخة المطورة: تحول المدخلات الخام إلى خطة تنفيذية ذكية.
    """
    raw_text = (idea or "").strip()
    platform = _normalize_platform(platform)
    
    # تحليل المؤشرات الحيوية للفكرة
    metrics = _evaluate_metrics(raw_text)
    
    # حقن الهيمنة (تعديل النص ليكون أقوى استراتيجياً)
    transformed_text, metrics = _inject_dominance(raw_text, metrics)

    return {
        "execute": True,
        "primary_platform": platform,
        "style_override": style or "Professional",
        "metrics": metrics,
        "transformed_input": transformed_text,
        "logic_trace": f"Applied Dominance Logic for {platform} with {style} style."
    }

def _normalize_platform(p: str) -> str:
    p = (p or "").strip().lower()
    if p in ("x", "twitter", "tweet"): return "twitter"
    if p in ("tt", "tiktok", "tik-tok"): return "tiktok"
    if p in ("ln", "linkedin"): return "linkedin"
    return "linkedin"

def _evaluate_metrics(text: str) -> Dict[str, float]:
    t = (text or "").lower()
    length = len(t)
    curiosity = 0.50 + (0.25 if "?" in t else 0.0)
    shock = 0.40 + (0.35 if any(w in t for w in ["الحقيقة", "سر", "خطير", "لا أحد"]) else 0.0)
    return {
        "curiosity": min(curiosity, 1.0),
        "shock": min(shock, 1.0),
        "hook_score": 0.75 if length > 10 else 0.40
    }

def _inject_dominance(text: str, metrics: Dict[str, float]) -> Tuple[str, Dict[str, float]]:
    t = (text or "").strip()
    if not t: t = "فكرة استراتيجية جديدة"
    
    # إضافة لمسة احترافية للنص قبل إرساله للـ AI
    if metrics["curiosity"] < 0.7:
        t = f"لماذا يتجاهل الجميع هذه الحقيقة؟ {t}"
    
    return t, metrics
