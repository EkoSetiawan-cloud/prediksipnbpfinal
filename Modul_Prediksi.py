import pandas as pd
import numpy as np
import streamlit as st
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_absolute_error, mean_squared_error


def rolling_forecast_arima(series, train_size=0.8, forecast_steps=3):
    n = len(series)
    train_end = int(n * train_size)
    predictions = [None] * train_end

    for t in range(train_end, n):
        train = series[:t]
        try:
            model = ARIMA(train, order=(1, 1, 1))
            model_fit = model.fit()
            forecast = model_fit.forecast()[0]
        except:
            forecast = np.nan
        predictions.append(forecast)

    # Forecast future steps
    future_preds = []
    history = series.copy()
    for _ in range(forecast_steps):
        try:
            model = ARIMA(history, order=(1, 1, 1))
            model_fit = model.fit()
            yhat = model_fit.forecast()[0]
        except:
            yhat = np.nan
        future_preds.append(yhat)
        history = np.append(history, yhat)

    return predictions, future_preds


def prediksi_pnbp_page():
    st.title("📈 Prediksi PNBP dengan ARIMA Rolling Forecast")

    if "pnbp_total_tahunan" not in st.session_state:
        st.warning("Silakan jalankan modul Preprocessing & Agregasi terlebih dahulu.")
        return

    df = st.session_state.pnbp_total_tahunan.copy()
    df = df.sort_values("Tahun")
    df["Total PNBP"] = pd.to_numeric(df["Total PNBP"], errors="coerce")
    series = df["Total PNBP"].dropna().values

    pred_hist, pred_future = rolling_forecast_arima(series)

    # Pad future years
    future_years = [df["Tahun"].max() + i for i in range(1, len(pred_future) + 1)]
    df_future = pd.DataFrame({
        "Tahun": future_years,
        "Aktual": [None]*len(pred_future),
        "Prediksi": pred_future,
        "Jenis Tahun": "Prediksi"
    })

    df_prediksi = df.copy()
    df_prediksi["Prediksi"] = pred_hist
    df_prediksi["Aktual"] = df_prediksi["Total PNBP"]
    df_prediksi["Jenis Tahun"] = "Historis"
    df_prediksi = df_prediksi.drop(columns="Total PNBP")

    df_final = pd.concat([df_prediksi, df_future], ignore_index=True)

    st.session_state.prediksi_pnbp = df_final

    st.success("✅ Prediksi berhasil dilakukan dengan ARIMA Rolling Forecast.")

    st.subheader("📄 Hasil Prediksi")
    st.dataframe(df_final)

    st.info("➡️ Lanjutkan ke menu Visualisasi untuk melihat grafik interaktif hasil prediksi.")
