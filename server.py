from flask import Flask, request, jsonify
from PIL import Image
from io import BytesIO
import requests
import base64

app = Flask(__name__)

@app.route('/edit', methods=['POST'])
def edit_image():
    data = request.json
    profile_url = data['url']

    # Unduh gambar profil
    response = requests.get(profile_url)
    img = Image.open(BytesIO(response.content)).convert("RGBA")

    # Muat overlay mask
    mask_response = requests.get('https://raw.githubusercontent.com/username/image-editor-bot/main/mask.png')
    mask = Image.open(BytesIO(mask_response.content)).convert("RGBA")
    mask = mask.resize(img.size, Image.ANTIALIAS)

    # Gabungkan gambar
    edited_img = Image.alpha_composite(img, mask)

    # Simpan sebagai base64
    buffered = BytesIO()
    edited_img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()

    return jsonify({"image": f"data:image/png;base64,{img_str}"})

if __name__ == '__main__':
    app.run()
