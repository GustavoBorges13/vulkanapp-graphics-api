from config import *
import shaders
 
class InputBundle:
    """
    Classe de entrada para encapsular os parâmetros necessários para criar um pipeline gráfico.
    """
    def __init__(self, device, 
    swapchainImageFormat, swapchainExtent, 
    vertexFilepath, fragmentFilepath
    ):

        self.device = device
        self.swapchainImageFormat = swapchainImageFormat
        self.swapchainExtent = swapchainExtent
        self.vertexFilepath = vertexFilepath
        self.fragmentFilepath = fragmentFilepath

class OuputBundle:
    """
    Classe de saída para encapsular os recursos gerados pelo pipeline gráfico: layout, render pass e o próprio pipeline.
    """
    def __init__(self, pipelineLayout, renderPass, pipeline):

        self.pipelineLayout = pipelineLayout
        self.renderPass = renderPass
        self.pipeline = pipeline

"""
A função create_render_pass define uma render pass no Vulkan.
Ela descreve os attachments (recursos de buffer, como a cor) e configura os estados de carregamento e armazenamento 
para cada subpass, além de como os dados devem ser tratados ao início e final da renderização.
"""
def create_render_pass(device, swapchainImageFormat):
    
    colorAttachment = VkAttachmentDescription(
        format = swapchainImageFormat,
        samples = VK_SAMPLE_COUNT_1_BIT,

        loadOp = VK_ATTACHMENT_LOAD_OP_CLEAR,
        storeOp = VK_ATTACHMENT_STORE_OP_STORE,

        stencilLoadOp = VK_ATTACHMENT_LOAD_OP_DONT_CARE,
        stencilStoreOp = VK_ATTACHMENT_STORE_OP_DONT_CARE,

        initialLayout=VK_IMAGE_LAYOUT_UNDEFINED,
        finalLayout=VK_IMAGE_LAYOUT_PRESENT_SRC_KHR 
    )

    # Referência para o attachment que será usado no subpass como color attachment
    colorAttachmentRef = VkAttachmentReference(
        attachment=0,
        layout=VK_IMAGE_LAYOUT_COLOR_ATTACHMENT_OPTIMAL
    )

    # Descreve o subpass, aqui um único subpass de renderização de cores
    subpass = VkSubpassDescription(
        pipelineBindPoint=VK_PIPELINE_BIND_POINT_GRAPHICS,
        colorAttachmentCount=1,
        pColorAttachments=colorAttachmentRef
    )

    # Criação da render pass
    renderPassInfo = VkRenderPassCreateInfo(
        sType=VK_STRUCTURE_TYPE_RENDER_PASS_CREATE_INFO,
        attachmentCount=1,
        pAttachments=colorAttachment,
        subpassCount=1,
        pSubpasses=subpass
    )

    return vkCreateRenderPass(device, renderPassInfo, None)

"""
A função create_pipeline_layout cria o layout do pipeline.
Aqui estamos criando um pipeline simples, sem push constants ou descritores.
"""
def create_pipeline_layout(device):

    pipelineLayoutInfo = VkPipelineLayoutCreateInfo(
        sType=VK_STRUCTURE_TYPE_PIPELINE_LAYOUT_CREATE_INFO,
        pushConstantRangeCount = 0,
        setLayoutCount = 0
    )

    return vkCreatePipelineLayout(
        device = device, pCreateInfo = pipelineLayoutInfo, pAllocator = None
    )


