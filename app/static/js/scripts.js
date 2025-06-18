const socket = io('http://localhost:5000');

const listaFrames = document.getElementById('frames_encontrados');
const wsSidInput = document.getElementById('wsSid');     
const uploadForm = document.getElementById('upload_form'); 
const paragrafoStatusServidor = document.getElementById('status_servidor'); 
const paragrafoStatusProcessamento = document.getElementById('status_processamento'); 
const thresholdInput = document.getElementById('threshold_input')

socket.on('connect', () => {
    wsSidInput.value = socket.id; // Guarda o ID da sessão WebSocket no campo oculto.
    atualizarStatusServidor('Conectado ao servidor', 'info'); 
});

function atualizarStatusServidor(msg, type='info') {  // função destinada a aterar o status do servidor.
    paragrafoStatusServidor.textContent = msg
}

function atualizarStatusProcessamento(msg, type='info') {  // função destinada a aterar o status do processamento.
    paragrafoStatusProcessamento.textContent = msg
}

function adicionarFramesEncontrados(msg, type = 'info') { // função destinada a incrementar a lista dos frames encontrados.
    const li = document.createElement('li');
    li.classList.add('frames_encontrados', type);
    li.textContent = msg;
    listaFrames.appendChild(li);
}

socket.on('template_found', (data) => { // acionado o evento de que o template foi encontrado é chamado a função adicionarFramesEncontrados para incrementar o li om a mensagem passada.
    adicionarFramesEncontrados(data.message, 'detection'); 
});

socket.on('processing_complete', (data) => { // Quando o processamento do vídeo termina é atualizado o <p> do satus de processamento.
    atualizarStatusProcessamento(data.message, 'success');
});

uploadForm.addEventListener('submit', async (event) => { // evento ao clicar em enviar, para realiar o pedido para flask e depois realizar o processamento com opencv que esta em app.py
    event.preventDefault(); 

    listaFrames.innerHTML = ''

    const formData = new FormData();
    formData.append('video', document.getElementById('arquivo_video').files[0]);
    formData.append('image', document.getElementById('arquivo_template').files[0]);
    formData.append('ws_sid', wsSidInput.value);
    formData.append('threshold', thresholdInput.value);
    
    atualizarStatusProcessamento('Enviando arquivos para processamento...', 'info');

    try {
        const response = await fetch('/uploads', {
            method: 'POST',
            body: formData
        });

        const result = await response.json();

        if (response.ok) {
            atualizarStatusProcessamento(result.message, 'info');
        } else {
            atualizarStatusProcessamento(`Erro no upload: ${result.error}`, 'error');
        }
    } catch (error) {
        atualizarStatusServidor(`Erro de rede ou servidor: ${error.message}`, 'error'); 
    }
});