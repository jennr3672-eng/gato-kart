import os
import sys

if getattr(sys, "frozen", False):
    os.chdir(os.path.dirname(sys.executable))
import pygame
import os

from login import mostrar_login
from registro import mostrar_registro
from juego_ranking import (
    login_jugador,
    registrar_jugador,
    obtener_top10,
    actualizar_jugador,
    eliminar_jugador
)

pygame.init()

ANCHO = 1000
ALTO = 700

pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("GATO KART | Menu principal")

reloj = pygame.time.Clock()

# COLORES
CREMA = (255, 248, 232)
ROSA = (247, 190, 205)
ROSA_OSCURO = (190, 112, 137)
LILA = (211, 195, 235)
MENTA = (185, 220, 193)
AMARILLO = (255, 225, 158)
ROJO_SUAVE = (245, 150, 150)
BLANCO = (255, 255, 255)
MARRON = (105, 76, 72)
SOMBRA = (125, 91, 95)

# FUENTES
fuente_titulo = pygame.font.SysFont("consolas", 68, bold=True)
fuente_subtitulo = pygame.font.SysFont("consolas", 19, bold=True)
fuente_boton = pygame.font.SysFont("consolas", 20, bold=True)
fuente_pequena = pygame.font.SysFont("consolas", 15)

# FONDO
fondo = None
if os.path.isfile("fondo_login.jpeg"):
    imagen = pygame.image.load("fondo_login.jpeg").convert()
    fondo = pygame.transform.scale(imagen, (ANCHO, ALTO))

# GATITO
gato = None
for archivo in ["gato_moto_azul_frente.png", "gato_carro_frente.png", "gato_bici_frente.png"]:
    if os.path.isfile(archivo):
        gato = pygame.image.load(archivo).convert_alpha()
        gato = pygame.transform.scale(gato, (235, 235))
        break


def dibujar_fondo():
    if fondo is not None:
        pantalla.blit(fondo, (0, 0))
    else:
        pantalla.fill((158, 205, 235))


def dibujar_corazon(x, y, color):
    pygame.draw.rect(pantalla, color, (x + 5, y, 10, 10))
    pygame.draw.rect(pantalla, color, (x, y + 5, 20, 10))
    pygame.draw.rect(pantalla, color, (x + 5, y + 15, 10, 5))


def dibujar_decoraciones():
    dibujar_corazon(80, 210, ROSA)
    dibujar_corazon(900, 180, ROSA)
    dibujar_corazon(100, 580, AMARILLO)
    dibujar_corazon(870, 580, LILA)


def dibujar_titulo():
    titulo_sombra = fuente_titulo.render("GATO KART", True, MARRON)
    titulo = fuente_titulo.render("GATO KART", True, CREMA)
    rect = titulo.get_rect(center=(500, 85))
    pantalla.blit(titulo_sombra, (rect.x + 4, rect.y + 5))
    pantalla.blit(titulo, rect)

    subtitulo = fuente_subtitulo.render("LA CARRERA MAS GATUNA", True, BLANCO)
    pantalla.blit(subtitulo, subtitulo.get_rect(center=(500, 140)))


def dibujar_panel(titulo_panel="BIENVENIDO A GATO KART"):
    pygame.draw.rect(pantalla, SOMBRA, (493, 183, 425, 455))
    pygame.draw.rect(pantalla, CREMA, (480, 170, 425, 455))
    pygame.draw.rect(pantalla, ROSA_OSCURO, (480, 170, 425, 455), 5)
    pygame.draw.rect(pantalla, ROSA, (480, 170, 425, 60))
    pygame.draw.line(pantalla, ROSA_OSCURO, (480, 230), (905, 230), 4)

    texto = fuente_subtitulo.render(titulo_panel, True, MARRON)
    pantalla.blit(texto, texto.get_rect(center=(692, 200)))


def dibujar_boton(rect, texto, color, mouse):
    color_actual = tuple(min(255, c + 15) for c in color) if rect.collidepoint(mouse) else color
    pygame.draw.rect(pantalla, SOMBRA, rect.move(4, 5))
    pygame.draw.rect(pantalla, color_actual, rect)
    pygame.draw.rect(pantalla, MARRON, rect, 3)

    texto_render = fuente_boton.render(texto, True, MARRON)
    pantalla.blit(texto_render, texto_render.get_rect(center=rect.center))


def dibujar_personaje():
    if gato is not None:
        pantalla.blit(gato, gato.get_rect(center=(255, 410)))
    mensaje = fuente_subtitulo.render("MIAU! VAMOS A CORRER", True, MARRON)
    pantalla.blit(mensaje, mensaje.get_rect(center=(255, 555)))


