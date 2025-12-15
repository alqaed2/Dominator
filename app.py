from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import os
import re

app = Flask(__name__)

# --- إعدادات النظام ---
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
GEMINI_MODEL = os.environ.get('GEMINI_MODEL')

if not GEMINI_API_KEY:
    # استخدام مفتاح احتياطي أو طباعة خطأ واضح في السجلات
    print("❌ Error: GEMINI_API_KEY not found.")

# تهيئة Gemini
try:
    genai.configure(api_key=GEMINI_API_KEY)
    # نستخدم الموديل السريع لضمان عدم حدوث Timeout
    model_name = GEMINI_MODEL if GEMINI_MODEL else "gemini-1.5-flash" 
    model = genai.GenerativeModel(model_name)
    print(f"🤖 System Ready using: {model_name}")
except Exception as e:
    print(f"❌ Setup Error: {e}")

# --- الأمر المبسط والسريع (Fast Prompt) ---
EDITOR_PROMPT = """
أنت خبير محتوى شامل. 
المهمة: توليد حملة تسويقية سريعة جداً.

الموضوع: {topic}
الأسلوب: {style_dna}
ستايل الصور: {image_style}

⚠️ المخرجات المطلوبة (التزم بالفواصل بدقة):

---LINKEDIN_START---
(مقال LinkedIn احترافي وقصير)
---LINKEDIN_END---

---TWITTER_START---
(ثريد X من 5 تغريدات)
---TWITTER_END---

---TIKTOK_START---
(سكريبت TikTok سريع: المشهد، الصوت)
---TIKTOK_END---

---IMAGE_MAIN_START---
(وصف إنجليزي لصورة المقال: {image_style})
---IMAGE_MAIN_END---

---TIKTOK_IMAGE_START---
(وصف إنجليزي لصورة غلاف التيك توك: {image_style})
---TIKTOK_IMAGE_END---

---VIDEO_PROMPT_START---
(Cinematic Video Prompt English)
---VIDEO_PROMPT_END---
"""

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze-style', methods=['POST'])
def analyze_style():
    return jsonify({'style_dna': "تم التحليل (وضع التوفير)."})

def extract_section(text, start_tag, end_tag):
    try:
        # استخدام البحث المرن لتجنب الأخطاء
        pattern = re.escape(start_tag) + r"(.*?)" + re.escape(end_tag)
        match = re.search(pattern, text, re.DOTALL)
        if match:
            return match.group(1).strip()
        else:
            return "Content not generated."
    except:
        return "Error parsing content."

@app.route('/generate', methods=['POST'])
def generate():
    try:
        data = request.json
        topic = data.get('text', '')
        style_dna = data.get('style', '') or "Professional"
        image_style = data.get('image_style', 'Cyberpunk')

        if not topic: return jsonify({'error': 'النص فارغ'}), 400

        print(f"🚀 Processing request for: {topic}")
        
        # التوليد
        final_prompt = EDITOR_PROMPT.format(topic=topic, style_dna=style_dna, image_style=image_style)
        response = model.generate_content(final_prompt)
        full_output = response.text

        # الاستخراج الآمن
        results = {
            'linkedin': extract_section(full_output, "---LINKEDIN_START---", "---LINKEDIN_END---"),
            'twitter': extract_section(full_output, "---TWITTER_START---", "---TWITTER_END---"),
            'tiktok': extract_section(full_output, "---TIKTOK_START---", "---TIKTOK_END---"),
            'image_main': extract_section(full_output, "---IMAGE_MAIN_START---", "---IMAGE_MAIN_END---"),
            'tiktok_image': extract_section(full_output, "---TIKTOK_IMAGE_START---", "---TIKTOK_IMAGE_END---"),
            'video_prompt': extract_section(full_output, "---VIDEO_PROMPT_START---", "---VIDEO_PROMPT_END---"),
            'debug': "Success (Fast Mode)"
        }

        # ملء الفراغات لتجنب الصور المكسورة
        fallback = f"{image_style} illustration about {topic}"
        if len(results['image_main']) < 5: results['image_main'] = fallback
        if len(results['tiktok_image']) < 5: results['tiktok_image'] = fallback

        return jsonify(results)

    except Exception as e:
        print(f"🔥 Server Error: {e}")
        # إرجاع رسالة خطأ واضحة للمتصفح بدلاً من 500 غامضة
        return jsonify({'error': f"فشل المعالجة: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
