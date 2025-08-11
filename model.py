import os
import numpy as np
from PIL import Image
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib

# Set your image directory
base_dir = 'dataset/Data/train'
classes = os.listdir(base_dir)



# Load images and labels for Logistic Regression
X = []
y = []
img_size = 128
for label_idx, label in enumerate(classes):
    class_dir = os.path.join(base_dir, label)
    if not os.path.isdir(class_dir):
        continue
    for fname in os.listdir(class_dir):
        if fname.endswith('.png'):
            img_path = os.path.join(class_dir, fname)
            img = Image.open(img_path).convert('L').resize((img_size, img_size))
            arr = np.array(img).flatten() / 255.0
            X.append(arr)
            y.append(label_idx)

X = np.array(X)
y = np.array(y)

print("X shape:", getattr(X, "shape", len(X)))
print("y shape:", getattr(y, "shape", len(y)))

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


# Train Random Forest model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Save model
joblib.dump(model, 'model.pkl')

# (Optional) Evaluate
print("Train accuracy:", model.score(X_train, y_train))
print("Test accuracy:", model.score(X_test, y_test))
