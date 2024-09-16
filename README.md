# VulkanApp Graphics API
[![NPM](https://img.shields.io/npm/l/react)](https://github.com/GustavoBorges13/vulkanapp-graphics-api/blob/main/LICENSE) 
[![Latest Actual-Development Version](https://img.shields.io/badge/version-v1.2.0-yellow)](https://github.com/GustavoBorges13/vulkanapp-graphics-api/releases)
[![Latest Stable Version](https://img.shields.io/badge/version-v1.2.0-blue)](https://github.com/GustavoBorges13/vulkanapp-graphics-api/releases)
[![GitHub last commit](https://img.shields.io/github/last-commit/GustavoBorges13/vulkanapp-graphics-api)](https://github.com/GustavoBorges13/vulkanapp-graphics-api/commits/main)
<!---[![Build Status](https://app.travis-ci.com/GustavoBorges13/RunBlocker.svg?branch=main)](https://app.travis-ci.com/GustavoBorges13/RunBlocker)-->

```diff
- In development [2024.2]!
+ Authors: Gustavo Silva, Danilo Dutra, Cláudio Evangelista, Matheus Araujo.
# Work for the Computer Graphics course at the Federal University of Catalão (UFCAT), Goiás
```
This project demonstrates how to create a window using GLFW and perform 3D rendering with the Vulkan API (using the Vulkan SDK provided by LunarG) written in python language. The code includes all the steps needed to render a rotating 3D cube, making it a comprehensive and easy-to-understand example of Vulkan-based rendering.<br><br>

## 🌟 Features 

- **GLFW Window Creation**: Easily set up a window for rendering with Vulkan.
- **Vulkan Integration**: Uses the Vulkan API for efficient 3D rendering.
- **3D Rotating Cube**: A simple, yet complete example of rendering a rotating 3D cube.
- **Easy to Understand**: The code is structured and commented for readability and ease of understanding.
- **Python Implementation**: Developed entirely in Python with Vulkan bindings.<br><br>


## 📋 Requirements 

- **Python 3.x**: Ensure you have Python 3 installed.
- **Vulkan SDK 1.3.x**: Download and install the Vulkan SDK from [LunarG](https://vulkan.lunarg.com/sdk/home).
- **GLFW**: Installed via Python's package manager `pip`:
  ```bash
  pip install glfw
  ```
- **Vulkan Python Bindings**: Install the Vulkan API bindings for Python via `pip` with the command:
  ```bash
  pip install vulkan
  ```
- **Docker** (optional): You can run this project using Docker for isolated development environments. For more details, see the [Docker Setup from Docker Hub](#-docker-setup-from-docker-hub) or [Docker Setup from Local Build](#-docker-setup-from-local-build).<br><br>


## 🔧 Installation 

### Manual setup

1. Clone the repository:
    ```bash
    git clone https://github.com/GustavoBorges13/vulkanapp-graphics-api.git
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
    
### Portable installation
> coming soon

### Installer setup
> comming soon

<br>

## 🐳 Docker Setup from Docker Hub 

To run graphical applications in Docker, you'll need to configure X11 display support based on your operating system.

### General Notes
Ensure Docker is installed and configured on your machine.

### For Windows Users
You can also follow the windows procedure in a solved problem [here](https://github.com/GustavoBorges13/vulkanapp-graphics-api/issues/1).
If you need to display graphical applications from Docker on Windows, follow these steps:

1. Download and Install X Server:

   - Install VcXsrv, a Windows X Server tool. This will set up Xming and Xlaunch.
  
3. Configure Xlaunch:

   1. Launch Xlaunch after installation.
   2. In the "Select Display Settings" screen, keep "Multiple windows" checked.
   3. In the "Select how to start clients" screen, choose "Start no client".
   4. In the "Extra settings" screen, check "Disable access control".
   5. Click "Finish" to complete the setup.

3. Run the Docker Container:
   
   ```bash
   docker run -it --rm --name my_vulkan_app -e DISPLAY=host.docker.internal:0 gustavoborges13/vulkan_app
 
   # If you have an NVIDIA GPU (optional), use:
   docker run --gpus all -it --rm --name my_vulkan_app -e DISPLAY=host.docker.internal:0 gustavoborges13/vulkan_app
   ```

   Xlaunch will run in the background, waiting for X11 applications to connect and use display :0.

### For Linux Users

To display graphical applications from Docker on Linux, follow these steps:

1. Install X Server:

   - Most Linux distributions come with an X server installed. If not, install it using your package manager:
     
     ```bash
     sudo apt-get install xorg
     ```

2. Configure X Server for Docker:

   - Allow Docker containers to access the X server:
     
     ```bash
     xhost +local:docker
     
     # To revoke access later (optional):
     xhost -local:docker
     ```

3. Run the Docker Container:
   
   ```bash
   docker run -it --rm --name my_vulkan_app -e DISPLAY=host.docker.internal:0 -v /tmp/.X11-unix:/tmp/.X11-unix gustavoborges13/vulkan_app
 
   # If you have an NVIDIA GPU (optional), use:
   docker run --gpus all -it --rm --name my_vulkan_app -e DISPLAY=host.docker.internal:0 -v /tmp/.X11-unix:/tmp/.X11-unix gustavoborges13/vulkan_app
   ```

   This setup will allow Docker containers to use the X11 display server on your Linux system.

### For macOS Users

To display graphical applications from Docker on macOS, follow these steps:

1. Install X Server:

   - Download and install XQuartz from the official website.

2. Configure XQuartz:

   1. Open XQuartz after installation.
   2. Go to XQuartz > Preferences.
   3. In the "Security" tab, check "Allow connections from network clients".
   4. Restart XQuartz to apply the changes.

3. Run the Docker Container:
  
   - Run the Docker container:
     
     ```bash
     docker run -it --rm --name my_vulkan_app -e DISPLAY=host.docker.internal:0 gustavoborges13/vulkan_app
    
     # If you have an NVIDIA GPU (optional), use:
     docker run --gpus all -it --rm --name my_vulkan_app -e DISPLAY=host.docker.internal:0 gustavoborges13/vulkan_app
     ```
  
   XQuartz will provide the display server necessary for running X11 applications.

<br>


## 🔄 Docker Setup from Local Build 

### Using Dockerfile

The build will be performed by ./Dockerfile.


1. Clone the repository:
   
   ```bash
     git clone https://github.com/GustavoBorges13/vulkanapp-graphics-api.git
     cd vulkanapp-graphics-api
   ```
2. To build the Docker image, use the following command:
   
   ```bash
     docker build -t vulkanapp-graphics-api .
   ```
3. Run the Docker container:
   
   ```bash
     docker run -it --rm -e DISPLAY=host.docker.internal:0 vulkanapp-graphics-api
  
     # If you have an NVIDIA GPU (optional), use:
     docker run --gpus all -it --rm -e DISPLAY=host.docker.internal:0 vulkanapp-graphics-api
   ```
This command ensures that the container has access to the GPU and connects to the X Server on your host machine for graphical output.

> It's worth remembering that the observations made earlier in the from docker hub procedure apply here too. Have the X server configured and docker installed.


### Using Docker Compose

The build will be performed by ./docker-compose.yml.

> It's worth remembering that the observations made earlier in the from docker hub procedure apply here too. Have the X server configured and docker installed for the application window to appear.

1. Clone the repository:

   ```bash
     git clone https://github.com/GustavoBorges13/vulkanapp-graphics-api.git
     cd vulkanapp-graphics-api
   ```
2. To build the Docker image and run, use the following command:

   ```bash
     docker-compose up
   ```

For detailed Docker commands, see the [docker-commands.md](docker-commands.md) file.<br><br>

## 📖 Usage 

Once the application is running, a window will open displaying a 3D cube. The cube will rotate indefinitely, demonstrating basic 3D rendering using the Vulkan API.<br><br>


## 🗂️ Project Structure 

```bash
.
├── .gitignore                  # Git ignore file
├── colors.py                   # Color handling for rendering
├── config.py                   # Vulkan configuration
├── device.py                   # Device selection and management
├── docker-commands.md          # Docker commands and setup instructions
├── docker-compose.yml          # Docker Compose configuration
├── Dockerfile                  # Docker configuration for building the image
├── Dockerfile copy             # Possibly an outdated or alternative Dockerfile
├── instance.py                 # Vulkan instance creation
├── LICENSE                     # License file for the project
├── logging.py                  # Logging utilities
├── main.py                     # Main script to launch the rendering
├── README.md                   # Project documentation and overview
├── requirements.txt            # Python dependencies
└── __pycache__                 # Compiled Python files

└── .github
    └── workflows
        └── Docker.yml          # GitHub Actions workflow for Docker
```
<br>

## 🚀 Getting Started with Vulkan API: Introduction and Basics 
Dive into the world of Vulkan API! Whether you're new to graphics programming or looking to expand your skills, our guide provides a clear and engaging introduction to Vulkan's core concepts. Start building high-performance graphics applications today!
[Explore the Wiki](https://github.com/GustavoBorges13/vulkanapp-graphics-api/wiki)
