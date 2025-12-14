from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import os

app = Flask(__name__)

# --- إعدادات المدير التقني (Strict Mode) ---
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
GEMINI_MODEL = os.environ.get('GEMINI_MODEL') # تأكد من وجود هذا المتغير في Render بقيمة مثل gemini-1.5-flash-001

if not GEMINI_API_KEY or not GEMINI_MODEL:
    raise ValueError("❌ خطأ قاتل: تأكد من إعداد GEMINI_API_KEY و GEMINI_MODEL في Render.")

try:
    genai.configure(api_key=GEMINI_API_KEY)
    print(f"🤖 الوكالة تعمل باستخدام المحرك: {GEMINI_MODEL}")
    model = genai.GenerativeModel(GEMINI_MODEL)
except Exception as e:
    print(f"❌ خطأ في تهيئة Gemini: {e}")

# --- فريق العمل الذكي (Prompts) ---

STYLE_ANALYZER_PROMPT = """
أنت خبير لغوي. حلل النص واستخرج "البصمة الأسلوبية" (DNA):
1. النبرة (Tone). 2. هيكل الجمل. 3. المفردات.
"""

CREATOR_PROMPT = """
أنت كاتب شبحي (Ghostwriter). اكتب منشوراً جديداً بتقمص هذا الأسلوب:
{style_dna}
الموضوع: {topic}
"""

CRITIC_PROMPT = """
أنت ناقد. هل النص يطابق الأسلوب؟ وهل هو قوي؟
"""

# 🔥 التحديث الأهم: المحرر البصري
EDITOR_PROMPT = """
أنت المحرر التنفيذي ومدير الإبداع (Creative Director).
مهمتك مزدوجة:
1. صياغة النص النهائي للنشر بناءً على النقد.
2. تخيل وتصميم صورة مذهلة تناسب هذا النص.

⚠️ يجب أن يكون مخرجك يحتوي على جزئين مفصولين تماماً بواسطة الفاصل "---IMAGE_SPLIT---":

الجزء الأول: النص النهائي (بالعربية، منسق، مع إيموجي وهاشتاقات، وتوقيع: ⚡ Engineered by AI Dominator).
---IMAGE_SPLIT---
الجزء الثاني: وصف دقيق جداً للصورة باللغة الإنجليزية (Visual Prompt). صف العناصر، الإضاءة، الأسلوب (مثلاً: cinematic, photorealistic, 4k, cyberpunk style)، والألوان. اجعله وصفاً مفصلاً لمولد صور متطور.
"""

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze-style', methods=['POST'])
def analyze_style():
    try:
        data = request.json
        text_samples = data.get('text', '')
        if len(text_samples) < 20: return jsonify({'error': 'النص قصير جداً.'}), 400
        response = model.generate_content(f"{STYLE_ANALYZER_PROMPT}\n\nالنص:\n{text_samples}")
        return jsonify({'style_dna': response.text})
    except Exception as e: return jsonify({'error': str(e)}), 500

@app.route('/generate', methods=['POST'])
def generate():
    try:
        data = request.json
        topic = data.get('text', '')
        style_dna = data.get('style', '') or "أسلوب احترافي ومباشر."

        if not topic: return jsonify({'error': 'النص فارغ!'}), 400

        # 1. الكاتب
        creator_resp = model.generate_content(CREATOR_PROMPT.format(style_dna=style_dna, topic=topic))
        draft = creator_resp.text

        # 2. الناقد
        critic_resp = model.generate_content(f"{CRITIC_PROMPT}\nالأسلوب:\n{style_dna}\nالمسودة:\n{draft}")
        feedback = critic_resp.text

        # 3. المحرر (الذي يرى ويكتب)
        final_resp = model.generate_content(f"{EDITOR_PROMPT}\nالمسودة:\n{draft}\nالنقد:\n{feedback}")
        full_output = final_resp.text

        # 🔥 الذكاء في الفصل: نقسم النص عن وصف الصورة
        final_text = ""
        image_prompt = ""
        
        if "---IMAGE_SPLIT---" in full_output:
            parts = full_output.split("---IMAGE_SPLIT---")
            final_text = parts[0].strip()
            image_prompt = parts[1].strip()
        else:
            # في حال فشل الموديل في وضع الفاصل (نادر الحدوث)
            final_text = full_output
            image_prompt = f"Editorial illustration about: {topic}, high quality, 4k"

        return jsonify({
            'result': final_text,
            'image_prompt': image_prompt, # نرسل وصف الصورة للواجهة
            'debug': feedback
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
