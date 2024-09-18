from config import *
import logging
import queue_families
import frame

class SwapChainSupportDetails:

    def __init__ (self):

        self.capabilities = None
        self.formats = None
        self.presentModes = None

class SwapChainBundle:

    def __init__(self):
        
        self.swapchain = None
        self.frames = []
        self.format = None
        self.extent = None

        #ESTRUTURA DE SUPORTE
def query_swapchain_support(instance, physicalDevice, surface, debug):

    support = SwapChainSupportDetails()

    vkGetPhysicalDeviceSurfaceCapabilitiesKHR = vkGetInstanceProcAddr(instance, "vkGetPhysicalDeviceSurfaceCapabilitiesKHR")

    support.capabilities = vkGetPhysicalDeviceSurfaceCapabilitiesKHR(physicalDevice, surface)

    if debug:
        """
        typedef struct VkSurfaceCapabilitiesKHR {
            uint32_t                         minImageCount;
            uint32_t                         maxImageCount;
            VkExtent2D                       currentExtent;
            VkExtent2D                       minImageExtent;
            VkExtent2D                       maxImageExtent;
            uint32_t                         maxImageArrayLayers;
            VkSurfaceTransformFlagsKHR       supportedTransforms;
            VkSurfaceTransformFlagBitsKHR    currentTransform;
            VkCompositeAlphaFlagsKHR         supportedCompositeAlpha;
            VkImageUsageFlags                supportedUsageFlags;
        } VkSurfaceCapabilitiesKHR;
        """
        print(f"{HEADER}O Swapchain (cadeia de troca) pode suportar os seguintes recursos de superfície:{RESET}")

        print(f"{WARNING}\tcontagem mínima de imagens: {OKBLUE}{support.capabilities.minImageCount}{RESET}")
        print(f"{WARNING}\tcontagem máxima de imagens: {OKBLUE}{support.capabilities.maxImageCount}{RESET}")

        print(f"{UNDERLINE}{WARNING}\textensão atual:{RESET}")
        """
        typedef struct VkExtent2D {
            uint32_t    width;
            uint32_t    height;
        } VkExtent2D;
        """

        #mesmo tamanho do tamanho da janela glfw que criamos
        #swapchains nao sao redimensionavel dinamicamente, ou seja, se minimizar ou maximizar uma janela
        #teremos que recriar tudo, todo o pipeline grafico da cadeia de troca e tudo.
        print(f"{OKBLUE}\t\twidth: {support.capabilities.currentExtent.width}{RESET}")
        print(f"{OKBLUE}\t\theight: {support.capabilities.currentExtent.height}{RESET}")

        print(f"{WARNING}\tminimum supported extent:{RESET}")
        print(f"{OKBLUE}\t\twidth: {support.capabilities.minImageExtent.width}{RESET}")
        print(f"{OKBLUE}\t\theight: {support.capabilities.minImageExtent.height}{RESET}")

        print(f"{WARNING}\tmaximum supported extent:{RESET}")
        print(f"{OKBLUE}\t\twidth: {support.capabilities.maxImageExtent.width}{RESET}")
        print(f"{OKBLUE}\t\theight: {support.capabilities.maxImageExtent.height}{RESET}")


        print(f"{WARNING}\tmáximo de camadas de matriz de imagem: {OKBLUE}{support.capabilities.maxImageArrayLayers}{RESET}")

        print(f"{WARNING}\ttransformações suportadas:{RESET}")
        stringList = logging.log_transform_bits(support.capabilities.supportedTransforms)
        for line in stringList:
            print(f"{OKBLUE}\t\t{line}{RESET}")

        print(f"{WARNING}\ttransformação atual:{RESET}")
        stringList = logging.log_transform_bits(support.capabilities.currentTransform)
        for line in stringList:
            print(f"{OKBLUE}\t\t{line}{RESET}")

        print(f"{WARNING}\toperações alfa suportadas:{RESET}")
        stringList = logging.log_alpha_composite_bits(support.capabilities.supportedCompositeAlpha)
        for line in stringList:
            print(f"{OKBLUE}\t\t{line}{RESET}")

        print(f"{WARNING}\tuso de imagem suportados:{RESET}")
        stringList = logging.log_image_usage_bits(support.capabilities.supportedUsageFlags)
        for line in stringList:
            print(f"{OKBLUE}\t\t{line}{RESET}")

        vkGetPhysicalDeviceSurfaceFormatsKHR = vkGetInstanceProcAddr(instance, 'vkGetPhysicalDeviceSurfaceFormatsKHR')
        support.formats = vkGetPhysicalDeviceSurfaceFormatsKHR(physicalDevice, surface)

        if debug:
            print(f"{WARNING}\tcombinações de formatos de pixel e espaços de cores suportados:{RESET}")
            for supportedFormat in support.formats:
                """
                * typedef struct VkSurfaceFormatKHR {
                    VkFormat           format;
                    VkColorSpaceKHR    colorSpace;
                } VkSurfaceFormatKHR;
                """

                print(f"{OKBLUE}\t\tformato de pixel suportado: {RESET}{logging.format_to_string(supportedFormat.format)}")
                print(f"{OKBLUE}\t\tespaço de cores suportado: {RESET}{logging.colorspace_to_string(supportedFormat.colorSpace)}")

        vkGetPhysicalDeviceSurfacePresentModesKHR = vkGetInstanceProcAddr(instance, 'vkGetPhysicalDeviceSurfacePresentModesKHR')

        support.presentModes = vkGetPhysicalDeviceSurfacePresentModesKHR(physicalDevice, surface)
        print(f"{WARNING}\tmodos de apresentação suportados:{RESET}")
        for presentMode in support.presentModes:
            print(f"{OKBLUE}\t\t{logging.log_present_mode(presentMode)}{RESET}")

        return support
    
    return support

