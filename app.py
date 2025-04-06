import streamlit as st
import google.generativeai as genai
import re
import os

# Configurar API Key (ocúltala en producción)
genai.configure(api_key="AIzaSyCxEJH-IffKIu3CiR-2-OfZ1vbETEpeteY")
modelo = genai.GenerativeModel("models/gemini-1.5-pro")

# Configuración de la página
st.set_page_config(page_title="Asistente IA Educativo", page_icon="📘", layout="wide")

# Estilos personalizados
st.markdown("""
    <style>
    .stApp {{
        background-color: #f5f9ff;
        font-family: 'Segoe UI', sans-serif;
    }}
    .big-title {{
        text-align: center;
        font-size: 2.5rem;
        color: #007bff;
        margin-bottom: 0.5rem;
    }}
    .sub-title {{
        text-align: center;
        font-size: 1.2rem;
        color: #555;
        margin-bottom: 2rem;
    }}
    .firma {{
        text-align: right;
        font-size: 0.9rem;
        color: #888;
        margin-top: 2rem;
    }}
    </style>
""", unsafe_allow_html=True)

# Introducción
st.markdown('<div class="big-title">💬 Asistente Educativo con Gemini</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Desarrollado por el profesor Néstor Fabio Montoya para apoyar el aprendizaje de los estudiantes de la institución educativa GABO y de la universidad del Valle sede cartago</div>', unsafe_allow_html=True)

# Entrada del usuario
pregunta = st.text_area("✏️ Escribe tu pregunta aquí", height=120)

if st.button("🔍 Consultar a Gemini"):
    if pregunta.strip() == "":
        st.warning("Por favor, escribe una pregunta.")
    else:
        with st.spinner("Consultando a Gemini..."):
            try:
                respuesta = modelo.generate_content(pregunta)
                texto = respuesta.text
                st.markdown("### 📘 Respuesta de Gemini:")
                st.markdown(texto)

                # Guardar pregunta y respuesta
                with open("historial_gemini.txt", "a", encoding="utf-8") as f:
                    f.write(f"Pregunta:\n{pregunta}\nRespuesta:\n{texto}\n{'-'*60}\n")

                # Detectar y ejecutar código si existe
                bloques = re.findall(r"```python(.*?)```", texto, re.DOTALL)
                if bloques:
                    for bloque in bloques:
                        st.markdown("### ⚙️ Ejecutando código generado:")
                        st.code(bloque.strip(), language="python")
                        try:
                            exec(bloque.strip(), globals())
                        except Exception as e:
                            st.error(f"Error al ejecutar el código: {e}")
                else:
                    st.info("No se detectó código Python en la respuesta.")
            except Exception as e:
                st.error(f"Ocurrió un error consultando a Gemini: {e}")

# Firma
st.markdown('<div class="firma">M.Sc. Néstor Fabio Montoya Palacios<br>Docente e Investigador</div>', unsafe_allow_html=True)
