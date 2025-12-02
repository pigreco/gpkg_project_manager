# 📋 Checklist Sviluppo e Release

Questo documento contiene tutte le checklist per gestire correttamente modifiche, nuove funzionalità e release del plugin.

---

## 🎯 Checklist Nuova Funzionalità

Quando aggiungi una nuova funzionalità, segui questi passaggi:

### 1. 💻 Implementazione Codice
- [ ] Implementa la funzionalità in `dialogs.py` o altri file Python
- [ ] Aggiungi gestione errori appropriata
- [ ] Verifica compatibilità Qt5/Qt6 (usa `get_qt_enum()` per gli enum)
- [ ] Aggiungi docstring ai nuovi metodi
- [ ] Testa la funzionalità su Qt5 e Qt6

### 2. 🎨 Interfaccia Utente
- [ ] Aggiungi elementi UI necessari (pulsanti, label, ecc.)
- [ ] Applica stili CSS coerenti con `MODERN_STYLE`
- [ ] Aggiungi tooltip descrittivi
- [ ] Verifica layout su diverse risoluzioni

### 3. 🌍 Traduzioni
- [ ] Identifica tutte le nuove stringhe da tradurre
- [ ] Aggiungi traduzioni in `i18n/gpkg_project_manager_en.ts`
- [ ] Formato corretto: `<source>` (italiano) e `<translation>` (inglese)
- [ ] Testa che le traduzioni funzionino correttamente

### 4. 📚 Documentazione
- [ ] **README.md**: Aggiungi la funzionalità nella sezione appropriata
  - Aggiorna "Funzionalità Principali" se applicabile
  - Aggiungi istruzioni nella sezione "Utilizzo"
  - Aggiungi esempi o casi d'uso se rilevanti
- [ ] **CHANGELOG.md**: Aggiungi voce nella versione corrente
  - Usa emoji appropriati (🎉 Aggiunto, 🛠️ Corretto, ecc.)
  - Descrizione chiara e concisa
- [ ] **metadata.txt**: Aggiorna changelog italiano e inglese
- [ ] Aggiorna screenshot se l'UI è cambiata

### 5. 🧪 Testing
- [ ] Testa la funzionalità manualmente
- [ ] Testa con Qt5 (se disponibile)
- [ ] Testa con Qt6
- [ ] Verifica che non ci siano regressioni
- [ ] Testa con diversi file GeoPackage

### 6. 🔍 Verifica Finale
- [ ] Controlla che non ci siano errori di sintassi
- [ ] Verifica che tutti i file siano salvati
- [ ] Esegui una build di test del plugin

---

## 🐛 Checklist Bug Fix

Quando correggi un bug:

### 1. 🔧 Correzione
- [ ] Identifica e correggi il problema
- [ ] Aggiungi gestione errori se mancante
- [ ] Testa la correzione

### 2. 📚 Documentazione
- [ ] **CHANGELOG.md**: Aggiungi nella sezione "🛠️ Corretto"
- [ ] **metadata.txt**: Aggiungi nel changelog se significativo
- [ ] README.md: Aggiorna FAQ se applicabile

### 3. 🧪 Testing
- [ ] Verifica che il bug sia risolto
- [ ] Testa che non ci siano regressioni
- [ ] Testa su Qt5 e Qt6

---

## 🚀 Checklist Release Nuova Versione

Quando prepari una nuova release:

### 1. 📌 Versione
Aggiorna il numero di versione in TUTTI questi file:

- [ ] **metadata.txt**: Campo `version=X.X.X` (riga 6)
- [ ] **dialogs.py**: Label versione nella GUI (cerca "Qt5/Qt6 Compatible")
- [ ] **i18n/gpkg_project_manager_en.ts**: Stringa versione GUI
- [ ] **README.md**: Aggiungi sezione nel Changelog
- [ ] **CHANGELOG.md**: Aggiungi nuova sezione `## [X.X.X] - YYYY-MM-DD`

### 2. 📝 Changelog Completo
Assicurati che il changelog sia completo in:

- [ ] **CHANGELOG.md**: Formato completo con categorie
  - 🎉 Aggiunto
  - 🛠️ Corretto
  - 🔄 Modificato
  - 🌍 Traduzioni
  - 📚 Documentazione
- [ ] **metadata.txt**: Changelog IT (campo `changelog=`)
- [ ] **metadata.txt**: Changelog EN (campo `changelog[en]=`)
- [ ] **README.md**: Sezione changelog aggiornata

### 3. 📚 Documentazione
- [ ] README.md aggiornato con nuove funzionalità
- [ ] Screenshot aggiornati se necessario
- [ ] Video demo aggiornato se cambio UI significativo
- [ ] FAQ aggiornate se necessario

