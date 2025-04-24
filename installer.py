#!/usr/bin/python3

import signal
import json
import sys
import subprocess
import os
import re

def checkPerms():
    if os.geteuid() != 0:
        print("Este script debe ejecutarse como root. Usa 'sudo python3 installer.py'.")
        exit(1)

def banner():
    print("""
:::    :::  ::::::::  ::::    ::: :::::::::: :::   ::: :::::::::   :::::::: :::::::::::
:+:    :+: :+:    :+: :+:+:   :+: :+:        :+:   :+: :+:    :+: :+:    :+:    :+:  
+:+    +:+ +:+    +:+ :+:+:+  +:+ +:+         +:+ +:+  +:+    +:+ +:+    +:+    +:+
+#++:++#++ +#+    +:+ +#+ +:+ +#+ +#++:++#     +#++:   +#++:++#+  +#+    +:+    +#+
+#+    +#+ +#+    +#+ +#+  +#+#+# +#+           +#+    +#+        +#+    +#+    +#+
#+#    #+# #+#    #+# #+#   #+#+# #+#           #+#    #+#        #+#    #+#    #+#                 
###    ###  ########  ###    #### ##########    ###    ###         ########     ###     

                      ~~~~~~~~  by Mark and Miquel ~~~~~~~~
    """)

# Mostrar el banner antes de cualquier otra acción
subprocess.run("clear", shell=True)
banner()
checkPerms()

def dependencias():
    """Instala el conector de MySQL para Python si no está instalado"""
    print("⚠️ mysql-connector-python no está instalado. Instalando...\n")
    subprocess.run("sudo pip3 install --break-system-packages mysql-connector-python", shell=True, check=True)
    subprocess.run("sudo apt install -y jq > /dev/null 2>&1", shell=True, check=True)
    subprocess.run("sudo python3 dependencias.py > /dev/null 2>&1", shell=True, check=True)
    
    import mysql.connector  # Intentar importar nuevamente
    print("✅ mysql-connector-python instalado correctamente.\n")
    

# Instalar dependencias después del banner
dependencias()

import shutil
import time
import mysql.connector

def actualizar_sistema():
    print("Actualizando repositorios... \n")
    subprocess.run("sudo apt update > /dev/null 2>&1", shell=True, check=True)
    print("Paquetes actualizados correctamente 🟢 \n")

def instalar_apache():
    print("Instalando Apache2... \n")
    subprocess.run("sudo apt install -y apache2 > /dev/null 2>&1", shell=True, check=True)
    print("Apache2 instalado correctamente 🟢 \n")

def configurar_apache():
    print("Configurando Apache para aceptar conexiones en todas las interfaces... \n")
    with open("/etc/apache2/ports.conf", "w") as f:
        f.write("Listen 80\n")
    with open("/etc/apache2/sites-available/000-default.conf", "w") as f:
        f.write("""
<VirtualHost *:80>
    DocumentRoot /var/www/html
    <Directory /var/www/html>
        Options Indexes FollowSymLinks
        AllowOverride None
        Require all granted
    </Directory>
</VirtualHost>
        """)
    print("Apache configurado correctamente 🟢 \n")

def iniciar_habilitar_apache():
    print("Habilitando y arrancando Apache2... \n")
    subprocess.run("sudo systemctl enable apache2 > /dev/null 2>&1", shell=True, check=True)
    subprocess.run("sudo systemctl restart apache2 > /dev/null 2>&1", shell=True, check=True)
    print("Apache2 habilitado y en ejecución 🟢 \n")

def ejecutar_scrapper():
    print("Ejecutando scrapper para obtener HTML y CSS... \n")
    subprocess.run("sudo python3 normal_scrapper.py", shell=True, check=True)
    
    html_origen = os.path.join(os.getcwd(), "extracted_html.html")
    css_origen = os.path.join(os.getcwd(), "styles.css")
    html_destino = "/var/www/html/index.html"
    css_destino = "/var/www/html/styles.css"
    
    if os.path.exists(html_origen):
        shutil.copy(html_origen, html_destino)
        print("Archivo index.html reemplazado con el scrappeado 🟢 \n")
        os.remove(html_origen)
    
    if os.path.exists(css_origen):
        shutil.copy(css_origen, css_destino)
        print("Archivo CSS reemplazado con el scrappeado 🟢 \n")
        os.remove(css_origen)

def instalar_suricata():
    print("Instalando Suricata... \n")
    subprocess.run("sudo apt install -y suricata > /dev/null 2>&1", shell=True, check=True)
    print("Suricata instalado correctamente 🟢 \n")

