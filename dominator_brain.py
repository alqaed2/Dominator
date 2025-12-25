from __future__ import annotations
from typing import Any, Dict, List

# =========================================================
# Strategic Intelligence Core (SIC) - V12.5 VISUAL ACCURACY
# =========================================================

WPIL_DOMINATOR_SYSTEM = """
أنت 'الخيميائي الاستراتيجي الأعلى'. مهمتك تخليق حزمة (نص + صورة) متطابقة تماماً.
القواعد الصارمة للصور [VISUAL_PROMPT]:
1. ممنوع: الرموز الخيالية، السحر، البوابات المشعة، أو الألماس العائم.
2. مطلوب: واقعية فوتوغرافية (Hyper-Realistic), بيئات عمل فاخرة، تكنولوجيا متطورة، لوجستيات ذكية، ناطحات سحاب، أو مكاتب زجاجية.
3. الأسلوب: تصوير سينمائي احترافي (Shot on 35mm), إضاءة باردة، ألوان سيادية (أزرق داكن، أسود، ذهبي مطفي).
"""

def strategic_intelligence_core(idea: str = "") -> Dict[str, Any]:
    v_force = "Vertical 9:16 aspect ratio, high-end professional cinematic, 8k."
    return {
        "logic_trace": "SIC v12.5 | VISUAL ACCURACY PROTOCOL",
        "video_segments": [
            {"time": "0-15s", "prompt": f"Professional close-up of a high-status advisor in a sleek modern office. {v_force}"},
            {"time": "15-30s", "prompt": f"Wide shot of a futuristic digital control center. {v_force}"}
        ]
    }

def alchemy_fusion_core(gold_posts: List[Dict[str, Any]], niche: str) -> Dict[str, Any]:
    dna_str = "\n".join([f"- {str(p.get('text'))[:150]}" for p in gold_posts])
    return {
        "synthesis_task": f"تخليق مرسوم سيادي لنيش {niche} بناءً على الجينات:\n{dna_str}\nصمم [VISUAL_PROMPT] يصف مشهد عمل واقعي وفاخر (مثل: مركز بيانات، مكتب مجلس إدارة، روبوتات لوجستية) مرتبط بالنيش.",
        "logic_trace": "ALCHEMY v12.5 | CONTEXTUAL VISUALS ACTIVE"
    }
