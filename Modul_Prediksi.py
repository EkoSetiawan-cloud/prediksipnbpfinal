import streamlit as st
import pandas as pd
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from prophet import Prophet
import numpy as np

def prediksi_pnbp_page():
    st.title("📈 Prediksi PNBP dengan Berbagai Model")

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

    model_choice = st.selectbox("🧠 Pilih Metode Prediksi:", ["Double-Smoothing", "Prophet"])
    st.session_state["model_choice"] = model_choice

    if model_choice == "Double-Smoothing":
        series = df.set_index("tahun")["total_pnbp"]
        model = ExponentialSmoothing(series, trend="add", seasonal=None, initialization_method="estimated")
        model_fit = model.fit()
        fitted = model_fit.fittedvalues
        forecast = model_fit.forecast(tahun_forecast)
        fitted.index = series.index
        forecast.index = forecast_years
        df_pred = pd.concat([fitted, forecast]).reset_index()
        df_pred.columns = ["Tahun", "Prediksi"]

    elif model_choice == "Prophet":
        df_prophet = df.rename(columns={"tahun": "ds", "total_pnbp": "y"})
        df_prophet["ds"] = pd.to_datetime(df_prophet["ds"], format="%Y")

        model = Prophet(yearly_seasonality=False, weekly_seasonality=False, daily_seasonality=False)
        model.fit(df_prophet)

        # Hitung range tahun secara manual
        tahun_terakhir = df_prophet["ds"].dt.year.max()
        tahun_target = tahun_terakhir + tahun_forecast
        tahun_semua = list(range(df_prophet["ds"].dt.year.min(), tahun_target + 1))

        future = pd.DataFrame({
            "ds": pd.to_datetime(tahun_semua, format="%Y")
        })

        forecast = model.predict(future)
        df_pred = forecast[["ds", "yhat"]]
        df_pred["Tahun"] = df_pred["ds"].dt.year
        df_pred = df_pred[["Tahun", "yhat"]].rename(columns={"yhat": "Prediksi"})

    # Gabungkan dengan data aktual
    df_aktual = df.rename(columns={"tahun": "Tahun", "total_pnbp": "Aktual"})
    df_final = pd.merge(df_pred, df_aktual[["Tahun", "Aktual"]], on="Tahun", how="left")
    df_final["Jenis Tahun"] = df_final["Aktual"].apply(lambda x: "Historis" if pd.notnull(x) else "Prediksi")

    st.session_state["prediksi_pnbp"] = df_final.copy()

    # Format tampilan ke Rupiah
    def format_rupiah(x):
        return f"Rp {x:,.0f}".replace(",", ".") if pd.notnull(x) else "-"

    df_display = df_final.copy()
    df_display["Aktual"] = df_display["Aktual"].apply(format_rupiah)
    df_display["Prediksi"] = df_display["Prediksi"].apply(format_rupiah)

    st.subheader(f"📄 Hasil Prediksi dengan Model: {model_choice}")
    st.dataframe(df_display, use_container_width=True)