### 4. 🌍 Traduzioni
- [ ] Tutte le stringhe tradotte in inglese
- [ ] File `.ts` validato (XML corretto)
- [ ] Traduzioni testate in entrambe le lingue

### 5. 🧪 Testing Pre-Release
- [ ] Test completo di tutte le funzionalità
- [ ] Test su Qt5 (se disponibile)
- [ ] Test su Qt6
- [ ] Test su Windows, Linux, macOS (se possibile)
- [ ] Verifica compatibilità con diverse versioni QGIS (3.x)

### 6. 📦 Build e Package
- [ ] Esegui `scripts/create_zip.sh` per creare il package
- [ ] Verifica contenuto dello ZIP
- [ ] Testa installazione dello ZIP in QGIS pulito
- [ ] Verifica che il plugin si carichi correttamente

### 7. 🏷️ Git e GitHub
- [ ] Commit di tutti i file modificati
- [ ] Tag della versione: `git tag -a vX.X.X -m "Release X.X.X"`
- [ ] Push del tag: `git push origin vX.X.X`
- [ ] Crea release su GitHub con note di rilascio
- [ ] Allega il file ZIP alla release

---

## 📋 File da Aggiornare - Quick Reference

### Per OGNI modifica:
1. **Codice**: `dialogs.py`, `main.py`, ecc.
2. **Traduzioni**: `i18n/gpkg_project_manager_en.ts`

### Per nuove funzionalità:
1. **Codice** (come sopra)
2. **Traduzioni** (come sopra)
3. **README.md**: Sezioni "Funzionalità" e "Utilizzo"
4. **CHANGELOG.md**: Nuova voce nella versione corrente
5. **metadata.txt**: Changelog IT e EN

### Per nuova release:
1. **metadata.txt**: Versione + Changelog IT/EN
2. **dialogs.py**: Versione GUI
3. **i18n/gpkg_project_manager_en.ts**: Versione GUI tradotta
4. **README.md**: Changelog
5. **CHANGELOG.md**: Nuova sezione versione
6. **Git**: Tag e release

---

## 🎨 Standard di Codice

### Stile Codice
- Usa 4 spazi per indentazione
- Docstring per metodi pubblici
- Commenti in italiano per logica complessa
- Nomi variabili in italiano per coerenza con codebase esistente

### Compatibilità Qt5/Qt6
```python
# ✅ CORRETTO - usa get_qt_enum()
UserRole = get_qt_enum(Qt, 'UserRole')
EventToolTip = get_qt_enum(QEvent, 'ToolTip')

# ❌ SBAGLIATO - non usare direttamente
role = Qt.UserRole  # Non funziona su Qt6!
```

### Traduzioni
```xml
<!-- ✅ CORRETTO -->
<message>
    <source>Testo in italiano</source>
    <translation>English text</translation>
</message>

<!-- ❌ SBAGLIATO - manca traduzione -->
<message>
    <source>Testo in italiano</source>
    <translation></translation>
</message>
```

### Gestione Errori
```python
# ✅ CORRETTO
try:
    # operazione
except Exception as e:
    import traceback
    self.mostra_errore(
        self.tr("Errore"),
        self.tr("Descrizione errore:\n{}").format(str(e) + "\n\n" + traceback.format_exc())
    )
```

---

## 🔍 Verifica Pre-Commit

Prima di ogni commit, verifica:

- [ ] Nessun errore di sintassi Python
- [ ] File `.ts` è XML valido (`xmllint --noout file.ts`)
- [ ] Nessun file temporaneo o `__pycache__` incluso
- [ ] Messaggi di debug rimossi (print, console.log, ecc.)
- [ ] Commit message descrittivo

---

## 📞 Supporto

Per domande o dubbi:
- GitHub Issues: https://github.com/pigreco/gpkg_project_manager/issues
- Email: pigrecoinfinito@gmail.com

---

**Nota**: Mantieni questo file aggiornato quando aggiungi nuovi processi o standard!

---

## 📊 Template Commit Messages

### Nuova funzionalità
```
feat: aggiungi [nome funzionalità]

- Implementazione in dialogs.py
- Traduzioni IT/EN
- Documentazione aggiornata
```

### Bug fix
```
fix: correggi [descrizione bug]

- Problema: [descrizione]
- Soluzione: [descrizione]
- Test: [come testato]
```

### Documentazione
```
docs: aggiorna [cosa]

- README.md
- CHANGELOG.md
- [altri file]
```

### Release
```
release: versione X.X.X

Nuove funzionalità:
- [elenco]

Bug fix:
- [elenco]

Vedi CHANGELOG.md per dettagli completi.
```
