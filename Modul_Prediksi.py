import streamlit as st
import pandas as pd
from statsmodels.tsa.holtwinters import ExponentialSmoothing
import numpy as np

def prediksi_pnbp_page():
    st.markdown("""
        <h1 style="color:#3C8DBC;">🔧 Prediksi Total PNBP Tahunan</h1>
     
    if "pnbp_total_tahunan" not in st.session_state:
        st.warning("⚠️ Data agregasi belum tersedia. Jalankan preprocessing terlebih dahulu.")
        return

    df = st.session_state["pnbp_total_tahunan"].copy()
    df.columns = df.columns.str.strip().str.lower()
    df = df.sort_values("tahun")
    df["total_pnbp"] = pd.to_numeric(df["total_pnbp"], errors="coerce")

    tahun_max = df["tahun"].max()
    tahun_forecast = 2
    forecast_years = list(range(tahun_max + 1, tahun_max + tahun_forecast + 1))

    st.subheader("\U0001F9E0 Metode Prediksi yang Digunakan")
    st.markdown("""
    Aplikasi ini menggunakan metode **Double Exponential Smoothing (Holt’s Method)** untuk memprediksi total PNBP tahunan.

    ### 🧠 Alasan Pemilihan
    Model ini sangat cocok untuk data PNBP karena:
    - Memiliki tren linier tahunan yang konsisten
    - Tidak menunjukkan pola musiman yang kompleks
    - Diperlukan model yang cepat, stabil, dan mudah dijelaskan
    """)

    st.markdown("""
    ### ⚙️ Cara Kerja Model
    Double exponential smoothing menggunakan dua komponen utama:
    - **Level (L_t)**: estimasi nilai saat ini
    - **Trend (T_t)**: estimasi arah perubahan
    """)

    st.latex(r"""
    \begin{aligned}
    L_t &= \alpha y_t + (1 - \alpha)(L_{t-1} + T_{t-1}) \\
    T_t &= \beta (L_t - L_{t-1}) + (1 - \beta) T_{t-1} \\
    \hat{y}_{t+m} &= L_t + m \cdot T_t
    \end{aligned}
    """)

    st.markdown("""
    ### ✅ Keunggulan
    - Cepat dan efisien
    - Sederhana untuk interpretasi dan visualisasi
    - Cocok untuk data dengan tren linier

    ### ⚠️ Keterbatasan
    - Tidak bisa menangani musiman
    - Kurang fleksibel jika tren berubah drastis

    ### 📚 Dukungan Ilmiah
    - Dikembangkan oleh Charles Holt (1957) dan disempurnakan oleh Winters
    - Digunakan luas dalam ekonomi, industri, dan bisnis ([Penn State Online](https://online.stat.psu.edu/stat501/lesson/6/6.2))
    - Validasi empiris oleh berbagai studi time series forecasting
    """)

    # Double Smoothing Prediction
    series = df.set_index("tahun")["total_pnbp"]
    model = ExponentialSmoothing(series, trend="add", seasonal=None, initialization_method="estimated")
    model_fit = model.fit()
    fitted = model_fit.fittedvalues
    forecast = model_fit.forecast(tahun_forecast)
    fitted.index = series.index
    forecast.index = forecast_years
    df_pred = pd.concat([fitted, forecast]).reset_index()
    df_pred.columns = ["Tahun", "Prediksi"]
    st.success("✅ Prediksi berhasil dilakukan dengan Double Smoothing.")

    # Gabungkan dengan data aktual
    df_aktual = df.rename(columns={"tahun": "Tahun", "total_pnbp": "Aktual"})
    df_final = pd.merge(df_pred, df_aktual[["Tahun", "Aktual"]], on="Tahun", how="left")
    df_final["Jenis Tahun"] = df_final["Aktual"].apply(lambda x: "Historis" if pd.notnull(x) else "Prediksi")
    st.session_state["prediksi_pnbp"] = df_final.copy()

    # Format ke Rupiah
    def format_rupiah(x):
        return f"Rp {x:,.0f}".replace(",", ".") if pd.notnull(x) else "-"

    df_display = df_final.copy()
    df_display["Aktual"] = df_display["Aktual"].apply(format_rupiah)
    df_display["Prediksi"] = df_display["Prediksi"].apply(format_rupiah)

    st.subheader("📄 Hasil Prediksi")
    st.caption("Tabel berikut menampilkan nilai aktual dan hasil proyeksi untuk dua tahun ke depan.")
    st.dataframe(df_display, use_container_width=True)

    st.info("ℹ️ Lanjutkan ke menu **Visualisasi** untuk melihat grafik interaktif hasil prediksi.")
