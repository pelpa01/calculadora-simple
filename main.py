import pygame
import sys
import math  
 
# Inicializa pygame
pygame.init()
 
# Configuración de la pantalla
ANCHO, ALTO = 800, 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Mover un sprite y disparar")
 
# Colores
ROJO = (255, 0, 0)
NEGRO = (0, 0, 0)
 
# Configuración inicial del círculo
x, y = ANCHO // 2, ALTO // 2
radio = 20
velocidad = 5
 
# Cargar el sprite
sprite = pygame.image.load("heroe.png")
sprite = pygame.transform.scale(sprite, (50, 50))  # Escalamos el sprite.
sprite_rect = sprite.get_rect()
sprite_rect.center = (x, y)  # Posición inicial del sprite
 
# Cargar el objeto de disparo
disparo = pygame.image.load("disparo.png")  # Cargamos la imagen del disparo.
disparo = pygame.transform.scale(disparo, (20, 20))  # Escalamos el disparo.
 
# Lista de disparos
disparos = []  # Creamos una lista para almacenar los disparos activos.
 
# ACTUALIZACIÓN: Cargar textura de suelo
fondo = pygame.image.load("fondo.png")
fondo = pygame.transform.scale(fondo, (150, 150))  # Escalamos las baldosas para que sean manejables.
 
# ACTUALIZACIÓN: Función para dibujar suelo en baldosas repetidas
def dibujar_suelo():
    for fila in range(0, ALTO, fondo.get_height()):  # Iteramos por filas.
        for columna in range(0, ANCHO, fondo.get_width()):  # Iteramos por columnas.
            pantalla.blit(fondo, (columna, fila))  # Dibujamos cada baldosa.
 
# Bucle principal
reloj = pygame.time.Clock()
 
while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
 
        # Detectar clic del mouse para disparar.
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:  # Botón izquierdo del mouse.
            mouse_x, mouse_y = pygame.mouse.get_pos()
            dx = mouse_x - x
            dy = mouse_y - y
            angle = math.atan2(-dy, dx)  # Ángulo hacia el mouse.
            disparos.append({"pos": [x, y], "vel": [math.cos(angle) * 10, -math.sin(angle) * 10]})  # Añadir disparo.
 
    # Detectar teclas presionadas
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_UP] or teclas[pygame.K_w]:
        y -= velocidad
    if teclas[pygame.K_DOWN] or teclas[pygame.K_s]:
        y += velocidad
    if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
        x -= velocidad
    if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
        x += velocidad
 
    # Actualizar posición del sprite
    sprite_rect.center = (x, y)
 
    # Calcular ángulo hacia el puntero del mouse
    mouse_x, mouse_y = pygame.mouse.get_pos()
    dx = mouse_x - x
    dy = mouse_y - y
    angle = math.degrees(math.atan2(-dy, dx))
    sprite_rotado = pygame.transform.rotate(sprite, angle)
    sprite_rect = sprite_rotado.get_rect(center=sprite_rect.center)
 
    # Mover los disparos
    for disparo_activo in disparos:
        disparo_activo["pos"][0] += disparo_activo["vel"][0]
        disparo_activo["pos"][1] += disparo_activo["vel"][1]
 
    # Dibujar todo
    dibujar_suelo()  # ACTUALIZACIÓN: Dibujar el suelo como fondo.
    pygame.draw.circle(pantalla, ROJO, (x, y), radio)  # Círculo rojo
    pantalla.blit(sprite_rotado, sprite_rect)
 
    # Dibujar los disparos
    for disparo_activo in disparos:
        pantalla.blit(disparo, disparo_activo["pos"])
 
    pygame.display.flip()
 
    # Controlar la velocidad de actualización
    reloj.tick(60)
