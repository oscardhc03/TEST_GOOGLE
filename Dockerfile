# Usa una imagen base de Python
FROM python:3.8-slim

# Establece el directorio de trabajo en el contenedor
WORKDIR /app

# Copia el código fuente al contenedor
COPY . /app

# Instala las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Expone el puerto en el que se ejecutará la aplicación
EXPOSE 8080

# Comando para ejecutar la aplicación Flask
CMD ["python", "Server.py"]
