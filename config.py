#carregar estaticamente a biblioteca vulkan
from vulkan import *
from colors import *

"""
 Ligar estaticamente o cabeçalho pré-construído do sdk do lunarg irá carregar
 a maioria das funções, mas não todas.
 
 As funções também podem ser carregadas dinamicamente, usando a chamada
 
 PFN_vkVoidFunction vkGetInstanceProcAddr(
    instância VkInstance,
    string pName);

 ou

 PFN_vkVoidFunction vkGetDeviceProcAddr(
	dispositivo VkDevice,
	string pName);

	Veremos isto mais tarde, quando tivermos criado uma instância e um dispositivo.
"""

import glfw
import glfw.GLFW as GLFW_CONSTANTS

# PT-BR console
import sys
import io

# Configurar o padrão de codificação para UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')