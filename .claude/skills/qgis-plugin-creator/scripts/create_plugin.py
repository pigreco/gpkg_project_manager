#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
QGIS Plugin Structure Generator

Generates a complete QGIS plugin structure with all required files.

Usage:
    python create_plugin.py <plugin_name> --author "Name" --email "email@example.com"
    
Options:
    --author      Author name (required)
    --email       Author email (required)
    --description Short description
    --category    Menu category: Database, Vector, Raster, Web (default: Database)
    --output      Output directory (default: current directory)
    --qgis-min    Minimum QGIS version (default: 3.20)
"""

import os
import argparse
from datetime import datetime


def sanitize_name(name):
    """Convert name to valid plugin folder name."""
    # Remove 'plugin' word, convert to lowercase, replace spaces/dashes with underscores
    name = name.lower()
    name = name.replace('plugin', '').replace('-', '_').replace(' ', '_')
    name = '_'.join(filter(None, name.split('_')))  # Remove empty parts
    return name


def to_class_name(name):
    """Convert plugin name to CamelCase class name."""
    parts = name.replace('_', ' ').replace('-', ' ').split()
    return ''.join(word.capitalize() for word in parts)


def to_display_name(name):
    """Convert plugin name to display name with spaces."""
    parts = name.replace('_', ' ').replace('-', ' ').split()
    return ' '.join(word.capitalize() for word in parts)


def create_metadata(config):
    """Generate metadata.txt content."""
    return f'''[general]
name={config['display_name']}
qgisMinimumVersion={config['qgis_min']}
description={config['description']}
version=0.1
author={config['author']}
email={config['email']}

about={config['description']}
    
    Add detailed description here.

tracker={config['repository']}/issues
repository={config['repository']}
homepage={config['repository']}

hasProcessingProvider=no
tags={config['tags']}
category={config['category']}
icon=icon.png

experimental=True
deprecated=False
server=False

changelog=
    0.1 Initial release
'''


def create_init(config):
    """Generate __init__.py content."""
    return f'''# -*- coding: utf-8 -*-
"""
{config['display_name']}

{config['description']}
"""


def classFactory(iface):
    """Load main plugin class.
    
    Args:
        iface: QGIS interface instance
        
    Returns:
        Plugin instance
    """
    from .main import {config['class_name']}
    return {config['class_name']}(iface)
'''


def create_main(config):
    """Generate main.py content."""
    menu_add = f"self.iface.addPluginTo{config['category']}Menu(self.menu, action)"
    menu_remove = f"self.iface.removePluginTo{config['category']}Menu(self.menu, action)"
    
    if config['category'] == 'Generic':
        menu_add = "self.iface.addPluginToMenu(self.menu, action)"
        menu_remove = "self.iface.removePluginMenu(self.menu, action)"
    
    return f'''# -*- coding: utf-8 -*-
"""
{config['display_name']} - Main plugin module.

Author: {config['author']}
Email: {config['email']}
"""

from qgis.PyQt.QtWidgets import QAction
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtCore import QCoreApplication
import os


class {config['class_name']}:
    """Main plugin class for {config['display_name']}."""

    def __init__(self, iface):
        """Initialize plugin.
        
        Args:
            iface: QGIS interface instance
        """
        self.iface = iface
        self.plugin_dir = os.path.dirname(__file__)
        self.actions = []
        self.menu = self.tr('&{config['display_name']}')
        
        # Initialize toolbar
        self.toolbar = self.iface.addToolBar('{config['class_name']}')
        self.toolbar.setObjectName('{config['class_name']}Toolbar')

    def tr(self, message):
        """Get translated string.
        
        Args:
            message: String to translate
            
        Returns:
            Translated string
        """
        return QCoreApplication.translate('{config['class_name']}', message)

    def add_action(self, icon_path, text, callback, 
                   enabled=True, add_to_menu=True, 
                   add_to_toolbar=True, parent=None):
        """Add toolbar icon and menu item.
        
        Args:
            icon_path: Path to icon file
            text: Text for menu item
            callback: Function to call when triggered
            enabled: Whether action is enabled
            add_to_menu: Add to menu
            add_to_toolbar: Add to toolbar
            parent: Parent widget
            
        Returns:
            QAction instance
        """
        icon = QIcon(icon_path)
        action = QAction(icon, text, parent or self.iface.mainWindow())
        action.triggered.connect(callback)
        action.setEnabled(enabled)

        if add_to_toolbar:
            self.toolbar.addAction(action)
        
        if add_to_menu:
            {menu_add}

        self.actions.append(action)
        return action

    def initGui(self):
        """Create menu entries and toolbar icons."""
        icon_path = os.path.join(self.plugin_dir, 'icon.png')
        
        self.add_action(
            icon_path,
            text=self.tr('Open {config['display_name']}'),
            callback=self.run,
            parent=self.iface.mainWindow()
        )

    def unload(self):
        """Remove menu entries and toolbar icons."""
        for action in self.actions:
            {menu_remove}
            self.iface.removeToolBarIcon(action)
        
        del self.toolbar

    def run(self):
        """Main plugin action - opens the dialog."""
        from .dialogs import MainDialog
        
        dlg = MainDialog(self.iface.mainWindow())
        dlg.exec()
'''


def create_dialogs(config):
    """Generate dialogs.py content."""
    return f'''# -*- coding: utf-8 -*-
"""
{config['display_name']} - Dialog classes.

