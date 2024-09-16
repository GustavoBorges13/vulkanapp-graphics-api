from config import *

"""
    * Debug call back:
    *
    *	typedef enum VkDebugUtilsMessageSeverityFlagBitsEXT {
            VK_DEBUG_UTILS_MESSAGE_SEVERITY_VERBOSE_BIT_EXT = 0x00000001,
            VK_DEBUG_UTILS_MESSAGE_SEVERITY_INFO_BIT_EXT = 0x00000010,
            VK_DEBUG_UTILS_MESSAGE_SEVERITY_WARNING_BIT_EXT = 0x00000100,
            VK_DEBUG_UTILS_MESSAGE_SEVERITY_ERROR_BIT_EXT = 0x00001000,
            VK_DEBUG_UTILS_MESSAGE_SEVERITY_FLAG_BITS_MAX_ENUM_EXT = 0x7FFFFFFF
        } VkDebugUtilsMessageSeverityFlagBitsEXT;

    *	typedef enum VkDebugUtilsMessageTypeFlagBitsEXT {
            VK_DEBUG_UTILS_MESSAGE_TYPE_GENERAL_BIT_EXT = 0x00000001,
            VK_DEBUG_UTILS_MESSAGE_TYPE_VALIDATION_BIT_EXT = 0x00000002,
            VK_DEBUG_UTILS_MESSAGE_TYPE_PERFORMANCE_BIT_EXT = 0x00000004,
            VK_DEBUG_UTILS_MESSAGE_TYPE_FLAG_BITS_MAX_ENUM_EXT = 0x7FFFFFFF
        } VkDebugUtilsMessageTypeFlagBitsEXT;

    *	typedef struct VkDebugUtilsMessengerCallbackDataEXT {
            VkStructureType                              sType;
            const void*                                  pNext;
            VkDebugUtilsMessengerCallbackDataFlagsEXT    flags;
            const char*                                  pMessageIdName;
            int32_t                                      messageIdNumber;
            const char*                                  pMessage;
            uint32_t                                     queueLabelCount;
            const VkDebugUtilsLabelEXT*                  pQueueLabels;
            uint32_t                                     cmdBufLabelCount;
            const VkDebugUtilsLabelEXT*                  pCmdBufLabels;
            uint32_t                                     objectCount;
            const VkDebugUtilsObjectNameInfoEXT*         pObjects;
        } VkDebugUtilsMessengerCallbackDataEXT;

"""
def debugCallback(*args):

    """
    print(f “O mensageiro de depuração tem {len(args)} componentes”)
    for arg in args:
        print(f"\t{arg}")
    """
    print(f"Camada de validação: {args[5]} {args[6]}")
    return 0

def createDebugReportCallbackEXT(instance, pCreateInfo, pAllocator):

    """
        def vkCreateDebugReportCallbackEXT(
            instance
            ,pCreateInfo
            ,pAllocator
            ,pCallback=None
            ,):
    """
    creationFunction = vkGetInstanceProcAddr(instance, 'vkCreateDebugReportCallbackEXT')
    if creationFunction:
        return creationFunction(instance, pCreateInfo, pAllocator)
    else:
        return VK_ERROR_EXTENSION_NOT_PRESENT
    
def make_debug_messenger(instance):

    """
        VkDebugReportCallbackCreateInfoEXT(
            sType=VK_STRUCTURE_TYPE_DEBUG_REPORT_CALLBACK_CREATE_INFO_EXT,
            pNext=None,
            flags=None,
            pfnCallback=None,
            pUserData=None,
        )
    """
    createInfo = VkDebugReportCallbackCreateInfoEXT(
        sType=VK_STRUCTURE_TYPE_DEBUG_REPORT_CALLBACK_CREATE_INFO_EXT,
        flags=VK_DEBUG_REPORT_ERROR_BIT_EXT | VK_DEBUG_REPORT_WARNING_BIT_EXT,
        pfnCallback=debugCallback
    )

    callback = createDebugReportCallbackEXT(instance, createInfo, None)

    if not callback:
            raise Exception("não foi possível configurar a chamada de retorno de depuração!")
    return callback
    
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

    print(f"Device name: {properties.deviceName}")

    print("Device type: ",end="")

    if properties.deviceType == VK_PHYSICAL_DEVICE_TYPE_CPU:
        print("CPU")
    elif properties.deviceType == VK_PHYSICAL_DEVICE_TYPE_DISCRETE_GPU:
        print("Discrete GPU")
    elif properties.deviceType == VK_PHYSICAL_DEVICE_TYPE_INTEGRATED_GPU:
        print("Integrated GPU")
    elif properties.deviceType == VK_PHYSICAL_DEVICE_TYPE_VIRTUAL_GPU:
        print("Virtual GPU")
    else:
        print("Other")

