from config import *
import instance
import logging
import device
import time

# https://registry.khronos.org/vulkan/specs/1.3/html/ documentacao vulkan

class Engine:

    def __init__(self):

        #se deve imprimir mensagens de depuração em funções
        self.debugMode = True

        #parâmetros da janela glfw
        self.width = 800
        self.height = 600

        if self.debugMode:
            print(f"{HEADER}:: Criar um motor gráfico{RESET}")

        self.build_gflw_window()
        self.make_instance()
        self.make_device()

    def build_gflw_window(self):

        #inicializar o glfw
        glfw.init()

        #nenhum cliente de renderização padrão, vamos conectar o Vulkan à janela mais tarde
        glfw.window_hint(GLFW_CONSTANTS.GLFW_CLIENT_API, GLFW_CONSTANTS.GLFW_NO_API)
        #o redimensionamento quebra a cadeia de troca, vamos desativá-lo por enquanto
        glfw.window_hint(GLFW_CONSTANTS.GLFW_RESIZABLE, GLFW_CONSTANTS.GLFW_FALSE)
        
        #create_window(int width, int height, const char *title, GLFWmonitor *monitor, GLFWwindow *share)
        self.glfw_title_name = "Vulkan application"
        self.window = glfw.create_window(self.width, self.height, self.glfw_title_name, None, None)
        if self.window is not None:
            if self.debugMode:
                print(f"{OKGREEN}Foi criada com êxito uma janela glfw chamada {self.glfw_title_name}, largura: {self.width}, altura: {self.height}{RESET}\n")
        else:
            if self.debugMode:
                print(f"{FAIL}Falha na criação da janela GLFW{RESET}\n")
  
    def make_instance(self):

        self.instance = instance.make_instance(self.debugMode, self.glfw_title_name)

        if self.debugMode:
            self.debugMessenger = logging.make_debug_messenger(self.instance)

        #criar a surface na janela
        c_style_surface = ffi.new("VkSurfaceKHR*")
        if(
            glfw.create_window_surface(
                instance = self.instance,
                window = self.window,
                allocator = None,
                surface = c_style_surface
            ) != VK_SUCCESS
        ):
            if self.debugMode:
                print(f"{FAIL}Falha ao abstrair a superfície do glfw para o Vulkan{RESET}")
        elif self.debugMode:
            print(f"{OKGREEN}Sucesso na abstração da superfície do glfw para o Vulkan{RESET}")
        
        self.surface = c_style_surface[0]
        
    def make_device(self):

        #escolhe o dispositivo fisico
        self.physicalDevice = device.choose_physical_device(self.instance, self.debugMode)
        

        #envolve a gpu em um dispositivo logico para podermos nos comunicar com ele
            #device.find_queue_families(self.physicalDevice, self.debugMode)
        self.device = device.create_logical_device(
            self.physicalDevice, self.instance, self.surface, self.debugMode)

        #obter fila de gráficos, para que possamos fazer o trabalho com gráficos
        (self.graphicsQueue, self.presentQueue) = device.get_queues(
            physicalDevice = self.physicalDevice, 
            logicalDevice = self.device, 
            instance = self.instance, 
            surface = self.surface,
            debug = self.debugMode
        )

    def close(self):

        if self.debugMode:
            print(f"{HEADER}\nAté logo!\n{RESET}")
        
        vkDestroyDevice(
            device = self.device, 
            pAllocator = None
        )

        destructionFunction = vkGetInstanceProcAddr(self.instance, 'vkDestroySurfaceKHR')
        destructionFunction(
            instance = self.instance, 
            surface = self.surface, 
            pAllocator = None
        )

        if self.debugMode:
            #função de destruição de busca
            destructionFunction = vkGetInstanceProcAddr(self.instance, 'vkDestroyDebugReportCallbackEXT')

            """
                def vkDestroyDebugReportCallbackEXT(
                    instance
                    ,callback
                    ,pAllocator
                ,):
            """
            destructionFunction(
                self.instance, 
                self.debugMessenger, 
                None
            )

        """
            from _vulkan.py:

            def vkDestroyInstance(
                instance,
                pAllocator,
            )
        """
        vkDestroyInstance(
            self.instance, 
            None
        )

	    #encerrar o glfw
        glfw.terminate()

if __name__ == "__main__":

	graphicsEngine = Engine()
    
	graphicsEngine.close()