def configurar_suricata():
    config_path = "/etc/suricata/suricata.yaml"
    try:
        # Leer el archivo de configuración
        with open(config_path, "r") as file:
            config = file.readlines()
        
        tiene_pcap_lo = any(re.search(r"^\s*- interface: lo", line) for line in config)
        tiene_af_eth0 = any(re.search(r"^\s*- interface: eth0", line) for line in config)
        
        if tiene_pcap_lo and tiene_af_eth0:
            print("✅ Suricata ya está configurado correctamente para 'pcap: lo' y 'af-packet: eth0'.")
            return
        
        print("🛠️ Modificando configuración de Suricata...")
        
        # Modificar pcap para incluir lo si no está
        for i, line in enumerate(config):
            if "pcap:" in line:
                insert_index = i + 1
                if not tiene_pcap_lo:
                    config.insert(insert_index, "  - interface: lo\n")
                break
        
        # Modificar af-packet para incluir eth0 si no está
        for i, line in enumerate(config):
            if "af-packet:" in line:
                insert_index = i + 1
                if not tiene_af_eth0:
                    config.insert(insert_index, "  - interface: eth0\n")
                break
        
        # Escribir cambios en el archivo
        with open(config_path, "w") as file:
            file.writelines(config)
        
        print("✅ Configuración de Suricata actualizada.")
        
        # Reiniciar Suricata para aplicar cambios
        print("🔄 Reiniciando Suricata...")
        subprocess.run("sudo systemctl restart suricata", shell=True, check=True)
        print("✅ Suricata reiniciado correctamente.")
        
    except Exception as e:
        print(f"❌ Error al modificar la configuración de Suricata: {e}")




def iniciar_habilitar_suricata():
    print("Habilitando y arrancando Suricata... \n")

    configurar_suricata()

    subprocess.run("sudo systemctl start suricata > /dev/null 2>&1", shell=True, check=True)
    subprocess.run("sudo chmod 644 /var/log/suricata/eve.json", shell=True, check=True)
    subprocess.run("sudo chown root:kali /var/log/suricata/eve.json", shell=True, check=True)
    subprocess.run("sudo systemctl restart suricata > /dev/null 2>&1", shell=True, check=True)
    subprocess.run("sudo systemctl disable suricata && sudo systemctl start suricata > /dev/null 2>&1", shell=True, check=True)
    print("Suricata habilitado y en ejecución 🟢 \n")



def instalar_mariadb():
    """Instala MariaDB y lo configura para iniciar automáticamente con usuario root y contraseña."""
    print("⚙️ Instalando MariaDB...\n")

    try:
        # Instalar MariaDB Server
        subprocess.run("sudo apt install -y mariadb-server > /dev/null 2>&1", shell=True, check=True)
        print("✅ MariaDB instalado correctamente.\n")

        # Iniciar y habilitar el servicio
        subprocess.run("sudo systemctl enable mariadb > /dev/null 2>&1", shell=True, check=True)
        subprocess.run("sudo systemctl start mariadb > /dev/null 2>&1", shell=True, check=True)
        print("🚀 MariaDB iniciado y habilitado en el arranque.\n")

        # Comprobar si el usuario root usa 'unix_socket'
        print("🔍 Comprobando método de autenticación de root...\n")
        check_auth_plugin_cmd = """
        sudo mysql -N -e "SELECT plugin FROM mysql.user WHERE User='root' AND Host='localhost';"
        """
        auth_plugin = subprocess.run(check_auth_plugin_cmd, shell=True, capture_output=True, text=True).stdout.strip()

        if auth_plugin == "unix_socket":
            print("⚠️  Root usa 'unix_socket'. Cambiando a 'mysql_native_password' con contraseña 'root'...\n")
            change_auth_cmd = """
            sudo mysql -e "
            ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'root';
            FLUSH PRIVILEGES;
            "
            """
            subprocess.run(change_auth_cmd, shell=True, check=True)
            print("✅ Autenticación cambiada a 'mysql_native_password' con contraseña 'root'.\n")
        else:
            print("🟢 Root ya usa 'mysql_native_password'. No se requieren cambios.\n")

    except subprocess.CalledProcessError as e:
        print(f"❌ Error durante la instalación de MariaDB: {e}")

