#!/bin/bash
set -e

echo "Actualizando dependencias de buf..."
rm -rf generated/*
buf dep update

echo "Generando stubs con buf..."
buf generate --include-imports protos

find generated -type d -exec touch {}/__init__.py \;

echo "Stubs generados correctamente."
