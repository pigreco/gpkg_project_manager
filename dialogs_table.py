# -*- coding: utf-8 -*-
"""
/***************************************************************************
 GeoPackage Project Manager - Table View Version
                              -------------------
        begin                : 2025-12-02
        git sha              : $Format:%H$
        copyright            : (C) 2025 by Salvatore Fiandaca
        email                : pigrecoinfinito@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

from qgis.core import QgsProject, Qgis
from qgis.utils import iface
from qgis.PyQt.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QComboBox, QTableWidget, QTableWidgetItem,
    QFileDialog, QMessageBox, QGroupBox, QFrame,
    QAbstractItemView, QSizePolicy, QInputDialog,
    QToolButton, QWidget, QProgressDialog, QApplication, QMenu, QCheckBox,
    QHeaderView
)
from qgis.PyQt.QtCore import Qt, QSize, QTimer, QSettings, QCoreApplication, QUrl
from qgis.PyQt.QtGui import QFont, QColor, QPalette, QIcon, QDesktopServices

import sqlite3
import os
import shutil
import re
from datetime import datetime

# Import custom TS translator
try:
    from .ts_translator import get_ts_translator
    TS_TRANSLATOR_AVAILABLE = True
except ImportError:
    TS_TRANSLATOR_AVAILABLE = False


# ============================================================
# COMPATIBILITÀ QT5/QT6
# ============================================================

def get_qt_enum(enum_class, value_name):
    """Ottiene il valore enum compatibile con Qt5 e Qt6."""
    if hasattr(enum_class, value_name):
        return getattr(enum_class, value_name)
    # Qt6 style nested enums
    for attr_name in dir(enum_class):
        attr = getattr(enum_class, attr_name)
        if hasattr(attr, value_name):
            return getattr(attr, value_name)
    return None


# Enum compatibili
UserRole = get_qt_enum(Qt, 'UserRole') or 0x0100
AlignCenter = get_qt_enum(Qt, 'AlignCenter') or 0x0084
AlignLeft = get_qt_enum(Qt, 'AlignLeft') or 0x0001
AlignVCenter = get_qt_enum(Qt, 'AlignVCenter') or 0x0080
AlignRight = get_qt_enum(Qt, 'AlignRight') or 0x0002
CustomContextMenu = get_qt_enum(Qt, 'CustomContextMenu') or 3

# QMessageBox buttons
MsgBoxYes = get_qt_enum(QMessageBox, 'Yes') or 0x00004000
MsgBoxNo = get_qt_enum(QMessageBox, 'No') or 0x00010000
MsgBoxInformation = get_qt_enum(QMessageBox, 'Information') or 1
MsgBoxCritical = get_qt_enum(QMessageBox, 'Critical') or 3
MsgBoxQuestion = get_qt_enum(QMessageBox, 'Question') or 4

# QSizePolicy
SizePolicyExpanding = get_qt_enum(QSizePolicy, 'Expanding') or 7
SizePolicyFixed = get_qt_enum(QSizePolicy, 'Fixed') or 0

# QAbstractItemView
try:
    SingleSelection = QAbstractItemView.SingleSelection
except AttributeError:
    SingleSelection = QAbstractItemView.SelectionMode.SingleSelection

try:
    NoEditTriggers = QAbstractItemView.NoEditTriggers
except AttributeError:
    NoEditTriggers = QAbstractItemView.EditTrigger.NoEditTriggers

try:
    SelectRows = QAbstractItemView.SelectRows
except AttributeError:
    SelectRows = QAbstractItemView.SelectionBehavior.SelectRows

# QHeaderView
try:
    ResizeToContents = QHeaderView.ResizeToContents
except AttributeError:
    ResizeToContents = QHeaderView.ResizeMode.ResizeToContents

try:
    Stretch = QHeaderView.Stretch
except AttributeError:
    Stretch = QHeaderView.ResizeMode.Stretch

try:
    Interactive = QHeaderView.Interactive
except AttributeError:
    Interactive = QHeaderView.ResizeMode.Interactive

try:
    Fixed = QHeaderView.Fixed
except AttributeError:
    Fixed = QHeaderView.ResizeMode.Fixed

# QFrame
HLine = get_qt_enum(QFrame, 'HLine') or 4

# QLineEdit
LineEditNormal = get_qt_enum(QLineEdit, 'Normal') or 0

# QToolButton
InstantPopup = get_qt_enum(QToolButton, 'InstantPopup') or 2

# Qt Window Modality
WindowModal = get_qt_enum(Qt, 'WindowModal') or 1


# ============================================================
# STILI CSS MODERNI
# ============================================================

MODERN_STYLE = """
QDialog {
    background-color: #ffffff;
    color: #1e1e2e;
}

QGroupBox {
    font-weight: bold;
    font-size: 13px;
    color: #1e40af;
    border: 2px solid #d1d5db;
    border-radius: 8px;
    margin-top: 12px;
    padding-top: 10px;
    background-color: #ffffff;
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: 15px;
    padding: 0 8px;
    background-color: #ffffff;
}

QLabel {
    color: #1e1e2e;
    font-size: 12px;
}

QLabel#titleLabel {
    font-size: 22px;
    font-weight: bold;
    color: #7c3aed;
    padding: 10px;
}

QLabel#subtitleLabel {
    font-size: 11px;
    color: #6b7280;
    padding-bottom: 10px;
}

