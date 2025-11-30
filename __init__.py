# -*- coding: utf-8 -*-
"""
GeoPackage Project Manager
Gestisci i progetti QGIS direttamente all'interno di GeoPackage
"""


def classFactory(iface):
    """Load GeoPackageProjectManagerPlugin class.

    Args:
        iface: QGIS interface instance

    Returns:
        GeoPackageProjectManagerPlugin instance
    """
    from .main import GeoPackageProjectManagerPlugin
    return GeoPackageProjectManagerPlugin(iface)
