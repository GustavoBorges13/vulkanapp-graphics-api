from config import *

"""
    O Vulkan separa o conceito de dispositivos físicos e lógicos. 

    Um dispositivo físico geralmente representa uma única implementação completa do Vulkan 
    (excluindo a funcionalidade ao nível da instância) disponível para o anfitrião, 
    e existe um número finito delas. 
  
    Um dispositivo lógico representa uma instância dessa implementação 
    com o seu próprio estado e recursos independentes de outros dispositivos lógicos.
"""
class QueueFamilyIndices:

    def __init__(self):
        self.graphicsFamily = None
        self.presentFamily = None
    
    def is_complete(self):
        
        return not(self.graphicsFamily is None or self.presentFamily is None)

def log_device_properties(device):
    
    """
        void vkGetPhysicalDeviceProperties(
            VkPhysicalDevice                            physicalDevice,
            VkPhysicalDeviceProperties*                 pProperties);

    """

    properties = vkGetPhysicalDeviceProperties(device)

    """
        typedef struct VkPhysicalDeviceProperties {
            uint32_t                            apiVersion;
            uint32_t                            driverVersion;
            uint32_t                            vendorID;
            uint32_t                            deviceID;
            VkPhysicalDeviceType                deviceType;
            char                                deviceName[VK_MAX_PHYSICAL_DEVICE_NAME_SIZE];
            uint8_t                             pipelineCacheUUID[VK_UUID_SIZE];
            VkPhysicalDeviceLimits              limits;
            VkPhysicalDeviceSparseProperties    sparseProperties;
            } VkPhysicalDeviceProperties;
    """

    print(f"{OKGREEN}Nome do dispositivo: {properties.deviceName}")

    print("Tipo de dispositivo: ",end="")

    if properties.deviceType == VK_PHYSICAL_DEVICE_TYPE_CPU:
        print(f"CPU{RESET}")
    elif properties.deviceType == VK_PHYSICAL_DEVICE_TYPE_DISCRETE_GPU:
        print(f"Discrete GPU{RESET}")
    elif properties.deviceType == VK_PHYSICAL_DEVICE_TYPE_INTEGRATED_GPU:
        print(f"Integrated GPU{RESET}")
    elif properties.deviceType == VK_PHYSICAL_DEVICE_TYPE_VIRTUAL_GPU:
        print(f"Virtual GPU{RESET}")
    else:
        print(f"Outro{RESET}")

def check_device_extension_support(device, requestedExtensions, debug):

    """
        Verifica se um determinado dispositivo físico pode satisfazer uma lista de extensões de dispositivo solicitadas.
    """

    supportedExtensions = [
        extension.extensionName 
        for extension in vkEnumerateDeviceExtensionProperties(device, None)
    ]

    if debug:
        print(f"{WARNING}O dispositivo pode suportar extensões:{RESET}")

        for extension in supportedExtensions:
            print(f"{GRAY_DARK}\t\"{extension}\"{RESET}")

    for extension in requestedExtensions:
        if extension not in supportedExtensions:
            return False
    
    return True

def is_suitable(device, debug):

    if debug:
        print(f"{HEADER}:: Verificar se o dispositivo é adequado{RESET}")

    """
        Um dispositivo é adequado se puder ser apresentado no ecrã, ou seja, se suportar
        a extensão swapchain
    """
    requestedExtensions = [
        VK_KHR_SWAPCHAIN_EXTENSION_NAME
    ]

    if debug:
        print(f"{HEADER}:: Extensões de dispositivos a solicitar:{RESET}")

        for extension in requestedExtensions:
            print(f"{UNDERLINE}\t\"{extension}\"{RESET}")

    if check_device_extension_support(device, requestedExtensions, debug):

        if debug:
            print(f"{OKGREEN}O dispositivo pode suportar as extensões solicitadas!{RESET}")
        return True
    
    if debug:
        print(f"{FAIL}O dispositivo não pode suportar as extensões solicitadas!{RESET}")

    return False

