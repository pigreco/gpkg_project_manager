# Sistema di Protezione con Trigger SQLite

## Panoramica

Il plugin GeoPackage Project Manager implementa un sistema di protezione basato su **trigger SQLite** per impedire modifiche e cancellazioni non autorizzate dei progetti salvati nel GeoPackage.

## Come Funziona

### 1. Trigger di Protezione

Quando si apre un GeoPackage, il plugin crea automaticamente due trigger:

#### `prevent_project_update`
Impedisce l'UPDATE sulla tabella `qgis_projects`:
```sql
CREATE TRIGGER IF NOT EXISTS prevent_project_update
BEFORE UPDATE ON qgis_projects
WHEN (SELECT bypass_active FROM qgis_projects_trigger_bypass WHERE id = 1) = 0
BEGIN
    SELECT RAISE(ABORT, '🔒 Modifica non consentita. I progetti sono protetti da modifiche. Crea una nuova versione invece di sovrascrivere.');
END
```

#### `prevent_project_delete`
Impedisce il DELETE sulla tabella `qgis_projects`:
```sql
CREATE TRIGGER IF NOT EXISTS prevent_project_delete
BEFORE DELETE ON qgis_projects
WHEN (SELECT bypass_active FROM qgis_projects_trigger_bypass WHERE id = 1) = 0
BEGIN
    SELECT RAISE(ABORT, '🔒 Eliminazione non consentita. I progetti sono protetti da cancellazione.');
END
```

### 2. Tabella di Controllo

Per permettere operazioni autorizzate dal plugin, viene creata una tabella di controllo:

```sql
CREATE TABLE IF NOT EXISTS qgis_projects_trigger_bypass (
    id INTEGER PRIMARY KEY CHECK (id = 1),
    bypass_active INTEGER DEFAULT 0
)
```

- `bypass_active = 0`: I trigger sono **attivi** (modifiche bloccate)
- `bypass_active = 1`: I trigger sono **disabilitati temporaneamente** (operazioni autorizzate)

### 3. Funzioni di Gestione

Il plugin fornisce tre funzioni per gestire i trigger:

#### `crea_trigger_protezione(conn)`
Crea i trigger e la tabella di controllo quando si carica un GeoPackage.

#### `abilita_bypass_trigger(conn)`
Disabilita temporaneamente i trigger per operazioni autorizzate:
```python
self.abilita_bypass_trigger(conn)
# Esegui operazione autorizzata (UPDATE/DELETE)
self.disabilita_bypass_trigger(conn)
```

#### `disabilita_bypass_trigger(conn)`
Riattiva i trigger dopo un'operazione autorizzata.

#### `rimuovi_trigger_protezione(conn)`
Rimuove completamente i trigger e la tabella di controllo (se necessario).

## Operazioni Protette

### ✅ Operazioni Autorizzate (con bypass automatico)

Il plugin gestisce automaticamente il bypass dei trigger per queste operazioni:

1. **Sovrascrittura progetto** (`salva_progetto` con `force_overwrite=True`)
   - L'utente conferma la sovrascrittura
   - Il bypass viene abilitato prima del `project.write()`
   - Il bypass viene disabilitato dopo il salvataggio

2. **Rinomina progetto** (`rinomina_progetto`)
   - Abilita bypass → UPDATE name → Disabilita bypass

3. **Eliminazione progetto** (`elimina_progetto`)
   - L'utente conferma l'eliminazione
   - Abilita bypass → DELETE → Disabilita bypass

### ❌ Operazioni Bloccate (senza autorizzazione)

Queste operazioni vengono bloccate dai trigger:

1. **Modifiche dirette al database** (tramite SQL esterno)
   ```sql
   -- BLOCCATO ❌
   UPDATE qgis_projects SET content = ... WHERE name = 'progetto1';

   -- Errore: 🔒 Modifica non consentita. I progetti sono protetti da modifiche.
   ```

2. **Cancellazioni dirette** (tramite SQL esterno)
   ```sql
   -- BLOCCATO ❌
   DELETE FROM qgis_projects WHERE name = 'progetto1';

   -- Errore: 🔒 Eliminazione non consentita. I progetti sono protetti da cancellazione.
   ```

3. **Modifiche da altri strumenti** (DB Browser, DBeaver, ecc.)
   - Anche modifiche tramite altri software SQLite vengono bloccate

## Vantaggi

✅ **Protezione a livello database**: I trigger funzionano indipendentemente dall'applicazione
✅ **Protezione universale**: Funziona anche se il GeoPackage viene modificato da altri strumenti
✅ **Tracciabilità**: Impedisce modifiche accidentali o non autorizzate
✅ **Versioning forzato**: Incoraggia la creazione di nuove versioni invece della sovrascrittura

## Limitazioni

