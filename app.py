from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import os

app = Flask(__name__)

# قراءة مفتاح Gemini من متغيرات البيئة
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
else:
    print("⚠️ GEMINI_API_KEY غير مضبوط – سيتم رفض الطلبات")

# اختيار نموذج مدعوم رسميًا من القائمة المتاحة
MODEL_NAME = "models/gemini-2.5-flash"
model = genai.GenerativeModel(MODEL_NAME)

SYSTEM_PROMPT = """
أنت خبير محتوى فيروسي (Viral Content Expert).
مهمتك إعادة صياغة النص ليناسب LinkedIn و X.

القواعد:
1. ابدأ بـ Hook قوي.
2. فقرات قصيرة وسهلة القراءة.
3. استخدم Emojis بذكاء.
4. أضف هاشتاغات مناسبة في النهاية.
5. أضف التوقيع: ⚡ Remixed by AI Dominator
"""

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    if not GEMINI_API_KEY:
        return jsonify({"error": "GEMINI_API_KEY غير مضبوط"}), 500

    data = request.get_json(silent=True) or {}
    original_text = data.get("text", "").strip()

    if not original_text:
        return jsonify({"error": "النص فارغ"}), 400

    full_prompt = f"{SYSTEM_PROMPT}\n\nالنص المراد إعادة صياغته:\n{original_text}"

    try:
        response = model.generate_content(full_prompt)
        return jsonify({"result": response.text})
    except Exception as e:
        print("❌ Gemini Error:", e)
        return jsonify({"error": "فشل توليد المحتوى"}), 500


if __name__ == "__main__":
    app.run(port=5000)
