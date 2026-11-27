# Gato Kart

## Cómo ejecutarlo

1. Instalar las dependencias:
   `pip install -r requirements.txt`

2. Crear un archivo `.env` en la misma carpeta que `index.py` con la conexión a la base de datos (Neon, PostgreSQL):
   `DATABASE_URL=postgresql://usuario:contraseña@host/neondb?sslmode=require`
  
3. Ejecutar:
   `python index.py`

También se entrega una versión para Windows (`GatoKart.zip`): descomprimir y abrir `GatoKart.exe`. Requiere internet.
