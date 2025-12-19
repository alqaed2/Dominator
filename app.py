from __future__ import annotations

from flask import Flask, render_template, request, jsonify
import os
import re

import google.generativeai as genai

from dominator_brain import strategic_intelligence_core
from sic_memory import record_success, record_failure

app = Flask(__name__)

# ----------------------------
# Gemini (lazy init)
# ----------------------------
_MODEL = None

def _get_gemini_model():
    global _MODEL
    if _MODEL is not None:
        return _MODEL

    api_key = os.getenv("GEMINI_API_KEY")
    model_name = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")

    if not api_key:
        raise RuntimeError("GEMINI_API_KEY missing")
    genai.configure(api_key=api_key)
    _MODEL = genai.GenerativeModel(model_name)
    return _MODEL

def _clean_text(x: str) -> str:
    x = (x or "").strip()
    # remove excessive whitespace
    x = re.sub(r"\n{3,}", "\n\n", x)
    return x

# ----------------------------
# Views
# ----------------------------
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/health")
def health():
    return jsonify({"ok": True})

# Optional: quick debugging endpoint
@app.route("/debug/decision", methods=["POST"])
def debug_decision():
    data = request.get_json(silent=True) or {}
    raw_text = (data.get("text") or "").strip()
    payload = {
        "text": raw_text,
        "content_signal": {"raw_text": raw_text},
        "style_signal": {"style_dna": data.get("style_dna", "Professional")},
        "context_signal": {"platforms_available": ["linkedin", "twitter", "tiktok"]},
    }
    decision = strategic_intelligence_core(payload)
    return jsonify(decision)

# ----------------------------
# Style Analysis (simple, safe)
# ----------------------------
@app.route("/analyze-style", methods=["POST"])
def analyze_style():
    data = request.get_json(silent=True) or {}
    sample = (data.get("style_text") or "").strip()

    # Heuristic fallback if empty
    if not sample:
        return jsonify({"style_dna": "Professional"})

    # Try Gemini, but never crash the app if it fails
    try:
        model = _get_gemini_model()
        prompt = (
            "حلّل أسلوب الكتابة التالي وأعطني Label واحد فقط (1-3 كلمات) "
            "بالإنجليزية مثل: Professional, Bold, Minimal, Storytelling, Analytical.\n\n"
            f"TEXT:\n{sample}\n"
        )
        resp = model.generate_content(prompt)
        style = _clean_text(getattr(resp, "text", "") or "")
        style = re.sub(r"[^A-Za-z ]+", "", style).strip() or "Professional"
        # Keep it compact
        style = " ".join(style.split()[:3])
        return jsonify({"style_dna": style})
    except Exception:
        return jsonify({"style_dna": "Professional"})