def choose_physical_device(instance, debug):

    """
        Selecionar um dispositivo físico adequado a partir de uma lista de candidatos.
    
        Nota: Os dispositivos físicos não são criados nem destruídos, eles existem
        independentemente do programa.
    """

    if debug:
        print(f"{HEADER}:: Seleção do dispositivo físico{RESET}")

    """
        vkEnumeratePhysicalDevices(instance) -> List(vkPhysicalDevice)
    """
    availableDevices = vkEnumeratePhysicalDevices(instance)

    if debug:
        print(f"{OKBLUE}Existem {len(availableDevices)} dispositivos físicos disponíveis neste sistema{RESET}")

    # verificar se é possível encontrar um dispositivo adequado
    for device in availableDevices:
        if debug:
            log_device_properties(device)
        if is_suitable(device, debug):
            return device

    return None

def find_queue_families(device, instance, surface, debug):

        indices = QueueFamilyIndices()
        
        surfaceSupport = vkGetInstanceProcAddr(instance, "vkGetPhysicalDeviceSurfaceSupportKHR")
        
        queuFamilies = vkGetPhysicalDeviceQueueFamilyProperties(device)


        if debug:
            print(f"{WARNING}Há {len(queuFamilies)} famílias de filas disponíveis no sistema.{RESET}")

        # Verificacao bit a bit para verificar se a fila suporta nossas operacoes graficas
        for i, queueFamily in enumerate(queuFamilies):

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

                if debug:
                    print(f"{OKGREEN}A família de filas {i} é adequada para gráficos.{RESET}")

            if surfaceSupport(device, i, surface):
                indices.presentFamily = i

                if debug:
                    print(f"{OKGREEN}A família de filas {i} é adequada para apresentar.{RESET}")

            if indices.is_complete():
                break

        return indices

def create_logical_device(physicalDevice, instance, surface, debug):

    """
        Criar uma abstração em torno da GPU
    """

    """
        No momento da criação, todas as filas necessárias também serão criadas,
        portanto, as informações de criação de fila devem ser passadas em
    """

    indices = find_queue_families(physicalDevice, instance, surface, debug)
    uniqueIndices = [indices.graphicsFamily,]
    if indices.graphicsFamily != indices.presentFamily:
            uniqueIndices.append(indices.presentFamily)

    queueCreateInfo = []

    for queueFamilyIndex in uniqueIndices:
        queueCreateInfo.append(
            VkDeviceQueueCreateInfo(
                queueFamilyIndex = queueFamilyIndex,
                queueCount = 1,
                pQueuePriorities= [1.0,]
            )
        )

    """
        Os recursos do dispositivo devem ser solicitados antes que o dispositivo seja abstraído,
        portanto, pagamos apenas pelo que usamos
    """
    devicesFeatures = VkPhysicalDeviceFeatures()

    enabledLayers = []
    if debug:
        enabledLayers.append("VK_LAYER_KHRONOS_validation")

    createInfo = VkDeviceCreateInfo(
        queueCreateInfoCount = len(queueCreateInfo), 
        pQueueCreateInfos = queueCreateInfo,
        enabledExtensionCount = 0,
        pEnabledFeatures = [devicesFeatures,],
        enabledLayerCount = len(enabledLayers), 
        ppEnabledLayerNames = enabledLayers
    )

    # Se pegarmos algo "[createInfo,] e embrulharmos/wrapper em uma lista, a API do vulkan vai 
    # entender como um ponteiro"
    return vkCreateDevice(
        physicalDevice = physicalDevice, 
        pCreateInfo = [createInfo,], 
        pAllocator = None
    )
   
def get_queues(physicalDevice, logicalDevice, instance, surface, debug):

    indices = find_queue_families(physicalDevice, instance, surface, debug)
    return [
        vkGetDeviceQueue(
            device = logicalDevice,
            queueFamilyIndex = indices.graphicsFamily,
            queueIndex = 0
        ),
        vkGetDeviceQueue(
            device = logicalDevice,
            queueFamilyIndex = indices.presentFamily,
            queueIndex = 0
        ),
    ]