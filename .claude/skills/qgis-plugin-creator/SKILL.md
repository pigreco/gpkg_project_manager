---
name: qgis-plugin-creator
description: Create complete, production-ready QGIS plugins following official guidelines and best practices. Use when user asks to create a QGIS plugin, convert a Python script to QGIS plugin, or needs help with plugin structure, metadata, or publishing to the official QGIS repository.
---

# QGIS Plugin Creator

Create complete, installable QGIS plugins following official repository guidelines.

## Quick Start

To create a plugin, collect this information from the user:

1. **Plugin name** (lowercase, underscores, NO word "plugin")
2. **Description** (short + extended)
3. **Author name and email**
4. **Repository URL** (GitHub)
5. **Menu category**: Vector | Raster | Database | Web | Sketching
6. **Minimum QGIS version** (default: 3.20)

## Plugin Structure

```
plugin_name/
├── __init__.py           # Entry point with classFactory()
├── metadata.txt          # Plugin metadata (REQUIRED)
├── main.py               # Main plugin class
├── dialogs.py            # UI dialogs (if needed)
├── resources.py          # Compiled resources (optional)
├── icon.png              # Toolbar icon (recommended: 24x24 or 32x32)
├── LICENSE               # GPLv2+ license file
└── README.md             # Documentation
```

### Naming Rules

- **NO** word "plugin" in folder name or filenames
- Use lowercase with underscores: `gpkg_manager`, `layer_tools`
- Main class: `CamelCase` without "Plugin" suffix

## Required Files

### 1. metadata.txt

```ini
[general]
name=Plugin Display Name
qgisMinimumVersion=3.20
description=Short description (one line)
version=0.1
author=Author Name
email=author@email.com
about=Extended description. Can be multi-line.
    Explain features, usage, and any dependencies.
tracker=https://github.com/user/repo/issues
repository=https://github.com/user/repo
homepage=https://github.com/user/repo
hasProcessingProvider=no
tags=comma, separated, tags
category=Database
icon=icon.png
experimental=True
deprecated=False
server=False
changelog=
    0.1 Initial release
```

### 2. __init__.py

```python
# -*- coding: utf-8 -*-
"""
Plugin Name
Description of what it does
"""

def classFactory(iface):
    """Load main plugin class.
    
    Args:
        iface: QGIS interface instance
    """
    from .main import PluginClassName
    return PluginClassName(iface)
```

### 3. main.py (Main Class Template)

```python
# -*- coding: utf-8 -*-
"""Main plugin module."""

from qgis.PyQt.QtWidgets import QAction, QMessageBox
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtCore import QCoreApplication
import os


class PluginClassName:
    """Main plugin class."""

    def __init__(self, iface):
        """Initialize plugin.
        
        Args:
            iface: QGIS interface instance
        """
        self.iface = iface
        self.plugin_dir = os.path.dirname(__file__)
        self.actions = []
        self.menu = self.tr('&Plugin Menu Name')
        self.toolbar = self.iface.addToolBar('PluginToolbar')
        self.toolbar.setObjectName('PluginToolbar')

    def tr(self, message):
        """Translate string."""
        return QCoreApplication.translate('PluginClassName', message)

    def add_action(self, icon_path, text, callback, 
                   enabled=True, add_to_menu=True, 
                   add_to_toolbar=True, parent=None):
        """Add toolbar icon and menu item."""
        icon = QIcon(icon_path)
        action = QAction(icon, text, parent or self.iface.mainWindow())
        action.triggered.connect(callback)
        action.setEnabled(enabled)

        if add_to_toolbar:
            self.toolbar.addAction(action)
        if add_to_menu:
            self.iface.addPluginToMenu(self.menu, action)
            # Or use specific menu:
            # self.iface.addPluginToDatabaseMenu(self.menu, action)
            # self.iface.addPluginToVectorMenu(self.menu, action)
            # self.iface.addPluginToRasterMenu(self.menu, action)
            # self.iface.addPluginToWebMenu(self.menu, action)

        self.actions.append(action)
        return action

    def initGui(self):
        """Create menu entries and toolbar icons."""
        icon_path = os.path.join(self.plugin_dir, 'icon.png')
        self.add_action(
            icon_path,
            text=self.tr('Open Tool'),
            callback=self.run,
            parent=self.iface.mainWindow()
        )

    def unload(self):
        """Remove menu entries and toolbar icons."""
        for action in self.actions:
            self.iface.removePluginMenu(self.menu, action)
            # Match with initGui:
            # self.iface.removePluginDatabaseMenu(self.menu, action)
            self.iface.removeToolBarIcon(action)
        del self.toolbar

    def run(self):
        """Main plugin action."""
        # Import dialog here to avoid loading on startup
        from .dialogs import MainDialog
        dlg = MainDialog(self.iface.mainWindow())
        dlg.exec()
```