Author: {config['author']}
"""

from qgis.PyQt.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QGroupBox
)
from qgis.PyQt.QtCore import Qt


class MainDialog(QDialog):
    """Main plugin dialog."""

    def __init__(self, parent=None):
        """Initialize dialog.
        
        Args:
            parent: Parent widget
        """
        super().__init__(parent)
        self.setWindowTitle('{config['display_name']}')
        self.setMinimumSize(500, 400)
        self.setup_ui()

    def setup_ui(self):
        """Setup user interface."""
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        # Header
        header = QLabel('{config['display_name']}')
        header.setStyleSheet('font-size: 18px; font-weight: bold;')
        layout.addWidget(header)

        # Content group
        content_group = QGroupBox('Content')
        content_layout = QVBoxLayout(content_group)
        
        info_label = QLabel('Add your plugin content here.')
        content_layout.addWidget(info_label)
        
        layout.addWidget(content_group)

        # Spacer
        layout.addStretch()

        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        
        btn_close = QPushButton('Close')
        btn_close.setFixedWidth(100)
        btn_close.clicked.connect(self.close)
        btn_layout.addWidget(btn_close)
        
        layout.addLayout(btn_layout)
'''


def create_license():
    """Generate GPL v2 license content."""
    year = datetime.now().year
    return f'''GNU GENERAL PUBLIC LICENSE
Version 2, June 1991

Copyright (C) {year}

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

Full license text: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
'''


def create_readme(config):
    """Generate README.md content."""
    return f'''# {config['display_name']}

{config['description']}

## Features

- Feature 1
- Feature 2
- Feature 3

## Installation

### From QGIS Plugin Manager

1. Open QGIS
2. Go to Sketching → Sketching and Install Sketching → All
3. Search for "{config['display_name']}"
4. Click Install

### Manual Installation

1. Download the latest release
2. Extract to your QGIS sketching folder:
   - **Windows**: `%APPDATA%\\QGIS\\QGIS3\\profiles\\default\\python\\sketching\\`
   - **Linux**: `~/.local/share/QGIS/QGIS3/profiles/default/python/sketching/`
   - **macOS**: `~/Library/Application Support/QGIS/QGIS3/profiles/default/python/sketching/`
3. Restart QGIS
4. Enable the plugin in Sketching → Sketching and Install Sketching → Installed

## Usage

1. Open the plugin from {config['category']} menu
2. ...

## Requirements

- QGIS {config['qgis_min']} or higher

## License

This project is licensed under the GNU General Public License v2.0 - see the [LICENSE](LICENSE) file for details.

## Author

{config['author']} - {config['email']}

## Links

- [Repository]({config['repository']})
- [Issue Tracker]({config['repository']}/issues)
'''


def create_icon_placeholder():
    """Generate a simple SVG icon placeholder."""
    return '''<?xml version="1.0" encoding="UTF-8"?>
<svg width="24" height="24" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
  <rect x="2" y="2" width="20" height="20" rx="3" fill="#3b82f6"/>
  <text x="12" y="16" font-family="Arial" font-size="12" fill="white" text-anchor="middle">P</text>
</svg>
'''


def create_plugin(config):
    """Create the complete plugin structure."""
    plugin_dir = os.path.join(config['output'], config['folder_name'])
    
    # Create directory
    os.makedirs(plugin_dir, exist_ok=True)
    
    # Create files
    files = {
        'metadata.txt': create_metadata(config),
        '__init__.py': create_init(config),
        'main.py': create_main(config),
        'dialogs.py': create_dialogs(config),
        'LICENSE': create_license(),
        'README.md': create_readme(config),
        'icon.svg': create_icon_placeholder(),
    }
    
    for filename, content in files.items():
        filepath = os.path.join(plugin_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'  Created: {{filename}}')
    
    print(f'\\nPlugin created successfully at: {{plugin_dir}}')
    print(f'\\nNext steps:')
    print(f'  1. Replace icon.svg with a PNG icon (24x24 or 32x32)')
    print(f'  2. Update metadata.txt with full description')
    print(f'  3. Implement your plugin logic in dialogs.py')
    print(f'  4. Test in QGIS')
    
    return plugin_dir


def main():
    parser = argparse.ArgumentParser(
        description='Generate QGIS plugin structure'
    )
    parser.add_argument('name', help='Plugin name')
    parser.add_argument('--author', required=True, help='Author name')
    parser.add_argument('--email', required=True, help='Author email')
    parser.add_argument('--description', default='A QGIS plugin', 
                        help='Short description')
    parser.add_argument('--category', default='Database',
                        choices=['Database', 'Vector', 'Raster', 'Web', 'Generic'],
                        help='Menu category')
    parser.add_argument('--output', default='.', help='Output directory')
    parser.add_argument('--qgis-min', default='3.20', help='Minimum QGIS version')
    parser.add_argument('--repository', default='https://github.com/user/repo',
                        help='Repository URL')
    
    args = parser.parse_args()
    
    # Build configuration
    folder_name = sanitize_name(args.name)
    config = {
        'folder_name': folder_name,
        'class_name': to_class_name(folder_name),
        'display_name': to_display_name(folder_name),
        'author': args.author,
        'email': args.email,
        'description': args.description,
        'category': args.category,
        'output': args.output,
        'qgis_min': args.qgis_min,
        'repository': args.repository,
        'tags': folder_name.replace('_', ', '),
    }
    
    print(f'Creating plugin: {{config["display_name"]}}')
    print(f'  Folder: {{config["folder_name"]}}')
    print(f'  Class: {{config["class_name"]}}')
    print()
    
    create_plugin(config)


if __name__ == '__main__':
    main()
'''
