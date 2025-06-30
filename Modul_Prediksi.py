import streamlit as st
import pandas as pd
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from statsmodels.tsa.arima.model import ARIMA
import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error


def prediksi_pnbp_page():
    st.markdown("<h1 style='color:#3C8DBC;'>📈 Model Prediksi PNBP</h1>", unsafe_allow_html=True)

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

    metode = st.selectbox("🧠 Pilih Metode Prediksi", ["Double Smoothing", "ARIMA Rolling Forecast"])

    if metode == "Double Smoothing":
        st.markdown("""
        ### 🧠 Alasan Pemilihan
        Model ini sangat cocok untuk data PNBP karena:
        - Memiliki tren linier tahunan yang konsisten
        - Tidak menunjukkan pola musiman yang kompleks
        - Diperlukan model yang cepat, stabil, dan mudah dijelaskan

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

    else:
        st.markdown("""
        ### 🧠 Alasan Pemilihan ARIMA Rolling Forecast
        ARIMA efektif untuk menangkap pola tren historis dengan pendekatan diferensiasi. Dengan rolling forecast, model diperbarui secara berkelanjutan.
        """)

        train = df.iloc[:-1]["total_pnbp"]
        test = df.iloc[-1:]["total_pnbp"]

        history = list(train)
        predictions = []

        for t in range(len(test)):
            model = ARIMA(history, order=(1, 1, 1))
            model_fit = model.fit()
            yhat = model_fit.forecast()[0]
            predictions.append(yhat)
            history.append(test.iloc[t])

        forecast_index = test.index.tolist()
        df_pred = pd.DataFrame({"Tahun": forecast_index, "Prediksi": predictions})
        st.success("✅ Prediksi berhasil dilakukan dengan ARIMA Rolling Forecast.")

        df_aktual = df.rename(columns={"tahun": "Tahun", "total_pnbp": "Aktual"})
        df_pred = pd.merge(df_pred, df_aktual, on="Tahun", how="left")
        df_pred["Jenis Tahun"] = df_pred["Aktual"].apply(lambda x: "Historis" if pd.notnull(x) else "Prediksi")
        st.session_state["prediksi_pnbp"] = df_pred.copy()
        
        df_display = df_pred.copy()
        df_display["Aktual"] = df_display["Aktual"].apply(lambda x: f"Rp {x:,.0f}".replace(",", ".") if pd.notnull(x) else "-")
        df_display["Prediksi"] = df_display["Prediksi"].apply(lambda x: f"Rp {x:,.0f}".replace(",", ".") if pd.notnull(x) else "-")

        st.subheader("📄 Hasil Prediksi")
        st.caption("Tabel berikut menampilkan nilai aktual dan hasil proyeksi.")
        st.dataframe(df_display, use_container_width=True)
        st.info("ℹ️ Lanjutkan ke menu **Visualisasi** untuk melihat grafik interaktif hasil prediksi.")
        return

    df_aktual = df.rename(columns={"tahun": "Tahun", "total_pnbp": "Aktual"})
    df_final = pd.merge(df_pred, df_aktual[["Tahun", "Aktual"]], on="Tahun", how="left")
    df_final["Jenis Tahun"] = df_final["Aktual"].apply(lambda x: "Historis" if pd.notnull(x) else "Prediksi")
    st.session_state["prediksi_pnbp"] = df_final.copy()

    df_display = df_final.copy()
    df_display["Aktual"] = df_display["Aktual"].apply(lambda x: f"Rp {x:,.0f}".replace(",", ".") if pd.notnull(x) else "-")
    df_display["Prediksi"] = df_display["Prediksi"].apply(lambda x: f"Rp {x:,.0f}".replace(",", ".") if pd.notnull(x) else "-")

    st.subheader("📄 Hasil Prediksi")
    st.caption("Tabel berikut menampilkan nilai aktual dan hasil proyeksi untuk dua tahun ke depan.")
    st.dataframe(df_display, use_container_width=True)

    st.info("ℹ️ Lanjutkan ke menu **Visualisasi** untuk melihat grafik interaktif hasil prediksi.")
