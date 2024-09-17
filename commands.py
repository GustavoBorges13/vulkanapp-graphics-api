from config import *
import queue_families
import logging

class commandPoolInputChunk:
    """
    Classe para armazenar dados necessários para criar um pool de comandos.
    """
    def __init__(self):

        self.device = None
        self.physicalDevice = None
        self.surface = None
        self.instance = None

class commandbufferInputChunk:
    """
    Classe para armazenar dados necessários para criar buffers de comando.
    """
    def __init__(self):

        self.device = None
        self.commandPool = None
        self.frames = None

def make_command_pool(inputChunk):
    
    #cria um pool de comandos Vulkan.
    #encontrar os índices das filas de comandos
    queueFamilyIndices = queue_families.find_queue_families(
        device = inputChunk.physicalDevice,
        instance = inputChunk.instance,
        surface = inputChunk.surface,
    )

    """
    teremos um monte de buffers de comando e o que faremos é, pegar um buffer de comando,
    redefini-lo e então gravar os comandos de desenho em cada imagem.
    """
    #especificar se temos permissão para redefinir os buffers de comandos individualmente
    poolInfo = VkCommandPoolCreateInfo(
        queueFamilyIndex=queueFamilyIndices.graphicsFamily,
        flags = VK_COMMAND_POOL_CREATE_RESET_COMMAND_BUFFER_BIT
    )

    try:
        commandPool = vkCreateCommandPool(
            inputChunk.device, poolInfo, None
        )
        logging.logger.print(f"{HEADER}Conjunto de comandos criado{RESET}")
        return commandPool
    except:
        logging.logger.print(f"{FAIL}Falha ao criar o pool de comandos{RESET}")
        return None
    
def make_frame_command_buffers(inputChunk: commandbufferInputChunk) -> None:

    """
        Cria buffers de comando para cada quadro.

        Parâmetros:
            inputChunk (commandBufferInputChunk): contém os vários objetos necessários.
    """
    #cria buffers de comando Vulkan para cada quadro.
    allocInfo = VkCommandBufferAllocateInfo(
        commandPool = inputChunk.commandPool,
        level = VK_COMMAND_BUFFER_LEVEL_PRIMARY,
        commandBufferCount = 1
    )

    #criar um buffer de comando para cada quadro
    for i,frame in enumerate(inputChunk.frames):

        try:
            frame.commandbuffer = vkAllocateCommandBuffers(inputChunk.device, allocInfo)[0]

            logging.logger.print(f"{OKGREEN}Buffer de comando alocado para o quadro {i}{RESET}")
        except:
            logging.logger.print(f"{FAIL}Falha ao alocar o buffer de comando para o quadro {i}{RESET}")

    
def make_command_buffer(inputChunk):
    """
        Crie um único buffer de comando para cada quadro.

        Parâmetros:
            inputChunk (commandBufferInputChunk): contém os vários objetos necessários.
    """
    allocInfo = VkCommandBufferAllocateInfo(
        commandPool = inputChunk.commandPool,
        level = VK_COMMAND_BUFFER_LEVEL_PRIMARY,
        commandBufferCount = 1
    )

    #alocar o buffer de comando principal
    try:
        commandbuffer = vkAllocateCommandBuffers(inputChunk.device, allocInfo)[0]

        logging.logger.print(f"{OKBLUE}Buffer de comando principal alocado{RESET}")
        return commandbuffer
    except:
        logging.logger.print(f"{FAIL}Failed to allocate main command buffer{RESET}")
        return None