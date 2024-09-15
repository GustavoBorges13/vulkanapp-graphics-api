# Usar a imagem base oficial do Ubuntu mais recente
FROM ubuntu:latest

# Instalar as dependências do sistema
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    libvulkan-dev \
    vulkan-utils \
    wget \
    libx11-xcb-dev \
    libx11-dev \
    mesa-utils \
    && rm -rf /var/lib/apt/lists/*

# Baixar e instalar o Vulkan SDK diretamente dos repositórios da LunarG
RUN wget -qO - https://packages.lunarg.com/lunarg-signing-key-pub.asc | apt-key add - && \
    wget -qO /etc/apt/sources.list.d/lunarg-vulkan.list https://packages.lunarg.com/vulkan/lunarg-vulkan.list && \
    apt update && \
    apt install -y vulkan-sdk

# Definir o diretório de trabalho para a aplicação
WORKDIR /usr/app/src

# Criar um ambiente virtual Python para dependências
RUN python3 -m venv /usr/app/venv

# Atualizar o pip e instalar as dependências do Python
RUN /usr/app/venv/bin/pip install --upgrade pip
COPY requirements.txt .
RUN /usr/app/venv/bin/pip install -r requirements.txt

# Copiar o código da aplicação para o diretório de trabalho no container
COPY . .

# Configurar a variável DISPLAY para Linux e fallback para Windows
ENV DISPLAY=${DISPLAY:-host.docker.internal:0}

# Comando padrão para iniciar a aplicação
CMD ["/usr/app/venv/bin/python3", "./main.py"]