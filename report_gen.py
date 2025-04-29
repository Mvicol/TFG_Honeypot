#!/usr/bin/python3

import signal
import json
import sys
import subprocess
import os
import re

from docx import Document
import mysql.connector

# Conexion a MYSQL (Esencial para extraer la informacion)
conn = mysql.connector.connect(
    host='root',
    user='root',
    password='root',
    database='honey'
)
cursor = conn.cursor()
cursor.execute("SELECT nombre, email FROM usuarios")
resultados = cursor.fetchall()

# Crear documento
doc = Document()
doc.add_heading('Informe de Usuarios', 0)

# Insertar tabla
table = doc.add_table(rows=1, cols=2)
hdr_cells = table.rows[0].cells
hdr_cells[0].text = 'Nombre'
hdr_cells[1].text = 'Email'

for nombre, email in resultados:
    row_cells = table.add_row().cells
    row_cells[0].text = nombre
    row_cells[1].text = email

doc.save('informe.docx')
