# =========================================================
# SIC Memory Store
# AI DOMINATOR – V16.1
# =========================================================

# Simple in-memory performance tracking (deterministic)

PLATFORM_MEMORY = {
    "linkedin": {
        "success": 0,
        "failure": 0
    },
    "twitter": {
        "success": 0,
        "failure": 0
    },
    "tiktok": {
        "success": 0,
        "failure": 0
    }
}

def record_success(platform: str):
    if platform in PLATFORM_MEMORY:
        PLATFORM_MEMORY[platform]["success"] += 1

def record_failure(platform: str):
    if platform in PLATFORM_MEMORY:
        PLATFORM_MEMORY[platform]["failure"] += 1

def get_platform_score(platform: str) -> float:
    data = PLATFORM_MEMORY.get(platform)
    if not data:
        return 0.5

    total = data["success"] + data["failure"]
    if total == 0:
        return 0.5

    return data["success"] / total
