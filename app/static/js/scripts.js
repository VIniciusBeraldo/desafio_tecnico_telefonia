const socket = io('http://localhost:5000');

const messagesList = document.getElementById('messages'); // Onde as mensagens serão exibidas na HTML
const wsSidInput = document.getElementById('wsSid');     // O campo oculto para guardar o SID
const uploadForm = document.getElementById('upload_form'); // Seu formulário

socket.on('template_found', (data) => {
    console.log("encontrou")
    addMessage(msg, 'detection'); 
});