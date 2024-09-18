from config import *
# https://registry.khronos.org/SPIR-V/specs/unified1/SPIRV.html

#verifica os arquivos shaders (.vert e .frag) compilados
def read_shader_src(filename):

    with open (filename, "rb") as file:

        code = file.read()
    
    return code

def create_shader_module(device, filename):

    code = read_shader_src(filename)

    createInfo = VkShaderModuleCreateInfo(
        sType=VK_STRUCTURE_TYPE_SHADER_MODULE_CREATE_INFO,
        codeSize=len(code),
        pCode=code
    )
    return vkCreateShaderModule(
        device = device, pCreateInfo = createInfo, pAllocator = None
    )