### 4. dialogs.py (Dialog Template)

```python
# -*- coding: utf-8 -*-
"""Plugin dialogs."""

from qgis.PyQt.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, 
    QPushButton, QLabel
)
from qgis.PyQt.QtCore import Qt


class MainDialog(QDialog):
    """Main plugin dialog."""

    def __init__(self, parent=None):
        """Initialize dialog."""
        super().__init__(parent)
        self.setWindowTitle('Dialog Title')
        self.setMinimumSize(400, 300)
        self.setup_ui()

    def setup_ui(self):
        """Setup user interface."""
        layout = QVBoxLayout(self)
        
        # Add widgets here
        label = QLabel('Content goes here')
        layout.addWidget(label)
        
        # Buttons
        btn_layout = QHBoxLayout()
        btn_close = QPushButton('Close')
        btn_close.clicked.connect(self.close)
        btn_layout.addStretch()
        btn_layout.addWidget(btn_close)
        layout.addLayout(btn_layout)
```

## Multilingual Support

### Overview

Implementing multilingual support allows users to switch plugin language independently from QGIS system settings.

### Implementation Steps

1. **Create i18n directory structure**:
```
plugin_name/
└── i18n/
    ├── plugin_name_en.ts    # Translation source (XML)
    ├── plugin_name_en.qm    # Compiled translation (binary)
    └── README.md            # Translation instructions
```

2. **Update metadata.txt with multilingual fields**:
```ini
description=Descrizione in italiano (lingua predefinita)
description(en)=English description (alternative format)
description[en]=English description (standard format)

about=Descrizione estesa in italiano.
    Funzionalità principali...

about[en]=Extended English description.
    Main features...

changelog=1.0.0
    • Prima versione
    0.1.0
    • Versione iniziale

changelog[en]=1.0.0
    • First release
    0.1.0
    • Initial version

available_languages=en,it
```

**Note**: Use both `description(en)` and `description[en]` for maximum compatibility. QGIS Plugin Manager displays metadata based on QGIS system language, NOT plugin's internal selector.

3. **Add translation loading in main.py**:
```python
from qgis.PyQt.QtCore import QSettings, QTranslator, QCoreApplication
import os

class PluginClassName:
    def __init__(self, iface):
        self.iface = iface
        self.plugin_dir = os.path.dirname(__file__)
        self.translator = None

        # Load translator
        self.load_translator()

    def load_translator(self, locale=None):
        """Load translator with priority: user preference > QGIS locale > default."""
        settings = QSettings()

        # Get locale with priority system
        if locale is None:
            # Try user preference first
            locale = settings.value('plugin_name/language', None)
            if locale is None:
                # Fall back to QGIS locale
                qgis_locale = settings.value('locale/userLocale', 'it_IT')
                locale = qgis_locale[0:2] if qgis_locale else 'it'

        # Try loading .qm file
        qm_path = os.path.join(self.plugin_dir, 'i18n', f'plugin_name_{locale}.qm')
        if os.path.exists(qm_path):
            self.translator = QTranslator()
            if self.translator.load(qm_path):
                QCoreApplication.installTranslator(self.translator)
                return True

        # Fallback: load .ts file directly (see Custom TS Translator below)
        return False

    def change_language(self, locale):
        """Change plugin language and reload dialog."""
        settings = QSettings()
        settings.setValue('plugin_name/language', locale)
        self.load_translator(locale)

        # Reload dialog if open
        if self.dialog:
            self.dialog.close()
            self.dialog = None
```

