FROM ubuntu:latest

# Atualize o sistema e instale o Python e dependências necessárias
RUN apt update && apt install -y \
    python3 \
    python3-pip \
    python3-venv \
    libvulkan-dev \
    cmake \
    build-essential \
    wget \
    gnupg

# Crie um ambiente virtual
RUN python3 -m venv /venv

# Ative o ambiente virtual e atualize o pip
RUN /venv/bin/pip install --upgrade pip

# Instale as bibliotecas Python necessárias no ambiente virtual
RUN /venv/bin/pip install glfw vulkan

# Adicione o repositório do Vulkan SDK e instale-o
RUN wget -qO - https://packages.lunarg.com/lunarg-signing-key-pub.asc | apt-key add - && \
    wget -qO /etc/apt/sources.list.d/lunarg-vulkan-1.3.290-noble.list https://packages.lunarg.com/vulkan/1.3.290/lunarg-vulkan-1.3.290-noble.list && \
    apt update && \
    apt install -y vulkan-sdk

# Defina o diretório de trabalho dentro do contêiner
WORKDIR /usr/app/src

# Copie todos os arquivos e diretórios do contexto de construção para o diretório de trabalho
COPY . .

# Defina o caminho do Python e pip para o ambiente virtual
ENV PATH="/venv/bin:$PATH"

# Comando padrão para executar o script Python
CMD ["python3", "./main.py"]