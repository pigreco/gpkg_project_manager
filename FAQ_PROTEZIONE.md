# ❓ FAQ - Protezione Trigger GeoPackage

## 🎯 Domanda Principale

### **"Appena attivo la protezione su un progetto viene applicata a tutti i progetti del GeoPackage, è normale?"**

## ✅ Risposta

**SÌ, È ASSOLUTAMENTE NORMALE!**

Questo è il comportamento **corretto e atteso** del sistema di protezione.

---

## 🔍 Spiegazione Dettagliata

### Come Funziona la Protezione

```
┌────────────────────────────────────────────────┐
│ GeoPackage: mio_file.gpkg                      │
│                                                │
│ ┌────────────────────────────────────┐         │
│ │ Tabella: qgis_projects             │         │
│ │ ┌────────────────────────────────┐ │         │
│ │ │ progetto_001                   │ │ ← Tutti │
│ │ │ progetto_002                   │ │   questi│
│ │ │ progetto_003                   │ │   sono  │
│ │ │ progetto_004                   │ │   nella │
│ │ └────────────────────────────────┘ │   stessa│
│ └────────────────────────────────────┘   tabella│
│                                                │
│ Trigger di Protezione (a livello TABELLA)     │
│ ├─ prevent_project_update                     │
│ └─ prevent_project_delete                     │
│                                                │
│ Protezione vale per: TUTTA LA TABELLA          │
│ = TUTTI i progetti insieme                     │
└────────────────────────────────────────────────┘
```

### Perché Non Posso Proteggere Solo Alcuni Progetti?

I **trigger SQLite** operano a livello di **TABELLA**, non di singolo record:

```sql
-- Il trigger è definito sulla TABELLA qgis_projects
CREATE TRIGGER prevent_project_update
BEFORE UPDATE ON qgis_projects  ← Intera tabella!
WHEN (SELECT bypass_active FROM qgis_projects_trigger_bypass WHERE id = 1) = 0
BEGIN
    SELECT RAISE(ABORT, '🔒 Modifica non consentita...');
END;
```

**Cosa significa?**
- Il trigger si attiva per **QUALSIASI** UPDATE sulla tabella `qgis_projects`
- Non distingue quale record (progetto) stai modificando
- Protegge **tutti i record** nella tabella

---

## 📊 Confronto Comportamenti

### ❌ SBAGLIATO (Non Possibile)
```
GeoPackage: progetti.gpkg
├── progetto_A  ← Protetto     ✅
├── progetto_B  ← Protetto     ✅
├── progetto_C  ← NON Protetto ❌  IMPOSSIBILE!
└── progetto_D  ← NON Protetto ❌  IMPOSSIBILE!
```

### ✅ CORRETTO (Come Funziona Realmente)
```
GeoPackage: progetti.gpkg
├── progetto_A  ← Protetto ✅
├── progetto_B  ← Protetto ✅
├── progetto_C  ← Protetto ✅
└── progetto_D  ← Protetto ✅

Tutti protetti insieme!
```

---

## 💡 Soluzioni Alternative

### Scenario: Vuoi protezione selettiva

**Problema:**
- Hai 4 progetti: A, B, C, D
- Vuoi proteggere solo A e B
- Vuoi lasciare C e D modificabili

**Soluzione:** Usa **GeoPackage separati**

```
📦 produzione.gpkg  (Protezione ATTIVA ✅)
   ├── progetto_A  ← Protetto
   └── progetto_B  ← Protetto

📦 sviluppo.gpkg  (Protezione DISATTIVATA ❌)
   ├── progetto_C  ← Modificabile
   └── progetto_D  ← Modificabile
```

**Vantaggi:**
- ✅ Controllo granulare su cosa proteggere
- ✅ Separazione logica produzione/sviluppo
- ✅ Più sicuro (file separati)
- ✅ Più chiaro (scopo evidente)

---

## 🎯 Best Practices

### ✅ Quando Usare la Protezione

**Usa la protezione (e proteggi TUTTI i progetti) quando:**
1. Il GeoPackage contiene progetti di **produzione**
2. Vuoi evitare modifiche accidentali
3. Il file è condiviso tra più persone
4. Vuoi tracciabilità delle modifiche

**Esempio:**
```
produzione_2025.gpkg  ← Protezione ATTIVA
├── progetto_clienteA_finale
├── progetto_clienteB_finale
└── progetto_clienteC_finale

Tutti i progetti sono "finali" → Proteggi tutto!
```

### ❌ Quando NON Usare la Protezione

**NON usare la protezione quando:**
1. Il GeoPackage contiene progetti di **sviluppo**
2. Devi modificare frequentemente i progetti
3. Sei in fase di test/sperimentazione
4. Lavori da solo e non hai rischi

**Esempio:**
```
test_2025.gpkg  ← Protezione DISATTIVATA
├── bozza_01
├── esperimento_nuovo
└── test_performance

Tutti i progetti sono "work in progress" → Nessuna protezione!
```

---

## 🔧 Operazioni Comuni

### Verificare lo Stato di Protezione

**Operazione:** Clicca **⋮** su un progetto → "🔒 Gestione Protezione" → "ℹ️ Stato Protezione"

