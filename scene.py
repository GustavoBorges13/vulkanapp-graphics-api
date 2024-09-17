from config import *

# A classe Scene, vai representar a cena gráfica onde objetos e posições serão gerados
# basicamente isso vai criar uma grade de posicoes que cobrirá a tela
class Scene:


    def __init__(self):
        #desenhando 3 listas diferentes
        # triangulo | quadrado | estrela
        self.triangle_positions = []
        self.square_positions = []
        self.star_positions = []

        y = -1.0
        while y < 1.0:
            self.triangle_positions.append(
                np.array([-0.3, y, 0], dtype = np.float32)
            )
            self.square_positions.append(
                np.array([0.0, y, 0], dtype = np.float32)
            )
            self.star_positions.append(
                np.array([0.3, y, 0], dtype = np.float32)
            )
            y += 0.2