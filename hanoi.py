import pygame
import sys
import time

pygame.init()

# Dimensiones y colores
ANCHO, ALTO = 900, 600
VENTANA = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Torre de Hanói - Estructura de Pila (Stack)")

BLANCO = (255, 255, 255)
GRIS_OSCURO = (40, 40, 40)
COLOR_POSTE = (120, 80, 40)
COLOR_BASE = (80, 50, 20)
COLOR_TEXTO = (50, 50, 50)
COLOR_BOTON = (52, 152, 219)
COLOR_CAJA = (240, 240, 240)
COLOR_BORDE_CAJA = (41, 128, 185)

COLORES_DISCOS = [
    (231, 76, 60), (241, 196, 15), (46, 204, 113),
    (52, 152, 219), (155, 89, 182), (230, 126, 34),
    (26, 188, 156), (243, 156, 18), (142, 68, 173)
]

# Clase Stack (Pila) personalizada
class Stack:
    def __init__(self, nombre):
        self.nombre = nombre
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if not self.is_empty():
            return self.items.pop()
        return None

    def peek(self):
        if not self.is_empty():
            return self.items[-1]
        return None

    def is_empty(self):
        return len(self.items) == 0

    def size(self):
        return len(self.items)


def main():
    # Variables de estado
    texto_discos = "3"  # Texto ingresado por el usuario
    num_discos = 3
    modo = "MENU" # MENU, MANUAL, AUTO
    postes = [Stack("Origen"), Stack("Auxiliar"), Stack("Destino")]
    
    # Contadores y métricas
    movimientos = 0
    tiempo_inicio = 0
    tiempo_fin = 0
    
    # Variables para modo manual
    poste_seleccionado = None
    
    # Variables para modo automático
    pasos = []
    pasos_iter = None
    tiempo_ultimo_movimiento = 0
    velocidad = 300 # ms entre movimientos automáticos

    def reiniciar_juego(n):
        nonlocal postes, movimientos, tiempo_inicio, tiempo_fin, poste_seleccionado, pasos, pasos_iter
        postes = [Stack("Origen"), Stack("Auxiliar"), Stack("Destino")]
        for i in range(n, 0, -1):
            postes[0].push(i)
        movimientos = 0
        tiempo_inicio = time.time()
        tiempo_fin = 0
        poste_seleccionado = None
        pasos = []
        pasos_iter = None

    def resolver_hanoi(n, origen, destino, auxiliar, lista_pasos):
        if n == 1:
            lista_pasos.append((origen, destino))
            return
        resolver_hanoi(n - 1, origen, auxiliar, destino, lista_pasos)
        lista_pasos.append((origen, destino))
        resolver_hanoi(n - 1, auxiliar, destino, origen, lista_pasos)

    reloj = pygame.time.Clock()
    fuente = pygame.font.SysFont(None, 24)
    fuente_titulo = pygame.font.SysFont(None, 36)
    fuente_grande = pygame.font.SysFont(None, 48)

    ejecutando = True
    while ejecutando:
        VENTANA.fill(BLANCO)
        tiempo_actual = pygame.time.get_ticks()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False

            elif evento.type == pygame.KEYDOWN:
                if modo == "MENU":
                    if evento.key == pygame.K_BACKSPACE:
                        texto_discos = texto_discos[:-1]
                    elif evento.unicode.isdigit():
                        if len(texto_discos) < 2:  # Limitar a 2 dígitos para evitar locuras gráficas
                            texto_discos += evento.unicode
                    
                    # Actualizar número de discos si el texto no está vacío
                    if texto_discos != "" and int(texto_discos) > 0:
                        num_discos = int(texto_discos)
                    else:
                        num_discos = 1

            elif evento.type == pygame.MOUSEBUTTONDOWN:
                mx, my = evento.pos

                if modo == "MENU":
                    # Botón Modo Manual
                    if 200 <= mx <= 420 and 320 <= my <= 380:
                        modo = "MANUAL"
                        reiniciar_juego(num_discos)

                    # Botón Modo Automático
                    elif 480 <= mx <= 700 and 320 <= my <= 380:
                        modo = "AUTO"
                        reiniciar_juego(num_discos)
                        resolver_hanoi(num_discos, 0, 2, 1, pasos)
                        pasos_iter = iter(pasos)

                elif modo in ["MANUAL", "AUTO"]:
                    # Botón Volver al Menú
                    if 20 <= mx <= 140 and 20 <= my <= 60:
                        modo = "MENU"

                    # Lógica de clics para el Modo Manual
                    if modo == "MANUAL" and tiempo_fin == 0:
                        p_idx = -1
                        if 150 <= mx <= 300: p_idx = 0
                        elif 375 <= mx <= 525: p_idx = 1
                        elif 600 <= mx <= 750: p_idx = 2

                        if p_idx != -1:
                            if poste_seleccionado is None:
                                if not postes[p_idx].is_empty():
                                    poste_seleccionado = p_idx
                            else:
                                origen_p = postes[poste_seleccionado]
                                destino_p = postes[p_idx]
                                
                                disco_mov = origen_p.peek()
                                disco_dest = destino_p.peek()

                                if disco_dest is None or disco_mov < disco_dest:
                                    movido = origen_p.pop()
                                    destino_p.push(movido)
                                    movimientos += 1
                                    
                                    if postes[2].size() == num_discos:
                                        tiempo_fin = time.time()
                                        
                                poste_seleccionado = None

        # --- LÓGICA MODO AUTOMÁTICO ---
        if modo == "AUTO" and tiempo_fin == 0:
            if tiempo_actual - tiempo_ultimo_movimiento > velocidad:
                try:
                    orig, dest = next(pasos_iter)
                    disco = postes[orig].pop()
                    postes[dest].push(disco)
                    movimientos += 1
                    tiempo_ultimo_movimiento = tiempo_actual
                    
                    if postes[2].size() == num_discos:
                        tiempo_fin = time.time()
                except StopIteration:
                    pass

        # --- RENDERIZADO DE PANTALLAS ---
        if modo == "MENU":
            txt_t = fuente_titulo.render("JUEGO DE LA TORRE DE HANÓI", True, COLOR_TEXTO)
            VENTANA.blit(txt_t, (230, 80))

            txt_d = fuente.render("Escribe el número de discos deseados:", True, COLOR_TEXTO)
            VENTANA.blit(txt_d, (300, 170))

            # Cuadro de texto interactivo
            pygame.draw.rect(VENTANA, COLOR_CAJA, (390, 210, 120, 60), border_radius=8)
            pygame.draw.rect(VENTANA, COLOR_BORDE_CAJA, (390, 210, 120, 60), 2, border_radius=8)
            
            txt_input = fuente_grande.render(texto_discos, True, COLOR_TEXTO)
            VENTANA.blit(txt_input, (415, 222))

            # Botones de Modo
            pygame.draw.rect(VENTANA, (46, 204, 113), (200, 320, 220, 60), border_radius=10)
            txt_m = fuente_titulo.render("Jugar Manual", True, BLANCO)
            VENTANA.blit(txt_m, (230, 335))

            pygame.draw.rect(VENTANA, (231, 76, 60), (480, 320, 220, 60), border_radius=10)
            txt_a = fuente_titulo.render("Modo Automático", True, BLANCO)
            VENTANA.blit(txt_a, (495, 335))

        else:
            # Pantalla de Juego
            pygame.draw.rect(VENTANA, GRIS_OSCURO, (20, 20, 120, 40), border_radius=5)
            txt_vol = fuente.render("<- Menú", True, BLANCO)
            VENTANA.blit(txt_vol, (50, 30))

            tiempo_actual_juego = (tiempo_fin if tiempo_fin > 0 else time.time()) - tiempo_inicio
            txt_mov = fuente.render(f"Movimientos: {movimientos}", True, COLOR_TEXTO)
            txt_time = fuente.render(f"Tiempo: {tiempo_actual_juego:.2f} s", True, COLOR_TEXTO)
            txt_modo = fuente.render(f"Modo: {modo} ({num_discos} Discos)", True, COLOR_TEXTO)
            
            VENTANA.blit(txt_mov, (160, 30))
            VENTANA.blit(txt_time, (340, 30))
            VENTANA.blit(txt_modo, (550, 30))

            # Dibujar Base y Postes
            pygame.draw.rect(VENTANA, COLOR_BASE, (100, 480, 700, 20))
            pos_x_postes = [225, 450, 675]
            
            for x in pos_x_postes:
                pygame.draw.rect(VENTANA, COLOR_POSTE, (x - 8, 220, 16, 260))

            nombres_postes = ["Origen", "Auxiliar", "Destino"]
            for i, x in enumerate(pos_x_postes):
                t_p = fuente.render(nombres_postes[i], True, COLOR_TEXTO)
                VENTANA.blit(t_p, (x - 30, 505))

            # Dibujar Discos usando la estructura Stack (con escala dinámica para que no se salgan si pones muchos)
            for i, poste in enumerate(postes):
                x_poste = pos_x_postes[i]
                total_en_poste = poste.size()
                for j, tamano in enumerate(poste.items):
                    # Ajustar el ancho y alto automáticamente según la cantidad de discos
                    ancho = max(15, 140 - (num_discos * 4)) + (tamano * 10)
                    alto = max(10, min(24, 220 // num_discos))
                    y = 480 - ((j + 1) * (alto + 2))
                    x = x_poste - (ancho // 2)

                    color = COLORES_DISCOS[tamano % len(COLORES_DISCOS)]
                    b_color = (255, 255, 255) if (modo == "MANUAL" and poste_seleccionado == i and j == total_en_poste - 1) else GRIS_OSCURO
                    
                    pygame.draw.rect(VENTANA, color, (x, y, ancho, alto), border_radius=3)
                    pygame.draw.rect(VENTANA, b_color, (x, y, ancho, alto), 1, border_radius=3)

            # Mensaje de Victoria
            if postes[2].size() == num_discos:
                txt_win = fuente_titulo.render("¡FELICIDADES! ¡HAS COMPLETADO EL RETO!", True, (39, 174, 96))
                VENTANA.blit(txt_win, (180, 150))

        pygame.display.flip()
        reloj.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()