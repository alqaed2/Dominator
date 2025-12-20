# =========================================================
# Strategic Intelligence Core (SIC) - AI DOMINATOR V2.0
# Optimized for Global Technical Dominance
# =========================================================

from __future__ import annotations
from typing import Dict, Any, List, Tuple

# الميثاق الأعلى للنظام (The Supreme System Prompt)
WPIL_DOMINATOR_SYSTEM = """
أنت "AI DOMINATOR"، العقل الاستراتيجي الأكثر تطوراً في صناعة المحتوى عالي التأثير.
مهمتك: تحويل الأفكار الخام إلى أسلحة ناعمة (Content Assets) تكتسح المنصات الرقمية.

مبادئك الصارمة:
1. Authority (السلطة): تحدث كخبير لا يُناقش، لست مجرد أداة مساعدة.
2. Structure (الهيكلية): استخدم (Hook خطاف قاتل، Value قيمة مكثفة، CTA دعوة للتحرك).
3. Nuance (التمايز): محتوى LinkedIn عميق واستراتيجي، X حاد وموجز، TikTok سكريبت بصري مذهل.
4. Language (اللغة): عربية قوية، حديثة، واثقة، ومباشرة جداً.
"""

def strategic_intelligence_core(idea: str, platform: str = "linkedin", style: str = "default") -> Dict[str, Any]:
    """
    محرك التحويل الاستراتيجي: يضمن أن أي فكرة يتم تمريرها يتم 'ترويضها' لتناسب المنصة.
    """
    raw_text = (idea or "").strip()
    platform = _normalize_platform(platform)
    
    # تحليل وتقوية النص قبل الإرسال للموديل
    transformed_text = _apply_dominance_logic(raw_text, platform)

    return {
        "status": "success",
        "primary_platform": platform,
        "transformed_input": transformed_text,
        "logic_trace": f"Dominance Applied | Platform: {platform} | Mode: {style}"
    }

def _normalize_platform(p: str) -> str:
    p = (p or "linkedin").strip().lower()
    mapping = {
        "x": "twitter", "twitter": "twitter", "tweet": "twitter",
        "tt": "tiktok", "tiktok": "tiktok", "tik-tok": "tiktok",
        "ln": "linkedin", "linkedin": "linkedin"
    }
    return mapping.get(p, "linkedin")

def _apply_dominance_logic(text: str, platform: str) -> str:
    """حقن قواعد الهيمنة بناءً على نوع المنصة"""
    if not text: return "فكرة استراتيجية للنمو"
    
    prefixes = {
        "linkedin": "تحليل استراتيجي عميق: ",
        "twitter": "إليك الحقيقة المختصرة: ",
        "tiktok": "المشهد الافتتاحي: "
    }
    return f"{prefixes.get(platform, '')}{text}"
