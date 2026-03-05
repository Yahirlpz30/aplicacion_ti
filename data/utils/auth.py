import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(
    page_title="Sistema Estatal Anticorrupción",
    layout="wide"
)

# -----------------------------
# FUNCIÓN LOGIN
# -----------------------------

def check_login(user, password):

    try:
        users = pd.read_excel("data/user-pass.xlsx")
    except:
        st.error("No se encontró el archivo user-pass.xlsx")
        return False

    user_row = users[
        (users["user"] == user) &
        (users["password"] == password)
    ]

    return not user_row.empty


# -----------------------------
# SESIÓN
# -----------------------------

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "acciones" not in st.session_state:

    st.session_state.acciones = pd.DataFrame({
        "Estrategia": [],
        "Linea de Acción": [],
        "Acción": [],
        "Inicio": [],
        "Fin": [],
        "Tipo de Acción": [],
        "Temática": []
    })


# -----------------------------
# LOGIN
# -----------------------------

def login():

    st.title("Sistema Estatal Anticorrupción")

    user = st.text_input("Usuario")
    password = st.text_input("Contraseña", type="password")

    if st.button("Ingresar"):

        if check_login(user, password):

            st.session_state.logged_in = True
            st.success("Acceso correcto")
            st.rerun()

        else:

            st.error("Usuario o contraseña incorrectos")


# -----------------------------
# APP PRINCIPAL
# -----------------------------

def main_app():

    st.title("Reporte de Acciones 2025")
    st.subheader("Programa de Implementación del PNA")

    st.divider()

    col1, col2, col3 = st.columns(3)

    add = col1.button("➕ Agregar Acción")
    save = col2.button("💾 Guardar Borrador")
    send = col3.button("📤 Enviar")

    st.divider()

    if add:

        nueva = pd.DataFrame({
            "Estrategia": [""],
            "Linea de Acción": [""],
            "Acción": [""],
            "Inicio": [""],
            "Fin": [""],
            "Tipo de Acción": [""],
            "Temática": [""]
        })

        st.session_state.acciones = pd.concat(
            [st.session_state.acciones, nueva],
            ignore_index=True
        )

    tabla = st.data_editor(
        st.session_state.acciones,
        num_rows="dynamic",
        use_container_width=True
    )

    st.session_state.acciones = tabla

    if save:

        tabla.to_excel("acciones_borrador.xlsx", index=False)

        st.success("Borrador guardado")

    if send:

        tabla["fecha_envio"] = datetime.now()

        tabla.to_excel("acciones_enviadas.xlsx", index=False)

        st.success("Acciones enviadas correctamente")


# -----------------------------
# FLUJO
# -----------------------------

if not st.session_state.logged_in:

    login()

else:

    main_app()
