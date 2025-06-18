import streamlit as st
import pandas as pd

def preprocessing_agregasi_page():
    st.title("🔧 Preprocessing & Agregasi Data PNBP")

    if "dataset_pnbp" not in st.session_state:
        st.warning("⚠️ Dataset belum tersedia. Silakan upload terlebih dahulu melalui Modul Input.")
        return

    df_raw = st.session_state["dataset_pnbp"].copy()

    st.subheader("📄 Dataset Asli (Tampilan Awal)")
    st.dataframe(df_raw)

    # Transpose data: kolom menjadi baris, baris menjadi kolom
    df_transposed = df_raw.set_index(df_raw.columns[0]).transpose()

    # Reset index agar tahun jadi kolom
    df_transposed.reset_index(inplace=True)
    df_transposed.rename(columns={"index": "tahun"}, inplace=True)

    # Pastikan kolom tahun dalam integer
    df_transposed["tahun"] = pd.to_numeric(df_transposed["tahun"], errors="coerce")
    df_transposed.dropna(subset=["tahun"], inplace=True)
    df_transposed["tahun"] = df_transposed["tahun"].astype(int)

    st.subheader("📌 Data Setelah Transpose")
    st.dataframe(df_transposed)

    # Hitung total PNBP dari seluruh jenis
    nominal_cols = [col for col in df_transposed.columns if col != "tahun"]
    df_transposed["total_pnbp"] = df_transposed[nominal_cols].sum(axis=1)

    df_total_per_tahun = df_transposed[["tahun", "total_pnbp"]]

    # Format ke Rupiah
    def format_rupiah(x):
        return f"Rp {x:,.0f}".replace(",", ".") if pd.notnull(x) else "-"

    df_display = df_total_per_tahun.copy()
    df_display["total_pnbp"] = df_display["total_pnbp"].apply(format_rupiah)

    st.subheader("📊 Agregasi Total PNBP per Tahun")
    st.dataframe(df_display)

    # Simpan data mentah (tanpa format) ke session_state
    st.session_state["pnbp_total_tahunan"] = df_total_per_tahun
