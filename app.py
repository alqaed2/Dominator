from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import os
import re

# 🧠 Strategic Intelligence Core
from dominator_brain import strategic_intelligence_core

# 🧠 Memory (optional)
from sic_memory import record_success, record_failure

app = Flask(__name__)

# -------------------------------------------------
# Environment Configuration
# -------------------------------------------------
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
GEMINI_MODEL = os.environ.get("GEMINI_MODEL")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY missing")
if not GEMINI_MODEL:
    raise ValueError("GEMINI_MODEL missing")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel(GEMINI_MODEL)

# -------------------------------------------------
# Helpers
# -------------------------------------------------
def extract(text, start, end):
    if not text:
        return ""
    m = re.search(re.escape(start) + r"(.*?)" + re.escape(end), text, re.DOTALL)
    return m.group(1).strip() if m else ""

def get_safe_response(prompt: str) -> str:
    response = model.generate_content(prompt)
    if hasattr(response, "text") and response.text:
        return response.text
    return response.candidates[0].content.parts[0].text

# -------------------------------------------------
# Brain Payload Builder
# -------------------------------------------------
def build_brain_payload(raw_text: str, style_dna: str):
    return {
        "content_signal": {
            "topic": raw_text,
            "raw_text": raw_text,
            "intent": "dominate"
        },
        "style_signal": {
            "style_dna": style_dna,
            "confidence_level": 0.9
        },
        "context_signal": {
            "platforms_available": ["linkedin", "twitter", "tiktok"],
            "time_context": "now"
        },
        "system_memory": {}
    }

# -------------------------------------------------
# Winning Posts Remix Engine (Prompt-based)
# -------------------------------------------------
def remix_winning_post(winning_post: str, niche: str, voice: str, platform: str) -> str:
    """
    Takes a high-performing post and rewrites it into a fresh, non-derivative version.
    Then returns a new 'raw_text' seed that SIC will further dominance-inject.
    """
    winning_post = (winning_post or "").strip()
    niche = (niche or "general").strip()
    voice = (voice or "Professional").strip()

    prompt = (
        f"You are an elite content remixer.\n"
        f"Goal: produce a NEW post inspired by the idea, NOT copying wording.\n"
        f"Niche: {niche}\n"
        f"Target platform: {platform}\n"
        f"Voice: {voice}\n\n"
        f"Rules:\n"
        f"- Keep the same core insight, but change structure, examples, phrasing, and angles.\n"
        f"- Add one personal micro-story (2-3 lines) and one strong CTA.\n"
        f"- Include a pattern-interrupt hook in the first line.\n"
        f"- Output in Arabic.\n\n"
        f"OUTPUT FORMAT:\n"
        f"---REMIX_START---\n"
        f"(Remixed seed text)\n"
        f"---REMIX_END---\n\n"
        f"WINNING POST INPUT:\n"
        f"{winning_post}\n"
    )

    txt = get_safe_response(prompt)
    remixed = extract(txt, "---REMIX_START---", "---REMIX_END---")
    return remixed.strip() if remixed.strip() else winning_post

# -------------------------------------------------
# Routes
# -------------------------------------------------
@app.route("/")
def home():
    return render_template("index.html")

