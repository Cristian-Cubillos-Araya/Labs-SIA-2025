FROM python:3.9-slim

# Establecer directorio de trabajo
WORKDIR /app

# Copiar los archivos de requisitos primero para aprovechar la caché de Docker
COPY requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto de la aplicación
COPY . .

# Exponer el puerto que usa Flask
EXPOSE 5000

# Establecer variables de entorno para Flask
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Comando para ejecutar la aplicación
CMD ["flask", "run"]