4. **Add language selector in dialog**:
```python
from qgis.PyQt.QtWidgets import QComboBox, QLabel, QHBoxLayout
from qgis.PyQt.QtCore import QSettings, QTimer, QCoreApplication

class MainDialog(QDialog):
    def __init__(self, parent=None, plugin=None):
        super().__init__(parent)
        self.plugin = plugin  # Store plugin reference
        self.setup_ui()

    def tr(self, message):
        """Translate string using Qt translation API."""
        return QCoreApplication.translate('DialogClassName', message)

    def setup_ui(self):
        """Setup user interface."""
        layout = QVBoxLayout(self)

        # ... main content ...

        # Language selector at bottom
        lang_layout = QHBoxLayout()
        lang_layout.addWidget(QLabel(self.tr("Select language / Seleziona lingua")))

        self.language_combo = QComboBox()
        self.language_combo.addItem("🇮🇹 Italiano", "it")
        self.language_combo.addItem("🇬🇧 English", "en")

        # Set current language from settings
        current_lang = QSettings().value('plugin_name/language', None)
        if current_lang:
            index = self.language_combo.findData(current_lang)
            if index >= 0:
                self.language_combo.setCurrentIndex(index)

        self.language_combo.currentIndexChanged.connect(self.on_language_changed)
        lang_layout.addWidget(self.language_combo)
        lang_layout.addStretch()

        layout.addLayout(lang_layout)

    def on_language_changed(self, index):
        """Handle language change."""
        new_locale = self.language_combo.currentData()
        current_locale = QSettings().value('plugin_name/language', None)

        if new_locale != current_locale and self.plugin:
            # Change language
            self.plugin.change_language(new_locale)

            # Show bilingual message
            msg = QMessageBox(self)
            msg.setWindowTitle(self.tr("Language Changed / Lingua Cambiata"))
            msg.setText(self.tr("Language has been changed.\\nThe dialog will be reloaded.\\n\\nLa lingua è stata cambiata.\\nIl dialog verrà ricaricato."))
            msg.exec()

            # Close and reopen dialog
            self.accept()
            QTimer.singleShot(100, self.plugin.run)
```

5. **Wrap ALL UI strings with tr()**:
```python
# WRONG - hardcoded strings
QPushButton("Save")
QLabel("Select file:")
QMessageBox.information(self, "Success", "Project saved!")

# CORRECT - translatable strings
QPushButton(self.tr("Save"))
QLabel(self.tr("Select file:"))
QMessageBox.information(
    self,
    self.tr("Success"),
    self.tr("Project '%1' saved!").replace('%1', project_name)
)
```

**Important**: Use `%1`, `%2` placeholders for string interpolation, then replace with actual values. This preserves translation context.

### Custom TS Translator (Fallback)

When .qm compilation is not available, implement a custom translator that reads .ts files directly:

```python
# ts_translator.py
import os
import xml.etree.ElementTree as ET

class TSTranslator:
    """Custom translator that reads .ts files directly."""

    def __init__(self):
        self.translations = {}
        self.loaded = False

    def load(self, ts_path):
        """Load translations from .ts file."""
        try:
            tree = ET.parse(ts_path)
            root = tree.getroot()

            for context_elem in root.findall('context'):
                context_name = context_elem.find('name')
                context_name = context_name.text if context_name is not None else ''

                if context_name not in self.translations:
                    self.translations[context_name] = {}

                for message_elem in context_elem.findall('message'):
                    source_elem = message_elem.find('source')
                    translation_elem = message_elem.find('translation')

                    if source_elem is not None and translation_elem is not None:
                        source = source_elem.text or ''
                        translation = translation_elem.text or ''

                        # Skip obsolete or unfinished translations
                        trans_type = translation_elem.get('type', '')
                        if trans_type in ('obsolete', 'unfinished'):
                            continue

                        if source and translation:
                            self.translations[context_name][source] = translation

            self.loaded = True
            return True
        except Exception as e:
            print(f"Error loading TS file: {e}")
            return False

    def translate(self, context, source):
        """Translate a string."""
        if context in self.translations and source in self.translations[context]:
            return self.translations[context][source]
        return source

# Singleton instance
_ts_translator = None

def get_ts_translator():
    global _ts_translator
    if _ts_translator is None:
        _ts_translator = TSTranslator()
    return _ts_translator

def install_ts_translator(ts_path):
    translator = get_ts_translator()
    return translator.load(ts_path)
```

