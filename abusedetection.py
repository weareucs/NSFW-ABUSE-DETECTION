import requests
import json

# 🔹 Replace with your actual Ngrok URLs from Colab output
#IMAGE_API_URL = "https://ef0d-35-194-65-23.ngrok-free.app/classify_image"
TEXT_API_URL = "https://8db8-35-194-65-23.ngrok-free.app/classify_text/"



# ✅ Test Image Classification
#def test_image(image_path):
#    files = {'file': open(image_path, 'rb')}
#    response = requests.post(IMAGE_API_URL, files=files)
#    
#    if response.status_code == 200:
#        result = response.json()
#        print("\n🔍 **Image Classification Result**")
#        print("📂 **File**:", image_path)
#        print("📜 **Status**:", result['status'])
#        print("\n📊 **Detailed Scores**:")
#        for res in result["results"]:
#            print(f"  🔹 {res['label'].capitalize()}: {res['score']:.4f}")
#    else:
#        print("\n❌ **Image Classification Failed!**")
#        print(response.text)



# ✅ Test Text Classification
def test_text(input_text):
    response = requests.post(TEXT_API_URL, json={"text": input_text})
    
    if response.status_code == 200:
        result = response.json()
        print("\n🔍 **Text Classification Result**")
        print("📝 **Text**:", input_text)
        print("⚠️ **Prediction**:", result['prediction'])
    else:
        print("\n❌ **Text Classification Failed!**")
        print(response.text)

# 🔥 Run Tests
#test_image("test_image1.jpg")  # Replace with your image file
test_text("hello bitch")  # Replace with your text input

