# -*- coding: utf-8 -*-
"""
/***************************************************************************
 GeoPackage Project Manager
                              -------------------
        begin                : 2025-11-30
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
    QPushButton, QComboBox, QListWidget, QListWidgetItem,
    QFileDialog, QMessageBox, QGroupBox, QFrame,
    QAbstractItemView, QSizePolicy, QInputDialog,
    QToolButton, QWidget, QProgressDialog, QApplication, QMenu, QCheckBox
)
from qgis.PyQt.QtCore import Qt, QSize, QTimer, QSettings, QCoreApplication, QUrl, QEvent
from qgis.PyQt.QtGui import QFont, QColor, QPalette, QIcon, QDesktopServices
from qgis.PyQt.QtWidgets import QToolTip

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
SingleSelection = get_qt_enum(QAbstractItemView, 'SingleSelection') or 1

# QFrame
HLine = get_qt_enum(QFrame, 'HLine') or 4

# QLineEdit
LineEditNormal = get_qt_enum(QLineEdit, 'Normal') or 0

# QToolButton
InstantPopup = get_qt_enum(QToolButton, 'InstantPopup') or 2

# QEvent
EventToolTip = get_qt_enum(QEvent, 'ToolTip') or 17

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

QListWidget {
    background-color: #ffffff;
    border: 2px solid #d1d5db;
    border-radius: 8px;
    padding: 5px;
    color: #1e1e2e;
    font-size: 12px;
    outline: none;
}

QListWidget::item {
    padding: 10px 15px;
    border-radius: 6px;
    margin: 2px 5px;
}

QListWidget::item:selected {
    background-color: #3b82f6;
    color: #ffffff;
}

QListWidget::item:hover:!selected {
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
    background-color: #e5e7eb;
    border: none;
    border-radius: 6px;
    padding: 10px 20px;
    color: #1e1e2e;
    font-size: 12px;
    font-weight: bold;
}

QToolButton:hover {
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


class GeoPackageProjectManagerDialog(QDialog):
    """Dialog moderno per gestire i progetti QGIS in GeoPackage."""

    def __init__(self, parent=None, plugin=None):
        super().__init__(parent or iface.mainWindow())
        self.plugin = plugin  # Reference to main plugin for language change
        self.gpkg_path = None

        self.setWindowTitle(self.tr("GeoPackage Project Manager"))
        self.setMinimumSize(680, 700)
        self.resize(720, 780)

        self.setup_ui()
        self.setStyleSheet(MODERN_STYLE)
        self.clear_gui()
        self.trova_geopackage_automatico()

    def tr(self, message):
        """Translate string using Qt translation API.

        Args:
            message: String to translate

        Returns:
            Translated string
        """
        # Try TS translator first if available
        if TS_TRANSLATOR_AVAILABLE:
            translator = get_ts_translator()
            if translator.loaded:
                translation = translator.translate('GeoPackageProjectManagerDialog', message)
                if translation != message:
                    return translation

        # Fall back to Qt translator
        return QCoreApplication.translate('GeoPackageProjectManagerDialog', message)

    def setup_ui(self):
        """Configura l'interfaccia utente moderna."""
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
        self.btn_clone_gpkg = QPushButton(self.tr("🔀 Clona GeoPackage"))
        self.btn_clone_gpkg.setObjectName("warningButton")
        self.btn_clone_gpkg.setToolTip(self.tr("Crea una copia del GeoPackage con percorsi aggiornati"))
        self.btn_clone_gpkg.clicked.connect(self.clona_geopackage)
        clone_layout.addWidget(self.btn_clone_gpkg)

        clone_layout.addSpacing(10)

        # Pulsante Ottimizza Database
        self.btn_ottimizza = QPushButton(self.tr("⚙️ Ottimizza Database"))
        self.btn_ottimizza.setToolTip(self.tr("Compatta il database per ridurre dimensioni e migliorare performance"))
        self.btn_ottimizza.clicked.connect(self.ottimizza_database)
        clone_layout.addWidget(self.btn_ottimizza)

        clone_layout.addSpacing(10)

        # Pulsante Aggiorna Metadati
        self.btn_aggiorna_metadati = QPushButton(self.tr("📊 Aggiorna Metadati"))
        self.btn_aggiorna_metadati.setObjectName("secondaryButton")
        self.btn_aggiorna_metadati.setToolTip(self.tr("Rigenera i metadati per tutti i progetti (data, dimensione, layer)"))
        self.btn_aggiorna_metadati.clicked.connect(self.aggiorna_tutti_metadati)
        clone_layout.addWidget(self.btn_aggiorna_metadati)

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

        self.btn_salva = QPushButton(self.tr("💾  Salva nel GeoPackage"))
        self.btn_salva.setObjectName("primaryButton")
        self.btn_salva.clicked.connect(self.salva_progetto)
        name_layout.addWidget(self.btn_salva)

        save_layout.addLayout(name_layout)

        # Checkbox per aggiungere timestamp (allineata con il campo nome)
        timestamp_layout = QHBoxLayout()
        timestamp_spacing = QLabel("")  # Label vuota per allineamento
        timestamp_spacing.setFixedWidth(50)
        timestamp_layout.addWidget(timestamp_spacing)
        self.chk_add_timestamp = QCheckBox(self.tr("Aggiungi timestamp al nome (es: progetto_YYYYMMDDHHmmss)"))
        self.chk_add_timestamp.setChecked(QSettings().value('gpkg_project_manager/add_timestamp', False, type=bool))
        self.chk_add_timestamp.stateChanged.connect(self.on_timestamp_changed)
        timestamp_layout.addWidget(self.chk_add_timestamp)
        timestamp_layout.addStretch()
        save_layout.addLayout(timestamp_layout)

        # Checkbox per aggiungere versione (allineata con il campo nome)
        version_layout = QHBoxLayout()
        version_spacing = QLabel("")  # Label vuota per allineamento
        version_spacing.setFixedWidth(50)
        version_layout.addWidget(version_spacing)
        self.chk_add_version = QCheckBox(self.tr("Aggiungi versione incrementale (es: progetto_v01, _v02, ...)"))
        self.chk_add_version.setChecked(QSettings().value('gpkg_project_manager/add_version', False, type=bool))
        self.chk_add_version.stateChanged.connect(self.on_version_changed)
        version_layout.addWidget(self.chk_add_version)
        version_layout.addStretch()
        save_layout.addLayout(version_layout)

        layout.addWidget(save_group)

        # === SEZIONE PROGETTI ===
        progetti_group = QGroupBox(self.tr("  📋  Progetti nel GeoPackage"))
        progetti_layout = QVBoxLayout(progetti_group)
        progetti_layout.setSpacing(12)

        self.lista_progetti = QListWidget()
        self.lista_progetti.setMinimumHeight(180)
        self.lista_progetti.setAlternatingRowColors(False)
        self.lista_progetti.setSelectionMode(SingleSelection)
        self.lista_progetti.itemDoubleClicked.connect(self.carica_progetto)
        self.lista_progetti.setContextMenuPolicy(CustomContextMenu)
        self.lista_progetti.customContextMenuRequested.connect(self.mostra_menu_contestuale)
        self.lista_progetti.setMouseTracking(True)
        self.lista_progetti.viewport().installEventFilter(self)
        progetti_layout.addWidget(self.lista_progetti)

        # Pulsanti azioni - Tutti in una riga
        btn_row = QHBoxLayout()
        btn_row.setSpacing(6)

        self.btn_carica = QPushButton(self.tr("📂 Carica"))
        self.btn_carica.setObjectName("successButton")
        self.btn_carica.clicked.connect(self.carica_progetto)
        btn_row.addWidget(self.btn_carica)

        self.btn_sovrascrivi = QPushButton(self.tr("⟳ Sovrascrivi"))
        self.btn_sovrascrivi.clicked.connect(self.sovrascrivi_progetto)
        btn_row.addWidget(self.btn_sovrascrivi)

        self.btn_elimina = QPushButton(self.tr("🗑️ Elimina"))
        self.btn_elimina.setObjectName("dangerButton")
        self.btn_elimina.clicked.connect(self.elimina_progetto)
        btn_row.addWidget(self.btn_elimina)

        self.btn_rinomina = QPushButton(self.tr("✏️ Rinomina"))
        self.btn_rinomina.setObjectName("secondaryButton")
        self.btn_rinomina.clicked.connect(self.rinomina_progetto)
        btn_row.addWidget(self.btn_rinomina)

        self.btn_duplica = QPushButton(self.tr("📋 Duplica"))
        self.btn_duplica.setObjectName("secondaryButton")
        self.btn_duplica.clicked.connect(self.duplica_progetto)
        btn_row.addWidget(self.btn_duplica)

        # Menu esportazione
        self.btn_esporta = QPushButton(self.tr("📤 Esporta ▾"))
        self.btn_esporta.setObjectName("secondaryButton")

        export_menu = QMenu(self.btn_esporta)
        export_menu.addAction(self.tr("📄  Esporta come QGS"), self.esporta_qgs)
        export_menu.addAction(self.tr("📦  Esporta come QGZ"), self.esporta_qgz)
        self.btn_esporta.setMenu(export_menu)
        btn_row.addWidget(self.btn_esporta)

        progetti_layout.addLayout(btn_row)

        layout.addWidget(progetti_group)

        # === TIP ===
        tip_label = QLabel(self.tr("💡 Doppio clic per caricare • Clic destro per menu contestuale"))
        tip_label.setObjectName("tipLabel")
        tip_label.setAlignment(AlignCenter)
        layout.addWidget(tip_label)

        # === FOOTER ===
        layout.addStretch()

        separator = QFrame()
        separator.setObjectName("separator")
        separator.setFrameShape(HLine)
        layout.addWidget(separator)

        footer_layout = QHBoxLayout()

        version_label = QLabel(self.tr("v3.3 • Qt5/Qt6 Compatible"))
        version_label.setObjectName("tipLabel")
        footer_layout.addWidget(version_label)

        footer_layout.addStretch()

        # Help button
        btn_help = QPushButton("📖 " + self.tr("Aiuto / Help"))
        btn_help.setFixedWidth(140)
        btn_help.setToolTip(self.tr("Apri la guida online / Open online guide"))
        btn_help.clicked.connect(self.open_help)
        footer_layout.addWidget(btn_help)

        footer_layout.addSpacing(10)

        # Language selector
        self.language_combo = QComboBox()
        self.language_combo.addItem("🇮🇹 Italiano", "it")
        self.language_combo.addItem("🇬🇧 English", "en")
        self.language_combo.setFixedWidth(140)
        self.language_combo.setToolTip(self.tr("Select language / Seleziona lingua"))

        # Set current language
        current_lang = QSettings().value('gpkg_project_manager/language', None)
        if current_lang:
            index = self.language_combo.findData(current_lang)
            if index >= 0:
                self.language_combo.setCurrentIndex(index)

        self.language_combo.currentIndexChanged.connect(self.on_language_changed)
        footer_layout.addWidget(self.language_combo)

        footer_layout.addSpacing(10)

        self.btn_chiudi = QPushButton(self.tr("Chiudi"))
        self.btn_chiudi.setFixedWidth(100)
        self.btn_chiudi.clicked.connect(self.close)
        footer_layout.addWidget(self.btn_chiudi)

        layout.addLayout(footer_layout)

        self.imposta_nome_progetto_default()

    def mostra_menu_contestuale(self, position):
        """Mostra il menu contestuale."""
        item = self.lista_progetti.itemAt(position)
        if not item:
            return

        menu = QMenu()
        menu.setStyleSheet(MODERN_STYLE)

        menu.addAction(self.tr("📂  Carica"), self.carica_progetto)
        menu.addAction(self.tr("⟳  Sovrascrivi"), self.sovrascrivi_progetto)
        menu.addSeparator()
        menu.addAction(self.tr("✏️  Rinomina"), self.rinomina_progetto)
        menu.addAction(self.tr("📋  Duplica"), self.duplica_progetto)
        menu.addSeparator()
        menu.addAction(self.tr("📄  Esporta come QGS"), self.esporta_qgs)
        menu.addAction(self.tr("📦  Esporta come QGZ"), self.esporta_qgz)
        menu.addSeparator()
        menu.addAction(self.tr("🗑️  Elimina"), self.elimina_progetto)

        menu.exec(self.lista_progetti.mapToGlobal(position))

    def imposta_nome_progetto_default(self):
        """Imposta il nome del progetto corrente come default."""
        project = QgsProject.instance()
        nome = project.baseName()
        self.txt_nome_progetto.setText(nome if nome else self.tr("progetto_qgis"))

    def trova_geopackage_automatico(self):
        """Trova tutti i GeoPackage usati nel progetto corrente."""
        # Salva il GeoPackage corrente (normalizza il percorso)
        current_gpkg = None
        if self.gpkg_path and not self.gpkg_path.startswith("--"):
            current_gpkg = os.path.normpath(os.path.abspath(self.gpkg_path))
        
        self.gpkg_combo.clear()
        project = QgsProject.instance()
        geopackages = {}  # Usa dict per mappare percorsi normalizzati -> percorsi originali

        for layer in project.mapLayers().values():
            source = layer.source()
            if '.gpkg' in source.lower():
                gpkg_path = source.split('|')[0].strip() if '|' in source else source.strip()
                if os.path.exists(gpkg_path):
                    normalized = os.path.normpath(os.path.abspath(gpkg_path))
                    geopackages[normalized] = gpkg_path
        
        # Aggiungi il GeoPackage corrente se esiste e non è già nella lista
        if current_gpkg and os.path.exists(current_gpkg):
            if current_gpkg not in geopackages:
                geopackages[current_gpkg] = self.gpkg_path

        if geopackages:
            # Ordina per percorso normalizzato e aggiungi usando i percorsi originali
            for normalized in sorted(geopackages.keys()):
                self.gpkg_combo.addItem(geopackages[normalized])
            
            # Ripristina la selezione corrente se presente
            if current_gpkg and current_gpkg in geopackages:
                original_path = geopackages[current_gpkg]
                index = self.gpkg_combo.findText(original_path)
                if index >= 0:
                    self.gpkg_combo.setCurrentIndex(index)
                    self.gpkg_path = original_path
                else:
                    self.gpkg_path = self.gpkg_combo.currentText()
            else:
                self.gpkg_path = self.gpkg_combo.currentText()
                
            self.aggiorna_lista_progetti()
        else:
            self.gpkg_combo.addItem(self.tr("-- Nessun GeoPackage trovato nel progetto --"))
            self.gpkg_path = None

    def clear_gui(self):
        """Pulisce la GUI all'avvio del plugin."""
        # Imposta valore di default per il nome progetto
        self.txt_nome_progetto.setText("progetto")
        # Pulisci lista progetti
        self.lista_progetti.clear()
        # Reset info GeoPackage
        self.gpkg_info_label.setText(self.tr("ℹ️ Info: --"))

    def on_gpkg_changed(self, text):
        """Gestisce il cambio di GeoPackage selezionato."""
        if text and not text.startswith("--"):
            self.gpkg_path = text
            self.aggiorna_lista_progetti()
        else:
            self.gpkg_path = None
            self.lista_progetti.clear()
            self.aggiorna_info_gpkg()

    def sfoglia_geopackage(self):
        """Apre un dialog per selezionare un GeoPackage."""
        file_path, _ = QFileDialog.getOpenFileName(
            self, self.tr("Seleziona GeoPackage"), "",
            self.tr("GeoPackage (*.gpkg);;Tutti i file (*.*)")
        )

        if file_path:
            index = self.gpkg_combo.findText(file_path)
            if index == -1:
                if self.gpkg_combo.currentText().startswith("--"):
                    self.gpkg_combo.clear()
                self.gpkg_combo.addItem(file_path)
                self.gpkg_combo.setCurrentText(file_path)
            else:
                self.gpkg_combo.setCurrentIndex(index)

    def aggiorna_lista_progetti(self):
        """Aggiorna la lista dei progetti salvati nel GeoPackage."""
        self.lista_progetti.clear()

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
                cursor.execute("SELECT name FROM qgis_projects ORDER BY name")
                for row in cursor.fetchall():
                    item = QListWidgetItem(f"  📋  {row[0]}")
                    item.setData(UserRole, row[0])
                    self.lista_progetti.addItem(item)

            conn.close()

        except Exception as e:
            self.mostra_errore(self.tr("Errore"), self.tr("Errore nella lettura dei progetti:\n{}").format(str(e)))

        # Aggiorna info GeoPackage
        self.aggiorna_info_gpkg()

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
            num_progetti = self.lista_progetti.count()

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

    def crea_tabella_metadata(self, conn):
        """Crea la tabella dei metadati se non esiste e la registra in gpkg_contents."""
        try:
            cursor = conn.cursor()
            
            # Crea la tabella dei metadati
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS qgis_projects_metadata (
                    project_name TEXT PRIMARY KEY,
                    created_date TEXT,
                    modified_date TEXT,
                    size_bytes INTEGER,
                    layer_count INTEGER,
                    vector_count INTEGER,
                    raster_count INTEGER,
                    table_count INTEGER,
                    crs_epsg TEXT
                )
            """)
            
            # Aggiunge colonne se non esistono (per retrocompatibilità)
            try:
                cursor.execute("ALTER TABLE qgis_projects_metadata ADD COLUMN crs_epsg TEXT")
            except:
                pass  # Colonna già esistente
            
            try:
                cursor.execute("ALTER TABLE qgis_projects_metadata ADD COLUMN table_count INTEGER")
            except:
                pass  # Colonna già esistente
            
            # Registra la tabella in gpkg_contents se non esiste già
            cursor.execute("""
                INSERT OR IGNORE INTO gpkg_contents 
                (table_name, data_type, identifier, description, last_change, srs_id)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                'qgis_projects_metadata',
                'attributes',
                'qgis_projects_metadata',
                'QGIS Projects Metadata - Extended information about QGIS projects stored in GeoPackage',
                datetime.now().strftime('%Y-%m-%dT%H:%M:%S.000Z'),
                0  # srs_id 0 per tabelle non spaziali
            ))
            
            conn.commit()
        except Exception as e:
            pass  # Tabella già esistente o errore non critico

    def estrai_metadati_progetto(self, content):
        """Estrae metadati automatici dal contenuto del progetto."""
        metadata = {
            'layer_count': 0,
            'vector_count': 0,
            'raster_count': 0,
            'table_count': 0,
            'size_bytes': len(content) if content else 0,
            'crs_epsg': None
        }

        try:
            # Decomprimi il contenuto del progetto
            files_content, is_compressed, was_hex = self._decomprimi_progetto(content)

            # Trova il contenuto XML principale
            qgs_content = None
            for file_name, file_content in files_content.items():
                if file_name.endswith('.qgs') or file_name == 'content' or not file_name.endswith('.db'):
                    try:
                        qgs_content = file_content.decode('utf-8')
                        break
                    except:
                        continue

            if qgs_content:
                # Conta i layer usando regex semplice (più veloce di XML parsing completo)
                import re
                
                # Conta layer vettoriali (con geometria)
                # Pattern per trovare layer vettoriali con geometria (Point, Line, Polygon, etc.)
                vector_with_geom = r'<maplayer[^>]*type="vector"[^>]*geometry="(?!No Geometry)([^"]+)"'
                metadata['vector_count'] = len(re.findall(vector_with_geom, qgs_content, re.DOTALL))
                
                # Conta layer raster
                raster_pattern = r'<maplayer[^>]*type="raster"'
                metadata['raster_count'] = len(re.findall(raster_pattern, qgs_content))
                
                # Conta tabelle (layer vettoriali senza geometria, escluse tabelle di sistema)
                # Le tabelle hanno geometry="No Geometry" o nessun attributo geometry
                table_pattern = r'<maplayer[^>]*type="vector"[^>]*geometry="No Geometry"'
                all_tables = re.findall(table_pattern, qgs_content, re.DOTALL)
                
                # Filtra tabelle di sistema (qgis_, sqlite_, gpkg_)
                # Cerca il nome della tabella per ogni match
                table_count = 0
                for match in re.finditer(table_pattern, qgs_content, re.DOTALL):
                    # Trova il datasource dopo questo match
                    start_pos = match.start()
                    datasource_match = re.search(r'<datasource>([^<]+)</datasource>', qgs_content[start_pos:start_pos+2000])
                    if datasource_match:
                        datasource = datasource_match.group(1)
                        # Controlla se NON è una tabella di sistema
                        if not any(sys_prefix in datasource.lower() for sys_prefix in ['qgis_', 'sqlite_', 'gpkg_', 'rtree_']):
                            table_count += 1
                    else:
                        # Se non troviamo datasource, contiamo comunque
                        table_count += 1
                
                metadata['table_count'] = table_count
                metadata['layer_count'] = metadata['vector_count'] + metadata['raster_count'] + metadata['table_count']
                
                # Estrai EPSG dal progetto - Prova diversi pattern
                # Pattern 1: <projectCrs><spatialrefsys>...<authid>EPSG:XXXX</authid>
                epsg_match = re.search(r'<projectCrs>.*?<authid>(EPSG:\d+)</authid>', qgs_content, re.DOTALL)
                if epsg_match:
                    metadata['crs_epsg'] = epsg_match.group(1)
                else:
                    # Pattern 2: <destinationsrs><spatialrefsys>...<authid>EPSG:XXXX</authid>
                    epsg_match = re.search(r'<destinationsrs>.*?<authid>(EPSG:\d+)</authid>', qgs_content, re.DOTALL)
                    if epsg_match:
                        metadata['crs_epsg'] = epsg_match.group(1)
                    else:
                        # Pattern 3: Qualsiasi <authid>EPSG:XXXX</authid> (prima occorrenza)
                        epsg_match = re.search(r'<authid>(EPSG:\d+)</authid>', qgs_content)
                        if epsg_match:
                            metadata['crs_epsg'] = epsg_match.group(1)
                        else:
                            # Pattern 4: <proj4>...+init=epsg:XXXX...
                            epsg_match = re.search(r'\+init=epsg:(\d+)', qgs_content, re.IGNORECASE)
                            if epsg_match:
                                metadata['crs_epsg'] = f"EPSG:{epsg_match.group(1)}"

        except Exception as e:
            # Se parsing fallisce, ritorna metadati base
            pass

        return metadata

    def salva_metadati_progetto(self, conn, project_name, content, is_new=True, update_modified_date=True, project_crs=None):
        """Salva o aggiorna i metadati del progetto.
        
        Args:
            conn: Connessione SQLite
            project_name: Nome del progetto
            content: Contenuto XML del progetto
            is_new: True se è un nuovo progetto
            update_modified_date: True per aggiornare la data di modifica (default), 
                                  False per mantenerla invariata (utile per aggiornamento metadati)
            project_crs: CRS del progetto (opzionale, se fornito ha priorità sull'estrazione dal XML)
        """
        try:
            # Assicurati che la tabella esista
            self.crea_tabella_metadata(conn)

            # Estrai metadati dal progetto
            metadata = self.estrai_metadati_progetto(content)
            
            # Se è stato fornito il CRS, usa quello (ha priorità)
            if project_crs:
                metadata['crs_epsg'] = project_crs

            cursor = conn.cursor()
            now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            if is_new:
                # Nuovo progetto: created_date = modified_date
                cursor.execute("""
                    INSERT OR REPLACE INTO qgis_projects_metadata
                    (project_name, created_date, modified_date, size_bytes, layer_count, vector_count, raster_count, table_count, crs_epsg)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (project_name, now, now, metadata['size_bytes'], metadata['layer_count'],
                      metadata['vector_count'], metadata['raster_count'], metadata['table_count'], metadata['crs_epsg']))
            else:
                # Aggiornamento: mantieni created_date, aggiorna modified_date solo se richiesto
                if update_modified_date:
                    # Progetto modificato realmente: aggiorna modified_date
                    cursor.execute("""
                        INSERT OR REPLACE INTO qgis_projects_metadata
                        (project_name, created_date, modified_date, size_bytes, layer_count, vector_count, raster_count, table_count, crs_epsg)
                        VALUES (
                            ?,
                            COALESCE((SELECT created_date FROM qgis_projects_metadata WHERE project_name = ?), ?),
                            ?,
                            ?, ?, ?, ?, ?, ?
                        )
                    """, (project_name, project_name, now, now, metadata['size_bytes'],
                          metadata['layer_count'], metadata['vector_count'], metadata['raster_count'], metadata['table_count'], metadata['crs_epsg']))
                else:
                    # Solo aggiornamento metadati: mantieni modified_date esistente
                    cursor.execute("""
                        INSERT OR REPLACE INTO qgis_projects_metadata
                        (project_name, created_date, modified_date, size_bytes, layer_count, vector_count, raster_count, table_count, crs_epsg)
                        VALUES (
                            ?,
                            COALESCE((SELECT created_date FROM qgis_projects_metadata WHERE project_name = ?), ?),
                            COALESCE((SELECT modified_date FROM qgis_projects_metadata WHERE project_name = ?), ?),
                            ?, ?, ?, ?, ?, ?
                        )
                    """, (project_name, project_name, now, project_name, now, metadata['size_bytes'],
                          metadata['layer_count'], metadata['vector_count'], metadata['raster_count'], metadata['table_count'], metadata['crs_epsg']))

            conn.commit()
        except Exception as e:
            pass  # Errore non critico

    def leggi_metadati_progetto(self, project_name):
        """Legge i metadati di un progetto."""
        if not self.gpkg_path or not os.path.exists(self.gpkg_path):
            return None

        try:
            conn = sqlite3.connect(self.gpkg_path)
            self.crea_tabella_metadata(conn)

            cursor = conn.cursor()
            cursor.execute("""
                SELECT created_date, modified_date, size_bytes, layer_count, vector_count, raster_count, table_count, crs_epsg
                FROM qgis_projects_metadata
                WHERE project_name = ?
            """, (project_name,))

            result = cursor.fetchone()
            conn.close()

            if result:
                return {
                    'created_date': result[0],
                    'modified_date': result[1],
                    'size_bytes': result[2],
                    'layer_count': result[3],
                    'vector_count': result[4],
                    'raster_count': result[5],
                    'table_count': result[6] if len(result) > 6 else 0,
                    'crs_epsg': result[7] if len(result) > 7 else None
                }
        except Exception as e:
            pass

        return None

    def eventFilter(self, obj, event):
        """Event filter per tooltip personalizzati nella lista progetti."""
        if obj == self.lista_progetti.viewport() and event.type() == EventToolTip:
            # Trova l'item sotto il mouse
            pos = event.pos()
            item = self.lista_progetti.itemAt(pos)

            if item:
                project_name = item.data(UserRole)
                if project_name:
                    # Leggi metadati
                    metadata = self.leggi_metadati_progetto(project_name)

                    if metadata:
                        # Formatta dimensione
                        size_bytes = metadata.get('size_bytes', 0)
                        if size_bytes < 1024:
                            size_str = f"{size_bytes} B"
                        elif size_bytes < 1024 * 1024:
                            size_str = f"{size_bytes / 1024:.1f} KB"
                        else:
                            size_str = f"{size_bytes / (1024 * 1024):.1f} MB"

                        # Formatta date
                        created = metadata.get('created_date', 'N/A')
                        if created and created != 'N/A':
                            try:
                                from datetime import datetime
                                dt = datetime.strptime(created, '%Y-%m-%d %H:%M:%S')
                                created = dt.strftime('%d/%m/%Y %H:%M')
                            except:
                                pass

                        modified = metadata.get('modified_date', 'N/A')
                        if modified and modified != 'N/A':
                            try:
                                from datetime import datetime
                                dt = datetime.strptime(modified, '%Y-%m-%d %H:%M:%S')
                                modified = dt.strftime('%d/%m/%Y %H:%M')
                            except:
                                pass

                        # Costruisci info layer
                        layer_count = metadata.get('layer_count', 0)
                        vector_count = metadata.get('vector_count', 0)
                        raster_count = metadata.get('raster_count', 0)

                        layer_info = f"{layer_count}"
                        if vector_count > 0 or raster_count > 0:
                            layer_info += f" ({vector_count}v, {raster_count}r)"

                        # Crea tooltip HTML
                        tooltip_html = f"""
                        <div style='background-color: #f8f9fa; padding: 8px; border: 1px solid #dee2e6; border-radius: 4px;'>
                            <div style='background-color: #3b82f6; color: white; padding: 6px; margin: -8px -8px 8px -8px; border-radius: 4px 4px 0 0; font-weight: bold;'>
                                📊 {project_name}
                            </div>
                            <table style='border-collapse: collapse; width: 100%;'>
                                <tr><td style='padding: 3px 8px 3px 0;'><b>📅 {self.tr("Creato")}:</b></td><td style='padding: 3px 0;'>{created}</td></tr>
                                <tr><td style='padding: 3px 8px 3px 0;'><b>🔄 {self.tr("Modificato")}:</b></td><td style='padding: 3px 0;'>{modified}</td></tr>
                                <tr><td style='padding: 3px 8px 3px 0;'><b>💾 {self.tr("Dimensione")}:</b></td><td style='padding: 3px 0;'>{size_str}</td></tr>
                                <tr><td style='padding: 3px 8px 3px 0;'><b>🗂️ {self.tr("Layer")}:</b></td><td style='padding: 3px 0;'>{layer_info}</td></tr>
                            </table>
                        </div>
                        """

                        QToolTip.showText(event.globalPos(), tooltip_html, self.lista_progetti)
                        return True
                    else:
                        # Fallback: leggi almeno la dimensione del progetto direttamente dal database
                        try:
                            conn = sqlite3.connect(self.gpkg_path)
                            cursor = conn.cursor()
                            cursor.execute("SELECT length(content) FROM qgis_projects WHERE name = ?", (project_name,))
                            result = cursor.fetchone()
                            conn.close()

                            if result and result[0]:
                                size_bytes = result[0]
                                if size_bytes < 1024:
                                    size_str = f"{size_bytes} B"
                                elif size_bytes < 1024 * 1024:
                                    size_str = f"{size_bytes / 1024:.1f} KB"
                                else:
                                    size_str = f"{size_bytes / (1024 * 1024):.1f} MB"

                                tooltip_simple = f"""
                                <div style='background-color: #f8f9fa; padding: 8px; border: 1px solid #dee2e6; border-radius: 4px;'>
                                    <div style='background-color: #6b7280; color: white; padding: 6px; margin: -8px -8px 8px -8px; border-radius: 4px 4px 0 0; font-weight: bold;'>
                                        📋 {project_name}
                                    </div>
                                    <div style='padding: 5px 0;'>
                                        <b>💾 {self.tr("Dimensione")}:</b> {size_str}
                                    </div>
                                    <div style='padding: 5px 0; font-size: 10px; color: #6b7280; font-style: italic;'>
                                        {self.tr("Dettagli completi disponibili dopo il primo salvataggio")}
                                    </div>
                                </div>
                                """
                            else:
                                tooltip_simple = f"<b>📋 {project_name}</b>"
                        except:
                            tooltip_simple = f"<b>📋 {project_name}</b>"

                        QToolTip.showText(event.globalPos(), tooltip_simple, self.lista_progetti)
                        return True

        return super().eventFilter(obj, event)

    def pulisci_nome(self, nome):
        """Pulisce il nome del progetto."""
        return "".join(c for c in nome if c.isalnum() or c in ('_', '-', ' '))

    def get_lista_nomi_progetti(self):
        """Restituisce la lista dei nomi dei progetti."""
        return [self.lista_progetti.item(i).data(UserRole)
                for i in range(self.lista_progetti.count())]

    def get_progetto_selezionato(self):
        """Restituisce il nome del progetto selezionato."""
        item = self.lista_progetti.currentItem()
        return item.data(UserRole) if item else None

    def mostra_info(self, titolo, messaggio):
        """Mostra un messaggio informativo."""
        msg = QMessageBox(self)
        msg.setIcon(MsgBoxInformation)
        msg.setWindowTitle(titolo)
        msg.setText(messaggio)
        msg.setStyleSheet(MODERN_STYLE)
        msg.exec()

    def mostra_errore(self, titolo, messaggio):
        """Mostra un messaggio di errore."""
        msg = QMessageBox(self)
        msg.setIcon(MsgBoxCritical)
        msg.setWindowTitle(titolo)
        msg.setText(messaggio)
        msg.setStyleSheet(MODERN_STYLE)
        msg.exec()

    def mostra_conferma(self, titolo, messaggio):
        """Mostra un dialog di conferma."""
        msg = QMessageBox(self)
        msg.setIcon(MsgBoxQuestion)
        msg.setWindowTitle(titolo)
        msg.setText(messaggio)
        msg.setStandardButtons(MsgBoxYes | MsgBoxNo)
        msg.setDefaultButton(MsgBoxNo)
        msg.setStyleSheet(MODERN_STYLE)
        return msg.exec() == MsgBoxYes

    def on_language_changed(self, index):
        """Handle language change from combo box.

        Args:
            index: Index of selected language
        """
        if index < 0:
            return

        new_locale = self.language_combo.currentData()
        current_locale = QSettings().value('gpkg_project_manager/language', None)

        # Only change if different
        if new_locale != current_locale:
            if self.plugin:
                # Call plugin method to change language
                self.plugin.change_language(new_locale)

                # Show message and reopen dialog
                msg = QMessageBox(self)
                msg.setIcon(MsgBoxInformation)
                msg.setWindowTitle(self.tr("Language Changed / Lingua Cambiata"))
                msg.setText(self.tr("Language has been changed.\nThe dialog will be reloaded.\n\nLa lingua è stata cambiata.\nIl dialog verrà ricaricato."))
                msg.setStyleSheet(MODERN_STYLE)
                msg.exec()

                # Close and reopen
                self.accept()  # Close with accept to trigger recreation

                # Reopen plugin
                QTimer.singleShot(100, self.plugin.run)

    def open_help(self):
        """Open online guide in default browser."""
        url = QUrl("https://github.com/pigreco/gpkg_project_manager/wiki")
        QDesktopServices.openUrl(url)

    def on_timestamp_changed(self, state):
        """Handle timestamp checkbox state change."""
        settings = QSettings()
        settings.setValue('gpkg_project_manager/add_timestamp', self.chk_add_timestamp.isChecked())

    def on_version_changed(self, state):
        """Handle version checkbox state change."""
        settings = QSettings()
        settings.setValue('gpkg_project_manager/add_version', self.chk_add_version.isChecked())

    def on_clone_version_changed(self, state):
        """Handle clone version checkbox state change."""
        settings = QSettings()
        settings.setValue('gpkg_project_manager/clone_add_version', self.chk_clone_add_version.isChecked())

    def salva_progetto(self, force_overwrite=False):
        """Salva il progetto corrente nel GeoPackage.
        
        Args:
            force_overwrite: Se True, forza la sovrascrittura senza chiedere conferma
                           e imposta is_new=False per aggiornare la data di modifica
        """
        if not self.gpkg_path:
            self.mostra_errore(self.tr("Attenzione"), self.tr("Seleziona prima un GeoPackage."))
            return

        nome_progetto = self.pulisci_nome(self.txt_nome_progetto.text().strip())
        if not nome_progetto:
            self.mostra_errore(self.tr("Attenzione"), self.tr("Inserisci un nome per il progetto."))
            return

        # Rimuovi timestamp e versione esistenti per ottenere il nome base
        nome_base = nome_progetto
        # Rimuovi timestamp se presente (pattern: _YYYYMMDDHHmmss)
        nome_base = re.sub(r'_\d{14}$', '', nome_base)
        # Rimuovi versione se presente (pattern: _vNN)
        nome_base = re.sub(r'_v\d{2}$', '', nome_base)

        # Aggiungi versione incrementale se l'opzione è attivata
        if self.chk_add_version.isChecked():
            # Cerca la versione più alta esistente
            progetti_esistenti = self.get_lista_nomi_progetti()
            max_version = 0
            # Pattern per trovare progetti con lo stesso nome base e versione
            # Supporta anche timestamp opzionale alla fine
            pattern = re.compile(rf'^{re.escape(nome_base)}_v(\d{{2}})(?:_\d{{14}})?$')

            for progetto in progetti_esistenti:
                match = pattern.match(progetto)
                if match:
                    version_num = int(match.group(1))
                    max_version = max(max_version, version_num)

            # Incrementa la versione
            next_version = max_version + 1
            if next_version > 99:
                self.mostra_errore(self.tr("Errore"), self.tr("Raggiunto il limite massimo di versioni (v99)."))
                return

            nome_progetto = f"{nome_base}_v{next_version:02d}"
        else:
            nome_progetto = nome_base

        # Aggiungi timestamp se l'opzione è attivata
        if self.chk_add_timestamp.isChecked():
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            nome_progetto = f"{nome_progetto}_{timestamp}"

        # Verifica se il progetto esiste già PRIMA del salvataggio
        progetti_esistenti = self.get_lista_nomi_progetti()
        is_new = nome_progetto not in progetti_esistenti

        # Se force_overwrite è True, tratta sempre come esistente (is_new=False)
        if force_overwrite:
            is_new = False
        elif not is_new:
            # Progetto esiste e non è force_overwrite: chiedi conferma
            if not self.mostra_conferma(
                self.tr("Progetto Esistente"),
                self.tr("Il progetto '%1' esiste già.\nVuoi sovrascriverlo?").replace('%1', nome_progetto)
            ):
                return

        try:
            project = QgsProject.instance()
            
            # Estrai il CRS del progetto PRIMA del salvataggio
            project_crs = None
            try:
                crs = project.crs()
                if crs.isValid():
                    auth_id = crs.authid()
                    if auth_id:
                        project_crs = auth_id
            except:
                pass
            
            uri = f"geopackage:{self.gpkg_path}?projectName={nome_progetto}"

            if project.write(uri):
                # Salva metadati del progetto
                try:
                    conn = sqlite3.connect(self.gpkg_path)
                    # Assicurati che la tabella metadata esista
                    self.crea_tabella_metadata(conn)
                    cursor = conn.cursor()
                    cursor.execute("SELECT content FROM qgis_projects WHERE name = ?", (nome_progetto,))
                    result = cursor.fetchone()
                    if result:
                        content = result[0]
                        # Passa il CRS estratto al metodo di salvataggio
                        self.salva_metadati_progetto(conn, nome_progetto, content, is_new=is_new, project_crs=project_crs)
                    conn.close()
                except Exception as e:
                    pass  # Errore non critico

                self.mostra_info(self.tr("Successo"), self.tr("Progetto '%1' salvato!").replace('%1', nome_progetto))
                self.aggiorna_lista_progetti()
                iface.messageBar().pushMessage(
                    self.tr("Successo"), self.tr("Progetto salvato in: %1").replace('%1', os.path.basename(self.gpkg_path)),
                    level=Qgis.Success, duration=3
                )
            else:
                self.mostra_errore(self.tr("Errore"), self.tr("Impossibile salvare il progetto."))

        except Exception as e:
            self.mostra_errore(self.tr("Errore"), self.tr("Errore durante il salvataggio:\n{}").format(str(e)))

    def carica_progetto(self, item=None):
        """Carica il progetto selezionato dal GeoPackage."""
        nome_progetto = self.get_progetto_selezionato()
        if not nome_progetto:
            self.mostra_errore(self.tr("Attenzione"), self.tr("Seleziona un progetto dalla lista."))
            return

        project = QgsProject.instance()
        if project.isDirty():
            if not self.mostra_conferma(
                self.tr("Modifiche non salvate"),
                self.tr("Il progetto corrente ha modifiche non salvate.\nVuoi continuare?")
            ):
                return

        try:
            uri = f"geopackage:{self.gpkg_path}?projectName={nome_progetto}"

            if project.read(uri):
                self.mostra_info(self.tr("Successo"), self.tr("Progetto '%1' caricato!").replace('%1', nome_progetto))
                self.imposta_nome_progetto_default()
                iface.messageBar().pushMessage(
                    self.tr("Successo"), self.tr("Progetto '%1' caricato").replace('%1', nome_progetto),
                    level=Qgis.Success, duration=3
                )
            else:
                self.mostra_errore(self.tr("Errore"), self.tr("Impossibile caricare il progetto."))

        except Exception as e:
            self.mostra_errore(self.tr("Errore"), self.tr("Errore durante il caricamento:\n{}").format(str(e)))

    def sovrascrivi_progetto(self):
        """Sovrascrive il progetto selezionato."""
        nome_progetto = self.get_progetto_selezionato()
        if not nome_progetto:
            self.mostra_errore(self.tr("Attenzione"), self.tr("Seleziona un progetto dalla lista."))
            return

        if self.mostra_conferma(
            self.tr("Conferma Sovrascrittura"),
            self.tr("Sovrascrivere il progetto '%1'?").replace('%1', nome_progetto)
        ):
            self.txt_nome_progetto.setText(nome_progetto)
            # Passa force_overwrite=True per forzare is_new=False e aggiornare modified_date
            self.salva_progetto(force_overwrite=True)

    def elimina_progetto(self):
        """Elimina il progetto selezionato."""
        nome_progetto = self.get_progetto_selezionato()
        if not nome_progetto:
            self.mostra_errore(self.tr("Attenzione"), self.tr("Seleziona un progetto dalla lista."))
            return

        if not self.mostra_conferma(
            self.tr("Conferma Eliminazione"),
            self.tr("Eliminare definitivamente '%1'?\nQuesta azione non può essere annullata.").replace('%1', nome_progetto)
        ):
            return

        try:
            conn = sqlite3.connect(self.gpkg_path)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM qgis_projects WHERE name = ?", (nome_progetto,))

            # Elimina anche i metadati
            try:
                cursor.execute("DELETE FROM qgis_projects_metadata WHERE project_name = ?", (nome_progetto,))
            except:
                pass  # Tabella potrebbe non esistere

            conn.commit()
            conn.close()

            self.mostra_info(self.tr("Successo"), self.tr("Progetto '%1' eliminato.").replace('%1', nome_progetto))
            self.aggiorna_lista_progetti()

        except Exception as e:
            self.mostra_errore(self.tr("Errore"), self.tr("Errore durante l'eliminazione:\n{}").format(str(e)))

    def rinomina_progetto(self):
        """Rinomina il progetto selezionato."""
        nome_progetto = self.get_progetto_selezionato()
        if not nome_progetto:
            self.mostra_errore(self.tr("Attenzione"), self.tr("Seleziona un progetto dalla lista."))
            return

        nuovo_nome, ok = QInputDialog.getText(
            self, self.tr("Rinomina Progetto"), self.tr("Nuovo nome:"),
            LineEditNormal, nome_progetto
        )

        if not ok or not nuovo_nome.strip():
            return

        nuovo_nome = self.pulisci_nome(nuovo_nome.strip())

        if nuovo_nome == nome_progetto:
            return

        if nuovo_nome in self.get_lista_nomi_progetti():
            self.mostra_errore(self.tr("Attenzione"), self.tr("Esiste già un progetto '%1'.").replace('%1', nuovo_nome))
            return

        try:
            conn = sqlite3.connect(self.gpkg_path)
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE qgis_projects SET name = ? WHERE name = ?",
                (nuovo_nome, nome_progetto)
            )

            # Aggiorna anche i metadati associati
            try:
                cursor.execute(
                    "UPDATE qgis_projects_metadata SET project_name = ? WHERE project_name = ?",
                    (nuovo_nome, nome_progetto)
                )
            except:
                pass  # Tabella potrebbe non esistere

            conn.commit()
            conn.close()

            self.mostra_info(self.tr("Successo"), self.tr("Progetto rinominato in '%1'.").replace('%1', nuovo_nome))
            self.aggiorna_lista_progetti()

        except Exception as e:
            self.mostra_errore(self.tr("Errore"), self.tr("Errore durante la rinomina:\n{}").format(str(e)))

    def duplica_progetto(self):
        """Duplica il progetto selezionato."""
        nome_progetto = self.get_progetto_selezionato()
        if not nome_progetto:
            self.mostra_errore(self.tr("Attenzione"), self.tr("Seleziona un progetto dalla lista."))
            return

        nome_suggerito = f"{nome_progetto}_copia"
        counter = 1
        nomi_esistenti = self.get_lista_nomi_progetti()
        while nome_suggerito in nomi_esistenti:
            counter += 1
            nome_suggerito = f"{nome_progetto}_copia{counter}"

        nuovo_nome, ok = QInputDialog.getText(
            self, self.tr("Duplica Progetto"), self.tr("Nome per la copia:"),
            LineEditNormal, nome_suggerito
        )

        if not ok or not nuovo_nome.strip():
            return

        nuovo_nome = self.pulisci_nome(nuovo_nome.strip())

        if nuovo_nome in nomi_esistenti:
            self.mostra_errore(self.tr("Attenzione"), self.tr("Esiste già un progetto '%1'.").replace('%1', nuovo_nome))
            return

        try:
            conn = sqlite3.connect(self.gpkg_path)
            cursor = conn.cursor()

            cursor.execute(
                "SELECT content FROM qgis_projects WHERE name = ?",
                (nome_progetto,)
            )
            row = cursor.fetchone()

            if row:
                cursor.execute(
                    "INSERT INTO qgis_projects (name, content) VALUES (?, ?)",
                    (nuovo_nome, row[0])
                )

                # Duplica anche i metadati
                self.salva_metadati_progetto(conn, nuovo_nome, row[0], is_new=True)

                conn.commit()
                self.mostra_info(self.tr("Successo"), self.tr("Progetto duplicato come '%1'.").replace('%1', nuovo_nome))
                self.aggiorna_lista_progetti()
            else:
                self.mostra_errore(self.tr("Errore"), self.tr("Progetto non trovato."))

            conn.close()

        except Exception as e:
            self.mostra_errore(self.tr("Errore"), self.tr("Errore durante la duplicazione:\n{}").format(str(e)))

    def esporta_qgs(self):
        """Esporta il progetto in formato QGS."""
        self._esporta_progetto("qgs")

    def esporta_qgz(self):
        """Esporta il progetto in formato QGZ."""
        self._esporta_progetto("qgz")

    def _esporta_progetto(self, formato):
        """Esporta il progetto nel formato specificato."""
        nome_progetto = self.get_progetto_selezionato()
        if not nome_progetto:
            self.mostra_errore(self.tr("Attenzione"), self.tr("Seleziona un progetto dalla lista."))
            return

        estensione = f".{formato}"
        filtro = self.tr("QGIS Project (*.%1)").replace('%1', formato)

        file_path, _ = QFileDialog.getSaveFileName(
            self, self.tr("Esporta come %1").replace('%1', formato.upper()),
            os.path.join(os.path.dirname(self.gpkg_path), nome_progetto + estensione),
            filtro
        )

        if not file_path:
            return

        if not file_path.lower().endswith(estensione):
            file_path += estensione

        try:
            project = QgsProject.instance()
            # Salva l'URI originale del progetto corrente
            progetto_corrente_uri = project.fileName()
            # Determina se il progetto corrente era caricato da un GeoPackage
            progetto_corrente_era_gpkg = progetto_corrente_uri.startswith('geopackage:') if progetto_corrente_uri else False

            uri = f"geopackage:{self.gpkg_path}?projectName={nome_progetto}"

            if project.read(uri):
                if project.write(file_path):
                    self.mostra_info(self.tr("Successo"), self.tr("Progetto esportato in:\n%1").replace('%1', file_path))

                    if not self.mostra_conferma(
                        self.tr("Aprire il progetto?"),
                        self.tr("Vuoi mantenere aperto il progetto esportato?")
                    ):
                        # Ripristina il progetto originale
                        if progetto_corrente_uri:
                            if progetto_corrente_era_gpkg:
                                # Era un progetto da GeoPackage, usa l'URI direttamente
                                project.read(progetto_corrente_uri)
                            else:
                                # Era un progetto da file, carica il file
                                project.read(progetto_corrente_uri)
                        else:
                            project.clear()
                else:
                    self.mostra_errore(self.tr("Errore"), self.tr("Impossibile esportare il progetto."))
            else:
                self.mostra_errore(self.tr("Errore"), self.tr("Impossibile leggere il progetto."))

        except Exception as e:
            self.mostra_errore(self.tr("Errore"), self.tr("Errore durante l'esportazione:\n{}").format(str(e)))

    def _aggiorna_percorsi_in_contenuto(self, content_str, vecchio_nome, nuovo_nome, vecchio_path, nuovo_path):
        """Aggiorna i percorsi nel contenuto XML del progetto."""
        nuovo_content = content_str
        modificato = False

        # PRIMA: Sostituzioni dirette più semplici e affidabili
        sostituzioni_dirette = [
            # Percorso relativo nel datasource: ./PI.gpkg -> ./PI_clone.gpkg
            (f'./{vecchio_nome}', f'./{nuovo_nome}'),
            (f'.\\{vecchio_nome}', f'.\\{nuovo_nome}'),
            # Solo nome file
            (vecchio_nome, nuovo_nome),
            # Percorso assoluto completo
            (vecchio_path, nuovo_path),
            (vecchio_path.replace('\\', '/'), nuovo_path.replace('\\', '/')),
            (vecchio_path.replace('/', '\\'), nuovo_path.replace('/', '\\')),
        ]

        for vecchio, nuovo in sostituzioni_dirette:
            if vecchio and nuovo and vecchio != nuovo and vecchio in nuovo_content:
                nuovo_content = nuovo_content.replace(vecchio, nuovo)
                modificato = True

        return nuovo_content, modificato

    def _hex_to_bytes(self, content):
        """Converte il contenuto da HEX string a bytes se necessario."""
        if isinstance(content, str):
            # È una stringa HEX
            try:
                return bytes.fromhex(content), True
            except ValueError:
                return content.encode('utf-8'), False
        elif isinstance(content, bytes):
            # Controlla se è una stringa HEX codificata come bytes
            try:
                hex_str = content.decode('utf-8')
                # Verifica se sembra HEX (solo caratteri 0-9, a-f)
                if all(c in '0123456789abcdefABCDEF' for c in hex_str[:100]):
                    return bytes.fromhex(hex_str), True
            except:
                pass
            return content, False
        return content, False

    def _bytes_to_hex(self, content_bytes):
        """Converte bytes in stringa HEX."""
        return content_bytes.hex()

    def _decomprimi_progetto(self, content):
        """Decomprime il contenuto del progetto QGIS (formato HEX + ZIP)."""
        import zipfile
        import io

        # Prima converti da HEX se necessario
        content_bytes, was_hex = self._hex_to_bytes(content)

        # Verifica se è un file ZIP (magic bytes: PK = 0x504B)
        if len(content_bytes) >= 4 and content_bytes[:4] == b'\x50\x4b\x03\x04':
            try:
                zip_buffer = io.BytesIO(content_bytes)
                files_content = {}

                with zipfile.ZipFile(zip_buffer, 'r') as zf:
                    for name in zf.namelist():
                        files_content[name] = zf.read(name)

                return files_content, True, was_hex
            except zipfile.BadZipFile:
                pass

        # Non è compresso, restituisci come singolo file
        return {'content': content_bytes}, False, was_hex

    def _comprimi_progetto(self, files_content, as_hex=False):
        """Ricomprime il contenuto del progetto QGIS in formato ZIP."""
        import zipfile
        import io

        zip_buffer = io.BytesIO()

        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zf:
            for name, content in files_content.items():
                zf.writestr(name, content)

        result = zip_buffer.getvalue()

        # Riconverti in HEX se era HEX originariamente
        if as_hex:
            return self._bytes_to_hex(result)

        return result

    def clona_geopackage(self):
        """Clona il GeoPackage aggiornando i percorsi nei progetti."""
        if not self.gpkg_path:
            self.mostra_errore(self.tr("Attenzione"), self.tr("Seleziona prima un GeoPackage."))
            return

        # Chiedi il percorso di destinazione
        nome_originale = os.path.basename(self.gpkg_path)
        nome_base = nome_originale.replace('.gpkg', '')

        # Determina il nome suggerito in base alle opzioni
        if self.chk_clone_add_version.isChecked():
            # Rimuovi versione esistente se presente (pattern: _vNN)
            nome_base_pulito = re.sub(r'_v\d{2}$', '', nome_base)

            # Cerca la versione più alta esistente nella directory di destinazione
            directory_destinazione = os.path.dirname(self.gpkg_path)
            max_version = 0

            # Cerca file esistenti con pattern versione
            if os.path.exists(directory_destinazione):
                pattern = re.compile(rf'^{re.escape(nome_base_pulito)}_v(\d{{2}})\.gpkg$')
                for filename in os.listdir(directory_destinazione):
                    match = pattern.match(filename)
                    if match:
                        version_num = int(match.group(1))
                        max_version = max(max_version, version_num)

            # Incrementa la versione
            next_version = max_version + 1
            if next_version > 99:
                self.mostra_errore(self.tr("Errore"), self.tr("Raggiunto il limite massimo di versioni (v99)."))
                return

            nome_suggerito = f"{nome_base_pulito}_v{next_version:02d}.gpkg"
        else:
            nome_suggerito = nome_originale.replace('.gpkg', '_clone.gpkg')

        file_path, _ = QFileDialog.getSaveFileName(
            self, self.tr("Salva Clone GeoPackage"),
            os.path.join(os.path.dirname(self.gpkg_path), nome_suggerito),
            self.tr("GeoPackage (*.gpkg)")
        )

        if not file_path:
            return

        if not file_path.lower().endswith('.gpkg'):
            file_path += '.gpkg'

        # Normalizza i percorsi
        file_path = os.path.normpath(file_path)

        if os.path.normpath(file_path) == os.path.normpath(self.gpkg_path):
            self.mostra_errore(self.tr("Errore"), self.tr("Non puoi sovrascrivere il GeoPackage originale."))
            return

        try:
            # Mostra progresso
            progress = QProgressDialog(
                self.tr("Clonazione GeoPackage in corso..."), None, 0, 100, self
            )
            progress.setWindowTitle(self.tr("Clone GeoPackage"))
            progress.setStyleSheet(MODERN_STYLE)
            progress.setMinimumDuration(0)
            progress.setValue(10)
            QApplication.processEvents()

            # Copia il file
            shutil.copy2(self.gpkg_path, file_path)
            progress.setValue(30)
            QApplication.processEvents()

            # Prepara i percorsi
            vecchio_path = os.path.normpath(self.gpkg_path)
            nuovo_path = os.path.normpath(file_path)
            vecchio_nome = os.path.basename(vecchio_path)
            nuovo_nome = os.path.basename(nuovo_path)

            conn = sqlite3.connect(file_path)
            cursor = conn.cursor()

            # Verifica se esistono progetti
            cursor.execute("""
                SELECT name FROM sqlite_master
                WHERE type='table' AND name='qgis_projects'
            """)

            progetti_aggiornati = 0

            if cursor.fetchone():
                cursor.execute("SELECT name, content FROM qgis_projects")
                progetti = cursor.fetchall()

                progress.setValue(40)
                QApplication.processEvents()

                for idx, (nome_progetto, content) in enumerate(progetti):
                    if not content:
                        continue

                    # Decomprimi il contenuto (gestisce HEX + ZIP)
                    files_content, is_compressed, was_hex = self._decomprimi_progetto(content)

                    progetto_modificato = False
                    nuovo_files_content = {}

                    for file_name, file_content in files_content.items():
                        # Salta i file binari (come styles.db)
                        if file_name.endswith('.db'):
                            nuovo_files_content[file_name] = file_content
                            continue

                        # Decodifica il contenuto XML
                        try:
                            content_str = file_content.decode('utf-8')
                        except UnicodeDecodeError:
                            try:
                                content_str = file_content.decode('latin-1')
                            except:
                                nuovo_files_content[file_name] = file_content
                                continue

                        # Aggiorna i percorsi
                        nuovo_content_str, modificato = self._aggiorna_percorsi_in_contenuto(
                            content_str, vecchio_nome, nuovo_nome, vecchio_path, nuovo_path
                        )

                        if modificato:
                            progetto_modificato = True

                        nuovo_files_content[file_name] = nuovo_content_str.encode('utf-8')

                    if progetto_modificato:
                        # Ricomprimi se era compresso
                        if is_compressed:
                            nuovo_content = self._comprimi_progetto(nuovo_files_content, as_hex=was_hex)
                        else:
                            nuovo_content = list(nuovo_files_content.values())[0]
                            if was_hex:
                                nuovo_content = self._bytes_to_hex(nuovo_content)

                        # Aggiorna nel database
                        cursor.execute(
                            "UPDATE qgis_projects SET content = ? WHERE name = ?",
                            (nuovo_content, nome_progetto)
                        )
                        progetti_aggiornati += 1

                    # Aggiorna progress
                    progress.setValue(40 + int((idx + 1) / len(progetti) * 50))
                    QApplication.processEvents()

                conn.commit()

            progress.setValue(95)
            QApplication.processEvents()

            conn.close()

            progress.setValue(100)

            self.mostra_info(
                self.tr("Clone Completato"),
                self.tr("GeoPackage clonato con successo!\n\n📁 Nuovo file:\n%1\n\n📋 Progetti aggiornati: %2\n\n✅ I percorsi dei layer sono stati aggiornati per puntare al nuovo GeoPackage.").replace('%1', file_path).replace('%2', str(progetti_aggiornati))
            )

            # Chiedi se aggiungere il nuovo GeoPackage alla lista
            if self.mostra_conferma(
                self.tr("Aggiungere alla lista?"),
                self.tr("Vuoi aggiungere il GeoPackage clonato alla lista?")
            ):
                self.gpkg_combo.addItem(file_path)
                self.gpkg_combo.setCurrentText(file_path)

        except Exception as e:
            import traceback
            self.mostra_errore(self.tr("Errore"), self.tr("Errore durante la clonazione:\n{}").format(str(e) + "\n\n" + traceback.format_exc()))

    def ottimizza_database(self):
        """Ottimizza il GeoPackage eseguendo VACUUM per ridurre dimensioni e migliorare performance."""
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

            # Conta progetti
            num_progetti = self.lista_progetti.count()

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

            # Registra tempo di inizio
            import time
            start_time = time.time()

            # Esegui VACUUM
            conn = sqlite3.connect(self.gpkg_path)
            cursor = conn.cursor()
            cursor.execute("VACUUM")
            conn.commit()
            conn.close()

            # Calcola tempo impiegato
            elapsed_time = time.time() - start_time

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

            # Calcola spazio risparmiato
            space_saved = size_before - size_after
            if space_saved < 0:
                space_saved = 0

            if space_saved < 1024:
                space_saved_str = f"{space_saved} B"
            elif space_saved < 1024 * 1024:
                space_saved_str = f"{space_saved / 1024:.1f} KB"
            elif space_saved < 1024 * 1024 * 1024:
                space_saved_str = f"{space_saved / (1024 * 1024):.1f} MB"
            else:
                space_saved_str = f"{space_saved / (1024 * 1024 * 1024):.2f} GB"

            percentage_saved = (space_saved / size_before * 100) if size_before > 0 else 0

            progress.close()

            # Dialog risultato
            result_msg = QMessageBox(self)
            result_msg.setIcon(MsgBoxInformation)
            result_msg.setWindowTitle(self.tr("✅ Ottimizzazione completata!"))
            result_msg.setText(
                self.tr("Dimensione prima:    {0}\n"
                        "Dimensione dopo:     {1}\n"
                        "────────────────────────────\n"
                        "Spazio risparmiato:  {2} ({3:.1f}%)\n\n"
                        "Tempo impiegato: {4:.1f} secondi").format(
                    size_before_str,
                    size_after_str,
                    space_saved_str,
                    percentage_saved,
                    elapsed_time
                )
            )
            result_msg.setStyleSheet(MODERN_STYLE)
            result_msg.exec()

            # Aggiorna le info del GeoPackage
            self.aggiorna_info_gpkg()

        except Exception as e:
            import traceback
            self.mostra_errore(
                self.tr("Errore"),
                self.tr("Errore durante l'ottimizzazione:\n{}").format(str(e) + "\n\n" + traceback.format_exc())
            )

    def aggiorna_tutti_metadati(self):
        """Rigenera i metadati per tutti i progetti nel GeoPackage."""
        if not self.gpkg_path:
            self.mostra_errore(self.tr("Attenzione"), self.tr("Seleziona prima un GeoPackage."))
            return

        if not os.path.exists(self.gpkg_path):
            self.mostra_errore(self.tr("Errore"), self.tr("Il file GeoPackage non esiste."))
            return

        try:
            # Conta progetti totali
            conn = sqlite3.connect(self.gpkg_path)
            cursor = conn.cursor()

            cursor.execute("SELECT COUNT(*) FROM qgis_projects")
            total_projects = cursor.fetchone()[0]
            conn.close()

            if total_projects == 0:
                self.mostra_info(self.tr("Nessun Progetto"), self.tr("Non ci sono progetti nel GeoPackage."))
                return

            # Dialog di conferma
            msg = QMessageBox(self)
            msg.setIcon(MsgBoxQuestion)
            msg.setWindowTitle(self.tr("📊 Aggiorna Metadati"))
            msg.setText(
                self.tr("Progetti trovati: {0}\n\n"
                        "Questa operazione rigenererà i metadati per tutti i progetti:\n"
                        "• Data creazione e modifica\n"
                        "• Dimensione del progetto\n"
                        "• Conteggio layer (vettoriali/raster)\n\n"
                        "Vuoi continuare?").format(total_projects)
            )
            msg.setStandardButtons(MsgBoxYes | MsgBoxNo)
            msg.setDefaultButton(MsgBoxYes)
            msg.setStyleSheet(MODERN_STYLE)

            if msg.exec() != MsgBoxYes:
                return

            # Progress dialog
            progress = QProgressDialog(
                self.tr("Elaborazione metadati in corso..."),
                self.tr("Annulla"), 0, total_projects, self
            )
            progress.setWindowTitle(self.tr("📊 Aggiornamento Metadati"))
            progress.setStyleSheet(MODERN_STYLE)
            progress.setWindowModality(WindowModal)
            progress.show()
            QApplication.processEvents()

            # Apri connessione
            conn = sqlite3.connect(self.gpkg_path)
            cursor = conn.cursor()

            # Assicurati che la tabella metadati esista
            self.crea_tabella_metadata(conn)

            # Leggi tutti i progetti
            cursor.execute("SELECT name, content FROM qgis_projects ORDER BY name")
            progetti = cursor.fetchall()

            progetti_aggiornati = 0
            progetti_saltati = 0

            for idx, (nome_progetto, content) in enumerate(progetti):
                # Verifica se l'utente ha annullato
                if progress.wasCanceled():
                    break

                # Aggiorna progress
                progress.setValue(idx)
                progress.setLabelText(self.tr("Elaborazione: {0}").format(nome_progetto))
                QApplication.processEvents()

                if not content:
                    progetti_saltati += 1
                    continue

                try:
                    # Salva i metadati (is_new=False per preservare la data di creazione,
                    # update_modified_date=False per NON cambiare la data di modifica)
                    self.salva_metadati_progetto(conn, nome_progetto, content, is_new=False, update_modified_date=False)
                    progetti_aggiornati += 1
                except Exception as e:
                    progetti_saltati += 1
                    continue

            conn.close()
            progress.setValue(total_projects)

            # Dialog risultato
            result_msg = QMessageBox(self)
            result_msg.setIcon(MsgBoxInformation)
            result_msg.setWindowTitle(self.tr("✅ Metadati Aggiornati!"))
            result_msg.setText(
                self.tr("Elaborazione completata!\n\n"
                        "Progetti aggiornati: {0}\n"
                        "Progetti saltati: {1}\n"
                        "Totale: {2}\n\n"
                        "I tooltip ora mostreranno informazioni complete.").format(
                    progetti_aggiornati,
                    progetti_saltati,
                    total_projects
                )
            )
            result_msg.setStyleSheet(MODERN_STYLE)
            result_msg.exec()

        except Exception as e:
            import traceback
            self.mostra_errore(
                self.tr("Errore"),
                self.tr("Errore durante l'aggiornamento metadati:\n{}").format(str(e) + "\n\n" + traceback.format_exc())
            )
