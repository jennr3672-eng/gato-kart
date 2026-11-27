-- TABLAS
-- ==========================================
CREATE TABLE IF NOT EXISTS jugadores (
    id_jugador SERIAL PRIMARY KEY,
    nombre VARCHAR(60) NOT NULL,
    correo VARCHAR(80) NOT NULL UNIQUE,
    password_hash VARCHAR(100) NOT NULL,
    nivel_avance INTEGER DEFAULT 1, -- 1: Facil, 2: Medio, 3: Dificil
    score_maximo INTEGER DEFAULT 0,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS historial_scores (
    id_historial SERIAL PRIMARY KEY,
    id_jugador INTEGER NOT NULL REFERENCES jugadores(id_jugador) ON DELETE CASCADE,
    nivel_jugado INTEGER NOT NULL,
    score_obtenido INTEGER NOT NULL,
    fecha_partida TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS auditoria_jugadores (
    id_auditoria SERIAL PRIMARY KEY,
    id_jugador INTEGER,
    accion VARCHAR(100),
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ==========================================
-- TRIGGERS
-- ==========================================
-- Trigger 1: al guardar una partida, actualiza el record y el nivel del jugador
CREATE OR REPLACE FUNCTION fn_actualizar_record_jugador()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE jugadores
    SET
        score_maximo = GREATEST(score_maximo, NEW.score_obtenido),
        nivel_avance = GREATEST(nivel_avance, NEW.nivel_jugado)
    WHERE id_jugador = NEW.id_jugador;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_actualizar_record_jugador ON historial_scores;
CREATE TRIGGER trg_actualizar_record_jugador
AFTER INSERT ON historial_scores
FOR EACH ROW
EXECUTE FUNCTION fn_actualizar_record_jugador();

-- Trigger 2: auditoria cuando alguien crea cuenta o cambia su nombre/contrasena
CREATE OR REPLACE FUNCTION fn_auditoria_registro_update()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        INSERT INTO auditoria_jugadores (id_jugador, accion)
        VALUES (NEW.id_jugador, 'Nuevo jugador registrado: ' || NEW.nombre);
    ELSIF TG_OP = 'UPDATE' THEN
        INSERT INTO auditoria_jugadores (id_jugador, accion)
        VALUES (NEW.id_jugador, 'Perfil actualizado: ' || NEW.nombre);
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_auditoria_registro_update ON jugadores;
CREATE TRIGGER trg_auditoria_registro_update
AFTER INSERT OR UPDATE OF nombre, password_hash ON jugadores
FOR EACH ROW
EXECUTE FUNCTION fn_auditoria_registro_update();

-- ==========================================
-- VISTA TOP 10
-- ==========================================
CREATE OR REPLACE VIEW vw_top10_jugadores AS
SELECT
    nombre AS usuario,
    CASE nivel_avance
        WHEN 1 THEN 'Facil'
        WHEN 2 THEN 'Medio'
        WHEN 3 THEN 'Dificil'
        ELSE 'Facil'
    END AS nivel,
    score_maximo
FROM jugadores
ORDER BY score_maximo DESC, nivel_avance DESC
LIMIT 10;

-- ==========================================
-- FUNCIONES (CRUD que usa el juego)
-- ==========================================
CREATE OR REPLACE FUNCTION fn_registrar_jugador(p_nombre VARCHAR, p_correo VARCHAR, p_password VARCHAR)
RETURNS INT AS $$
DECLARE
    v_id INT;
BEGIN
    IF EXISTS (SELECT 1 FROM jugadores WHERE correo = p_correo) THEN
        RAISE EXCEPTION 'El correo ya esta registrado.';
    END IF;

    INSERT INTO jugadores (nombre, correo, password_hash)
    VALUES (p_nombre, p_correo, p_password)
    RETURNING id_jugador INTO v_id;

    RETURN v_id;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION fn_login_jugador(p_correo VARCHAR, p_password VARCHAR)
RETURNS TABLE (id_jugador INT, nombre VARCHAR, correo VARCHAR, nivel_avance INT, score_maximo INT) AS $$
    SELECT j.id_jugador, j.nombre, j.correo, j.nivel_avance, j.score_maximo
    FROM jugadores j
    WHERE j.correo = p_correo AND j.password_hash = p_password;
$$ LANGUAGE sql;

CREATE OR REPLACE FUNCTION fn_guardar_partida(p_id INT, p_nivel INT, p_score INT)
RETURNS VOID AS $$
    INSERT INTO historial_scores (id_jugador, nivel_jugado, score_obtenido)
    VALUES (p_id, p_nivel, p_score);
$$ LANGUAGE sql;

CREATE OR REPLACE FUNCTION fn_actualizar_jugador(p_id INT, p_nombre VARCHAR, p_password VARCHAR)
RETURNS VOID AS $$
    UPDATE jugadores
    SET nombre = p_nombre, password_hash = p_password
    WHERE id_jugador = p_id;
$$ LANGUAGE sql;

CREATE OR REPLACE FUNCTION fn_eliminar_jugador(p_id INT)
RETURNS VOID AS $$
    DELETE FROM jugadores WHERE id_jugador = p_id;
$$ LANGUAGE sql;
