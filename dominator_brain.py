from __future__ import annotations
from typing import Any, Dict, List

# =========================================================
# Strategic Intelligence Core (SIC) - V5.7 FINAL STABILITY
# =========================================================

WPIL_DOMINATOR_SYSTEM = """
أنت 'الخيميائي الاستراتيجي الأعلى' (THE SUPREME ALCHEMIST). 
مهمتك: تشريح المحتوى العالمي، استخلاص الجينات الفيروسية، وتخليق منشورات خارقة تمتلك سلطة معرفية مطلقة.
الهوية البصرية: واقعية سينمائية فخمة (9:16).
اللغة: العربية النخبوية الاستراتيجية.
"""

def strategic_intelligence_core(idea: str = "", platform: str = "linkedin", style: str = "default", reference_post: str = "") -> Dict[str, Any]:
    idea_clean = str(idea or "السيادة والنمو").strip()
    # أوامر تقنية قهرية للأبعاد الطولية 9:16
    v_force = "Vertical 9:16 aspect ratio, portrait orientation, smartphone mobile view, --ar 9:16,"
    char_dna = "ultra-realistic cinematic 8k, elite male strategic advisor, bespoke suit, luxury office,"
    
    scenes = [
        {"time": "0-8s", "prompt": f"{v_force} Extreme close-up of advisor looking sharp. {char_dna} Vertical framing."},
        {"time": "8-16s", "prompt": f"{v_force} Full vertical shot, advisor walking towards camera. {char_dna} Mobile format."},
        {"time": "16-32s", "prompt": f"{v_force} Portrait shot of advisor gesturing with hands. {char_dna} 9:16 AR."}
    ]
    return {
        "transformed_input": f"صمم محتوى قيادي للفكرة: [{idea_clean}]",
        "logic_trace": "VERTICAL OPTIMIZED v5.7 | SUPREME COMMAND",
        "video_segments": scenes,
        "viral_signature": "\n\n---\n💡 تم الهندسة بواسطة مفاعل AI DOMINATOR الاستباقي"
    }

def alchemy_fusion_core(gold_posts: List[Dict[str, Any]], niche: str) -> Dict[str, Any]:
    dna = [f"Post: {p['text']} | Stats: {p['engagement']}" for p in gold_posts]
    task = f"دمج وتخليق منشور واحد خارق لنيش {niche} بناءً على الجينات الحقيقية التالية: {dna}"
    return {
        "synthesis_task": task,
        "dominance_score": 99,
        "logic_trace": f"LIVE INGESTION ACTIVE | NICHE: {niche} | v5.7"
    }
