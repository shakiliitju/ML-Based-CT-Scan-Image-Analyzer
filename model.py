
import os
import numpy as np
from PIL import Image
from sklearn.model_selection import train_test_split
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.optimizers import Adam

# Set your image directory
base_dir = 'test images'
classes = os.listdir(base_dir)


# Load images and labels for CNN
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
            arr = np.array(img) / 255.0
            X.append(arr)
            y.append(label_idx)

X = np.array(X)
y = np.array(y)
X = X.reshape(-1, img_size, img_size, 1)
y_cat = to_categorical(y, num_classes=len(classes))


# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y_cat, test_size=0.2, random_state=42)

# Build a simple CNN
model = Sequential([
    Conv2D(32, (3,3), activation='relu', input_shape=(img_size, img_size, 1)),
    MaxPooling2D(2,2),
    Conv2D(64, (3,3), activation='relu'),
    MaxPooling2D(2,2),
    Flatten(),
    Dense(128, activation='relu'),
    Dropout(0.5),
    Dense(len(classes), activation='softmax')
])
model.compile(optimizer=Adam(), loss='categorical_crossentropy', metrics=['accuracy'])

# Train model
model.fit(X_train, y_train, epochs=10, batch_size=32, validation_data=(X_test, y_test))

# Save model
model.save('model.h5')

# (Optional) Evaluate
train_loss, train_acc = model.evaluate(X_train, y_train, verbose=0)
test_loss, test_acc = model.evaluate(X_test, y_test, verbose=0)
print("Train accuracy:", train_acc)
print("Test accuracy:", test_acc)
