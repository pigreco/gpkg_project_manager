# -*- coding: utf-8 -*-
"""
/***************************************************************************
 GeoPackage Styles Manager
                              -------------------
        begin                : 2025-12-04
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

from qgis.core import QgsProject, Qgis, QgsMapLayer
from qgis.utils import iface
from qgis.PyQt.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QTableWidget, QTableWidgetItem,
    QFileDialog, QMessageBox, QGroupBox, QFrame,
    QAbstractItemView, QSizePolicy, QInputDialog,
    QToolButton, QMenu, QHeaderView, QApplication, QComboBox
)
from qgis.PyQt.QtCore import Qt, QCoreApplication
from qgis.PyQt.QtGui import QFont, QColor

import sqlite3
import os
from datetime import datetime

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

# QToolButton
InstantPopup = get_qt_enum(QToolButton, 'InstantPopup') or 2


# ============================================================
# STILE CSS
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
    font-size: 20px;
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
"""


class StylesManagerDialog(QDialog):
    """Dialog per gestire gli stili nel GeoPackage."""

    def __init__(self, gpkg_path, parent=None):
        """Inizializza il dialog.

        Args:
            gpkg_path: Percorso del file GeoPackage
            parent: Widget padre
        """
        super().__init__(parent)
        self.gpkg_path = gpkg_path
        self.setWindowTitle(self.tr("🎨 Gestione Stili GeoPackage"))
        self.setMinimumSize(900, 500)
        self.setup_ui()
        self.load_styles()

    def tr(self, message):
        """Translate string using Qt translation API."""
        return QCoreApplication.translate('StylesManagerDialog', message)

    def setup_ui(self):
        """Configura l'interfaccia utente."""
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        # === HEADER ===
        header_widget = QGroupBox()
        header_layout = QVBoxLayout(header_widget)
        header_layout.setContentsMargins(10, 10, 10, 10)
        header_layout.setSpacing(5)

        title_label = QLabel(self.tr("🎨 Gestione Stili Layer"))
        title_label.setObjectName("titleLabel")
        header_layout.addWidget(title_label)

        subtitle_label = QLabel(self.tr("Visualizza e gestisci gli stili salvati nel GeoPackage"))
        subtitle_label.setObjectName("subtitleLabel")
        header_layout.addWidget(subtitle_label)

        # Info GeoPackage
        gpkg_name = os.path.basename(self.gpkg_path)
        self.info_label = QLabel(self.tr("📦 GeoPackage: {}").format(gpkg_name))
        self.info_label.setObjectName("tipLabel")
        self.info_label.setStyleSheet("""
            QLabel {
                color: #6b7280;
                font-size: 11px;
                padding: 5px 10px;
                background-color: #f9fafb;
                border-radius: 4px;
            }
        """)
        header_layout.addWidget(self.info_label)

        layout.addWidget(header_widget)

        # === TABELLA STILI ===
        styles_group = QGroupBox(self.tr("  📋  Stili disponibili  (Doppio clic per applicare • Icona ⚙️ per opzioni)"))
        styles_layout = QVBoxLayout(styles_group)

        self.table_styles = QTableWidget()
        self.table_styles.setColumnCount(6)  # 5 colonne dati + 1 colonna opzioni
        self.table_styles.setHorizontalHeaderLabels([
            self.tr("Layer"),
            self.tr("Nome Stile"),
            self.tr("Default"),
            self.tr("Descrizione"),
            self.tr("Ultima Modifica"),
            self.tr("⚙️")  # Colonna opzioni
        ])

        self.table_styles.setAlternatingRowColors(True)
        self.table_styles.setSelectionMode(SingleSelection)
        self.table_styles.setSelectionBehavior(SelectRows)
        self.table_styles.setEditTriggers(NoEditTriggers)
        self.table_styles.verticalHeader().setVisible(False)
        self.table_styles.setSortingEnabled(True)

        # Imposta il ridimensionamento delle colonne
        header = self.table_styles.horizontalHeader()
        header.setSectionResizeMode(0, Stretch)  # Layer - si espande automaticamente
        # Colonne 1-4 ridimensionabili manualmente dall'utente
        for i in range(1, 5):
            header.setSectionResizeMode(i, Interactive)
        # Colonna 5 (opzioni) ha larghezza fissa non ridimensionabile
        self.table_styles.setColumnWidth(5, 40)  # Larghezza fissa 40px
        header.setSectionResizeMode(5, Fixed)

        # Eventi
        self.table_styles.cellDoubleClicked.connect(self.apply_style_from_table)

        styles_layout.addWidget(self.table_styles)

        layout.addWidget(styles_group)

        # === FOOTER ===
        separator = QFrame()
        separator.setObjectName("separator")
        separator.setFrameShape(HLine)
        layout.addWidget(separator)

        footer_layout = QHBoxLayout()

        self.styles_count_label = QLabel(self.tr("Stili trovati: 0"))
        self.styles_count_label.setObjectName("tipLabel")
        footer_layout.addWidget(self.styles_count_label)

        footer_layout.addStretch()

        btn_refresh = QPushButton(self.tr("⟳ Aggiorna"))
        btn_refresh.setFixedWidth(120)
        btn_refresh.clicked.connect(self.load_styles)
        footer_layout.addWidget(btn_refresh)

        btn_close = QPushButton(self.tr("Chiudi"))
        btn_close.setFixedWidth(100)
        btn_close.clicked.connect(self.close)
        footer_layout.addWidget(btn_close)

        layout.addLayout(footer_layout)

    def load_styles(self):
        """Carica gli stili dal GeoPackage."""
        self.table_styles.setRowCount(0)

        if not os.path.exists(self.gpkg_path):
            QMessageBox.critical(self, self.tr("Errore"),
                                self.tr("Il file GeoPackage non esiste."))
            return

        try:
            conn = sqlite3.connect(self.gpkg_path)
            cursor = conn.cursor()

            # Verifica se esiste la tabella layer_styles
            cursor.execute("""
                SELECT name FROM sqlite_master
                WHERE type='table' AND name='layer_styles'
            """)

            if not cursor.fetchone():
                self.styles_count_label.setText(self.tr("ℹ️ Nessuna tabella 'layer_styles' trovata nel GeoPackage"))
                conn.close()
                return

            # Carica gli stili
            cursor.execute("""
                SELECT
                    id,
                    f_table_name,
                    styleName,
                    useAsDefault,
                    description,
                    update_time
                FROM layer_styles
                ORDER BY f_table_name, styleName
            """)

            styles = cursor.fetchall()
            conn.close()

            if not styles:
                self.styles_count_label.setText(self.tr("ℹ️ Nessuno stile trovato nel GeoPackage"))
                return

            # Aggiungi le righe
            for style_data in styles:
                self.add_style_row(style_data)

            # Aggiorna il conteggio
            self.styles_count_label.setText(self.tr("Stili trovati: {}").format(len(styles)))

        except Exception as e:
            QMessageBox.critical(self, self.tr("Errore"),
                                self.tr("Errore nella lettura degli stili:\n{}").format(str(e)))

    def add_style_row(self, style_data):
        """Aggiunge una riga alla tabella stili.

        Args:
            style_data: tuple (id, f_table_name, styleName, useAsDefault, description, update_time)
        """
        style_id, f_table_name, style_name, use_as_default, description, update_time = style_data

        row_position = self.table_styles.rowCount()
        self.table_styles.insertRow(row_position)

        # Colonna 0: Layer
        item_layer = QTableWidgetItem(f"  📊  {f_table_name or 'N/A'}")
        item_layer.setData(UserRole, style_id)  # Salva l'ID dello stile
        self.table_styles.setItem(row_position, 0, item_layer)

        # Colonna 1: Nome Stile
        item_style = QTableWidgetItem(style_name or "N/A")
        self.table_styles.setItem(row_position, 1, item_style)

        # Colonna 2: Default
        default_text = "✓" if use_as_default == 1 else ""
        item_default = QTableWidgetItem(default_text)
        item_default.setTextAlignment(AlignCenter | AlignVCenter)
        self.table_styles.setItem(row_position, 2, item_default)

        # Colonna 3: Descrizione
        item_desc = QTableWidgetItem(description or "")
        self.table_styles.setItem(row_position, 3, item_desc)

        # Colonna 4: Ultima Modifica
        if update_time:
            try:
                # Prova vari formati di data
                for fmt in ['%Y-%m-%d %H:%M:%S', '%Y-%m-%dT%H:%M:%S', '%Y-%m-%d']:
                    try:
                        dt = datetime.strptime(update_time, fmt)
                        date_str = dt.strftime('%d/%m/%Y %H:%M')
                        break
                    except:
                        continue
                else:
                    date_str = update_time
            except:
                date_str = update_time
        else:
            date_str = "N/A"
        item_date = QTableWidgetItem(date_str)
        item_date.setTextAlignment(AlignCenter | AlignVCenter)
        self.table_styles.setItem(row_position, 4, item_date)

        # Colonna 5: Pulsante Opzioni
        btn_options = QToolButton()
        btn_options.setText("⋮")
        btn_options.setPopupMode(InstantPopup)
        btn_options.setStyleSheet("""
            QToolButton {
                font-size: 20px;
                font-weight: bold;
                padding: 2px 8px;
            }
        """)

        menu_options = QMenu()
        menu_options.addAction(self.tr("🎨  Applica"), lambda sid=style_id: self.apply_style(sid))
        menu_options.addAction(self.tr("💾  Esporta QML"), lambda sid=style_id: self.export_style(sid))
        menu_options.addSeparator()
        menu_options.addAction(self.tr("✏️  Rinomina"), lambda sid=style_id: self.rename_style(sid))
        menu_options.addAction(self.tr("📋  Duplica"), lambda sid=style_id: self.duplicate_style(sid))
        menu_options.addAction(self.tr("⭐  Imposta come default"), lambda sid=style_id: self.set_as_default(sid))
        menu_options.addSeparator()
        menu_options.addAction(self.tr("🗑️  Elimina"), lambda sid=style_id: self.delete_style(sid))

        btn_options.setMenu(menu_options)

        self.table_styles.setCellWidget(row_position, 5, btn_options)

    def apply_style_from_table(self, row, column):
        """Applica lo stile quando si fa doppio clic su una cella."""
        item = self.table_styles.item(row, 0)
        if item:
            style_id = item.data(UserRole)
            self.apply_style(style_id)

    def get_style_data(self, style_id):
        """Ottiene i dati completi di uno stile.

        Args:
            style_id: ID dello stile

        Returns:
            dict con i dati dello stile o None
        """
        try:
            conn = sqlite3.connect(self.gpkg_path)
            cursor = conn.cursor()

            cursor.execute("""
                SELECT id, f_table_name, styleName, styleQML, useAsDefault, description
                FROM layer_styles
                WHERE id = ?
            """, (style_id,))

            row = cursor.fetchone()
            conn.close()

            if row:
                return {
                    'id': row[0],
                    'f_table_name': row[1],
                    'styleName': row[2],
                    'styleQML': row[3],
                    'useAsDefault': row[4],
                    'description': row[5]
                }
            return None

        except Exception as e:
            QMessageBox.critical(self, self.tr("Errore"),
                                self.tr("Errore nella lettura dello stile:\n{}").format(str(e)))
            return None

    def apply_style(self, style_id):
        """Applica uno stile a un layer caricato in QGIS.

        Args:
            style_id: ID dello stile da applicare
        """
        style_data = self.get_style_data(style_id)
        if not style_data:
            return

        layer_name = style_data['f_table_name']
        style_name = style_data['styleName']
        style_qml = style_data['styleQML']

        # Cerca il layer nel progetto corrente
        project = QgsProject.instance()
        layers = project.mapLayersByName(layer_name)

        if not layers:
            QMessageBox.warning(self, self.tr("Layer non trovato"),
                               self.tr("Il layer '{}' non è caricato nel progetto corrente.\n\n"
                                      "Carica prima il layer per poter applicare lo stile.").format(layer_name))
            return

        layer = layers[0]

        # Crea un file temporaneo con lo stile QML
        import tempfile
        with tempfile.NamedTemporaryFile(mode='w', suffix='.qml', delete=False, encoding='utf-8') as f:
            f.write(style_qml)
            temp_qml = f.name

        try:
            # Applica lo stile al layer
            msg, success = layer.loadNamedStyle(temp_qml)

            if success:
                layer.triggerRepaint()
                iface.layerTreeView().refreshLayerSymbology(layer.id())
                iface.messageBar().pushMessage(
                    self.tr("✅ Stile applicato"),
                    self.tr("Stile '{}' applicato al layer '{}'").format(style_name, layer_name),
                    level=Qgis.Success,
                    duration=5
                )
            else:
                QMessageBox.warning(self, self.tr("Errore"),
                                   self.tr("Impossibile applicare lo stile:\n{}").format(msg))
        finally:
            # Rimuovi il file temporaneo
            try:
                os.unlink(temp_qml)
            except:
                pass

    def export_style(self, style_id):
        """Esporta uno stile come file QML.

        Args:
            style_id: ID dello stile da esportare
        """
        style_data = self.get_style_data(style_id)
        if not style_data:
            return

        layer_name = style_data['f_table_name']
        style_name = style_data['styleName']
        style_qml = style_data['styleQML']

        # Proponi un nome file
        default_filename = f"{layer_name}_{style_name}.qml"

        file_path, _ = QFileDialog.getSaveFileName(
            self,
            self.tr("Esporta Stile come QML"),
            default_filename,
            self.tr("File QML (*.qml)")
        )

        if not file_path:
            return

        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(style_qml)

            iface.messageBar().pushMessage(
                self.tr("✅ Stile esportato"),
                self.tr("Stile salvato in: {}").format(file_path),
                level=Qgis.Success,
                duration=5
            )
        except Exception as e:
            QMessageBox.critical(self, self.tr("Errore"),
                                self.tr("Errore nell'esportazione dello stile:\n{}").format(str(e)))

    def rename_style(self, style_id):
        """Rinomina uno stile.

        Args:
            style_id: ID dello stile da rinominare
        """
        style_data = self.get_style_data(style_id)
        if not style_data:
            return

        current_name = style_data['styleName']

        new_name, ok = QInputDialog.getText(
            self,
            self.tr("✏️ Rinomina Stile"),
            self.tr("Nuovo nome per lo stile:"),
            text=current_name
        )

        if not ok or not new_name or new_name == current_name:
            return

        try:
            conn = sqlite3.connect(self.gpkg_path)
            cursor = conn.cursor()

            # Aggiorna il nome dello stile
            cursor.execute("""
                UPDATE layer_styles
                SET styleName = ?,
                    update_time = CURRENT_TIMESTAMP
                WHERE id = ?
            """, (new_name, style_id))

            conn.commit()
            conn.close()

            iface.messageBar().pushMessage(
                self.tr("✅ Stile rinominato"),
                self.tr("Stile rinominato da '{}' a '{}'").format(current_name, new_name),
                level=Qgis.Success,
                duration=5
            )

            self.load_styles()

        except Exception as e:
            QMessageBox.critical(self, self.tr("Errore"),
                                self.tr("Errore nella rinominazione dello stile:\n{}").format(str(e)))

    def duplicate_style(self, style_id):
        """Duplica uno stile.

        Args:
            style_id: ID dello stile da duplicare
        """
        style_data = self.get_style_data(style_id)
        if not style_data:
            return

        current_name = style_data['styleName']
        new_name = f"{current_name}_copia"

        # Chiedi il nome per la copia
        new_name, ok = QInputDialog.getText(
            self,
            self.tr("📋 Duplica Stile"),
            self.tr("Nome per lo stile duplicato:"),
            text=new_name
        )

        if not ok or not new_name:
            return

        try:
            conn = sqlite3.connect(self.gpkg_path)
            cursor = conn.cursor()

            # Duplica lo stile
            cursor.execute("""
                INSERT INTO layer_styles (
                    f_table_catalog, f_table_schema, f_table_name,
                    f_geometry_column, styleName, styleQML, styleSLD,
                    useAsDefault, description, owner, ui, update_time
                )
                SELECT
                    f_table_catalog, f_table_schema, f_table_name,
                    f_geometry_column, ?, styleQML, styleSLD,
                    0, description, owner, ui, CURRENT_TIMESTAMP
                FROM layer_styles
                WHERE id = ?
            """, (new_name, style_id))

            conn.commit()
            conn.close()

            iface.messageBar().pushMessage(
                self.tr("✅ Stile duplicato"),
                self.tr("Stile '{}' duplicato come '{}'").format(current_name, new_name),
                level=Qgis.Success,
                duration=5
            )

            self.load_styles()

        except Exception as e:
            QMessageBox.critical(self, self.tr("Errore"),
                                self.tr("Errore nella duplicazione dello stile:\n{}").format(str(e)))

    def set_as_default(self, style_id):
        """Imposta uno stile come default.

        Args:
            style_id: ID dello stile da impostare come default
        """
        style_data = self.get_style_data(style_id)
        if not style_data:
            return

        layer_name = style_data['f_table_name']
        style_name = style_data['styleName']

        try:
            conn = sqlite3.connect(self.gpkg_path)
            cursor = conn.cursor()

            # Rimuovi il flag default da tutti gli altri stili dello stesso layer
            cursor.execute("""
                UPDATE layer_styles
                SET useAsDefault = 0
                WHERE f_table_name = ?
            """, (layer_name,))

            # Imposta questo stile come default
            cursor.execute("""
                UPDATE layer_styles
                SET useAsDefault = 1,
                    update_time = CURRENT_TIMESTAMP
                WHERE id = ?
            """, (style_id,))

            conn.commit()
            conn.close()

            iface.messageBar().pushMessage(
                self.tr("✅ Stile default aggiornato"),
                self.tr("Stile '{}' impostato come default per il layer '{}'").format(style_name, layer_name),
                level=Qgis.Success,
                duration=5
            )

            self.load_styles()

        except Exception as e:
            QMessageBox.critical(self, self.tr("Errore"),
                                self.tr("Errore nell'impostazione dello stile default:\n{}").format(str(e)))

    def delete_style(self, style_id):
        """Elimina uno stile.

        Args:
            style_id: ID dello stile da eliminare
        """
        style_data = self.get_style_data(style_id)
        if not style_data:
            return

        style_name = style_data['styleName']
        layer_name = style_data['f_table_name']

        # Conferma eliminazione
        reply = QMessageBox.question(
            self,
            self.tr("🗑️ Elimina Stile"),
            self.tr("Sei sicuro di voler eliminare lo stile '{}'?\n\n"
                   "Layer: {}\n\n"
                   "⚠️ Questa operazione non può essere annullata.").format(style_name, layer_name),
            MsgBoxYes | MsgBoxNo,
            MsgBoxNo
        )

        if reply != MsgBoxYes:
            return

        try:
            conn = sqlite3.connect(self.gpkg_path)
            cursor = conn.cursor()

            cursor.execute("DELETE FROM layer_styles WHERE id = ?", (style_id,))

            conn.commit()
            conn.close()

            iface.messageBar().pushMessage(
                self.tr("✅ Stile eliminato"),
                self.tr("Stile '{}' eliminato con successo").format(style_name),
                level=Qgis.Success,
                duration=5
            )

            self.load_styles()

        except Exception as e:
            QMessageBox.critical(self, self.tr("Errore"),
                                self.tr("Errore nell'eliminazione dello stile:\n{}").format(str(e)))
