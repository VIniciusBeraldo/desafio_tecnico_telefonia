# Sistema de Detecção de Template em Vídeo

Este é um sistema web que permite o upload de um vídeo e uma imagem de template, processando o vídeo em tempo real para detectar a ocorrência do template em seus frames. O status do processamento e os frames onde o template foi encontrado são exibidos na interface do usuário através de comunicação em tempo real (WebSockets).

## Funcionalidades

* **Upload de Vídeo e Imagem:** Carregue um arquivo de vídeo e uma imagem de template.
* **Processamento em Background:** O processamento do vídeo ocorre em uma thread separada no servidor, sem travar a interface.
* **Comunicação em Tempo Real:** Use WebSockets (Socket.IO) para receber atualizações instantâneas sobre o processamento e as detecções.
* **Limiar de Detecção (Threshold):** Campo opcional para ajustar a sensibilidade da detecção de template.
* **Listagem de Detecções:** Os frames onde o template é encontrado são listados na interface.
* **Feedback de Status:** Monitore o status do servidor e do processamento.

## Tecnologias Utilizadas

* **Backend:** Python (Flask, Flask-SocketIO, OpenCV, NumPy, Redis)
* **Frontend:** HTML, CSS, JavaScript (Socket.IO client)
* **Fila de Mensagens:** Redis

---

## 🚀 Guia de Instalação Completo (Desde o Ubuntu no WSL)

Este guia cobre a instalação e configuração em um ambiente Windows usando o Subsistema Windows para Linux (WSL), que é o ambiente recomendado para este projeto no Windows.

### Parte 1: Configurando o Ambiente WSL no Windows

Esta etapa permite que você execute um sistema Linux (Ubuntu) diretamente no Windows.

1.  **Ativar o Subsistema Windows para Linux (WSL):**
    * Abra o **PowerShell como Administrador** (clique com o botão direito no ícone do PowerShell no menu Iniciar e selecione "Executar como administrador").
    * Execute o seguinte comando:
        ```powershell
        wsl --install
        ```
    * Este comando ativará os recursos necessários do WSL e instalará o Ubuntu por padrão.
    * **Reinicie o seu computador** quando solicitado.

2.  **Configurar o Ubuntu no WSL:**
    * Após o reinício, o terminal do Ubuntu deve abrir automaticamente. Se não abrir, procure por "Ubuntu" no menu Iniciar e abra-o.
    * Na primeira execução, ele pedirá para você criar um **nome de usuário UNIX** e uma **senha**. Crie-os e anote, pois você precisará deles para comandos `sudo`.

3.  **Atualizar o Ubuntu:**
    * É uma boa prática atualizar os pacotes do Ubuntu. No seu terminal WSL (Ubuntu), execute:
        ```bash
        sudo apt update
        sudo apt upgrade -y
        ```
    * Isso pode levar alguns minutos.

### Parte 2: Instalação e Execução do Redis no WSL

O Redis será usado como uma fila de mensagens para a comunicação entre o seu backend e o frontend.

1.  **No seu terminal WSL (Ubuntu), instale o Redis:**
    ```bash
    sudo apt install redis-server
    ```
    * Pressione `Y` e Enter quando solicitado.

2.  **Inicie o serviço Redis no WSL:**
    ```bash
    sudo service redis-server start
    ```
    * Você precisará digitar sua senha do Ubuntu.
    * *Nota: `sudo systemctl enable redis-server` e `sudo systemctl start redis-server` podem não funcionar em todas as distribuições WSL ou em todas as versões do WSL. `sudo service redis-server start` é mais universal para iniciar o serviço dentro da sessão WSL atual.*

3.  **Verifique se o Redis está rodando:**
    ```bash
    redis-cli ping
    ```
    * Se retornar `PONG`, o Redis está funcionando corretamente.
    * **Importante:** Mantenha este terminal WSL aberto com o Redis rodando enquanto você usa sua aplicação.

### Parte 3: Clonando o projeto para a pasta desejada

Após configurar o ambiente do redis, podemos clonar o projeto desejado para sua maquina e baixar as dependencias do python.

1. **Abrir o cmd e navegar ate o repositorio desejado na sua maquina e digitar o comando:**
    ```bash
    git clone https://github.com/VIniciusBeraldo/desafio_tecnico_telefonia.git
    ```
    * Feito isso devera dar inicio ao clone do projeto para o reposiorio desejado.

### Parte 4: Instalando as dependencias do python

Instalar todas as dependencias necessarias para rodar o projeto.

1. **Após realizar o clone do projeto, devemos navegar para dentro da pasta <desafio_tecnico_telefonia> e realizar o comando abaixo para instalar todas as depencias que se encontra no requirements.txt**
    ```bash
    pip install -r requirements.txt
    ```
    * Vai ser dado o inicio dos downloads das depencias necessarias para o projeto.

### Parte 5: Iniciar a aplicação

1. **Certificar que o redis está ativo com o comando redis-cli ping no ubunto e então navegar para pasta app e iniciar o arquivo app.py, conforme o comando abaixo.**
    ```bash
    python app.py
    ```
    Ou
    ```bash
    python <CAMINHO COMPLETO ATÉ O ARQUIVO APP.PY>
    Ex: python C:\\Users\\vberaldo\\Documents\\desafio_tecnico_telefonia\\app\\app.py
    ```
2. **Após iniciar a aplicação deverá clicar na url http://127.0.0.1:5000, que se encontra no terminal de comando para acessar a aplicação.**