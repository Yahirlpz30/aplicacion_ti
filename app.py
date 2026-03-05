import streamlit as st
import pandas as pd
from datetime import datetime

from utils.auth import check_login
from utils.dropbox_manager import read_excel_dropbox, upload_excel_dropbox


st.set_page_config(
    page_title="Sistema Estatal Anticorrupción",
    layout="wide"
)


# -------------------------
# SESSION STATE
# -------------------------

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "acciones" not in st.session_state:
    st.session_state.acciones = pd.DataFrame()


# -------------------------
# LOGIN
# -------------------------

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


# -------------------------
# APP PRINCIPAL
# -------------------------

def main_app():

    st.title("Reporte de Acciones 2025")

    st.divider()

    col1, col2, col3 = st.columns(3)

    add = col1.button("Agregar Acción")
    save = col2.button("Guardar")
    send = col3.button("Enviar")

    if st.session_state.acciones.empty:

        st.session_state.acciones = pd.DataFrame({
            "Estrategia": [],
            "Linea": [],
            "Accion": [],
            "Inicio": [],
            "Fin": [],
            "Tipo": [],
            "Tematica": []
        })

    if add:

        nueva = pd.DataFrame({
            "Estrategia": [""],
            "Linea": [""],
            "Accion": [""],
            "Inicio": [""],
            "Fin": [""],
            "Tipo": [""],
            "Tematica": [""]
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

        upload_excel_dropbox(
            tabla,
            "/acciones/borrador.xlsx"
        )

        st.success("Borrador guardado en Dropbox")

    if send:

        tabla["fecha_envio"] = datetime.now()

        upload_excel_dropbox(
            tabla,
            "/acciones/enviado.xlsx"
        )

        st.success("Información enviada")


# -------------------------
# FLUJO
# -------------------------

if not st.session_state.logged_in:

    login()

else:

    main_app()
