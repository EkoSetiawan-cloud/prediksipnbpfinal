import streamlit as st
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
import numpy as np


def prediksi_pnbp_page():
    st.title("📈 Prediksi PNBP dengan ARIMA Rolling Forecast")

    if "pnbp_total_tahunan" not in st.session_state:
        st.warning("Silakan jalankan modul preprocessing terlebih dahulu.")
        return

    df = st.session_state.pnbp_total_tahunan.copy()
    df = df.sort_values("Tahun")
    df = df.reset_index(drop=True)

    st.markdown("""
    ### 🧠 Alasan Pemilihan ARIMA Rolling Forecast
    ARIMA efektif untuk menangkap pola tren historis dengan pendekatan diferensiasi. Dengan rolling forecast, model diperbarui secara berkelanjutan.
    """)

    # Parameter ARIMA
    order = (1, 1, 1)
    horizon = 2

    # Rolling Forecast
    predictions = []
    years = df["Tahun"].tolist()
    values = df["Total PNBP"].tolist()

    for i in range(horizon):
        model = ARIMA(values, order=order)
        model_fit = model.fit()
        forecast = model_fit.forecast()[0]
        predictions.append(forecast)
        values.append(forecast)
        years.append(years[-1] + 1)

    # Buat DataFrame hasil
    df_future = pd.DataFrame({
        "Tahun": years[-horizon:],
        "Prediksi": predictions,
        "Aktual": [np.nan]*horizon,
        "Jenis Tahun": ["Prediksi"]*horizon
    })

    df_hist = df.copy()
    df_hist = df_hist.rename(columns={"Total PNBP": "Aktual"})
    df_hist["Prediksi"] = np.nan
    df_hist["Jenis Tahun"] = "Historis"

    df_prediksi = pd.concat([df_hist, df_future], ignore_index=True)
    df_prediksi["Tahun"] = df_prediksi["Tahun"].astype(int)

    st.success("✅ Prediksi berhasil dilakukan dengan ARIMA Rolling Forecast.")

    st.subheader("📄 Hasil Prediksi")
    st.dataframe(df_prediksi)

    st.session_state.prediksi_pnbp = df_prediksi
    st.info("📤 Lanjutkan ke menu Visualisasi untuk melihat grafik interaktif hasil prediksi.")
