from config import *
import engine
import scene
import vklogging

class App:


    def __init__(self, width, height, glfw_title_name, debug_mode):

        vklogging.logger.set_debug_mode(debug_mode)

        # Constrói a janela GLFW e inicializa a engine gráfica
        self.build_glfw_window(width, height, glfw_title_name)

        # Inicializa o motor gráfico com parâmetros como dimensões e janela
        self.graphicsEngine = engine.Engine(width, height, self.window, glfw_title_name)
        self.scene = scene.Scene() #carrega a cena com grades de posicoes que cobrirá a tela
        
        # Variáveis para cálculo do framerate
        self.lastTime = glfw.get_time()         # Tempo do último frame
        self.currentTime = glfw.get_time()      # Tempo atual
        self.numFrames = 0                      # Contador de frames
        self.frameTime = 0                      # Tempo médio de um frame

    def build_glfw_window(self, width, height, glfw_title_name):

        #inicializar o glfw
        glfw.init()

        # Configurações da janela GLFW
        # Sem API de cliente (não cria contexto OpenGL por padrão), vamos conectar o Vulkan à janela mais tarde
        glfw.window_hint(GLFW_CONSTANTS.GLFW_CLIENT_API, GLFW_CONSTANTS.GLFW_NO_API)
        # Desabilita redimensionamento da janela para evitar quebra da swapchain
        glfw.window_hint(GLFW_CONSTANTS.GLFW_RESIZABLE, GLFW_CONSTANTS.GLFW_TRUE)
        
        # Cria a janela GLFW com as dimensões fornecidas
        self.window = glfw.create_window(width, height, glfw_title_name, None, None)

        # Verifica se a janela foi criada com sucesso
        if self.window is not None:
            vklogging.logger.print(f"{OKGREEN}Foi criada com êxito uma janela glfw chamada {glfw_title_name}, largura: {width}, altura: {height}{RESET}\n")
        else:
            vklogging.logger.print(f"{FAIL}Falha na criação da janela GLFW{RESET}\n")

    def calculate_framerate(self):

        # Atualiza o tempo atual e calcula o delta (diferença de tempo entre frames)
        self.currentTime = glfw.get_time()
        delta = self.currentTime - self.lastTime

        # Atualiza o título da janela com o framerate a cada segundo
        if delta >= 1:
            framerate = max(1, int(self.numFrames // delta))                    # Calcula o framerate
            glfw.set_window_title(self.window, f"Running at {framerate} fps.")  # Define o título da janela
            self.lastTime = self.currentTime                                    # Atualiza o tempo do último frame
            self.numFrames = -1                                                 # Reseta o contador de frames
            self.frameTime = 1000.0 / framerate                                 # Calcula o tempo médio de um frame em ms
        
        self.numFrames += 1                                                     # Incrementa o número de frames
        
    def run(self):

        # Loop principal da aplicação
        while not glfw.window_should_close(self.window):
            # Processa eventos do GLFW (como entradas de teclado e mouse)
            glfw.poll_events()

            # Chama o motor gráfico para renderizar a cena
            self.graphicsEngine.render(self.scene)

            # Calcula o framerate e atualiza a janela
            self.calculate_framerate()

    def close(self):
        # Fecha corretamente o motor gráfico
        self.graphicsEngine.close()