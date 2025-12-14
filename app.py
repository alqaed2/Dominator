from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import os

app = Flask(__name__)

# --- إعدادات المدير التقني (Strict Mode) ---

# 1. جلب المفتاح
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')

# 2. جلب اسم الموديل (إجباري)
GEMINI_MODEL = os.environ.get('GEMINI_MODEL')

# التحقق الصارم: إذا لم توجد المتغيرات، أوقف النظام فوراً
if not GEMINI_API_KEY:
    raise ValueError("❌ خطأ قاتل: مفتاح GEMINI_API_KEY غير موجود في متغيرات البيئة!")

if not GEMINI_MODEL:
    raise ValueError("❌ خطأ قاتل: لم تحدد الموديل! يجب إضافة متغير GEMINI_MODEL في إعدادات Render.")

try:
    genai.configure(api_key=GEMINI_API_KEY)
    print(f"🤖 النظام يعمل الآن باستخدام الموديل المحدد: {GEMINI_MODEL}")
    # استخدام الموديل المحدد في المتغير حصراً
    model = genai.GenerativeModel(GEMINI_MODEL)
    
except Exception as e:
    print(f"❌ خطأ في تهيئة Gemini: {e}")

# --- عقل النظام (Prompts) ---

STYLE_ANALYZER_PROMPT = """
أنت خبير لغوي. حلل النص واستخرج "البصمة الأسلوبية" (DNA):
1. النبرة (Tone). 2. هيكل الجمل. 3. المفردات.
أعطني ملخصاً دقيقاً لكي يتقمصه كاتب آخر.
"""

CREATOR_PROMPT = """
أنت كاتب شبحي (Ghostwriter). اكتب منشوراً جديداً بتقمص هذا الأسلوب:
{style_dna}
الموضوع: {topic}
"""

CRITIC_PROMPT = """
أنت ناقد محتوى. هل النص المكتوب يطابق الأسلوب المطلوب؟ وهل هو جذاب؟
أعطِ تقييماً وتوجيهات للتحسين.
"""

EDITOR_PROMPT = """
أنت المحرر النهائي. صغ النص النهائي للنشر بناءً على النقد.
أضف التوقيع: ⚡ Engineered by AI Dominator
"""

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze-style', methods=['POST'])
def analyze_style():
    try:
        data = request.json
        text_samples = data.get('text', '')
        
        if len(text_samples) < 20:
             return jsonify({'error': 'النص قصير جداً للتحليل.'}), 400
        
        response = model.generate_content(f"{STYLE_ANALYZER_PROMPT}\n\nالنص:\n{text_samples}")
        return jsonify({'style_dna': response.text})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/generate', methods=['POST'])
def generate():
    try:
        data = request.json
        topic = data.get('text', '')
        style_dna = data.get('style', '')

        if not topic:
            return jsonify({'error': 'النص فارغ!'}), 400

        if not style_dna:
            style_dna = "أسلوب احترافي ومباشر."

        # 1. الكاتب
        creator_resp = model.generate_content(CREATOR_PROMPT.format(style_dna=style_dna, topic=topic))
        draft = creator_resp.text

        # 2. الناقد
        critic_resp = model.generate_content(f"{CRITIC_PROMPT}\nالأسلوب:\n{style_dna}\nالمسودة:\n{draft}")
        feedback = critic_resp.text

        # 3. المحرر
        final_resp = model.generate_content(f"{EDITOR_PROMPT}\nالمسودة:\n{draft}\nالنقد:\n{feedback}")
        
        return jsonify({
            'result': final_resp.text,
            'debug': feedback
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
