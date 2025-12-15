from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import os
import re

app = Flask(__name__)

# --- إعدادات النظام من بيئة الخادم (Render) ---
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
GEMINI_MODEL = os.environ.get('GEMINI_MODEL') # الاعتماد الكلي على المتغير

# التحقق من المتغيرات
if not GEMINI_API_KEY:
    print("❌ CRITICAL ERROR: GEMINI_API_KEY is missing in environment variables.")
if not GEMINI_MODEL:
    print("⚠️ WARNING: GEMINI_MODEL is missing. Defaulting to gemini-1.5-flash if available.")

try:
    genai.configure(api_key=GEMINI_API_KEY)
    # استخدام الموديل من البيئة فقط
    model_name = GEMINI_MODEL if GEMINI_MODEL else "gemini-1.5-flash"
    model = genai.GenerativeModel(model_name)
    print(f"🤖 System Online. Using Model from Env: {model_name}")
except Exception as e:
    print(f"❌ Setup Error: {e}")

# --- دوال مساعدة ---
def extract(text, start, end):
    try:
        if not text: return ""
        p = re.escape(start) + r"(.*?)" + re.escape(end)
        m = re.search(p, text, re.DOTALL)
        return m.group(1).strip() if m else ""
    except: return ""

def get_safe_response(prompt):
    """دالة آمنة جداً لتوليد النص والتعامل مع الأخطاء"""
    try:
        response = model.generate_content(prompt)
        
        # محاولة استخراج النص بعدة طرق لتجنب الانهيار
        if hasattr(response, 'text') and response.text:
            return response.text
        elif hasattr(response, 'parts'):
            return response.parts[0].text
        elif hasattr(response, 'candidates'):
            return response.candidates[0].content.parts[0].text
        else:
            return "Error: Empty response from AI."
    except Exception as e:
        # طباعة الخطأ في السيرفر للمراقبة
        print(f"🔥 GEMINI ERROR: {str(e)}")
        # إعادة رفع الخطأ ليتم التقاطه في الدالة الرئيسية
        raise e

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze-style', methods=['POST'])
def analyze_style():
    return jsonify({'style_dna': "تم التحليل بنجاح."})

# --- نقاط النهاية المحصنة (Fortified Endpoints) ---

@app.route('/generate/linkedin', methods=['POST'])
def generate_linkedin():
    try:
        # 1. استقبال البيانات بأمان
        data = request.get_json(silent=True)
        if not data or 'text' not in data:
            return jsonify({"error": "No data provided"}), 400
            
        topic = data['text']
        style = data.get('style_dna', 'Professional')
        image_style = data.get('image_style', 'Corporate')

        prompt = f"""
        Act as a LinkedIn Expert. Write a viral post about: {topic}
        Style: {style}
        Image Style: {image_style}
        
        OUTPUT FORMAT:
        ---LINKEDIN_START---
        (Content)
        ---LINKEDIN_END---
        ---IMAGE_MAIN_START---
        (Image Prompt)
        ---IMAGE_MAIN_END---
        """
        
        # 2. التوليد الآمن
        text_response = get_safe_response(prompt)
        
        return jsonify({
            'text': extract(text_response, "---LINKEDIN_START---", "---LINKEDIN_END---") or "Failed to generate text",
            'image': extract(text_response, "---IMAGE_MAIN_START---", "---IMAGE_MAIN_END---")
        })

    except Exception as e:
        print(f"🔥 BACKEND ERROR (LinkedIn): {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/generate/twitter', methods=['POST'])
def generate_twitter():
    try:
        data = request.get_json(silent=True)
        if not data or 'text' not in data:
            return jsonify({"error": "No data provided"}), 400

        topic = data['text']
        style = data.get('style_dna', 'Viral')

        prompt = f"""
        Act as a Twitter Expert. Write a 5-tweet thread about: {topic}
        Style: {style}
        
        OUTPUT FORMAT:
        ---TWITTER_START---
        (Thread content)
        ---TWITTER_END---
        """
        
        text_response = get_safe_response(prompt)
        
        return jsonify({
            'text': extract(text_response, "---TWITTER_START---", "---TWITTER_END---") or "Failed to generate thread"
        })

    except Exception as e:
        print(f"🔥 BACKEND ERROR (Twitter): {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/generate/tiktok', methods=['POST'])
def generate_tiktok():
    try:
        data = request.get_json(silent=True)
        if not data or 'text' not in data:
            return jsonify({"error": "No data provided"}), 400

        topic = data['text']
        style = data.get('style_dna', 'Engaging')
        image_style = data.get('image_style', 'Cyberpunk')

        prompt = f"""
        Act as a TikTok Director. Write a script for: {topic}
        Style: {style}
        Image Style: {image_style}
        
        OUTPUT FORMAT:
        ---TIKTOK_START---
        (Script)
        ---TIKTOK_END---
        ---TIKTOK_IMAGE_START---
        (Cover Image Prompt)
        ---TIKTOK_IMAGE_END---
        ---VIDEO_PROMPT_START---
        (Video Gen Prompt)
        ---VIDEO_PROMPT_END---
        """
        
        text_response = get_safe_response(prompt)
        
        return jsonify({
            'text': extract(text_response, "---TIKTOK_START---", "---TIKTOK_END---") or "Failed to generate script",
            'image': extract(text_response, "---TIKTOK_IMAGE_START---", "---TIKTOK_IMAGE_END---"),
            'video_prompt': extract(text_response, "---VIDEO_PROMPT_START---", "---VIDEO_PROMPT_END---")
        })

    except Exception as e:
        print(f"🔥 BACKEND ERROR (TikTok): {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