"""
A função create_graphics_pipeline cria um pipeline gráfico completo,
incluindo shaders, estados fixos (como a viewport, rasterizador e blending),
e associa o pipeline ao layout e à render pass.
"""
def create_graphics_pipeline(inputBundle, debug):

    # Sem descrição de entrada de vértices, pois não estamos passando dados de vértices (apenas um triângulo por exemplo)
    vertexInputInfo = VkPipelineVertexInputStateCreateInfo(
        sType=VK_STRUCTURE_TYPE_PIPELINE_VERTEX_INPUT_STATE_CREATE_INFO,
        vertexBindingDescriptionCount=0,
        vertexAttributeDescriptionCount=0
    )

    # Configurar a topologia de entrada de vértices, aqui desenhando triângulos!!
    inputAssembly = VkPipelineInputAssemblyStateCreateInfo(
        sType=VK_STRUCTURE_TYPE_PIPELINE_INPUT_ASSEMBLY_STATE_CREATE_INFO,
        topology=VK_PRIMITIVE_TOPOLOGY_TRIANGLE_LIST,
        primitiveRestartEnable=VK_FALSE #permite o “desmembramento” de topologias de faixas
    )

    # Carregar e configurar o shader de vértices
    if (debug):
        print(f"{HEADER}Carregar módulo de sombreamento (shader module): {inputBundle.vertexFilepath}{RESET}")
    vertexShaderModule = shaders.create_shader_module(inputBundle.device, inputBundle.vertexFilepath)
    vertexShaderStageInfo = VkPipelineShaderStageCreateInfo(
            sType=VK_STRUCTURE_TYPE_PIPELINE_SHADER_STAGE_CREATE_INFO,
            stage=VK_SHADER_STAGE_VERTEX_BIT,
            module=vertexShaderModule,
            pName="main"
        )


    #Tessellation -> tesselação (nao estamos usando)

    #Geometry shader -> shader geometrico (nao estamos usando)
    #Pega a saida do shader de tesselacao mas se tiver sem subdivisao pode obter infos extras...

    # Definir a área de visualização (viewport) e o recorte (scissor)
    viewport = VkViewport(
        x=0,
        y=0,
        width=inputBundle.swapchainExtent.width,
        height = inputBundle.swapchainExtent.height,
        minDepth=0.0,
        maxDepth=1.0
    )
    #transformação de imagem para framebuffer: recorte
    scissor = VkRect2D(
        offset=[0,0],
        extent=inputBundle.swapchainExtent
    )

    # Combinação da viewport e do scissor
    viewportState = VkPipelineViewportStateCreateInfo(
        sType=VK_STRUCTURE_TYPE_PIPELINE_VIEWPORT_STATE_CREATE_INFO,
        viewportCount=1,
        pViewports=viewport,
        scissorCount=1,
        pScissors=scissor
    )

    # Configurações do rasterizador: define como os fragmentos serão gerados a partir dos vértices
    # -> preencher shapes
    raterizer = VkPipelineRasterizationStateCreateInfo(
        sType=VK_STRUCTURE_TYPE_PIPELINE_RASTERIZATION_STATE_CREATE_INFO,
        depthClampEnable=VK_FALSE,
        rasterizerDiscardEnable=VK_FALSE,
        polygonMode=VK_POLYGON_MODE_FILL,
        lineWidth=1.0,
        cullMode=VK_CULL_MODE_BACK_BIT,
        frontFace=VK_FRONT_FACE_CLOCKWISE,
        depthBiasEnable=VK_FALSE #transformação opcional em valores de profundidade
    )

    # Configurações de multisampling (desativado neste caso)
    # melhora a qualidade visual das bordas dos objetos.
    # suaviza transicoes entre pixel e elimita o efeito serrilhado (aliasing)
    # que pode ocorrer quando linhas e bordas de objetos aparecem de forma
    # abrupta e pixelizada.
    multisampling = VkPipelineMultisampleStateCreateInfo(
        sType=VK_STRUCTURE_TYPE_PIPELINE_MULTISAMPLE_STATE_CREATE_INFO,
        sampleShadingEnable=VK_FALSE,
        rasterizationSamples=VK_SAMPLE_COUNT_1_BIT
    )

    #O sombreador de fragmentos carrega os fragmentos do rasterizador e os colore apropriadamente
    if (debug):
        print(f"{HEADER}Carregar módulo de sombreamento (shader module): {inputBundle.fragmentFilepath}{RESET}")
    fragmentShaderModule = shaders.create_shader_module(inputBundle.device, inputBundle.fragmentFilepath)
    fragmentShaderStageInfo = VkPipelineShaderStageCreateInfo(
        sType=VK_STRUCTURE_TYPE_PIPELINE_SHADER_STAGE_CREATE_INFO,
        stage=VK_SHADER_STAGE_FRAGMENT_BIT,
        module=fragmentShaderModule,
        pName="main"
    )

    #shader vertex, geometry shader (se tiver usado), fragment shader : : em comum!
    shaderStages = [vertexShaderStageInfo, fragmentShaderStageInfo]


    #Color blend em um anexo de cor especifico (Desativado para este caso)
    #combinação de cores, pegue a saída do fragment shader e incorpore-a ao pixel existente, se ele tiver sido definido.
    colorBlendAttachment = VkPipelineColorBlendAttachmentState(
        colorWriteMask=VK_COLOR_COMPONENT_R_BIT | VK_COLOR_COMPONENT_G_BIT | VK_COLOR_COMPONENT_B_BIT | VK_COLOR_COMPONENT_A_BIT,
        blendEnable=VK_FALSE #função sem blend
    )
    #Color blending (desativado para este caso)
    colorBlending = VkPipelineColorBlendStateCreateInfo(
        sType=VK_STRUCTURE_TYPE_PIPELINE_COLOR_BLEND_STATE_CREATE_INFO,
        logicOpEnable=VK_FALSE, #sem operações lógicas
        attachmentCount=1,
        pAttachments=colorBlendAttachment,
        blendConstants=[0.0, 0.0, 0.0, 0.0]
    )

    # Criar o layout do pipeline e a render pass
    pipelineLayout = create_pipeline_layout(inputBundle.device)
    renderPass = create_render_pass(inputBundle.device, inputBundle.swapchainImageFormat)

    # Criar o pipeline gráfico
    pipelineInfo = VkGraphicsPipelineCreateInfo(
        sType=VK_STRUCTURE_TYPE_GRAPHICS_PIPELINE_CREATE_INFO,
        stageCount=2,
        pStages=shaderStages,
        pVertexInputState=vertexInputInfo,
        pInputAssemblyState=inputAssembly,
        pViewportState=viewportState,
        pRasterizationState=raterizer,
        pMultisampleState=multisampling,
        pDepthStencilState=None,
        pColorBlendState=colorBlending,
        layout=pipelineLayout,
        renderPass=renderPass,
        subpass=0 #índice da subpasta 0, a única subpasta
    )

    #vkCreateGraphicsPipelines(device, pipelineCache, createInfoCount, pCreateInfos, pAllocator, pPipelines=None)
    graphicsPipeline = vkCreateGraphicsPipelines(inputBundle.device, VK_NULL_HANDLE, 1, pipelineInfo, None)[0]

    vkDestroyShaderModule(inputBundle.device, vertexShaderModule, None)
    vkDestroyShaderModule(inputBundle.device, fragmentShaderModule, None)

    return OuputBundle(
        pipelineLayout = pipelineLayout,
        renderPass = renderPass,
        pipeline = graphicsPipeline
    )