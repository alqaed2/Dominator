from __future__ import annotations
from typing import Any, Dict, List

# =========================================================
# Strategic Intelligence Core (SIC) - V5.3 SUPREME STABILITY
# =========================================================

# ميثاق النظام الأساسي - الضروري لتشغيل app.py
WPIL_DOMINATOR_SYSTEM = """
أنت 'الخيميائي الاستراتيجي الأعلى' (THE SUPREME ALCHEMIST). 
مهمتك: تشريح المحتوى العالمي، استخلاص الجينات الفيروسية، وتخليق منشورات خارقة تمتلك سلطة معرفية مطلقة.
الهوية البصرية: واقعية سينمائية فخمة (9:16).
اللغة: العربية النخبوية.
"""

def strategic_intelligence_core(idea: str = "", platform: str = "linkedin", style: str = "default", reference_post: str = "") -> Dict[str, Any]:
    """المحرك الاستراتيجي للنتائج الفردية والطولية."""
    idea_clean = str(idea or "السيادة الاستراتيجية").strip()
    
    # أوامر تقنية قهرية للأبعاد الطولية 9:16
    vertical_force = "Vertical 9:16 portrait mode, smartphone aspect ratio, --ar 9:16, height 1920 width 1080,"
    char_dna = "ultra-realistic cinematic 8k, elite male strategic advisor in luxury office,"
    
    scenes = [
        {"time": "0-8s", "prompt": f"{vertical_force} Portrait close-up of advisor looking sharp. {char_dna} Vertical framing."},
        {"time": "8-16s", "prompt": f"{vertical_force} Full vertical shot, advisor walking towards camera. {char_dna} Mobile format."},
        {"time": "16-32s", "prompt": f"{vertical_force} Portrait shot of advisor gesturing with hands. {char_dna} 9:16 AR."}
    ]

    return {
        "transformed_input": f"صمم محتوى قيادي للفكرة: [{idea_clean}]",
        "logic_trace": "VERTICAL OPTIMIZED v5.3 | SUPREME STABLE",
        "video_segments": scenes,
        "viral_signature": "\n\n---\n💡 تم التخليق بواسطة مفاعل AI DOMINATOR الاستباقي"
    }

def alchemy_fusion_core(gold_posts: List[Dict[str, Any]], niche: str) -> Dict[str, Any]:
    """مفاعل الاندماج: دمج الجينات الفيروسية."""
    dna = [f"Post: {p['text']}" for p in gold_posts]
    task = f"دمج وتخليق منشور واحد خارق لنيش {niche} بناءً على الجينات التالية: {dna}"
    return {
        "synthesis_task": task,
        "dominance_score": 99,
        "logic_trace": f"LIVE INGESTION ACTIVE | NICHE: {niche} | v5.3"
    }
