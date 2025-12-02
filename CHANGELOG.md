# Changelog

Tutte le modifiche rilevanti a questo progetto saranno documentate in questo file.

Il formato è basato su [Keep a Changelog](https://keepachangelog.com/it/1.0.0/),
e questo progetto aderisce al [Versionamento Semantico](https://semver.org/lang/it/).

---

## [3.3.0] - 2025-12-02

### 🎉 Aggiunto
- **Sistema metadati completo**: Estrazione e salvataggio automatico di metadati dettagliati per ogni progetto
  - Data di creazione e modifica
  - Dimensione del progetto in bytes
  - Conteggio layer totali, vettoriali e raster
- **Tooltip intelligenti**: Visualizzazione informazioni complete al passaggio del mouse sui progetti
  - Tooltip completo per progetti con metadati: mostra data, dimensione, layer count
  - Tooltip base per progetti senza metadati: mostra almeno la dimensione
  - Tooltip fallback minimo: mostra il nome del progetto
- **Pulsante "Aggiorna Metadati"**: Nuovo pulsante per rigenerare tutti i metadati con un clic
  - Dialog di conferma con statistiche
  - Progress bar con possibilità di annullamento
  - Report finale con progetti aggiornati/saltati
- **Tabella `qgis_projects_metadata`**: Nuova tabella per memorizzare informazioni dettagliate sui progetti

### 🛠️ Corretto
- **Compatibilità Qt5/Qt6**: Risolti problemi con i tooltip su diverse versioni di Qt
  - Aggiunto enum compatibile `EventToolTip` per gestire `QEvent.ToolTip`
  - I tooltip ora funzionano correttamente sia su Qt5 che Qt6

### 🌍 Traduzioni
- Aggiornate traduzioni italiane e inglesi per tutte le nuove funzionalità
- Aggiunte 13 nuove stringhe tradotte nel file `gpkg_project_manager_en.ts`

### 📚 Documentazione
- Aggiornato README.md con sezione "Sistema Metadati"
- Aggiunte istruzioni per l'utilizzo dei tooltip e aggiornamento metadati
- Creato CHANGELOG.md per tracciare le modifiche

---

## [3.2.0] - 2025

### 🎉 Aggiunto
- **Ottimizzazione database**: Compatta il GeoPackage con VACUUM SQLite per ridurre dimensioni e migliorare performance
- **Info GeoPackage in tempo reale**: Visualizza dimensione file e numero progetti aggiornati automaticamente
- **Statistiche ottimizzazione**: Mostra spazio risparmiato, percentuale di riduzione e tempo impiegato
- **Gestione performance**: Rimuove spazio inutilizzato e ottimizza tabelle del database

---

## [3.1.0] - 2025

### 🎉 Aggiunto
- **Timestamp automatico**: Aggiungi timestamp ai nomi dei progetti (YYYYMMDDHHmmss)
- **Versioning incrementale progetti**: Sistema automatico di versioning (v01, v02, ..., v99)
- **Versioning GeoPackage clonati**: Versioning automatico per i file clonati
- **Impostazioni persistenti**: Le preferenze vengono salvate tra le sessioni
- **Sostituzione intelligente**: Evita l'accumulo di timestamp e versioni duplicate

---

## [3.0.0] - 2025

### 🎉 Aggiunto
- Interfaccia moderna completamente ridisegnata
- Funzionalità di clonazione GeoPackage con aggiornamento automatico percorsi
- Supporto completo Qt5/Qt6
- Esportazione progetti in formato QGS/QGZ
- Menu contestuale per azioni rapide
- Funzioni di duplicazione e rinomina progetti

### 🛠️ Corretto
- Miglioramenti alla stabilità e gestione errori

---

## Legenda

- 🎉 **Aggiunto**: Nuove funzionalità
- 🛠️ **Corretto**: Bug fix
- 🔄 **Modificato**: Modifiche a funzionalità esistenti
- ❌ **Rimosso**: Funzionalità rimosse
- 🔒 **Sicurezza**: Fix di sicurezza
- 📚 **Documentazione**: Modifiche alla documentazione
- 🌍 **Traduzioni**: Aggiornamenti alle traduzioni
