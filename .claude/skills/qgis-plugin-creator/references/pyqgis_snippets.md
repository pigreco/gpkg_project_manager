# PyQGIS Common Snippets

Frequently used code patterns for QGIS plugin development.

## Project and Layers

### Get Current Project
```python
from qgis.core import QgsProject
project = QgsProject.instance()
```

### Get All Layers
```python
layers = project.mapLayers()  # dict {id: layer}
layer_list = list(project.mapLayers().values())
```

### Get Layer by Name
```python
layers = project.mapLayersByName('layer_name')
if layers:
    layer = layers[0]
```

### Get Selected Layer
```python
from qgis.utils import iface
layer = iface.activeLayer()
```

### Add Vector Layer
```python
from qgis.core import QgsVectorLayer
layer = QgsVectorLayer('/path/to/file.gpkg|layername=table', 'Display Name', 'ogr')
if layer.isValid():
    project.addMapLayer(layer)
```

## Interface (iface)

### Message Bar
```python
from qgis.core import Qgis
iface.messageBar().pushMessage(
    "Title", "Message text",
    level=Qgis.Success,  # Info, Warning, Critical, Success
    duration=5  # seconds, 0 = permanent
)
```

### Status Bar
```python
iface.mainWindow().statusBar().showMessage("Status message", 5000)  # ms
```

### Refresh Map Canvas
```python
iface.mapCanvas().refresh()
```

## File Dialogs

### Open File
```python
from qgis.PyQt.QtWidgets import QFileDialog

file_path, _ = QFileDialog.getOpenFileName(
    parent,
    "Select File",
    "",  # start directory
    "GeoPackage (*.gpkg);;All Files (*.*)"
)
```

### Save File
```python
file_path, _ = QFileDialog.getSaveFileName(
    parent,
    "Save File",
    "/suggested/path/file.gpkg",
    "GeoPackage (*.gpkg)"
)
```

### Select Directory
```python
dir_path = QFileDialog.getExistingDirectory(
    parent,
    "Select Directory",
    ""
)
```

## Message Boxes

### Information
```python
from qgis.PyQt.QtWidgets import QMessageBox
QMessageBox.information(parent, "Title", "Message")
```

### Warning
```python
QMessageBox.warning(parent, "Title", "Warning message")
```

### Error
```python
QMessageBox.critical(parent, "Title", "Error message")
```

### Confirmation
```python
reply = QMessageBox.question(
    parent, "Confirm",
    "Are you sure?",
    QMessageBox.Yes | QMessageBox.No,
    QMessageBox.No  # default
)
if reply == QMessageBox.Yes:
    # proceed
```

### Input Dialog
```python
from qgis.PyQt.QtWidgets import QInputDialog

text, ok = QInputDialog.getText(parent, "Title", "Enter value:")
if ok and text:
    # use text

number, ok = QInputDialog.getInt(parent, "Title", "Enter number:", 0, 0, 100)
```

## Settings

### Save Setting
```python
from qgis.PyQt.QtCore import QSettings
settings = QSettings()
settings.setValue('plugin_name/setting_key', value)
```

### Load Setting
```python
value = settings.value('plugin_name/setting_key', defaultValue)
```

## sketching Tools

### Run sketching Algorithm
```python
import sketching
result = sketching.run(
    "native:buffer",
    {
        'INPUT': layer,
        'DISTANCE': 100,
        'OUTPUT': 'memory:'
    }
)
output_layer = result['OUTPUT']
```

### Run with Sketching Dialog
```python
sketching.execAlgorithmDialog('native:buffer', {'INPUT': layer})
```

## GeoPackage Operations

### List Tables in GeoPackage
```python
import sqlite3
conn = sqlite3.connect('/path/to/file.gpkg')
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
conn.close()
```

### Check for QGIS Projects Table
```python
cursor.execute("""
    SELECT name FROM sqlite_master 
    WHERE type='table' AND name='qgis_projects'
""")
has_projects = cursor.fetchone() is not None
```

## Progress Dialog

```python
from qgis.PyQt.QtWidgets import QProgressDialog, QApplication

progress = QProgressDialog("Working...", "Cancel", 0, 100, parent)
progress.setWindowTitle("Progress")
progress.setMinimumDuration(0)

for i in range(100):
    if progress.wasCanceled():
        break
    progress.setValue(i)
    QApplication.processEvents()
    # do work

progress.setValue(100)
```

## Logging

```python
from qgis.core import QgsMessageLog, Qgis

QgsMessageLog.logMessage(
    "Log message",
    "PluginName",
    level=Qgis.Info  # Info, Warning, Critical
)
```

## Icons and Resources

### Load Icon from Plugin Directory
```python
import os
plugin_dir = os.path.dirname(__file__)
icon_path = os.path.join(plugin_dir, 'icon.png')
icon = QIcon(icon_path)
```

### Get QGIS Built-in Icons
```python
from qgis.PyQt.QtGui import QIcon
icon = QIcon(':/images/themes/default/mActionFileOpen.svg')
```

## Canvas and Map Tools

### Get Map Canvas
```python
canvas = iface.mapCanvas()
```

### Get Current Extent
```python
extent = canvas.extent()
```

### Zoom to Layer
```python
canvas.setExtent(layer.extent())
canvas.refresh()
```

### Zoom to Features
```python
box = layer.boundingBoxOfSelected()
canvas.setExtent(box)
canvas.refresh()
```
