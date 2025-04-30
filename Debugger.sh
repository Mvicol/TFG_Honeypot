#!/bin/bash

# 🔥 Full uninstall of MariaDB and all its related packages and files

set -e

echo "🧨 Eliminando completamente MariaDB y todos sus rastros..."

# 1. Parar servicios si existen
sudo systemctl stop mariadb || true
sudo systemctl disable mariadb || true

# 2. Purga de paquetes relacionados con MariaDB
sudo apt purge --remove -y mariadb-server mariadb-client mariadb-common mariadb-backup mariadb-core-* libmariadb3 libmariadb-dev libmariadb-dev-compat mysql-common

# 3. Autoremove de dependencias
sudo apt autoremove --purge -y

# 4. Eliminar directorios de configuración y datos
sudo rm -rf /etc/mysql
sudo rm -rf /var/lib/mysql
sudo rm -rf /var/log/mysql
sudo rm -rf /etc/my.cnf /etc/my.cnf.d
sudo rm -rf /var/lib/mysql-files /var/lib/mysql-keyring

# 5. Limpiar registros fallidos de systemd
sudo systemctl daemon-reexec
sudo systemctl daemon-reload
sudo systemctl reset-failed

echo "\n✅ MariaDB y todos sus componentes han sido eliminados completamente."
echo "💡 Ahora puedes reinstalar desde cero con: sudo apt install mariadb-server"
