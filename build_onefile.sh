#!/bin/bash
set -e

# Caminho para o diretório do projeto
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_DIR"

echo "=== Ativando ambiente virtual ==="
source ./venv_linux/bin/activate

echo "=== Iniciando compilação com PyInstaller ==="
# Limpar compilações antigas
rm -rf build dist MaiaNote.spec

# Executar PyInstaller
pyinstaller --onefile --windowed \
    --name MaiaNote \
    --hidden-import PIL._tkinter_finder \
    --add-data "icones:icones" \
    --add-data "venv_linux/lib/python3.13/site-packages/customtkinter:customtkinter" \
    main.py

echo "=== Compilação concluída com sucesso! ==="
echo "O executável independente foi gerado em: dist/MaiaNote"
