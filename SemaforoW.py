import network
import socket
from machine import Pin
from time import sleep
from threading import Thread

# Configurar los LEDs del semáforo 1
red1 = Pin(15, Pin.OUT)
yellow1 = Pin(14, Pin.OUT)
green1 = Pin(13, Pin.OUT)

# Configurar los LEDs del semáforo 2
red2 = Pin(12, Pin.OUT)
yellow2 = Pin(11, Pin.OUT)
green2 = Pin(10, Pin.OUT)

# Funciones para cambiar el estado de los semáforos
def semaforo1_verde():
    green1.on()
    yellow1.off()
    red1.off()

def semaforo1_amarillo():
    green1.off()
    yellow1.on()
    red1.off()

def semaforo1_rojo():
    green1.off()
    yellow1.off()
    red1.on()

def semaforo2_verde():
    green2.on()
    yellow2.off()
    red2.off()

def semaforo2_amarillo():
    green2.off()
    yellow2.on()
    red2.off()

def semaforo2_rojo():
    green2.off()
    yellow2.off()
    red2.on()

# Conectar a Wi-Fi
ssid = "DLL-WiFi"  # Cambia esto por tu SSID
password = "Uwf0Lo1@_{.__;"  # Cambia esto por tu contraseña

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

# Esperar a que se conecte a la red Wi-Fi
while not wlan.isconnected():
    print("Conectando a la red Wi-Fi...")
    sleep(1)
print("Conectado a la red Wi-Fi con IP:", wlan.ifconfig()[0])

# Crear la página web que mostrará el estado de los semáforos
def generar_pagina_html():
    estado_semaforo_1 = "Verde" if green1.value() else "Amarillo" if yellow1.value() else "Rojo"
    estado_semaforo_2 = "Verde" if green2.value() else "Amarillo" if yellow2.value() else "Rojo"
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Control de Semáforos</title>
        <meta http-equiv="refresh" content="1">
        <style>
            h1 {{text-align: center;}}
            .semaforo {{display: inline-block; margin: 20px;}}
            .rojo {{ width: 50px; height: 50px; border-radius: 50%; display: block; margin: 10px auto;
                    background-color: {'#ff0000' if estado_semaforo_1 == 'Rojo' else '#555'}; }}
            .amarillo {{ width: 50px; height: 50px; border-radius: 50%; display: block; margin: 10px auto;
                         background-color: {'#ffff00' if estado_semaforo_1 == 'Amarillo' else '#555'}; }}
            .verde {{ width: 50px; height: 50px; border-radius: 50%; display: block; margin: 10px auto;
                      background-color: {'#00ff00' if estado_semaforo_1 == 'Verde' else '#555'}; }}
            .rojo2 {{ width: 50px; height: 50px; border-radius: 50%; display: block; margin: 10px auto;
                     background-color: {'#ff0000' if estado_semaforo_2 == 'Rojo' else '#555'}; }}
            .amarillo2 {{ width: 50px; height: 50px; border-radius: 50%; display: block; margin: 10px auto;
                          background-color: {'#ffff00' if estado_semaforo_2 == 'Amarillo' else '#555'}; }}
            .verde2 {{ width: 50px; height: 50px; border-radius: 50%; display: block; margin: 10px auto;
                       background-color: {'#00ff00' if estado_semaforo_2 == 'Verde' else '#555'}; }}
        </style>
    </head>
    <body>
        <h1>Estado de los Semaforos</h1>
        <div class="semaforo">
            <h2>Semaforo 1</h2>
            <span class="rojo"></span>
            <span class="amarillo"></span>
            <span class="verde"></span>
        </div>
        <div class="semaforo">
            <h2>Semaforo 2</h2>
            <span class="rojo2"></span>
            <span class="amarillo2"></span>
            <span class="verde2"></span>
        </div>
    </body>
    </html>
    """
    return html

# Servidor web para mostrar el estado de los semáforos
def iniciar_servidor_web():
    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
    s = socket.socket()
    s.bind(addr)
    s.listen(1)
    print('Servidor web iniciado en http://', addr)

    while True:
        cl, addr = s.accept()
        print('Cliente conectado desde', addr)
        request = cl.recv(1024)
        response = generar_pagina_html()
        cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
        cl.send(response)
        cl.close()

# Ciclo de semáforos
def ciclo_semaforos():
    while True:
        semaforo1_verde()
        semaforo2_rojo()
        sleep(10)

        semaforo1_amarillo()
        semaforo2_rojo()
        sleep(2)

        semaforo1_rojo()
        semaforo2_verde()
        sleep(10)

        semaforo1_rojo()
        semaforo2_amarillo()
        sleep(2)
        

# Iniciar servidor web y ciclo de semáforos
def main():
    # Iniciar el ciclo de semáforos en un hilo separado
    Thread(target=ciclo_semaforos).start()
    iniciar_servidor_web()
        
main()
