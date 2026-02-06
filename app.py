import os
import numpy as np
import tensorflow as tf
from flask import Flask, render_template, request
from keras.preprocessing import image

# ---------------- PATH SETUP ----------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(BASE_DIR, "model", "bone_feature.tflite")
UPLOAD_FOLDER = os.path.join(BASE_DIR, "static", "bone_images")

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ---------------- LOAD TFLITE MODEL ----------------
interpreter = tf.lite.Interpreter(model_path=MODEL_PATH)
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# ---------------- FLASK APP ----------------
app = Flask(__name__)


@app.route('/')
def home_page():
    return render_template('home.html')


@app.route('/predict', methods=['POST'])
def prediction():
    try:
        name = request.form.get('user_name')
        age = request.form.get('age')
        phone_number = request.form.get('phone')

        img_file = request.files.get('image')

        if img_file is None or img_file.filename == "":
            return "No image uploaded", 400

        # -------- SAVE IMAGE --------
        img_path = os.path.join(UPLOAD_FOLDER, img_file.filename)
        img_file.save(img_path)

        # -------- PREPROCESS --------
        bone_image = image.load_img(img_path, target_size=(128, 128))
        new_image = image.img_to_array(bone_image)
        new_image = np.expand_dims(new_image, axis=0)
        new_image = new_image / 255.0
        new_image = new_image.astype(np.float32)

        # -------- PREDICTION --------
        interpreter.set_tensor(input_details[0]['index'], new_image)
        interpreter.invoke()
        pred = interpreter.get_tensor(output_details[0]['index'])

        if pred[0][0] < 0.5:
            result = "The bone is FRACTURED"
        else:
            result = "The bone is NORMAL"

        # -------- RETURN RESULT --------
        return render_template(
            'result.html',
            name=name,
            age=age,
            phone_number=phone_number,
            result=result,
            image_path='bone_images/' + img_file.filename
        )

    except Exception as e:
        print("Prediction error:", e)
        return "Internal Server Error", 500


# ---------------- RUN SERVER ----------------
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
