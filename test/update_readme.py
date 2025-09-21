#!/usr/bin/env python3
"""
Script para actualizar el README principal con una lista de todos los archivos .md
"""

import os
import glob
from datetime import datetime
import re

def get_md_files():
    """Obtener todos los archivos .md excluyendo el README principal"""
    md_files = glob.glob("*.md")
    # Excluir el README principal y el script de actualización
    exclude_files = ["README.md", "README-mejoras-hogar.md", "update_readme.py"]
    return [f for f in md_files if f not in exclude_files]

def get_file_info(filename):
    """Obtener información del archivo incluyendo fecha de modificación"""
    try:
        stat = os.stat(filename)
        mod_time = datetime.fromtimestamp(stat.st_mtime)
        return {
            'filename': filename,
            'modified_date': mod_time.strftime('%Y-%m-%d'),
            'size': stat.st_size
        }
    except:
        return {
            'filename': filename,
            'modified_date': 'Unknown',
            'size': 0
        }

def generate_md_list():
    """Generar la lista de archivos .md en formato markdown"""
    files = get_md_files()
    file_infos = [get_file_info(f) for f in files]

    # Ordenar por fecha de modificación (más reciente primero)
    file_infos.sort(key=lambda x: x['modified_date'], reverse=True)

    md_list = "## Archivos Markdown\n\n"
    md_list += "| Archivo | Última Modificación | Tamaño |\n"
    md_list += "|---------|---------------------|--------|\n"

    for info in file_infos:
        size_kb = info['size'] / 1024
        md_list += f"| [{info['filename']}]({info['filename']}) | {info['modified_date']} | {size_kb:.1f} KB |\n"

    return md_list

def update_main_readme():
    """Actualizar el README principal con la lista de archivos"""
    readme_path = "README-mejoras-hogar.md"

    if not os.path.exists(readme_path):
        print(f"ERROR: No se encuentra {readme_path}")
        return False

    # Leer el README actual
    with open(readme_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Eliminar la sección anterior si existe
    content = re.sub(r'## Archivos Markdown.*?(?=## |$)', '', content, flags=re.DOTALL)

    # Generar nueva lista
    md_list = generate_md_list()

    # Insertar la nueva lista antes de la última sección
    sections = content.split('## ')
    if len(sections) > 1:
        # Insertar después de la primera sección
        sections.insert(1, md_list + '\n\n## ')
        content = '## '.join(sections)
    else:
        content += '\n\n' + md_list

    # Escribir el README actualizado
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"README actualizado con {len(get_md_files())} archivos .md")
    return True

if __name__ == "__main__":
    update_main_readme()