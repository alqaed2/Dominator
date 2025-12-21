# ... (لا تغيير في الاستيرادات) ...

@app.route("/generate/<platform>", methods=["POST", "GET"])
@app.route("/remix", methods=["POST", "GET"])
def handle_execution(platform="linkedin"):
    # ... (نفس منطق استخراج البيانات) ...
    idea, seed, style = extract_ui_data()
    
    try:
        brain = strategic_intelligence_core(idea, platform, style, seed)
        # توليد النص
        text_output = get_ai_response_with_failover(f"{WPIL_DOMINATOR_SYSTEM}\nالمهمة: {brain['transformed_input']}")
        final_text = f"{text_output}{brain['viral_signature']}"

        payload = {
            "platform": platform,
            "text": final_text,
            "trace": brain["logic_trace"],
            "remixed_seed": idea if idea else seed,
            "sic_transformed_input": brain['transformed_input']
        }

        if platform == "tiktok":
            # تعليمات واضحة للمستخدم لاستخدام الأبعاد الصحيحة
            v_prompt = "🚨 **هام: استخدم إعدادات (9:16) أو (Vertical) في محرك الفيديو**\n\n"
            for seg in brain["video_segments"]:
                v_prompt += f"### المشهد ({seg['time']}):\n```text\n{seg['prompt']}\n```\n\n"
            payload["video_prompt"] = v_prompt

        return jsonify(payload), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
