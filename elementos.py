from colorama import Fore, Style

class ElementoMapa:
    def __init__(self, r, c, tipo, simbolo, color):
        self.r = r
        self.c = c
        self.tipo = tipo
        self.simbolo = simbolo
        self.color = color

class FabricaElementos:
    @staticmethod
    def crear_tesoro(r, c):
        return ElementoMapa(r, c, "TESORO", "$", Fore.YELLOW)

    @staticmethod
    def crear_pocion(r, c):
        return ElementoMapa(r, c, "POCION", "+", Fore.GREEN)

    @staticmethod
    def crear_trampa(r, c):
        return ElementoMapa(r, c, "TRAMPA", "X", Fore.MAGENTA)

    @staticmethod
    def crear_monstruo(r, c):
        return ElementoMapa(r, c, "MONSTRUO", "M", Fore.RED)