⚠️ **Permanenza**: I trigger rimangono nel GeoPackage fino a quando non vengono rimossi
⚠️ **Gestione errori**: Il plugin deve gestire correttamente gli errori per evitare che il bypass rimanga attivo
⚠️ **Operazioni di manutenzione**: Alcune operazioni di manutenzione potrebbero richiedere la rimozione temporanea dei trigger

## Disabilitazione dei Trigger

Se hai bisogno di disabilitare completamente i trigger (ad esempio per operazioni di manutenzione avanzate), puoi:

### Opzione 1: Tramite SQL (manualmente)
```sql
DROP TRIGGER IF EXISTS prevent_project_update;
DROP TRIGGER IF EXISTS prevent_project_delete;
DROP TABLE IF EXISTS qgis_projects_trigger_bypass;
```

### Opzione 2: Tramite codice Python
```python
conn = sqlite3.connect('percorso/al/file.gpkg')
dialog = GeoPackageProjectManagerDialog()
dialog.rimuovi_trigger_protezione(conn)
conn.close()
```

## Verifica dello Stato

Per verificare se i trigger sono attivi nel tuo GeoPackage:

```sql
-- Lista dei trigger
SELECT name, sql FROM sqlite_master
WHERE type='trigger'
AND (name='prevent_project_update' OR name='prevent_project_delete');

-- Stato bypass
SELECT bypass_active FROM qgis_projects_trigger_bypass WHERE id = 1;
-- 0 = Trigger attivi (protezione ON)
-- 1 = Trigger disabilitati (protezione OFF)
```

## Test Manuale

Per testare che i trigger funzionino:

```sql
-- 1. Prova a modificare un progetto (dovrebbe fallire)
UPDATE qgis_projects SET name = 'nuovo_nome' WHERE name = 'progetto_test';
-- Risultato atteso: Errore 🔒

-- 2. Prova a eliminare un progetto (dovrebbe fallire)
DELETE FROM qgis_projects WHERE name = 'progetto_test';
-- Risultato atteso: Errore 🔒

-- 3. Abilita bypass e riprova (dovrebbe funzionare)
UPDATE qgis_projects_trigger_bypass SET bypass_active = 1 WHERE id = 1;
UPDATE qgis_projects SET name = 'nuovo_nome' WHERE name = 'progetto_test';
-- Risultato atteso: Successo ✅

-- 4. IMPORTANTE: Disabilita sempre il bypass dopo il test!
UPDATE qgis_projects_trigger_bypass SET bypass_active = 0 WHERE id = 1;
```

## Domande Frequenti (FAQ)

### ❓ La protezione vale per un singolo progetto o per tutti?

**R:** La protezione si applica a **TUTTI i progetti** all'interno del GeoPackage.

**Dettagli tecnici:**
- I trigger SQLite operano a livello di **TABELLA** (`qgis_projects`)
- La tabella `qgis_projects` contiene **TUTTI** i progetti del GeoPackage
- Non è possibile proteggere selettivamente solo alcuni progetti

**Esempio:**
```
GeoPackage: progetti_2025.gpkg
├── progetto_A  ← Protetto
├── progetto_B  ← Protetto
├── progetto_C  ← Protetto
└── progetto_D  ← Protetto

Tutti insieme! Non è possibile proteggere solo A e B.
```

**Soluzione per protezione selettiva:**
Usa GeoPackage separati:
```
produzione.gpkg     → Protezione ATTIVA (progetti A, B)
sviluppo.gpkg       → Protezione DISATTIVATA (progetti C, D)
```

### ❓ Posso proteggere un progetto ma non gli altri nello stesso GeoPackage?

**R:** No, tecnicamente non è possibile con i trigger SQLite standard. La protezione è "tutto o niente" per l'intero file GeoPackage.

### ❓ Se disabilito la protezione, vale per tutti i progetti?

**R:** Sì, esattamente. Quando disabiliti la protezione tramite "🔓 Disabilita Temporanea", rimuovi i trigger dall'intera tabella `qgis_projects`, quindi TUTTI i progetti diventano modificabili.

## Note di Sicurezza

🔐 **Importante**: I trigger proteggono i dati ma **NON sostituiscono** un sistema di backup completo.
💾 Continua a fare backup regolari dei tuoi GeoPackage.
⚠️ In caso di corruzione del database, i trigger potrebbero complicare il recupero dati.
📦 **Ambito protezione**: Ricorda che la protezione è a livello di GeoPackage intero, non di singolo progetto.

## Integrazione con il Plugin

Il sistema di trigger è completamente integrato nel workflow del plugin:

1. **All'apertura del GeoPackage**: I trigger vengono creati automaticamente
2. **Durante il salvataggio/modifica**: Il bypass viene gestito automaticamente
3. **Nessuna azione richiesta**: L'utente non deve fare nulla, la protezione è trasparente

---

**Versione**: 3.5.0
**Data**: 2025-12-20
**Autore**: Salvatore Fiandaca