def log_transform_bits(bits):

    result = []

    """
    * typedef enum VkSurfaceTransformFlagBitsKHR {
        VK_SURFACE_TRANSFORM_IDENTITY_BIT_KHR = 0x00000001,
        VK_SURFACE_TRANSFORM_ROTATE_90_BIT_KHR = 0x00000002,
        VK_SURFACE_TRANSFORM_ROTATE_180_BIT_KHR = 0x00000004,
        VK_SURFACE_TRANSFORM_ROTATE_270_BIT_KHR = 0x00000008,
        VK_SURFACE_TRANSFORM_HORIZONTAL_MIRROR_BIT_KHR = 0x00000010,
        VK_SURFACE_TRANSFORM_HORIZONTAL_MIRROR_ROTATE_90_BIT_KHR = 0x00000020,
        VK_SURFACE_TRANSFORM_HORIZONTAL_MIRROR_ROTATE_180_BIT_KHR = 0x00000040,
        VK_SURFACE_TRANSFORM_HORIZONTAL_MIRROR_ROTATE_270_BIT_KHR = 0x00000080,
        VK_SURFACE_TRANSFORM_INHERIT_BIT_KHR = 0x00000100,
    } VkSurfaceTransformFlagBitsKHR;
    """
    if (bits & VK_SURFACE_TRANSFORM_IDENTITY_BIT_KHR):
        result.append("identidade")
    if (bits & VK_SURFACE_TRANSFORM_ROTATE_90_BIT_KHR):
        result.append("rotação de 90 graus")
    if (bits & VK_SURFACE_TRANSFORM_ROTATE_180_BIT_KHR):
        result.append("rotação de 180 graus")
    if (bits & VK_SURFACE_TRANSFORM_ROTATE_270_BIT_KHR):
        result.append("rotação de 270 graus")
    if (bits & VK_SURFACE_TRANSFORM_HORIZONTAL_MIRROR_BIT_KHR):
        result.append("espelho horizontal")
    if (bits & VK_SURFACE_TRANSFORM_HORIZONTAL_MIRROR_ROTATE_90_BIT_KHR):
        result.append("espelho horizontal e, em seguida, rotação de 90 graus")
    if (bits & VK_SURFACE_TRANSFORM_HORIZONTAL_MIRROR_ROTATE_180_BIT_KHR):
        result.append("espelho horizontal e, em seguida, rotação de 180 graus")
    if (bits & VK_SURFACE_TRANSFORM_HORIZONTAL_MIRROR_ROTATE_270_BIT_KHR):
        result.append("espelho horizontal e, em seguida, rotação de 270 graus")
    if (bits & VK_SURFACE_TRANSFORM_INHERIT_BIT_KHR):
        result.append("herdado")

    return result

#se uma imagem no swapchain (cadeia de troca) tem algum tipo de comportamento alfa
# como ele vai lidar com isso 
def log_alpha_composite_bits(bits):

    result = []

    """
    typedef enum VkCompositeAlphaFlagBitsKHR {
        VK_COMPOSITE_ALPHA_OPAQUE_BIT_KHR = 0x00000001,
        VK_COMPOSITE_ALPHA_PRE_MULTIPLIED_BIT_KHR = 0x00000002,
        VK_COMPOSITE_ALPHA_POST_MULTIPLIED_BIT_KHR = 0x00000004,
        VK_COMPOSITE_ALPHA_INHERIT_BIT_KHR = 0x00000008,
    } VkCompositeAlphaFlagBitsKHR;
    """

    if (bits & VK_COMPOSITE_ALPHA_OPAQUE_BIT_KHR):
        result.append("opaco (alfa ignorado)")
    if (bits & VK_COMPOSITE_ALPHA_PRE_MULTIPLIED_BIT_KHR):
        result.append("pré-multiplicado (espera-se que o alfa já esteja multiplicado na imagem)")
    if (bits & VK_COMPOSITE_ALPHA_POST_MULTIPLIED_BIT_KHR):
        result.append("pós-multiplicado (o alfa será aplicado durante a composição)")
    if (bits & VK_COMPOSITE_ALPHA_INHERIT_BIT_KHR):
        result.append("herdado")

    return result

