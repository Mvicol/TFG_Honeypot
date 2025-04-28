import subprocess
import sys
import shutil

def instalar_paquetes_apt():
    print("⚡ Instalando paquetes de sistema con APT...\n")
    paquetes_apt = ["python3-pip", "mariadb-server", "mariadb-client"]
    paquetes_a_instalar = []

    for paquete in paquetes_apt:
        result = subprocess.run(["dpkg", "-s", paquete], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if result.returncode != 0:
            paquetes_a_instalar.append(paquete)
        else:
            print(f"✅ {paquete} ya está instalado, saltando...")

    if paquetes_a_instalar:
        try:
            subprocess.run(["sudo", "apt", "update"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
            subprocess.run(["sudo", "apt", "install", "-y"] + paquetes_a_instalar, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        except subprocess.CalledProcessError:
            print("❌ Error al instalar paquetes APT.")
            sys.exit(1)
    else:
        print("✅ Todos los paquetes de APT ya están instalados.\n")

def instalar_paquetes_pip():
    print("🐍 Instalando paquetes de Python con PIP...\n")
    paquetes_pip = ["mysql-connector-python", "python-dotenv"]
    paquetes_a_instalar = []

    for paquete in paquetes_pip:
        result = subprocess.run(["pip3", "show", paquete], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if result.returncode != 0:
            paquetes_a_instalar.append(paquete)
        else:
            print(f"✅ {paquete} ya está instalado, saltando...")

    if paquetes_a_instalar:
        try:
            subprocess.run(["pip3", "install", "--break-system-packages"] + paquetes_a_instalar, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        except subprocess.CalledProcessError:
            print("❌ Error al instalar paquetes PIP.")
            sys.exit(1)
    else:
        print("✅ Todos los paquetes de PIP ya están instalados.\n")

def instalar_dependencias():
    instalar_paquetes_apt()
    instalar_paquetes_pip()
    print("✅ Todas las dependencias han sido instaladas correctamente.\n")

if __name__ == "__main__":
    instalar_dependencias()
