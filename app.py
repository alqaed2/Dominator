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
أنت كاتب شبحي. اكتب منشوراً بتقمص هذا الأسلوب:
{style_dna}
الموضوع: {topic}
"""

CRITIC_PROMPT = """
أنت ناقد. هل النص يطابق الأسلوب؟ وهل هو قوي؟
"""

# 🔥 تحديث المحرر لدعم الستايلات الفنية
EDITOR_PROMPT = """
أنت المدير الفني (Art Director).
مهمتك:
1. صياغة النص النهائي للنشر.
2. تصميم صورة مذهلة بالأسلوب التالي: {image_style}.

⚠️ المخرج يجب أن يكون مفصولاً بـ "---IMAGE_SPLIT---":
الجزء الأول: النص النهائي (بالعربية، منسق، إيموجي، وهاشتاغات).
---IMAGE_SPLIT---
الجزء الثاني: وصف الصورة بالإنجليزية (Visual Prompt). ركز بشدة على تطبيق أسلوب {image_style} في الوصف.
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
        # نستلم ستايل الصورة المختار
        image_style = data.get('image_style', 'Cinematic Photorealistic')

        if not topic: return jsonify({'error': 'النص فارغ!'}), 400

        # 1. الكاتب
        creator_resp = model.generate_content(CREATOR_PROMPT.format(style_dna=style_dna, topic=topic))
        draft = creator_resp.text

        # 2. الناقد
        critic_resp = model.generate_content(f"{CRITIC_PROMPT}\nالأسلوب:\n{style_dna}\nالمسودة:\n{draft}")
        feedback = critic_resp.text

        # 3. المحرر (مع ستايل الصورة)
        final_prompt = EDITOR_PROMPT.format(image_style=image_style) + f"\nالمسودة:\n{draft}\nالنقد:\n{feedback}"
        final_resp = model.generate_content(final_prompt)
        full_output = final_resp.text

        final_text = ""
        image_prompt = ""
        
        if "---IMAGE_SPLIT---" in full_output:
            parts = full_output.split("---IMAGE_SPLIT---")
            final_text = parts[0].strip()
            image_prompt = parts[1].strip()
        else:
            final_text = full_output
            image_prompt = f"{image_style} illustration about {topic}"

        return jsonify({
            'result': final_text,
            'image_prompt': image_prompt,
            'debug': feedback
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
