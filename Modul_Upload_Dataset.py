import streamlit as st
import pandas as pd

def upload_dataset_page():
    st.title("📂 Upload Dataset PNBP")
    st.write("Silakan upload file Excel (*.xlsx) yang berisi data historis PNBP dari tahun 2014–2024.")

    uploaded_file = st.file_uploader("Pilih file Excel", type=["xlsx"])

    if uploaded_file is not None:
        try:
            df = pd.read_excel(uploaded_file)
            st.success("✅ File berhasil diunggah!")
            st.write("📄 Pratinjau Data:")
            st.dataframe(df)

            # Menyimpan dataframe ke session_state agar bisa digunakan di halaman lain
            st.session_state["dataset_pnbp"] = df

        except Exception as e:
            st.error(f"Terjadi kesalahan saat membaca file: {e}")
    else:
        st.info("⬆️ Upload file untuk mulai.")