#podemos transferir memoria da swapchain para outras texturas, 
# para que possamos fazer uma amostragem da tela e entre outras coisas...
def log_image_usage_bits(bits):

    result = []

    """
    typedef enum VkImageUsageFlagBits {
        VK_IMAGE_USAGE_TRANSFER_SRC_BIT = 0x00000001,
        VK_IMAGE_USAGE_TRANSFER_DST_BIT = 0x00000002,
        VK_IMAGE_USAGE_SAMPLED_BIT = 0x00000004,
        VK_IMAGE_USAGE_STORAGE_BIT = 0x00000008,
        VK_IMAGE_USAGE_COLOR_ATTACHMENT_BIT = 0x00000010,
        VK_IMAGE_USAGE_DEPTH_STENCIL_ATTACHMENT_BIT = 0x00000020,
        VK_IMAGE_USAGE_TRANSIENT_ATTACHMENT_BIT = 0x00000040,
        VK_IMAGE_USAGE_INPUT_ATTACHMENT_BIT = 0x00000080,
        #ifdef VK_ENABLE_BETA_EXTENSIONS
            // Provided by VK_KHR_video_decode_queue
            VK_IMAGE_USAGE_VIDEO_DECODE_DST_BIT_KHR = 0x00000400,
        #endif
        #ifdef VK_ENABLE_BETA_EXTENSIONS
            // Provided by VK_KHR_video_decode_queue
            VK_IMAGE_USAGE_VIDEO_DECODE_SRC_BIT_KHR = 0x00000800,
        #endif
        #ifdef VK_ENABLE_BETA_EXTENSIONS
            // Provided by VK_KHR_video_decode_queue
            VK_IMAGE_USAGE_VIDEO_DECODE_DPB_BIT_KHR = 0x00001000,
        #endif
        // Provided by VK_EXT_fragment_density_map
        VK_IMAGE_USAGE_FRAGMENT_DENSITY_MAP_BIT_EXT = 0x00000200,
        // Provided by VK_KHR_fragment_shading_rate
        VK_IMAGE_USAGE_FRAGMENT_SHADING_RATE_ATTACHMENT_BIT_KHR = 0x00000100,
        #ifdef VK_ENABLE_BETA_EXTENSIONS
            // Provided by VK_KHR_video_encode_queue
            VK_IMAGE_USAGE_VIDEO_ENCODE_DST_BIT_KHR = 0x00002000,
        #endif
        #ifdef VK_ENABLE_BETA_EXTENSIONS
            // Provided by VK_KHR_video_encode_queue
            VK_IMAGE_USAGE_VIDEO_ENCODE_SRC_BIT_KHR = 0x00004000,
        #endif
        #ifdef VK_ENABLE_BETA_EXTENSIONS
            // Provided by VK_KHR_video_encode_queue
            VK_IMAGE_USAGE_VIDEO_ENCODE_DPB_BIT_KHR = 0x00008000,
        #endif
        // Provided by VK_HUAWEI_invocation_mask
        VK_IMAGE_USAGE_INVOCATION_MASK_BIT_HUAWEI = 0x00040000,
        // Provided by VK_NV_shading_rate_image
        VK_IMAGE_USAGE_SHADING_RATE_IMAGE_BIT_NV = VK_IMAGE_USAGE_FRAGMENT_SHADING_RATE_ATTACHMENT_BIT_KHR,
    } VkImageUsageFlagBits;
    """

    if (bits & VK_IMAGE_USAGE_TRANSFER_SRC_BIT):
        result.append("transfer src: a imagem pode ser usada como a origem de um comando de transferência.")
    if (bits & VK_IMAGE_USAGE_TRANSFER_DST_BIT):
        result.append("transfer dst: a imagem pode ser usada como destino de um comando de transferência.")
    if (bits & VK_IMAGE_USAGE_SAMPLED_BIT):
        result.append("""
                Sampled: a imagem pode ser usada para criar um VkImageView adequado para ocupar um slot 
                VkDescriptorSet do tipo VK_DESCRIPTOR_TYPE_SAMPLED_IMAGE ou 
                VK_DESCRIPTOR_TYPE_COMBINED_IMAGE_SAMPLER, e ser amostrada por um shader.""")

    if (bits & VK_IMAGE_USAGE_STORAGE_BIT):
        result.append("""
                Storage: a imagem pode ser usada para criar um VkImageView adequado para ocupar um slot 
                VkDescriptorSet do tipo VK_DESCRIPTOR_TYPE_STORAGE_IMAGE.""")
    if (bits & VK_IMAGE_USAGE_COLOR_ATTACHMENT_BIT):
        result.append("""
                Color attachment: a imagem pode ser usada para criar um VkImageView adequado para uso como 
                um anexo de cor ou resolução em um VkFramebuffer.""")
    if (bits & VK_IMAGE_USAGE_DEPTH_STENCIL_ATTACHMENT_BIT):
        result.append("""
                Depth/Stencil attachment: a imagem pode ser usada para criar um VkImageView 
                adequado para uso como um anexo de profundidade/estêncil ou de resolução de profundidade/estêncil em um VkFramebuffer.""")
    if (bits & VK_IMAGE_USAGE_TRANSIENT_ATTACHMENT_BIT ):
        result.append("""
                Transient attachment: as implementações podem suportar o uso de alocações de memória 
                com o VK_MEMORY_PROPERTY_LAZILY_ALLOCATED_BIT para fazer o backup de uma imagem com esse uso. Esse 
                bit pode ser definido para qualquer imagem que possa ser usada para criar um VkImageView adequado para uso como 
                uma cor, resolução, profundidade/estêncil ou anexo de entrada.""")

    if (bits & VK_IMAGE_USAGE_INPUT_ATTACHMENT_BIT):
        result.append("""
                Input attachment: A imagem pode ser usada para criar um VkImageView adequado para 
                ocupar o slot VkDescriptorSet do tipo VK_DESCRIPTOR_TYPE_INPUT_ATTACHMENT; ser lida de um 
                shader como um anexo de entrada; e ser usada como um anexo de entrada em um framebuffer.""")
    if (bits & VK_IMAGE_USAGE_FRAGMENT_DENSITY_MAP_BIT_EXT):
        result.append("""
                Fragment density map: pode ser usada para criar um VkImageView adequado 
                para uso como uma imagem de mapa de densidade de fragmento.""")

    return result