# ----------------------------
# Core generator per platform
# IMPORTANT: matches index.html loop behavior.
# - returns 404 if requested platform is not primary_platform
# - returns 200 for the primary_platform
# ----------------------------
@app.route("/generate/<platform>", methods=["POST"])
def generate(platform: str):
    platform = (platform or "").strip().lower()
    if platform not in ("linkedin", "twitter", "tiktok"):
        return jsonify({"error": "Unsupported platform"}), 400

    data = request.get_json(silent=True) or {}
    raw_text = (data.get("text") or "").strip()
    style_text = (data.get("style_text") or "").strip()
    image_style = (data.get("image_style") or "Cinematic").strip()

    if not raw_text:
        return jsonify({"error": "Missing text"}), 400

    # Build SIC payload
    sic_payload = {
        "text": raw_text,
        "content_signal": {"raw_text": raw_text},
        "style_signal": {"style_dna": data.get("style_dna", "Professional")},
        "context_signal": {"platforms_available": ["linkedin", "twitter", "tiktok"]},
    }

    decision = strategic_intelligence_core(sic_payload)

    # If SIC ever says don't execute (should not), treat as reject
    if not decision.get("execute", False):
        return jsonify({"error": "Rejected by SIC", "decision": decision}), 404

    primary = (decision.get("primary_platform") or "").strip().lower()

    # Key behavior: only the primary platform returns 200 (to satisfy index.html)
    if platform != primary:
        return jsonify({"approved": False, "primary_platform": primary}), 404

    # Generate content
    try:
        model = _get_gemini_model()
    except Exception as e:
        # This should be 500, not 404
        return jsonify({"error": str(e)}), 500

    transformed = decision.get("transformed_input", raw_text)
    style_override = decision.get("style_override", "Professional")
    mode = decision.get("content_mode", "post")
    length = (decision.get("rules", {}) or {}).get("length", "short")

    try:
        if platform == "linkedin":
            prompt = (
                f"Write a high-quality LinkedIn post in Arabic.\n"
                f"Style: {style_override}\n"
                f"Length: {length}\n"
                f"Must include: a strong hook, 3-5 short paragraphs, and a subtle CTA.\n\n"
                f"INPUT:\n{transformed}\n"
            )
            resp = model.generate_content(prompt)
            out = _clean_text(getattr(resp, "text", "") or "")
            record_success(platform)

            return jsonify({
                **decision,
                "approved": True,
                "platform": platform,
                "output_text": out
            }), 200

        if platform == "twitter":
            prompt = (
                f"Write an Arabic Twitter/X thread (6-9 tweets).\n"
                f"Style: {style_override}\n"
                f"Each tweet <= 240 chars.\n"
                f"First tweet is a hook. End with a curiosity CTA.\n\n"
                f"INPUT:\n{transformed}\n"
            )
            resp = model.generate_content(prompt)
            out = _clean_text(getattr(resp, "text", "") or "")
            record_success(platform)

            return jsonify({
                **decision,
                "approved": True,
                "platform": platform,
                "output_text": out
            }), 200

        # tiktok
        prompt = (
            f"Create a TikTok video script in Arabic.\n"
            f"Style: {style_override}\n"
            f"Duration: 45-60 seconds.\n"
            f"Return strictly in this format:\n"
            f"VIDEO_PROMPT: <one paragraph visual prompt>\n"
            f"SCRIPT:\n"
            f"1) <0:00-0:05 hook>\n"
            f"2) <0:05-0:20>\n"
            f"3) <0:20-0:45>\n"
            f"4) <0:45-0:60 CTA>\n"
            f"IMAGE_PROMPT: <one paragraph prompt for a cover image, {image_style}>\n\n"
            f"INPUT:\n{transformed}\n"
        )
        resp = model.generate_content(prompt)
        txt = _clean_text(getattr(resp, "text", "") or "")

        # Parse fields
        video_prompt = ""
        script = ""
        image_prompt = ""

        m1 = re.search(r"VIDEO_PROMPT:\s*(.+?)\nSCRIPT:", txt, flags=re.S | re.I)
        if m1:
            video_prompt = _clean_text(m1.group(1))

        m2 = re.search(r"SCRIPT:\s*(.+?)\nIMAGE_PROMPT:", txt, flags=re.S | re.I)
        if m2:
            script = _clean_text(m2.group(1))

        m3 = re.search(r"IMAGE_PROMPT:\s*(.+)$", txt, flags=re.S | re.I)
        if m3:
            image_prompt = _clean_text(m3.group(1))

        # Fallback: if parsing failed, return the whole thing as script
        if not script:
            script = txt

        record_success(platform)

        return jsonify({
            **decision,
            "approved": True,
            "platform": platform,
            "video_prompt": video_prompt,
            "script": script,
            "image_prompt": image_prompt,
            "output_text": txt
        }), 200

    except Exception as e:
        record_failure(platform)
        return jsonify({"error": str(e), "decision": decision}), 500


if __name__ == "__main__":
    port = int(os.getenv("PORT", "10000"))
    app.run(host="0.0.0.0", port=port)