#Sessao dos Formatos apropriados, apresentar modos e extensoes

#Escolhe os formatos apropriados
def choose_swapchain_surface_format(formats):

    for format in formats:
        if (format.format == VK_FORMAT_B8G8R8A8_UNORM
            and format.colorSpace == VK_COLOR_SPACE_SRGB_NONLINEAR_KHR):
            return format

    return formats[0]

#Escolhe as apresentacoes apropriadas
def choose_swapchain_present_mode(presentModes):
        
    for presentMode in presentModes:
        if presentMode == VK_PRESENT_MODE_MAILBOX_KHR:
            return presentMode

    return VK_PRESENT_MODE_FIFO_KHR

#Escolhe as extensoes apropriadas
def choose_swapchain_extent(width, height, capabilities):
    
    extent = VkExtent2D(width, height)

    extent.width = min(
        capabilities.maxImageExtent.width, 
        max(capabilities.minImageExtent.width, extent.width)
    )

    extent.height = min(
        capabilities.maxImageExtent.height,
        max(capabilities.minImageExtent.height, extent.height)
    )

    return extent

def create_swapchain(instance, logicalDevice, physicalDevice, surface, width, height, debug):

    #usando as funcoes que criamos anteriormente...
    support = query_swapchain_support(instance, physicalDevice, surface, debug)

    format = choose_swapchain_surface_format(support.formats)

    presentMode = choose_swapchain_present_mode(support.presentModes)

    extent = choose_swapchain_extent(width, height, support.capabilities)

    """
        nos podemos ter duas imagens e ainda obter uma taxa de quadros ilimitada,
        mas ter mais uma imgem no swapchain nos da recursos extras para renderizar e 
        apresentá-las ao mesmo tempo.

        Então é como se nos tivemos 2 imagens, uma para a qual estamos renderizando
        quando estivermos apresentando e depois teremos outra por precaução para que
        possamos continuar nos movendo rapidamente.
    """
    imageCount = min(
        support.capabilities.maxImageCount,
        support.capabilities.minImageCount + 1
    )

    """
        * VULKAN_HPP_CONSTEXPR SwapchainCreateInfoKHR(
            VULKAN_HPP_NAMESPACE::SwapchainCreateFlagsKHR flags_         = {},
            VULKAN_HPP_NAMESPACE::SurfaceKHR              surface_       = {},
            uint32_t                                      minImageCount_ = {},
            VULKAN_HPP_NAMESPACE::Format                  imageFormat_   = VULKAN_HPP_NAMESPACE::Format::eUndefined,
            VULKAN_HPP_NAMESPACE::ColorSpaceKHR   imageColorSpace_  = VULKAN_HPP_NAMESPACE::ColorSpaceKHR::eSrgbNonlinear,
            VULKAN_HPP_NAMESPACE::Extent2D        imageExtent_      = {},
            uint32_t                              imageArrayLayers_ = {},
            VULKAN_HPP_NAMESPACE::ImageUsageFlags imageUsage_       = {},
            VULKAN_HPP_NAMESPACE::SharingMode     imageSharingMode_ = VULKAN_HPP_NAMESPACE::SharingMode::eExclusive,
            uint32_t                              queueFamilyIndexCount_ = {},
            const uint32_t *                      pQueueFamilyIndices_   = {},
            VULKAN_HPP_NAMESPACE::SurfaceTransformFlagBitsKHR preTransform_ =
            VULKAN_HPP_NAMESPACE::SurfaceTransformFlagBitsKHR::eIdentity,
            VULKAN_HPP_NAMESPACE::CompositeAlphaFlagBitsKHR compositeAlpha_ =
            VULKAN_HPP_NAMESPACE::CompositeAlphaFlagBitsKHR::eOpaque,
            VULKAN_HPP_NAMESPACE::PresentModeKHR presentMode_  = VULKAN_HPP_NAMESPACE::PresentModeKHR::eImmediate,
            VULKAN_HPP_NAMESPACE::Bool32         clipped_      = {},
            VULKAN_HPP_NAMESPACE::SwapchainKHR   oldSwapchain_ = {} 
        ) VULKAN_HPP_NOEXCEPT
    """

    """
    Verificar se os graficos presentes tem diferentes indices ou nao
    se tiver indices diferentes entao esse é o modo de compartilhamento (imageSharingMode)
    pois sera a swapchain que será usada simultaneamente por duas ou mais familia de filas (queue family) diferentes.

    Neste caso, precisamos especificar quantas familias que estao usando-a e fornecer um ponteiro para os indices
    da familia que o usuarão.

    Caso contrario, sera usado exclusivamente  por uma familia de filas e nao precisaremos definir tais parametros.
    """
    indices = queue_families.find_queue_families(physicalDevice, instance, surface, debug)
    queueFamilyIndices = [
        indices.graphicsFamily, indices.presentFamily
    ]
    if (indices.graphicsFamily != indices.presentFamily):
        imageSharingMode = VK_SHARING_MODE_CONCURRENT
        queueFamilyIndexCount = 2
        pQueueFamilyIndices = queueFamilyIndices
    else:
        imageSharingMode = VK_SHARING_MODE_EXCLUSIVE
        queueFamilyIndexCount = 0 
        pQueueFamilyIndices = None # nao precisa definir.

    createInfo = VkSwapchainCreateInfoKHR(
        surface = surface, 
        minImageCount = imageCount, 
        imageFormat = format.format,
        imageColorSpace = format.colorSpace, 
        imageExtent = extent, imageArrayLayers = 1,
        imageUsage = VK_IMAGE_USAGE_COLOR_ATTACHMENT_BIT, 
        imageSharingMode = imageSharingMode,
        queueFamilyIndexCount = queueFamilyIndexCount, 
        pQueueFamilyIndices = pQueueFamilyIndices,
        preTransform = support.capabilities.currentTransform,
        compositeAlpha = VK_COMPOSITE_ALPHA_OPAQUE_BIT_KHR,
        presentMode = presentMode, clipped = VK_TRUE
    )

    bundle = SwapChainBundle()

    vkCreateSwapchainKHR = vkGetDeviceProcAddr(logicalDevice, 'vkCreateSwapchainKHR')
    bundle.swapchain = vkCreateSwapchainKHR(logicalDevice, createInfo, None)
    vkGetSwapchainImagesKHR = vkGetDeviceProcAddr(logicalDevice, 'vkGetSwapchainImagesKHR')
    
    images = vkGetSwapchainImagesKHR(logicalDevice, bundle.swapchain)

    """
    isso pega o grupo de imagens que foram alocados pela gpu.
    E depois olhamos para as imagens construindo uma visualizacao de imagem a cada imagem,
    em seguida, armazenar toda informacao em um frame e colocoar esse frame em um pacote.
    """
    for image in images:

        components = VkComponentMapping(
            r = VK_COMPONENT_SWIZZLE_IDENTITY,
            g = VK_COMPONENT_SWIZZLE_IDENTITY,
            b = VK_COMPONENT_SWIZZLE_IDENTITY,
            a = VK_COMPONENT_SWIZZLE_IDENTITY
        )

        subresourceRange = VkImageSubresourceRange(
            aspectMask = VK_IMAGE_ASPECT_COLOR_BIT,
            baseMipLevel = 0, levelCount = 1,
            baseArrayLayer = 0, layerCount = 1
        )

        #Da pra usar 3d view type...
        create_info = VkImageViewCreateInfo(
            image = image, 
            viewType = VK_IMAGE_VIEW_TYPE_2D,
            format = format.format, 
            components = components,
            subresourceRange = subresourceRange
        )

        swapchain_frame = frame.SwapChainFrame()
        swapchain_frame.image = image
        swapchain_frame.image_view = vkCreateImageView(
            device = logicalDevice, 
            pCreateInfo = create_info, 
            pAllocator = None
        )
        bundle.frames.append(swapchain_frame)

    bundle.format = format.format
    bundle.extent = extent

    return bundle