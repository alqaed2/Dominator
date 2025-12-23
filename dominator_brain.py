from __future__ import annotations
from typing import Any, Dict, List

# =========================================================
# Strategic Intelligence Core (SIC) - V6.0 FINAL AUTHORITY
# =========================================================

WPIL_DOMINATOR_SYSTEM = """
أنت 'الخيميائي الاستراتيجي الأعلى' (THE SUPREME ALCHEMIST). 
مهمتك: استقبال الجينات الفيروسية وتخليق محتوى مهيمن يمتلك سلطة معرفية مطلقة.
الهوية: واقعية سينمائية فخمة (9:16).
"""

def strategic_intelligence_core(idea: str = "", platform: str = "linkedin", style: str = "default", reference_post: str = "") -> Dict[str, Any]:
    idea_clean = str(idea or "السيادة المطلقة").strip()
    v_force = "Vertical 9:16 aspect ratio, portrait orientation, smartphone mobile view, --ar 9:16,"
    char_dna = "ultra-realistic cinematic 8k, elite male strategic advisor, bespoke suit,"
    
    scenes = [
        {"time": "0-10s", "prompt": f"{v_force} Close-up of advisor's face. {char_dna}"},
        {"time": "10-20s", "prompt": f"{v_force} Advisor in a high-tech obsidian office. {char_dna}"},
        {"time": "20-30s", "prompt": f"{v_force} Full body shot, advisor walking confidently. {char_dna}"}
    ]
    return {
        "transformed_input": f"توليد محتوى قيادي حاد لـ [{idea_clean}]",
        "logic_trace": "V6.0 | SUPREME COMMAND ENABLED",
        "video_segments": scenes,
        "viral_signature": "\n\n---\n💡 تم الهندسة بواسطة مفاعل AI DOMINATOR v6.0"
    }

def alchemy_fusion_core(gold_posts: List[Dict[str, Any]], niche: str) -> Dict[str, Any]:
    dna = [f"Text: {p['text']} | Stats: {p['engagement']}" for p in gold_posts]
    return {
        "synthesis_task": f"دمج وتخليق منشور واحد خارق لنيش {niche} بناءً على الجينات: {dna}",
        "dominance_score": 99,
        "logic_trace": f"SYNTHESIS ACTIVE | v6.0"
    }
