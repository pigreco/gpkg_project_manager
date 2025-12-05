# Changelog

Tutte le modifiche rilevanti a questo progetto saranno documentate in questo file.

Il formato è basato su [Keep a Changelog](https://keepachangelog.com/it/1.0.0/),
e questo progetto aderisce al [Versionamento Semantico](https://semver.org/lang/it/).

---

## [3.4.2] - 2025-12-05

### 🎉 Aggiunto
- **Checkbox "Usa nome GeoPackage"**: Nuovo checkbox nella sezione "Salva Progetto Corrente"
  - Imposta automaticamente il nome del progetto uguale al nome del GeoPackage
  - Comodo per mantenere consistenza tra nome progetto e file GeoPackage
  - Supporto in entrambe le interfacce (lista e tabella)

### 🔧 Migliorato
- **Checkbox Versioning GeoPackage**: Ottimizzata la visualizzazione nella GUI
  - Spostato nella riga delle informazioni GeoPackage per migliore organizzazione
  - Testo semplificato: "Versioning" (rimossa descrizione tra parentesi)
  - Aggiunto tooltip descrittivo: "Aggiungi versione progressiva al nome del clone (v01, v02, v03, ...)"
  - Layout più pulito e allineato a destra
  - Migliore usabilità con descrizione disponibile al passaggio del mouse

---

## [3.4.1] - 2025-12-04

### 🎉 Aggiunto
- **Colonna EPSG**: Nuova colonna nella tabella progetti che mostra il sistema di riferimento (CRS) del progetto
  - Estrazione CRS tramite API QGIS (`QgsProject.instance().crs().authid()`) al momento del salvataggio
  - Metodo 100% affidabile che legge il CRS reale del progetto attivo
  - Fallback su 4 pattern XML per progetti già salvati (projectCrs, destinationsrs, authid, proj4)
  - Visualizzazione formato "EPSG:XXXX" nella tabella
  - Campo `crs_epsg` aggiunto alla tabella `qgis_projects_metadata`
  - Supporto retrocompatibilità: colonna aggiunta automaticamente se non esiste
- **Dettaglio conteggio layer**: La colonna "Layer" ora mostra il dettaglio dei layer
  - Formato: "V:3 R:2 T:1" (Vettoriali, Raster, Tabelle)
  - Conteggio tabelle esclude tabelle di sistema (qgis_, sqlite_, gpkg_, rtree_)
  - Distinzione tra layer vettoriali con geometria e tabelle senza geometria
  - Campo `table_count` aggiunto alla tabella `qgis_projects_metadata`
  - Visualizza solo i tipi presenti (es. solo "V:5" se ci sono solo vettoriali)

### 🛠️ Corretto
- **Estrazione EPSG affidabile**: Corretto il rilevamento del CRS che prima mostrava sempre "N/A"
  - Ora usa API QGIS invece di parsing XML per massima affidabilità
  - Funziona con qualsiasi sistema di riferimento supportato da QGIS

---

## [3.4.0] - 2025-12-04

### 🎉 Aggiunto
- **Gestione Stili Layer**: Nuova funzionalità per visualizzare e gestire gli stili salvati nel GeoPackage
  - Nuovo dialog **🎨 Stili** accessibile dalla finestra principale
  - Visualizzazione completa degli stili dalla tabella `layer_styles` (standard OGC)
  - Tabella ordinabile per layer, nome stile, default, descrizione e data modifica
  - **Applica stili**: Applica gli stili ai layer caricati nel progetto corrente
  - **Esporta stili**: Esporta stili come file QML per riutilizzo
  - **Rinomina stili**: Modifica il nome degli stili esistenti
  - **Duplica stili**: Crea copie di stili per modificarli senza alterare l'originale
  - **Imposta come default**: Imposta uno stile come predefinito per un layer
  - **Elimina stili**: Rimuovi stili non più necessari
  - Menu contestuale ⚙️ per accesso rapido a tutte le funzioni
  - Doppio clic per applicare rapidamente uno stile
  - Compatibilità completa Qt5/Qt6
  - File: `dialog_styles.py` (nuovo)
  - Integrazione in `dialogs_table.py` con pulsante **🎨 Stili**

### 🌍 Traduzioni
- Aggiornate traduzioni inglesi per il nuovo dialogo stili
- Aggiunte 56 nuove stringhe tradotte nel file `gpkg_project_manager_en.ts`
- Traduzione del pulsante "🎨 Stili" e tooltip nella finestra principale

### 📚 Documentazione
- Aggiornato README.md con sezione "Gestione Stili"
- Aggiunte istruzioni dettagliate per l'utilizzo del gestore stili
- Aggiornato CHANGELOG.md

---

## [3.3.2] - 2025-12-03

### 🛠️ Corretto
- **Gestione date di modifica**: Corretta la logica di aggiornamento delle date di modifica dei progetti
  - La data di modifica (`modified_date`) ora si aggiorna SOLO quando si sovrascrive realmente un progetto
  - Aggiunto parametro `update_modified_date` al metodo `salva_metadati_progetto()`
  - Quando si usa "📊 Aggiorna Metadati", le date di modifica rimangono invariate (aggiorna solo dimensione/layer count)
  - Aggiunto parametro `force_overwrite` al metodo `salva_progetto()` per gestire correttamente la sovrascrittura
  - Il pulsante "⟳ Sovrascrivi" ora imposta correttamente `is_new=False` per aggiornare la data di modifica

### 🎨 Interfaccia
- **Doppia interfaccia**: Mantenute entrambe le versioni per offrire scelta all'utente
  - **dialogs.py**: Interfaccia originale con lista verticale dei progetti
  - **dialogs_table.py**: Interfaccia moderna con tabella a colonne (attualmente in uso)
  - `dialogs_table.py` eredita dinamicamente da `dialogs.py` per evitare duplicazione codice
  - Possibilità di cambiare interfaccia modificando l'import in `main.py`

### 📝 Documentazione
- Aggiornato README.md con spiegazione della doppia interfaccia
- Aggiornato CHANGELOG.md con tutte le modifiche alla gestione date

### 📝 Note
- Tutti i fix sono retrocompatibili con versioni precedenti
- Nessuna modifica alla struttura del database
- Comportamento corretto ora:
  - 💾 **Salva nuovo progetto**: `created_date = modified_date = now`
  - ⟳ **Sovrascrivi progetto**: mantiene `created_date`, aggiorna `modified_date = now`
  - 📊 **Aggiorna metadati**: mantiene sia `created_date` che `modified_date` invariate

---

## [3.3.1] - 2025-12-02

### 🛠️ Corretto
- **Bug rinomina progetto**: I metadati ora vengono correttamente aggiornati quando si rinomina un progetto
  - Aggiornamento automatico del `project_name` nella tabella `qgis_projects_metadata`
  - I tooltip continuano a funzionare correttamente dopo la rinomina
- **Bug duplicazione progetto**: I metadati ora vengono copiati insieme al progetto duplicato
  - Il progetto duplicato eredita tutti i metadati (data creazione, dimensione, layer count)
  - I tooltip sono immediatamente disponibili per i progetti duplicati
- **Flag `is_new` nel salvataggio**: Risolto bug nel riconoscimento di progetti nuovi vs sovrascritti
  - Il flag `is_new` viene ora calcolato PRIMA del salvataggio anziché dopo
  - I metadati ora distinguono correttamente tra nuovi progetti (data creazione = data modifica) e progetti sovrascritti (mantiene data creazione originale)
- **Test traduzione in italiano**: Il test di caricamento traduzione ora funziona correttamente per la lingua italiana
  - Per italiano (lingua default), il test verifica solo il caricamento del file
  - Per altre lingue, il test verifica anche la traduzione delle stringhe
- **Reset dialog**: Il dialog viene ora sempre resettato alla chiusura, indipendentemente dal metodo di chiusura
  - Garantisce che il dialog venga sempre ricreato con stato fresco alla prossima apertura
- **Ricaricamento progetto dopo esportazione**: Migliorata la gestione del ricaricamento del progetto originale
  - Distinzione corretta tra progetti caricati da GeoPackage e da file
  - Il progetto originale viene ripristinato correttamente dopo l'esportazione

### 📝 Note
- Tutti i fix sono retrocompatibili con versioni precedenti
- Nessuna modifica alla struttura del database
- I progetti esistenti continuano a funzionare normalmente

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
  - Aggiunto enum compatibile `WindowModal` per gestire `Qt.WindowModal`
  - I tooltip ora funzionano correttamente sia su Qt5 che Qt6
- **Visibilità checkbox in Qt6**: Aggiunto stile CSS esplicito per QCheckBox
  - Risolto problema di testo invisibile nei checkbox con Qt6
  - Checkbox ora visibili e stilizzati correttamente su tutte le versioni Qt
- **Progress dialog**: Risolto errore AttributeError in aggiornamento metadati batch

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
