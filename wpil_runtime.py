# wpil_runtime.py
# WPIL Runtime Interface
# This module enforces winning constraints before SIC execution

from typing import Dict


def invoke_wpil(content_signal: Dict) -> Dict:
    """
    Runtime invocation for WPIL.
    WPIL does NOT generate content.
    WPIL ONLY returns enforced winning constraints.
    """

    platform = content_signal.get("platform")
    niche = content_signal.get("niche")
    intent = content_signal.get("intent")

    # --- Default Winning Constraints ---
    constraints = {
        "hook": {
            "type": "bold_claim",
            "max_words": 12
        },
        "structure": {
            "line_density": "one_idea_per_line",
            "avg_sentence_length": "short"
        },
        "narrative": {
            "arc": "problem_reframe_authority"
        },
        "cta": {
            "type": "curiosity",
            "position": "final_line"
        }
    }

    # --- Platform-specific enforcement ---
    if platform == "linkedin":
        constraints["hook"]["type"] = "contrarian"

    if platform == "x":
        constraints["hook"]["max_words"] = 10

    if platform == "tiktok":
        constraints["narrative"]["arc"] = "pattern_interrupt"

    return constraints
