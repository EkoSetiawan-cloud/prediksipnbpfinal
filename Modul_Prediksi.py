import pandas as pd
import streamlit as st
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_absolute_error, mean_squared_error
import numpy as np


def prediksi_pnbp_page():
    st.title("📈 Prediksi PNBP dengan ARIMA Rolling Forecast")

    if "pnbp_total_tahunan" not in st.session_state:
        st.warning("Silakan jalankan modul preprocessing terlebih dahulu.")
        return

    df = st.session_state.pnbp_total_tahunan.copy()
    df = df.sort_values("Tahun")

    st.subheader("🧠 Alasan Pemilihan ARIMA Rolling Forecast")
    st.markdown("""
    ARIMA efektif untuk menangkap pola tren historis dengan pendekatan diferensiasi. Dengan rolling forecast, model diperbarui secara berkelanjutan.
    """)

    # Parameter
    forecast_horizon = 2  # Tahun yang ingin diprediksi
    train = df.copy()
    train['Prediksi'] = np.nan

    for i in range(len(train) - forecast_horizon):
        train_data = train.iloc[:i + forecast_horizon]['Total PNBP']
        model = ARIMA(train_data, order=(1, 1, 1))
        model_fit = model.fit()
        pred = model_fit.forecast()[0]
        train.loc[i + forecast_horizon, 'Prediksi'] = pred

    # Simpan hasil prediksi historis
    df_prediksi = train.copy()
    df_prediksi['Aktual'] = df_prediksi['Total PNBP']
    df_prediksi = df_prediksi[['Tahun', 'Aktual', 'Prediksi']]

    # Prediksi masa depan (1 langkah ke depan)
    future_year = df_prediksi['Tahun'].max() + 1
    model = ARIMA(df['Total PNBP'], order=(1, 1, 1))
    model_fit = model.fit()
    future_pred = model_fit.forecast()[0]
    df_future = pd.DataFrame({
        'Tahun': [future_year],
        'Aktual': [None],
        'Prediksi': [future_pred]
    })

    df_prediksi = pd.concat([df_prediksi, df_future], ignore_index=True)
    df_prediksi['Jenis Tahun'] = df_prediksi['Aktual'].apply(lambda x: "Historis" if pd.notnull(x) else "Prediksi")

    st.success("✅ Prediksi berhasil dilakukan dengan ARIMA Rolling Forecast.")

    st.subheader("📄 Hasil Prediksi")
    st.write("Tabel berikut menampilkan nilai aktual dan hasil proyeksi.")
    st.dataframe(df_prediksi)

    # Simpan ke session state
    st.session_state.prediksi_pnbp = df_prediksi

    st.info("➡️ Lanjutkan ke menu Visualisasi untuk melihat grafik interaktif hasil prediksi.")
