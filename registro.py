import pygame
import os
import re

pygame.init()

ANCHO = 1000
ALTO = 700

pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("GATO KART | Crear cuenta")

reloj = pygame.time.Clock()

# COLORES
CREMA = (255, 248, 232)
ROSA = (247, 190, 205)
ROSA_OSCURO = (190, 112, 137)
LILA = (211, 195, 235)
MENTA = (185, 220, 193)
BLANCO = (255, 255, 255)
MARRON = (105, 76, 72)

# FUENTES
fuente_titulo = pygame.font.SysFont("consolas", 39, bold=True)
fuente_texto = pygame.font.SysFont("consolas", 17)
fuente_boton = pygame.font.SysFont("consolas", 17, bold=True)
fuente_pequena = pygame.font.SysFont("consolas", 14)

# FONDO
fondo = None

if os.path.isfile("fondo_login.jpeg"):
    imagen = pygame.image.load("fondo_login.jpeg").convert()
    fondo = pygame.transform.scale(imagen, (ANCHO, ALTO))


def dibujar_fondo():
    if fondo is not None:
        pantalla.blit(fondo, (0, 0))
    else:
        pantalla.fill((158, 205, 235))


def dibujar_texto(texto, fuente, color, x, y):
    render = fuente.render(texto, True, color)
    pantalla.blit(render, (x, y))


def dibujar_campo(rect, etiqueta, valor, activo, oculto=False):

    color_borde = ROSA_OSCURO if activo else LILA

    pygame.draw.rect(pantalla, BLANCO, rect)
    pygame.draw.rect(pantalla, color_borde, rect, 3)

    dibujar_texto(
        etiqueta,
        fuente_texto,
        MARRON,
        rect.x,
        rect.y - 25
    )

    contenido = "*" * len(valor) if oculto else valor

    if contenido:
        render = fuente_texto.render(
            contenido, True, MARRON
        )
        pantalla.blit(
            render,
            (rect.x + 10, rect.y + 12)
        )


def dibujar_boton(rect, texto, color, mouse):

    color_actual = color

    if rect.collidepoint(mouse):
        color_actual = tuple(
            min(255, c + 15) for c in color
        )

    pygame.draw.rect(
        pantalla, (125, 91, 95), rect.move(4, 5)
    )

    pygame.draw.rect(
        pantalla, color_actual, rect
    )

    pygame.draw.rect(
        pantalla, MARRON, rect, 3
    )

    render = fuente_boton.render(
        texto, True, MARRON
    )

    pantalla.blit(
        render,
        render.get_rect(center=rect.center)
    )


