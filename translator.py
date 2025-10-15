from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
from transformers import pipeline 

#translator = pipeline(task='translation', model='Helsinki-NLP/opus-mt-en-ru', use_safetensors=True)
#text = 'Artificial intelligence is changing the world!'
#result = translator(text)
#print(result[0]['translation_text'])




import io
import fitz  # PyMuPDF
import streamlit as st
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline

MODEL_ID = "sshleifer/distilbart-cnn-12-6"  # kleiner & schneller als bart-large-cnn

def extract_text_from_pdf(file) -> str:
    try:
        file.seek(0)
    except Exception:
        pass
    data = file.read()
    if not data:
        return ""
    with fitz.open(stream=io.BytesIO(data), filetype="pdf") as doc:
        texts = [p.get_text("text") for p in doc]
    return "\n".join(texts).strip()

@st.cache_resource(show_spinner=False)
def get_summarizer():
    tok = AutoTokenizer.from_pretrained(MODEL_ID, use_fast=True)
    mdl = AutoModelForSeq2SeqLM.from_pretrained(
        MODEL_ID,
        use_safetensors=True,     # nur .safetensors laden
        low_cpu_mem_usage=False,  # Lazy Loading AUS -> keine Meta-Tensors
        device_map=None,          # nichts auf "meta" initialisieren
        torch_dtype=None          # Standard FP32 auf CPU
    )
    return pipeline(
        "summarization",
        model=mdl,
        tokenizer=tok,
        device=-1   # CPU
    )
st.title("PDF zusammenfassen & (optional) übersetzen")
uploaded = st.file_uploader("PDF auswählen", type=["pdf"])

full_text = ""
if uploaded:
    full_text = extract_text_from_pdf(uploaded)
    if full_text:
        st.success(f"PDF geladen, {len(full_text)} Zeichen")
        st.text_area("Extrahierter Text (Vorschau)", full_text[:5000], height=300)
    else:
        st.error("Kein extrahierbarer Text gefunden (evtl. Scan-PDF).")

if uploaded and full_text:
    input_text = full_text[:2000]  # CPU-freundlich kürzen
    if st.button("Zusammenfassung erstellen"):
        with st.spinner("Erstelle Zusammenfassung..."):
            summarizer = get_summarizer()
            # Limits passend setzen, sonst meckert die Pipeline
            summary = summarizer(
            input_text,
            max_length=220,
            min_length=60,
            do_sample=False,
            truncation=True
)   [0]["summary_text"]
 
            st.subheader("Zusammenfassung")
            st.write(summary)
 