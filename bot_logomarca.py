from flask import Flask, request, send_file
from rembg import remove
from PIL import Image
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/processar-imagem", methods=["POST"])
def processar_imagem():
    if "file" not in request.files:
        return {"error": "Nenhuma imagem enviada"}, 400

    file = request.files["file"]
    input_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(input_path)

    output_path = os.path.join(UPLOAD_FOLDER, "logomarca_final.png")
    processar_logo(input_path, output_path)

    return send_file(output_path, mimetype="image/png")

def processar_logo(input_path, output_path):
    with open(input_path, "rb") as inp_file:
        input_data = inp_file.read()
        output_data = remove(input_data)

    with open(output_path, "wb") as out_file:
        out_file.write(output_data)

    template_size = (550, 150)
    image = Image.open(output_path)
    image.thumbnail(template_size, Image.ANTIALIAS)
    image.save(output_path)

if __name__ == "__main__":
    import os
port = int(os.environ.get("PORT", 5000))
app.run(host="0.0.0.0", port=port)

