# VulkanApp Graphics API
[![NPM](https://img.shields.io/npm/l/react)](https://github.com/GustavoBorges13/vulkanapp-graphics-api/blob/main/LICENSE) 
[![Latest Actual-Development Version](https://img.shields.io/badge/version-v1.0.0-yellow)](https://github.com/GustavoBorges13/vulkanapp-graphics-api/releases)
[![Latest Stable Version](https://img.shields.io/badge/version-v1.0.0-blue)](https://github.com/GustavoBorges13/vulkanapp-graphics-api/releases)
[![GitHub last commit](https://img.shields.io/github/last-commit/GustavoBorges13/vulkanapp-graphics-api)](https://github.com/GustavoBorges13/vulkanapp-graphics-api/commits/main)
<!---[![Build Status](https://app.travis-ci.com/GustavoBorges13/RunBlocker.svg?branch=main)](https://app.travis-ci.com/GustavoBorges13/RunBlocker)-->

```diff
- In development [2024.2]!
+ Authors: Gustavo Silva, Danilo Dutra, Cláudio Evangelista, Matheus Araujo.
# Work for the Computer Graphics course at the Federal University of Catalão (UFCAT), Goiás
```
This project demonstrates how to create a window using GLFW and perform 3D rendering with the Vulkan API (using the Vulkan SDK provided by LunarG) written in python language. The code includes all the steps needed to render a rotating 3D cube, making it a comprehensive and easy-to-understand example of Vulkan-based rendering.

## 🌟 Features 

- **GLFW Window Creation**: Easily set up a window for rendering with Vulkan.
- **Vulkan Integration**: Uses the Vulkan API for efficient 3D rendering.
- **3D Rotating Cube**: A simple, yet complete example of rendering a rotating 3D cube.
- **Easy to Understand**: The code is structured and commented for readability and ease of understanding.
- **Python Implementation**: Developed entirely in Python with Vulkan bindings.

## 📋 Requirements 

- **Python 3.x**: Ensure you have Python 3 installed.
- **Vulkan SDK**: Download and install the Vulkan SDK from [LunarG](https://vulkan.lunarg.com/sdk/home).
- **GLFW**: Installed via Python's package manager `pip`:
  ```bash
  pip install glfw
  ```
- **Vulkan Python Bindings**: Install the Vulkan API bindings for Python via `pip` with the command:
  ```bash
  pip install vulkan
  ```
- **Docker** (optional): You can run this project using Docker for isolated development environments.

## 🔧 Installation 

### 🛠️ Local Setup 

1. Clone the repository:
    ```bash
    git clone https://github.com/your-username/vulkanapp-graphics-api.git
    cd vulkanapp-graphics-api
    ```

2. Install the required Python packages:
    ```bash
    pip install -r requirements.txt
    ```

3. Ensure the Vulkan SDK is properly installed on your system. You can check by running:
    ```bash
    vulkaninfo
    ```

4. Run the Python script to launch the 3D rotating cube:
    ```bash
    python main.py
    ```
### 🐳 Docker Setup from Docker Hub 

- If you are using the image from Docker Hub, run the container with:
    ```bash
    docker run -it --rm --name my_vulkan_app gustavoborges13/vulkan_app
    ```

### 🔄 Docker Setup from Local Build 

You can also use Docker to set up the project in a containerized environment.

1. To build the Docker image, use the following command:
    ```bash
    docker build -t vulkanapp-graphics-api .
    ```

2. Run the Docker container:
    ```bash
    docker run -it python_vulkan_api
    ```

For detailed Docker commands, see the [docker-commands.md](docker-commands.md) file.

## 📖 Usage 

Once the application is running, a window will open displaying a 3D cube. The cube will rotate indefinitely, demonstrating basic 3D rendering using the Vulkan API.

## 🗂️ Project Structure 

```bash
├── Dockerfile                # Docker configuration
├── colors.py                 # Color handling for rendering
├── config.py                 # Vulkan configuration
├── device.py                 # Device selection and management
├── instance.py               # Vulkan instance creation
├── logging.py                # Logging utilities
├── main.py                   # Main script to launch the rendering
├── requirements.txt          # Python dependencies
└── __pycache__               # Compiled Python files
```


## 🚀 Getting Started with Vulkan API: Introduction and Basics 
Dive into the world of Vulkan API! Whether you're new to graphics programming or looking to expand your skills, our guide provides a clear and engaging introduction to Vulkan's core concepts. Start building high-performance graphics applications today!
[Explore the Wiki](https://github.com/GustavoBorges13/vulkanapp-graphics-api/wiki)