Use in dialog's tr() method:
```python
# dialogs.py
try:
    from .ts_translator import get_ts_translator
    TS_TRANSLATOR_AVAILABLE = True
except ImportError:
    TS_TRANSLATOR_AVAILABLE = False

class MainDialog(QDialog):
    def tr(self, message):
        """Translate string with TS fallback."""
        # Try TS translator first if available
        if TS_TRANSLATOR_AVAILABLE:
            translator = get_ts_translator()
            if translator.loaded:
                translation = translator.translate('DialogClassName', message)
                if translation != message:
                    return translation

        # Fall back to Qt translator
        return QCoreApplication.translate('DialogClassName', message)
```

## Qt5/Qt6 Compatibility

QGIS 3.x uses Qt5, future versions may use Qt6. For enum compatibility:

```python
def get_qt_enum(enum_class, value_name):
    """Get enum value compatible with Qt5 and Qt6."""
    if hasattr(enum_class, value_name):
        return getattr(enum_class, value_name)
    for attr_name in dir(enum_class):
        attr = getattr(enum_class, attr_name)
        if hasattr(attr, value_name):
            return getattr(attr, value_name)
    return None

# Usage
from qgis.PyQt.QtCore import Qt
AlignCenter = get_qt_enum(Qt, 'AlignCenter') or 0x0084
```

## Database & GeoPackage Management

### SQLite/GeoPackage Connections

When working with GeoPackage or SQLite databases:

```python
import sqlite3

# Connect to database
conn = sqlite3.connect(gpkg_path)
cursor = conn.cursor()

try:
    # Execute queries
    cursor.execute("SELECT name FROM qgis_projects")
    projects = cursor.fetchall()

    # Insert/Update with parameters (prevents SQL injection)
    cursor.execute(
        "INSERT INTO qgis_projects (name, content) VALUES (?, ?)",
        (project_name, project_content)
    )

    # Commit changes
    conn.commit()

except Exception as e:
    # Handle errors
    conn.rollback()
    print(f"Database error: {e}")

finally:
    # Always close connection
    conn.close()
```

**Important**: Always use parameterized queries (`?` placeholders) to prevent SQL injection.

### QGIS Project Management in GeoPackage

Save and load QGIS projects from GeoPackage:

```python
from qgis.core import QgsProject

# Save current project to GeoPackage
project = QgsProject.instance()
uri = f"geopackage:{gpkg_path}?projectName={project_name}"
success = project.write(uri)

# Load project from GeoPackage
uri = f"geopackage:{gpkg_path}?projectName={project_name}"
success = project.read(uri)
```

### XML Content Manipulation

When updating paths in project XML:

```python
import re

def update_paths_in_xml(content_str, old_path, new_path):
    """Update file paths in QGIS project XML."""
    # Normalize paths for different OS
    old_path_unix = old_path.replace('\\', '/')
    new_path_unix = new_path.replace('\\', '/')

    # Direct substitutions
    replacements = [
        (old_path, new_path),  # Windows format
        (old_path_unix, new_path_unix),  # Unix format
    ]

    modified = content_str
    for old, new in replacements:
        if old in modified:
            modified = modified.replace(old, new)

    return modified
```

## Context Menus

Add right-click context menus to list widgets:

```python
from qgis.PyQt.QtWidgets import QListWidget, QMenu
from qgis.PyQt.QtCore import Qt

class MainDialog(QDialog):
    def setup_ui(self):
        self.list_widget = QListWidget()
        self.list_widget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.list_widget.customContextMenuRequested.connect(self.show_context_menu)

    def show_context_menu(self, position):
        """Show context menu at cursor position."""
        if not self.list_widget.currentItem():
            return

        menu = QMenu(self)
        menu.addAction(self.tr("📂 Open"), self.open_item)
        menu.addAction(self.tr("✏️  Rename"), self.rename_item)
        menu.addSeparator()
        menu.addAction(self.tr("📋 Duplicate"), self.duplicate_item)
        menu.addAction(self.tr("🗑️  Delete"), self.delete_item)

        menu.exec(self.list_widget.mapToGlobal(position))
```

