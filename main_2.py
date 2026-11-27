import pygame
import random
import os
from juego_ranking import guardar_partida

pygame.init()

personajes = {
    "Gato cars": {
        "frente": "gato_carro_frente.png",
        "trasera": "gato_carro_trasera.png"
    },
    "Gato motoneta azul": {
        "frente": "gato_moto_azul_frente.png",
        "trasera": "gato_moto_azul_trasera.png"
    },
    "Gato bicicleta": {
        "frente": "gato_bici_frente.png",
        "trasera": "gato_bici_trasera.png"
    },
    "Gato Carro": {
        "frente": "gato_krato_frente.png",
        "trasera": "gato_krato_trasera.png"
    }
}

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Gato Kart")
clock = pygame.time.Clock()

# FONDO DEL MENU
fondo_menu = pygame.image.load("fondo_menu.png").convert()
fondo_menu = pygame.transform.smoothscale(fondo_menu, (800, 600))

# FONDO DEL MENU DE PERSONAJES
fondo_personajes = pygame.image.load("fondo_personajes.png").convert()
fondo_personajes = pygame.transform.smoothscale(fondo_personajes, (800, 600))

# FONDO CARRETERA
background = pygame.image.load("carretera.png").convert()
background = pygame.transform.smoothscale(background, (600, 1200))

# IMAGENES DE LOS OBSTACULOS
imagenes_gatos = [
    "gato_bomba_obs.png",
    "perro_golpe.png",
    "Sandbox_obs.png",
    "obstaculo.png",
    "aguacate.png",
    "platano.png",
    "fresa.png",
    "galleta.png",
    "pollo.png",
    "bomba.png"
]

# DIFICULTADES
niveles = {
    "Facil": {"velocidad": 6, "aparicion": 1500},
    "Medio": {"velocidad": 12, "aparicion": 1000},
    "Dificil": {"velocidad": 15, "aparicion": 750}
}

fuente = pygame.font.SysFont("arial", 35)
fuente_pequena = pygame.font.SysFont("arial", 22)
fuente_grande = pygame.font.SysFont("arial", 55)


def menu():
    while True:
        screen.blit(fondo_menu, (0, 0))

        opciones = [
            ("Facil", 220, (100, 200, 100)),
            ("Medio", 320, (255, 200, 80)),
            ("Dificil", 420, (255, 100, 100))
        ]

        for nombre, y, color in opciones:
            rect = pygame.Rect(275, y, 250, 65)
            pygame.draw.rect(screen, color, rect, border_radius=15)
            texto = fuente.render(nombre, True, (0, 0, 0))
            screen.blit(texto, texto.get_rect(center=rect.center))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for nombre, y, color in opciones:
                    rect = pygame.Rect(275, y, 250, 65)
                    if rect.collidepoint(event.pos):
                        return nombre

        pygame.display.flip()
        clock.tick(60)


def new_car(cars, ultimo_tipo):
    usadas = [car["tipo"] for car in cars]
    disponibles = [
        imagen for imagen in imagenes_gatos
        if imagen not in usadas and imagen != ultimo_tipo
    ]

    if len(disponibles) == 0:
        return None

    tipo = random.choice(disponibles)
    car_image = pygame.image.load(tipo).convert_alpha()
    car_image = pygame.transform.smoothscale(car_image, (85, 150))

    carriles = [120, 240, 360, 480, 600]
    carriles_libres = [
        x for x in carriles
        if not any(car["x"] == x and car["y"] < 20 for car in cars)
    ]

    if len(carriles_libres) == 0:
        return None

    return {
        "x": random.choice(carriles_libres),
        "y": -150,
        "image": car_image,
        "tipo": tipo,
        "mask": pygame.mask.from_surface(car_image)
    }


def is_crashing(cars, my_car):
    my_car_rect = my_car["image"].get_rect()
    my_car_rect.topleft = (my_car["x"], my_car["y"])
    my_car_mask = pygame.mask.from_surface(my_car["image"])

    for car in cars:
        car_rect = car["image"].get_rect()
        car_rect.topleft = (car["x"], car["y"])
        offset = (car_rect.x - my_car_rect.x, car_rect.y - my_car_rect.y)

        if my_car_mask.overlap(car["mask"], offset):
            return True

    return False


def show_score(score, nombre_jugador):
    score_surface = fuente.render(f"Score: {score}", True, (255, 255, 0))
    screen.blit(score_surface, (120, 20))

    jugador_surface = fuente_pequena.render(f"Corredor: {nombre_jugador}", True, (255, 255, 255))
    screen.blit(jugador_surface, (120, 60))


