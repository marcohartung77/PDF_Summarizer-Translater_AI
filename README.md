# PDF-Zusammenfassen & Übersetzen

## Überblick

Kleine Streamlit-App, mit der du:
- Text aus einer PDF extrahierst,
- eine Zusammenfassung mit einem Hugging-Face-Modell erstellst und
- den Ausgangstext oder die Zusammenfassung Englisch → Deutsch übersetzt.
- Die Übersetzung kannst du als TXT herunterladen.

Die App ist bewusst anfängerfreundlich gehalten und zeigt, wie man in Streamlit mit st.session_state sauber arbeitet (Reruns, Button-Klicks, Auswahlelemente).

## Features

- 📄 PDF-Text extrahieren (PyMuPDF / fitz)
- 🧠 Summarization mit facebook/bart-large-cnn
- 🌐 Translation mit Helsinki-NLP/opus-mt-en-de
- 🔁 Zustandsverwaltung: full_text, summary_text, translated_text, translate_choice, uploaded_name
- ⬇️ Übersetzung als TXT herunterladen

## Installation

### 1. Repository/Projektordner vorbereiten

```bash
git clone <dein-repo-oder-ordner>
cd <ordner>
```

### 2. (Optional) Virtuelle Umgebung

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS / Linux:
source .venv/bin/activate
```

### 3. Abhängigkeiten

```bash
pip install --upgrade pip
pip install streamlit transformers torch pymupdf
```

Hinweise

- Beim ersten Start lädt transformers die Modelle automatisch herunter (Internet nötig).
- Auf CPU läuft alles; GPU wird automatisch genutzt, falls vorhanden.

## Starten

```bash
streamlit run app.py
```

Die App öffnet sich im Browser (standardmäßig http://localhost:8501).