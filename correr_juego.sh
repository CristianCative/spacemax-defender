#!/bin/bash

# Construir la imagen
docker build -t spacemax-defender .

# Permitir a Docker usar el servidor X para mostrar la ventana
xhost +local:docker

# Ejecutar el contenedor con acceso a la interfaz gráfica
docker run -it --rm \
  -e DISPLAY=$DISPLAY \
  -v /tmp/.X11-unix:/tmp/.X11-unix \
  spacemax-defender
