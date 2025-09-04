#!/bin/bash

# Script básico para ejecutar pruebas
# Uso: ./run_tests.sh [opciones]

echo "🧪 Ejecutando pruebas..."

PYTHON_CMD="/opt/homebrew/bin/python3.11"

# Función de ayuda
show_help() {
    echo "Uso: $0 [OPCIONES]"
    echo ""
    echo "OPCIONES:"
    echo "  -h, --help       Mostrar ayuda"
    echo "  -c, --coverage   Ejecutar con cobertura"
    echo "  -v, --verbose    Modo verbose"
    echo "  -f FILE          Ejecutar archivo específico"
    echo ""
    echo "Ejemplos:"
    echo "  $0               # Todas las pruebas"
    echo "  $0 -c            # Con cobertura"
    echo "  $0 -f endpoints  # Solo endpoints"
}

# Verificar pytest
if ! $PYTHON_CMD -c "import pytest" 2>/dev/null; then
    echo "❌ pytest no encontrado. Instalando..."
    $PYTHON_CMD -m pip install pytest pytest-cov httpx pytest-mock
fi

# Parsear argumentos
COVERAGE=""
VERBOSE=""
SPECIFIC=""

while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help) show_help; exit 0 ;;
        -c|--coverage) COVERAGE="--cov=. --cov-report=term-missing"; shift ;;
        -v|--verbose) VERBOSE="-vvv"; shift ;;
        -f) SPECIFIC="tests/test_$2.py"; shift 2 ;;
        *) echo "Opción desconocida: $1"; exit 1 ;;
    esac
done

# Ejecutar pruebas
TEST_PATH=${SPECIFIC:-"tests/"}
CMD="$PYTHON_CMD -m pytest $TEST_PATH $COVERAGE $VERBOSE"

echo "Ejecutando: $CMD"
echo "=================================================="

if eval $CMD; then
    echo "✅ Pruebas completadas exitosamente"
else
    echo "❌ Algunas pruebas fallaron"
    exit 1
fi
