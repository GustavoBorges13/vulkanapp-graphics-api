from config import *
import logging

class QueueFamilyIndices:

    def __init__(self):
        self.graphicsFamily = None
        self.presentFamily = None
    
    def is_complete(self):
        
        return not(self.graphicsFamily is None or self.presentFamily is None)
    
def find_queue_families(device, instance, surface):

        indices = QueueFamilyIndices()
        
        surfaceSupport = vkGetInstanceProcAddr(instance, "vkGetPhysicalDeviceSurfaceSupportKHR")
        
        queueFamilies = vkGetPhysicalDeviceQueueFamilyProperties(device)


        logging.logger.print(f"{WARNING}Há {len(queueFamilies)} famílias de filas disponíveis no sistema.{RESET}")

        # Verificacao bit a bit para verificar se a fila suporta nossas operacoes graficas
        for i, queueFamily in enumerate(queueFamilies):

            """
            // Provided by VK_VERSION_1_0
                typedef struct VkQueueFamilyProperties {
                VkQueueFlags    queueFlags;
                uint32_t        queueCount;
                uint32_t        timestampValidBits;
                VkExtent3D      minImageTransferGranularity;
                } VkQueueFamilyProperties;

            // Provided by VK_VERSION_1_0
            typedef enum VkQueueFlagBits {
                VK_QUEUE_GRAPHICS_BIT = 0x00000001,
                VK_QUEUE_COMPUTE_BIT = 0x00000002,
                VK_QUEUE_TRANSFER_BIT = 0x00000004,
                VK_QUEUE_SPARSE_BINDING_BIT = 0x00000008,
                // Provided by VK_VERSION_1_1
                VK_QUEUE_PROTECTED_BIT = 0x00000010,
            } VkQueueFlagBits;

            As famílias de filas no Vulkan são categorizadas por tipos de operações que suportam, como:
            - Gráficos: Para renderização gráfica.
            - Computação: Para cálculos gerais em GPU, sem necessariamente envolver gráficos.
            - Transferência de dados: Para movimentar dados entre a memória da CPU e GPU.
            - Memória esparsa: Para gerenciar memória de maneira otimizada, como em alocação dinâmica.
            - Memória protegida: Para operações que envolvem o uso de memória protegida, garantindo segurança e isolamento de dados sensíveis dentro da GPU.

            """

            if queueFamily.queueFlags & VK_QUEUE_GRAPHICS_BIT:
                indices.graphicsFamily = i

                logging.logger.print(f"{OKGREEN}A família de filas {i} é adequada para gráficos.{RESET}")

            if surfaceSupport(device, i, surface):
                indices.presentFamily = i

                logging.logger.print(f"{OKGREEN}A família de filas {i} é adequada para apresentar.{RESET}")

            if indices.is_complete():
                break

        return indices