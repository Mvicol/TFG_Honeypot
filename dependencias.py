#!/usr/bin/python3

import subprocess
import sys

def instalar_paquetes_apt():
    print("⚡ Instalando paquetes de sistema con APT...\n")
    paquetes_apt = ["python3-pip", "mariadb-server", "mariadb-client"]
    try:
        subprocess.run(["sudo", "apt", "update"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        subprocess.run(["sudo", "apt", "install", "-y"] + paquetes_apt, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    except subprocess.CalledProcessError:
        print("❌ Error al instalar paquetes APT.")
        sys.exit(1)

def instalar_paquetes_pip():
    print("🐍 Instalando paquetes de Python con PIP...\n")
    paquetes_pip = ["mysql-connector-python", "python-dotenv"]
    try:
        subprocess.run(["pip3", "install", "--break-system-packages"] + paquetes_pip, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    except subprocess.CalledProcessError:
        print("❌ Error al instalar paquetes PIP.")
        sys.exit(1)

def instalar_dependencias():
    instalar_paquetes_apt()
    instalar_paquetes_pip()
    print("✅ Todas las dependencias han sido instaladas correctamente.\n")

if __name__ == "__main__":
    instalar_dependencias()
