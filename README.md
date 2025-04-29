# HONEY POT

## Proyecto de final de grado CFGS Ciberseguridad

### `$--Dark$Trackers--$`

> Licencia: GPL-3.0 / Public License

---

### 📌 Descripción (pendiente de completar)
Este proyecto tiene como objetivo el monitoreo de actividades maliciosas en la dark web y la web superficial mediante honeypots y técnicas de web scraping. [**Descripción detallada en desarrollo.**]

---

### 📂 Estructura del proyecto

- `normal_scrapper.py`: Script principal para copiar el contenido HTML y CSS de una web legítima y convertirlo en un honeypot.
- `onion_scrapper.py`: Script en desarrollo para clonar páginas .onion (dark web).
- `suricata/`: Configuración y reglas personalizadas de Suricata para detección de tráfico malicioso.
- `output/`: Directorio donde se almacenan las copias clonadas de las webs, organizadas por dominio.
- `logs/`: Registros de eventos generados por los honeypots y herramientas IDS/IPS.

---

### ⚙️ Tecnologías utilizadas

- Python 3.13
- Suricata
- MariaDB
- Apache2
- Kali Linux
- HTML/CSS
- Web scraping con `requests`, `BeautifulSoup` y `urllib3`

---

### 🚀 Cómo ejecutar

1. Clonar este repositorio en tu entorno de pruebas.
2. Configurar Suricata y MariaDB según el manual de instalación incluido.
3. Ejecutar el scrapper con permisos de administrador:

```bash
sudo python3 normal_scrapper.py