def mostrar_registro():

    nombre = ""
    correo = ""
    contrasena = ""
    confirmar = ""

    campo_activo = "nombre"
    mostrar_claves = False
    mensaje = ""

    campo_nombre = pygame.Rect(365, 235, 270, 40)
    campo_correo = pygame.Rect(365, 315, 270, 40)
    campo_contrasena = pygame.Rect(365, 395, 270, 40)
    campo_confirmar = pygame.Rect(365, 475, 270, 40)

    boton_ver = pygame.Rect(645, 395, 65, 40)
    boton_crear = pygame.Rect(355, 545, 310, 50)
    boton_volver = pygame.Rect(400, 610, 220, 40)

    while True:

        mouse = pygame.mouse.get_pos()

        dibujar_fondo()

        # PANEL
        pygame.draw.rect(
            pantalla,
            (125, 91, 95),
            (289, 85, 430, 585)
        )

        pygame.draw.rect(
            pantalla,
            CREMA,
            (280, 75, 430, 585)
        )

        pygame.draw.rect(
            pantalla,
            ROSA_OSCURO,
            (280, 75, 430, 585),
            5
        )

        pygame.draw.rect(
            pantalla,
            ROSA,
            (280, 75, 430, 80)
        )

        titulo = fuente_titulo.render(
            "CREAR CUENTA",
            True,
            MARRON
        )

        pantalla.blit(
            titulo,
            titulo.get_rect(center=(495, 115))
        )

        dibujar_texto(
            "Unete a la carrera mas gatuna!",
            fuente_pequena,
            MARRON,
            370,
            180
        )

        dibujar_campo(
            campo_nombre,
            "NOMBRE COMPLETO",
            nombre,
            campo_activo == "nombre"
        )

        dibujar_campo(
            campo_correo,
            "CORREO ELECTRONICO",
            correo,
            campo_activo == "correo"
        )

        dibujar_campo(
            campo_contrasena,
            "CONTRASENA (MINIMO 6)",
            contrasena,
            campo_activo == "contrasena",
            not mostrar_claves
        )

        dibujar_campo(
            campo_confirmar,
            "CONFIRMAR CONTRASENA",
            confirmar,
            campo_activo == "confirmar",
            not mostrar_claves
        )

        dibujar_boton(
            boton_ver,
            "VER" if not mostrar_claves else "OC.",
            LILA,
            mouse
        )

        dibujar_boton(
            boton_crear,
            "CREAR MI CUENTA",
            MENTA,
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
                mensaje,
                True,
                ROSA_OSCURO
            )

            pantalla.blit(
                render,
                render.get_rect(center=(495, 525))
            )

        pygame.display.flip()

        for evento in pygame.event.get():

            if evento.type == pygame.QUIT:
                return ("salir", "", "", "")

            if evento.type == pygame.MOUSEBUTTONDOWN:

                if campo_nombre.collidepoint(evento.pos):
                    campo_activo = "nombre"

                elif campo_correo.collidepoint(evento.pos):
                    campo_activo = "correo"

                elif campo_contrasena.collidepoint(evento.pos):
                    campo_activo = "contrasena"

                elif campo_confirmar.collidepoint(evento.pos):
                    campo_activo = "confirmar"

                elif boton_ver.collidepoint(evento.pos):
                    mostrar_claves = not mostrar_claves

                elif boton_volver.collidepoint(evento.pos):
                    return ("volver", "", "", "")

                elif boton_crear.collidepoint(evento.pos):

                    if not all([
                        nombre.strip(),
                        correo.strip(),
                        contrasena,
                        confirmar
                    ]):
                        mensaje = "Completa todos los campos."

                    elif not re.match(
                        r"^[^@\s]+@[^@\s]+\.[^@\s]+$",
                        correo.strip()
                    ):
                        mensaje = "El correo no es valido."

                    elif len(contrasena) < 6:
                        mensaje = "La contrasena necesita 6 caracteres."

                    elif contrasena != confirmar:
                        mensaje = "Las contrasenas no coinciden."

                    else:
                        return (
                            "validado",
                            nombre.strip(),
                            correo.strip(),
                            contrasena
                        )

            if evento.type == pygame.KEYDOWN:

                if evento.key == pygame.K_ESCAPE:
                    return ("volver", "", "", "")

                elif evento.key == pygame.K_TAB:

                    orden = [
                        "nombre",
                        "correo",
                        "contrasena",
                        "confirmar"
                    ]

                    indice = orden.index(campo_activo)
                    campo_activo = orden[
                        (indice + 1) % len(orden)
                    ]

                elif evento.key == pygame.K_BACKSPACE:

                    if campo_activo == "nombre":
                        nombre = nombre[:-1]

                    elif campo_activo == "correo":
                        correo = correo[:-1]

                    elif campo_activo == "contrasena":
                        contrasena = contrasena[:-1]

                    elif campo_activo == "confirmar":
                        confirmar = confirmar[:-1]

                else:

                    if evento.unicode.isprintable():

                        if campo_activo == "nombre" and len(nombre) < 60:
                            nombre += evento.unicode

                        elif campo_activo == "correo" and len(correo) < 80:
                            correo += evento.unicode

                        elif campo_activo == "contrasena" and len(contrasena) < 50:
                            contrasena += evento.unicode

                        elif campo_activo == "confirmar" and len(confirmar) < 50:
                            confirmar += evento.unicode

        reloj.tick(60)