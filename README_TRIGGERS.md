# Sistema di Protezione Progetti con Trigger SQLite

## 🎯 Obiettivo

Impedire modifiche e cancellazioni accidentali o non autorizzate dei progetti QGIS salvati nel GeoPackage.

## ⚠️ IMPORTANTE: Protezione a Livello GeoPackage

**La protezione si applica a TUTTI i progetti all'interno del GeoPackage, non ai singoli progetti.**

Quando attivi la protezione:
- ✅ TUTTI i progetti nel GeoPackage sono protetti
- ✅ La protezione è a livello di file GeoPackage intero
- ✅ Non è possibile proteggere solo alcuni progetti selettivamente

**Perché?** I trigger SQLite operano a livello di tabella (`qgis_projects`), che contiene tutti i progetti. Non è tecnicamente possibile con i trigger proteggere solo alcuni record specifici.

**Soluzione:** Se hai bisogno di progetti protetti e non protetti, usa GeoPackage separati:
- `produzione.gpkg` → Protezione ATTIVA
- `sviluppo.gpkg` → Protezione DISATTIVATA

## 🚀 Utilizzo

### Attivazione Automatica

Il sistema di protezione si attiva **automaticamente** quando:
1. Apri un GeoPackage con il plugin
2. Il plugin crea i trigger di protezione nella tabella `qgis_projects`

**Nessuna configurazione richiesta!** Il sistema è trasparente per l'utente.

### Operazioni Protette

#### ✅ Operazioni Permesse (tramite plugin)
- Salvare nuovi progetti
- Sovrascrivere progetti esistenti (con conferma)
- Rinominare progetti
- Eliminare progetti (con conferma)
- Duplicare progetti

#### ❌ Operazioni Bloccate (senza autorizzazione)
- Modifiche dirette al database tramite SQL
- Cancellazioni tramite altri strumenti (DB Browser, DBeaver, ecc.)
- UPDATE/DELETE non autorizzati

## 🧪 Test del Sistema

### Test Automatico

Usa lo script di test fornito:

```bash
python3 test_triggers.py /percorso/al/tuo/file.gpkg
```

Lo script verifica:
- Esistenza dei trigger
- Blocco UPDATE
- Blocco DELETE
- Funzionamento bypass

### Test Manuale

1. Apri il GeoPackage con DB Browser for SQLite
2. Prova a eseguire:
   ```sql
   UPDATE qgis_projects SET name = 'test' WHERE name = 'progetto1';
   ```
3. Dovresti ricevere l'errore: `🔒 Modifica non consentita`

## 📋 Verifica Stato Trigger

Per verificare che i trigger siano attivi:

```sql
-- Lista trigger
SELECT name FROM sqlite_master
WHERE type='trigger'
AND name LIKE 'prevent_project_%';

-- Risultato atteso:
-- prevent_project_update
-- prevent_project_delete
```

## 🔧 Rimozione Trigger (se necessario)

### Opzione 1: SQL
```sql
DROP TRIGGER IF EXISTS prevent_project_update;
DROP TRIGGER IF EXISTS prevent_project_delete;
DROP TABLE IF EXISTS qgis_projects_trigger_bypass;
```

### Opzione 2: Python (nel plugin)
```python
conn = sqlite3.connect('file.gpkg')
self.rimuovi_trigger_protezione(conn)
conn.close()
```

## 📚 Documentazione Completa

Per dettagli tecnici completi, consulta: [TRIGGERS_PROTECTION.md](TRIGGERS_PROTECTION.md)

## ⚠️ Note Importanti

- I trigger proteggono i dati ma **NON sostituiscono** i backup
- Continua a fare backup regolari dei GeoPackage
- I trigger sono permanenti fino alla rimozione manuale

## 🐛 Troubleshooting

### "I trigger non si creano"
- Verifica che il GeoPackage contenga la tabella `qgis_projects`
- Salva almeno un progetto nel GeoPackage

### "Le operazioni dal plugin falliscono"
- Verifica che il bypass non sia rimasto attivo:
  ```sql
  SELECT bypass_active FROM qgis_projects_trigger_bypass;
  -- Deve essere 0
  ```
- Se è 1, ripristina:
  ```sql
  UPDATE qgis_projects_trigger_bypass SET bypass_active = 0;
  ```

### "Voglio disabilitare temporaneamente la protezione"
- Usa il metodo SQL sopra per rimuovere i trigger
- Riapri il GeoPackage con il plugin per ricrearli

## 📝 Versione

- **Plugin**: GeoPackage Project Manager v3.5.0
- **Feature**: Sistema Trigger Protezione
- **Data**: 2025-12-20
- **Autore**: Salvatore Fiandaca

---

**💡 Suggerimento**: Questo sistema di protezione è ideale per ambienti di produzione dove più utenti accedono al GeoPackage, garantendo che le modifiche avvengano solo tramite il plugin ufficiale.