# ==========================================
# PANTALLA VISUAL TOP 10 (VISTA SQL)
# ==========================================
def mostrar_pantalla_top10():
    ranking = obtener_top10()
    boton_volver = pygame.Rect(390, 585, 220, 50)

    while True:
        mouse = pygame.mouse.get_pos()
        dibujar_fondo()

        pygame.draw.rect(pantalla, SOMBRA, (189, 89, 630, 560))
        pygame.draw.rect(pantalla, CREMA, (180, 80, 630, 560))
        pygame.draw.rect(pantalla, ROSA_OSCURO, (180, 80, 630, 560), 5)
        pygame.draw.rect(pantalla, AMARILLO, (180, 80, 630, 70))

        titulo = fuente_subtitulo.render("RANKING TOP 10 - MEJORES CORREDORES", True, MARRON)
        pantalla.blit(titulo, titulo.get_rect(center=(495, 115)))

        encabezado = fuente_pequena.render(f"{'POS':<6} {'CORREDOR':<22} {'NIVEL MAX':<12} {'SCORE'}", True, ROSA_OSCURO)
        pantalla.blit(encabezado, (220, 175))
        pygame.draw.line(pantalla, MARRON, (210, 200), (780, 200), 2)

        if not ranking:
            vacio = fuente_pequena.render("Aun no hay puntuaciones registradas.", True, MARRON)
            pantalla.blit(vacio, vacio.get_rect(center=(495, 320)))
        else:
            for idx, fila in enumerate(ranking, start=1):
                linea = f"#{idx:<5} {str(fila[0])[:20]:<22} {str(fila[1]):<12} {fila[2]}"
                render = fuente_pequena.render(linea, True, MARRON)
                pantalla.blit(render, (220, 215 + (idx - 1) * 34))

        dibujar_boton(boton_volver, "VOLVER", LILA, mouse)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return "salir"
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                return "volver"
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                if boton_volver.collidepoint(evento.pos):
                    return "volver"

        pygame.display.flip()
        reloj.tick(60)


# ==========================================
# PANTALLA PERFIL (UPDATE Y DELETE CRUD)
# ==========================================
def mostrar_pantalla_perfil(jugador):
    nuevo_nombre = jugador["nombre"]
    nueva_clave = ""
    campo_activo = "nombre"
    mensaje = ""

    rect_nombre = pygame.Rect(350, 250, 300, 45)
    rect_clave = pygame.Rect(350, 345, 300, 45)
    btn_guardar = pygame.Rect(350, 420, 300, 50)
    btn_eliminar = pygame.Rect(350, 485, 300, 50)
    btn_volver = pygame.Rect(390, 555, 220, 45)

    while True:
        mouse = pygame.mouse.get_pos()
        dibujar_fondo()

        pygame.draw.rect(pantalla, SOMBRA, (289, 109, 430, 515))
        pygame.draw.rect(pantalla, CREMA, (280, 100, 430, 515))
        pygame.draw.rect(pantalla, ROSA_OSCURO, (280, 100, 430, 515), 5)
        pygame.draw.rect(pantalla, LILA, (280, 100, 430, 70))

        titulo = fuente_subtitulo.render("MI PERFIL DE CORREDOR", True, MARRON)
        pantalla.blit(titulo, titulo.get_rect(center=(495, 135)))

        info = fuente_pequena.render(f"Correo: {jugador['correo']}", True, MARRON)
        pantalla.blit(info, (350, 185))

        # Campo Nombre
        pantalla.blit(fuente_pequena.render("EDITAR NOMBRE:", True, MARRON), (350, 225))
        pygame.draw.rect(pantalla, BLANCO, rect_nombre)
        pygame.draw.rect(pantalla, ROSA_OSCURO if campo_activo == "nombre" else LILA, rect_nombre, 3)
        pantalla.blit(fuente_pequena.render(nuevo_nombre, True, MARRON), (rect_nombre.x + 10, rect_nombre.y + 14))

        # Campo Contraseña
        pantalla.blit(fuente_pequena.render("NUEVA CONTRASEÑA (MIN 6):", True, MARRON), (350, 320))
        pygame.draw.rect(pantalla, BLANCO, rect_clave)
        pygame.draw.rect(pantalla, ROSA_OSCURO if campo_activo == "clave" else LILA, rect_clave, 3)
        pantalla.blit(fuente_pequena.render("*" * len(nueva_clave), True, MARRON), (rect_clave.x + 10, rect_clave.y + 14))

        dibujar_boton(btn_guardar, "GUARDAR CAMBIOS", MENTA, mouse)
        dibujar_boton(btn_eliminar, "ELIMINAR CUENTA", ROJO_SUAVE, mouse)
        dibujar_boton(btn_volver, "VOLVER", LILA, mouse)

        if mensaje:
            msg_render = fuente_pequena.render(mensaje, True, ROSA_OSCURO)
            pantalla.blit(msg_render, msg_render.get_rect(center=(495, 402)))

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return "salir", jugador
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                if rect_nombre.collidepoint(evento.pos):
                    campo_activo = "nombre"
                elif rect_clave.collidepoint(evento.pos):
                    campo_activo = "clave"
                elif btn_volver.collidepoint(evento.pos):
                    return "volver", jugador
                elif btn_guardar.collidepoint(evento.pos):
                    if len(nuevo_nombre.strip()) < 2 or len(nueva_clave) < 6:
                        mensaje = "Nombre valido y clave min. 6 chars."
                    else:
                        if actualizar_jugador(jugador["id"], nuevo_nombre.strip(), nueva_clave):
                            jugador["nombre"] = nuevo_nombre.strip()
                            mensaje = "Datos actualizados en SQL!"
                        else:
                            mensaje = "Error al actualizar."
                elif btn_eliminar.collidepoint(evento.pos):
                    if eliminar_jugador(jugador["id"]):
                        return "eliminado", None
                    else:
                        mensaje = "Error al eliminar cuenta."

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_BACKSPACE:
                    if campo_activo == "nombre":
                        nuevo_nombre = nuevo_nombre[:-1]
                    else:
                        nueva_clave = nueva_clave[:-1]
                elif evento.unicode.isprintable():
                    if campo_activo == "nombre" and len(nuevo_nombre) < 50:
                        nuevo_nombre += evento.unicode
                    elif campo_activo == "clave" and len(nueva_clave) < 50:
                        nueva_clave += evento.unicode

        pygame.display.flip()
        reloj.tick(60)


