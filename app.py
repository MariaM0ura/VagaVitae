import streamlit as st
import os
from pathlib import Path
import uuid
from src.personalized_resume import process

# Criar diretório data se não existir
DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

# Novo Estilo CSS
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;600&display=swap');
        
        html, body, [class*="css"] {
            font-family: 'Poppins', sans-serif;
            background-color: #f9f9f9;
        }
        .main {
            padding: 2rem 1rem;
        }
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
            max-width: 60rem;
            margin: auto;
        }
        .stButton button {
            background-color: #0066cc;
            color: white;
            border: none;
            padding: 0.75rem;
            border-radius: 0.5rem;
            font-size: 1rem;
            transition: background-color 0.3s;
            width: 100%;
        }
        .stButton button:hover {
            background-color: #004c99;
        }
        .stTextInput>div>div>input {
            padding: 0.75rem;
            border-radius: 0.5rem;
            border: 1px solid #ccc;
        }
        .stFileUploader>div>div {
            background-color: #fff;
            border: 2px dashed #ccc;
            padding: 2rem;
            border-radius: 0.5rem;
            text-align: center;
        }
        footer, header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# Inicialização da sessão
if 'show_download' not in st.session_state:
    st.session_state.show_download = False
if 'result' not in st.session_state:
    st.session_state.result = None

# Cabeçalho
st.markdown("<h1 style='text-align: center; color: #0066cc;'>VagaVitae</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 1.2rem;'>Crie um currículo personalizado para a vaga que você deseja!</p>", unsafe_allow_html=True)

# Entrada de dados
with st.container():
    job_url = st.text_input("🔗 Insira o link da vaga:", placeholder="https://www.linkedin.com/jobs/view/<job_id>")
    pdf_file = st.file_uploader("📄 Faça upload do seu currículo:", type=["pdf"])

left_col, center_col, right_col = st.columns([1, 2, 1])

if not st.session_state.show_download:
    if center_col.button("🚀 Produzir Currículo Personalizado"):
        if job_url and pdf_file:
            try:
                file_id = str(uuid.uuid4())
                pdf_path = DATA_DIR / f"{file_id}.pdf"
                
                with open(pdf_path, "wb") as f:
                    f.write(pdf_file.getbuffer())

                status_container = st.empty()
                status_container.success("✅ Link e PDF recebidos com sucesso!")

                with st.spinner("🛠️ Processando seu currículo..."):
                    try:
                        result = process(file_id, job_url)
                        if result["status"] == "success":
                            status_container.empty()
                            status_container.success("🎯 Currículo personalizado gerado com sucesso!")

                            st.session_state.pdf_path = result["pdf_path"]
                            st.session_state.result = result
                            st.session_state.show_download = True
                            st.rerun()
                    except Exception as e:
                        st.error(f"❌ Erro ao processar o currículo: {str(e)}")
                        raise

            except Exception as e:
                st.error(f"❌ Erro ao processar: {str(e)}")
            finally:
                if os.path.exists(pdf_path):
                    os.remove(pdf_path)
        else:
            st.error("⚠️ Por favor, insira o link da vaga e faça upload do PDF.")
else:
    try:
        with open(st.session_state.pdf_path, "rb") as pdf_file:
            center_col.download_button(
                label="⬇️ Baixar Currículo PDF",
                data=pdf_file,
                file_name="curriculo_personalizado.pdf",
                mime="application/pdf"
            )

            metrics_container = center_col.container()

            metrics_container.markdown(
                f"<h3 style='text-align: center;'>Sua correspondência com essa vaga é de: "
                f"<span style='color: #0066cc;'>{st.session_state.result['result']['match_metric']}</span></h3>", 
                unsafe_allow_html=True
            )

            all_reqs = set(st.session_state.result['result']['requirements'])
            matched_reqs = set(st.session_state.result['result']['matched_requirements'])
            missing_reqs = all_reqs - matched_reqs

            if missing_reqs:
                metrics_container.markdown(
                    "<h4 style='text-align: center;'>Requisitos a desenvolver:</h4>",
                    unsafe_allow_html=True
                )
                for req in missing_reqs:
                    metrics_container.markdown(
                        f"<p style='text-align: center; color: #ffc04b;'>⚡ {req}</p>",
                        unsafe_allow_html=True
                    )
            if center_col.button("🔄 Reiniciar"):
                st.session_state.show_download = False
                st.session_state.result = None
                st.session_state.pdf_path = None
                st.rerun()

    except Exception as e:
        st.error(f"❌ Erro ao exibir resultado: {str(e)}")
