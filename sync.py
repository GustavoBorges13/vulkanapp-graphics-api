from config import *
import logging

def make_semaphore(device):

     #cria as informações para o semáforo usando a estrutura VkSemaphoreCreateInfo
    semaphoreInfo = VkSemaphoreCreateInfo()

    try:
        #tenta criar o semáforo usando a função Vulkan vkCreateSemaphore
        return vkCreateSemaphore(device, semaphoreInfo, None)
    
    except:

        logging.logger.print(f"{FAIL}Falha ao criar o semáforo{RESET}")
        
        return None

def make_fence(device):

    #cria as informações para a cerca, inicializando-a já sinalizada
    fenceInfo = VkFenceCreateInfo(
        flags = VK_FENCE_CREATE_SIGNALED_BIT #define a cerca como sinalizada inicialmente
    )

    try:
        #tenta criar a cerca usando a função Vulkan vkCreateFence
        return vkCreateFence(device, fenceInfo, None)
    
    except:

        logging.logger.print(f"{FAIL}Failed to create fence{RESET}")
        
        return None