# ✅ NEW: Dedicated Remix endpoint
@app.route("/remix", methods=["POST"])
def remix_endpoint():
    try:
        data = request.get_json(silent=True) or {}
        winning_post = data.get("winning_post", "")
        niche = data.get("niche", "general")
        voice = data.get("style_dna", "Professional")
        platform = data.get("platform", "linkedin")

        if not winning_post or len(winning_post.strip()) < 30:
            return jsonify({"error": "winning_post is required (min ~30 chars)."}), 400

        remixed = remix_winning_post(winning_post, niche, voice, platform)

        # Pass through SIC for dominance shaping
        decision = strategic_intelligence_core(build_brain_payload(remixed, voice))

        return jsonify({
            "remixed_seed": remixed,
            "sic_transformed_input": decision.get("transformed_input", remixed),
            "sic_decision": {
                "primary_platform": decision.get("primary_platform"),
                "secondary_platforms": decision.get("secondary_platforms", []),
                "content_mode": decision.get("content_mode"),
                "rules": decision.get("rules", {}),
                "decision_reason": decision.get("decision_reason"),
            }
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/generate/linkedin", methods=["POST"])
def generate_linkedin():
    return execute_with_brain("linkedin")

@app.route("/generate/twitter", methods=["POST"])
def generate_twitter():
    return execute_with_brain("twitter")

@app.route("/generate/tiktok", methods=["POST"])
def generate_tiktok():
    return execute_with_brain("tiktok")

# -------------------------------------------------
# 🧠 Unified Execution Gate (NO BLOCK MODE)
# -------------------------------------------------
def execute_with_brain(requested_platform: str):
    try:
        data = request.get_json(silent=True) or {}
        if "text" not in data:
            return jsonify({"error": "No data provided (missing 'text')."}), 400

        user_text = (data.get("text") or "").strip()
        style = data.get("style_dna", "Professional")
        image_style = data.get("image_style", "Default")

        # Optional Winning Posts Remix
        winning_post = (data.get("winning_post") or "").strip()
        niche = data.get("niche", "general")

        # 1) If winning_post provided → remix into fresh seed
        seed_text = user_text
        if winning_post:
            seed_text = remix_winning_post(
                winning_post=winning_post,
                niche=niche,
                voice=style,
                platform=requested_platform
            )

        # 2) SIC shapes the final input (dominance injection)
        decision = strategic_intelligence_core(build_brain_payload(seed_text, style))
        final_input = decision.get("transformed_input") or seed_text

        # 3) Generate per platform (SIC never blocks; only guides)
        if requested_platform == "linkedin":
            prompt = (
                f"Act as a LinkedIn Expert.\n"
                f"Write a viral post.\n"
                f"Topic seed: {final_input}\n"
                f"Style: {style}\n"
                f"Image Style: {image_style}\n"
                f"Constraints: hook_required={decision.get('rules', {}).get('hook_required', True)} "
                f"cta_type={decision.get('rules', {}).get('cta_type', 'curiosity')} "
                f"length={decision.get('rules', {}).get('length', 'medium')}\n\n"
                f"OUTPUT FORMAT:\n"
                f"---LINKEDIN_START---\n"
                f"(Content)\n"
                f"---LINKEDIN_END---\n"
                f"---IMAGE_MAIN_START---\n"
                f"(Image Prompt)\n"
                f"---IMAGE_MAIN_END---\n"
            )

            text = get_safe_response(prompt)
            payload = {
                "text": extract(text, "---LINKEDIN_START---", "---LINKEDIN_END---"),
                "image": extract(text, "---IMAGE_MAIN_START---", "---IMAGE_MAIN_END---"),
                "meta": {"sic": decision, "seed_used": seed_text, "final_input": final_input}
            }
            record_success("linkedin")
            return jsonify(payload)

        if requested_platform == "twitter":
            prompt = (
                f"Act as a Twitter/X Expert.\n"
                f"Write a 5-tweet thread.\n"
                f"Topic seed: {final_input}\n"
                f"Style: {style}\n"
                f"Constraints: hook_required={decision.get('rules', {}).get('hook_required', True)} "
                f"cta_type={decision.get('rules', {}).get('cta_type', 'curiosity')} "
                f"length={decision.get('rules', {}).get('length', 'short')}\n\n"
                f"OUTPUT FORMAT:\n"
                f"---TWITTER_START---\n"
                f"(Thread)\n"
                f"---TWITTER_END---\n"
            )

            text = get_safe_response(prompt)
            payload = {
                "text": extract(text, "---TWITTER_START---", "---TWITTER_END---"),
                "meta": {"sic": decision, "seed_used": seed_text, "final_input": final_input}
            }
            record_success("twitter")
            return jsonify(payload)

        if requested_platform == "tiktok":
            prompt = (
                f"Act as a TikTok Director.\n"
                f"Write a script AND a video generation prompt.\n"
                f"Topic seed: {final_input}\n"
                f"Style: {style}\n"
                f"Image Style: {image_style}\n"
                f"Constraints: hook_required={decision.get('rules', {}).get('hook_required', True)} "
                f"cta_type={decision.get('rules', {}).get('cta_type', 'curiosity')} "
                f"length={decision.get('rules', {}).get('length', 'medium')}\n\n"
                f"OUTPUT FORMAT:\n"
                f"---TIKTOK_START---\n"
                f"(Script)\n"
                f"---TIKTOK_END---\n"
                f"---TIKTOK_IMAGE_START---\n"
                f"(Cover Image Prompt)\n"
                f"---TIKTOK_IMAGE_END---\n"
                f"---VIDEO_PROMPT_START---\n"
                f"(Video Prompt)\n"
                f"---VIDEO_PROMPT_END---\n"
            )

            text = get_safe_response(prompt)
            payload = {
                "text": extract(text, "---TIKTOK_START---", "---TIKTOK_END---"),
                "image": extract(text, "---TIKTOK_IMAGE_START---", "---TIKTOK_IMAGE_END---"),
                "video_prompt": extract(text, "---VIDEO_PROMPT_START---", "---VIDEO_PROMPT_END---"),
                "meta": {"sic": decision, "seed_used": seed_text, "final_input": final_input}
            }
            record_success("tiktok")
            return jsonify(payload)

        record_failure(requested_platform)
        return jsonify({"error": "Unsupported platform"}), 400

    except Exception as e:
        # If anything fails, record failure but do not block future runs
        try:
            record_failure(requested_platform)
        except:
            pass
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
