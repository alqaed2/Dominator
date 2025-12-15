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

# --- أوامر متخصصة وسريعة (Specialized Prompts) ---

LINKEDIN_PROMPT = """
بصفتك خبير LinkedIn، اكتب مقالاً احترافياً وتفاعلياً.
الموضوع: {topic}
الأسلوب: {style_dna}
النمط البصري للصورة: {image_style}

المخرجات المطلوبة (التزم بالفواصل):
---LINKEDIN_START---
(نص المقال هنا)
---LINKEDIN_END---

---IMAGE_MAIN_START---
(وصف إنجليزي للصورة الرئيسية: {image_style})
---IMAGE_MAIN_END---
"""

TWITTER_PROMPT = """
بصفتك خبير X (Twitter)، اكتب ثريد فيروسي (Viral Thread).
الموضوع: {topic}
الأسلوب: {style_dna}

المخرجات المطلوبة:
---TWITTER_START---
(5-7 تغريدات مرقمة وجذابة)
---TWITTER_END---
"""

TIKTOK_PROMPT = """
بصفتك مخرج سينمائي، اكتب سكريبت TikTok وقصة مصورة.
الموضوع: {topic}
الأسلوب: {style_dna}
النمط البصري: {image_style}

المخرجات المطلوبة:
---TIKTOK_START---
(السكريبت النصي: المشهد، الصوت)
---TIKTOK_END---

---STORYBOARD_IMG1_START---
(وصف مشهد 1 إنجليزي: {image_style})
---STORYBOARD_IMG1_END---

---STORYBOARD_IMG2_START---
(وصف مشهد 2 إنجليزي: {image_style})
---STORYBOARD_IMG2_END---

---STORYBOARD_IMG3_START---
(وصف مشهد 3 إنجليزي: {image_style})
---STORYBOARD_IMG3_END---

---VIDEO_PROMPT_START---
(Detailed Cinematic Video Prompt in English)
---VIDEO_PROMPT_END---
"""

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze-style', methods=['POST'])
def analyze_style():
    return jsonify({'style_dna': "تم تفعيل تحليل النمط."})

def extract(text, start, end):
    try:
        p = re.escape(start) + r"(.*?)" + re.escape(end)
        m = re.search(p, text, re.DOTALL)
        return m.group(1).strip() if m else "Generating..."
    except: return "Error"

# --- 3 مسارات منفصلة (API Endpoints) ---

@app.route('/generate/linkedin', methods=['POST'])
def generate_linkedin():
    try:
        data = request.json
        resp = model.generate_content(LINKEDIN_PROMPT.format(**data))
        return jsonify({
            'text': extract(resp.text, "---LINKEDIN_START---", "---LINKEDIN_END---"),
            'image': extract(resp.text, "---IMAGE_MAIN_START---", "---IMAGE_MAIN_END---")
        })
    except Exception as e: return jsonify({'error': str(e)}), 500

@app.route('/generate/twitter', methods=['POST'])
def generate_twitter():
    try:
        data = request.json
        resp = model.generate_content(TWITTER_PROMPT.format(**data))
        return jsonify({
            'text': extract(resp.text, "---TWITTER_START---", "---TWITTER_END---")
        })
    except Exception as e: return jsonify({'error': str(e)}), 500

@app.route('/generate/tiktok', methods=['POST'])
def generate_tiktok():
    try:
        data = request.json
        resp = model.generate_content(TIKTOK_PROMPT.format(**data))
        txt = resp.text
        return jsonify({
            'text': extract(txt, "---TIKTOK_START---", "---TIKTOK_END---"),
            'img1': extract(txt, "---STORYBOARD_IMG1_START---", "---STORYBOARD_IMG1_END---"),
            'img2': extract(txt, "---STORYBOARD_IMG2_START---", "---STORYBOARD_IMG2_END---"),
            'img3': extract(txt, "---STORYBOARD_IMG3_START---", "---STORYBOARD_IMG3_END---"),
            'video_prompt': extract(txt, "---VIDEO_PROMPT_START---", "---VIDEO_PROMPT_END---")
        })
    except Exception as e: return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
