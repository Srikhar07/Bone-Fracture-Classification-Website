import os
import numpy as np
from flask import Flask, render_template, request
from tensorflow.keras.models import load_model
from keras.preprocessing import image
from email_utils import send_email

# -------------------- PATH SETUP --------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(BASE_DIR, "model", "bone_feature.h5")
UPLOAD_FOLDER = os.path.join(BASE_DIR, "static", "bone_images")

# create folder if not exists (important for Railway)
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# -------------------- LOAD MODEL --------------------
model = load_model(MODEL_PATH)

# -------------------- FLASK APP --------------------
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

    # Save uploaded image
    img_path = os.path.join(UPLOAD_FOLDER, img_file.filename)
    img_file.save(img_path)

    # -------------------- PREPROCESS --------------------
    bone_image = image.load_img(img_path, target_size=(128, 128))
    new_image = image.img_to_array(bone_image)
    new_image = np.expand_dims(new_image, axis=0)
    new_image = new_image / 255.0

    # -------------------- PREDICTION --------------------
    pred = model.predict(new_image)

    if pred[0][0] < 0.5:
        result = "The bone is FRACTURED"
    else:
        result = "The bone is NORMAL"

    # -------------------- EMAIL --------------------
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


# -------------------- RUN SERVER --------------------
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
