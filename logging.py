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
    