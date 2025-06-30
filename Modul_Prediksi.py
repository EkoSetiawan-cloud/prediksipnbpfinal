import streamlit as st
import pandas as pd
import numpy as np
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.stattools import adfuller

def prediksi_pnbp_page():
    st.markdown("<h1 style='color:#3C8DBC;'>📈 Model Prediksi PNBP - ARIMA</h1>", unsafe_allow_html=True)

    # Cek ketersediaan data
    if "pnbp_series_arima" not in st.session_state:
        st.warning("⚠️ Data belum tersedia. Jalankan modul preprocessing terlebih dahulu.")
        return

    series = st.session_state["pnbp_series_arima"].copy()

    st.subheader("📊 Data Siap ARIMA")
    st.line_chart(series)

    # Uji stasioneritas
    st.subheader("🧪 Uji Stasioneritas (ADF Test)")
    adf_result = adfuller(series)
    adf_stat = adf_result[0]
    adf_pvalue = adf_result[1]

    st.markdown(f"- **ADF Statistic**: `{adf_stat:.4f}`")
    st.markdown(f"- **p-value**: `{adf_pvalue:.4f}`")
    if adf_pvalue <= 0.05:
        st.success("✅ Data sudah stasioner (p ≤ 0.05)")
        d = 0
    else:
        st.warning("⚠️ Data belum stasioner. Akan diterapkan differencing (d=1).")
        d = 1

    # Tentukan parameter ARIMA
    p, q = 1, 1
    st.markdown(f"📌 Menggunakan parameter: **ARIMA({p}, {d}, {q})**")

    # Fit ARIMA
    model = ARIMA(series, order=(p, d, q))
    model_fit = model.fit()
    st.success("✅ Model ARIMA berhasil dilatih.")

    st.subheader("📈 Ringkasan Model")
    st.text(model_fit.summary())

    # Prediksi 2 tahun ke depan
    tahun_akhir = series.index.max()
    tahun_forecast = 2
    forecast_years = list(range(tahun_akhir + 1, tahun_akhir + tahun_forecast + 1))
    forecast = model_fit.forecast(steps=tahun_forecast)
    forecast.index = forecast_years

    # Gabungkan dengan data historis
    df_actual = series.reset_index()
    df_actual.columns = ["Tahun", "Aktual"]

    df_forecast = forecast.reset_index()
    df_forecast.columns = ["Tahun", "Prediksi"]

    df_final = pd.merge(df_actual, df_forecast, on="Tahun", how="outer")
    df_final["Jenis Tahun"] = df_final["Aktual"].apply(lambda x: "Historis" if pd.notnull(x) else "Prediksi")

    # Simpan ke session state
    st.session_state["prediksi_pnbp"] = df_final.copy()

    # Format rupiah untuk tampilan
    def format_rupiah(x):
        return f"Rp {x:,.0f}".replace(",", ".") if pd.notnull(x) else "-"

    df_display = df_final.copy()
    df_display["Aktual"] = df_display["Aktual"].apply(format_rupiah)
    df_display["Prediksi"] = df_display["Prediksi"].apply(format_rupiah)

    st.subheader("📄 Hasil Prediksi ARIMA")
    st.caption("Tabel berikut menampilkan nilai aktual dan hasil proyeksi 2 tahun ke depan.")
    st.dataframe(df_display, use_container_width=True)

    st.info("ℹ️ Lanjutkan ke menu **Visualisasi** dan **Evaluasi** untuk analisis lanjut.")
