HONEY POT
Proyecto de final de grado CFGS Ciberseguridad
$--Dark$Trackers--$
Licencia: GPL-3.0 / Public License

---
🕵️‍♂️ Monitoreo de Actividades Maliciosas en la Dark Web a partir de Honeypots y Web Scraping
Este Trabajo de Fin de Grado (TFG) tiene como objetivo la detección, monitorización y análisis de ciberamenazas activas en la web superficial y la dark web, empleando técnicas de web scraping, honeypots personalizados y herramientas como Suricata. Se busca generar inteligencia en tiempo real sobre los vectores de ataque más comunes y patrones de comportamiento malicioso detectados tanto en la surface como en la dark web.

Estructura del proyecto
tfg-honeypots-darkweb/
├── src/
│   ├── honeypot_generator.py
│   ├── surface_scraper.py
│   ├── db_connector.py
│   └── report_generator.py
├── suricata/
│   ├── suricata.yaml
│   └── logs/
├── output/
│   └── informes/
├── sql/
│   └── esquema_base_datos.sql
├── installer.py
├── dependencies.
└── README.md

📦 Instalación y Uso
Requisitos
Sistema Linux (probado en Kali y derivados)
Python 3
Acceso root
Conexión a Internet

##🛠️ Tecnologías Utilizadas

🐍 Python 3

🐬 MariaDB

🧰 Suricata IDS

🕷️ BeautifulSoup, Requests, Tor (scraping de webs .onion)

🖥️ Apache2

🔁 Cron

🐧 Kali Linux / MINIX

🧅 TorWeb

🖊️ LibreOffice


⚠️ Aviso Legal
Este proyecto ha sido desarrollado con fines estrictamente educativos y de investigación dentro del marco de un Trabajo de Fin de Grado. No se autoriza ni se aprueba el uso de este software para fines maliciosos, delictivos o fuera del ámbito académico o profesional autorizado. El autor no se hace responsable del uso indebido por parte de terceros.

Instrucciones
```bash
git clone https://github.com/tuusuario/tfg-honeypots-darkweb.git
cd tfg-honeypots-darkweb
sudo python3 installer.py

Los informes generados se guardan automáticamente en: la propia carpeta de Informes

Cada informe incluye:

. IPs atacantes detectadas

. Rutas accedidas

. Alertas de Suricata

. Resumen de actividad maliciosa