from config import *

"""
    O Vulkan separa o conceito de dispositivos físicos e lógicos. 

    Um dispositivo físico geralmente representa uma única implementação completa do Vulkan 
    (excluindo a funcionalidade ao nível da instância) disponível para o anfitrião, 
    e existe um número finito delas. 
  
    Um dispositivo lógico representa uma instância dessa implementação 
    com o seu próprio estado e recursos independentes de outros dispositivos lógicos.
"""

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