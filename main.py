from config import *
import instance
import logging
import device
import time

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
                print(f"{OKGREEN}Successfully made a glfw window called {self.glfw_title_name}, width: {self.width}, height: {self.height}{RESET}\n")
        else:
            if self.debugMode:
                print(f"{FAIL}GLFW window creation failed{RESET}\n")
  
    def make_instance(self):

        self.instance = instance.make_instance(self.debugMode, self.glfw_title_name)

        if self.debugMode:
            self.debugMessenger = logging.make_debug_messenger(self.instance)
    
    def make_device(self):

        self.physicalDevice = device.choose_physical_device(self.instance, self.debugMode)

    def close(self):

        if self.debugMode:
            print(f"{HEADER}\nAté logo!\n{RESET}")
        
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
            destructionFunction(self.instance, self.debugMessenger, None)

        """
            from _vulkan.py:

            def vkDestroyInstance(
                instance,
                pAllocator,
            )
        """
        vkDestroyInstance(self.instance, None)

	    #encerrar o glfw
        time.sleep(5)
        glfw.terminate()

if __name__ == "__main__":

	graphicsEngine = Engine()
    
	graphicsEngine.close()