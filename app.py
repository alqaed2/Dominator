from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import os
import re # إضافة مكتبة التعامل مع النصوص

app = Flask(__name__)

# --- إعدادات المدير التقني ---
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
GEMINI_MODEL = os.environ.get('GEMINI_MODEL')

if not GEMINI_API_KEY or not GEMINI_MODEL:
    raise ValueError("❌ خطأ قاتل: تأكد من المتغيرات البيئية في Render.")

try:
    genai.configure(api_key=GEMINI_API_KEY)
    print(f"🤖 النظام V10 يعمل بمحرك: {GEMINI_MODEL}")
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
مهمتك: توليد أفكار حملة لمنصات متعددة بناءً على الفكرة، مع تقمص الأسلوب: {style_dna}
الموضوع: {topic}
"""

CRITIC_PROMPT = """
أنت ناقد. هل الأفكار قوية وتناسب كل منصة؟ هل التسلسل البصري المقترح للفيديو منطقي؟
"""

# 🔥 التحديث الأضخم: المحرر السينمائي الشامل (V10)
EDITOR_PROMPT = """
أنت رئيس تحرير ومخرج سينمائي (Editor-in-Chief & Film Director).
مهمتك تحويل المسودة إلى حملة متكاملة، بما في ذلك قصة مصورة (Storyboard) وبرومبت فيديو.

⚠️ يجب أن يكون المخرج مقسماً بدقة متناهية باستخدام الفواصل التالية:

---LINKEDIN_START---
(مقال LinkedIn الاحترافي)
---LINKEDIN_END---

---TWITTER_START---
(ثريد X المكون من 5-7 تغريدات)
---TWITTER_END---

---TIKTOK_START---
(سكريبت TikTok النصي: المشهد، الصوت، النص على الشاشة)
---TIKTOK_END---

---IMAGE_MAIN_START---
(وصف الصورة الرئيسية للمقال بالإنجليزية بأسلوب {image_style})
---IMAGE_MAIN_END---

---STORYBOARD_IMG1_START---
(وصف إنجليزي للمشهد الأول من الفيديو: الـ Hook/البداية الخاطفة. بأسلوب {image_style})
---STORYBOARD_IMG1_END---

---STORYBOARD_IMG2_START---
(وصف إنجليزي للمشهد الثاني: الوسط/شرح القيمة. بأسلوب {image_style})
---STORYBOARD_IMG2_END---

---STORYBOARD_IMG3_START---
(وصف إنجليزي للمشهد الثالث: النهاية/Call to Action قوي. بأسلوب {image_style})
---STORYBOARD_IMG3_END---

---VIDEO_PROMPT_START---
(برومبت فيديو احترافي بالإنجليزية [Cinematic Video Prompt] يصف حركة الكاميرا والمشهد كاملاً، جاهز للاستخدام في أدوات مثل Sora/Veo/Runway. صف الأجواء والحركة بدقة.)
---VIDEO_PROMPT_END---
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

# دالة مساعدة لاستخراج الأقسام بدقة باستخدام Regular Expressions
def extract_section(text, start_tag, end_tag):
    try:
        pattern = re.escape(start_tag) + r"(.*?)" + re.escape(end_tag)
        match = re.search(pattern, text, re.DOTALL)
        return match.group(1).strip() if match else "Generating..."
    except:
        return "Error fetching section."

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

        # 3. المحرر السينمائي (V10)
        final_prompt = EDITOR_PROMPT.format(image_style=image_style) + f"\nالمسودة:\n{draft}\nالنقد:\n{feedback}"
        final_resp = model.generate_content(final_prompt)
        full_output = final_resp.text

        # استخراج الـ 8 أقسام المختلفة!
        results = {
            'linkedin': extract_section(full_output, "---LINKEDIN_START---", "---LINKEDIN_END---"),
            'twitter': extract_section(full_output, "---TWITTER_START---", "---TWITTER_END---"),
            'tiktok': extract_section(full_output, "---TIKTOK_START---", "---TIKTOK_END---"),
            'image_main': extract_section(full_output, "---IMAGE_MAIN_START---", "---IMAGE_MAIN_END---"),
            'story_img1': extract_section(full_output, "---STORYBOARD_IMG1_START---", "---STORYBOARD_IMG1_END---"),
            'story_img2': extract_section(full_output, "---STORYBOARD_IMG2_START---", "---STORYBOARD_IMG2_END---"),
            'story_img3': extract_section(full_output, "---STORYBOARD_IMG3_START---", "---STORYBOARD_IMG3_END---"),
            'video_prompt': extract_section(full_output, "---VIDEO_PROMPT_START---", "---VIDEO_PROMPT_END---"),
            'debug': feedback
        }

        # التأكد من وجود وصف للصور في حال فشل الاستخراج
        fallback_prompt = f"{image_style} illustration about {topic}"
        if len(results['image_main']) < 5: results['image_main'] = fallback_prompt
        if len(results['story_img1']) < 5: results['story_img1'] = fallback_prompt + " scene 1 start"
        if len(results['story_img2']) < 5: results['story_img2'] = fallback_prompt + " scene 2 middle"
        if len(results['story_img3']) < 5: results['story_img3'] = fallback_prompt + " scene 3 end"

        return jsonify(results)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
