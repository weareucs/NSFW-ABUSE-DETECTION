#from transformers import pipeline, AutoImageProcessor, AutoModelForImageClassification
from transformers import pipeline, ViTImageProcessor, AutoModelForImageClassification
from PIL import Image
import torch

# Initialize pipeline
def classify_image_pipeline(image_path):
    pipe = pipeline("image-classification", model="LukeJacob2023/nsfw-image-detector")
    image = Image.open(image_path)
    results = pipe(image)
    return results

# Load model directly
def classify_image_direct(image_path):
#    processor = AutoImageProcessor.from_pretrained("LukeJacob2023/nsfw-image-detector")
    processor = ViTImageProcessor.from_pretrained("LukeJacob2023/nsfw-image-detector")
    model = AutoModelForImageClassification.from_pretrained("LukeJacob2023/nsfw-image-detector")
    
    
    image = Image.open(image_path)
    inputs = processor(image, return_tensors="pt")
    with torch.no_grad():
        outputs = model(**inputs)
    logits = outputs.logits
    predicted_class = torch.argmax(logits, dim=-1).item()
    
    return predicted_class

# Example usage
image_path = "test_image2.jpg"  # Replace with your image file
pipeline_results = classify_image_pipeline(image_path)
direct_results = classify_image_direct(image_path)

# Print results only
for result in pipeline_results:
    print(f"{result['label']}: {result['score']:.10f}")

# Determine NSFW or SFW based on classification
nsfw_labels = {"sexy", "porn", "hentai"}
classification_label = max(pipeline_results, key=lambda x: x['score'])['label']
nsfw_status = "NSFW" if classification_label in nsfw_labels else "SFW"

print(f"Class Index: {direct_results}")
print(f"Content Type: {nsfw_status}")

