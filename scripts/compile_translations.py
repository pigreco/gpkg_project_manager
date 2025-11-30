#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script per compilare i file di traduzione .ts in .qm
Richiede PyQt5 o PyQt6
"""

import os
import sys
from pathlib import Path

def compile_translations():
    """Compila tutti i file .ts nella directory i18n."""

    # Trova la directory base del plugin
    script_dir = Path(__file__).parent
    plugin_dir = script_dir.parent
    i18n_dir = plugin_dir / 'i18n'

    if not i18n_dir.exists():
        print(f"❌ Directory i18n non trovata: {i18n_dir}")
        return False

    # Prova a importare PyQt
    try:
        from PyQt5.QtCore import QLibraryInfo, QProcess
        qt_module = 'PyQt5'
    except ImportError:
        try:
            from PyQt6.QtCore import QLibraryInfo, QProcess
            qt_module = 'PyQt6'
        except ImportError:
            print("❌ PyQt5 o PyQt6 non trovato. Installa uno dei due:")
            print("   pip install PyQt5")
            print("   o")
            print("   pip install PyQt6")
            return False

    print(f"✓ Usando {qt_module}")
    print(f"✓ Directory traduzioni: {i18n_dir}")
    print()

    # Trova lrelease
    try:
        if hasattr(QLibraryInfo, 'location'):  # PyQt5
            bin_path = QLibraryInfo.location(QLibraryInfo.BinariesPath)
        else:  # PyQt6
            bin_path = QLibraryInfo.path(QLibraryInfo.LibraryPath.BinariesPath)
    except:
        bin_path = None

    # Cerca lrelease
    lrelease_names = ['lrelease', 'lrelease-qt5', 'lrelease-qt6']
    lrelease_cmd = None

    # Cerca nei percorsi standard
    for name in lrelease_names:
        # Cerca nel PATH
        from shutil import which
        cmd = which(name)
        if cmd:
            lrelease_cmd = cmd
            break

    # Cerca nella directory bin di Qt
    if not lrelease_cmd and bin_path:
        for name in lrelease_names:
            cmd = os.path.join(bin_path, name)
            if os.path.exists(cmd):
                lrelease_cmd = cmd
                break
            # Prova con .exe su Windows
            cmd_exe = cmd + '.exe'
            if os.path.exists(cmd_exe):
                lrelease_cmd = cmd_exe
                break

    if not lrelease_cmd:
        print("❌ lrelease non trovato!")
        print()
        print("Soluzioni:")
        print("1. Installa Qt Tools:")
        print("   - Linux: sudo apt-get install qttools5-dev-tools")
        print("   - macOS: brew install qt5")
        print("   - Windows: Incluso in Qt installer")
        print()
        print("2. Oppure usa il metodo manuale (vedi sotto)")
        return False

    print(f"✓ Trovato lrelease: {lrelease_cmd}")
    print()

    # Compila tutti i file .ts
    ts_files = list(i18n_dir.glob('*.ts'))

    if not ts_files:
        print(f"⚠️  Nessun file .ts trovato in {i18n_dir}")
        return True

    print(f"Trovati {len(ts_files)} file di traduzione:")
    compiled = 0
    errors = 0

    for ts_file in ts_files:
        qm_file = ts_file.with_suffix('.qm')
        print(f"  Compilazione: {ts_file.name} → {qm_file.name}...", end=' ')

        # Esegui lrelease
        process = QProcess()
        process.start(lrelease_cmd, [str(ts_file), '-qm', str(qm_file)])

        if not process.waitForFinished(5000):  # 5 secondi timeout
            print("❌ Timeout")
            errors += 1
            continue

        if process.exitCode() == 0 and qm_file.exists():
            size = qm_file.stat().st_size
            print(f"✓ ({size} bytes)")
            compiled += 1
        else:
            error_msg = process.readAllStandardError().data().decode('utf-8', errors='ignore')
            print(f"❌ Errore: {error_msg}")
            errors += 1

    print()
    print("=" * 50)
    print(f"✓ Compilati: {compiled}/{len(ts_files)}")
    if errors > 0:
        print(f"❌ Errori: {errors}")
    print("=" * 50)

    return errors == 0


def compile_manual():
    """Compila manualmente usando Python puro (metodo alternativo)."""
    print("Metodo manuale di compilazione non ancora implementato.")
    print("Usa lrelease per ora.")
    return False


if __name__ == '__main__':
    print("=" * 50)
    print("  Compilazione Traduzioni")
    print("  GeoPackage Project Manager")
    print("=" * 50)
    print()

    success = compile_translations()

    if success:
        print()
        print("✅ Compilazione completata con successo!")
        print()
        print("I file .qm sono pronti per essere inclusi nel plugin.")
        sys.exit(0)
    else:
        print()
        print("❌ Compilazione fallita.")
        print()
        print("METODO ALTERNATIVO:")
        print("Puoi compilare manualmente con:")
        print("  lrelease i18n/*.ts")
        sys.exit(1)
