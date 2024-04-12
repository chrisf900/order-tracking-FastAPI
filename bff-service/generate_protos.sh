#!/bin/bash
set -e

echo "--- Iniciando generación de contratos gRPC ---"

# 1. Limpiar generación anterior para evitar archivos huérfanos
rm -rf generated/*

# 2. Actualizar dependencias (si usas buf.build/google/protobuf, etc.)
buf dep update

# 3. Generar stubs.
# Asegúrate de que en tu buf.gen.yaml la ruta de salida (out) sea "gen"
buf generate

# 4. El truco del __init__.py para que Python reconozca la carpeta como módulo
find generated -type d -exec touch {}/__init__.py \;

echo "✅ Stubs generados correctamente en la carpeta /generated"