def game_over(score, nivel, jugador):
    # Guardar en SQL Server si el jugador inicio sesion
    guardado_msg = "Modo Invitado (no se guarda puntaje)"
    if jugador is not None:
        guardar_partida(jugador["id"], nivel, score)
        guardado_msg = f"Partida guardada en SQL para {jugador['nombre']}!"

    while True:
        screen.fill((30, 20, 40))

        texto = fuente_grande.render("GAME OVER", True, (255, 80, 100))
        screen.blit(texto, texto.get_rect(center=(400, 170)))

        puntos = fuente.render(f"Puntuacion: {score} ({nivel})", True, (255, 255, 255))
        screen.blit(puntos, puntos.get_rect(center=(400, 250)))

        aviso = fuente_pequena.render(guardado_msg, True, (185, 220, 193))
        screen.blit(aviso, aviso.get_rect(center=(400, 310)))

        volver = fuente.render("Presiona M para volver al menu", True, (255, 200, 220))
        screen.blit(volver, volver.get_rect(center=(400, 390)))

        salir = fuente_pequena.render("Presiona ESC para salir al inicio", True, (200, 200, 200))
        screen.blit(salir, salir.get_rect(center=(400, 445)))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    return True
                if event.key == pygame.K_ESCAPE:
                    return False

        pygame.display.flip()
        clock.tick(60)


def menu_personajes():
    opciones = []
    for nombre, imagenes in personajes.items():
        archivo_frente = imagenes["frente"]
        archivo_trasera = imagenes["trasera"]

        if os.path.isfile(archivo_frente) and os.path.isfile(archivo_trasera):
            imagen = pygame.image.load(archivo_frente).convert_alpha()
            imagen = pygame.transform.smoothscale(imagen, (130, 130))
            opciones.append((nombre, archivo_trasera, imagen))

    while True:
        screen.blit(fondo_personajes, (0, 0))
        botones = []

        for i, (nombre, archivo, imagen) in enumerate(opciones):
            x = (i + 1) * 800 // (len(opciones) + 1)
            rect = pygame.Rect(x - 90, 280, 180, 240)

            pygame.draw.rect(screen, (255, 255, 255), rect, border_radius=15)
            screen.blit(imagen, (x - 65, 300))

            texto = pygame.font.SysFont("arial", 20).render(nombre, True, (80, 20, 80))
            screen.blit(texto, texto.get_rect(center=(x, 465)))
            botones.append((rect, archivo))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return "volver"
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for rect, archivo in botones:
                    if rect.collidepoint(event.pos):
                        return archivo

        pygame.display.flip()
        clock.tick(60)


def jugar(nivel, personaje, jugador):
  Gato_en_scooter_image_original = pygame.image.load(personaje).convert_alpha()
  Gato_en_scooter_image_original = pygame.transform.smoothscale(
      Gato_en_scooter_image_original, (150, 150)
  )

  velocidad_base = niveles[nivel]["velocidad"]
  velocidad_maxima = velocidad_base + 6
  aparicion_base = niveles[nivel]["aparicion"]
  aparicion_minima = 400

  Gato_en_scooter_x = 400
  background_y = 0
  cars = []
  score = 0

  ultimo_tipo = None
  ultimo_obstaculo = pygame.time.get_ticks()
  nombre_mostrar = jugador["nombre"] if jugador else "Invitado"

  while True:
    clock.tick(60)

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        return False
      if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
        return True

    # Aumenta suavemente cada 100 puntos
    escalones = score // 100
    velocidad = min(velocidad_base + escalones * 0.5, velocidad_maxima)
    aparicion_actual = max(aparicion_minima, aparicion_base - escalones * 50)

    keys = pygame.key.get_pressed()
    angulo = 0

    if keys[pygame.K_RIGHT]:
      Gato_en_scooter_x += 6
      angulo = -5
    if keys[pygame.K_LEFT]:
      Gato_en_scooter_x -= 6
      angulo = 5

    Gato_en_scooter_x = max(100, min(Gato_en_scooter_x, 550))
    Gato_en_scooter_image = pygame.transform.rotate(
        Gato_en_scooter_image_original, angulo
    )

    background_y += velocidad
    if background_y >= 1200:
      background_y -= 1200

    tiempo_actual = pygame.time.get_ticks()
    if tiempo_actual - ultimo_obstaculo >= aparicion_actual:
      c = new_car(cars, ultimo_tipo)
      if c is not None:
        cars.append(c)
        ultimo_tipo = c["tipo"]
      ultimo_obstaculo = tiempo_actual

    for car in cars[:]:
      car["y"] += velocidad
      if car["y"] > 600:
        cars.remove(car)
        score += 10

    screen.fill((0, 0, 0))
    screen.blit(background, (100, background_y))
    screen.blit(background, (100, background_y - 1200))
    screen.blit(Gato_en_scooter_image, (Gato_en_scooter_x, 425))

    for car in cars:
      screen.blit(car["image"], (car["x"], car["y"]))

    show_score(score, nombre_mostrar)
    pygame.display.flip()

    my_car_dict = {
        "x": Gato_en_scooter_x,
        "y": 425,
        "image": Gato_en_scooter_image,
    }

    if is_crashing(cars, my_car_dict):
      return game_over(score, nivel, jugador)

def ejecutar_juego(jugador=None):
    global screen
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("GATO KART")

    while True:
        personaje = menu_personajes()
        if personaje is None or personaje == "volver":
            break

        nivel = menu()
        if nivel is None:
            break

        continuar = jugar(nivel, personaje, jugador)
        if not continuar:
            break


if __name__ == "__main__":
    from index import ejecutar_index
    ejecutar_index()