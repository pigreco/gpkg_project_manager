#!/bin/bash
# Script per creare il file ZIP del plugin QGIS
# Versione: 1.0

set -e  # Exit on error

# Colori per output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Directory del progetto
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PLUGIN_NAME="gpkg_project_manager"
ZIP_NAME="${PLUGIN_NAME}.zip"

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  QGIS Plugin ZIP Creator${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Vai alla directory del progetto
cd "$PROJECT_DIR"

echo -e "${YELLOW}📂 Directory progetto:${NC} $PROJECT_DIR"
echo -e "${YELLOW}📦 Nome plugin:${NC} $PLUGIN_NAME"
echo ""

# Rimuovi ZIP precedente se esiste
if [ -f "../${ZIP_NAME}" ]; then
    echo -e "${YELLOW}🗑️  Rimozione ZIP precedente...${NC}"
    rm -f "../${ZIP_NAME}"
fi

# File e cartelle da includere
echo -e "${GREEN}✓ Creazione ZIP...${NC}"

# I file sono nella directory corrente, dobbiamo crearli con il path corretto nel ZIP
zip -r "../${ZIP_NAME}" \
    __init__.py \
    main.py \
    dialogs.py \
    ts_translator.py \
    metadata.txt \
    icon.png \
    README.md \
    i18n/ \
    -x "*.pyc" \
    -x "*__pycache__*" \
    -x "*.git*" \
    -x "*__MACOSX*" \
    -x "*.DS_Store" \
    > /dev/null 2>&1

# Rinomina la struttura interna del ZIP per includere la cartella plugin
if [ -f "../${ZIP_NAME}" ]; then
    # Crea temporary directory
    TEMP_DIR=$(mktemp -d)

    # Estrai il ZIP
    unzip -q "../${ZIP_NAME}" -d "$TEMP_DIR"

    # Crea la directory del plugin
    mkdir -p "$TEMP_DIR/$PLUGIN_NAME"

    # Muovi i file nella directory del plugin
    mv "$TEMP_DIR"/*.py "$TEMP_DIR/$PLUGIN_NAME/" 2>/dev/null || true
    mv "$TEMP_DIR"/*.txt "$TEMP_DIR/$PLUGIN_NAME/" 2>/dev/null || true
    mv "$TEMP_DIR"/*.png "$TEMP_DIR/$PLUGIN_NAME/" 2>/dev/null || true
    mv "$TEMP_DIR"/*.md "$TEMP_DIR/$PLUGIN_NAME/" 2>/dev/null || true
    mv "$TEMP_DIR"/i18n "$TEMP_DIR/$PLUGIN_NAME/" 2>/dev/null || true

    # Rimuovi il vecchio ZIP
    rm "../${ZIP_NAME}"

    # Crea il nuovo ZIP con la struttura corretta
    cd "$TEMP_DIR"
    zip -r "$PROJECT_DIR/../${ZIP_NAME}" "$PLUGIN_NAME" \
        -x "*.pyc" \
        -x "*__pycache__*" \
        > /dev/null 2>&1

    # Torna alla directory del progetto
    cd "$PROJECT_DIR"

    # Rimuovi temporary directory
    rm -rf "$TEMP_DIR"
fi

# Verifica creazione
if [ -f "../${ZIP_NAME}" ]; then
    echo -e "${GREEN}✓ ZIP creato con successo!${NC}"
    echo ""

    # Mostra informazioni sul file
    SIZE=$(du -h "../${ZIP_NAME}" | cut -f1)
    DATE=$(stat -c %y "../${ZIP_NAME}" | cut -d' ' -f1,2 | cut -d'.' -f1)

    echo -e "${BLUE}📋 Informazioni file:${NC}"
    echo -e "   📁 Percorso: ${GREEN}../gpkg_project_manager.zip${NC}"
    echo -e "   💾 Dimensione: ${GREEN}${SIZE}${NC}"
    echo -e "   📅 Data: ${GREEN}${DATE}${NC}"
    echo ""

    # Mostra contenuto ZIP
    echo -e "${BLUE}📦 Contenuto ZIP:${NC}"
    unzip -l "../${ZIP_NAME}" | tail -n +4 | head -n -2
    echo ""

    # Conta file
    FILE_COUNT=$(unzip -l "../${ZIP_NAME}" | tail -n 1 | awk '{print $2}')
    echo -e "${GREEN}✓ Totale file inclusi: ${FILE_COUNT}${NC}"
    echo ""

    echo -e "${GREEN}========================================${NC}"
    echo -e "${GREEN}  Plugin pronto per l'installazione!${NC}"
    echo -e "${GREEN}========================================${NC}"
else
    echo -e "${YELLOW}❌ Errore nella creazione del ZIP${NC}"
    exit 1
fi
