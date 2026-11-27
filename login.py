
import pygame
import os

pygame.init()

ANCHO = 1000
ALTO = 700

pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("GATO KART | Iniciar sesión")

reloj = pygame.time.Clock()

# COLORES
CREMA = (255, 248, 232)
ROSA = (247, 190, 205)
ROSA_OSCURO = (190, 112, 137)
LILA = (211, 195, 235)
BLANCO = (255, 255, 255)
MARRON = (105, 76, 72)
GRIS = (160, 145, 140)

# FUENTES
fuente_titulo = pygame.font.SysFont("consolas", 42, bold=True)
fuente_texto = pygame.font.SysFont("consolas", 19)
fuente_boton = pygame.font.SysFont("consolas", 19, bold=True)
fuente_pequena = pygame.font.SysFont("consolas", 15)

# FONDO
fondo = None

if os.path.isfile("fondo_login.jpeg"):
    imagen = pygame.image.load("fondo_login.jpeg").convert()
    fondo = pygame.transform.scale(imagen, (ANCHO, ALTO))


def dibujar_fondo():
    if fondo:
        pantalla.blit(fondo, (0, 0))
    else:
        pantalla.fill((158, 205, 235))


def dibujar_texto(texto, fuente, color, x, y):
    render = fuente.render(texto, True, color)
    pantalla.blit(render, (x, y))


def dibujar_campo(rect, texto, valor, activo, oculto=False):
    color_borde = ROSA_OSCURO if activo else LILA

    pygame.draw.rect(pantalla, BLANCO, rect)
    pygame.draw.rect(pantalla, color_borde, rect, 3)

    dibujar_texto(texto, fuente_texto, MARRON, rect.x, rect.y - 32)

    contenido = valor

    if oculto:
        contenido = "*" * len(valor)

    if contenido:
        dibujar_texto(
            contenido,
            fuente_texto,
            MARRON,
            rect.x + 12,
            rect.y + 14
        )


def dibujar_boton(rect, texto, color, mouse):
    color_actual = color

    if rect.collidepoint(mouse):
        color_actual = tuple(min(255, c + 15) for c in color)

    pygame.draw.rect(pantalla, (125, 91, 95), rect.move(4, 5))
    pygame.draw.rect(pantalla, color_actual, rect)
    pygame.draw.rect(pantalla, MARRON, rect, 3)

    render = fuente_boton.render(texto, True, MARRON)
    pantalla.blit(render, render.get_rect(center=rect.center))


def mostrar_login():

    correo = ""
    contrasena = ""

    campo_activo = "correo"
    mostrar_contrasena = False
    mensaje = ""

    campo_correo = pygame.Rect(355, 285, 290, 48)
    campo_contrasena = pygame.Rect(355, 390, 290, 48)

    boton_ver = pygame.Rect(655, 390, 65, 48)
    boton_ingresar = pygame.Rect(355, 485, 310, 58)
    boton_volver = pygame.Rect(400, 570, 220, 45)

    while True:

        mouse = pygame.mouse.get_pos()

        dibujar_fondo()

        # PANEL
        pygame.draw.rect(
            pantalla, (125, 91, 95),
            (289, 139, 430, 510)
        )

        pygame.draw.rect(
            pantalla, CREMA,
            (280, 130, 430, 510)
        )

        pygame.draw.rect(
            pantalla, ROSA_OSCURO,
            (280, 130, 430, 510), 5
        )

        pygame.draw.rect(
            pantalla, ROSA,
            (280, 130, 430, 85)
        )

        titulo = fuente_titulo.render(
            "INICIAR SESION", True, MARRON
        )

        pantalla.blit(
            titulo,
            titulo.get_rect(center=(495, 173))
        )

        dibujar_texto(
            "Bienvenido de nuevo, corredor!",
            fuente_pequena,
            MARRON,
            360,
            235
        )

        dibujar_campo(
            campo_correo,
            "CORREO ELECTRONICO",
            correo,
            campo_activo == "correo"
        )

        dibujar_campo(
            campo_contrasena,
            "CONTRASENA",
            contrasena,
            campo_activo == "contrasena",
            not mostrar_contrasena
        )

        dibujar_boton(
            boton_ver,
            "VER" if not mostrar_contrasena else "OC.",
            LILA,
            mouse
        )

        dibujar_boton(
            boton_ingresar,
            "INICIAR SESION",
            ROSA,
            mouse
        )

        dibujar_boton(
            boton_volver,
            "VOLVER",
            LILA,
            mouse
        )

        if mensaje:
            render = fuente_pequena.render(
                mensaje, True, ROSA_OSCURO
            )
            pantalla.blit(
                render,
                render.get_rect(center=(495, 455))
            )

        pygame.display.flip()

        for evento in pygame.event.get():

            if evento.type == pygame.QUIT:
                return ("salir", "", "")

            if evento.type == pygame.MOUSEBUTTONDOWN:

                if campo_correo.collidepoint(evento.pos):
                    campo_activo = "correo"

                elif campo_contrasena.collidepoint(evento.pos):
                    campo_activo = "contrasena"

                elif boton_ver.collidepoint(evento.pos):
                    mostrar_contrasena = not mostrar_contrasena

                elif boton_volver.collidepoint(evento.pos):
                    return ("volver", "", "")

                elif boton_ingresar.collidepoint(evento.pos):

                    if not correo.strip() or not contrasena:
                        mensaje = "Completa todos los campos."

                    else:
                        return ("ingresar", correo.strip(), contrasena)

            if evento.type == pygame.KEYDOWN:

                if evento.key == pygame.K_ESCAPE:
                    return ("volver", "", "")

                elif evento.key == pygame.K_TAB:
                    campo_activo = (
                        "contrasena"
                        if campo_activo == "correo"
                        else "correo"
                    )

                elif evento.key == pygame.K_BACKSPACE:

                    if campo_activo == "correo":
                        correo = correo[:-1]
                    else:
                        contrasena = contrasena[:-1]

                elif evento.key == pygame.K_RETURN:

                    if correo.strip() and contrasena:
                        return ("ingresar", correo.strip(), contrasena)

                else:

                    if evento.unicode.isprintable():

                        if campo_activo == "correo" and len(correo) < 80:
                            correo += evento.unicode

                        elif campo_activo == "contrasena" and len(contrasena) < 50:
                            contrasena += evento.unicode

        reloj.tick(60)