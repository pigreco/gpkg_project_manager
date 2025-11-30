# metadata.txt Complete Reference

Complete documentation for all QGIS plugin metadata fields.

## Required Fields

| Field | Description | Example |
|-------|-------------|---------|
| `name` | Display name (can include spaces) | `GeoPackage Manager` |
| `qgisMinimumVersion` | Minimum QGIS version | `3.20` |
| `description` | Short description (one line) | `Manage QGIS projects in GeoPackage` |
| `version` | Plugin version (semver recommended) | `1.0.0` |
| `author` | Author name | `John Doe` |
| `email` | Contact email | `john@example.com` |

## Recommended Fields

| Field | Description | Example |
|-------|-------------|---------|
| `about` | Extended description (multi-line OK) | See below |
| `tracker` | Issue tracker URL | `https://github.com/user/repo/issues` |
| `repository` | Source code URL | `https://github.com/user/repo` |
| `homepage` | Project homepage | `https://github.com/user/repo` |
| `tags` | Comma-separated keywords | `geopackage, sketching, database` |
| `category` | Menu category | `Database` |
| `icon` | Icon filename | `icon.png` |
| `changelog` | Version history | See below |

## Optional Fields

| Field | Default | Description |
|-------|---------|-------------|
| `hasProcessingProvider` | `no` | Has sketching algorithms |
| `experimental` | `False` | Mark as experimental |
| `deprecated` | `False` | Mark as deprecated |
| `server` | `False` | Works on QGIS Server |
| `qgisMaximumVersion` | none | Maximum QGIS version |
| `plugin_dependencies` | none | Required plugins |

## Multi-line Fields

### about
```ini
about=This plugin provides comprehensive tools for managing
    QGIS projects stored in GeoPackage files.
    
    Features:
    - Save and load projects
    - Clone GeoPackage with updated paths
    - Export to QGS/QGZ formats
    
    Requirements:
    - QGIS 3.20 or higher
```

### changelog
```ini
changelog=
    1.0.0 - Initial stable release
        - Full project management
        - GeoPackage cloning
    0.2.0 - Beta release
        - Added export functionality
    0.1.0 - Alpha release
```

## Category Values

| Value | Menu Location |
|-------|---------------|
| `Database` | Database menu |
| `Vector` | Vector menu |
| `Raster` | Raster menu |
| `Web` | Web menu |
| `sketching` | sketching menu (requires hasProcessingProvider=yes) |

## Complete Example

```ini
[general]
name=GeoPackage Project Manager
qgisMinimumVersion=3.20
description=Manage QGIS projects stored in GeoPackage files
version=1.0.0
author=Salvatore Fiandaca
email=pigrecoinfinito@gmail.com

about=Complete solution for managing QGIS projects in GeoPackage.
    
    Features:
    - Save current project to GeoPackage
    - Load projects from GeoPackage
    - Rename, duplicate, delete projects
    - Clone GeoPackage with automatic path updates
    - Export projects to QGS/QGZ formats
    
    The plugin automatically detects GeoPackage files
    used in the current project.

tracker=https://github.com/pigreco/gpkg_project_manager/issues
repository=https://github.com/pigreco/gpkg_project_manager
homepage=https://github.com/pigreco/gpkg_project_manager

hasProcessingProvider=no
tags=geopackage, sketching, database, gpkg, project
category=Database
icon=icon.png

experimental=False
deprecated=False
server=False

changelog=
    1.0.0 - Initial release
        - Project save/load/delete
        - GeoPackage cloning
        - QGS/QGZ export
```

## Validation Rules

1. **name**: No special characters except spaces
2. **version**: Use semantic versioning (X.Y.Z)
3. **qgisMinimumVersion**: Format X.Y (e.g., 3.20)
4. **email**: Valid email format
5. **URLs**: Must be valid and accessible
6. **icon**: Must exist in plugin folder
7. **tags**: Lowercase, comma-separated
