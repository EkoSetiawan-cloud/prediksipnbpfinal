import streamlit as st
import pandas as pd
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from prophet import Prophet
import numpy as np

def prediksi_pnbp_page():
    st.title("\U0001F4C8 Prediksi Total PNBP Tahunan")

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

    st.subheader("\U0001F9E0 Pilih Metode Prediksi")
    model_choice = st.selectbox(
        "Model yang akan digunakan untuk prediksi:",
        ["Double-Smoothing", "Prophet"],
        help="Double Smoothing untuk tren linier, Prophet untuk tren non-linier dan musiman."
    )
    st.session_state["model_choice"] = model_choice

    with st.expander("\U0001F4D8 Penjelasan Metode Prediksi", expanded=True):
        if model_choice == "Double-Smoothing":
            st.markdown("""
            **🔹 Double Exponential Smoothing (Holt’s Method)**  
            Model ini memprediksi data dengan tren linier. Digunakan dua komponen: _level_ dan _trend_, dengan rumus:
            
            $$
            \begin{aligned}
            L_t &= \alpha y_t + (1 - \alpha)(L_{t-1} + T_{t-1}) \\
            T_t &= \beta (L_t - L_{t-1}) + (1 - \beta) T_{t-1} \\
            \hat{y}_{t+m} &= L_t + m \cdot T_t
            \end{aligned}
            $$
            - Cocok untuk data tren jangka pendek.
            - Tidak menangani musiman.
            """)
        else:
            st.markdown("""
            **🔹 Prophet (Facebook)**  
            Model decomposable time series:
            
            $$ y(t) = g(t) + s(t) + h(t) + \varepsilon_t $$
            - \(g(t)\): tren non-linier
            - \(s(t)\): musiman tahunan/mingguan
            - \(h(t)\): liburan/spesial event
            - \(\varepsilon_t\): noise/residual
            
            Prophet cocok untuk data musiman, outlier, dan tren berubah.
            """)

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
        st.success("✅ Prediksi berhasil dilakukan dengan Double Smoothing.")

    elif model_choice == "Prophet":
        df_prophet = df.rename(columns={"tahun": "ds", "total_pnbp": "y"})
        df_prophet["ds"] = pd.to_datetime(df_prophet["ds"], format="%Y")

        model = Prophet(yearly_seasonality=False, weekly_seasonality=False, daily_seasonality=False)
        model.fit(df_prophet)

        tahun_target = df_prophet["ds"].dt.year.max() + tahun_forecast
        tahun_semua = list(range(df_prophet["ds"].dt.year.min(), tahun_target + 1))
        future = pd.DataFrame({"ds": pd.to_datetime(tahun_semua, format="%Y")})
        forecast = model.predict(future)
        df_pred = forecast[["ds", "yhat"]]
        df_pred["Tahun"] = df_pred["ds"].dt.year
        df_pred = df_pred[["Tahun", "yhat"]].rename(columns={"yhat": "Prediksi"})
        st.success("✅ Prediksi berhasil dilakukan dengan model Prophet.")

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
