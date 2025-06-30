import streamlit as st
import pandas as pd

def preprocessing_agregasi_page():
    st.markdown("""
        <h1 style="color:#3C8DBC;">🔧 Preprocessing & Agregasi Data PNBP</h1>
        <p style="font-size:16px; color:gray;">
            Proses ini bertujuan untuk mengubah format data mentah menjadi bentuk agregat tahunan 
            agar dapat digunakan pada proses prediksi. Data akan di-transpose, dibersihkan, dan dijumlahkan
            berdasarkan <strong>total PNBP per tahun</strong>.
        </p>
        <hr style="margin-top:20px; margin-bottom:20px;">
    """, unsafe_allow_html=True)

    if "dataset_pnbp" not in st.session_state:
        st.warning("⚠️ Dataset belum tersedia. Silakan upload terlebih dahulu melalui Modul Input.")
        return

    # Salin data asli
    df_raw = st.session_state["dataset_pnbp"].copy()

    st.subheader("📄 Dataset Asli (Tampilan Awal)")
    st.caption("Data mentah sebelum diubah ke format prediksi.")
    st.dataframe(df_raw, use_container_width=True)

    # Transpose data
    df_transposed = df_raw.set_index(df_raw.columns[0]).transpose()
    df_transposed.reset_index(inplace=True)
    df_transposed.rename(columns={"index": "tahun"}, inplace=True)
    df_transposed["tahun"] = pd.to_numeric(df_transposed["tahun"], errors="coerce")
    df_transposed.dropna(subset=["tahun"], inplace=True)
    df_transposed["tahun"] = df_transposed["tahun"].astype(int)

    st.subheader("🔁 Data Setelah Transpose")
    st.caption("Baris menjadi kolom dan kolom menjadi baris, dengan 'tahun' sebagai index.")
    st.dataframe(df_transposed, use_container_width=True)

    # Agregasi total PNBP
    nominal_cols = [col for col in df_transposed.columns if col != "tahun"]
    df_transposed["total_pnbp"] = df_transposed[nominal_cols].sum(axis=1)
    df_total_per_tahun = df_transposed[["tahun", "total_pnbp"]]

    # Tampilkan hanya versi format rupiah untuk UI
    df_display = df_total_per_tahun.copy()
    df_display["total_pnbp"] = df_display["total_pnbp"].apply(lambda x: f"Rp {x:,.0f}".replace(",", "."))

    st.subheader("📊 Agregasi Total PNBP per Tahun")
    st.caption("Total kumulatif dari semua jenis PNBP untuk setiap tahun.")
    st.dataframe(df_display, use_container_width=True)

    # Simpan DataFrame dan Series numerik untuk prediksi
    st.session_state["pnbp_total_tahunan"] = df_total_per_tahun  # untuk Holt's
    st.session_state["pnbp_series_arima"] = df_total_per_tahun.set_index("tahun")["total_pnbp"]  # untuk ARIMA

    st.success("✅ Data berhasil diproses dan disimpan dalam format numerik untuk model prediksi.")