def configurar_base_datos():
    """Configura la base de datos usando usuario y contraseña."""
    print("⚡ Configurando base de datos en MariaDB... \n")
    try:
        # Conectar con usuario root y contraseña
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            auth_plugin='mysql_native_password'  # Asegurar autenticación correcta
        )
        cursor = conexion.cursor()
        cursor.execute("DROP DATABASE IF EXISTS honey;")
        cursor.execute("CREATE DATABASE IF NOT EXISTS honey;")
        cursor.execute("USE honey;")
        cursor.execute("DROP TABLE IF EXISTS logs_ataques")
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS logs_ataques (
            id INT AUTO_INCREMENT PRIMARY KEY,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            event_type VARCHAR(50) DEFAULT 'unknown',
            ip_origen VARCHAR(45) DEFAULT 'unknown',
            puerto_origen INT DEFAULT 0,
            ip_destino VARCHAR(45) DEFAULT 'unknown',
            puerto_destino INT DEFAULT 0,
            protocolo VARCHAR(10) DEFAULT 'unknown',
            alerta TEXT DEFAULT 'unknown',
            payload TEXT DEFAULT 'unknown',
            user_agent VARCHAR(255) DEFAULT 'unknown',
            hostname VARCHAR(255) DEFAULT 'unknown'
        );
        """)
        print("🟢 Base de datos 'honey' y tabla 'logs_ataques' configuradas correctamente.\n")
        cursor.close()
        conexion.close()
    except mysql.connector.Error as err:
        print(f"❌ Error al configurar la base de datos: {err}")


def insertar_evento_en_db(cursor, conexion, evento):
    try:
        dest_ip = evento.get("dest_ip", "")
        
        # Solo insertar eventos relacionados con el honeypot

        event_type = evento.get("event_type", "unknown")
        src_ip = evento.get("src_ip", "unknown")
        src_port = evento.get("src_port", 0)
        dest_port = evento.get("dest_port", 0)
        proto = evento.get("proto", "unknown")
        alerta = "unknown"
        payload = "unknown"
        user_agent = "unknown"
        hostname = "unknown"

        if event_type == "http":
            http = evento.get("http", {})
            user_agent = http.get("http_user_agent", "unknown")
            hostname = http.get("hostname", "unknown")
            payload = http.get("url", "unknown")

        query = """
        INSERT INTO logs_ataques (timestamp, event_type, ip_origen, puerto_origen, ip_destino, puerto_destino, 
                                  protocolo, alerta, payload, user_agent, hostname) 
        VALUES (NOW(), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (
            event_type,
            src_ip,
            src_port,
            dest_ip,
            dest_port,
            proto,
            alerta,
            payload,
            user_agent,
            hostname
        ))
        conexion.commit()
        print(f"🟢 Evento de tipo '{event_type}' insertado en la base de datos.")
    except Exception as e:
        print(f"❌ Error al insertar evento: {e}")


def monitorear_suricata():
    print("📡 Monitoreando eventos de Suricata...\n")
    
    log_path = "/var/log/suricata/eve.json"

    try:
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="honey"
        )
        cursor = conexion.cursor()

        if not os.path.exists(log_path):
            print(f"❌ El archivo de logs {log_path} no existe.")
            return

        with open(log_path, "r") as log_file:
            log_file.seek(0, 2)  # Ir al final del archivo
            while True:
                linea = log_file.readline()
                if not linea:
                    time.sleep(1)
                    continue
                
                try:
                    evento = json.loads(linea)
                    # Filtrar solo eventos de tipo alert, http o dns
                    if evento.get("event_type") in ["alert", "http", "dns"]:
                        insertar_evento_en_db(cursor, conexion, evento)
                except json.JSONDecodeError:
                    print("❌ Error al decodificar JSON")
                except Exception as e:
                    print(f"❌ Error inesperado: {e}")

    except mysql.connector.Error as err:
        print(f"❌ Error en la base de datos: {err}")

def parar_suricata():
    """Detiene Suricata de manera segura."""
    print("🛑 Deteniendo Suricata...")
    subprocess.run(["sudo", "systemctl", "stop", "suricata"], check=True)
    print("✅ Suricata detenido correctamente.")

def manejar_salida(signum, frame):
    """Maneja la señal SIGINT (Ctrl+C) para salir correctamente."""
    print("\n🔴 Señal de interrupción recibida. Deteniendo el script...")
    parar_suricata()
    sys.exit(0)

def reiniciar_eve_json():
    """Reinicia el archivo eve.json para eliminar eventos anteriores."""
    log_path = "/var/log/suricata/eve.json"
    try:
        if os.path.exists(log_path):
            with open(log_path, "w") as f:
                f.write("")  # Escribir una cadena vacía
            print(f"🟢 Archivo {log_path} reiniciado correctamente.")
        else:
            print(f"⚠️ El archivo {log_path} no existe. No se requiere reinicio.")
    except Exception as e:
        print(f"❌ Error al reiniciar {log_path}: {e}")


# Registrar el manejador de la señal SIGINT
signal.signal(signal.SIGINT, manejar_salida)


def main():
    subprocess.run("clear", shell=True)
    banner()
    actualizar_sistema()
    time.sleep(2)
    subprocess.run("clear", shell=True)
    banner()
    print("-------INSTALACION DE TOOLS NECESARIAS------- \n")
    #instalar_apache()
    configurar_apache()
    iniciar_habilitar_apache()
    #instalar_suricata()
    iniciar_habilitar_suricata()
    reiniciar_eve_json()
    #instalar_mariadb()
    configurar_base_datos()
    time.sleep(2)
    print("-------URL PARA COMENZAR A DESPLEGAR EL HONEYPOT------- \n")
    ejecutar_scrapper()
    print("\033[1;32m" + "\n" + "="*72)
    print("--------🚀🟢HONEYPOT DESPLEGADO Y CONFIGURADO CORRECTAMENTE 🟢🚀--------")
    print("="*72 + "\033[0m\n\n\n")
    print("\033[1;32m" + "\n" + "="*72)
    print("--------🐿️🟢SURICATA VIGILANDO HONEYPOT 🟢🐿️--------")
    print("="*72 + "\033[0m\n")
    monitorear_suricata()
   

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
    finally:
        # Asegurarse de que Suricata se detenga incluso si hay un error
        parar_suricata()
