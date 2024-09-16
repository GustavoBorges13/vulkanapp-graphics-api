from config import *
import shaders
 
class InputBundle:

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

    def __init__(self, pipelineLayout, renderPass, pipeline):

        self.pipelineLayout = pipelineLayout
        self.renderPass = renderPass
        self.pipeline = pipeline

"""
renderpass -> uma especie de descricao dos varios recursos que estao anexados a
uma execucao completa do pipeline, incluindo todos os subpass
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

    #similar ao opengl
    colorAttachmentRef = VkAttachmentReference(
        attachment=0,
        layout=VK_IMAGE_LAYOUT_COLOR_ATTACHMENT_OPTIMAL
    )

    subpass = VkSubpassDescription(
        pipelineBindPoint=VK_PIPELINE_BIND_POINT_GRAPHICS,
        colorAttachmentCount=1,
        pColorAttachments=colorAttachmentRef
    )

    renderPassInfo = VkRenderPassCreateInfo(
        sType=VK_STRUCTURE_TYPE_RENDER_PASS_CREATE_INFO,
        attachmentCount=1,
        pAttachments=colorAttachment,
        subpassCount=1,
        pSubpasses=subpass
    )

    return vkCreateRenderPass(device, renderPassInfo, None)

"""Pipeline layout, descreve quais push constants e conjuntos de descritores (descriptions set, set layouts) serao
utilizados com um determinado pipeline.

Em nosso exemplo, nao estamos pegando nenhum dado (por isso = 0) mas ainda temos que criar o layout de pipeline.
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
Primeiro -> vertex input, como vamos receber a entrada no pipeline, que tipo de ligacoes e atributos
Segundo -> vertex shader, qual estagio estamos criando, onde está o codigo compilado e a entrada entrypoint
"""
def create_graphics_pipeline(inputBundle, debug):

    #estágio de entrada do vértice
    #Nesse estágio, nenhum dado de vértice está sendo obtido.
    vertexInputInfo = VkPipelineVertexInputStateCreateInfo(
        sType=VK_STRUCTURE_TYPE_PIPELINE_VERTEX_INPUT_STATE_CREATE_INFO,
        vertexBindingDescriptionCount=0,
        vertexAttributeDescriptionCount=0
    )

    #O sombreador de vértice transforma os vértices adequadamente
    if (debug):
        print(f"{HEADER}Carregar módulo de sombreamento (shader module): {inputBundle.vertexFilepath}{RESET}")
    vertexShaderModule = shaders.create_shader_module(inputBundle.device, inputBundle.vertexFilepath)
    vertexShaderStageInfo = VkPipelineShaderStageCreateInfo(
            sType=VK_STRUCTURE_TYPE_PIPELINE_SHADER_STAGE_CREATE_INFO,
            stage=VK_SHADER_STAGE_VERTEX_BIT,
            module=vertexShaderModule,
            pName="main"
        )

    #topologia de criacao de shapes -> para triangulo 2d usar essa
    #Assembly entrada, qual método de construção usar com vértices
    inputAssembly = VkPipelineInputAssemblyStateCreateInfo(
        sType=VK_STRUCTURE_TYPE_PIPELINE_INPUT_ASSEMBLY_STATE_CREATE_INFO,
        topology=VK_PRIMITIVE_TOPOLOGY_TRIANGLE_LIST,
        primitiveRestartEnable=VK_FALSE #permite o “desmembramento” de topologias de faixas
    )

    #transformação da imagem para o framebuffer: stretch
    #janela de visualizacao
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

    #essas duas transformações se combinam para definir o estado da janela de visualização
    viewportState = VkPipelineViewportStateCreateInfo(
        sType=VK_STRUCTURE_TYPE_PIPELINE_VIEWPORT_STATE_CREATE_INFO,
        viewportCount=1,
        pViewports=viewport,
        scissorCount=1,
        pScissors=scissor
    )

    #rasterizador interpola entre os vértices para produzir fragmentos e também realiza testes de visibilidade
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

    #parâmetros de multisampling
    multisampling = VkPipelineMultisampleStateCreateInfo(
        sType=VK_STRUCTURE_TYPE_PIPELINE_MULTISAMPLE_STATE_CREATE_INFO,
        sampleShadingEnable=VK_FALSE,
        rasterizationSamples=VK_SAMPLE_COUNT_1_BIT
    )

    #O sombreador de fragmentos pega os fragmentos do rasterizador e os colore apropriadamente
    if (debug):
        print(f"{HEADER}Carregar módulo de sombreamento (shader module): {inputBundle.fragmentFilepath}{RESET}")
    fragmentShaderModule = shaders.create_shader_module(inputBundle.device, inputBundle.fragmentFilepath)
    fragmentShaderStageInfo = VkPipelineShaderStageCreateInfo(
        sType=VK_STRUCTURE_TYPE_PIPELINE_SHADER_STAGE_CREATE_INFO,
        stage=VK_SHADER_STAGE_FRAGMENT_BIT,
        module=fragmentShaderModule,
        pName="main"
    )

    shaderStages = [vertexShaderStageInfo, fragmentShaderStageInfo]

    #combinação de cores, pegue a saída do fragment shader e incorpore-a ao pixel existente, se ele tiver sido definido.
    colorBlendAttachment = VkPipelineColorBlendAttachmentState(
        colorWriteMask=VK_COLOR_COMPONENT_R_BIT | VK_COLOR_COMPONENT_G_BIT | VK_COLOR_COMPONENT_B_BIT | VK_COLOR_COMPONENT_A_BIT,
        blendEnable=VK_FALSE #Função blend
    )
    colorBlending = VkPipelineColorBlendStateCreateInfo(
        sType=VK_STRUCTURE_TYPE_PIPELINE_COLOR_BLEND_STATE_CREATE_INFO,
        logicOpEnable=VK_FALSE, #operações lógicas
        attachmentCount=1,
        pAttachments=colorBlendAttachment,
        blendConstants=[0.0, 0.0, 0.0, 0.0]
    )

    pipelineLayout = create_pipeline_layout(inputBundle.device)
    renderPass = create_render_pass(inputBundle.device, inputBundle.swapchainImageFormat)

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