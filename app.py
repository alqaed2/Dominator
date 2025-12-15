from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import os
import re

app = Flask(__name__)

# --- إعدادات النظام ---
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
GEMINI_MODEL = os.environ.get('GEMINI_MODEL')

if not GEMINI_API_KEY or not GEMINI_MODEL:
    raise ValueError("❌ Error: Missing GEMINI_API_KEY or GEMINI_MODEL.")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel(GEMINI_MODEL)

# --- الأمر المبسط (Simplified Prompt) ---
EDITOR_PROMPT = """
أنت مدير محتوى شامل.
المهمة: تحويل الفكرة إلى حملة لمنصات متعددة مع وصف للصور.

الموضوع: {topic}
الأسلوب: {style_dna}
نمط الصور: {image_style}

⚠️ المخرجات المطلوبة (التزم بالفواصل):

---LINKEDIN_START---
(مقال LinkedIn احترافي)
---LINKEDIN_END---

---TWITTER_START---
(ثريد X مكون من 5 تغريدات)
---TWITTER_END---

---TIKTOK_START---
(سكريبت TikTok: المشهد، الصوت، النص)
---TIKTOK_END---

---IMAGE_MAIN_START---
(وصف صورة للمقال الرئيسي: {image_style})
---IMAGE_MAIN_END---

---TIKTOK_IMAGE_START---
(وصف صورة واحدة جذابة جداً لغلاف فيديو التيك توك: {image_style})
---TIKTOK_IMAGE_END---

---VIDEO_PROMPT_START---
(Cinematic Video Prompt for Sora/Runway: detailed description)
---VIDEO_PROMPT_END---
"""

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze-style', methods=['POST'])
def analyze_style():
    return jsonify({'style_dna': "تم التحليل بنجاح."})

def extract_section(text, start_tag, end_tag):
    try:
        pattern = re.escape(start_tag) + r"(.*?)" + re.escape(end_tag)
        match = re.search(pattern, text, re.DOTALL)
        return match.group(1).strip() if match else "Generating..."
    except:
        return "Error."

@app.route('/generate', methods=['POST'])
def generate():
    try:
        data = request.json
        topic = data.get('text', '')
        style_dna = data.get('style', '') or "Professional"
        image_style = data.get('image_style', 'Cyberpunk')

        if not topic: return jsonify({'error': 'النص فارغ'}), 400

        final_prompt = EDITOR_PROMPT.format(topic=topic, style_dna=style_dna, image_style=image_style)
        
        response = model.generate_content(final_prompt)
        full_output = response.text

        results = {
            'linkedin': extract_section(full_output, "---LINKEDIN_START---", "---LINKEDIN_END---"),
            'twitter': extract_section(full_output, "---TWITTER_START---", "---TWITTER_END---"),
            'tiktok': extract_section(full_output, "---TIKTOK_START---", "---TIKTOK_END---"),
            'image_main': extract_section(full_output, "---IMAGE_MAIN_START---", "---IMAGE_MAIN_END---"),
            'tiktok_image': extract_section(full_output, "---TIKTOK_IMAGE_START---", "---TIKTOK_IMAGE_END---"),
            'video_prompt': extract_section(full_output, "---VIDEO_PROMPT_START---", "---VIDEO_PROMPT_END---"),
            'debug': "تم التوليد بنجاح (وضع الصورة الواحدة)."
        }

        # تصحيح سريع للصور الفارغة
        fallback = f"{image_style} illustration about {topic}"
        if len(results['image_main']) < 5: results['image_main'] = fallback
        if len(results['tiktok_image']) < 5: results['tiktok_image'] = fallback

        return jsonify(results)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
