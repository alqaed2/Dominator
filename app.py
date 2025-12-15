from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import os
import re

app = Flask(__name__)

# --- إعدادات النظام من بيئة الخادم (Render) ---
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
GEMINI_MODEL = os.environ.get('GEMINI_MODEL') # الاعتماد الكلي والوحيد على هذا المتغير

# 1. التحقق الصارم: النظام لن يعمل إذا كانت المتغيرات ناقصة
if not GEMINI_API_KEY:
    raise ValueError("❌ CRITICAL ERROR: GEMINI_API_KEY is missing in environment variables.")

if not GEMINI_MODEL:
    raise ValueError("❌ CRITICAL ERROR: GEMINI_MODEL is missing in environment variables. Please add it in Render settings.")

# 2. التهيئة باستخدام المتغير فقط
try:
    genai.configure(api_key=GEMINI_API_KEY)
    
    # لا توجد قيم افتراضية هنا، نستخدم ما هو موجود في البيئة فقط
    model = genai.GenerativeModel(GEMINI_MODEL)
    
    print(f"🤖 System Online. Model Configured from Env: {GEMINI_MODEL}")

except Exception as e:
    # هذا سيمنع التطبيق من العمل إذا كان اسم الموديل في البيئة خاطئاً
    print(f"❌ Setup Error: {e}")
    raise e

# --- دوال مساعدة ---
def extract(text, start, end):
    try:
        if not text: return ""
        p = re.escape(start) + r"(.*?)" + re.escape(end)
        m = re.search(p, text, re.DOTALL)
        return m.group(1).strip() if m else ""
    except: return ""

def get_safe_response(prompt):
    """دالة آمنة لتوليد النص والتعامل مع الأخطاء"""
    try:
        response = model.generate_content(prompt)
        
        if hasattr(response, 'text') and response.text:
            return response.text
        elif hasattr(response, 'parts'):
            return response.parts[0].text
        elif hasattr(response, 'candidates'):
            return response.candidates[0].content.parts[0].text
        else:
            return "Error: Empty response from AI."
    except Exception as e:
        print(f"🔥 GEMINI ERROR: {str(e)}")
        raise e

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze-style', methods=['POST'])
def analyze_style():
    return jsonify({'style_dna': "تم التحليل بنجاح."})

# --- نقاط النهاية (Endpoints) ---

@app.route('/generate/linkedin', methods=['POST'])
def generate_linkedin():
    try:
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
        
        text_response = get_safe_response(prompt)
        
        return jsonify({
            'text': extract(text_response, "---LINKEDIN_START---", "---LINKEDIN_END---"),
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
            'text': extract(text_response, "---TWITTER_START---", "---TWITTER_END---")
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
            'text': extract(text_response, "---TIKTOK_START---", "---TIKTOK_END---"),
            'image': extract(text_response, "---TIKTOK_IMAGE_START---", "---TIKTOK_IMAGE_END---"),
            'video_prompt': extract(text_response, "---VIDEO_PROMPT_START---", "---VIDEO_PROMPT_END---")
        })

    except Exception as e:
        print(f"🔥 BACKEND ERROR (TikTok): {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
