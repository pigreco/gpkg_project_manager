#!/usr/bin/env python3
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
            if not os.path.exists(ts_path):
                print(f"TS file not found: {ts_path}")
                return False

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
                        source = source_elem.text if source_elem.text else ''
                        translation = translation_elem.text if translation_elem.text else ''

                        # Skip obsolete or unfinished translations
                        trans_type = translation_elem.get('type', '')
                        if trans_type in ('obsolete', 'unfinished'):
                            continue

                        # Store translation
                        if source and translation:
                            self.translations[context_name][source] = translation

            self.loaded = True
            print(f"✓ TS Translator loaded from {ts_path}")
            print(f"✓ Loaded {len(self.translations)} contexts with {sum(len(v) for v in self.translations.values())} translations")
            return True

        except Exception as e:
            print(f"❌ Error loading TS file: {e}")
            import traceback
            traceback.print_exc()
            return False

    def translate(self, context, source):
        """Translate a string."""
        if not self.loaded:
            return source

        # Look up translation
        if context in self.translations:
            if source in self.translations[context]:
                return self.translations[context][source]

        # Return original if not found
        return source


# Singleton instance
_ts_translator = None


def get_ts_translator():
    """Get the global TS translator instance."""
    global _ts_translator
    if _ts_translator is None:
        _ts_translator = TSTranslator()
    return _ts_translator


def install_ts_translator(ts_path):
    """Install a TS translator for the given .ts file."""
    translator = get_ts_translator()
    return translator.load(ts_path)
