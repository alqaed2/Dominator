from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import os
import re

app = Flask(__name__)

# إعدادات النظام
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
GEMINI_MODEL = os.environ.get('GEMINI_MODEL')

if not GEMINI_API_KEY:
    print("❌ Error: Missing API Key.")

try:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel(GEMINI_MODEL or "gemini-1.5-flash")
except Exception as e:
    print(f"❌ Setup Error: {e}")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze-style', methods=['POST'])
def analyze_style():
    return jsonify({'style_dna': "تم التحليل."})

def extract(text, start, end):
    try:
        p = re.escape(start) + r"(.*?)" + re.escape(end)
        m = re.search(p, text, re.DOTALL)
        return m.group(1).strip() if m else ""
    except: return ""

# --- المسارات المنفصلة (السر وراء السرعة والاستقرار) ---

@app.route('/generate/linkedin', methods=['POST'])
def generate_linkedin():
    try:
        data = request.json
        prompt = f"""
        Act as a LinkedIn Expert. Write a viral post about: {data['topic']}
        Style: {data['style_dna']}
        Image Style: {data['image_style']}
        
        Output format:
        ---LINKEDIN_START---
        (Post content here)
        ---LINKEDIN_END---
        ---IMAGE_MAIN_START---
        (English image description)
        ---IMAGE_MAIN_END---
        """
        resp = model.generate_content(prompt)
        return jsonify({
            'text': extract(resp.text, "---LINKEDIN_START---", "---LINKEDIN_END---"),
            'image': extract(resp.text, "---IMAGE_MAIN_START---", "---IMAGE_MAIN_END---")
        })
    except Exception as e: return jsonify({'error': str(e)}), 500

@app.route('/generate/twitter', methods=['POST'])
def generate_twitter():
    try:
        data = request.json
        prompt = f"""
        Act as a Twitter Expert. Write a 5-tweet thread about: {data['topic']}
        Style: {data['style_dna']}
        
        Output format:
        ---TWITTER_START---
        (Thread content here)
        ---TWITTER_END---
        """
        resp = model.generate_content(prompt)
        return jsonify({
            'text': extract(resp.text, "---TWITTER_START---", "---TWITTER_END---")
        })
    except Exception as e: return jsonify({'error': str(e)}), 500

@app.route('/generate/tiktok', methods=['POST'])
def generate_tiktok():
    try:
        data = request.json
        prompt = f"""
        Act as a TikTok Director. Write a script about: {data['topic']}
        Style: {data['style_dna']}
        Image Style: {data['image_style']}
        
        Output format:
        ---TIKTOK_START---
        (Script content)
        ---TIKTOK_END---
        ---TIKTOK_IMAGE_START---
        (One English image prompt for cover)
        ---TIKTOK_IMAGE_END---
        ---VIDEO_PROMPT_START---
        (Video generation prompt)
        ---VIDEO_PROMPT_END---
        """
        resp = model.generate_content(prompt)
        return jsonify({
            'text': extract(resp.text, "---TIKTOK_START---", "---TIKTOK_END---"),
            'image': extract(resp.text, "---TIKTOK_IMAGE_START---", "---TIKTOK_IMAGE_END---"),
            'video_prompt': extract(resp.text, "---VIDEO_PROMPT_START---", "---VIDEO_PROMPT_END---")
        })
    except Exception as e: return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
