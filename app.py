import streamlit as st
import google.generativeai as genai
import re

# Configurar API Key
genai.configure(api_key="AIzaSyCxEJH-IffKIu3CiR-2-OfZ1vbETEpeteY")
modelo = genai.GenerativeModel("models/gemini-1.5-pro")

# Configuración general
st.set_page_config(page_title="Asistente Educativo con IA", page_icon="🧠", layout="centered")

# Estilos modernos para fines educativos
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(to right, #f0f4f8, #d9e8ff);
        font-family: 'Segoe UI', sans-serif;
        color: #1a1a1a;
    }
    .title {
        font-size: 2.3rem;
        font-weight: bold;
        color: #004080;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .subtitle {
        font-size: 1.2rem;
        text-align: center;
        color: #333;
        margin-bottom: 2rem;
    }
    .info-box {
        background-color: #ffffffaa;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0px 2px 10px rgba(0,0,0,0.1);
    }
    .footer {
        font-size: 0.9rem;
        text-align: center;
        margin-top: 30px;
        color: #555;
    }
    </style>
""", unsafe_allow_html=True)

# Título e introducción
st.markdown('<div class="title">✨ Asistente Educativo con IA 🧠</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Una herramienta didáctica para estudiantes de secundaria y universidad.</div>', unsafe_allow_html=True)

st.markdown("""<div class='info-box'>
Soy **M.Sc. Néstor Fabio Montoya Palacios**, docente de **matemáticas, física y programación**.  
He creado esta aplicación con fines educativos para que explores conceptos, resuelvas dudas y avances en tu aprendizaje con ayuda de **inteligencia artificial**.  
Puedes preguntarme sobre temas académicos y científicos, y si es posible, la IA responderá con ejemplos y código.
</div>""", unsafe_allow_html=True)

# Entrada del usuario
st.markdown("### ✏️ Escribe tu pregunta:")
pregunta = st.text_area("", height=100, placeholder="Ejemplo: ¿Qué es una derivada?")

# Botón de consulta
if st.button("🔍 Consultar"):
    if pregunta.strip() == "":
        st.warning("Por favor, escribe una pregunta.")
    else:
        with st.spinner("Consultando a Gemini..."):
            try:
                respuesta = modelo.generate_content(pregunta)
                texto = respuesta.text
                st.markdown("### 📘 Respuesta de Gemini:")
                st.markdown(texto)

                # Guardar historial
                with open("historial_estudiantes.txt", "a", encoding="utf-8") as f:
                    f.write(f"""
Pregunta:
{pregunta}

Respuesta:
{texto}

{'-'*60}
""")

                # Buscar y ejecutar código Python dentro de la respuesta
                bloques = re.findall(r"```python(.*?)```", texto, re.DOTALL)
                if bloques:
                    for bloque in bloques:
                        st.markdown("### ⚙️ Código detectado:")
                        st.code(bloque.strip(), language="python")
                        try:
                            exec(bloque.strip(), globals())
                        except Exception as e:
                            st.error(f"Error al ejecutar el código: {e}")
                else:
                    st.info("No se detectó código Python en la respuesta.")
            except Exception as e:
                st.error(f"Ocurrió un error consultando a Gemini: {e}")

# Pie de página
st.markdown('<div class="footer">Universidad del Valle | Universidad Tecnológica de Pereira | Institución Educativa Gabo<br>Con fines netamente educativos. © 2025</div>', unsafe_allow_html=True)
