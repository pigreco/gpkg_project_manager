# Traduzioni / Translations

Questa cartella contiene le traduzioni del plugin GeoPackage Project Manager.

This folder contains translations for the GeoPackage Project Manager plugin.

## Lingue Disponibili / Available Languages

- 🇮🇹 **Italiano** (it) - Default
- 🇬🇧 **English** (en) - Disponibile / Available

## File

- `gpkg_project_manager_en.ts` - File sorgente traduzione inglese / English translation source
- `gpkg_project_manager_en.qm` - File compilato traduzione inglese / Compiled English translation

## Come Aggiungere una Nuova Traduzione / How to Add a New Translation

### 1. Crea un nuovo file .ts / Create a new .ts file

Copia il file `gpkg_project_manager_en.ts` e rinominalo con il codice della tua lingua:

Copy the file `gpkg_project_manager_en.ts` and rename it with your language code:

```bash
cp gpkg_project_manager_en.ts gpkg_project_manager_fr.ts  # Esempio per francese / Example for French
```

### 2. Traduci le stringhe / Translate the strings

Apri il file `.ts` con un editor di testo e traduci solo il contenuto dei tag `<translation>`:

Open the `.ts` file with a text editor and translate only the content of `<translation>` tags:

```xml
<message>
    <source>Open GeoPackage Project Manager</source>
    <translation>Apri GeoPackage Project Manager</translation>  <!-- Traduci qui / Translate here -->
</message>
```

**OPPURE / OR** usa Qt Linguist (consigliato):

```bash
linguist gpkg_project_manager_fr.ts
```

### 3. Compila il file .qm / Compile the .qm file

Usa lo script fornito / Use the provided script:

```bash
cd ..
python3 scripts/compile_translations.py
```

OPPURE manualmente con lrelease / OR manually with lrelease:

```bash
lrelease gpkg_project_manager_fr.ts -qm gpkg_project_manager_fr.qm
```

### 4. Testa la traduzione / Test the translation

1. Riavvia QGIS / Restart QGIS
2. Cambia la lingua in QGIS: **Impostazioni** → **Opzioni** → **Generale** → **Lingua interfaccia utente**

   Change language in QGIS: **Settings** → **Options** → **General** → **User Interface Translation**

3. Riavvia QGIS di nuovo / Restart QGIS again
4. Il plugin dovrebbe ora usare la tua traduzione / The plugin should now use your translation

### 5. Contribuisci / Contribute

Invia una Pull Request con il tuo file `.ts` e `.qm` su GitHub!

Send a Pull Request with your `.ts` and `.qm` file on GitHub!

## Codici Lingua / Language Codes

Usa i codici ISO 639-1 / Use ISO 639-1 codes:

- `en` - English
- `it` - Italiano
- `fr` - Français
- `de` - Deutsch
- `es` - Español
- `pt` - Português
- `ru` - Русский
- `zh` - 中文
- etc.

## Strumenti / Tools

### Qt Linguist (Consigliato / Recommended)

Qt Linguist è un'interfaccia grafica per tradurre i file `.ts`.

Qt Linguist is a GUI tool for translating `.ts` files.

**Installazione / Installation:**

- **Linux**: `sudo apt-get install qttools5-dev-tools`
- **macOS**: `brew install qt5`
- **Windows**: Incluso in Qt installer / Included in Qt installer

### Compilazione Traduzioni / Compiling Translations

**Metodo 1**: Script Python

```bash
python3 ../scripts/compile_translations.py
```

**Metodo 2**: lrelease diretto / Direct lrelease

```bash
lrelease *.ts
```

**Metodo 3**: Makefile (se disponibile / if available)

```bash
make translations
```

## Contribuire con Nuove Traduzioni / Contributing New Translations

Le traduzioni sono molto apprezzate! Puoi contribuire:

Translations are much appreciated! You can contribute by:

1. Creando un nuovo file `.ts` con la tua lingua / Creating a new `.ts` file with your language
2. Traducendo tutte le stringhe / Translating all strings
3. Compilando in `.qm` / Compiling to `.qm`
4. Aprendo una Pull Request / Opening a Pull Request

## Domande / Questions

Per domande sulle traduzioni / For questions about translations:

- **Issues**: https://github.com/pigreco/gpkg_project_manager/issues
- **Email**: pigrecoinfinito@gmail.com

---

Grazie per contribuire alle traduzioni! 🌍

Thank you for contributing translations! 🌍
