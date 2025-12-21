# ... (نفس الإعدادات السابقة) ...

@app.route("/generate/<platform>", methods=["POST"])
def handle_generation(platform):
    idea, seed, style = extract_ui_data() # الدالة التي كتبناها سابقاً
    
    try:
        brain = strategic_intelligence_core(idea, platform, style, seed)
        
        # طلب المحتوى النصي
        prompt = f"{WPIL_DOMINATOR_SYSTEM}\nالمهمة: {brain['transformed_input']}\nالمنصة: {platform}"
        text_output = get_ai_response(prompt)

        payload = {
            "platform": platform,
            "text": text_output,
            "trace": brain["logic_trace"]
        }

        # تنسيق مقاطع الفيديو بصيغة كود للمستخدم
        if platform == "tiktok" and "video_segments" in brain:
            formatted_prompts = ""
            for seg in brain["video_segments"]:
                formatted_prompts += f"### Scene: {seg['time']}\n```text\n{seg['prompt']}\n```\n\n"
            payload["video_prompt"] = formatted_prompts

        return jsonify(payload), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
