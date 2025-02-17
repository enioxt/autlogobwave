from flask import Flask, request, send_file
from rembg import remove
from PIL import Image
import os

app = Flask(__name__)

# Define a pasta onde os arquivos serão salvos
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/processar-imagem", methods=["POST"])
def processar_imagem():
    if "file" not in request.files:
        return {"error": "Nenhuma imagem enviada"}, 400

    file = request.files["file"]
    
    # Caminho para salvar a imagem original
    input_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(input_path)

    # Caminho para salvar a imagem processada
    output_path = os.path.join(UPLOAD_FOLDER, "logomarca_final.png")
    processar_logo(input_path, output_path)

    return send_file(output_path, mimetype="image/png")

def processar_logo(input_path, output_path):
    # Remover fundo
    with open(input_path, "rb") as inp_file:
        input_data = inp_file.read()
        output_data = remove(input_data)

    # Salvar sem fundo
    with open(output_path, "wb") as out_file:
        out_file.write(output_data)

    # Redimensionar mantendo a proporção
    template_size = (550, 150)
    image = Image.open(output_path)
    image.thumbnail(template_size, Image.ANTIALIAS)
    image.save(output_path)

# Corrigindo a porta para o Railway
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Obtém a porta do Railway ou usa 5000 por padrão
    app.run(host="0.0.0.0", port=port)
