from fastapi import FastAPI, File, UploadFile
from flask import Flask, request, jsonify
from pydantic import BaseModel
from transformers import pipeline
from PIL import Image
import joblib
import re
import string
import io
import uvicorn
from threading import Thread

# Initialize Flask & FastAPI
app = Flask(__name__)
api = FastAPI()

# ✅ Load NSFW Image Classification Model
pipe = pipeline("image-classification", model="LukeJacob2023/nsfw-image-detector")

# ✅ Load Toxic Text Classification Model
try:
    model = joblib.load("toxic_classifier.pkl")
    vectorizer = joblib.load("vectorizer.pkl")
    print("✅ Model & Vectorizer Loaded Successfully!")
except Exception as e:
    print(f"❌ Error: {e}")
    exit(1)

# 📌 Text Input Data Model
class TextInput(BaseModel):
    text: str

# 🔹 Text Preprocessing Function
def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'\d+', '', text)  # Remove numbers
    text = text.translate(str.maketrans('', '', string.punctuation))  # Remove punctuation
    return text.strip()

# 📌 NSFW Image Classification API (Flask)
@app.route('/classify_image', methods=['POST'])
def classify_image():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['file']
    image = Image.open(io.BytesIO(file.read()))
    results = pipe(image)
    
    classification_label = max(results, key=lambda x: x['score'])['label']
    nsfw_labels = {"sexy", "porn", "hentai"}
    nsfw_status = "NSFW" if classification_label in nsfw_labels else "SFW"

    return jsonify({"status": nsfw_status, "results": results})

# 📌 Toxic Text Classification API (FastAPI)
@api.post("/classify_text/")
async def classify_text(data: TextInput):
    try:
        processed_text = preprocess_text(data.text)
        text_vectorized = vectorizer.transform([processed_text])
        prediction = model.predict(text_vectorized)
        result = "Toxic" if prediction[0] == 1 else "Safe"
        return {"prediction": result}
    except Exception as e:
        return {"error": str(e)}

# 🔥 Run both servers using Gunicorn
def run_flask():
    app.run(host="0.0.0.0", port=5000)

def run_fastapi():
    uvicorn.run(api, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    Thread(target=run_flask).start()
    Thread(target=run_fastapi).start()

