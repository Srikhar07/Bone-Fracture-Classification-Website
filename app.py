import os
import numpy as np
import tensorflow as tf
from flask import Flask, render_template, request
from keras.preprocessing import image
from email_utils import send_email

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
    name = request.form.get('user_name')
    age = request.form.get('age')
    email = request.form.get('email')
    phone_number = request.form.get('phone')

    img_file = request.files.get('image')

    # -------- SAVE IMAGE --------
    img_path = os.path.join(UPLOAD_FOLDER, img_file.filename)
    img_file.save(img_path)

    # -------- PREPROCESS --------
    bone_image = image.load_img(img_path, target_size=(128, 128))
    new_image = image.img_to_array(bone_image)
    new_image = np.expand_dims(new_image, axis=0)
    new_image = new_image / 255.0
    new_image = new_image.astype(np.float32)

    # -------- PREDICT USING TFLITE --------
    interpreter.set_tensor(input_details[0]['index'], new_image)
    interpreter.invoke()
    pred = interpreter.get_tensor(output_details[0]['index'])

    # -------- RESULT --------
    if pred[0][0] < 0.5:
        result = "The bone is FRACTURED"
    else:
        result = "The bone is NORMAL"

    # -------- EMAIL --------
    try:
        send_email(
            to_email=email,
            username=name,
            age=age,
            result=result,
            image_path=img_path,
            phone_number=phone_number
        )
        status = "Email sent successfully!"
    except Exception as e:
        status = "Email sending failed."
        print(e)

    # -------- RETURN RESULT PAGE --------
    return render_template(
        'result.html',
        name=name,
        age=age,
        email=email,
        phone_number=phone_number,
        result=result,
        image_path='bone_images/' + img_file.filename,
        status=status
    )


# ---------------- RUN SERVER ----------------
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
