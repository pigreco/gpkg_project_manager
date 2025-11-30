# -*- coding: utf-8 -*-
"""
GeoPackage Project Manager - Main Plugin Class
"""

from qgis.PyQt.QtWidgets import QAction
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtCore import QCoreApplication, QTranslator, QSettings, QLocale
from qgis.core import Qgis
import os

# Import custom TS translator as fallback
try:
    from .ts_translator import install_ts_translator
    TS_TRANSLATOR_AVAILABLE = True
except ImportError:
    TS_TRANSLATOR_AVAILABLE = False


class GeoPackageProjectManagerPlugin:
    """Main plugin class for GeoPackage Project Manager."""

    def __init__(self, iface):
        """Initialize plugin.

        Args:
            iface: QGIS interface instance
        """
        self.iface = iface
        self.plugin_dir = os.path.dirname(__file__)
        self.actions = []
        self.menu = self.tr('&GeoPackage Project Manager')
        self.toolbar = None
        self.dialog = None

        # Initialize translation
        self.translator = None
        self.load_translator()

    def load_translator(self, locale=None):
        """Load translator for the plugin.

        Priority:
        1. User preference (if set via language selector)
        2. QGIS locale
        3. Italian (default)

        Args:
            locale: Language code (e.g., 'en', 'it'). If None, uses priority order.
        """
        settings = QSettings()

        # Determine locale to use
        if locale is None:
            # Check user preference first
            locale = settings.value('gpkg_project_manager/language', None)

            if locale is None:
                # Fall back to QGIS locale
                qgis_locale = settings.value('locale/userLocale', 'it_IT')
                if qgis_locale:
                    locale = qgis_locale[0:2]
                else:
                    locale = 'it'

        # Remove old translator if exists
        if self.translator:
            QCoreApplication.removeTranslator(self.translator)
            self.translator = None

        # Load new translator
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'gpkg_project_manager_{}.qm'.format(locale)
        )

        # Try to load .qm file first
        if os.path.exists(locale_path):
            self.translator = QTranslator()
            if self.translator.load(locale_path):
                QCoreApplication.installTranslator(self.translator)
                print(f"✓ QM Translator loaded: {locale}")
                test = QCoreApplication.translate('GeoPackageProjectManagerDialog', '📂 Sfoglia')
                print(f"✓ Test translation: {test}")
                if test != '📂 Sfoglia':  # Translation worked
                    return True
                else:
                    print(f"⚠️  QM loaded but translation not working, trying TS fallback...")

        # Fallback to .ts file direct loading
        if TS_TRANSLATOR_AVAILABLE:
            ts_path = os.path.join(
                self.plugin_dir,
                'i18n',
                'gpkg_project_manager_{}.ts'.format(locale)
            )
            if os.path.exists(ts_path):
                print(f"Using TS translator fallback for {locale}")
                if install_ts_translator(ts_path):
                    test = QCoreApplication.translate('GeoPackageProjectManagerDialog', '📂 Sfoglia')
                    print(f"✓ TS Test translation: {test}")
                    return True

        print(f"❌ No working translator found for {locale}")
        return False

    def tr(self, message):
        """Translate string using Qt translation API.

        Args:
            message: String to translate

        Returns:
            Translated string
        """
        return QCoreApplication.translate('GeoPackageProjectManager', message)

    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None
    ):
        """Add a toolbar icon to the toolbar.

        Args:
            icon_path: Path to the icon file
            text: Text that should be shown in menu items
            callback: Function to be called when action is triggered
            enabled: Whether the action is enabled by default
            add_to_menu: Whether to add action to plugin menu
            add_to_toolbar: Whether to add action to toolbar
            status_tip: Optional text to show in status bar
            whats_this: Optional text for whats this help
            parent: Parent widget for the action

        Returns:
            The action that was created
        """
        icon = QIcon(icon_path)
        action = QAction(icon, text, parent or self.iface.mainWindow())
        action.triggered.connect(callback)
        action.setEnabled(enabled)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            if self.toolbar is None:
                self.toolbar = self.iface.addToolBar('GeoPackage Project Manager')
                self.toolbar.setObjectName('GeoPackageProjectManagerToolbar')
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToDatabaseMenu(self.menu, action)

        self.actions.append(action)
        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""
        icon_path = os.path.join(self.plugin_dir, 'icon.png')

        self.add_action(
            icon_path,
            text=self.tr('Open GeoPackage Project Manager'),
            callback=self.run,
            status_tip=self.tr('Gestisci i progetti QGIS in GeoPackage'),
            parent=self.iface.mainWindow()
        )

    def unload(self):
        """Remove the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginDatabaseMenu(self.menu, action)
            if self.toolbar:
                self.iface.removeToolBarIcon(action)

        # Remove toolbar
        if self.toolbar:
            del self.toolbar
            self.toolbar = None

        # Remove translator
        if self.translator:
            QCoreApplication.removeTranslator(self.translator)

    def change_language(self, locale):
        """Change plugin language and reload dialog.

        Args:
            locale: Language code (e.g., 'en', 'it')
        """
        # Save user preference
        settings = QSettings()
        settings.setValue('gpkg_project_manager/language', locale)

        # Reload translator
        self.load_translator(locale)

        # Force recreation of dialog on next open
        if self.dialog:
            self.dialog.close()
            self.dialog = None

    def run(self):
        """Run method that performs all the real work."""
        # Import dialog here to avoid loading it on QGIS startup
        from .dialogs import GeoPackageProjectManagerDialog

        # Create the dialog if it doesn't exist
        if self.dialog is None:
            self.dialog = GeoPackageProjectManagerDialog(self.iface.mainWindow(), self)

        # Show the dialog
        self.dialog.show()
        # Run the dialog event loop
        result = self.dialog.exec()

        # Reset dialog reference when closed to allow recreation with fresh state
        if result:
            self.dialog = None
