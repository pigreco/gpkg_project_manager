# Changelog - Sistema Trigger Protezione

## [3.7.1] - 2025-12-20

### 🔧 UX Migliorata

**Problema risolto:** Il menu "Gestione Protezione" nel menu contestuale di ogni progetto era fuorviante, suggerendo che la protezione fosse a livello di singolo progetto invece che dell'intero GeoPackage.

**Modifiche implementate:**

1. **Rimosso menu contestuale progetti**
   - Eliminato il sottomenu "🔒 Gestione Protezione" dal menu ⋮ di ogni progetto
   - Il menu a livello di progetto era semanticamente scorretto

2. **Aggiunto indicatore a livello GeoPackage**
   - Nuovo indicatore visibile sulla riga Info: `ℹ️ Info: 2.4 MB • 5 progetti  •  🔒 Protezione: ATTIVA ✅ [⚙️]`
   - Stati visivi con colori:
     - `ATTIVA ✅` (verde) - 2 trigger presenti
     - `DISATTIVATA` (rosso) - 0 trigger
     - `PARZIALE ⚠️` (arancione) - 1 trigger
   - Pulsante ⚙️ per accesso al menu gestione

3. **Menu protezione a livello GeoPackage**
   - Il menu appare ora nel contesto corretto (GeoPackage intero)
   - Chiarisce visivamente che la protezione vale per tutti i progetti
   - Tre opzioni disponibili:
     - ℹ️ Stato Protezione
     - 🔓 Disabilita Temporanea
     - 🔐 Ripristina Protezione

### 🎯 Chiarimenti Documentazione

**Aggiornate tutte le FAQ** per evidenziare:
- La protezione è a livello di TABELLA `qgis_projects`
- TUTTI i progetti nel GeoPackage sono protetti insieme
- NON è possibile protezione selettiva per singoli progetti
- Soluzione: usare GeoPackage separati per progetti protetti/non protetti

**File aggiornati:**
- `README_TRIGGERS.md` - Aggiunta sezione "IMPORTANTE: Protezione a Livello GeoPackage"
- `TRIGGERS_PROTECTION.md` - Aggiunta sezione FAQ con 3 domande principali
- `INTERFACCIA_GUI_v3.7.0.md` - Aggiunta sezione "Ambito della Protezione"
- `FAQ_PROTEZIONE.md` - Nuovo documento dedicato (500+ linee)

### 🔄 Technical Changes

**File modificati:**

1. **dialogs_table.py** (linee 611-665, 1955-1999)
   - Aggiunta `protezione_label` nell'info_layout
   - Aggiunto `btn_protezione_menu` con menu a tendina
   - Aggiunta funzione `aggiorna_stato_protezione()`
   - Rimosso sottomenu dal menu contestuale progetti (linee 1876-1881 → rimosso)

2. **dialogs.py** (linee 1216-1218, 1275-1277)
   - `disabilita_protezione_temporanea()`: aggiunta chiamata `aggiorna_stato_protezione()`
   - `ripristina_protezione()`: aggiunta chiamata `aggiorna_stato_protezione()`

### 📋 Benefici UX

✅ **Chiarezza**: Ovvio che la protezione è a livello GeoPackage
✅ **Feedback visivo**: Stato sempre visibile senza azioni
✅ **Accesso rapido**: Un solo clic su ⚙️
✅ **Semanticamente corretto**: Menu nel contesto giusto
✅ **Meno confusione**: No menu ripetuti per ogni progetto

---

## [3.7.0] - 2025-12-20 (Versione Iniziale)

### 🆕 Nuove Funzionalità

#### Sistema di Protezione con Trigger SQLite
Implementato un sistema completo di protezione basato su trigger SQLite per impedire modifiche non autorizzate ai progetti salvati nel GeoPackage.

**Caratteristiche principali:**
- ✅ Protezione automatica contro UPDATE non autorizzati
- ✅ Protezione automatica contro DELETE non autorizzati
- ✅ Sistema di bypass per operazioni autorizzate dal plugin
- ✅ Protezione universale (funziona anche con strumenti esterni)
- ✅ Implementazione trasparente per l'utente

