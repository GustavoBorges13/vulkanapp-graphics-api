FROM ubuntu:latest

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    libvulkan-dev \
    wget \
    && rm -rf /var/lib/apt/lists/*

RUN wget -qO - https://packages.lunarg.com/lunarg-signing-key-pub.asc | apt-key add - && \
    wget -qO /etc/apt/sources.list.d/lunarg-vulkan-1.3.290-noble.list https://packages.lunarg.com/vulkan/1.3.290/lunarg-vulkan-1.3.290-noble.list && \
    apt update && \
    apt install -y vulkan-sdk

WORKDIR /usr/app/src

RUN python3 -m venv /usr/app/venv

RUN /usr/app/venv/bin/pip install --upgrade pip
COPY requirements.txt .
RUN /usr/app/venv/bin/pip install -r requirements.txt

COPY . .

CMD ["/usr/app/venv/bin/python3", "./main.py"]