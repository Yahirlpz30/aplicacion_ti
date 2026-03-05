import dropbox
import pandas as pd
from io import BytesIO
import streamlit as st

DROPBOX_TOKEN = st.secrets["DROPBOX_TOKEN"]

dbx = dropbox.Dropbox(DROPBOX_TOKEN)


def read_excel_dropbox(path):

    metadata, res = dbx.files_download(path)

    with BytesIO(res.content) as f:
        df = pd.read_excel(f)

    return df


def upload_excel_dropbox(df, path):

    output = BytesIO()

    df.to_excel(output, index=False)

    dbx.files_upload(
        output.getvalue(),
        path,
        mode=dropbox.files.WriteMode.overwrite
    )
