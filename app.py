
import os
from PIL import Image
import cv2
import numpy as np
from flask import Flask, request, render_template, jsonify
import joblib

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)



# Load the trained RandomForest model
MODEL_PATH = 'model.pkl'
model = joblib.load(MODEL_PATH)



def preprocess_image_for_model(image_path):
    # For RandomForest: grayscale, resize, flatten, normalize
    img = Image.open(image_path).convert('L')
    img = img.resize((128, 128))
    arr = np.array(img).flatten() / 255.0
    return arr.reshape(1, -1)

def basic_ct_analysis(image_path):
    """
    EDUCATIONAL PURPOSES ONLY - NOT FOR MEDICAL DIAGNOSIS
    This is a basic image analysis demonstration
    """
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    
    # Basic image statistics
    mean_intensity = np.mean(image)
    std_intensity = np.std(image)
    
    # Edge detection for structural analysis
    edges = cv2.Canny(image, 100, 200)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Simple brightness/darkness analysis
    dark_regions = np.sum(image < 50)  # Very dark pixels
    bright_regions = np.sum(image > 200)  # Very bright pixels
    
    # Basic "analysis" (NOT medical diagnosis)
    findings = []
    
    if std_intensity > 60:
        findings.append("High contrast regions detected (could indicate structural variations)")
    
    if len(contours) > 100:
        findings.append("Multiple edge structures detected")
    
    if dark_regions > (image.size * 0.3):
        findings.append("Significant dark regions present")
    
    if bright_regions > (image.size * 0.1):
        findings.append("High-density regions detected (possible bone/contrast material)")
    
    # Always include disclaimer
    findings.append("⚠️ IMPORTANT: This is NOT a medical diagnosis!")
    findings.append("⚠️ Consult a qualified radiologist for proper interpretation!")
    
    return {
        'mean_intensity': float(mean_intensity),
        'std_intensity': float(std_intensity),
        'edge_count': len(contours),
        'findings': findings,
        'disclaimer': 'FOR EDUCATIONAL PURPOSES ONLY - NOT FOR MEDICAL USE'
    }

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    try:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)

        # Basic CT analysis (educational only)
        analysis = basic_ct_analysis(filepath)

        # Model prediction


        img_arr = preprocess_image_for_model(filepath)
        prediction = model.predict(img_arr)
        prediction_label = str(prediction[0])

        return jsonify({
            'analysis': analysis,
            'model_prediction': prediction_label
        })

    except Exception as e:
        import traceback
        print(traceback.format_exc())
        return jsonify({'error': f'Error: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)
