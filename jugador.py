from colorama import Fore, Style

class Jugador:
    def _init_(self, r=5, c=5, nombre="Heroe"):
        self.r = r
        self.c = c
        self.nombre = nombre
        self.vida = 60
        self.vida_max = 100
        self.oro = 0
        self.simbolo = "@"

    def mover(self, dr, dc):
        self.r += dr
        self.c += dc

    def recibir_dano(self, cantidad):
        self.vida = max(0, self.vida - cantidad)

    def curar(self, cantidad):
        self.vida = min(self.vida_max, self.vida + cantidad)

    def sumar_oro(self, cantidad):
        self.oro += cantidad