# SpaceMax Defender - Juego Espacial en Python con Docker

SpaceMax Defender es un juego espacial desarrollado en Python utilizando la biblioteca pygame. El objetivo del jugador es evitar la colisión
con meteoritos y sobrevivir el mayor tiempo posible mientras se acumulan puntos.Este proyecto no solo involucra el diseño del juego
con gráficos y sonido, sino que también demuestra cómo contenerizar la aplicación con Docker para garantizar su portabilidad.

## Estructura del Proyecto

El proyecto está organizado de la siguiente forma:

8_Juego_espacial/ 
├── assets/ 
│   ├── fondo.jpg 
│   ├── nave.png
│   ├── meteorito.png 
│   └── sonido_disparo.wav 
├── main.py 
├── requirements.txt 
├── Dockerfile 
├── run_game.sh 
└── README.md

## Dockerización del Juego

Se utilizó una imagen base ligera python:3.12-slim en el Dockerfile. El flujo general consiste en copiar todos los archivos del juego
 al contenedor, instalar las dependencias (pygame), establecer las variables de entorno necesarias para el sonido y la visualización
 (SDL_AUDIODRIVER=alsa, DISPLAY=:0), y ejecutar main.py al iniciar el contenedor.

## Pasos para Ejecutar el Juego

1. Dar permisos de ejecución al script:

chmod +x correr_juego.sh

2. Ejecutar el script para construir y correr el juego:

./correr_juego.sh

Este script realizará los siguientes pasos automáticamente: construye la imagen de Docker con el nombre spacemax-defender, habilita el acceso gráfico desde el host (xhost +local:docker), y corre el contenedor con variables de entorno para gráficos y sonido, ejecutando el juego.

## Configuración del Sonido

El sonido se configuró utilizando ALSA (SDL_AUDIODRIVER=alsa), lo cual es compatible con WSLg (Windows 11) y la mayoría de distribuciones Linux. Si el sonido no funciona, verifica que ALSA esté disponible en tu host y que el contenedor tenga acceso a /dev/snd. Puedes añadir --device /dev/snd al comando docker run.

## Dependencias

pygame==2.6.1

Estas dependencias están especificadas en el archivo requirements.txt.
