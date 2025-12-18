# wpil_runtime.py
# WPIL Runtime Enforcement Engine
# Applies selected winning patterns as non-negotiable constraints

from typing import Dict
from wpil_selector import select_winning_pattern


def invoke_wpil(content_signal: Dict) -> Dict:
    """
    Invokes WPIL runtime.
    Selects a winning pattern and converts it into enforced constraints.
    """

    # Select the best winning pattern for this signal
    winning_pattern = select_winning_pattern(content_signal)

    # Base enforced constraints
    enforced_constraints = {
        "hook": winning_pattern.get("hook"),
        "structure": winning_pattern.get("structure"),
        "cta": winning_pattern.get("cta"),
        "enforcement": {
            "mode": "strict",
            "fallback": False
        }
    }

    return enforced_constraints
