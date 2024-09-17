from config import *
import instance
import vklogging
import device
import swapchain
import pipeline
import framebuffer
import commands
import sync
import vertex_menagerie
import descriptors
import frame
import scene
import image

# https://registry.khronos.org/vulkan/specs/1.3/html/ documentacao vulkan

class Engine:

    def __init__(self, width, height, window, glfw_title_name):
        #nome da janela glfw 
        self.glfw_title_name = glfw_title_name

        #parâmetros da janela glfw
        self.width = width
        self.height = height

        self.window = window

        vklogging.logger.print(f"{HEADER}:: Criar um motor gráfico (ENGINE){RESET}")

        self.make_instance()
        self.make_device()
        self.make_descriptor_set_layout()
        self.make_pipeline()
        self.finalize_setup()
        self.make_assets()
  
    def make_instance(self):
        #cria uma instância do Vulkan, que é a base para qualquer aplicação Vulkan.
        self.instance = instance.make_instance(self.glfw_title_name)

        #se o modo de depuração estiver ativado, cria o mensageiro de depuração
        if vklogging.logger.debug_mode:
            self.debugMessenger = vklogging.make_debug_messenger(self.instance)

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
            vklogging.logger.print(f"{FAIL}Falha ao criar a superfície da janela com GLFW para o Vulkan{RESET}")
        else:
            vklogging.logger.print(f"{OKGREEN}Superfície (surface) da janela criada com sucesso e vinculada ao Vulkan{RESET}")

        #armazena a superfície criada no objeto.
        self.surface = c_style_surface[0]
        
    def make_device(self):

        #escolhe o dispositivo físico (GPU) adequado para a aplicação, com base nos critérios fornecidos
        self.physicalDevice = device.choose_physical_device(self.instance)
        

        #envolve a gpu em um dispositivo logico para podermos nos comunicar com ele
            #device.find_queue_families(self.physicalDevice, self.debug_mode)
        self.device = device.create_logical_device(
            self.physicalDevice, self.instance, self.surface)

        #obtém as filas de gráficos e de apresentação do dispositivo lógico
        #essas filas são necessárias para enviar comandos de renderização e apresentação de imagens
        queues = device.get_queues(
            physicalDevice = self.physicalDevice, 
            logicalDevice = self.device, 
            instance = self.instance, 
            surface = self.surface,
        )
        self.graphicsQueue = queues[0]
        self.presentQueue = queues[1]

        #cria swapchain (cadeia de trocas)
        self.make_swapchain()

        self.frameNumber = 0

    def make_swapchain(self):
        """
            Cria a cadeia de troca do mecanismo; observe que isso criará imagens e visualizações de imagens, mas não criará quadros prontos para renderização.
            e visualizações de imagem, mas não deixará os quadros prontos para renderização.
        """
        #device.query_swapchain_support(self.instance, self.physicalDevice, self.surface, True)
        #criação do swapchain, que gerencia a troca de buffers de renderização (quadros) com a tela
        #ele é essencial para desenhar e apresentar imagens na tela em Vulkan
        bundle = swapchain.create_swapchain(
            self.instance, self.device, self.physicalDevice, self.surface,
            self.width, self.height
        )

        #atribui os recursos criados pelo swapchain ao objeto atual
        self.swapchain = bundle.swapchain
        self.swapchainFrames = bundle.frames
        self.swapchainFormat = bundle.format
        self.swapchainExtent = bundle.extent
        self.maxFramesInFlight = len(self.swapchainFrames)

    def recreate_swapchain(self):
        """
            Destruir a cadeia de troca atual e, em seguida, reconstruir uma nova cadeia
        """

        self.width = 0
        self.height = 0
        while (self.width == 0 or self.height == 0):
            self.width, self.height = glfw.get_window_size(self.window)
            glfw.wait_events()

        vkDeviceWaitIdle(self.device)
        self.cleanup_swapchain()

        self.make_swapchain()
        self.make_framebuffers()
        self.make_frame_command_buffers()
        self.make_frame_resources()
    
    def make_descriptor_set_layout(self):
        """
            Criar uma classe de estrutura de ligações e preenche-la.
        """
        bindings = descriptors.DescriptorSetLayoutData()
        bindings.count = 2

        bindings.indices.append(0)
        bindings.types.append(VK_DESCRIPTOR_TYPE_UNIFORM_BUFFER)
        bindings.counts.append(1)
        bindings.stages.append(VK_SHADER_STAGE_VERTEX_BIT)

        bindings.indices.append(1)
        bindings.types.append(VK_DESCRIPTOR_TYPE_STORAGE_BUFFER)
        bindings.counts.append(1)
        bindings.stages.append(VK_SHADER_STAGE_VERTEX_BIT)

        self.frameDescriptorSetLayout = descriptors.make_descriptor_set_layout(
            self.device, bindings
        )

        bindings.count = 1

        bindings.indices[0] = 0
        bindings.types[0] = VK_DESCRIPTOR_TYPE_COMBINED_IMAGE_SAMPLER
        bindings.counts[0] = 1
        bindings.stages[0] = VK_SHADER_STAGE_FRAGMENT_BIT

        self.materialDescriptorSetLayout = descriptors.make_descriptor_set_layout(
            self.device, bindings
        )

    def make_pipeline(self):

        #criação do pacote de entrada (input bundle) com os parâmetros necessários para criar o pipeline gráfico
        inputBundle = pipeline.InputBundle(
            device = self.device,
            swapchainImageFormat = self.swapchainFormat,
            swapchainExtent = self.swapchainExtent,
            vertexFilepath = "shaders/vert.spv",
            fragmentFilepath = "shaders/frag.spv",
            descriptorSetLayouts = [
                self.frameDescriptorSetLayout, 
                self.materialDescriptorSetLayout
            ]
        )

        #criação do pipeline gráfico utilizando o pacote de entrada
        outputBundle = pipeline.create_graphics_pipeline(inputBundle)

        #configuração do layout do pipeline, renderpass e pipeline em si a partir do bundle de saída   
        self.pipelineLayout = outputBundle.pipelineLayout
        self.renderpass = outputBundle.renderPass
        self.pipeline = outputBundle.pipeline       

    def make_framebuffers(self):
        """
            Cria um framebuffer para cada quadro na cadeia de troca.
        """
        #frame buffers
        framebufferInput = framebuffer.framebufferInput()
        framebufferInput.device = self.device
        framebufferInput.renderpass = self.renderpass
        framebufferInput.swapchainExtent = self.swapchainExtent
        framebuffer.make_framebuffers(
            framebufferInput, self.swapchainFrames
        )

    def make_frame_command_buffers(self):
        """
            Crie um buffer de comando para cada quadro na cadeia de troca.
        """
        #alocar um monte de buffers de comando
        commandbufferInput = commands.commandbufferInputChunk()
        commandbufferInput.device = self.device
        commandbufferInput.commandPool = self.commandPool
        commandbufferInput.frames = self.swapchainFrames 
        commands.make_frame_command_buffers(commandbufferInput)

    def make_frame_resources(self):
        """
            Crie os semáforos e as cercas necessárias para renderizar cada quadro.
        """

        bindings = descriptors.DescriptorSetLayoutData()
        bindings.types.append(VK_DESCRIPTOR_TYPE_UNIFORM_BUFFER)
        bindings.types.append(VK_DESCRIPTOR_TYPE_STORAGE_BUFFER)

        self.descriptorPool = descriptors.make_descriptor_pool(
            device = self.device, size = len(self.swapchainFrames), 
            bindings = bindings
        )

        """
        Primitivos de sincronização  (singlethreading)
        - inFlightFence: Usado para garantir que as operações de renderização estejam concluídas antes de avançar para o próximo quadro.
        - imageAvailable: Semáforo sinalizado quando uma imagem do swapchain está disponível para uso. O trabalho gráfico só pode prosseguir após essa sinalização.
        - renderFinished: Semáforo sinalizado quando a renderização do quadro atual está concluída. Espera-se que o sistema só apresente a imagem quando esta semáforo estiver sinalizado, indicando que a renderização foi finalizada corretamente.
        
        Como estamos no contexto singlethreading, todos os quadros compartilham o mesmo conjunto de semáforos e fences. Isso significa que a renderização de cada quadro deve ser sequencial e sincronizada, garantindo que não haja concorrência entre quadros.
        Não podemos apresentar uma imagem até que ela tenha sido processada corretamente, e a sincronização é feita de maneira linear no ciclo de renderização.
        """
        #singleThread rendering
        #self.inFlightFence = sync.make_fence(self.device, self.debug_mode)
        #self.imageAvailable = sync.make_semaphore(self.device, self.debug_mode)
        #self.renderFinished = sync.make_semaphore(self.device, self.debug_mode)

        """
        Primitivos de sincronização (multithreading)
        - inFlightFence: Usado para garantir que as operações de renderização estejam concluídas antes de avançar para o próximo quadro.
        - imageAvailable: Semáforo sinalizado quando uma imagem do swapchain está disponível para uso. O trabalho gráfico só pode prosseguir após essa sinalização.
        - renderFinished: Semáforo sinalizado quando a renderização do quadro atual está concluída. Espera-se que o sistema só apresente a imagem quando esta semáforo estiver sinalizado, indicando que a renderização foi finalizada corretamente.
        
        Como agora estamos no contexto multithreading, cada quadro do swapchain possui seus próprios semáforos e fences, permitindo que múltiplos quadros sejam renderizados simultaneamente em threads diferentes, se necessário.
        Não podemos apresentar uma imagem até que ela tenha sido processada corretamente e a sincronização entre as threads garante que isso seja feito de forma ordenada.
        """
        #multithreading rendering
        #criacao do objeto de sincronizacao -> semaforos e cercas (fences)
        for frame in self.swapchainFrames:
            frame.inFlight = sync.make_fence(self.device)
            frame.imageAvailable = sync.make_semaphore(self.device)
            frame.renderFinished = sync.make_semaphore(self.device)

            frame.make_descriptor_resources(self.device, self.physicalDevice)

            frame.descriptorSet = descriptors.allocate_descriptor_set(
                self.device, self.descriptorPool, self.frameDescriptorSetLayout
            )

    def finalize_setup(self):

        #cria framebuffers
        self.make_framebuffers()

        #piscina de comandos -> command pools
        commandPoolInput = commands.commandPoolInputChunk()
        commandPoolInput.device = self.device
        commandPoolInput.physicalDevice = self.physicalDevice
        commandPoolInput.surface = self.surface
        commandPoolInput.instance = self.instance
        self.commandPool = commands.make_command_pool(commandPoolInput)

        #alocar um monte de buffers de comando
        commandbufferInput = commands.commandbufferInputChunk()
        commandbufferInput.device = self.device
        commandbufferInput.commandPool = self.commandPool
        commandbufferInput.frames = self.swapchainFrames
        self.mainCommandbuffer = commands.make_command_buffer(commandbufferInput)
        commands.make_frame_command_buffers(commandbufferInput)

        #criacao do objeto de sincronizacao -> semaforos e cercas (fences)
        self.make_frame_resources()

    def make_assets(self):

        self.meshes = vertex_menagerie.VertexMenagerie()
        
        vertices = np.array(
            (
                 0.0, -0.1, 0.0, 1.0, 0.0, 0.5, 0.0, #0
                 0.1,  0.1, 0.0, 1.0, 0.0, 1.0, 1.0, #1
                -0.1,  0.1, 0.0, 1.0, 0.0, 0.0, 1.0  #2
            ), dtype = np.float32
        )
        indices = [0, 1, 2]

        meshType = TRIANGLE
        self.meshes.consume(meshType, vertices, indices)

        vertices = np.array(
            (
                -0.1,  0.1, 1.0, 0.0, 0.0, 0.0, 1.0, #0
		        -0.1, -0.1, 1.0, 0.0, 0.0, 0.0, 0.0, #1
		         0.1, -0.1, 1.0, 0.0, 0.0, 1.0, 0.0, #2
		         0.1,  0.1, 1.0, 0.0, 0.0, 1.0, 1.0, #3
            ), dtype = np.float32
        )
        indices = [
            0, 1, 2,
            2, 3, 0
        ]

        meshType = SQUARE
        self.meshes.consume(meshType, vertices, indices)

        vertices = np.array(
            (
                 -0.1, -0.05, 1.0, 1.0, 1.0, 0.0, 0.25, #0
		        -0.04, -0.05, 1.0, 1.0, 1.0, 0.3, 0.25, #1
		        -0.06,   0.0, 1.0, 1.0, 1.0, 0.2,  0.5, #2
		          0.0,  -0.1, 1.0, 1.0, 1.0, 0.5,  0.0, #3
		         0.04, -0.05, 1.0, 1.0, 1.0, 0.7, 0.25, #4
		          0.1, -0.05, 1.0, 1.0, 1.0, 1.0, 0.25, #5
		         0.06,   0.0, 1.0, 1.0, 1.0, 0.8,  0.5, #6
		         0.08,   0.1, 1.0, 1.0, 1.0, 0.9,  1.0, #7
		          0.0,  0.02, 1.0, 1.0, 1.0, 0.5,  0.6, #8
		        -0.08,   0.1, 1.0, 1.0, 1.0, 0.1,  1.0  #9
            ), dtype = np.float32
        )
        indices = [
            0, 1, 2,
            1, 3, 4,
            2, 1, 4,
            4, 5, 6,
            2, 4, 6,
            6, 7, 8,
            2, 6, 8,
            2, 8, 9
        ]

        meshType = STAR
        self.meshes.consume(meshType, vertices, indices)

        finalization_chunk = vertex_menagerie.VertexBufferFinalizationChunk()
        finalization_chunk.command_buffer = self.mainCommandbuffer
        finalization_chunk.logical_device = self.device
        finalization_chunk.physical_device = self.physicalDevice
        finalization_chunk.queue = self.graphicsQueue
        self.meshes.finalize(finalization_chunk)

        #Materiais
        self.materials: dict[int, image.Texture] = {}
        filenames = {
            TRIANGLE: "tex/grama.jpg",
            SQUARE: "tex/rocha.jpg",
            STAR: "tex/cristal.jpg"
        }

        bindings = descriptors.DescriptorSetLayoutData()
        bindings.count = 1
        bindings.types.append(VK_DESCRIPTOR_TYPE_COMBINED_IMAGE_SAMPLER)
        self.materialDescriptorPool = descriptors.make_descriptor_pool(
            device = self.device, size = len(filenames), bindings = bindings
        )

        textureInfo = image.TextureInputChunk()
        textureInfo.descriptorPool = self.materialDescriptorPool
        textureInfo.descriptorSetLayout = self.materialDescriptorSetLayout
        textureInfo.logicalDevice = self.device
        textureInfo.physicalDevice = self.physicalDevice
        textureInfo.commandBuffer = self.mainCommandbuffer
        textureInfo.queue = self.graphicsQueue

        for (objectType, filename) in filenames.items():
            textureInfo.filename = filename
            self.materials[objectType] = image.Texture(textureInfo)

    def prepare_frame(self, imageIndex: int, _scene: scene.Scene) -> None:

        _frame: frame.SwapChainFrame = self.swapchainFrames[imageIndex]

        position = np.array([1, 0, -1],dtype=np.float32)
        target = np.array([0, 0, 0],dtype=np.float32)
        up = np.array([0, 0, -1],dtype=np.float32)
        _frame.cameraData.view = pyrr.matrix44.create_look_at(position, target, up, dtype=np.float32)

        fov = 45
        aspect = self.swapchainExtent.width/float(self.swapchainExtent.height)
        near = 0.1
        far = 10
        _frame.cameraData.projection = pyrr.matrix44.create_perspective_projection(fov, aspect, near, far, dtype=np.float32)
        _frame.cameraData.projection[1][1] *= -1

        _frame.cameraData.view_projection = pyrr.matrix44.multiply(
            m1 = _frame.cameraData.view, m2 = _frame.cameraData.projection
        )

        flattened_data = _frame.cameraData.view.astype("f").tobytes() \
            + _frame.cameraData.projection.astype("f").tobytes() \
            + _frame.cameraData.view_projection.astype("f").tobytes()
        
        bufferSize = 3 * 4 * 4 * 4
        ffi.memmove(
            dest = _frame.uniformBufferWriteLocation, 
            src = flattened_data, n = bufferSize
        )

        i = 0
        for position in _scene.triangle_positions:
            
            _frame.modelTransforms[i] = pyrr.matrix44.create_from_translation(
                vec = position, dtype = np.float32
            )
            i += 1
        
        for position in _scene.square_positions:
            
            _frame.modelTransforms[i] = pyrr.matrix44.create_from_translation(
                vec = position, dtype = np.float32
            )
            i += 1
        
        for position in _scene.star_positions:
            
            _frame.modelTransforms[i] = pyrr.matrix44.create_from_translation(
                vec = position, dtype = np.float32
            )
            i += 1
        
        flattened_data = _frame.modelTransforms.astype("f").tobytes()
        
        bufferSize = i * 16 * 4
        ffi.memmove(
            dest = _frame.modelBufferWriteLocation, 
            src = flattened_data, n = bufferSize
        )

        _frame.write_descriptor_set(self.device)

    def prepare_scene(self, commandBuffer):
        """
            Preparar cena para renderizar
        """
        #vincular buffers de vertice em uma lista de buffers
        vkCmdBindVertexBuffers(
            commandBuffer = commandBuffer, firstBinding = 0,
            bindingCount = 1, pBuffers = (self.meshes.vertexBuffer.buffer,),
            pOffsets = (0,)
        )

        #vincular o buffer de indice
        #precisamos vincular os buffers de vertice e de indice
        # para que possamos nos referir adequadamente a cada um deles
        vkCmdBindIndexBuffer(
            commandBuffer = commandBuffer, buffer = self.meshes.indexBuffer.buffer,
            offset = 0, indexType =  VK_INDEX_TYPE_UINT32
        )

    def record_draw_commands(self, commandBuffer, imageIndex, _scene: scene.Scene):

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
            vklogging.logger.print(f"{FAIL}Falha ao iniciar o buffer de comando de gravação{RESET}")

        #configura as informações da renderpass, incluindo a área de renderização e o framebuffer
        renderpassInfo = VkRenderPassBeginInfo(
            renderPass = self.renderpass,
            framebuffer = self.swapchainFrames[imageIndex].framebuffer,
            renderArea = [[0,0], self.swapchainExtent]
        )

        vkCmdBindDescriptorSets(
            commandBuffer=commandBuffer, 
            pipelineBindPoint=VK_PIPELINE_BIND_POINT_GRAPHICS,
            layout = self.pipelineLayout,
            firstSet = 0, descriptorSetCount = 1, 
            pDescriptorSets=[self.swapchainFrames[imageIndex].descriptorSet,],
            dynamicOffsetCount = 0, pDynamicOffsets=[0,]
        )

        #define o valor de limpeza da tela para cada quadro (limpa com a cor especificada)
        clearColor = VkClearValue([[1.0, 0.5, 0.25, 1.0]]) # Limpa a tela com cor laranja suave em cada quadro
        renderpassInfo.clearValueCount = 1
        renderpassInfo.pClearValues = ffi.addressof(clearColor)
        
        #iniciar a render pass, indicando que os comandos subsequentes serão gráficos.
        #isso estabelece o contexto de renderização para o framebuffer de destino.
        vkCmdBeginRenderPass(commandBuffer, renderpassInfo, VK_SUBPASS_CONTENTS_INLINE)

        #vincular o pipeline gráfico, que contém os shaders e o estado do pipeline.
        #a partir deste ponto, todas as operações seguirão as configurações definidas no pipeline.
        vkCmdBindPipeline(commandBuffer, VK_PIPELINE_BIND_POINT_GRAPHICS, self.pipeline)


        #preparar cena para desenhar o vertex_menagerie
        self.prepare_scene(commandBuffer)
        firstInstance = 0
        
        #desenha triangulo 2d
        firstInstance = self.render_objects(
            commandBuffer, TRIANGLE, firstInstance, len(_scene.triangle_positions)
        )
        
        #desenha cubo 2d
        firstInstance = self.render_objects(
            commandBuffer, SQUARE, firstInstance, len(_scene.square_positions)
        )

        #desenha estrela 2d
        firstInstance = self.render_objects(
            commandBuffer, STAR, firstInstance, len(_scene.star_positions)
        )
            
        #finalizar a renderpass
        vkCmdEndRenderPass(commandBuffer)

        #finalizar o buffer de comando
        try:
            vkEndCommandBuffer(commandBuffer)
        except:
            vklogging.logger.print(f"{FAIL}Falha ao terminar o buffer de comando de gravação{RESET}")

    def render_objects(
        self, commandBuffer, objectType: int, firstInstance: int, instanceCount: int) -> int:

        self.materials[objectType].use(commandBuffer, self.pipelineLayout)

        firstIndex = self.meshes.firstIndices[objectType]
        indexCount = self.meshes.indexCounts[objectType]
        vkCmdDrawIndexed(
            commandBuffer = commandBuffer, 
            indexCount = indexCount, instanceCount = instanceCount, 
            firstIndex = firstIndex, vertexOffset = 0,
            firstInstance = firstInstance
        )
        
        return firstInstance + instanceCount

    def render(self, _scene: scene.Scene):

        #procedimentos de instância de captura
        vkAcquireNextImageKHR = vkGetDeviceProcAddr(self.device, 'vkAcquireNextImageKHR')
        vkQueuePresentKHR = vkGetDeviceProcAddr(self.device, 'vkQueuePresentKHR')
        
        # (multithreading)
        # Sincronização inicial: verifica se o quadro anterior já foi processado completamente.
        # Aqui, estamos esperando que a fence associada ao quadro atual (self.frameNumber) seja sinalizada,
        # indicando que a execução anterior terminou. Isso é essencial para evitar sobrescrita do buffer de comandos.
        vkWaitForFences(
            device = self.device, fenceCount = 1, pFences = [self.swapchainFrames[self.frameNumber].inFlight,], 
            waitAll = VK_TRUE, timeout = 1000000000
        ) # Timeout em nanosegundos (1 segundo)

        # Após verificar a fence, ela é resetada para ser reutilizada na próxima submissão de comandos.
        vkResetFences(
            device = self.device, fenceCount = 1, pFences = [self.swapchainFrames[self.frameNumber].inFlight,]
        )

        # Adquire o índice da próxima imagem disponível do swapchain para renderização.
        # Essa operação é bloqueante até que a imagem esteja disponível ou o timeout seja atingido.
        # O semáforo 'imageAvailable' será sinalizado quando a imagem estiver pronta.
        try:
            imageIndex = vkAcquireNextImageKHR(
                device = self.device, swapchain = self.swapchain, timeout = 1000000000, 
                semaphore = self.swapchainFrames[self.frameNumber].imageAvailable, fence = VK_NULL_HANDLE
            )
        except:
            vklogging.logger.print("recriar a cadeia de troca")
            self.recreate_swapchain()
            return
        
        # Reseta o comando de buffer associado ao frame atual para preparar novos comandos de desenho.
        commandBuffer = self.swapchainFrames[self.frameNumber].commandbuffer
        vkResetCommandBuffer(commandBuffer = commandBuffer, flags = 0)

        self.prepare_frame(imageIndex, _scene)
                # Grava os comandos de desenho no buffer de comando para o índice de imagem obtido.
        # Isso inclui comandos de renderização, configuração de estados e envio dos dados da cena.
        self.record_draw_commands(commandBuffer, imageIndex, _scene)

        # Configura as informações necessárias para submeter os comandos à fila gráfica.
        # Isso inclui sincronizar com o semáforo 'imageAvailable' e sinalizar o semáforo 'renderFinished'
        # quando o processamento do quadro estiver completo.
        submitInfo = VkSubmitInfo(
            waitSemaphoreCount = 1, pWaitSemaphores = [self.swapchainFrames[self.frameNumber].imageAvailable,], 
            pWaitDstStageMask=[VK_PIPELINE_STAGE_COLOR_ATTACHMENT_OUTPUT_BIT,],
            commandBufferCount = 1, pCommandBuffers = [commandBuffer,], signalSemaphoreCount = 1,
            pSignalSemaphores = [self.swapchainFrames[self.frameNumber].renderFinished,]
        )

        # Submete o buffer de comando à fila gráfica.
        # A fence associada é usada para garantir que o quadro atual seja finalizado antes de ser reutilizado.
        try:
            vkQueueSubmit(
                queue = self.graphicsQueue, submitCount = 1, 
                pSubmits = submitInfo, fence = self.swapchainFrames[self.frameNumber].inFlight
            )
        except:
            vklogging.logger.print("Falha ao enviar comandos de desenho")
            self.recreate_swapchain()
            return


        # Configura as informações necessárias para a apresentação da imagem.
        # Isso inclui garantir que a imagem só será apresentada após o semáforo 'renderFinished' ser sinalizado,
        # o que indica que a renderização está concluída.
        presentInfo = VkPresentInfoKHR(
            waitSemaphoreCount = 1, pWaitSemaphores = [self.swapchainFrames[self.frameNumber].renderFinished,],
            swapchainCount = 1, pSwapchains = [self.swapchain,],
            pImageIndices = [imageIndex,]
        )

        # Apresenta a imagem renderizada na fila de apresentação (tipicamente, na tela).
        try:
            vkQueuePresentKHR(self.presentQueue, presentInfo)
        except:
            vklogging.logger.print("recriar a cadeia de troca")
            self.recreate_swapchain()
            return
        
        # Atualiza o índice do frame para que o próximo ciclo de renderização use o próximo conjunto de buffers.
        self.frameNumber = (self.frameNumber + 1) % self.maxFramesInFlight

    def cleanup_swapchain(self):
        """
            Libere a memória alocada para cada quadro e destrua a cadeia de troca.
        """
        for frame in self.swapchainFrames:
            vkDestroyImageView(
                device = self.device, imageView = frame.image_view, pAllocator = None
            )
            vkDestroyFramebuffer(
                device = self.device, framebuffer = frame.framebuffer, pAllocator = None
            )
            vkDestroyFence(self.device, frame.inFlight, None)
            vkDestroySemaphore(self.device, frame.imageAvailable, None)
            vkDestroySemaphore(self.device, frame.renderFinished, None)
        
            vkUnmapMemory(
                device = self.device, 
                memory = frame.uniformBuffer.buffer_memory)
            vkFreeMemory(
                device = self.device,
                memory = frame.uniformBuffer.buffer_memory,
                pAllocator = None
            )
            vkDestroyBuffer(
                device = self.device,
                buffer = frame.uniformBuffer.buffer,
                pAllocator = None
            )

            vkUnmapMemory(
                device = self.device, 
                memory = frame.modelBuffer.buffer_memory)
            vkFreeMemory(
                device = self.device,
                memory = frame.modelBuffer.buffer_memory,
                pAllocator = None
            )
            vkDestroyBuffer(
                device = self.device,
                buffer = frame.modelBuffer.buffer,
                pAllocator = None
            )

        vkDestroyDescriptorPool(self.device, self.descriptorPool, None)

        destructionFunction = vkGetDeviceProcAddr(self.device, 'vkDestroySwapchainKHR')
        destructionFunction(self.device, self.swapchain, None)

    def close(self):    
        vkDeviceWaitIdle(self.device)

        vklogging.logger.print(f"{HEADER}\nAté logo!\n{RESET}")

        vkDestroyCommandPool(self.device, self.commandPool, None)

        vkDestroyPipeline(self.device, self.pipeline, None)
        vkDestroyPipelineLayout(self.device, self.pipelineLayout, None)
        vkDestroyRenderPass(self.device, self.renderpass, None)
        
        self.cleanup_swapchain()

        vkDestroyDescriptorSetLayout(
            self.device, 
            self.frameDescriptorSetLayout, 
            None
        )

        self.meshes.destroy()
        
        for _,material in self.materials:
            material.destroy()
        vkDestroyDevice(
            device = self.device, pAllocator = None
        )
        
        destructionFunction = vkGetInstanceProcAddr(self.instance, "vkDestroySurfaceKHR")
        destructionFunction(self.instance, self.surface, None)
        if vklogging.logger.debug_mode:
            #fetch destruction function
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

        #terminate glfw
        glfw.terminate()