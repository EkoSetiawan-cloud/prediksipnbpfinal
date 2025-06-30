import streamlit as st
import pandas as pd
import numpy as np
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.stattools import adfuller

def prediksi_pnbp_page():
    st.markdown("<h1 style='color:#3C8DBC;'>📈 Model Prediksi PNBP - ARIMA</h1>", unsafe_allow_html=True)

    if "pnbp_series_arima" not in st.session_state:
        st.warning("⚠️ Data belum tersedia. Jalankan modul preprocessing terlebih dahulu.")
        return

    series = st.session_state["pnbp_series_arima"].copy()
    st.subheader("📊 Data Siap ARIMA")
    st.line_chart(series)

    st.subheader("🧪 Uji Stasioneritas (ADF Test)")
    adf_result = adfuller(series)
    st.markdown(f"""
    - **ADF Statistic**: `{adf_result[0]:.4f}`
    - **p-value**: `{adf_result[1]:.4f}`
    """)
    if adf_result[1] <= 0.05:
        st.success("✅ Data sudah stasioner (p ≤ 0.05)")
        d = 0
    else:
        st.warning("⚠️ Data belum stasioner (p > 0.05). Differencing akan diterapkan.")
        d = 1

    st.subheader("⚙️ Pemilihan Parameter ARIMA(p,d,q)")
    st.markdown("Untuk percobaan awal, digunakan nilai `(p=1, d=1, q=1)` secara default. Diimplementasikan secara manual tanpa auto_tuning.")
    p, q = 1, 1

    st.info(f"Model ARIMA({p},{d},{q}) sedang dilatih...")

    # Fit model
    model = ARIMA(series, order=(p, d, q))
    model_fit = model.fit()
    st.success("✅ Model ARIMA berhasil dilatih.")

    st.subheader("📈 Ringkasan Model")
    st.text(model_fit.summary())

    # Prediksi
    tahun_max = series.index.max()
    tahun_forecast = 2
    forecast_years = list(range(tahun_max + 1, tahun_max + tahun_forecast + 1))

    forecast = model_fit.forecast(steps=tahun_forecast)
    forecast.index = forecast_years

    # Gabung hasil aktual & prediksi
    df_actual = series.reset_index()
    df_actual.columns = ["Tahun", "Aktual"]

    df_forecast = forecast.reset_index()
    df_forecast.columns = ["Tahun", "Prediksi"]

    df_final = pd.merge(df_actual, df_forecast, on="Tahun", how="outer")
    df_final["Jenis Tahun"] = df_final["Aktual"].apply(lambda x: "Historis" if pd.notnull(x) else "Prediksi")

    st.session_state["prediksi_pnbp"] = df_final.copy()

    # Tampilkan tabel
    def format_rupiah(x):
        return f"Rp {x:,.0f}".replace(",", ".") if pd.notnull(x) else "-"

    df_display = df_final.copy()
    df_display["Aktual"] = df_display["Aktual"].apply(format_rupiah)
    df_display["Prediksi"] = df_display["Prediksi"].apply(format_rupiah)

    st.subheader("📄 Hasil Prediksi ARIMA")
    st.caption("Tabel berikut menampilkan nilai aktual dan hasil proyeksi 2 tahun ke depan.")
    st.dataframe(df_display, use_container_width=True)

    st.info("ℹ️ Lanjutkan ke menu **Visualisasi** dan **Evaluasi** untuk analisis lanjut.")
