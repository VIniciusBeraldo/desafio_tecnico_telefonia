import os, cv2, threading
import numpy as np
from flask import Flask, request, render_template
from flask_socketio import SocketIO, emit, join_room, leave_room

app = Flask(__name__)

# --- Configurações para Upload ---
# Define o diretório onde os arquivos serão salvos temporariamente
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'avi', 'mov'} # Adicione os tipos de arquivo que você permite

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Cria o diretório de uploads se ele não existir
# Isso garante que a pasta 'uploads' esteja pronta quando o app iniciar
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def detectacao_template(video_path, image_path, sid=None):

    # Carregar o template
    template = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    # Verificar se o template foi carregado
    if template is None:
        print(f"Erro: Não foi possível carregar o template em '{image_path}'")
        print("Verifique se o arquivo existe e o caminho está correto.")
        exit()

    cap = cv2.VideoCapture(video_path)

    # Verificar se o vídeo foi aberto corretamente
    if not cap.isOpened():
        print(f"Erro: Não foi possível abrir o vídeo em '{video_path}'")
        print("Verifique se o arquivo de vídeo existe, o caminho está correto e se ele não está corrompido.")
        print("Se estiver usando webcam (0), verifique se ela está conectada e disponível.")
        exit()

    frame_count = 0

    while True:
        
        ret, frame = cap.read()

        if not ret:
            print("Fim do vídeo ou erro ao ler frame.")
            break

        frame_count += 1

        frame_cinza = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        res = cv2.matchTemplate(frame_cinza, template, cv2.TM_CCOEFF_NORMED)

        threshold = 0.7

        loc = np.where(res >= threshold)

        num_deteccoes_no_frame = 0

        for pt in zip(*loc[::-1]): # Itera sobre todas as detecções encontradas
            num_deteccoes_no_frame += 1

        if num_deteccoes_no_frame > 0:
            print(f"Template detectado no Frame {frame_count}!")

# --- Rotas da Aplicação ---

@app.route('/')
def index():
    # Rota para exibir o formulário de upload
    return render_template('index.html')

@app.route('/uploads', methods=['POST'])
def upload_files():
    if 'video' not in request.files or 'image' not in request.files:
        return 'Nenhum arquivo de vídeo ou imagem enviado', 400

    video_file = request.files['video']
    image_file = request.files['image']

    video_path = None
    image_path = None

    # Processa o arquivo de vídeo
    if video_file and allowed_file(video_file.filename):
        video_path = os.path.join(app.config['UPLOAD_FOLDER'], video_file.filename)
        video_file.save(video_path) # SALVA O ARQUIVO NO DIRETÓRIO TEMPORÁRIO
        print(f"Vídeo salvo temporariamente em: {video_path}") # Para depuração

    # Processa o arquivo de imagem
    if image_file and allowed_file(image_file.filename):
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_file.filename)
        image_file.save(image_path) # SALVA O ARQUIVO NO DIRETÓRIO TEMPORÁRIO
        print(f"Imagem salva temporariamente em: {image_path}") # Para depuração

    # Após salvar, você pode usar video_path e image_path para seu processamento com OpenCV
    # Por exemplo:
    if video_path and image_path:
        thread = threading.Thread(target=detectacao_template, args=(video_path, image_path))
        thread.start()

        return {"message": "Arquivos recebidos e processamento iniciado em background!"}, 200
    else:
        return 'Erro ao salvar um ou ambos os arquivos.', 500
    
if __name__ == '__main__':
    app.run(debug=True) # Rode em modo de depuração para facilitar o desenvolvimento