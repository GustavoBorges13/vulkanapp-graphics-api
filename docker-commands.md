
# Docker Commands Reference

This document contains useful Docker commands to manage containers, images, and volumes.

## Images

- **View all images**:
  ```bash
  docker images
  ```

## Volumes

- **List all volumes**:
  ```bash
  docker volume ls
  ```

## Containers

- **View running containers**:
  ```bash
  docker ps
  ```

- **View all containers (including stopped)**:
  ```bash
  docker ps -a
  ```

## Container Management

- **Start a container**:
  ```bash
  docker start ubuntu_vulkan_api
  ```

- **Access a running container**:
  ```bash
  docker attach ubuntu_vulkan_api
  ```
  Or:
  ```bash
  docker exec -it ubuntu_vulkan_api bash
  ```

## Exiting the Container

- **Exit the container without stopping it**:
  - Use `exit` to leave the container.
  - Use `Ctrl + Q` (Read Escape Sequence) to leave the terminal without stopping the container.

---

For more Docker commands and details, refer to the [Docker documentation](https://docs.docker.com/).
