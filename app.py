from flask import Flask, render_template, request
from base64 import b64decode, b64encode
from io import BytesIO
from PIL import Image
import numpy as np
from tensorflow import keras
import cv2

from unet_architecture.util import dice_coefficient, PSNR, SSIM

app = Flask(__name__)


@app.route('/')
def load_page():
    return render_template('index.html')


@app.route('/inpaint', methods=['POST'])
def inpaint():
    canvas_data_url = request.json['canvas']
    mask_received = canvas_data_url.split(',')[1].encode('utf-8')
    mask_received = b64decode(mask_received)

    image_data_url = request.json['original_image']
    image_received = image_data_url.split(',')[1].encode('utf-8')
    image_received = b64decode(image_received)

    left = request.json['left']
    top = request.json['top']

    final_image = Image.open(BytesIO(image_received))
    final_image = final_image.convert('RGB')
    box = (left, top, left + 64, top + 64)
    orig_image = final_image.crop(box)

    mask = Image.open(BytesIO(mask_received))
    mask_array = np.array(mask, np.uint8)
    if mask_array.shape[2] == 4:
        mask_array = cv2.cvtColor(mask_array, cv2.COLOR_BGRA2BGR)
    image_masked = cv2.bitwise_and(np.array(orig_image), np.array(mask_array))

    image_array = image_masked / 255
    model = keras.models.load_model("unet_architecture/trained_models/model_split_into_64x64",
                                    custom_objects={"dice_coefficient": dice_coefficient, "PSNR": PSNR, "SSIM": SSIM})

    inpainted_image = model.predict(image_array.reshape((1,) + image_array.shape))

    final_image = Image.open(BytesIO(image_received))
    final_image = final_image.convert('RGB')
    image_to_paste = Image.fromarray(np.uint8(255 * inpainted_image.reshape(inpainted_image.shape[1:])))
    print(final_image.size, image_to_paste.size)
    box = (left, top, left + 64, top + 64)
    final_image.paste(image_to_paste, box)

    image_buffer = BytesIO()
    final_image.save(image_buffer, format='JPEG')
    image_data = image_buffer.getvalue()
    encoded_image = b64encode(image_data).decode('utf-8')

    return {'image': encoded_image}


if __name__ == '__main__':
    from waitress import serve
    serve(app, host="0.0.0.0", port=8080)
