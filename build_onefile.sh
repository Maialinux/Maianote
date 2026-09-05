#!/bin/bash
set -e

# Caminho para o diretório do projeto
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_DIR"

VENV="$PROJECT_DIR/.venv_linux"
PY_VER="$("$VENV/bin/python" -c 'import sys; print(f"python{sys.version_info.major}.{sys.version_info.minor}")')"
CTK_DIR="$VENV/lib/$PY_VER/site-packages/customtkinter"

echo "=== Ativando ambiente virtual ==="
source "$VENV/bin/activate"
echo "    $PY_VER | customtkinter em: $CTK_DIR"

echo "=== Iniciando compilação com PyInstaller ==="
# Limpar compilações antigas
rm -rf build dist MaiaNote.spec

# Executar PyInstaller
pyinstaller --onefile --windowed \
    --name maianote \
    --hidden-import PIL._tkinter_finder \
    --add-data "icones:icones" \
    --add-data "$CTK_DIR:customtkinter" \
    main.py

echo "=== Compilação concluída com sucesso! ==="
echo "O executável independente foi gerado em: dist/maianote"