## Menu Categories

Use appropriate menu based on plugin functionality:

| Category | Method | Use for |
|----------|--------|---------|
| Database | `addPluginToDatabaseMenu()` | GeoPackage, PostGIS, SQLite |
| Vector | `addPluginToVectorMenu()` | Vector operations |
| Raster | `addPluginToRasterMenu()` | Raster operations |
| Web | `addPluginToWebMenu()` | Web services, APIs |
| Generic | `addPluginToMenu()` | General tools |

## Python String Best Practices

### Escape Sequences

Always use escape sequences instead of literal newlines in strings:

```python
# WRONG - literal newlines cause SyntaxError
msg = "First line
Second line"

# CORRECT - use \n escape sequence
msg = "First line\nSecond line"
```

### Backslash Handling

Properly escape backslashes, especially in file paths:

```python
# WRONG - single backslash in replace
path = path.replace('\', '/')  # SyntaxError

# CORRECT - escape backslash
path = path.replace('\\', '/')

# ALTERNATIVE - use raw strings for paths
path = r'C:\Users\name\file.txt'
```

### Quote Handling

Avoid unnecessary escaping inside strings:

```python
# WRONG - escaping single quotes in double-quoted string
msg = "Il progetto \'project\' esiste"  # SyntaxError

# CORRECT - no escaping needed
msg = "Il progetto 'project' esiste"

# Or use the opposite quote type
msg = 'Il progetto "project" esiste'
```

### Multi-line Strings

For long messages, use single line with `\n`:

```python
# WRONG - literal newlines
error_msg = "Errore durante
l'operazione"

# CORRECT - single line with escape sequences
error_msg = "Errore durante\nl'operazione"

# Or use triple quotes for docstrings only
about = """This is a long description.
It can span multiple lines.
"""
```

### String Formatting for Translations

Use placeholders for proper translation context:

```python
# WRONG - f-strings break translations
self.tr(f"Progetto {nome} salvato")

# CORRECT - use placeholders
self.tr("Progetto '%1' salvato").replace('%1', nome)

# For multiple replacements
self.tr("File '%1' saved to '%2'").replace('%1', filename).replace('%2', path)
```

## Publishing Checklist

Before publishing to official QGIS repository:

### Required
- [ ] Valid OSGEO ID account
- [ ] All metadata links work (homepage, repository, tracker)
- [ ] GPLv2+ compatible license
- [ ] No binaries in package
- [ ] Package size < 25MB
- [ ] Minimal documentation (README.md)

### Recommended
- [ ] Comments in English
- [ ] PEP8 compliant code
- [ ] Cross-platform (Windows, Linux, macOS)
- [ ] No `__pycache__/`, `.git/`, `__MACOSX/` in package
- [ ] All UI strings wrapped with `tr()` for translation

### Forbidden in Package
- `ui_*.py` (generated files)
- `resources_rc.py` (generated files)
- `__pycache__/`
- `.git/`
- `__MACOSX/`
- `.pyc` files
- Development scripts (batch files, PowerShell scripts)
- Temporary files and build artifacts

### ZIP Structure

Create plugin ZIP with correct structure:

```bash
# CORRECT structure
zip -r plugin_name.zip plugin_name/__init__.py plugin_name/main.py plugin_name/dialogs.py plugin_name/metadata.txt plugin_name/icon.png plugin_name/i18n/

# The ZIP should contain:
plugin_name.zip
└── plugin_name/
    ├── __init__.py
    ├── main.py
    ├── dialogs.py
    ├── metadata.txt
    ├── icon.png
    ├── README.md
    └── i18n/
        ├── plugin_name_en.ts
        └── plugin_name_en.qm
```

**Important**: The plugin folder must be INSIDE the ZIP, not at the root level.

## Network Requests

