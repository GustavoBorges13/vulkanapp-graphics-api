from config import *

# A classe Scene, vai representar a cena gráfica onde objetos e posições serão gerados
# basicamente isso vai criar uma grade de posicoes que cobrirá a tela
class Scene:


    def __init__(self):

        self.triangle_positions = []

        x = -1.0
        while x < 1.0:
            y = -1.0
            while y < 1.0:
                self.triangle_positions.append(
                    np.array([x, y, 0], dtype = np.float32)
                )
                y += 0.2
            x += 0.2