QLabel#tipLabel {
    font-size: 10px;
    color: #6b7280;
    font-style: italic;
}

QLineEdit {
    background-color: #ffffff;
    border: 2px solid #d1d5db;
    border-radius: 6px;
    padding: 8px 12px;
    color: #1e1e2e;
    font-size: 12px;
    selection-background-color: #3b82f6;
}

QLineEdit:focus {
    border-color: #3b82f6;
}

QLineEdit:hover {
    border-color: #9ca3af;
}

QComboBox {
    background-color: #ffffff;
    border: 2px solid #d1d5db;
    border-radius: 6px;
    padding: 8px 12px;
    color: #1e1e2e;
    font-size: 12px;
    min-height: 20px;
}

QComboBox:hover {
    border-color: #9ca3af;
}

QComboBox:focus {
    border-color: #3b82f6;
}

QComboBox::drop-down {
    subcontrol-origin: padding;
    subcontrol-position: center right;
    width: 20px;
}

QComboBox QAbstractItemView {
    background-color: #ffffff;
    border: 2px solid #d1d5db;
    border-radius: 6px;
    color: #1e1e2e;
    selection-background-color: #3b82f6;
    selection-color: #ffffff;
    padding: 5px;
    outline: none;
}

QComboBox QAbstractItemView::item {
    padding: 8px 12px;
    min-height: 25px;
    color: #1e1e2e;
    background-color: #ffffff;
}

QComboBox QAbstractItemView::item:hover {
    background-color: #e5e7eb;
    color: #1e1e2e;
}

QComboBox QAbstractItemView::item:selected {
    background-color: #3b82f6;
    color: #ffffff;
}

QTableWidget {
    background-color: #ffffff;
    border: 2px solid #d1d5db;
    border-radius: 8px;
    padding: 5px;
    color: #1e1e2e;
    font-size: 12px;
    outline: none;
    gridline-color: #e5e7eb;
}

QTableWidget::item {
    padding: 8px 10px;
    border: none;
}

QTableWidget::item:selected {
    background-color: #3b82f6;
    color: #ffffff;
}

QTableWidget::item:hover:!selected {
    background-color: #e5e7eb;
}

QHeaderView::section {
    background-color: #f3f4f6;
    color: #1e40af;
    font-weight: bold;
    font-size: 11px;
    padding: 8px 10px;
    border: none;
    border-right: 1px solid #d1d5db;
    border-bottom: 2px solid #d1d5db;
}

QHeaderView::section:first {
    border-top-left-radius: 6px;
}

QHeaderView::section:last {
    border-top-right-radius: 6px;
    border-right: none;
}

QHeaderView::section:hover {
    background-color: #e5e7eb;
}

QPushButton {
    background-color: #e5e7eb;
    border: none;
    border-radius: 6px;
    padding: 10px 20px;
    color: #1e1e2e;
    font-size: 12px;
    font-weight: bold;
}

QPushButton:hover {
    background-color: #d1d5db;
}

QPushButton:pressed {
    background-color: #9ca3af;
}

QPushButton:disabled {
    background-color: #f3f4f6;
    color: #9ca3af;
}

QPushButton#primaryButton {
    background-color: #3b82f6;
    color: #ffffff;
}

QPushButton#primaryButton:hover {
    background-color: #2563eb;
}

QPushButton#primaryButton:pressed {
    background-color: #1d4ed8;
}

QPushButton#dangerButton {
    background-color: #ef4444;
    color: #ffffff;
}

QPushButton#dangerButton:hover {
    background-color: #dc2626;
}

QPushButton#successButton {
    background-color: #22c55e;
    color: #ffffff;
}

QPushButton#successButton:hover {
    background-color: #16a34a;
}

QPushButton#warningButton {
    background-color: #f97316;
    color: #ffffff;
}

QPushButton#warningButton:hover {
    background-color: #ea580c;
}

QPushButton#secondaryButton {
    background-color: #6366f1;
    color: #ffffff;
}

QPushButton#secondaryButton:hover {
    background-color: #4f46e5;
}

QPushButton#secondaryButton::menu-indicator {
    subcontrol-position: right center;
    subcontrol-origin: padding;
    right: 8px;
}

QToolButton {
    background-color: transparent;
    border: none;
    border-radius: 4px;
    padding: 4px;
    color: #6b7280;
    font-size: 16px;
}

QToolButton:hover {
    background-color: #e5e7eb;
    color: #1e1e2e;
}

QToolButton:pressed {
    background-color: #d1d5db;
}

QToolButton::menu-indicator {
    image: none;
}

QMenu {
    background-color: #ffffff;
    border: 2px solid #d1d5db;
    border-radius: 8px;
    padding: 5px;
    color: #1e1e2e;
}

QMenu::item {
    padding: 8px 25px;
    border-radius: 4px;
    margin: 2px 5px;
}

QMenu::item:selected {
    background-color: #3b82f6;
    color: #ffffff;
}

QMenu::separator {
    height: 1px;
    background-color: #d1d5db;
    margin: 5px 10px;
}

QProgressDialog {
    background-color: #f5f5f5;
    color: #1e1e2e;
}

QProgressBar {
    background-color: #e5e7eb;
    border: none;
    border-radius: 4px;
    height: 8px;
    text-align: center;
}

QProgressBar::chunk {
    background-color: #3b82f6;
    border-radius: 4px;
}

QScrollBar:vertical {
    background-color: #f3f4f6;
    width: 12px;
    border-radius: 6px;
    margin: 0;
}

