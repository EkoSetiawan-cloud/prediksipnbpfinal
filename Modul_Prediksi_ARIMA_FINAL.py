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
    
    p, q = 1, 1
    st.markdown(f"📌 Menggunakan parameter: **ARIMA({p}, {d}, {q})**")
    
    model = ARIMA(series, order=(p, d, q))
    model_fit = model.fit()
    
    st.success("✅ Model ARIMA berhasil dilatih.")
    
    st.subheader("📈 Ringkasan Model")
    st.text(model_fit.summary())
    
    # Prediksi
    tahun_akhir = series.index.max()
    tahun_forecast = 2
    forecast_years = list(range(tahun_akhir + 1, tahun_akhir + tahun_forecast + 1))
    
    forecast = model_fit.forecast(steps=tahun_forecast)
    
    # Debug: Cek nilai forecast
    st.write("Debug - Forecast values:", forecast.values)
    st.write("Debug - Forecast years:", forecast_years)
    
    # Buat list untuk menampung semua data
    all_years = list(series.index) + forecast_years
    all_actual = list(series.values) + [None] * len(forecast_years)
    all_prediksi = [None] * len(series) + list(forecast.values)
    all_jenis = ["Historis"] * len(series) + ["Prediksi"] * len(forecast_years)
    
    # Buat DataFrame final
    df_final = pd.DataFrame({
        "Tahun": all_years,
        "Aktual": all_actual,
        "Prediksi": all_prediksi,
        "Jenis Tahun": all_jenis
    })
    
    # Simpan ke session state
    st.session_state["prediksi_pnbp"] = df_final.copy()
    
    # Buat DataFrame untuk display dengan formatting
    df_display = df_final.copy()
    
    # Format kolom Aktual
    df_display["Aktual"] = df_display["Aktual"].apply(
        lambda x: f"Rp {x:,.0f}".replace(",", ".") if x is not None and pd.notnull(x) else "-"
    )
    
    # Format kolom Prediksi
    df_display["Prediksi"] = df_display["Prediksi"].apply(
        lambda x: f"Rp {x:,.0f}".replace(",", ".") if x is not None and pd.notnull(x) else "-"
    )
    
    st.subheader("📄 Hasil Prediksi ARIMA")
    st.caption("Tabel berikut menampilkan nilai aktual dan hasil proyeksi 2 tahun ke depan.")
    
    # Tampilkan tabel
    st.dataframe(df_display, use_container_width=True)
    
    # Tampilkan ringkasan prediksi
    st.subheader("🎯 Ringkasan Prediksi")
    for i, year in enumerate(forecast_years):
        if i < len(forecast.values):
            formatted_value = f"Rp {forecast.values[i]:,.0f}".replace(",", ".")
            st.markdown(f"- **Tahun {year}**: {formatted_value}")
    
    st.info("ℹ️ Lanjutkan ke menu **Visualisasi** dan **Evaluasi** untuk analisis lanjut.")
