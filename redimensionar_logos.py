from PIL import Image
import os

def redimensionar_logo(caminho_entrada, caminho_saida, largura_max=550, altura_max=150):
    try:
        # Abrir a imagem
        print(f"Processando: {caminho_entrada}")
        imagem = Image.open(caminho_entrada)

        # Calcular novas dimensões mantendo a proporção
        largura_original, altura_original = imagem.size
        razao = min(largura_max / largura_original, altura_max / altura_original)
        nova_largura = int(largura_original * razao)
        nova_altura = int(altura_original * razao)

        # Redimensionar a imagem
        imagem_redimensionada = imagem.resize((nova_largura, nova_altura), Image.LANCZOS)

        # Salvar a imagem em PNG
        imagem_redimensionada.save(caminho_saida, 'PNG')
        print(f"Imagem redimensionada e salva com sucesso: {caminho_saida}")

    except Exception as e:
        print(f"Erro ao processar {caminho_entrada}: {str(e)}")

def processar_arquivos():
    pasta_entrada = "logos_originais"
    pasta_saida = "logos_processadas"

    # Criar pasta de saída se não existir
    os.makedirs(pasta_saida, exist_ok=True)

    # Processar todas as imagens na pasta de entrada
    for nome_arquivo in os.listdir(pasta_entrada):
        if nome_arquivo.lower().endswith(('.png', '.jpg', '.jpeg')):
            caminho_entrada = os.path.join(pasta_entrada, nome_arquivo)
            caminho_saida = os.path.join(pasta_saida, f"processado_{nome_arquivo.split('.')[0]}.png")
            redimensionar_logo(caminho_entrada, caminho_saida)

if __name__ == "__main__":
    processar_arquivos()