### 📝 Modifiche ai File

#### `dialogs.py`

**Nuove Funzioni:**
1. `crea_trigger_protezione(conn)` - Linea 1010
   - Crea trigger di protezione quando si carica il GeoPackage
   - Crea tabella di controllo `qgis_projects_trigger_bypass`
   - Gestisce errori senza interrompere l'esecuzione

2. `abilita_bypass_trigger(conn)` - Linea 1059
   - Abilita temporaneamente il bypass dei trigger
   - Usato prima di operazioni autorizzate

3. `disabilita_bypass_trigger(conn)` - Linea 1072
   - Disabilita il bypass dopo operazioni autorizzate
   - Riattiva la protezione

4. `rimuovi_trigger_protezione(conn)` - Linea 1085
   - Rimuove completamente i trigger e la tabella di controllo
   - Usato per manutenzione o disabilitazione permanente

**Funzioni Modificate:**

1. `aggiorna_lista_progetti()` - Linea 902
   - Aggiunto: Chiamata a `crea_trigger_protezione(conn)` dopo verifica tabella progetti
   - Trigger vengono creati automaticamente all'apertura del GeoPackage

2. `salva_progetto(force_overwrite)` - Linea 1419
   - Aggiunto: Gestione bypass quando si sovrascrive un progetto esistente
   - Inizializzazione `conn_bypass` prima del try block
   - Abilita bypass se `is_new == False`
   - Disabilita bypass dopo `project.write()`
   - Gestione errori con cleanup del bypass

3. `elimina_progetto()` - Linea 1580
   - Aggiunto: Abilita bypass prima del DELETE
   - Aggiunto: Disabilita bypass dopo il DELETE
   - Aggiunta gestione errori con cleanup

4. `rinomina_progetto()` - Linea 1627
   - Aggiunto: Abilita bypass prima dell'UPDATE
   - Aggiunto: Disabilita bypass dopo l'UPDATE
   - Aggiunta gestione errori con cleanup

### 📄 Nuovi File

1. **TRIGGERS_PROTECTION.md**
   - Documentazione tecnica completa
   - Descrizione del funzionamento dei trigger
   - Esempi di utilizzo e configurazione
   - Sezione troubleshooting

2. **README_TRIGGERS.md**
   - Guida rapida per l'utente
   - Istruzioni di utilizzo
   - Test e verifica
   - FAQ e risoluzione problemi

3. **test_triggers.py**
   - Script automatico di test
   - Verifica esistenza trigger
   - Test blocco UPDATE/DELETE
   - Test funzionamento bypass
   - Report dettagliato dei risultati

4. **esempio_trigger.sql**
   - Esempi SQL pratici
   - Test manuali dei trigger
   - Comandi di verifica e debug
   - Ricreazione trigger se necessario

5. **CHANGELOG_TRIGGERS.md** (questo file)
   - Documentazione delle modifiche
   - Versioning delle funzionalità

### 🔧 Modifiche al Database

#### Nuova Tabella: `qgis_projects_trigger_bypass`
```sql
CREATE TABLE qgis_projects_trigger_bypass (
    id INTEGER PRIMARY KEY CHECK (id = 1),
    bypass_active INTEGER DEFAULT 0
);
```
- `id`: Chiave primaria fissa (sempre = 1)
- `bypass_active`: Flag controllo (0 = protezione ON, 1 = protezione OFF)

#### Nuovi Trigger

**1. prevent_project_update**
```sql
CREATE TRIGGER prevent_project_update
BEFORE UPDATE ON qgis_projects
WHEN (SELECT bypass_active FROM qgis_projects_trigger_bypass WHERE id = 1) = 0
BEGIN
    SELECT RAISE(ABORT, '🔒 Modifica non consentita...');
END
```

