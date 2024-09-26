from config import *
import logging
import queue_families  
import tkinter as tk
from tkinter import messagebox

validationLayers = ["VK_LAYER_KHRONOS_validation"]

"""
    O Vulkan separa o conceito de dispositivos físicos e lógicos. 

    Um dispositivo físico geralmente representa uma única implementação completa do Vulkan 
    (excluindo a funcionalidade ao nível da instância) disponível para o anfitrião, 
    e existe um número finito delas. 
  
    Um dispositivo lógico representa uma instância dessa implementação 
    com o seu próprio estado e recursos independentes de outros dispositivos lógicos.
"""

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
            logging.log_device_properties(device)
        if is_suitable(device, debug):
            return device

    return None

def create_logical_device(physicalDevice, instance, surface, debug):

    """
        Criar uma abstração em torno da GPU
    """

    """
        No momento da criação, todas as filas necessárias também serão criadas,
        portanto, as informações de criação de fila devem ser passadas em
    """

    indices = queue_families.find_queue_families(physicalDevice, instance, surface, debug)
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
        enabledLayers.extend(validationLayers)

    deviceExtensions = [
        VK_KHR_SWAPCHAIN_EXTENSION_NAME,
    ]



    createInfo = VkDeviceCreateInfo(
        queueCreateInfoCount = len(queueCreateInfo), 
        pQueueCreateInfos = queueCreateInfo,
        enabledExtensionCount = len(deviceExtensions),
        ppEnabledExtensionNames= deviceExtensions,
        pEnabledFeatures = [devicesFeatures,],
        enabledLayerCount = len(enabledLayers), 
        ppEnabledLayerNames = enabledLayers
    )

    """
    # Cria uma janela oculta
    root = tk.Tk()
    root.withdraw()  # Esconde a janela principal

    # Exibe a caixa de mensagem
    messagebox.showinfo("TESTE", f"Resultado do createInfo: {createInfo}\nResultado do [createInfo,]: {[createInfo,]}")
    print(f"Resultado do createInfo: {createInfo}\nResultado do [createInfo,]: {[createInfo,]}")
    # Fecha o aplicativo após o fechamento da mensagem
    root.destroy()
    """

    # Se pegarmos algo "[createInfo,] e embrulharmos/wrapper em uma lista, a API do vulkan vai 
    # entender como um ponteiro"
    return vkCreateDevice(
        physicalDevice = physicalDevice, 
        pCreateInfo = [createInfo,], 
        pAllocator = None
    )

def get_queues(physicalDevice, logicalDevice, instance, surface, debug):

    indices = queue_families.find_queue_families(physicalDevice, instance, surface, debug)
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