**Cosa vedi:**
```
┌─────────────────────────────────────┐
│ ✅ Protezione ATTIVA                │
│                                     │
│ GeoPackage: progetti.gpkg           │
│ Trigger:                            │
│  • ✅ prevent_project_update        │
│  • ✅ prevent_project_delete        │
│                                     │
│ TUTTI i progetti sono protetti      │
└─────────────────────────────────────┘
```

**Interpretazione:**
- Se vedi "✅ Protezione ATTIVA" → TUTTI i progetti sono protetti
- Se vedi "❌ Protezione DISATTIVATA" → NESSUN progetto è protetto
- **Non esiste** uno stato "parzialmente protetto"

---

## 🤔 Altre Domande Frequenti

### Q: "Posso modificare i trigger per proteggere solo alcuni progetti?"

**A:** Tecnicamente sì, ma è molto complesso:

```sql
-- Esempio avanzato (NON consigliato)
CREATE TRIGGER prevent_project_update_selective
BEFORE UPDATE ON qgis_projects
WHEN NEW.name IN ('progetto_A', 'progetto_B')  -- Solo questi
  AND (SELECT bypass_active FROM qgis_projects_trigger_bypass WHERE id = 1) = 0
BEGIN
    SELECT RAISE(ABORT, '🔒 Questo progetto è protetto');
END;
```

**Problemi:**
- Devi elencare manualmente i nomi dei progetti
- Se rinomini un progetto, devi aggiornare il trigger
- Complessità molto alta
- Difficile da mantenere
- **NON implementato nel plugin**

**Soluzione consigliata:** Usa GeoPackage separati (vedi sopra)

---

### Q: "Se apro un GeoPackage con 10 progetti, sono tutti protetti?"

**A:** Dipende se il GeoPackage ha i trigger:
- ✅ **CON trigger** → TUTTI i 10 progetti sono protetti
- ❌ **SENZA trigger** → NESSUNO dei 10 progetti è protetto

I trigger si creano automaticamente quando **apri il GeoPackage con il plugin**.

---

### Q: "Se aggiungo un nuovo progetto, è automaticamente protetto?"

**A:** **SÌ!**

Se il GeoPackage ha già i trigger attivi:
1. Apri il GeoPackage (trigger già presenti)
2. Salvi un nuovo progetto
3. Il nuovo progetto viene inserito nella tabella `qgis_projects`
4. Il trigger protegge anche questo nuovo record

**È automatico!**

---

### Q: "Se faccio 'Disabilita Temporanea', posso modificare solo un progetto?"

**A:** **NO!**

Quando disabiliti la protezione:
- I trigger vengono **completamente rimossi** dal database
- TUTTI i progetti diventano modificabili
- Non c'è modo di disabilitare "solo per un progetto"

**Workflow:**
1. Disabilita protezione → TUTTI modificabili
2. Fai le tue modifiche (su uno o più progetti)
3. Ripristina protezione → TUTTI protetti di nuovo

---

## 📋 Riepilogo Finale

### ✅ Comportamento Normale (Come Funziona)

| Azione | Effetto |
|--------|---------|
| Apro GeoPackage con 5 progetti | I trigger si creano |
| Stato protezione | TUTTI i 5 progetti sono protetti |
| Aggiungo 6° progetto | Automaticamente protetto |
| Modifico un progetto via plugin | ✅ Funziona (bypass automatico) |
| Modifico un progetto via DB Browser | ❌ BLOCCATO dal trigger |
| Elimino un progetto via plugin | ✅ Funziona (con conferma + bypass) |
| Elimino un progetto via DB Browser | ❌ BLOCCATO dal trigger |

### 🎯 Principio Fondamentale

```
┌─────────────────────────────────────────┐
│ REGOLA D'ORO                            │
│                                         │
│ 1 GeoPackage = 1 Stato di Protezione   │
│                                         │
│ • Protetto → TUTTI protetti             │
│ • Non protetto → NESSUNO protetto       │
│                                         │
│ NON esiste "protezione parziale"        │
└─────────────────────────────────────────┘
```

---

## 📞 Hai Ancora Dubbi?

### 🔍 Test Pratico

Prova tu stesso:

1. **Crea un GeoPackage con 3 progetti**
   - progetto_test_1
   - progetto_test_2
   - progetto_test_3

2. **Apri con il plugin**
   - I trigger si creano automaticamente

3. **Verifica stato**
   - Clicca ⋮ su progetto_test_1
   - "🔒 Gestione Protezione" → "ℹ️ Stato Protezione"
   - Vedi: "✅ Protezione ATTIVA"

4. **Prova a modificare con DB Browser**
   - Apri il file .gpkg con DB Browser for SQLite
   - Prova: `UPDATE qgis_projects SET name='nuovo_nome' WHERE name='progetto_test_2'`
   - Risultato: ❌ Errore "🔒 Modifica non consentita"

5. **Conclusione**
   - Anche se hai provato a modificare solo progetto_test_2
   - TUTTI i progetti (1, 2, 3) sono protetti
   - **È normale!**

---

**Versione:** 3.7.0
**Data:** 2025-12-20
**Autore:** Salvatore Fiandaca
**Documento:** FAQ Protezione Trigger
