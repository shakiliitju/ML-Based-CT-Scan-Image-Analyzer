# ML-Based CT Scan Image Analyzer

This project is a web application for analyzing CT scan images using a machine learning model (RandomForestClassifier). It provides basic image statistics and a prediction of the image class.

## Features
- Upload CT scan images for analysis
- Basic image statistics (mean, std, edge count, etc.)
- Machine learning prediction (RandomForestClassifier)
- Educational disclaimer (not for medical use)

## Requirements
Install dependencies with:
```
pip install -r requirements.txt
```

## Usage
1. Train your model using `model.py`. The script loads images from `dataset/Data/train/<class_folder>` and saves the trained model as `model.pkl` in the project folder.
2. Start the Flask app:
```
python app.py
```
3. Open your browser and go to `http://127.0.0.1:5000/`
4. Upload a CT scan image to get analysis and prediction results.

## File Structure
- `app.py` - Main Flask application
- `model.py` - Example script to train and save a RandomForest model
- `model.pkl` - Saved trained model
- `dataset/Data/train/` - Training images organized in class folders
- `requirements.txt` - Python dependencies
- `static/` - Static files (JS, CSS)
- `templates/` - HTML templates
- `uploads/` - Uploaded images
- `test images/` - Example images for training/testing

## Disclaimer
This tool is for educational purposes only and is not intended for medical diagnosis. Always consult a qualified radiologist for medical interpretation.
