#!/bin/bash
set -e

echo "Actualizando dependencias de buf..."
buf dep update

echo "Generando stubs con buf..."
buf generate --include-imports protos

# Asegura que todos los directorios tengan __init__.py
find generated -type d -exec touch {}/__init__.py \;

echo "Stubs generados correctamente."