QScrollBar::handle:vertical {
    background-color: #d1d5db;
    border-radius: 6px;
    min-height: 30px;
}

QScrollBar::handle:vertical:hover {
    background-color: #9ca3af;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0;
}

QScrollBar:horizontal {
    background-color: #f3f4f6;
    height: 12px;
    border-radius: 6px;
    margin: 0;
}

QScrollBar::handle:horizontal {
    background-color: #d1d5db;
    border-radius: 6px;
    min-width: 30px;
}

QScrollBar::handle:horizontal:hover {
    background-color: #9ca3af;
}

QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
    width: 0;
}

QFrame#separator {
    background-color: #d1d5db;
    max-height: 1px;
}

QCheckBox {
    color: #1e1e2e;
    font-size: 12px;
    spacing: 8px;
    padding: 5px;
}

QCheckBox::indicator {
    width: 18px;
    height: 18px;
    border: 2px solid #d1d5db;
    border-radius: 4px;
    background-color: #ffffff;
}

QCheckBox::indicator:hover {
    border-color: #3b82f6;
}

QCheckBox::indicator:checked {
    background-color: #3b82f6;
    border-color: #3b82f6;
    image: none;
}

QCheckBox::indicator:checked:hover {
    background-color: #2563eb;
    border-color: #2563eb;
}

QCheckBox::indicator:disabled {
    background-color: #f3f4f6;
    border-color: #d1d5db;
}

QMessageBox {
    background-color: #ffffff;
}

