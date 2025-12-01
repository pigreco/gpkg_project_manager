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


def classFactory(iface):
    """Load GeoPackageProjectManagerPlugin class.

    Args:
        iface: QGIS interface instance

    Returns:
        GeoPackageProjectManagerPlugin instance
    """
    from .main import GeoPackageProjectManagerPlugin
    return GeoPackageProjectManagerPlugin(iface)