**2. prevent_project_delete**
```sql
CREATE TRIGGER prevent_project_delete
BEFORE DELETE ON qgis_projects
WHEN (SELECT bypass_active FROM qgis_projects_trigger_bypass WHERE id = 1) = 0
BEGIN
    SELECT RAISE(ABORT, '🔒 Eliminazione non consentita...');
END
```

### 🧪 Testing

**Test Implementati:**
- ✅ Verifica creazione automatica trigger
- ✅ Test blocco UPDATE senza autorizzazione
- ✅ Test blocco DELETE senza autorizzazione
- ✅ Test bypass per operazioni autorizzate
- ✅ Test cleanup bypass in caso di errori

**Come Testare:**
```bash
# Test automatico
python3 test_triggers.py /percorso/al/file.gpkg

# Test manuale
sqlite3 file.gpkg < esempio_trigger.sql
```

### 📊 Impatto sulle Prestazioni

**Impatto Minimo:**
- Trigger vengono valutati solo durante UPDATE/DELETE
- Query sulla tabella bypass è istantanea (1 record)
- Nessun overhead durante SELECT o INSERT
- Creazione trigger eseguita una sola volta all'apertura

### 🔐 Sicurezza

**Miglioramenti:**
- ✅ Protezione contro modifiche accidentali
- ✅ Protezione contro modifiche da strumenti esterni
- ✅ Tracciabilità: Solo il plugin può modificare progetti
- ✅ Versioning forzato: Incoraggia creazione nuove versioni

**Limitazioni:**
- ⚠️ Non protegge contro eliminazione file GeoPackage
- ⚠️ Non sostituisce sistema di backup
- ⚠️ Utenti con accesso SQL possono rimuovere trigger

### 🐛 Bug Fix

Nessun bug fix in questa release (nuova funzionalità).

### 🔄 Compatibilità

**Retrocompatibilità:**
- ✅ Funziona con GeoPackage esistenti
- ✅ Trigger vengono creati automaticamente
- ✅ Non richiede migrazione dati
- ✅ Compatibile con versioni precedenti del plugin

**Compatibilità Sistema:**
- ✅ SQLite 3.x
- ✅ QGIS 3.x
- ✅ Python 3.6+
- ✅ Qt5 e Qt6

### 📚 Documentazione

**Nuova Documentazione:**
- TRIGGERS_PROTECTION.md (tecnica, 350+ linee)
- README_TRIGGERS.md (utente, 150+ linee)
- Commenti inline nel codice
- Esempi SQL pratici

### 🚀 Migrazione

**Per utenti esistenti:**
1. Aggiorna il plugin alla versione 3.5.0
2. Apri un GeoPackage esistente
3. I trigger vengono creati automaticamente
4. Nessuna azione richiesta

**Rimozione (se necessario):**
```sql
DROP TRIGGER IF EXISTS prevent_project_update;
DROP TRIGGER IF EXISTS prevent_project_delete;
DROP TABLE IF EXISTS qgis_projects_trigger_bypass;
```

### 🎯 Prossimi Sviluppi

**Possibili migliorie future:**
- [ ] Opzione UI per abilitare/disabilitare protezione
- [ ] Log delle operazioni bloccate
- [ ] Trigger configurabili (solo UPDATE, solo DELETE, etc.)
- [ ] Sistema di permessi per utenti multipli
- [ ] Audit trail delle modifiche autorizzate

### 👥 Crediti

- **Sviluppatore:** Salvatore Fiandaca
- **Richiesta Feature:** Utente (domanda su trigger GeoPackage)
- **Data Implementazione:** 2025-12-20
- **Versione Plugin:** 3.5.0

### 📞 Supporto

Per problemi o domande:
- Consulta: README_TRIGGERS.md
- Documentazione tecnica: TRIGGERS_PROTECTION.md
- Script di test: test_triggers.py
- Email: pigrecoinfinito@gmail.com

---

**Note:** Questa implementazione risponde alla domanda "tramite trigger su geopackage è possibile impedire la modifica del progetto salvato dentro il geopackage?" con una soluzione completa e funzionante.
