# Changelog

Tutte le modifiche rilevanti a questo progetto saranno documentate in questo file.

Il formato è basato su [Keep a Changelog](https://keepachangelog.com/it/1.0.0/),
e questo progetto aderisce al [Versionamento Semantico](https://semver.org/lang/it/).

---

## [3.7.1] - 2025-12-20

### 🔧 Migliorato
- **Posizionamento menu protezione**: Rimosso sottomenu dal menu contestuale progetti (era fuorviante)
- **Indicatore protezione visibile**: Aggiunto indicatore stato protezione sulla stessa riga di "ℹ️ Info"
  - Mostra stato in tempo reale: `🔒 Protezione: ATTIVA ✅` / `🔓 DISATTIVATA` / `⚠️ PARZIALE`
  - Colori distinti per ogni stato (verde/rosso/arancione)
  - Pulsante ⚙️ per accesso rapido al menu gestione
- **UX migliorata**: Menu protezione ora a livello GeoPackage (più chiaro e semanticamente corretto)
- **Aggiornamento automatico**: Lo stato protezione si aggiorna dopo ogni operazione (disabilita/ripristina)

### 📝 Chiarimenti
- **Documentazione aggiornata**: Chiarito che la protezione vale per TUTTO il GeoPackage, non per singoli progetti
- **FAQ estese**: Aggiunte risposte alle domande frequenti sull'ambito della protezione
- **Design rationale**: Il menu a livello GeoPackage riflette correttamente che i trigger proteggono l'intera tabella

---

## [3.7.0] - 2025-12-20

### 🎉 Aggiunto
- **Sistema di Protezione con Trigger SQLite**: Implementato sistema completo di protezione automatica dei progetti
  - **Trigger automatici**: Creazione automatica di trigger che impediscono UPDATE e DELETE non autorizzati sulla tabella `qgis_projects`
  - **Protezione trasparente**: I trigger si creano automaticamente all'apertura del GeoPackage
  - **Sistema di bypass intelligente**: Gestione automatica del bypass per operazioni autorizzate dal plugin
  - **Tabella di controllo**: `qgis_projects_trigger_bypass` per gestire l'abilitazione/disabilitazione temporanea
  - **Protezione universale**: Funziona anche contro modifiche da strumenti esterni (DB Browser, DBeaver, etc.)

- **Menu Gestione Protezione**: Nuovo sottomenu contestuale "🔒 Gestione Protezione" per ogni progetto
  - **ℹ️ Stato Protezione**: Mostra dialog con informazioni dettagliate sullo stato dei trigger
    - Visualizzazione grafica dello stato (ATTIVA ✅ / PARZIALE ⚠️ / DISATTIVATA ❌)
    - Lista dei trigger presenti (prevent_project_update, prevent_project_delete)
    - Stato corrente del bypass (protezione attiva o disattivata)
    - Avvisi se il bypass è attivo
  - **🔓 Disabilita Temporanea**: Rimuove i trigger per operazioni di manutenzione avanzata
    - Conferma richiesta prima della disabilitazione
    - Messaggio di avviso persistente nella barra messaggi QGIS
  - **🔐 Ripristina Protezione**: Ricrea i trigger se sono stati rimossi
    - Verifica automatica dello stato esistente
    - Conferma visiva del ripristino

### 🔧 Migliorato
- **Funzioni di salvataggio/modifica**: Integrate con sistema bypass trigger
  - `salva_progetto()`: Abilita bypass automatico quando si sovrascrive un progetto esistente
  - `elimina_progetto()`: Abilita bypass automatico prima del DELETE
  - `rinomina_progetto()`: Abilita bypass automatico prima dell'UPDATE
  - Gestione errori robusta con cleanup automatico del bypass in caso di eccezioni

- **Gestione database**: Nuove funzioni per gestione protezione
  - `crea_trigger_protezione(conn)`: Crea trigger e tabella di controllo
  - `abilita_bypass_trigger(conn)`: Abilita temporaneamente il bypass
  - `disabilita_bypass_trigger(conn)`: Riattiva la protezione
  - `rimuovi_trigger_protezione(conn)`: Rimuove completamente i trigger
  - `verifica_stato_protezione()`: Mostra dialog con stato dettagliato
  - `disabilita_protezione_temporanea()`: Interfaccia per disabilitare la protezione
  - `ripristina_protezione()`: Interfaccia per ripristinare la protezione

### 📚 Documentazione
- **TRIGGERS_PROTECTION.md**: Documentazione tecnica completa (350+ linee)
  - Descrizione dettagliata del funzionamento dei trigger
  - Esempi SQL e Python
  - Sezioni troubleshooting e best practices
- **README_TRIGGERS.md**: Guida rapida per l'utente
  - Istruzioni di utilizzo semplificate
  - Test e verifica dello stato
  - FAQ e risoluzione problemi comuni
- **test_triggers.py**: Script automatico di test
  - Verifica esistenza e funzionamento dei trigger
  - Test blocco UPDATE/DELETE
  - Test funzionamento bypass
  - Report dettagliato con esito dei test
- **esempio_trigger.sql**: File SQL con esempi pratici
  - Query di verifica stato trigger
  - Esempi di test manuali
  - Comandi per rimozione/ripristino trigger
- **CHANGELOG_TRIGGERS.md**: Changelog specifico per la feature trigger
  - Dettaglio completo delle modifiche
  - Impatto sulle prestazioni
  - Note di migrazione

### 🔐 Sicurezza
- **Protezione progetti a livello database**: I trigger operano direttamente in SQLite
- **Blocco modifiche esterne**: Impedisce modifiche da qualsiasi strumento che non sia il plugin
- **Versioning forzato**: Incoraggia creazione di nuove versioni invece della sovrascrittura
- **Audit trail**: Solo operazioni autorizzate dal plugin possono modificare i progetti

### 🧪 Testing
- Script di test automatico (`test_triggers.py`) con 6 test completi
- Esempi SQL per test manuali
- Verifica in produzione con GeoPackage reali

### ⚡ Prestazioni
- **Overhead minimo**: I trigger si attivano solo durante UPDATE/DELETE
- **Query istantanea**: Verifica bypass su tabella con 1 solo record
- **Nessun impatto su SELECT/INSERT**: Operazioni di lettura e inserimento non influenzate

---

## [3.6.0] - 2025-12-06

### 🎉 Aggiunto
- **Tab "🔗 Relazioni"**: Nuova tab dedicata alla visualizzazione delle relazioni tra tabelle
  - Visualizzazione **Foreign Keys** (FK) definite a livello database
  - Visualizzazione **GeoPackage Extension** (relazioni definite tramite tabella `gpkgext_relations`)
  - **Visualizzazione Relazioni di Progetto QGIS**: Mostra le relazioni definite nel progetto QGIS selezionato
    - Estrazione automatica delle relazioni dal progetto QGIS salvato nel GeoPackage
    - Supporto decodifica HEX per progetti salvati come stringa esadecimale
    - Estrazione intelligente dei nomi tabelle dai layer ID (da attributo `source` in `<layer-tree-layer>`)
    - Mostra **tipo di relazione**: Association (relazione debole) o Composition (relazione forte con cascata)
    - Mostra **cardinalità**: 1:N (one-to-many)
    - Filtro anti-duplicati automatico per relazioni ripetute
  - Tabella con 6 colonne: Nome Relazione, Tabella Origine, Campo Origine, Tabella Destinazione, Campo Destinazione, Tipo
  - Contatore dettagliato: mostra numero totale relazioni e dettaglio per tipo (FK, GPKG, Progetto)
  - Aggiornamento automatico quando si seleziona un progetto
  - Pulsante "⟳ Aggiorna" per ricaricare manualmente le relazioni
- **Popolamento automatico descrizione**: Il campo descrizione si popola automaticamente quando si seleziona un progetto
  - Consente di visualizzare e modificare la descrizione del progetto selezionato
  - Sincronizzazione tramite signal `itemSelectionChanged` della tabella progetti

### 🔧 Migliorato
- **Tabella Progetti**: Semplificata rimuovendo colonne non essenziali
  - Rimosse colonne "Layer" e "Dimensioni" per una vista più pulita
  - Rimaste solo le colonne essenziali: Nome Progetto, Data Creazione, Data Modifica, EPSG, Opzioni
- **Tabella Metadati**: Semplificata la struttura della tabella `qgis_projects_metadata`
  - Rimossi campi non utilizzati: `size_bytes`, `layer_count`, `vector_count`, `raster_count`, `table_count`
  - Campi attuali: `project_name`, `created_date`, `modified_date`, `crs_epsg`, `description`
  - Database più leggero e manutenzione più semplice
- **Dialog "Aggiorna Metadati"**: Aggiornato per riflettere i cambiamenti
  - Messaggio semplificato che mostra solo le operazioni effettive (date e EPSG)
  - Rimossi riferimenti a layer e dimensioni

### 🐛 Corretto
- **Decompressione progetti**: Risolto problema con progetti salvati come stringa HEX nel database
  - Aggiunta rilevazione e decodifica automatica HEX prima della decompressione
  - Supporto per tutti i formati: ZIP (QGZ), GZIP, e plain text (QGS)
- **Estrazione nomi tabelle**: Risolto problema di estrazione nomi tabelle dai layer ID
  - Implementato metodo robusto che cerca in `<layer-tree-layer>` prima di `<maplayer>`
  - Pattern regex migliorato per gestire attributi in ordine variabile

---

## [3.5.0] - 2025-12-05

### 🎉 Aggiunto
- **Interfaccia a Tab**: Implementata navigazione a tab nell'interfaccia principale
  - **Tab "📋 Progetti"**: Gestione completa dei progetti GeoPackage (tutte le funzionalità esistenti)
  - **Tab "🎨 Stili"**: Gestione stili integrata direttamente nell'interfaccia
  - Visualizzazione e caricamento degli stili salvati nel GeoPackage
  - Tabella stili con colonne: Layer, Nome Stile, Default, Descrizione, Ultima Modifica, Opzioni
  - Aggiornamento automatico degli stili quando si passa al tab
  - Info GeoPackage sincronizzata tra i tab
  - Tab posizionato solo nella sezione bassa (selezione GPKG e salvataggio sempre visibili)
- **Applicazione Stili**: Implementata funzionalità completa di applicazione stili ai layer
  - Applica stili ai layer presenti nel progetto corrente con doppio clic o menu
  - Recupero automatico dello stile QML dal database
  - Aggiornamento immediato della visualizzazione della mappa
  - Gestione errori con messaggi chiari (layer non trovato, GPKG non valido, ecc.)
- **Menu Opzioni Stili**: Menu completo per ogni stile con azioni funzionanti
  - 🎨 Applica Stile: applica lo stile al layer nel progetto
  - 📥 Esporta QML: esporta lo stile come file QML
  - ✏️ Rinomina: rinomina lo stile nel database
  - 📋 Duplica: crea una copia dello stile
  - ⭐ Imposta come Default: imposta lo stile come default per il layer
  - 🗑️ Elimina: elimina lo stile dal database (con conferma)

### 🔧 Migliorato
- **Gestione Stili**: Rimosso dialog separato, ora integrato come tab
  - Navigazione più fluida senza aprire/chiudere finestre
  - Accesso diretto agli stili con un solo clic sul tab
  - Interfaccia più pulita e moderna (rimosso header ridondante)
  - Miglior esperienza utente con tutto in un'unica finestra
  - Layout ottimizzato: sezioni principali sempre accessibili, tab solo per progetti/stili
- **Codice**: Rimosso file `dialog_styles.py` obsoleto e ottimizzato script di creazione ZIP

---

## [3.4.2] - 2025-12-05

### 🎉 Aggiunto
- **Checkbox "Usa nome GeoPackage"**: Nuovo checkbox nella sezione "Salva Progetto Corrente"
  - Imposta automaticamente il nome del progetto uguale al nome del GeoPackage
  - Comodo per mantenere consistenza tra nome progetto e file GeoPackage
  - Supporto in entrambe le interfacce (lista e tabella)
- **Campo Descrizione Progetto**: Aggiunto campo opzionale per descrivere i progetti
  - Nuovo campo "Descr:" nella sezione "Salva Progetto Corrente"
  - Descrizione salvata nella tabella `qgis_projects_metadata` (colonna `description`)
  - Tooltip informativo sui progetti mostra la descrizione quando presente
  - Tooltip completo con: nome progetto, descrizione, date creazione/modifica, dimensione, layer, EPSG
  - Supporto retrocompatibilità: colonna aggiunta automaticamente se non esiste

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
