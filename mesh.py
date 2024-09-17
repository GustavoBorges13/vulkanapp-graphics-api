from config import *

def get_pos_color_binding_description():
    """
        Obtém a descrição da ligação de entrada para um formato de vértice
        (vec2 pos, vec3 color) formato de vértice
    """

    """
    typedef struct VkVertexInputBindingDescription {
        uint32_t             binding;
        uint32_t             stride;
        VkVertexInputRate    inputRate;
    } VkVertexInputBindingDescription;
    """

    return VkVertexInputBindingDescription(
        binding = 0, stride = 20, inputRate = VK_VERTEX_INPUT_RATE_VERTEX
    )

def get_pos_color_attribute_descriptions():
    """
        Obtém as descrições de atributos para um formato de vértice
        (vec2 pos, vec3 color) formato de vértice
    """

    """
    typedef struct VkVertexInputAttributeDescription {
        uint32_t    location;
        uint32_t    binding;
        VkFormat    format;
        uint32_t    offset;
    } VkVertexInputAttributeDescription;
    """

    return (
        VkVertexInputAttributeDescription(
            binding = 0, location = 0,
            format = VK_FORMAT_R32G32_SFLOAT,
            offset = 0
        ),
        VkVertexInputAttributeDescription(
            binding = 0, location = 1,
            format = VK_FORMAT_R32G32B32_SFLOAT,
            offset = 8
        )
    )