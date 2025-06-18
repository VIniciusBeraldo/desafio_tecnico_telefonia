import os, cv2, threading
import numpy as np
from flask import Flask, request, render_template, jsonify
from flask_socketio import SocketIO

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'mp4'} 

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Caso não exista o diretorio para o armazenamento dos arquivos, o mesmo sera criado.
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Verificando se os arquivos estão dentro das extensões permtidas.
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Configurando o socekio para buscar as informações enviadas ao redis quando a trehad emite um template_found.
socketio = SocketIO(app, message_queue='redis://localhost:6379/0', cors_allowed_origins="*")

def detectacao_template(video_path, image_path, sid=None, threshold=0.7):

    try:
        # Carregamando a imagem template
        template = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        video_base = cv2.VideoCapture(video_path)

        # Verificar se o vídeo foi aberto corretamente
        if not video_base.isOpened():
            if sid:
                socketio.emit('processing_error', {'message': 'Erro ao abrir vídeo.'}, room=sid)
            return

        frame_count = 0

        while True:
            
            ret, frame = video_base.read()

            if not ret: # caso nã encontre nenhum frame, finaliza o processamento.
                print("Fim do vídeo ou erro ao ler frame.")
                break

            frame_count += 1

            frame_cinza = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            res = cv2.matchTemplate(frame_cinza, template, cv2.TM_CCOEFF_NORMED)

            loc = np.where(res >= threshold)

            num_deteccoes_no_frame = 0

            for pt in zip(*loc[::-1]):
                num_deteccoes_no_frame += 1

            if num_deteccoes_no_frame > 0:
                print(f"Template detectado no Frame {frame_count}!")
                if sid: 
                    message_data = {
                        'message': f"Template detectado no Frame {frame_count}"
                    }
                    socketio.emit('template_found', message_data, room=sid) 

        if num_deteccoes_no_frame == 0:
            if sid: 
                message_data = {
                    'message': f"Template não encontrado."
                }
                socketio.emit('template_found', message_data, room=sid) 

    except Exception as e:
        if sid:
            socketio.emit('processing_error', {'message': f"Erro inesperado: {str(e)}"}, room=sid)
    finally:
        if 'cap' in locals() and video_base.isOpened():
            video_base.release()

        if sid: # Notifica que o processamento terminou
            socketio.emit('processing_complete', {'message': 'Processamento de vídeo concluído.'}, room=sid)
        
        if os.path.exists(video_path):
            os.remove(video_path)
        if os.path.exists(image_path):
            os.remove(image_path)
            
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

    client_ws_sid = request.form.get('ws_sid')
    threshold     = request.form.get('threshold')
    threshold_value = float(threshold)

    if not client_ws_sid:
        print("Aviso: SID do WebSocket não recebido no upload. Mensagens WebSocket não serão enviadas para um cliente específico.")

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
        thread = threading.Thread(target=detectacao_template, args=(video_path, image_path, client_ws_sid, threshold_value))
        thread.start()

        return jsonify({"message": "Processamento iniciado."}), 200
    else:
        return jsonify({'error': 'Erro ao salvar um ou ambos os arquivos.'}), 500 # Retorno JSON
    
if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)