# ==========================================
#  INDEX PRINCIPAL
# ==========================================
def mostrar_index(jugador_actual=None, mensaje_estado=""):
    if jugador_actual is None:
        botones = [
            {"texto": "INICIAR SESION", "color": LILA, "accion": "login"},
            {"texto": "CREAR CUENTA", "color": ROSA, "accion": "registro"},
            {"texto": "JUGAR COMO INVITADO", "color": MENTA, "accion": "invitado"},
            {"texto": "VER TOP 10", "color": AMARILLO, "accion": "top10"}
        ]
        titulo_panel = "BIENVENIDO A GATO KART"
    else:
        botones = [
            {"texto": "JUGAR CARRERA", "color": MENTA, "accion": "jugar"},
            {"texto": "VER TOP 10", "color": AMARILLO, "accion": "top10"},
            {"texto": "MI PERFIL (EDITAR)", "color": LILA, "accion": "perfil"},
            {"texto": "CERRAR SESION", "color": ROSA, "accion": "logout"}
        ]
        titulo_panel = f"HOLA, {jugador_actual['nombre'].upper()[:16]}"

    rectangulos = [pygame.Rect(525, 255 + i * 82, 335, 62) for i in range(len(botones))]

    while True:
        mouse = pygame.mouse.get_pos()

        dibujar_fondo()
        dibujar_decoraciones()
        dibujar_titulo()
        dibujar_panel(titulo_panel)
        dibujar_personaje()

        for i, boton in enumerate(botones):
            dibujar_boton(rectangulos[i], boton["texto"], boton["color"], mouse)

        if mensaje_estado:
            aviso = fuente_pequena.render(mensaje_estado, True, ROSA_OSCURO)
            pantalla.blit(aviso, aviso.get_rect(center=(692, 602)))

        pie = fuente_pequena.render("GATO KART | PIXEL CAT RACING", True, MARRON)
        pantalla.blit(pie, (20, 675))

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return "salir"
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                for i, rect in enumerate(rectangulos):
                    if rect.collidepoint(evento.pos):
                        return botones[i]["accion"]

        pygame.display.flip()
        reloj.tick(60)


def ejecutar_index():
    global pantalla
    jugador_actual = None
    mensaje_estado = ""

    while True:
        resultado = mostrar_index(jugador_actual, mensaje_estado)
        mensaje_estado = ""

        if resultado == "salir":
            break

        elif resultado == "login":
            estado, correo, contrasena = mostrar_login()
            if estado == "salir":
                break
            elif estado == "ingresar":
                usuario_bd = login_jugador(correo, contrasena)
                if usuario_bd:
                    jugador_actual = usuario_bd
                    mensaje_estado = "Se inicio sesion correctamente jochis!"
                else:
                    mensaje_estado = "Correo o contrasena incorrectos."

        elif resultado == "registro":
            estado, nombre, correo, contrasena = mostrar_registro()
            if estado == "salir":
                break
            elif estado == "validado":
                exito, res = registrar_jugador(nombre, correo, contrasena)
                if exito:
                    jugador_actual = {"id": res, "nombre": nombre, "correo": correo}
                    mensaje_estado = "Cuenta creada! Bienvenido!"
                else:
                    mensaje_estado = res

        elif resultado in ("invitado", "jugar"):
            from main_2 import ejecutar_juego
            ejecutar_juego(jugador_actual)
            pantalla = pygame.display.set_mode((ANCHO, ALTO))
            pygame.display.set_caption("GATO KART | Menu principal")

        elif resultado == "top10":
            res = mostrar_pantalla_top10()
            if res == "salir":
                break

        elif resultado == "perfil":
            res, jugador_actual = mostrar_pantalla_perfil(jugador_actual)
            if res == "salir":
                break
            elif res == "eliminado":
                mensaje_estado = "Cuenta eliminada de SQL Server."

        elif resultado == "logout":
            jugador_actual = None
            mensaje_estado = "Sesion cerrada."

    pygame.quit()


if __name__ == "__main__":
    ejecutar_index()