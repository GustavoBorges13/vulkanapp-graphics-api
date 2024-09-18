from config import *

validationLayers = ["VK_LAYER_KHRONOS_validation"]

def supported(extensions, layers, debug):

    """
        ExtensionProperties( std::array<char, VK_MAX_EXTENSION_NAME_SIZE> const & extensionName_ = {},
                           uint32_t                                             specVersion_ = {} )
    """
    #verifica o suporte das extensões
    supportedExtensions = [extension.extensionName for extension in vkEnumerateInstanceExtensionProperties(None)]

    if debug:
        print(f"{WARNING}O dispositivo pode suportar as seguintes extensões:{RESET}")
        for supportedExtension in supportedExtensions:
            print(f"{GRAY_DARK}\t\"{supportedExtension}\"{RESET}")
    
    for extension in extensions:
        
        if extension in supportedExtensions:
            if debug:
                print(f"{OKGREEN}Extensão \"{extension}\" é suportada!{RESET}")
        else:
            if debug:
                print(f"{WARNING}Extensão \"{extension}\" não é suportada!{RESET}")
            return False

    #verifica o suporte das camadas
    supportedLayers = [layer.layerName for layer in vkEnumerateInstanceLayerProperties()]

    if debug:
        print(f"{WARNING}O dispositivo pode suportar as seguintes camadas:{RESET}")
        for supportedLayer in supportedLayers:
            print(f"{GRAY_DARK}\t\"{supportedLayer}\"{RESET}")

    for layer in layers:
        if layer in supportedLayers:
            if debug:
                print(f"{OKGREEN}Camada \"{layer}\" é suportada!{RESET}")
        else:
            if debug:
                print(f"{WARNING}Camada \"{layer}\" não é suportada!{RESET}")
            return False

    return True

def make_instance(debug, applicationName):
    if debug:
        print(f"{HEADER}:: Fazer uma instância...{RESET}")

    """
        Uma instância armazena todas as informações de estado por aplicação, é um identificador Vulkan
        (Um número inteiro opaco ou um valor de ponteiro utilizado para se referir a um objeto Vulkan)
        
        Podemos analisar o sistema e verificar até que versão é compatível,
        a partir de vulkan 1.1
        
        VkResult vkEnumerateInstanceVersion(
            uint32_t*                                   pApiVersion);
    """
    version = vkEnumerateInstanceVersion()
    
    if debug:
        print(
            f"{OKBLUE}O sistema pode suportar a variante vulkan: {version >> 29}\
            , Major: {VK_VERSION_MAJOR(version)}\
            , Minor: {VK_VERSION_MINOR(version)}\
            , Patch: {VK_VERSION_PATCH(version)}{RESET}"
        )

    """
    Podemos então utilizar esta versão
    (Devemos apenas certificar-nos de definir o patch para 0 para melhor compatibilidade/estabilidade)
    """
    version &= ~(0xFFF)

    """
    Ou desça para uma versão anterior para garantir a compatibilidade com mais dispositivos
    VK_MAKE_API_VERSION(major, minor, patch)
    """
    version = VK_MAKE_VERSION(1, 3, 0)
    
    """
        from _vulkan.py:

        def VkApplicationInfo(
            sType=VK_STRUCTURE_TYPE_APPLICATION_INFO,
            pNext=None,
            pApplicationName=None,
            applicationVersion=None,
            pEngineName=None,
            engineVersion=None,
            apiVersion=None,
        )
    """

    appInfo = VkApplicationInfo(
        sType=VK_STRUCTURE_TYPE_APPLICATION_INFO,
        pApplicationName = applicationName,
        applicationVersion = version,
        pEngineName = "Fazer as coisas da maneira mais difícil",
        engineVersion = version,
        apiVersion = version
    )

    """
        Tudo com o Vulkan é “opt-in”, então nós precisamos consultar quais extensões o glfw precisa
        para fazer interface com o Vulkan.
    """
    extensions = glfw.get_required_instance_extensions()
    if debug:
        extensions.append(VK_EXT_DEBUG_REPORT_EXTENSION_NAME)

    if debug:
        print(f"{HEADER}:: Extensões a solicitar:{RESET}")

        for extensionName in extensions:
            print(f"{UNDERLINE}\t\" {extensionName}\"{RESET}")
    
    layers = []
    if debug:
        print(f"{HEADER}:: Camadas a solicitar:{RESET}")
        for layerName in validationLayers:
            print(f"{UNDERLINE}\t\" {layerName}\"{RESET}")
        layers.extend(validationLayers)

    supported(extensions, layers, debug)

    """
        de _vulkan.py:

        def VkInstanceCreateInfo(
            sType=VK_STRUCTURE_TYPE_INSTANCE_CREATE_INFO,
            pNext=None,
            flags=None,
            pApplicationInfo=None,
            enabledLayerCount=None,ppEnabledLayerNames=None,
            enabledExtensionCount=None,ppEnabledExtensionNames=None,
        )
    """
    createInfo = VkInstanceCreateInfo(
        sType=VK_STRUCTURE_TYPE_INSTANCE_CREATE_INFO,
        pApplicationInfo = appInfo,
        enabledLayerCount = len(layers), ppEnabledLayerNames = layers,
        enabledExtensionCount = len(extensions), ppEnabledExtensionNames = extensions
    )

    """
        def vkCreateInstance(
            pCreateInfo,
            pAllocator,
            pInstance=None,
        )
        
        lança uma exceção em caso de falha
    """
    try:
        return vkCreateInstance(createInfo, None)
    except:
        if (debug):
            print(f"{FAIL}Falha ao criar a instância!{RESET}")
        return None