def log_present_mode(presentMode):
    
    """
    * // Provided by VK_KHR_surface
    typedef enum VkPresentModeKHR {
        VK_PRESENT_MODE_IMMEDIATE_KHR = 0,
        VK_PRESENT_MODE_MAILBOX_KHR = 1,
        VK_PRESENT_MODE_FIFO_KHR = 2,
        VK_PRESENT_MODE_FIFO_RELAXED_KHR = 3,
        // Provided by VK_KHR_shared_presentable_image
        VK_PRESENT_MODE_SHARED_DEMAND_REFRESH_KHR = 1000111000,
        // Provided by VK_KHR_shared_presentable_image
        VK_PRESENT_MODE_SHARED_CONTINUOUS_REFRESH_KHR = 1000111001,
    } VkPresentModeKHR;
    """

    if (presentMode == VK_PRESENT_MODE_IMMEDIATE_KHR):
        return """
                immediate: o mecanismo de apresentação não espera por um período de apagamento vertical 
                para atualizar a imagem atual, o que significa que esse modo pode resultar em rasgos visíveis. Não é necessária nenhuma 
                enfileiramento interno de solicitações de apresentação é necessário, pois as solicitações são aplicadas imediatamente."""
    if (presentMode == VK_PRESENT_MODE_MAILBOX_KHR):
        return """
                mailbox: o mecanismo de apresentação aguarda o próximo período de obstrução vertical 
                para atualizar a imagem atual. Não é possível observar rasgos. Uma fila interna de entrada única é 
                usada para manter as solicitações de apresentação pendentes. Se a fila estiver cheia quando uma nova solicitação de apresentação 
                apresentação for recebida, a nova solicitação substituirá a entrada existente e todas as imagens associadas 
                com a entrada anterior ficam disponíveis para reutilização pelo aplicativo. Uma solicitação é removida 
                da fila e processada durante cada período de apagamento vertical em que a fila não estiver vazia."""
    if (presentMode == VK_PRESENT_MODE_FIFO_KHR):
        return """
                fifo: o mecanismo de apresentação aguarda o próximo período de obstrução vertical 
                para atualizar a imagem atual. Não é possível observar o rasgo. Uma fila interna é usada para 
                manter solicitações de apresentação pendentes. Novas solicitações são anexadas ao final da fila e uma 
                e uma solicitação é removida do início da fila e processada durante cada 
                vertical em que a fila não está vazia. Esse é o único valor de presentMode que deve ser 
                seja suportado."""
    if (presentMode == VK_PRESENT_MODE_FIFO_RELAXED_KHR):
        return """
                relaxed fifo: o mecanismo de apresentação geralmente aguarda o próximo período de 
                para atualizar a imagem atual. Se um período de obturação vertical já tiver passado 
                desde a última atualização da imagem atual, o mecanismo de apresentação não esperará por 
                outro período de obturação vertical para a atualização, o que significa que esse modo pode resultar em rasgo visível 
                nesse caso. Esse modo é útil para reduzir a gagueira visual com um aplicativo que 
                apresentar uma nova imagem antes do próximo período de blanking vertical, mas pode ocasionalmente se atrasar e apresentar uma nova 
                atrasar e apresentar uma nova imagem logo após o próximo período de obturação vertical. Uma fila interna 
                é usada para manter as solicitações de apresentação pendentes. Novas solicitações são anexadas ao final da fila, 
                e uma solicitação é removida do início da fila e processada durante ou após cada 
                período de obturação vertical em que a fila não estiver vazia."""
    if (presentMode == VK_PRESENT_MODE_SHARED_DEMAND_REFRESH_KHR):
        return """
                shared demand refresh: o mecanismo de apresentação e o aplicativo têm 
                acesso simultâneo a uma única imagem, que é chamada de imagem apresentável compartilhada. 
                O mecanismo de apresentação só precisa atualizar a imagem atual depois que uma nova solicitação de apresentação é recebida. 
                solicitação de apresentação for recebida. Portanto, o aplicativo deve fazer uma solicitação de apresentação sempre que uma 
                atualização for necessária. Entretanto, o mecanismo de apresentação pode atualizar a imagem atual a qualquer momento, 
                o que significa que esse modo pode resultar em tearing visível."""
    if (presentMode == VK_PRESENT_MODE_SHARED_CONTINUOUS_REFRESH_KHR):
        return """
                shared continuous refresh: o mecanismo de apresentação e o aplicativo têm 
                acesso simultâneo a uma única imagem, que é chamada de imagem apresentável compartilhada. O mecanismo de 
                mecanismo de apresentação atualiza periodicamente a imagem atual em seu ciclo de atualização regular. O aplicativo 
                aplicativo só precisa fazer uma solicitação de apresentação inicial, após a qual o mecanismo de 
                motor de apresentação deve atualizar a imagem atual sem a necessidade de outras solicitações de apresentação. 
                solicitações de apresentação. O aplicativo pode indicar que o conteúdo da imagem foi atualizado por meio de uma 
                solicitação de apresentação, mas isso não garante o momento em que ela será atualizada. 
                Esse modo pode resultar em rasgo visível se a renderização da imagem não for cronometrada corretamente."""

    return "none/undefined"