QMessageBox QLabel {
    color: #1e1e2e;
}
"""


# Importa tutte le funzioni e classi dal dialogs.py originale
# per mantenere la compatibilità con i metodi non modificati
import sys
import importlib.util

# Carica dialogs.py per ereditare i metodi
spec = importlib.util.spec_from_file_location("dialogs_original", 
                                               os.path.join(os.path.dirname(__file__), "dialogs.py"))
dialogs_original = importlib.util.module_from_spec(spec)
spec.loader.exec_module(dialogs_original)

# Eredita la classe base
GeoPackageProjectManagerDialogBase = dialogs_original.GeoPackageProjectManagerDialog


class GeoPackageProjectManagerDialog(GeoPackageProjectManagerDialogBase):
    """Dialog moderno per gestire i progetti QGIS in GeoPackage con vista tabella."""

    def setup_ui(self):
        """Configura l'interfaccia utente moderna con tabella."""
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        # === HEADER ===
        header_widget = QWidget()
        header_layout = QVBoxLayout(header_widget)
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(0)

        title_label = QLabel(self.tr("📦 GeoPackage Project Manager"))
        title_label.setObjectName("titleLabel")
        header_layout.addWidget(title_label)

        subtitle_label = QLabel(self.tr("Gestisci i tuoi progetti QGIS direttamente nel GeoPackage"))
        subtitle_label.setObjectName("subtitleLabel")
        header_layout.addWidget(subtitle_label)

        layout.addWidget(header_widget)

        # === SEZIONE GEOPACKAGE ===
        gpkg_group = QGroupBox(self.tr("  📁  Seleziona GeoPackage"))
        gpkg_layout = QVBoxLayout(gpkg_group)
        gpkg_layout.setSpacing(10)

        gpkg_select_layout = QHBoxLayout()
        self.gpkg_combo = QComboBox()
        self.gpkg_combo.setSizePolicy(SizePolicyExpanding, SizePolicyFixed)
        self.gpkg_combo.currentTextChanged.connect(self.on_gpkg_changed)
        gpkg_select_layout.addWidget(self.gpkg_combo)

        self.btn_sfoglia = QPushButton(self.tr("📂 Sfoglia"))
        self.btn_sfoglia.setFixedWidth(100)
        self.btn_sfoglia.clicked.connect(self.sfoglia_geopackage)
        gpkg_select_layout.addWidget(self.btn_sfoglia)

        self.btn_aggiorna = QPushButton(self.tr("⟳"))
        self.btn_aggiorna.setFixedWidth(45)
        self.btn_aggiorna.setStyleSheet("""
            QPushButton {
                font-size: 20px;
                font-weight: bold;
                padding: 4px;
            }
        """)
        self.btn_aggiorna.setToolTip(self.tr("Aggiorna lista GeoPackage"))
        self.btn_aggiorna.clicked.connect(self.trova_geopackage_automatico)
        gpkg_select_layout.addWidget(self.btn_aggiorna)

        gpkg_layout.addLayout(gpkg_select_layout)

        # Info box: dimensione e numero progetti
        self.gpkg_info_label = QLabel(self.tr("ℹ️ Info: --"))
        self.gpkg_info_label.setObjectName("tipLabel")
        self.gpkg_info_label.setStyleSheet("""
            QLabel {
                color: #6b7280;
                font-size: 11px;
                padding: 5px 10px;
                background-color: #f9fafb;
                border-radius: 4px;
            }
        """)
        gpkg_layout.addWidget(self.gpkg_info_label)

        # Pulsante Clone GeoPackage e opzioni
        clone_layout = QHBoxLayout()
        clone_layout.addStretch()
        self.btn_clone_gpkg = QPushButton(self.tr("🔀 Clona GPKG"))
        self.btn_clone_gpkg.setObjectName("warningButton")
        self.btn_clone_gpkg.setToolTip(self.tr("Crea una copia del GeoPackage con percorsi aggiornati"))
        self.btn_clone_gpkg.clicked.connect(self.clona_geopackage)
        clone_layout.addWidget(self.btn_clone_gpkg)

        clone_layout.addSpacing(10)

        # Pulsante Ottimizza Database
        self.btn_ottimizza = QPushButton(self.tr("⚙️ Ottimizza DB"))
        self.btn_ottimizza.setToolTip(self.tr("Compatta il database per ridurre dimensioni e migliorare performance"))
        self.btn_ottimizza.clicked.connect(self.ottimizza_database)
        clone_layout.addWidget(self.btn_ottimizza)

        clone_layout.addSpacing(10)

        # Pulsante Aggiorna Metadati
        self.btn_aggiorna_metadati = QPushButton(self.tr("📊 Metadati"))
        self.btn_aggiorna_metadati.setObjectName("secondaryButton")
        self.btn_aggiorna_metadati.setToolTip(self.tr("Rigenera i metadati per tutti i progetti (data, dimensione, layer)"))
        self.btn_aggiorna_metadati.clicked.connect(self.aggiorna_tutti_metadati)
        clone_layout.addWidget(self.btn_aggiorna_metadati)

        clone_layout.addSpacing(10)

        # Pulsante Gestione Stili
        self.btn_gestione_stili = QPushButton(self.tr("🎨 Stili"))
        self.btn_gestione_stili.setObjectName("secondaryButton")
        self.btn_gestione_stili.setToolTip(self.tr("Visualizza e gestisci gli stili salvati nel GeoPackage"))
        self.btn_gestione_stili.clicked.connect(self.apri_gestione_stili)
        clone_layout.addWidget(self.btn_gestione_stili)

        # Checkbox per aggiungere versione al clone
        self.chk_clone_add_version = QCheckBox(self.tr("Versioning (v01, v02, ...)"))
        self.chk_clone_add_version.setChecked(QSettings().value('gpkg_project_manager/clone_add_version', False, type=bool))
        self.chk_clone_add_version.stateChanged.connect(self.on_clone_version_changed)
        clone_layout.addWidget(self.chk_clone_add_version)

        clone_layout.addStretch()
        gpkg_layout.addLayout(clone_layout)

        layout.addWidget(gpkg_group)

        # === SEZIONE SALVATAGGIO ===
        save_group = QGroupBox(self.tr("  💾  Salva Progetto Corrente"))
        save_layout = QVBoxLayout(save_group)
        save_layout.setSpacing(12)

        name_layout = QHBoxLayout()
        name_label = QLabel(self.tr("Nome:"))
        name_label.setFixedWidth(50)
        name_layout.addWidget(name_label)
        self.txt_nome_progetto = QLineEdit()
        self.txt_nome_progetto.setPlaceholderText(self.tr("Inserisci il nome del progetto..."))
        name_layout.addWidget(self.txt_nome_progetto)

        self.btn_salva = QPushButton(self.tr("💾  Salva nel GPKG"))
        self.btn_salva.setObjectName("primaryButton")
        self.btn_salva.clicked.connect(self.salva_progetto)
        name_layout.addWidget(self.btn_salva)

        save_layout.addLayout(name_layout)

        # Checkbox per opzioni di salvataggio (allineata con il campo nome)
        options_layout = QHBoxLayout()
        options_spacing = QLabel("")  # Label vuota per allineamento
        options_spacing.setFixedWidth(50)
        options_layout.addWidget(options_spacing)
        
        self.chk_add_timestamp = QCheckBox(self.tr("Timestamp"))
        self.chk_add_timestamp.setChecked(QSettings().value('gpkg_project_manager/add_timestamp', False, type=bool))
        self.chk_add_timestamp.setToolTip(self.tr("Aggiungi timestamp al nome del progetto\nFormato: progetto_YYYYMMDDHHmmss\nEsempio: mio_progetto_20251202143055"))
        self.chk_add_timestamp.stateChanged.connect(self.on_timestamp_changed)
        options_layout.addWidget(self.chk_add_timestamp)
        
        options_layout.addSpacing(20)
        
        self.chk_add_version = QCheckBox(self.tr("Versioning"))
        self.chk_add_version.setChecked(QSettings().value('gpkg_project_manager/add_version', False, type=bool))
        self.chk_add_version.setToolTip(self.tr("Aggiungi versione incrementale al nome del progetto\nFormato: progetto_vNN (dove NN è un numero progressivo)\nEsempio: mio_progetto_v01, mio_progetto_v02, ..."))
        self.chk_add_version.stateChanged.connect(self.on_version_changed)
        options_layout.addWidget(self.chk_add_version)
        
        options_layout.addStretch()
        save_layout.addLayout(options_layout)

        layout.addWidget(save_group)

        # === SEZIONE PROGETTI - TABELLA ===
        progetti_group = QGroupBox(self.tr("  📋  Progetti nel GeoPackage  (Doppio clic per caricare • Icona ⚙️ per opzioni)"))
        progetti_layout = QVBoxLayout(progetti_group)
        progetti_layout.setSpacing(8)

        # TABELLA invece di LISTA
        self.tabella_progetti = QTableWidget()
        self.tabella_progetti.setColumnCount(7)  # 6 colonne dati + 1 colonna opzioni
        self.tabella_progetti.setHorizontalHeaderLabels([
            self.tr("Nome Progetto"),
            self.tr("Data Creazione"),
            self.tr("Data Modifica"),
            self.tr("Dimensione"),
            self.tr("Layer"),
            self.tr("EPSG"),
            self.tr("⚙️")  # Colonna opzioni
        ])
        
        # Calcola altezza per 2 righe + header
        row_height = 35  # Altezza stimata per riga
        header_height = 30  # Altezza header
        total_height = (row_height * 2) + header_height + 10  # 10px di padding
        self.tabella_progetti.setMinimumHeight(total_height)
        self.tabella_progetti.setMaximumHeight(total_height)
        
        self.tabella_progetti.setAlternatingRowColors(True)
        self.tabella_progetti.setSelectionMode(SingleSelection)
        self.tabella_progetti.setSelectionBehavior(SelectRows)
        self.tabella_progetti.setEditTriggers(NoEditTriggers)
        self.tabella_progetti.verticalHeader().setVisible(False)
        self.tabella_progetti.setSortingEnabled(True)
        
        # Imposta il ridimensionamento delle colonne
        header = self.tabella_progetti.horizontalHeader()
        header.setSectionResizeMode(0, Stretch)  # Nome Progetto - si espande automaticamente
        # Colonne 1-5 ridimensionabili manualmente dall'utente
        for i in range(1, 6):
            header.setSectionResizeMode(i, Interactive)
        # Colonna 6 (opzioni) ha larghezza fissa non ridimensionabile
        self.tabella_progetti.setColumnWidth(6, 40)  # Larghezza fissa 40px
        header.setSectionResizeMode(6, Fixed)
        
        # Eventi
        self.tabella_progetti.cellDoubleClicked.connect(self.carica_progetto_da_tabella)
        
        progetti_layout.addWidget(self.tabella_progetti)

        layout.addWidget(progetti_group)

        # === FOOTER ===
        layout.addStretch()

        separator = QFrame()
        separator.setObjectName("separator")
        separator.setFrameShape(HLine)
        layout.addWidget(separator)

        footer_layout = QHBoxLayout()

        version_label = QLabel(self.tr("v3.3 • Qt5/Qt6 Compatible • Table View"))
        version_label.setObjectName("tipLabel")
        footer_layout.addWidget(version_label)

        footer_layout.addStretch()

        # Help button
        btn_help = QPushButton("📖 " + self.tr("Aiuto / Help"))
        btn_help.setFixedWidth(140)
        btn_help.setToolTip(self.tr("Apri la guida online / Open online guide"))
        btn_help.clicked.connect(self.open_help)
        footer_layout.addWidget(btn_help)

        self.btn_chiudi = QPushButton(self.tr("Chiudi"))
        self.btn_chiudi.setFixedWidth(100)
        self.btn_chiudi.clicked.connect(self.close)
        footer_layout.addWidget(self.btn_chiudi)

        layout.addLayout(footer_layout)

        self.imposta_nome_progetto_default()

    def aggiorna_lista_progetti(self):
        """Aggiorna la tabella dei progetti salvati nel GeoPackage."""
        self.tabella_progetti.setRowCount(0)

        if not self.gpkg_path or not os.path.exists(self.gpkg_path):
            return

        try:
            conn = sqlite3.connect(self.gpkg_path)
            cursor = conn.cursor()

            cursor.execute("""
                SELECT name FROM sqlite_master
                WHERE type='table' AND name='qgis_projects'
            """)

            if cursor.fetchone():
                # Assicura che la tabella metadati esista
                self.crea_tabella_metadata(conn)
                
                cursor.execute("""
                    SELECT 
                        p.name,
                        m.created_date,
                        m.modified_date,
                        m.size_bytes,
                        m.layer_count,
                        m.vector_count,
                        m.raster_count,
                        m.table_count,
                        m.crs_epsg
                    FROM qgis_projects p
                    LEFT JOIN qgis_projects_metadata m ON p.name = m.project_name
                    ORDER BY p.name
                """)
                
                for row in cursor.fetchall():
                    self.aggiungi_riga_progetto(row)

            conn.close()

        except Exception as e:
            self.mostra_errore(self.tr("Errore"), self.tr("Errore nella lettura dei progetti:\n{}").format(str(e)))

        # Aggiorna info GeoPackage
        self.aggiorna_info_gpkg()

    def aggiungi_riga_progetto(self, dati):
        """Aggiunge una riga alla tabella progetti.
        
        Args:
            dati: tuple (nome, data_creazione, data_modifica, size_bytes, layer_count, vector_count, raster_count, table_count, crs_epsg)
        """
        nome, created_date, modified_date, size_bytes, layer_count, vector_count, raster_count, table_count, crs_epsg = dati
        
        row_position = self.tabella_progetti.rowCount()
        self.tabella_progetti.insertRow(row_position)
        
        # Verifica se questo progetto è quello correntemente caricato
        current_project = QgsProject.instance()
        is_current_project = False
        
        if current_project and self.gpkg_path:
            # Verifica se il progetto corrente è caricato dal GeoPackage
            project_file = current_project.fileName()
            
            # Caso 1: Progetto caricato dal GeoPackage (URI formato: geopackage:path?projectName=nome)
            if project_file and project_file.startswith("geopackage:"):
                # Estrai il nome del progetto dall'URI
                if "?projectName=" in project_file:
                    uri_parts = project_file.split("?projectName=")
                    if len(uri_parts) == 2:
                        gpkg_path_in_uri = uri_parts[0].replace("geopackage:", "")
                        project_name_in_uri = uri_parts[1]
                        # Verifica che sia lo stesso GeoPackage e lo stesso progetto
                        if os.path.normpath(gpkg_path_in_uri) == os.path.normpath(self.gpkg_path) and project_name_in_uri == nome:
                            is_current_project = True
            # Caso 2: Progetto salvato come file .qgs/.qgz (confronta nome base)
            elif project_file:
                current_project_name = os.path.splitext(os.path.basename(project_file))[0]
                if current_project_name == nome:
                    is_current_project = True
        
        # Colonna 0: Nome Progetto
        # Aggiungi icona verde se è il progetto corrente
        if is_current_project:
            item_nome = QTableWidgetItem(f"  ✅  {nome}")
        else:
            item_nome = QTableWidgetItem(f"  📋  {nome}")
        item_nome.setData(UserRole, nome)
        self.tabella_progetti.setItem(row_position, 0, item_nome)
        
        # Colonna 1: Data Creazione
        if created_date:
            try:
                dt = datetime.strptime(created_date, '%Y-%m-%d %H:%M:%S')
                data_formattata = dt.strftime('%d/%m/%Y %H:%M')
            except:
                data_formattata = created_date
        else:
            data_formattata = "N/A"
        item_created = QTableWidgetItem(data_formattata)
        item_created.setTextAlignment(AlignCenter | AlignVCenter)
        self.tabella_progetti.setItem(row_position, 1, item_created)
        
        # Colonna 2: Data Modifica
        if modified_date:
            try:
                dt = datetime.strptime(modified_date, '%Y-%m-%d %H:%M:%S')
                data_formattata = dt.strftime('%d/%m/%Y %H:%M')
            except:
                data_formattata = modified_date
        else:
            data_formattata = "N/A"
        item_modified = QTableWidgetItem(data_formattata)
        item_modified.setTextAlignment(AlignCenter | AlignVCenter)
        self.tabella_progetti.setItem(row_position, 2, item_modified)
        
        # Colonna 3: Dimensione
        if size_bytes:
            if size_bytes < 1024:
                size_str = f"{size_bytes} B"
            elif size_bytes < 1024 * 1024:
                size_str = f"{size_bytes / 1024:.1f} KB"
            else:
                size_str = f"{size_bytes / (1024 * 1024):.1f} MB"
        else:
            size_str = "N/A"
        item_size = QTableWidgetItem(size_str)
        item_size.setTextAlignment(AlignCenter | AlignVCenter)
        self.tabella_progetti.setItem(row_position, 3, item_size)
        
        # Colonna 4: Layer (dettaglio: vettoriali, raster, tabelle)
        if layer_count:
            v = vector_count if vector_count else 0
            r = raster_count if raster_count else 0
            t = table_count if table_count else 0
            # Formato: "V:3 R:2 T:1" o solo numeri non zero
            parts = []
            if v > 0:
                parts.append(f"V:{v}")
            if r > 0:
                parts.append(f"R:{r}")
            if t > 0:
                parts.append(f"T:{t}")
            layer_str = " ".join(parts) if parts else str(layer_count)
        else:
            layer_str = "N/A"
        item_layers = QTableWidgetItem(layer_str)
        item_layers.setTextAlignment(AlignCenter | AlignVCenter)
        self.tabella_progetti.setItem(row_position, 4, item_layers)
        
        # Colonna 5: EPSG
        epsg_str = crs_epsg if crs_epsg else "N/A"
        item_epsg = QTableWidgetItem(epsg_str)
        item_epsg.setTextAlignment(AlignCenter | AlignVCenter)
        self.tabella_progetti.setItem(row_position, 5, item_epsg)
        
        # Colonna 6: Pulsante Opzioni
        btn_opzioni = QToolButton()
        btn_opzioni.setText("⋮")
        btn_opzioni.setPopupMode(InstantPopup)
        btn_opzioni.setStyleSheet("""
            QToolButton {
                font-size: 20px;
                font-weight: bold;
                padding: 2px 8px;
            }
        """)
        
        menu_opzioni = QMenu()
        menu_opzioni.addAction(self.tr("📂  Carica"), lambda n=nome: self.carica_progetto_per_nome(n))
        menu_opzioni.addAction(self.tr("⟳  Sovrascrivi"), lambda n=nome: self.sovrascrivi_progetto_per_nome(n))
        menu_opzioni.addSeparator()
        menu_opzioni.addAction(self.tr("✏️  Rinomina"), lambda n=nome: self.rinomina_progetto_per_nome(n))
        menu_opzioni.addAction(self.tr("📋  Duplica"), lambda n=nome: self.duplica_progetto_per_nome(n))
        menu_opzioni.addSeparator()
        menu_opzioni.addAction(self.tr("📄  Esporta come QGS"), lambda n=nome: self.esporta_qgs_per_nome(n))
        menu_opzioni.addAction(self.tr("📦  Esporta come QGZ"), lambda n=nome: self.esporta_qgz_per_nome(n))
        menu_opzioni.addSeparator()
        menu_opzioni.addAction(self.tr("🗑️  Elimina"), lambda n=nome: self.elimina_progetto_per_nome(n))
        
        btn_opzioni.setMenu(menu_opzioni)
        
        self.tabella_progetti.setCellWidget(row_position, 6, btn_opzioni)

    def aggiorna_info_gpkg(self):
        """Aggiorna le informazioni del GeoPackage (dimensione e numero progetti)."""
        if not self.gpkg_path or not os.path.exists(self.gpkg_path):
            self.gpkg_info_label.setText(self.tr("ℹ️ Info: --"))
            return

        try:
            # Calcola dimensione file
            size_bytes = os.path.getsize(self.gpkg_path)
            if size_bytes < 1024:
                size_str = f"{size_bytes} B"
            elif size_bytes < 1024 * 1024:
                size_str = f"{size_bytes / 1024:.1f} KB"
            elif size_bytes < 1024 * 1024 * 1024:
                size_str = f"{size_bytes / (1024 * 1024):.1f} MB"
            else:
                size_str = f"{size_bytes / (1024 * 1024 * 1024):.2f} GB"

            # Conta progetti
            num_progetti = self.tabella_progetti.rowCount()

            # Aggiorna label
            self.gpkg_info_label.setText(
                self.tr("ℹ️ Info: {0} • {1} {2}").format(
                    size_str,
                    num_progetti,
                    self.tr("progetti") if num_progetti != 1 else self.tr("progetto")
                )
            )
        except Exception as e:
            self.gpkg_info_label.setText(self.tr("ℹ️ Info: Errore lettura"))

    def get_progetto_selezionato(self):
        """Restituisce il nome del progetto selezionato nella tabella."""
        current_row = self.tabella_progetti.currentRow()
        if current_row >= 0:
            item = self.tabella_progetti.item(current_row, 0)
            if item:
                return item.data(UserRole)
        return None

    def get_lista_nomi_progetti(self):
        """Restituisce la lista dei nomi dei progetti dalla tabella."""
        nomi = []
        for row in range(self.tabella_progetti.rowCount()):
            item = self.tabella_progetti.item(row, 0)
            if item:
                nomi.append(item.data(UserRole))
        return nomi

    def carica_progetto_da_tabella(self, row, column):
        """Carica il progetto quando si fa doppio clic su una cella."""
        item = self.tabella_progetti.item(row, 0)
        if item:
            nome_progetto = item.data(UserRole)
            self.carica_progetto_per_nome(nome_progetto)

    def mostra_menu_contestuale_tabella(self, position):
        """Mostra il menu contestuale sulla tabella."""
        item = self.tabella_progetti.itemAt(position)
        if not item:
            return

        # Seleziona la riga
        row = item.row()
        self.tabella_progetti.selectRow(row)

        nome_progetto = self.tabella_progetti.item(row, 0).data(UserRole)

        menu = QMenu()
        menu.setStyleSheet(MODERN_STYLE)

        menu.addAction(self.tr("📂  Carica"), lambda: self.carica_progetto_per_nome(nome_progetto))
        menu.addAction(self.tr("⟳  Sovrascrivi"), lambda: self.sovrascrivi_progetto_per_nome(nome_progetto))
        menu.addSeparator()
        menu.addAction(self.tr("✏️  Rinomina"), lambda: self.rinomina_progetto_per_nome(nome_progetto))
        menu.addAction(self.tr("📋  Duplica"), lambda: self.duplica_progetto_per_nome(nome_progetto))
        menu.addSeparator()
        menu.addAction(self.tr("📄  Esporta come QGS"), lambda: self.esporta_qgs_per_nome(nome_progetto))
        menu.addAction(self.tr("📦  Esporta come QGZ"), lambda: self.esporta_qgz_per_nome(nome_progetto))
        menu.addSeparator()
        menu.addAction(self.tr("🗑️  Elimina"), lambda: self.elimina_progetto_per_nome(nome_progetto))

        menu.exec(self.tabella_progetti.mapToGlobal(position))

    # Metodi helper per le azioni sui progetti specifici
    def carica_progetto_per_nome(self, nome_progetto):
        """Carica un progetto specifico per nome."""
        self.seleziona_progetto_per_nome(nome_progetto)
        self.carica_progetto()

    def sovrascrivi_progetto_per_nome(self, nome_progetto):
        """Sovrascrive un progetto specifico per nome."""
        self.seleziona_progetto_per_nome(nome_progetto)
        self.sovrascrivi_progetto()

    def rinomina_progetto_per_nome(self, nome_progetto):
        """Rinomina un progetto specifico per nome."""
        self.seleziona_progetto_per_nome(nome_progetto)
        self.rinomina_progetto()

    def duplica_progetto_per_nome(self, nome_progetto):
        """Duplica un progetto specifico per nome."""
        self.seleziona_progetto_per_nome(nome_progetto)
        self.duplica_progetto()

    def elimina_progetto_per_nome(self, nome_progetto):
        """Elimina un progetto specifico per nome."""
        self.seleziona_progetto_per_nome(nome_progetto)
        self.elimina_progetto()

    def esporta_qgs_per_nome(self, nome_progetto):
        """Esporta un progetto come QGS per nome."""
        self.seleziona_progetto_per_nome(nome_progetto)
        self.esporta_qgs()

    def esporta_qgz_per_nome(self, nome_progetto):
        """Esporta un progetto come QGZ per nome."""
        self.seleziona_progetto_per_nome(nome_progetto)
        self.esporta_qgz()

    def seleziona_progetto_per_nome(self, nome_progetto):
        """Seleziona un progetto nella tabella per nome."""
        for row in range(self.tabella_progetti.rowCount()):
            item = self.tabella_progetti.item(row, 0)
            if item and item.data(UserRole) == nome_progetto:
                self.tabella_progetti.selectRow(row)
                return

    def on_gpkg_changed(self, text):
        """Gestisce il cambio di GeoPackage selezionato."""
        if text and not text.startswith("--"):
            self.gpkg_path = text
            self.aggiorna_lista_progetti()
        else:
            self.gpkg_path = None
            self.tabella_progetti.setRowCount(0)
            self.aggiorna_info_gpkg()

    def ottimizza_database(self):
        """Override per usare tabella_progetti invece di lista_progetti."""
        if not self.gpkg_path:
            self.mostra_errore(self.tr("Attenzione"), self.tr("Seleziona prima un GeoPackage."))
            return

        if not os.path.exists(self.gpkg_path):
            self.mostra_errore(self.tr("Errore"), self.tr("Il file GeoPackage non esiste."))
            return

        try:
            # Calcola dimensione prima dell'ottimizzazione
            size_before = os.path.getsize(self.gpkg_path)
            if size_before < 1024:
                size_before_str = f"{size_before} B"
            elif size_before < 1024 * 1024:
                size_before_str = f"{size_before / 1024:.1f} KB"
            elif size_before < 1024 * 1024 * 1024:
                size_before_str = f"{size_before / (1024 * 1024):.1f} MB"
            else:
                size_before_str = f"{size_before / (1024 * 1024 * 1024):.2f} GB"

            # Conta progetti dalla tabella
            num_progetti = self.tabella_progetti.rowCount()

            # Dialog di conferma
            msg = QMessageBox(self)
            msg.setIcon(MsgBoxQuestion)
            msg.setWindowTitle(self.tr("⚙️ Ottimizza GeoPackage"))
            msg.setText(
                self.tr("Dimensione attuale: {0}\nProgetti: {1}\n\n"
                        "⚠️ L'ottimizzazione può richiedere tempo per file di grandi dimensioni.\n\n"
                        "Vuoi continuare?").format(size_before_str, num_progetti)
            )
            msg.setStandardButtons(MsgBoxYes | MsgBoxNo)
            msg.setDefaultButton(MsgBoxNo)
            msg.setStyleSheet(MODERN_STYLE)

            if msg.exec() != MsgBoxYes:
                return

            # Progress dialog
            progress = QProgressDialog(
                self.tr("Ottimizzazione del database in corso...\n\nCompattazione e pulizia dello spazio inutilizzato..."),
                None, 0, 0, self
            )
            progress.setWindowTitle(self.tr("⚙️ Ottimizzazione"))
            progress.setStyleSheet(MODERN_STYLE)
            progress.setWindowModality(WindowModal)
            progress.show()
            QApplication.processEvents()

            # Esegui VACUUM
            conn = sqlite3.connect(self.gpkg_path)
            conn.execute("VACUUM")
            conn.close()

            progress.close()

            # Calcola dimensione dopo l'ottimizzazione
            size_after = os.path.getsize(self.gpkg_path)
            if size_after < 1024:
                size_after_str = f"{size_after} B"
            elif size_after < 1024 * 1024:
                size_after_str = f"{size_after / 1024:.1f} KB"
            elif size_after < 1024 * 1024 * 1024:
                size_after_str = f"{size_after / (1024 * 1024):.1f} MB"
            else:
                size_after_str = f"{size_after / (1024 * 1024 * 1024):.2f} GB"

            # Calcola risparmio
            saved = size_before - size_after
            if saved < 1024:
                saved_str = f"{saved} B"
            elif saved < 1024 * 1024:
                saved_str = f"{saved / 1024:.1f} KB"
            elif saved < 1024 * 1024 * 1024:
                saved_str = f"{saved / (1024 * 1024):.1f} MB"
            else:
                saved_str = f"{saved / (1024 * 1024 * 1024):.2f} GB"

            percentage = (saved / size_before * 100) if size_before > 0 else 0

            # Aggiorna info
            self.aggiorna_info_gpkg()

            # Messaggio di successo
            iface.messageBar().pushMessage(
                self.tr("✅ Ottimizzazione completata"),
                self.tr("Prima: {0} • Dopo: {1} • Risparmiati: {2} ({3:.1f}%)").format(
                    size_before_str, size_after_str, saved_str, percentage
                ),
                level=Qgis.Success,
                duration=10
            )

        except Exception as e:
            import traceback
            self.mostra_errore(self.tr("Errore"), self.tr("Errore durante l'ottimizzazione:\n{}").format(str(e) + "\n\n" + traceback.format_exc()))

    def apri_gestione_stili(self):
        """Apre il dialogo per la gestione degli stili."""
        if not self.gpkg_path:
            self.mostra_errore(self.tr("Attenzione"), self.tr("Seleziona prima un GeoPackage."))
            return

        if not os.path.exists(self.gpkg_path):
            self.mostra_errore(self.tr("Errore"), self.tr("Il file GeoPackage non esiste."))
            return

        # Importa il dialogo stili
        from .dialog_styles import StylesManagerDialog

        # Apri il dialogo
        dialog = StylesManagerDialog(self.gpkg_path, self)
        dialog.exec()

    def clear_gui(self):
        """Pulisce la GUI all'avvio del plugin."""
        # Imposta valore di default per il nome progetto
        self.txt_nome_progetto.setText("progetto")
        # Pulisci tabella progetti
        self.tabella_progetti.setRowCount(0)
        # Reset info GeoPackage
        self.gpkg_info_label.setText(self.tr("ℹ️ Info: --"))
