import os
import sys
import hashlib
import psycopg2
from dotenv import load_dotenv

# Carpeta donde vive el juego (o el .exe, si esta empaquetado)
if getattr(sys, "frozen", False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

load_dotenv(os.path.join(BASE_DIR, ".env"))
DATABASE_URL = os.getenv("DATABASE_URL")


def hashear(password):
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def obtener_conexion():
    try:
        return psycopg2.connect(DATABASE_URL)
    except Exception as e:
        print(f"Error de conexion a Neon: {e}")
        return None


def registrar_jugador(nombre, correo, password):
    conexion = obtener_conexion()
    if not conexion:
        return False, "No se pudo conectar a la base de datos."
    cursor = conexion.cursor()
    try:
        cursor.execute("SELECT fn_registrar_jugador(%s, %s, %s)",
                       (nombre, correo, hashear(password)))
        fila = cursor.fetchone()
        conexion.commit()
        return True, int(fila[0]) if fila else None
    except Exception as e:
        conexion.rollback()
        print(f"Error real al registrar: {e}")
        return False, "El correo ya existe o hubo un error."
    finally:
        cursor.close()
        conexion.close()


def login_jugador(correo, password):
    conexion = obtener_conexion()
    if not conexion:
        return None
    cursor = conexion.cursor()
    try:
        cursor.execute("SELECT * FROM fn_login_jugador(%s, %s)",
                       (correo, hashear(password)))
        fila = cursor.fetchone()
        if fila:
            return {
                "id": fila[0],
                "nombre": fila[1],
                "correo": fila[2],
                "nivel": fila[3],
                "score": fila[4]
            }
        return None
    except Exception as e:
        print(f"Error al iniciar sesion: {e}")
        return None
    finally:
        cursor.close()
        conexion.close()


def guardar_partida(id_jugador, nivel_texto, score):
    if id_jugador is None:
        return  # Invitado: no se guarda
    mapa_niveles = {"Facil": 1, "Medio": 2, "Dificil": 3}
    nivel_num = mapa_niveles.get(nivel_texto, 1)

    conexion = obtener_conexion()
    if not conexion:
        return
    cursor = conexion.cursor()
    try:
        cursor.execute("SELECT fn_guardar_partida(%s, %s, %s)",
                       (id_jugador, nivel_num, score))
        conexion.commit()
    except Exception as e:
        conexion.rollback()
        print(f"Error al guardar partida: {e}")
    finally:
        cursor.close()
        conexion.close()


def obtener_top10():
    conexion = obtener_conexion()
    if not conexion:
        return []
    cursor = conexion.cursor()
    try:
        cursor.execute("SELECT usuario, nivel, score_maximo FROM vw_top10_jugadores")
        return cursor.fetchall()
    except Exception as e:
        print(f"Error al leer Top 10: {e}")
        return []
    finally:
        cursor.close()
        conexion.close()


def actualizar_jugador(id_jugador, nuevo_nombre, nueva_password):
    conexion = obtener_conexion()
    if not conexion:
        return False
    cursor = conexion.cursor()
    try:
        cursor.execute("SELECT fn_actualizar_jugador(%s, %s, %s)",
                       (id_jugador, nuevo_nombre, hashear(nueva_password)))
        conexion.commit()
        return True
    except Exception as e:
        conexion.rollback()
        print(f"Error al actualizar: {e}")
        return False
    finally:
        cursor.close()
        conexion.close()


def eliminar_jugador(id_jugador):
    conexion = obtener_conexion()
    if not conexion:
        return False
    cursor = conexion.cursor()
    try:
        cursor.execute("SELECT fn_eliminar_jugador(%s)", (id_jugador,))
        conexion.commit()
        return True
    except Exception as e:
        conexion.rollback()
        print(f"Error al eliminar: {e}")
        return False
    finally:
        cursor.close()
        conexion.close()