import pandas as pd
import streamlit as st

def preprocessing_agregasi_page():
    st.title("🧪 Preprocessing & Agregasi Data PNBP")

    if "dataset_pnbp" not in st.session_state:
        st.warning("Silakan upload dataset terlebih dahulu di modul Input Dataset.")
        return

    # Ambil data dari session
    df_raw = st.session_state.dataset_pnbp.copy()
    st.subheader("🔍 Data Awal (Per Jenis PNBP per Tahun)")
    st.dataframe(df_raw)

    # Transpose data
    df_transposed = df_raw.set_index(df_raw.columns[0]).T.reset_index()
    df_transposed = df_transposed.rename(columns={"index": "Tahun"})
    df_transposed["Tahun"] = df_transposed["Tahun"].astype(int)

    st.subheader("🔄 Data Setelah Transpose")
    st.dataframe(df_transposed)

    # Hitung agregasi total PNBP per tahun
    df_transposed["Total PNBP"] = df_transposed.drop(columns=["Tahun"]).sum(axis=1)
    df_agregasi = df_transposed[["Tahun", "Total PNBP"]]

    st.subheader("📊 Agregasi Total PNBP per Tahun")
    st.dataframe(df_agregasi)

    # Simpan ke session state
    st.session_state.transposed_data = df_transposed
    st.session_state.pnbp_total_tahunan = df_agregasi

    st.success("Data berhasil diproses dan disimpan untuk digunakan pada modul selanjutnya.")