Always use `QgsNetworkAccessManager` instead of `urllib`/`requests`:

```python
from qgis.core import QgsNetworkAccessManager
from qgis.PyQt.QtNetwork import QNetworkRequest
from qgis.PyQt.QtCore import QUrl

manager = QgsNetworkAccessManager.instance()
request = QNetworkRequest(QUrl('https://api.example.com/data'))
reply = manager.get(request)
```

## Processing Provider (Optional)

To add sketching algorithms, set `hasProcessingProvider=yes` in metadata.txt and implement:

```python
from qgis.core import QgsProcessingProvider

class MyProvider(QgsProcessingProvider):
    def loadAlgorithms(self):
        self.addAlgorithm(MyAlgorithm())
    
    def id(self):
        return 'myprovider'
    
    def name(self):
        return 'My Provider'
```

## Persistent Settings with QSettings

Store user preferences across sessions:

```python
from qgis.PyQt.QtCore import QSettings

# Save settings
settings = QSettings()
settings.setValue('plugin_name/language', 'en')
settings.setValue('plugin_name/last_directory', '/path/to/dir')
settings.setValue('plugin_name/show_warnings', True)

# Load settings with defaults
language = settings.value('plugin_name/language', 'it')  # default: 'it'
last_dir = settings.value('plugin_name/last_directory', '')
show_warnings = settings.value('plugin_name/show_warnings', True)

# Remove settings
settings.remove('plugin_name/old_setting')
```

**Important**: Always prefix setting keys with your plugin name to avoid conflicts.

## Common Patterns

### Progress Dialog

Show progress for long operations:

```python
from qgis.PyQt.QtWidgets import QProgressDialog, QApplication

progress = QProgressDialog("Processing...", None, 0, 100, self)
progress.setWindowTitle("Operation Title")
progress.setMinimumDuration(0)
progress.setValue(0)
QApplication.processEvents()

for i in range(100):
    # Do work...
    progress.setValue(i)
    QApplication.processEvents()

progress.setValue(100)
```

### File Dialogs

Use Qt file dialogs for file selection:

```python
from qgis.PyQt.QtWidgets import QFileDialog

# Open file
file_path, _ = QFileDialog.getOpenFileName(
    self,
    self.tr("Select GeoPackage"),
    "",
    self.tr("GeoPackage (*.gpkg);;All files (*.*)")
)

# Save file
file_path, _ = QFileDialog.getSaveFileName(
    self,
    self.tr("Save Project"),
    "/default/path/filename.qgs",
    self.tr("QGIS Project (*.qgs)")
)

# Select directory
dir_path = QFileDialog.getExistingDirectory(
    self,
    self.tr("Select Directory"),
    ""
)
```

### Input Dialogs

Get user input with simple dialogs:

```python
from qgis.PyQt.QtWidgets import QInputDialog

# Text input
text, ok = QInputDialog.getText(
    self,
    self.tr("Rename Project"),
    self.tr("New name:"),
    QLineEdit.Normal,
    "default_value"
)

if ok and text:
    # Use the input
    print(f"User entered: {text}")
```

## Resources

### Documentation
- See `references/metadata_fields.md` for complete metadata.txt documentation
- See `references/pyqgis_snippets.md` for common PyQGIS code patterns
- Official QGIS Plugin Repository: https://plugins.qgis.org/

### Tools
- See `scripts/create_plugin.py` to generate plugin structure automatically
- Qt Linguist: Create and edit translation files (.ts)
- lrelease: Compile .ts files to .qm (or use custom TS translator)

### Templates
- See `assets/icon_template.svg` for icon template (24x24 or 32x32 PNG recommended)

### Key Learnings
- **Always wrap UI strings with `tr()`** - even if you only support one language initially
- **Use placeholders (`%1`, `%2`)** instead of f-strings for translatable text
- **Test with different QGIS versions** - especially Qt5 vs Qt6 compatibility
- **Keep metadata.txt bilingual** - use both `[en]` and `(en)` formats
- **Validate all SQL queries** - use parameterized queries to prevent injection
- **Clean up resources** - remove actions, toolbars, and translators in `unload()`
