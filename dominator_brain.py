from __future__ import annotations
from typing import Any, Dict, List

# =========================================================
# Strategic Intelligence Core (SIC) - V12.8 ABSOLUTE
# =========================================================

WPIL_DOMINATOR_SYSTEM = """
أنت 'الخيميائي الاستراتيجي الأعلى'. مهمتك تخليق حزمة سيادية (نص + صورة) متطابقة تماماً.
القواعد الصارمة للصور [VISUAL_PROMPT]:
1. ممنوع تماماً: الرموز الخيالية، السحر، البوابات المشعة، أو الألماس العائم.
2. المطلوب: واقعية فوتوغرافية احترافية، بيئات عمل فاخرة، تكنولوجيا متطورة، ناطحات سحاب، أو مكاتب زجاجية.
3. التنسيق: رد واحد يحتوي على المنصات مفصولة بـ [LINKEDIN], [TWITTER], [TIKTOK] وفي النهاية [VISUAL_PROMPT] بالإنجليزية.
"""

def strategic_intelligence_core(idea: str = "") -> Dict[str, Any]:
    v_force = "Vertical 9:16 aspect ratio, high-end professional cinematic, 8k portrait."
    return {
        "logic_trace": "SIC v12.8 | AUTHORITY LOCKDOWN",
        "video_segments": [
            {"time": "0-15s", "prompt": f"Professional close-up of high-status advisor. {v_force}"},
            {"time": "15-30s", "prompt": f"Advisor in a minimalist luxury boardroom. {v_force}"}
        ]
    }

def alchemy_fusion_core(gold_posts: List[Dict[str, Any]], niche: str) -> Dict[str, Any]:
    dna_str = "\n".join([f"- {str(p.get('text'))[:150]}" for p in gold_posts])
    return {
        "synthesis_task": f"تخليق مرسوم سيادي لنيش {niche} بناءً على الجينات التالية المستخرجة من الهدف:\n{dna_str}\nقم بصياغة فكرة محتوى خارقة تعتمد على هذه الجينات ثم أضف [VISUAL_PROMPT] بالإنجليزية.",
        "logic_trace": "ALCHEMY v12.8 | STABLE FUSION ACTIVE"
    }
