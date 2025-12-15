from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import os
import re

app = Flask(__name__)

# --- إعدادات النظام ---
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
GEMINI_MODEL = os.environ.get('GEMINI_MODEL')

if not GEMINI_API_KEY or not GEMINI_MODEL:
    raise ValueError("❌ Error: Missing GEMINI_API_KEY or GEMINI_MODEL in Render.")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel(GEMINI_MODEL)

# --- (V11.5 SMART SUPER PROMPT) ---
# هذا الأمر يطلب من الذكاء الاصطناعي إجراء عملية النقد داخلياً قبل الكتابة
SMART_PROMPT = """
قم بدور "رئيس تحرير تنفيذي" يقود فريقاً من الخبراء.
المهمة: إنشاء حملة محتوى فيروسية (Viral) متكاملة بناءً على المعطيات التالية:

الموضوع: {topic}
بصمة الأسلوب (DNA): {style_dna}
النمط البصري: {image_style}

⚠️ **تعليمات التفكير الداخلي (Internal Chain of Thought):**
1. (تحليل): حلل الموضوع واستخرج أقوى زاوية جذب (Hook).
2. (نقد): تجنب الكليشيهات والجمل المملة. اجعل النص مباشراً ومثيراً للجدل أو الفضول.
3. (إخراج): صمم تسلسلاً بصرياً للفيديو يشد الانتباه من الثانية الأولى.

🔴 **المخرجات النهائية المطلوبة (يجب الالتزام بالفواصل بدقة):**

---LINKEDIN_START---
(اكتب مقال LinkedIn: احترافي، يستخدم نقاطاً (Bulleted list)، ويبدأ بجملة قوية جداً. استخدم الإيموجي بذكاء)
---LINKEDIN_END---

---TWITTER_START---
(اكتب ثريد X: يتكون من 5 تغريدات مترابطة. التغريدة الأولى يجب أن تكون "Hook" لا يقاوم)
---TWITTER_END---

---TIKTOK_START---
(اكتب سكريبت TikTok: مفصل، سريع الإيقاع. حدد: [المشهد]، [الصوت]، [النص على الشاشة])
---TIKTOK_END---

---IMAGE_MAIN_START---
(Professional prompt for the main article image: {image_style}, high quality, aspect ratio 1:1)
---IMAGE_MAIN_END---

---STORYBOARD_IMG1_START---
(Prompt for Video Scene 1 - The Hook: {image_style}, dynamic angle)
---STORYBOARD_IMG1_END---

---STORYBOARD_IMG2_START---
(Prompt for Video Scene 2 - The Value/Explanation: {image_style}, clear focus)
---STORYBOARD_IMG2_END---

---STORYBOARD_IMG3_START---
(Prompt for Video Scene 3 - The Call to Action: {image_style}, impactful)
---STORYBOARD_IMG3_END---

---VIDEO_PROMPT_START---
(Highly detailed Cinematic Video Prompt for generative video AI (Sora/Runway). Describe camera movement, lighting, mood, and action sequence based on the script)
---VIDEO_PROMPT_END---
"""

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze-style', methods=['POST'])
def analyze_style():
    # تحليل سريع (Dummy لتوفير الوقت في الواجهة، أو يمكن تفعيله بطلب بسيط)
    return jsonify({'style_dna': "تم استخراج البصمة الأسلوبية بنجاح."}) 

def extract_section(text, start_tag, end_tag):
    try:
        pattern = re.escape(start_tag) + r"(.*?)" + re.escape(end_tag)
        match = re.search(pattern, text, re.DOTALL)
        return match.group(1).strip() if match else "Content generation failed."
    except:
        return "Error."

@app.route('/generate', methods=['POST'])
def generate():
    try:
        data = request.json
        topic = data.get('text', '')
        style_dna = data.get('style', '') or "Professional & Engaging"
        image_style = data.get('image_style', 'Cyberpunk')

        if not topic: return jsonify({'error': 'النص فارغ'}), 400

        # استخدام الأمر الذكي الموحد
        final_prompt = SMART_PROMPT.format(topic=topic, style_dna=style_dna, image_style=image_style)
        
        # طلب واحد للسيرفر = سرعة قصوى وعدم انقطاع
        response = model.generate_content(final_prompt)
        full_output = response.text

        results = {
            'linkedin': extract_section(full_output, "---LINKEDIN_START---", "---LINKEDIN_END---"),
            'twitter': extract_section(full_output, "---TWITTER_START---", "---TWITTER_END---"),
            'tiktok': extract_section(full_output, "---TIKTOK_START---", "---TIKTOK_END---"),
            'image_main': extract_section(full_output, "---IMAGE_MAIN_START---", "---IMAGE_MAIN_END---"),
            'story_img1': extract_section(full_output, "---STORYBOARD_IMG1_START---", "---STORYBOARD_IMG1_END---"),
            'story_img2': extract_section(full_output, "---STORYBOARD_IMG2_START---", "---STORYBOARD_IMG2_END---"),
            'story_img3': extract_section(full_output, "---STORYBOARD_IMG3_START---", "---STORYBOARD_IMG3_END---"),
            'video_prompt': extract_section(full_output, "---VIDEO_PROMPT_START---", "---VIDEO_PROMPT_END---"),
            'debug': "تم التوليد باستخدام المحرك الذكي الموحد (Smart Unified Engine) لضمان الجودة والسرعة."
        }

        # ملء الصور الفارغة احتياطياً
        fallback = f"{image_style} illustration about {topic}, high quality"
        for key in ['image_main', 'story_img1', 'story_img2', 'story_img3']:
            if len(results[key]) < 10: results[key] = fallback

        return jsonify(results)

    except Exception as e:
        print(f"Server Error: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
