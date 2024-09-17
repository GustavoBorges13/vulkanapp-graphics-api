from config import *
import os

def debugCallback(*args):
    """
        Função de retorno de chamada para camadas de validação/depuração.
    """

    
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

    print(f"Camada de validação: {args[5]} {args[6]}")
    return 0

def make_debug_messenger(instance):
    """
        Criar uma chamada de retorno de relatório de depuração para as camadas de validação chamarem

        Parameters:
            instance (VkInstance): The vulkan instance whose validation layers
            will use the callback function.
    """

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
        flags=VK_DEBUG_REPORT_ERROR_BIT_EXT | VK_DEBUG_REPORT_WARNING_BIT_EXT,
        pfnCallback=debugCallback
    )

    #fetch creation function
    creationFunction = vkGetInstanceProcAddr(instance, 'vkCreateDebugReportCallbackEXT')

    """
        def vkCreateDebugReportCallbackEXT(
            instance
            ,pCreateInfo
            ,pAllocator
            ,pCallback=None
            ,):
    """
    return creationFunction(instance, createInfo, None)

class Logger:
    """
        Classe estática para registro de depuração (impressão de informações personalizadas no console).
    """

    def __init__(self):
        """
            Crie o registrador.
        """

        self.debug_mode = False

        self.physical_device_types = {
            VK_PHYSICAL_DEVICE_TYPE_CPU: "CPU",
            VK_PHYSICAL_DEVICE_TYPE_DISCRETE_GPU: "Discrete GPU",
            VK_PHYSICAL_DEVICE_TYPE_INTEGRATED_GPU: "Integrated GPU",
            VK_PHYSICAL_DEVICE_TYPE_VIRTUAL_GPU: "Virtual GPU",
            VK_PHYSICAL_DEVICE_TYPE_OTHER: "Other"
        }

        self.colorspace_lookup = {
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

        self.format_lookup = {
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

        self.present_mode_lookup = {
            VK_PRESENT_MODE_IMMEDIATE_KHR: """immediate: the presentation engine does not wait for a vertical blanking period 
    to update the current image, meaning this mode may result in visible tearing. No internal 
    queuing of presentation requests is needed, as the requests are applied immediately.""",
            VK_PRESENT_MODE_MAILBOX_KHR: """mailbox: the presentation engine waits for the next vertical blanking period 
    to update the current image. Tearing cannot be observed. An internal single-entry queue is 
    used to hold pending presentation requests. If the queue is full when a new presentation 
    request is received, the new request replaces the existing entry, and any images associated 
    with the prior entry become available for re-use by the application. One request is removed 
    from the queue and processed during each vertical blanking period in which the queue is non-empty.""",
            VK_PRESENT_MODE_FIFO_KHR: """fifo: the presentation engine waits for the next vertical blanking 
    period to update the current image. Tearing cannot be observed. An internal queue is used to 
    hold pending presentation requests. New requests are appended to the end of the queue, and one 
    request is removed from the beginning of the queue and processed during each vertical blanking 
    period in which the queue is non-empty. This is the only value of presentMode that is required 
    to be supported.""",
            VK_PRESENT_MODE_FIFO_RELAXED_KHR: """relaxed fifo: the presentation engine generally waits for the next vertical 
    blanking period to update the current image. If a vertical blanking period has already passed 
    since the last update of the current image then the presentation engine does not wait for 
    another vertical blanking period for the update, meaning this mode may result in visible tearing 
    in this case. This mode is useful for reducing visual stutter with an application that will 
    mostly present a new image before the next vertical blanking period, but may occasionally be 
    late, and present a new image just after the next vertical blanking period. An internal queue 
    is used to hold pending presentation requests. New requests are appended to the end of the queue, 
    and one request is removed from the beginning of the queue and processed during or after each 
    vertical blanking period in which the queue is non-empty.""",
            VK_PRESENT_MODE_SHARED_DEMAND_REFRESH_KHR: """shared demand refresh: the presentation engine and application have 
    concurrent access to a single image, which is referred to as a shared presentable image. 
    The presentation engine is only required to update the current image after a new presentation 
    request is received. Therefore the application must make a presentation request whenever an 
    update is required. However, the presentation engine may update the current image at any point, 
    meaning this mode may result in visible tearing.""",
            VK_PRESENT_MODE_SHARED_CONTINUOUS_REFRESH_KHR: """shared continuous refresh: the presentation engine and application have 
    concurrent access to a single image, which is referred to as a shared presentable image. The 
    presentation engine periodically updates the current image on its regular refresh cycle. The 
    application is only required to make one initial presentation request, after which the 
    presentation engine must update the current image without any need for further presentation 
    requests. The application can indicate the image contents have been updated by making a 
    presentation request, but this does not guarantee the timing of when it will be updated. 
    This mode may result in visible tearing if rendering to the image is not timed correctly."""
        }
    
    def set_debug_mode(self, debug_mode: bool) -> None:
        """
            Definir o modo de depuração do registrador

            Parameters:
                debug_mode (bool): O novo modo de depuração a ser usado
        """

        self.debug_mode = debug_mode

    def _extract_version_number(self, version: int) -> tuple[int, int, int, int]:
        """
            Extrai as versões variante, principal, secundária e de correção de um número de versão

            Parâmetros:
                version (int): O número da versão, compactado em um número inteiro de 32 bits
            
            Retorna:
                tuple[int, int, int, int]: Números das versões Variant, Major, Minor e Patch
        """

        return (
            version >> 29, 
            VK_VERSION_MAJOR(version),
            VK_VERSION_MINOR(version),
            VK_VERSION_PATCH(version)
        )
    
    def _extract_driver_version_nvidia(self, version: int) -> str:
        """
            Extraia o número do driver gráfico,
            de acordo com as convenções da nvidia

            Parâmetros:
                version (int): O número da versão, compactado em um número inteiro de 32 bits.
            
            Retorna:
                str: O número do driver da Nvidia.
        """

        return f"{(version >> 22) & 0x3ff}.{(version >> 14) & 0x0ff}.{(version >> 6) & 0x0ff}.{version & 0x003f}"

    def _extract_driver_version_intel(self, version: int) -> str:
        """
            Extraia o número do driver gráfico,
            de acordo com as convenções da Intel no Windows

            Parâmetros:
                version (int): O número da versão, compactado em um número inteiro de 32 bits.
            
            Retorna:
                str: O número do driver Intel
        """

        return f"{version >> 14}.{version & 0x3fff}"
    
    def _extract_driver_version_standard(self, version: int) -> str:
        """
            Extraia o número do driver gráfico,
            quando nenhuma convenção de fornecedor estiver disponível.

            Parâmetros:
                version (int): O número da versão, compactado em um número inteiro de 32 bits.
            
            Retorna:
                str: O número do driver Intel
        """

        return f"{version >> 22}.{(version >> 12) & 0x3ff}.{version & 0xfff}"
    
    def _log_physical_device_limits(self, limits) -> None:
        """
            Registre vários limites do dispositivo.

            Parâmetros:
                limits (VkPhysicalDeviceLimits): a estrutura de limites do dispositivo
        """

        """
            typedef struct VkPhysicalDeviceLimits {
        uint32_t              maxImageDimension1D;
        uint32_t              maxImageDimension2D;
        uint32_t              maxImageDimension3D;
        uint32_t              maxImageDimensionCube;
        uint32_t              maxImageArrayLayers;
        uint32_t              maxTexelBufferElements;
        uint32_t              maxUniformBufferRange;
        uint32_t              maxStorageBufferRange;
        uint32_t              maxPushConstantsSize;
        uint32_t              maxMemoryAllocationCount;
        uint32_t              maxSamplerAllocationCount;
        VkDeviceSize          bufferImageGranularity;
        VkDeviceSize          sparseAddressSpaceSize;
        uint32_t              maxBoundDescriptorSets;
        uint32_t              maxPerStageDescriptorSamplers;
        uint32_t              maxPerStageDescriptorUniformBuffers;
        uint32_t              maxPerStageDescriptorStorageBuffers;
        uint32_t              maxPerStageDescriptorSampledImages;
        uint32_t              maxPerStageDescriptorStorageImages;
        uint32_t              maxPerStageDescriptorInputAttachments;
        uint32_t              maxPerStageResources;
        uint32_t              maxDescriptorSetSamplers;
        uint32_t              maxDescriptorSetUniformBuffers;
        uint32_t              maxDescriptorSetUniformBuffersDynamic;
        uint32_t              maxDescriptorSetStorageBuffers;
        uint32_t              maxDescriptorSetStorageBuffersDynamic;
        uint32_t              maxDescriptorSetSampledImages;
        uint32_t              maxDescriptorSetStorageImages;
        uint32_t              maxDescriptorSetInputAttachments;
        uint32_t              maxVertexInputAttributes;
        uint32_t              maxVertexInputBindings;
        uint32_t              maxVertexInputAttributeOffset;
        uint32_t              maxVertexInputBindingStride;
        uint32_t              maxVertexOutputComponents;
        uint32_t              maxTessellationGenerationLevel;
        uint32_t              maxTessellationPatchSize;
        uint32_t              maxTessellationControlPerVertexInputComponents;
        uint32_t              maxTessellationControlPerVertexOutputComponents;
        uint32_t              maxTessellationControlPerPatchOutputComponents;
        uint32_t              maxTessellationControlTotalOutputComponents;
        uint32_t              maxTessellationEvaluationInputComponents;
        uint32_t              maxTessellationEvaluationOutputComponents;
        uint32_t              maxGeometryShaderInvocations;
        uint32_t              maxGeometryInputComponents;
        uint32_t              maxGeometryOutputComponents;
        uint32_t              maxGeometryOutputVertices;
        uint32_t              maxGeometryTotalOutputComponents;
        uint32_t              maxFragmentInputComponents;
        uint32_t              maxFragmentOutputAttachments;
        uint32_t              maxFragmentDualSrcAttachments;
        uint32_t              maxFragmentCombinedOutputResources;
        uint32_t              maxComputeSharedMemorySize;
        uint32_t              maxComputeWorkGroupCount[3];
        uint32_t              maxComputeWorkGroupInvocations;
        uint32_t              maxComputeWorkGroupSize[3];
        uint32_t              subPixelPrecisionBits;
        uint32_t              subTexelPrecisionBits;
        uint32_t              mipmapPrecisionBits;
        uint32_t              maxDrawIndexedIndexValue;
        uint32_t              maxDrawIndirectCount;
        float                 maxSamplerLodBias;
        float                 maxSamplerAnisotropy;
        uint32_t              maxViewports;
        uint32_t              maxViewportDimensions[2];
        float                 viewportBoundsRange[2];
        uint32_t              viewportSubPixelBits;
        size_t                minMemoryMapAlignment;
        VkDeviceSize          minTexelBufferOffsetAlignment;
        VkDeviceSize          minUniformBufferOffsetAlignment;
        VkDeviceSize          minStorageBufferOffsetAlignment;
        int32_t               minTexelOffset;
        uint32_t              maxTexelOffset;
        int32_t               minTexelGatherOffset;
        uint32_t              maxTexelGatherOffset;
        float                 minInterpolationOffset;
        float                 maxInterpolationOffset;
        uint32_t              subPixelInterpolationOffsetBits;
        uint32_t              maxFramebufferWidth;
        uint32_t              maxFramebufferHeight;
        uint32_t              maxFramebufferLayers;
        VkSampleCountFlags    framebufferColorSampleCounts;
        VkSampleCountFlags    framebufferDepthSampleCounts;
        VkSampleCountFlags    framebufferStencilSampleCounts;
        VkSampleCountFlags    framebufferNoAttachmentsSampleCounts;
        uint32_t              maxColorAttachments;
        VkSampleCountFlags    sampledImageColorSampleCounts;
        VkSampleCountFlags    sampledImageIntegerSampleCounts;
        VkSampleCountFlags    sampledImageDepthSampleCounts;
        VkSampleCountFlags    sampledImageStencilSampleCounts;
        VkSampleCountFlags    storageImageSampleCounts;
        uint32_t              maxSampleMaskWords;
        VkBool32              timestampComputeAndGraphics;
        float                 timestampPeriod;
        uint32_t              maxClipDistances;
        uint32_t              maxCullDistances;
        uint32_t              maxCombinedClipAndCullDistances;
        uint32_t              discreteQueuePriorities;
        float                 pointSizeRange[2];
        float                 lineWidthRange[2];
        float                 pointSizeGranularity;
        float                 lineWidthGranularity;
        VkBool32              strictLines;
        VkBool32              standardSampleLocations;
        VkDeviceSize          optimalBufferCopyOffsetAlignment;
        VkDeviceSize          optimalBufferCopyRowPitchAlignment;
        VkDeviceSize          nonCoherentAtomSize;
    } VkPhysicalDeviceLimits;
        """
        print(f"{WARNING}Limites do dispositivo físico:{RESET}")
        print(f"\t{OKGREEN}Tamanho máximo da imagem 1D: {OKBLUE}{limits.maxImageDimension1D}")
        print(f"\t{OKGREEN}Tamanho máximo da imagem 2D: {OKBLUE}{limits.maxImageDimension2D}")
        print(f"\t{OKGREEN}Tamanho máximo da imagem 3D: {OKBLUE}{limits.maxImageDimension3D}")
        print(f"\t{OKGREEN}Tamanho máximo da imagem do cubo 2D: {OKBLUE}{limits.maxImageDimensionCube}")
        print(f"\t{OKGREEN}Máximo de camadas de matriz de imagem: {OKBLUE}{limits.maxImageArrayLayers}")
        print(f"\t{OKGREEN}Maximum Descriptor Sets per stage: {OKBLUE}{limits.maxBoundDescriptorSets}")
        print(f"\t{OKGREEN}Máximo de descritores do amostrador por estágio: {OKBLUE}{limits.maxPerStageDescriptorSamplers}")

    def log_device_properties(self, device) -> None:
        """
            Imprime as propriedades de um dispositivo físico no console.

            Parâmetros:

                device (VkPhysicalDevice): o dispositivo físico a ser consultado e registrado
        """

        if not self.debug_mode:
            return
        
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

        variant, major, minor, patch = self._extract_version_number(properties.apiVersion)
        print(f"{ORANGE}Versão da API do dispositivo: Variante: {variant}, Major: {major}, Minor: {minor}, Patch: {patch}{RESET}")

        # driverVersion: a convenção sobre como os números de driver são empacotados é específica do fornecedor
        if (properties.vendorID == 4318):
            print(f"{OKGREEN}----Nvidia Card Detectado----{RESET}")
            driver_version = self._extract_driver_version_nvidia(properties.driverVersion)
        elif (os.name == "nt" and properties.vendorID == 0x8086):
            print(f"{OKGREEN}----Intel Windows Detectado----{RESET}")
            driver_version = self._extract_driver_version_intel(properties.driverVersion)
        else:
            print(f"{OKGREEN}----Fallback para o controle de versão padrão do Vulkan----{RESET}")
            driver_version = self._extract_driver_version_standard(properties.driverVersion)
        print(f"{WARNING}Versão do driver do dispositivo: {OKGREEN}{driver_version}{RESET}")

        if properties.deviceType in self.physical_device_types:
            print(f"{WARNING}Tipo de dispositivo: {OKGREEN}",end="")
            print(self.physical_device_types[properties.deviceType])
        
        print(f"{WARNING}Nome do dispositivo: {OKGREEN}{properties.deviceName}{RESET}")

        # ID único do cache do pipeline para garantir a exclusividade dos pipelines em Vulkan
        print(f"{WARNING}ID universalmente exclusivo do cache do Pipeline: {OKGREEN}", end="")
        for byte in properties.pipelineCacheUUID:
            print(byte, end=" ")
        print()

        self._log_physical_device_limits(properties.limits)

    def _log_transform_bits(self, bits: int) -> list[str]:
        """
            Obtém os tipos de transformação de um determinado sinalizador.

            Parâmetros:
                bits (int): O número inteiro que representa um conjunto de transformações.
            
            Retorna:
                list[str]: As transformações contidas no sinalizador inteiro.
        """

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
            result.append("Rotação de 90 graus")
        if (bits & VK_SURFACE_TRANSFORM_ROTATE_180_BIT_KHR):
            result.append("Rotação de 180 graus")
        if (bits & VK_SURFACE_TRANSFORM_ROTATE_270_BIT_KHR):
            result.append("Rotação de 270 graus")
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

    def _log_alpha_composite_bits(self, bits: int) -> list[str]:
        """
            Extrai os vários modos alfa compostos da máscara de bits fornecida

            Parâmetros:
                bits (int): A máscara de bits fornecida, que armazena um conjunto de modos alfa compostos.
            
            Retorna:
                list[str]: Descreve os modos alfa compostos na máscara de bits
        """
        
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

    def _log_image_usage_bits(self, bits: int) -> list[str]:
        """
            Extrai os vários modos de uso da imagem da máscara de bits fornecida

            Parâmetros:
                bits (int): A máscara de bits fornecida, que armazena vários modos de uso da imagem.
            
            Retorna:
                list[str]: Descreve os modos de uso da imagem na máscara de bits
        """

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
            result.append("transfer src: a imagem pode ser usada como a origem de um comando de transferência.\n")
        if (bits & VK_IMAGE_USAGE_TRANSFER_DST_BIT):
            result.append("transfer dst: a imagem pode ser usada como destino de um comando de transferência.")
        if (bits & VK_IMAGE_USAGE_SAMPLED_BIT):
            result.append("""
                sampled: pode ser usada para criar um VkImageView adequado para ocupar um slot 
                VkDescriptorSet do tipo VK_DESCRIPTOR_TYPE_SAMPLED_IMAGE ou 
                VK_DESCRIPTOR_TYPE_COMBINED_IMAGE_SAMPLER, e ser amostrada por um shader.""")
        if (bits & VK_IMAGE_USAGE_STORAGE_BIT):
            result.append("""
                storage: pode ser usada para criar um VkImageView adequado para ocupar um slot 
                VkDescriptorSet do tipo VK_DESCRIPTOR_TYPE_STORAGE_IMAGE.""")
        if (bits & VK_IMAGE_USAGE_COLOR_ATTACHMENT_BIT):
            result.append("""
                color attachment: a imagem pode ser usada para criar um VkImageView adequado para uso como 
                um anexo de cor ou resolução em um VkFramebuffer.""")
        if (bits & VK_IMAGE_USAGE_DEPTH_STENCIL_ATTACHMENT_BIT):
            result.append("""
                depth/stencil attachment: pode ser usada para criar um VkImageView 
                adequado para uso como um anexo de resolução de profundidade/estêncil ou profundidade/estêncil em um VkFramebuffer.""")
        if (bits & VK_IMAGE_USAGE_TRANSIENT_ATTACHMENT_BIT ):
            result.append("""
                transient attachment: as implementações podem suportar o uso de alocações de memória 
                com o VK_MEMORY_PROPERTY_LAZILY_ALLOCATED_BIT para fazer o backup de uma imagem com esse uso. Esse bit 
                bit pode ser definido para qualquer imagem que possa ser usada para criar um VkImageView adequado para uso como 
                uma cor, resolução, profundidade/estêncil ou anexo de entrada.""")
        if (bits & VK_IMAGE_USAGE_INPUT_ATTACHMENT_BIT):
            result.append("""
                input attachment: a imagem pode ser usada para criar um VkImageView adequado para 
                ocupar o slot VkDescriptorSet do tipo VK_DESCRIPTOR_TYPE_INPUT_ATTACHMENT; ser lida de um 
                um shader como um anexo de entrada; e ser usado como um anexo de entrada em um framebuffer.""")
        if (bits & VK_IMAGE_USAGE_FRAGMENT_DENSITY_MAP_BIT_EXT):
            result.append("""
                fragment density map: pode ser usada para criar um VkImageView adequado 
                para uso como uma imagem de mapa de densidade de fragmento.""")

        return result

    def print(self, message: str) -> None:
        """
            Função simples para imprimir coisas simples.
        """

        if not self.debug_mode:
            return

        print(message)
    
    def log_list(self, items: list[str]) -> None:
        """
            Imprimir uma lista geral de itens
        """

        if not self.debug_mode:
            return
        
        for item in items:
            print(f"{GRAY_DARK}\t\"{item}\"{RESET}")
    
    def log_surface_capabilities(self, support) -> None:
        """
            Registra os recursos de um Vulkan Surface.

            Prarametros:
                support (VkSurfaceCapabilitiesKHR): descreve o suporte à cadeia de troca
        """

        if not self.debug_mode:
            return


        print(f"{HEADER}O Swapchain pode suportar os seguintes recursos de superfície:{RESET}")

        print(f"\t{WARNING}contagem mínima de imagens: {OKBLUE}{support.capabilities.minImageCount}")
        print(f"\t{WARNING}contagem máxima de imagens: {OKBLUE}{support.capabilities.maxImageCount}")

        print(f"\t{WARNING}extensão atual:")
        """
        typedef struct VkExtent2D {
            uint32_t    width;
            uint32_t    height;
        } VkExtent2D;
        """
        print(f"\t\t{OKBLUE}largura: {support.capabilities.currentExtent.width}")
        print(f"\t\taltura: {support.capabilities.currentExtent.height}")

        print(f"\t{WARNING}extensão mínima suportada:")
        print(f"\t\t{OKBLUE}largura: {support.capabilities.minImageExtent.width}")
        print(f"\t\taltura: {support.capabilities.minImageExtent.height}")

        print(f"\t{WARNING}extensão máxima suportada:")
        print(f"\t\t{OKBLUE}largura: {support.capabilities.maxImageExtent.width}")
        print(f"\t\taltura: {support.capabilities.maxImageExtent.height}")

        print(f"\t{WARNING}máximo de camadas de matriz de imagem: {OKBLUE}{support.capabilities.maxImageArrayLayers}")

            
        print(f"\t{WARNING}transformações suportadas:{OKBLUE}")
        stringList = self._log_transform_bits(support.capabilities.supportedTransforms)
        for line in stringList:
            print(f"\t\t{line}")

        print(f"\t{WARNING}transformação atual:{OKBLUE}")
        stringList = self._log_transform_bits(support.capabilities.currentTransform)
        for line in stringList:
            print(f"\t\t{line}")

        print(f"\t{WARNING}operações alfa suportadas:{OKBLUE}")
        stringList = self._log_alpha_composite_bits(support.capabilities.supportedCompositeAlpha)
        for line in stringList:
            print(f"\t\t{line}")

        print(f"\t{WARNING}uso de imagem suportado:{OKBLUE}")
        stringList = self._log_image_usage_bits(support.capabilities.supportedUsageFlags)
        for line in stringList:
            print(f"\t\t{line}")
    
    def log_surface_format(self, surface_format) -> None:
        """
            Imprime o formato e o espaço de cores do formato fornecido.

            Parâmetros:
                surface_format (VkSurfaceFormatKHR): O formato fornecido
        """

        if not self.debug_mode:
            return
        
        """
            * typedef struct VkSurfaceFormatKHR {
                VkFormat           format;
                VkColorSpaceKHR    colorSpace;
            } VkSurfaceFormatKHR;
        """

        print(f"\t\t{OKBLUE}formato de pixel suportado: {RESET}{self.format_lookup[surface_format.format]}")
        print(f"\t\t{OKBLUE}espaço de cores suportado: {RESET}{self.colorspace_lookup[surface_format.colorSpace]}")

    
logger = Logger()