def format_to_string(format):

    format_lookup = {
        VK_FORMAT_UNDEFINED: "VK_FORMAT_UNDEFINED", VK_FORMAT_R4G4_UNORM_PACK8: "VK_FORMAT_R4G4_UNORM_PACK8",
        VK_FORMAT_R4G4B4A4_UNORM_PACK16: "VK_FORMAT_R4G4B4A4_UNORM_PACK16", VK_FORMAT_B4G4R4A4_UNORM_PACK16 : "VK_FORMAT_B4G4R4A4_UNORM_PACK16",
        VK_FORMAT_R5G6B5_UNORM_PACK16 : "VK_FORMAT_R5G6B5_UNORM_PACK16", VK_FORMAT_B5G6R5_UNORM_PACK16 : "VK_FORMAT_B5G6R5_UNORM_PACK16",
        VK_FORMAT_R5G5B5A1_UNORM_PACK16 : "VK_FORMAT_R5G5B5A1_UNORM_PACK16", VK_FORMAT_B5G5R5A1_UNORM_PACK16 : "VK_FORMAT_B5G5R5A1_UNORM_PACK16",
        VK_FORMAT_A1R5G5B5_UNORM_PACK16 : "VK_FORMAT_A1R5G5B5_UNORM_PACK16", VK_FORMAT_R8_UNORM : "VK_FORMAT_R8_UNORM", 
        VK_FORMAT_R8_SNORM : "VK_FORMAT_R8_SNORM", VK_FORMAT_R8_USCALED : "VK_FORMAT_R8_USCALED", 
        VK_FORMAT_R8_SSCALED : "VK_FORMAT_R8_SSCALED", VK_FORMAT_R8_UINT : "VK_FORMAT_R8_UINT", 
        VK_FORMAT_R8_SINT : "VK_FORMAT_R8_SINT", VK_FORMAT_R8_SRGB : "VK_FORMAT_R8_SRGB", 
        VK_FORMAT_R8G8_UNORM : "VK_FORMAT_R8G8_UNORM", VK_FORMAT_R8G8_SNORM : "VK_FORMAT_R8G8_SNORM", 
        VK_FORMAT_R8G8_USCALED : "VK_FORMAT_R8G8_USCALED", VK_FORMAT_R8G8_SSCALED : "VK_FORMAT_R8G8_SSCALED", 
        VK_FORMAT_R8G8_UINT : "VK_FORMAT_R8G8_UINT", VK_FORMAT_R8G8_SINT : "VK_FORMAT_R8G8_SINT", 
        VK_FORMAT_R8G8_SRGB : "VK_FORMAT_R8G8_SRGB", VK_FORMAT_R8G8B8_UNORM : "VK_FORMAT_R8G8B8_UNORM", 
        VK_FORMAT_R8G8B8_SNORM : "VK_FORMAT_R8G8B8_SNORM", VK_FORMAT_R8G8B8_USCALED : "VK_FORMAT_R8G8B8_USCALED", 
        VK_FORMAT_R8G8B8_SSCALED : "VK_FORMAT_R8G8B8_SSCALED", VK_FORMAT_R8G8B8_UINT : "VK_FORMAT_R8G8B8_UINT", 
        VK_FORMAT_R8G8B8_SINT : "VK_FORMAT_R8G8B8_SINT", VK_FORMAT_R8G8B8_SRGB : "VK_FORMAT_R8G8B8_SRGB", 
        VK_FORMAT_B8G8R8_UNORM : "VK_FORMAT_B8G8R8_UNORM", VK_FORMAT_B8G8R8_SNORM : "VK_FORMAT_B8G8R8_SNORM", 
        VK_FORMAT_B8G8R8_USCALED : "VK_FORMAT_B8G8R8_USCALED", VK_FORMAT_B8G8R8_SSCALED : "VK_FORMAT_B8G8R8_SSCALED", 
        VK_FORMAT_B8G8R8_UINT : "VK_FORMAT_B8G8R8_UINT", VK_FORMAT_B8G8R8_SINT : "VK_FORMAT_B8G8R8_SINT", 
        VK_FORMAT_B8G8R8_SRGB : "VK_FORMAT_B8G8R8_SRGB", VK_FORMAT_R8G8B8A8_UNORM : "VK_FORMAT_R8G8B8A8_UNORM", 
        VK_FORMAT_R8G8B8A8_SNORM : "VK_FORMAT_R8G8B8A8_SNORM", VK_FORMAT_R8G8B8A8_USCALED : "VK_FORMAT_R8G8B8A8_USCALED", 
        VK_FORMAT_R8G8B8A8_SSCALED : "VK_FORMAT_R8G8B8A8_SSCALED", VK_FORMAT_R8G8B8A8_UINT : "VK_FORMAT_R8G8B8A8_UINT", 
        VK_FORMAT_R8G8B8A8_SINT : "VK_FORMAT_R8G8B8A8_SINT", VK_FORMAT_R8G8B8A8_SRGB : "VK_FORMAT_R8G8B8A8_SRGB", 
        VK_FORMAT_B8G8R8A8_UNORM : "VK_FORMAT_B8G8R8A8_UNORM", VK_FORMAT_B8G8R8A8_SNORM : "VK_FORMAT_B8G8R8A8_SNORM", 
        VK_FORMAT_B8G8R8A8_USCALED : "VK_FORMAT_B8G8R8A8_USCALED", VK_FORMAT_B8G8R8A8_SSCALED : "VK_FORMAT_B8G8R8A8_SSCALED", 
        VK_FORMAT_B8G8R8A8_UINT : "VK_FORMAT_B8G8R8A8_UINT", VK_FORMAT_B8G8R8A8_SINT : "VK_FORMAT_B8G8R8A8_SINT",
        VK_FORMAT_B8G8R8A8_SRGB : "VK_FORMAT_B8G8R8A8_SRGB", VK_FORMAT_A8B8G8R8_UNORM_PACK32 : "VK_FORMAT_A8B8G8R8_UNORM_PACK32",
        VK_FORMAT_A8B8G8R8_SNORM_PACK32 : "VK_FORMAT_A8B8G8R8_SNORM_PACK32", VK_FORMAT_A8B8G8R8_USCALED_PACK32 : "VK_FORMAT_A8B8G8R8_USCALED_PACK32",
        VK_FORMAT_A8B8G8R8_SSCALED_PACK32 : "VK_FORMAT_A8B8G8R8_SSCALED_PACK32", VK_FORMAT_A8B8G8R8_UINT_PACK32 : "VK_FORMAT_A8B8G8R8_UINT_PACK32",
        VK_FORMAT_A8B8G8R8_SINT_PACK32 : "VK_FORMAT_A8B8G8R8_SINT_PACK32", VK_FORMAT_A8B8G8R8_SRGB_PACK32 : "VK_FORMAT_A8B8G8R8_SRGB_PACK32",
        VK_FORMAT_A2R10G10B10_UNORM_PACK32 : "VK_FORMAT_A2R10G10B10_UNORM_PACK32", VK_FORMAT_A2R10G10B10_SNORM_PACK32 : "VK_FORMAT_A2R10G10B10_SNORM_PACK32",
        VK_FORMAT_A2R10G10B10_USCALED_PACK32 : "VK_FORMAT_A2R10G10B10_USCALED_PACK32", VK_FORMAT_A2R10G10B10_SSCALED_PACK32 : "VK_FORMAT_A2R10G10B10_SSCALED_PACK32",
        VK_FORMAT_A2R10G10B10_UINT_PACK32 : "VK_FORMAT_A2R10G10B10_UINT_PACK32", VK_FORMAT_A2R10G10B10_SINT_PACK32 : "VK_FORMAT_A2R10G10B10_SINT_PACK32",
        VK_FORMAT_A2B10G10R10_UNORM_PACK32 : "VK_FORMAT_A2B10G10R10_UNORM_PACK32", VK_FORMAT_A2B10G10R10_SNORM_PACK32 : "VK_FORMAT_A2B10G10R10_SNORM_PACK32",
        VK_FORMAT_A2B10G10R10_USCALED_PACK32 : "VK_FORMAT_A2B10G10R10_USCALED_PACK32", VK_FORMAT_A2B10G10R10_SSCALED_PACK32 : "VK_FORMAT_A2B10G10R10_SSCALED_PACK32",
        VK_FORMAT_A2B10G10R10_UINT_PACK32 : "VK_FORMAT_A2B10G10R10_UINT_PACK32", VK_FORMAT_A2B10G10R10_SINT_PACK32 : "VK_FORMAT_A2B10G10R10_SINT_PACK32",
        VK_FORMAT_R16_UNORM : "VK_FORMAT_R16_UNORM", VK_FORMAT_R16_SNORM : "VK_FORMAT_R16_SNORM",
        VK_FORMAT_R16_USCALED : "VK_FORMAT_R16_USCALED", VK_FORMAT_R16_SSCALED : "VK_FORMAT_R16_SSCALED",
        VK_FORMAT_R16_UINT : "VK_FORMAT_R16_UINT", VK_FORMAT_R16_SINT : "VK_FORMAT_R16_SINT",
        VK_FORMAT_R16_SFLOAT : "VK_FORMAT_R16_SFLOAT", VK_FORMAT_R16G16_UNORM : "VK_FORMAT_R16G16_UNORM",
        VK_FORMAT_R16G16_SNORM : "VK_FORMAT_R16G16_SNORM", VK_FORMAT_R16G16_USCALED : "VK_FORMAT_R16G16_USCALED",
        VK_FORMAT_R16G16_SSCALED : "VK_FORMAT_R16G16_SSCALED", VK_FORMAT_R16G16_UINT : "VK_FORMAT_R16G16_UINT",
        VK_FORMAT_R16G16_SINT : "VK_FORMAT_R16G16_SINT", VK_FORMAT_R16G16_SFLOAT : "VK_FORMAT_R16G16_SFLOAT",
        VK_FORMAT_R16G16B16_UNORM : "VK_FORMAT_R16G16B16_UNORM", VK_FORMAT_R16G16B16_SNORM : "VK_FORMAT_R16G16B16_SNORM",
        VK_FORMAT_R16G16B16_USCALED : "VK_FORMAT_R16G16B16_USCALED", VK_FORMAT_R16G16B16_SSCALED : "VK_FORMAT_R16G16B16_SSCALED",
        VK_FORMAT_R16G16B16_UINT : "VK_FORMAT_R16G16B16_UINT", VK_FORMAT_R16G16B16_SINT : "VK_FORMAT_R16G16B16_SINT",
        VK_FORMAT_R16G16B16_SFLOAT : "VK_FORMAT_R16G16B16_SFLOAT", VK_FORMAT_R16G16B16A16_UNORM : "VK_FORMAT_R16G16B16A16_UNORM",
        VK_FORMAT_R16G16B16A16_SNORM : "VK_FORMAT_R16G16B16A16_SNORM", VK_FORMAT_R16G16B16A16_USCALED : "VK_FORMAT_R16G16B16A16_USCALED",
        VK_FORMAT_R16G16B16A16_SSCALED : "VK_FORMAT_R16G16B16A16_SSCALED", VK_FORMAT_R16G16B16A16_UINT : "VK_FORMAT_R16G16B16A16_UINT",
        VK_FORMAT_R16G16B16A16_SINT : "VK_FORMAT_R16G16B16A16_SINT", VK_FORMAT_R16G16B16A16_SFLOAT : "VK_FORMAT_R16G16B16A16_SFLOAT",
        VK_FORMAT_R32_UINT : "VK_FORMAT_R32_UINT", VK_FORMAT_R32_SINT : "VK_FORMAT_R32_SINT",
        VK_FORMAT_R32_SFLOAT : "VK_FORMAT_R32_SFLOAT", VK_FORMAT_R32G32_UINT : "VK_FORMAT_R32G32_UINT",
        VK_FORMAT_R32G32_SINT : "VK_FORMAT_R32G32_SINT", VK_FORMAT_R32G32_SFLOAT : "VK_FORMAT_R32G32_SFLOAT",
        VK_FORMAT_R32G32B32_UINT : "VK_FORMAT_R32G32B32_UINT", VK_FORMAT_R32G32B32_SINT : "VK_FORMAT_R32G32B32_SINT",
        VK_FORMAT_R32G32B32_SFLOAT : "VK_FORMAT_R32G32B32_SFLOAT", VK_FORMAT_R32G32B32A32_UINT : "VK_FORMAT_R32G32B32A32_UINT",
        VK_FORMAT_R32G32B32A32_SINT : "VK_FORMAT_R32G32B32A32_SINT", VK_FORMAT_R32G32B32A32_SFLOAT : "VK_FORMAT_R32G32B32A32_SFLOAT",
        VK_FORMAT_R64_UINT : "VK_FORMAT_R64_UINT", VK_FORMAT_R64_SINT : "VK_FORMAT_R64_SINT",
        VK_FORMAT_R64_SFLOAT : "VK_FORMAT_R64_SFLOAT", VK_FORMAT_R64G64_UINT : "VK_FORMAT_R64G64_UINT",
        VK_FORMAT_R64G64_SINT : "VK_FORMAT_R64G64_SINT", VK_FORMAT_R64G64_SFLOAT : "VK_FORMAT_R64G64_SFLOAT",
        VK_FORMAT_R64G64B64_UINT : "VK_FORMAT_R64G64B64_UINT", VK_FORMAT_R64G64B64_SINT : "VK_FORMAT_R64G64B64_SINT",
        VK_FORMAT_R64G64B64_SFLOAT : "VK_FORMAT_R64G64B64_SFLOAT", VK_FORMAT_R64G64B64A64_UINT : "VK_FORMAT_R64G64B64A64_UINT",
        VK_FORMAT_R64G64B64A64_SINT : "VK_FORMAT_R64G64B64A64_SINT", VK_FORMAT_R64G64B64A64_SFLOAT : "VK_FORMAT_R64G64B64A64_SFLOAT",
        VK_FORMAT_B10G11R11_UFLOAT_PACK32 : "VK_FORMAT_B10G11R11_UFLOAT_PACK32", VK_FORMAT_E5B9G9R9_UFLOAT_PACK32 : "VK_FORMAT_E5B9G9R9_UFLOAT_PACK32",
        VK_FORMAT_D16_UNORM : "VK_FORMAT_D16_UNORM", VK_FORMAT_X8_D24_UNORM_PACK32 : "VK_FORMAT_X8_D24_UNORM_PACK325",
        VK_FORMAT_D32_SFLOAT : "VK_FORMAT_D32_SFLOAT", VK_FORMAT_S8_UINT : "VK_FORMAT_S8_UINT",
        VK_FORMAT_D16_UNORM_S8_UINT : "VK_FORMAT_D16_UNORM_S8_UINT", VK_FORMAT_D24_UNORM_S8_UINT : "VK_FORMAT_D24_UNORM_S8_UINT",
        VK_FORMAT_D32_SFLOAT_S8_UINT : "VK_FORMAT_D32_SFLOAT_S8_UINT", VK_FORMAT_BC1_RGB_UNORM_BLOCK : "VK_FORMAT_BC1_RGB_UNORM_BLOCK",
        VK_FORMAT_BC1_RGB_SRGB_BLOCK : "VK_FORMAT_BC1_RGB_SRGB_BLOCK", VK_FORMAT_BC1_RGBA_UNORM_BLOCK : "VK_FORMAT_BC1_RGBA_UNORM_BLOCK",
        VK_FORMAT_BC1_RGBA_SRGB_BLOCK : "VK_FORMAT_BC1_RGBA_SRGB_BLOCK", VK_FORMAT_BC2_UNORM_BLOCK : "VK_FORMAT_BC2_UNORM_BLOCK",
        VK_FORMAT_BC2_SRGB_BLOCK : "VK_FORMAT_BC2_SRGB_BLOCK", VK_FORMAT_BC3_UNORM_BLOCK : "VK_FORMAT_BC3_UNORM_BLOCK",
        VK_FORMAT_BC3_SRGB_BLOCK : "VK_FORMAT_BC3_SRGB_BLOCK", VK_FORMAT_BC4_UNORM_BLOCK : "VK_FORMAT_BC4_UNORM_BLOCK",
        VK_FORMAT_BC4_SNORM_BLOCK : "VK_FORMAT_BC4_SNORM_BLOCK", VK_FORMAT_BC5_UNORM_BLOCK : "VK_FORMAT_BC5_UNORM_BLOCK",
        VK_FORMAT_BC5_SNORM_BLOCK : "VK_FORMAT_BC5_SNORM_BLOCK", VK_FORMAT_BC6H_UFLOAT_BLOCK : "VK_FORMAT_BC6H_UFLOAT_BLOCK",
        VK_FORMAT_BC6H_SFLOAT_BLOCK : "VK_FORMAT_BC6H_SFLOAT_BLOCK", VK_FORMAT_BC7_UNORM_BLOCK : "VK_FORMAT_BC7_UNORM_BLOCK",
        VK_FORMAT_BC7_SRGB_BLOCK : "VK_FORMAT_BC7_SRGB_BLOCK", VK_FORMAT_ETC2_R8G8B8_UNORM_BLOCK : "VK_FORMAT_ETC2_R8G8B8_UNORM_BLOCK",
        VK_FORMAT_ETC2_R8G8B8_SRGB_BLOCK : "VK_FORMAT_ETC2_R8G8B8_SRGB_BLOCK", VK_FORMAT_ETC2_R8G8B8A1_UNORM_BLOCK : "VK_FORMAT_ETC2_R8G8B8A1_UNORM_BLOCK",
        VK_FORMAT_ETC2_R8G8B8A1_SRGB_BLOCK : "VK_FORMAT_ETC2_R8G8B8A1_SRGB_BLOCK", VK_FORMAT_ETC2_R8G8B8A8_UNORM_BLOCK : "VK_FORMAT_ETC2_R8G8B8A8_UNORM_BLOCK",
        VK_FORMAT_ETC2_R8G8B8A8_SRGB_BLOCK : "VK_FORMAT_ETC2_R8G8B8A8_SRGB_BLOCK", VK_FORMAT_EAC_R11_UNORM_BLOCK : "VK_FORMAT_EAC_R11_UNORM_BLOCK",
        VK_FORMAT_EAC_R11_SNORM_BLOCK : "VK_FORMAT_EAC_R11_SNORM_BLOCK", VK_FORMAT_EAC_R11G11_UNORM_BLOCK : "VK_FORMAT_EAC_R11G11_UNORM_BLOCK",
        VK_FORMAT_EAC_R11G11_SNORM_BLOCK : "VK_FORMAT_EAC_R11G11_SNORM_BLOCK", VK_FORMAT_ASTC_4x4_UNORM_BLOCK : "VK_FORMAT_ASTC_4x4_UNORM_BLOCK",
        VK_FORMAT_ASTC_4x4_SRGB_BLOCK : "VK_FORMAT_ASTC_4x4_SRGB_BLOCK", VK_FORMAT_ASTC_5x4_UNORM_BLOCK : "VK_FORMAT_ASTC_5x4_UNORM_BLOCK",
        VK_FORMAT_ASTC_5x4_SRGB_BLOCK : "VK_FORMAT_ASTC_5x4_SRGB_BLOCK", VK_FORMAT_ASTC_5x5_UNORM_BLOCK : "VK_FORMAT_ASTC_5x5_UNORM_BLOCK",
        VK_FORMAT_ASTC_5x5_SRGB_BLOCK : "VK_FORMAT_ASTC_5x5_SRGB_BLOCK", VK_FORMAT_ASTC_6x5_UNORM_BLOCK : "VK_FORMAT_ASTC_6x5_UNORM_BLOCK",
        VK_FORMAT_ASTC_6x5_SRGB_BLOCK : "VK_FORMAT_ASTC_6x5_SRGB_BLOCK", VK_FORMAT_ASTC_6x6_UNORM_BLOCK : "VK_FORMAT_ASTC_6x6_UNORM_BLOCK",
        VK_FORMAT_ASTC_6x6_SRGB_BLOCK : "VK_FORMAT_ASTC_6x6_SRGB_BLOCK", VK_FORMAT_ASTC_8x5_UNORM_BLOCK : "VK_FORMAT_ASTC_8x5_UNORM_BLOCK",
        VK_FORMAT_ASTC_8x5_SRGB_BLOCK : "VK_FORMAT_ASTC_8x5_SRGB_BLOCK", VK_FORMAT_ASTC_8x6_UNORM_BLOCK : "VK_FORMAT_ASTC_8x6_UNORM_BLOCK",
        VK_FORMAT_ASTC_8x6_SRGB_BLOCK : "VK_FORMAT_ASTC_8x6_SRGB_BLOCK", VK_FORMAT_ASTC_8x8_UNORM_BLOCK : "VK_FORMAT_ASTC_8x8_UNORM_BLOCK",
        VK_FORMAT_ASTC_8x8_SRGB_BLOCK : "VK_FORMAT_ASTC_8x8_SRGB_BLOCK", VK_FORMAT_ASTC_10x5_UNORM_BLOCK : "VK_FORMAT_ASTC_10x5_UNORM_BLOCK",
        VK_FORMAT_ASTC_10x5_SRGB_BLOCK : "VK_FORMAT_ASTC_10x5_SRGB_BLOCK", VK_FORMAT_ASTC_10x6_UNORM_BLOCK : "VK_FORMAT_ASTC_10x6_UNORM_BLOCK",
        VK_FORMAT_ASTC_10x6_SRGB_BLOCK : "VK_FORMAT_ASTC_10x6_SRGB_BLOCK", VK_FORMAT_ASTC_10x8_UNORM_BLOCK : "VK_FORMAT_ASTC_10x8_UNORM_BLOCK",
        VK_FORMAT_ASTC_10x8_SRGB_BLOCK : "VK_FORMAT_ASTC_10x8_SRGB_BLOCK", VK_FORMAT_ASTC_10x10_UNORM_BLOCK : "VK_FORMAT_ASTC_10x10_UNORM_BLOCK",
        VK_FORMAT_ASTC_10x10_SRGB_BLOCK : "VK_FORMAT_ASTC_10x10_SRGB_BLOCK", VK_FORMAT_ASTC_12x10_UNORM_BLOCK : "VK_FORMAT_ASTC_12x10_UNORM_BLOCK",
        VK_FORMAT_ASTC_12x10_SRGB_BLOCK : "VK_FORMAT_ASTC_12x10_SRGB_BLOCK", VK_FORMAT_ASTC_12x12_UNORM_BLOCK : "VK_FORMAT_ASTC_12x12_UNORM_BLOCK",
        VK_FORMAT_ASTC_12x12_SRGB_BLOCK : "VK_FORMAT_ASTC_12x12_SRGB_BLOCK"
    }

    return format_lookup[format]

