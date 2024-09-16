from config import *
import frame

class framebufferInput:
    """
    Classe para armazenar dados necessários para a criação de framebuffers.
    """
    def __init__(self):
        """
        Inicializa uma instância da classe FramebufferInput.
        """
        self.device = None
        self.renderpass = None
        self.swapchainExtent = None

def make_framebuffers(inputChunk, frames, debug):
    """
    Cria um framebuffer para cada quadro fornecido e o associa à entrada correspondente.
    """
    for i,frame in enumerate(frames):
        # Cria uma lista com os attachments necessários (neste caso, apenas um image_view)
        attachments = [frame.image_view,]

        framebufferInfo = VkFramebufferCreateInfo(
            renderPass = inputChunk.renderpass,
            attachmentCount = 1,
            pAttachments = attachments,
            width = inputChunk.swapchainExtent.width,
            height = inputChunk.swapchainExtent.height,
            layers=1
        )

        try:
            frame.framebuffer = vkCreateFramebuffer(
                inputChunk.device, framebufferInfo, None
            )

            if debug:
                print(f"{OKGREEN}Criou o framebuffer para o quadro {i}{RESET}")
            
        except:

            if debug:
                print(f"{FAIL}Falha ao criar o framebuffer para o quadro {i}{RESET}")