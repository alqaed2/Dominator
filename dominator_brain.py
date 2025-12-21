def strategic_intelligence_core(idea: str = "", platform: str = "linkedin", style: str = "default", reference_post: str = "") -> Dict[str, Any]:
    # منطق الاندماج الفائق
    primary_subject = (idea or "محتوى استراتيجي").strip()
    ref_content = (reference_post or "").strip()
    
    if ref_content and idea:
        transformed_task = f"ادمج الفكرة: [{primary_subject}] مع هيكل المنشور المرجعي: [{ref_content}]"
        logic_mode = "HYBRID FUSION"
    elif ref_content:
        transformed_task = f"أعد إنتاج هيمنة هذا المنشور المرجعي: [{ref_content}]"
        logic_mode = "REMIX MODE"
    else:
        transformed_task = f"صمم محتوى أصلياً للفكرة: [{primary_subject}]"
        logic_mode = "DIRECT MODE"

    visual_identity = "Ultra-realistic cinematic male advisor, bespoke suit, high-end office, obsidian lighting."

    return {
        "execute": True,
        "primary_platform": platform,
        "transformed_input": transformed_task,
        "visual_prompt": visual_identity,
        "logic_trace": f"MODE: {logic_mode} | PLATFORM: {platform}"
    }