def colorspace_to_string(colorspace):

    colorspace_lookup = {
        VK_COLOR_SPACE_SRGB_NONLINEAR_KHR : "VK_COLOR_SPACE_SRGB_NONLINEAR_KHR",
        VK_COLOR_SPACE_DISPLAY_P3_NONLINEAR_EXT : "VK_COLOR_SPACE_DISPLAY_P3_NONLINEAR_EXT",
        VK_COLOR_SPACE_EXTENDED_SRGB_LINEAR_EXT : "VK_COLOR_SPACE_EXTENDED_SRGB_LINEAR_EXT",
        VK_COLOR_SPACE_DCI_P3_NONLINEAR_EXT : "VK_COLOR_SPACE_DCI_P3_NONLINEAR_EXT",
        VK_COLOR_SPACE_BT709_LINEAR_EXT : "VK_COLOR_SPACE_BT709_LINEAR_EXT",
        VK_COLOR_SPACE_BT709_NONLINEAR_EXT : "VK_COLOR_SPACE_BT709_NONLINEAR_EXT",
        VK_COLOR_SPACE_BT2020_LINEAR_EXT : "VK_COLOR_SPACE_BT2020_LINEAR_EXT",
        VK_COLOR_SPACE_HDR10_ST2084_EXT : "VK_COLOR_SPACE_HDR10_ST2084_EXT",
        VK_COLOR_SPACE_DOLBYVISION_EXT : "VK_COLOR_SPACE_DOLBYVISION_EXT",
        VK_COLOR_SPACE_HDR10_HLG_EXT : "VK_COLOR_SPACE_HDR10_HLG_EXT",
        VK_COLOR_SPACE_ADOBERGB_LINEAR_EXT : "VK_COLOR_SPACE_ADOBERGB_LINEAR_EXT",
        VK_COLOR_SPACE_ADOBERGB_NONLINEAR_EXT : "VK_COLOR_SPACE_ADOBERGB_NONLINEAR_EXT",
        VK_COLOR_SPACE_PASS_THROUGH_EXT : "VK_COLOR_SPACE_PASS_THROUGH_EXT",
        VK_COLOR_SPACE_EXTENDED_SRGB_NONLINEAR_EXT : "VK_COLOR_SPACE_EXTENDED_SRGB_NONLINEAR_EXT"
    }

    return colorspace_lookup[colorspace]