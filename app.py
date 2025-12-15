from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import os

app = Flask(__name__)

# --- إعدادات المدير التقني ---
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
GEMINI_MODEL = os.environ.get('GEMINI_MODEL')

if not GEMINI_API_KEY or not GEMINI_MODEL:
    raise ValueError("❌ خطأ قاتل: تأكد من المتغيرات البيئية في Render.")

try:
    genai.configure(api_key=GEMINI_API_KEY)
    print(f"🤖 النظام يعمل بمحرك: {GEMINI_MODEL}")
    model = genai.GenerativeModel(GEMINI_MODEL)
except Exception as e:
    print(f"❌ خطأ في تهيئة Gemini: {e}")

# --- الموظفون الافتراضيون ---

STYLE_ANALYZER_PROMPT = """
أنت خبير لغوي. حلل النص واستخرج "البصمة الأسلوبية" (DNA):
1. النبرة. 2. الهيكل. 3. المفردات.
"""

CREATOR_PROMPT = """
أنت استراتيجي محتوى شامل.
مهمتك: توليد محتوى لمنصات متعددة بناءً على الفكرة، مع تقمص الأسلوب: {style_dna}
الموضوع: {topic}
"""

CRITIC_PROMPT = """
أنت ناقد. هل الأفكار قوية وتناسب كل منصة؟
"""

# 🔥 التحديث العبقري: المحرر متعدد المنصات
EDITOR_PROMPT = """
أنت رئيس تحرير إمبراطورية إعلامية (Editor-in-Chief).
مهمتك تحويل المسودة إلى حملة متكاملة لـ 3 منصات، بالإضافة لتصميم صورة.

⚠️ يجب أن يكون المخرج مقسماً بدقة باستخدام الفواصل التالية (لا تغيرها):

---LINKEDIN_START---
(هنا اكتب مقالاً احترافياً لـ LinkedIn: قوي، منسق، فقرات، هاشتاقات، وتوقيع).
---LINKEDIN_END---

---TWITTER_START---
(هنا اكتب ثريد Thread لـ X: مكون من 5-7 تغريدات مرقمة 1/5، قصيرة، جذابة جداً).
---TWITTER_END---

---TIKTOK_START---
(هنا اكتب سكريبت فيديو TikTok/Reels: قسمه إلى "المشهد"، "زاوية الكاميرا"، "الصوت/الكلام". اجعله سريعاً وحماسياً).
---TIKTOK_END---

---IMAGE_START---
(هنا اكتب وصف الصورة بالإنجليزية Visual Prompt بأسلوب: {image_style}).
---IMAGE_END---
"""

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze-style', methods=['POST'])
def analyze_style():
    try:
        data = request.json
        text = data.get('text', '')
        if len(text) < 20: return jsonify({'error': 'النص قصير جداً.'}), 400
        resp = model.generate_content(f"{STYLE_ANALYZER_PROMPT}\nالنص:\n{text}")
        return jsonify({'style_dna': resp.text})
    except Exception as e: return jsonify({'error': str(e)}), 500

@app.route('/generate', methods=['POST'])
def generate():
    try:
        data = request.json
        topic = data.get('text', '')
        style_dna = data.get('style', '') or "أسلوب احترافي."
        image_style = data.get('image_style', 'Cyberpunk')

        if not topic: return jsonify({'error': 'النص فارغ!'}), 400

        # 1. الكاتب
        creator_resp = model.generate_content(CREATOR_PROMPT.format(style_dna=style_dna, topic=topic))
        draft = creator_resp.text

        # 2. الناقد
        critic_resp = model.generate_content(f"{CRITIC_PROMPT}\nالأسلوب:\n{style_dna}\nالمسودة:\n{draft}")
        feedback = critic_resp.text

        # 3. المحرر (الموزع)
        final_prompt = EDITOR_PROMPT.format(image_style=image_style) + f"\nالمسودة:\n{draft}\nالنقد:\n{feedback}"
        final_resp = model.generate_content(final_prompt)
        full_output = final_resp.text

        # تفكيك الرد الذكي (Parsing)
        def extract_section(text, start_tag, end_tag):
            try:
                return text.split(start_tag)[1].split(end_tag)[0].strip()
            except:
                return "فشل في توليد هذا القسم."

        linkedin_text = extract_section(full_output, "---LINKEDIN_START---", "---LINKEDIN_END---")
        twitter_text = extract_section(full_output, "---TWITTER_START---", "---TWITTER_END---")
        tiktok_text = extract_section(full_output, "---TIKTOK_START---", "---TIKTOK_END---")
        image_prompt = extract_section(full_output, "---IMAGE_START---", "---IMAGE_END---")
        
        # تصحيح سريع لو فشل استخراج الصورة
        if "فشل" in image_prompt or len(image_prompt) < 5:
            image_prompt = f"{image_style} illustration about {topic}"

        return jsonify({
            'linkedin': linkedin_text,
            'twitter': twitter_text,
            'tiktok': tiktok_text,
            'image_prompt': image_prompt,
            'debug': feedback
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
