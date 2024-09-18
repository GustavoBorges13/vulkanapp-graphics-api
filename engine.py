from config import *
import instance
import logging
import device
import swapchain
import frame
import pipeline
import framebuffer
import commands
import sync

# https://registry.khronos.org/vulkan/specs/1.3/html/ documentacao vulkan

class Engine:

    def __init__(self, width, height, window, glfw_title_name, debugMode):
        #nome da janela glfw 
        self.glfw_title_name = glfw_title_name

        #se deve imprimir mensagens de depuração em funções
        self.debugMode = debugMode

        #parâmetros da janela glfw
        self.width = width
        self.height = height

        self.window = window

        if self.debugMode:
            print(f"{HEADER}:: Criar um motor gráfico{RESET}")

        self.make_instance()
        self.make_device()
        self.make_pipeline()
        self.finalize_setup()
  
    def make_instance(self):
        #cria uma instância do Vulkan, que é a base para qualquer aplicação Vulkan.
        self.instance = instance.make_instance(self.debugMode, self.glfw_title_name)

        #se o modo de depuração estiver ativado, cria o camada de validacao
        if self.debugMode:
            self.debugMessenger = logging.make_debug_messenger(self.instance)

        #criar a superfície de renderização a partir da janela GLFW.
        #a superfície permite que o Vulkan interaja com o sistema de janelas para desenhar na tela.
        c_style_surface = ffi.new("VkSurfaceKHR*")

        #tenta criar a superfície da janela usando GLFW e vinculá-la à instância Vulkan.
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

        #armazena a superfície criada no objeto.
        self.surface = c_style_surface[0]
        
    def make_device(self):

        #escolhe o dispositivo físico (GPU) adequado para a aplicação, com base nos critérios fornecidos
        self.physicalDevice = device.choose_physical_device(self.instance, self.debugMode)
        

        #envolve a gpu em um dispositivo logico para podermos nos comunicar com ele
        #device.find_queue_families(self.physicalDevice, self.debugMode)
        self.device = device.create_logical_device(
            self.physicalDevice, self.instance, self.surface, self.debugMode)

        #obtém as filas de gráficos e de apresentação do dispositivo lógico
        #essas filas são necessárias para enviar comandos de renderização e apresentação de imagens
        queues = device.get_queues(
            physicalDevice = self.physicalDevice, 
            logicalDevice = self.device, 
            instance = self.instance, 
            surface = self.surface,
            debug = self.debugMode
        )
        self.graphicsQueue = queues[0]
        self.presentQueue = queues[1]

        #device.query_swapchain_support(self.instance, self.physicalDevice, self.surface, True)
        #criação do swapchain, que gerencia a troca de buffers de renderização (quadros) com a tela
        #ele é essencial para desenhar e apresentar imagens na tela em Vulkan
        bundle = swapchain.create_swapchain(
            self.instance, self.device, self.physicalDevice, self.surface,
            self.width, self.height, self.debugMode
        )

        #atribui os recursos criados pelo swapchain ao objeto atual
        self.swapchain = bundle.swapchain
        self.swapchainFrames = bundle.frames
        self.swapchainFormat = bundle.format
        self.swapchainExtent = bundle.extent

    def make_pipeline(self):

        #criação do pacote de entrada (input bundle) com os parâmetros necessários para criar o pipeline gráfico
        inputBundle = pipeline.InputBundle(
            device = self.device,
            swapchainImageFormat = self.swapchainFormat,
            swapchainExtent = self.swapchainExtent,
            vertexFilepath = "shaders/vert.spv",
            fragmentFilepath = "shaders/frag.spv"
        )

        #criação do pipeline gráfico utilizando o pacote de entrada
        outputBundle = pipeline.create_graphics_pipeline(inputBundle, self.debugMode)

        #configuração do layout do pipeline, renderpass e pipeline em si a partir do bundle de saída   
        self.pipelineLayout = outputBundle.pipelineLayout
        self.renderpass = outputBundle.renderPass
        self.pipeline = outputBundle.pipeline        

    def finalize_setup(self):

        #frame buffers
        framebufferInput = framebuffer.framebufferInput()
        framebufferInput.device = self.device
        framebufferInput.renderpass = self.renderpass # para escolher quais os frames que serao utilizados
        framebufferInput.swapchainExtent = self.swapchainExtent
        framebuffer.make_framebuffers(
            framebufferInput, self.swapchainFrames, self.debugMode
        )

        #piscina de comandos -> command pools
        commandPoolInput = commands.commandPoolInputChunk()
        commandPoolInput.device = self.device
        commandPoolInput.physicalDevice = self.physicalDevice
        commandPoolInput.surface = self.surface
        commandPoolInput.instance = self.instance
        self.commandPool = commands.make_command_pool(
            commandPoolInput, self.debugMode
        )

        #alocar um monte de buffers de comando
        commandbufferInput = commands.commandbufferInputChunk()
        commandbufferInput.device = self.device
        commandbufferInput.commandPool = self.commandPool
        commandbufferInput.frames = self.swapchainFrames
        self.mainCommandbuffer = commands.make_command_buffers(
            commandbufferInput, self.debugMode
        )

        """
        Primitivos de sincronização:
        - inFlightFence: Usado para garantir que as operações de renderização estejam concluídas antes de avançar para o próximo quadro.
        - imageAvailable: Semáforo sinalizado quando uma imagem do swapchain está disponível para uso. O trabalho gráfico só pode prosseguir após essa sinalização.
        - renderFinished: Semáforo sinalizado quando a renderização do quadro atual está concluída. Espera-se que o sistema só apresente a imagem quando esta semáforo estiver sinalizado, indicando que a renderização foi finalizada corretamente.
        Nao podemos apresentar uma imagem ate que ela tenha sido processada corretamente.
        """
        self.inFlightFence = sync.make_fence(self.device, self.debugMode)
        self.imageAvailable = sync.make_semaphore(self.device, self.debugMode)
        self.renderFinished = sync.make_semaphore(self.device, self.debugMode)
        
    def record_draw_commands(self, commandBuffer, imageIndex):

        """
        Etapas para gravar os comandos de desenho no buffer de comando:
            1. Iniciar o buffer de comando.
            2. Definir as informações necessárias para iniciar uma passagem de renderização (renderpass).
            Isso inclui a área de renderização e os valores de limpeza.
            3. Iniciar a passagem de renderização, vincular o pipeline gráfico que contém os shaders.
            Em seguida, emitir o comando para desenhar o conteúdo.
        """
        beginInfo = VkCommandBufferBeginInfo()

        try:
            vkBeginCommandBuffer(commandBuffer, beginInfo)
        except:
            if self.debugMode:
                print(f"{FAIL}Falha ao iniciar o buffer de comando de gravação{RESET}")

        #configura as informações da renderpass, incluindo a área de renderização e o framebuffer
        renderpassInfo = VkRenderPassBeginInfo(
            renderPass = self.renderpass,
            framebuffer = self.swapchainFrames[imageIndex].framebuffer,
            renderArea = [[0,0], self.swapchainExtent]
        )

        #define o valor de limpeza da tela para cada quadro (limpa com a cor especificada)
        clearColor = VkClearValue([[1.0, 0.5, 0.25, 1.0]]) # Limpa a tela com cor laranja suave em cada quadro
        renderpassInfo.clearValueCount = 1
        renderpassInfo.pClearValues = ffi.addressof(clearColor)
        
        #iniciar a renderpass, indicando que os comandos subsequentes serão gráficos
        vkCmdBeginRenderPass(commandBuffer, renderpassInfo, VK_SUBPASS_CONTENTS_INLINE)

        #vincular o pipeline gráfico, que contém os shaders e o estado do pipeline
        vkCmdBindPipeline(commandBuffer, VK_PIPELINE_BIND_POINT_GRAPHICS, self.pipeline)

        #emitir o comando de desenho para desenhar 3 vértices (um triângulo)
        vkCmdDraw(
            commandBuffer = commandBuffer, vertexCount = 3, 
            instanceCount = 1, firstVertex = 0, firstInstance = 0
        )

        #finalizar a renderpass
        vkCmdEndRenderPass(commandBuffer)

        #finalizar o buffer de comando
        try:
            vkEndCommandBuffer(commandBuffer)
        except:
            if self.debugMode:
                print(f"{FAIL}Falha ao terminar o buffer de comando de gravação{RESET}")

    def render(self):

        #procedimentos de instância de captura
        vkAcquireNextImageKHR = vkGetDeviceProcAddr(self.device, 'vkAcquireNextImageKHR')
        vkQueuePresentKHR = vkGetDeviceProcAddr(self.device, 'vkQueuePresentKHR')


        #verificar se a cerca (caminho) esta aberta
        #verifica se a cerca (fence) está sinalizada, garantindo que o processamento do quadro anterior foi concluído.
        vkWaitForFences(
            device = self.device, fenceCount = 1, pFences = [self.inFlightFence,], 
            waitAll = VK_TRUE, timeout = 1000000000
        ) # Timeout em nanosegundos (1 segundo)

        #reseta a fence para ser usada no próximo quadro
        vkResetFences(
            device = self.device, fenceCount = 1, pFences = [self.inFlightFence,]
        )

        #adquire o próximo índice de imagem do swapchain. Isso bloqueia até que a imagem esteja disponível
        # ou o timeout seja atingido. O semáforo `imageAvailable` será sinalizado quando a imagem estiver disponível.
        imageIndex = vkAcquireNextImageKHR(
            device = self.device, swapchain = self.swapchain, timeout = 1000000000, 
            semaphore = self.imageAvailable, fence = VK_NULL_HANDLE
        )

        #resetar o buffer de comando para o quadro atual
        commandBuffer = self.swapchainFrames[imageIndex].commandbuffer
        vkResetCommandBuffer(commandBuffer = commandBuffer, flags = 0)

        #grava os comandos de desenho no buffer de comando
        self.record_draw_commands(commandBuffer, imageIndex)

        #configurar as informações para submissão dos comandos à fila gráfica
        submitInfo = VkSubmitInfo(
            waitSemaphoreCount = 1, pWaitSemaphores = [self.imageAvailable,], 
            pWaitDstStageMask=[VK_PIPELINE_STAGE_COLOR_ATTACHMENT_OUTPUT_BIT,],
            commandBufferCount = 1, pCommandBuffers = [commandBuffer,], signalSemaphoreCount = 1,
            pSignalSemaphores = [self.renderFinished,]
        )

        #submete o comando de desenho à fila gráfica e usa a fence para sincronização
        try:
            vkQueueSubmit(
                queue = self.graphicsQueue, submitCount = 1, 
                pSubmits = submitInfo, fence = self.inFlightFence
            )
        except:
            if self.debugMode:
                print("Falha ao enviar comandos de desenho")

        #configurar e realizar a apresentação da imagem renderizada
        presentInfo = VkPresentInfoKHR(
            waitSemaphoreCount = 1, pWaitSemaphores = [self.renderFinished,],
            swapchainCount = 1, pSwapchains = [self.swapchain,],
            pImageIndices = [imageIndex,]
        )

        #apresenta a imagem à fila de apresentação
        vkQueuePresentKHR(self.presentQueue, presentInfo)

    def close(self):
        vkDeviceWaitIdle(self.device)

        if self.debugMode:
            print(f"{HEADER}\nAté logo!\n{RESET}")

        vkDestroyFence(self.device, self.inFlightFence, None)
        vkDestroySemaphore(self.device, self.imageAvailable, None)
        vkDestroySemaphore(self.device, self.renderFinished, None)
        vkDestroyCommandPool(self.device, self.commandPool, None)
        vkDestroyPipeline(self.device, self.pipeline, None)
        vkDestroyPipelineLayout(self.device, self.pipelineLayout, None)
        vkDestroyRenderPass(self.device, self.renderpass, None)
        for frame in self.swapchainFrames:
            vkDestroyImageView(
                device = self.device, imageView = frame.image_view, pAllocator = None
            )
            vkDestroyFramebuffer(
                device = self.device, framebuffer = frame.framebuffer, pAllocator = None
            )
        destructionFunction = vkGetDeviceProcAddr(self.device, 'vkDestroySwapchainKHR')
        destructionFunction(self.device, self.swapchain, None)
        vkDestroyDevice(
            device = self.device, pAllocator = None
        )
        destructionFunction = vkGetInstanceProcAddr(self.instance, "vkDestroySurfaceKHR")
        destructionFunction(self.instance, self.surface, None)
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
        glfw.terminate()