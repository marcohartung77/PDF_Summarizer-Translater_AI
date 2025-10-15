from transformers import pipeline
import streamlit as st
import fitz
import io

def extract_text_from_pdf(file):
    with fitz.open(stream=io.BytesIO(file.read()), filetype="pdf") as doc:
        seiten_text = []
        for seite in doc:
            text_der_seite = seite.get_text("text")
            seiten_text.append(text_der_seite)
        gesamter_text = "\n".join(seiten_text)
        gesamter_text = gesamter_text.strip()
        return gesamter_text

@st.cache_resource
def get_summarizer():
        return pipeline(task="summarization", model="facebook/bart-large-cnn")

@st.cache_resource 
def get_translator():
    return pipeline(task="translation", model="Helsinki-NLP/opus-mt-en-de")
    
            
st.title("PDF-Zusammenfassen & Übersätzen")
st.subheader("Englisch zu Deutsch Übersätzung")

if "full_text" not in st.session_state:
    st.session_state.full_text = ""
if "summary_text" not in st.session_state:
    st.session_state.summary_text = ""
if "translate_choice" not in st.session_state:
    st.session_state.translate_choice = "Ausgangstext"
if "uploaded_name" not in st.session_state:
    st.session_state.uploaded_name = None
if "translated_text" not in st.session_state:
    st.session_state.translated_text = ""

uploaded = st.file_uploader(label="PDF auswählen", type=["pdf"])
if uploaded and uploaded.name != st.session_state.uploaded_name:
    st.session_state.full_text = extract_text_from_pdf(uploaded)
    st.session_state.uploaded_name = uploaded.name 
    st.subheader("Text aus PDF:")
    st.write(st.session_state.full_text)
    st.session_state.summary_text = ""
    st.session_state.translate_choice = "Ausgangstext"
    
if not st.session_state.full_text:
    st.error("Kein extrahierbarer Text gefunden.")
else:
    st.success(f"PDF geladen mit {len(st.session_state.full_text)} Zeichen")
    input_text = st.session_state.full_text[:2000] # Slicing-Operator

if st.button("Zusammenfassung"):
    with st.spinner("Erstelle Zusammenfassung..."):
        summarizer = get_summarizer()
        summary = summarizer(
            input_text,
            min_length=30,
            max_length=160,
            do_sample=False
        )
    st.session_state.summary_text = summary[0]["summary_text"]
    st.session_state.translate_choice = "Zusammenfassung"
    
    
if st.session_state.summary_text:
    st.subheader("Zusammenfassung")
    st.write(st.session_state.summary_text)

st.divider()
choice = st.radio(
    label="Was soll übersetzt werden?",
    options=["Ausgangstext", "Zusammenfassung"],
    key="translate_choice"
)

if st.button("Übersetzen"):
    # Bestimmen welcher Text übersetzt werden soll:
    if choice == "Zusammenfassung":
        source_text = st.session_state.summary_text
    else:
        source_text = st.session_state.full_text
    
    # Prüfen ob Text vorhanden ist:
    if not source_text.strip():
        st.warning("Bitte erst ein PDF laden oder eine Zusammenfassung erstellen")
    else:
        with st.spinner("Übersetze..."):
            translator = get_translator()
            result = translator(source_text)
            st.session_state.translated_text = result[0]["translation_text"]
            st.subheader("Übersetzung")
            st.write(st.session_state.translated_text)
            
    # Download Button Logik:
    if st.session_state.translated_text:
        filename = f"Übersetzung_{st.session_state.translate_choice.lower()}.txt"
        st.download_button(
            label="Übersetzung downloaden",
            data=st.session_state.translated_text,
            file_name=filename,
            mime="text/plain"
        )  