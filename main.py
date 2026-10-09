import os
import random
from colorama import init, Fore, Style
from jugador import Jugador
from elementos import FabricaElementos

init(autoreset=True)

def limpiar():
    os.system("cls" if os.name == "nt" else "clear")

def print_at(r, c, s):
    print(f"\033[{r};{c}H{s}", end="", flush=True)

def marco(r_ini, c_ini, ancho, alto):
    for c in range(c_ini, c_ini + ancho):
        print_at(r_ini, c, "─")
        print_at(r_ini + alto - 1, c, "─")
    for r in range(r_ini, r_ini + alto):
        print_at(r, c_ini, "│")
        print_at(r, c_ini + ancho - 1, "│")
    print_at(r_ini, c_ini, "┌")
    print_at(r_ini, c_ini + ancho - 1, "┐")
    print_at(r_ini + alto - 1, c_ini, "└")
    print_at(r_ini + alto - 1, c_ini + ancho - 1, "┘")

class Juego:
    def __init__(self):
        self.limite_r_min = 4
        self.limite_r_max = 18
        self.limite_c_min = 3
        self.limite_c_max = 117
        self.jugador = Jugador(r=5, c=5, nombre="Merlina")
        self.paredes = set()
        self.elementos = []
        self.mensaje = "Explora la mazmorra con precaucion."
        self.ejecutando = True
        self.inicializar_mapa()

    def inicializar_mapa(self):
        # Paredes del borde
        for c in range(self.limite_c_min, self.limite_c_max + 1):
            self.paredes.add((self.limite_r_min, c))
            self.paredes.add((self.limite_r_max, c))
        for r in range(self.limite_r_min, self.limite_r_max + 1):
            self.paredes.add((r, self.limite_c_min))
            self.paredes.add((r, self.limite_c_max))

        # Pasillos internos
        for c in range(10, 40):
            self.paredes.add((8, c))
        for c in range(50, 110):
            self.paredes.add((8, c))
        for c in range(20, 95):
            self.paredes.add((13, c))
        for r in range(9, 13):
            self.paredes.add((r, 45))
            self.paredes.add((r, 75))

        # Tesoros ($)
        self.elementos.append(FabricaElementos.crear_tesoro(6, 12))
        self.elementos.append(FabricaElementos.crear_tesoro(6, 42))
        self.elementos.append(FabricaElementos.crear_tesoro(15, 25))
        self.elementos.append(FabricaElementos.crear_tesoro(16, 80))

        # Pociones (+)
        self.elementos.append(FabricaElementos.crear_pocion(6, 60))
        self.elementos.append(FabricaElementos.crear_pocion(10, 30))
        self.elementos.append(FabricaElementos.crear_pocion(15, 10))

        # Trampas (X)
        self.elementos.append(FabricaElementos.crear_trampa(10, 20))
        self.elementos.append(FabricaElementos.crear_trampa(10, 50))
        self.elementos.append(FabricaElementos.crear_trampa(15, 60))

        # Monstruos magicos (M)
        self.elementos.append(FabricaElementos.crear_monstruo(6, 90))
        self.elementos.append(FabricaElementos.crear_monstruo(10, 40))
        self.elementos.append(FabricaElementos.crear_monstruo(16, 30))
        self.elementos.append(FabricaElementos.crear_monstruo(16, 105))

    def dibujar(self):
        limpiar()
        marco(1, 1, 120, 24)
        titulo = "MAZMORRA PERDIDA DE LA UTN - PACÍFICO"
        col_titulo = (120 - len(titulo)) // 2
        print_at(2, col_titulo, Style.BRIGHT + titulo)

        # Dibujar paredes
        for r, c in self.paredes:
            print_at(r, c, Fore.WHITE + "░")

        # Dibujar elementos
        for elem in self.elementos:
            print_at(elem.r, elem.c, elem.color + elem.simbolo)

        # Dibujar heroe
        print_at(self.jugador.r, self.jugador.c, Fore.CYAN + Style.BRIGHT + self.jugador.simbolo)

        # Panel inferior
        corazones = "♥️" * max(1, self.jugador.vida // 20)
        estado = (f"JUGADOR: {self.jugador.nombre} | VIDA: [{corazones}] {self.jugador.vida}/{self.jugador.vida_max} "
                  f"| ORO: {self.jugador.oro} pts | POSICIÓN: (Fila: {self.jugador.r}, Col: {self.jugador.c})")
        print_at(20, 3, estado)
        print_at(21, 3, f"MENSAJE: {self.mensaje}")
        print_at(22, 3, "Moverse (W=Arriba, S=Abajo, A=Izquierda, D=Derecha, Q=Salir): ")

    def mover_monstruos(self):
        ocupadas = set(self.paredes)
        for elem in self.elementos:
            if elem.tipo != "MONSTRUO":
                ocupadas.add((elem.r, elem.c))

        monstruos = [e for e in self.elementos if e.tipo == "MONSTRUO"]
        nuevas_posiciones = set()

        for m in monstruos:
            posicion_valida = False
            intentos = 0
            while not posicion_valida and intentos < 200:
                intentos += 1
                nr = random.randint(self.limite_r_min + 1, self.limite_r_max - 1)
                nc = random.randint(self.limite_c_min + 1, self.limite_c_max - 1)

                if (nr, nc) not in ocupadas and (nr, nc) not in nuevas_posiciones:
                    posicion_valida = True
                    m.r = nr
                    m.c = nc
                    nuevas_posiciones.add((nr, nc))

                    if nr == self.jugador.r and nc == self.jugador.c:
                        self.jugador.vida = 0
                        self.mensaje = Fore.RED + "¡Un monstruo aparecio sobre ti y te derroto al instante!"

    def procesar_turno(self, accion):
        accion = accion.strip().upper()
        if accion == "Q":
            self.ejecutando = False
            return

        movimientos = {"W": (-1, 0), "S": (1, 0), "A": (0, -1), "D": (0, 1)}
        if accion not in movimientos:
            self.mensaje = "Comando invalido. Use W, A, S, D o Q."
            return

        dr, dc = movimientos[accion]
        nueva_r = self.jugador.r + dr
        nueva_c = self.jugador.c + dc

        if (nueva_r, nueva_c) in self.paredes:
            self.mensaje = "¡Atención! No puedes atravesar la pared (░)."
            return

        self.jugador.mover(dr, dc)
        self.mensaje = "Avanzaste por la mazmorra."

        for elem in self.elementos[:]:
            if elem.r == self.jugador.r and elem.c == self.jugador.c:
                if elem.tipo == "TESORO":
                    self.jugador.sumar_oro(50)
                    self.mensaje = Fore.YELLOW + "¡Recogiste un tesoro! +50 de oro."
                    self.elementos.remove(elem)
                elif elem.tipo == "POCION":
                    self.jugador.curar(25)
                    self.mensaje = Fore.GREEN + "¡Bebiste una pocion! +25 de salud."
                    self.elementos.remove(elem)
                elif elem.tipo == "TRAMPA":
                    self.jugador.recibir_dano(20)
                    self.mensaje = Fore.MAGENTA + "¡Caiste en una trampa! Perdiste 20 de vida."
                    self.elementos.remove(elem)
                elif elem.tipo == "MONSTRUO":
                    self.jugador.vida = 0
                    self.mensaje = Fore.RED + "¡Atacaste de frente a un monstruo y pereciste!"

        if self.jugador.vida > 0:
            self.mover_monstruos()

        tesoros = [e for e in self.elementos if e.tipo == "TESORO"]
        if not tesoros:
            self.dibujar()
            print_at(23, 3, Fore.GREEN + Style.BRIGHT + "¡Victoria! Has recolectado todos los tesoros.")
            self.ejecutando = False
            input()

        if self.jugador.vida <= 0:
            self.dibujar()
            print_at(23, 3, Fore.RED + Style.BRIGHT + "Has muerto. Fin del juego.")
            self.ejecutando = False
            input()

    def ejecutar(self):
        while self.ejecutando:
            self.dibujar()
            print_at(22, 65, "")
            try:
                tecla = input()
            except (KeyboardInterrupt, EOFError):
                break
            self.procesar_turno(tecla)

if __name__ == "__main__":
    juego = Juego()
    juego.ejecutar()