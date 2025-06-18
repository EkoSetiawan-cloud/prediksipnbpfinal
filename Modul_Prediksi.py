import streamlit as st
import pandas as pd
from statsmodels.tsa.holtwinters import ExponentialSmoothing

def prediksi_holt_winters_page():
    st.title("📈 Prediksi PNBP Holt-Winters")

    if "pnbp_total_tahunan" not in st.session_state:
        st.warning("⚠️ Data agregasi belum tersedia. Jalankan preprocessing terlebih dahulu.")
        return

    # Ambil dan siapkan data
    df = st.session_state["pnbp_total_tahunan"].copy()
    df.columns = df.columns.str.strip().str.lower()
    df = df.sort_values("tahun")
    df["total_pnbp"] = pd.to_numeric(df["total_pnbp"], errors="coerce")

    tahun_min = df["tahun"].min()
    tahun_max = df["tahun"].max()
    tahun_forecast = 3

    series = df.set_index("tahun")["total_pnbp"]

    # Fit model
    model = ExponentialSmoothing(series, trend="add", seasonal=None, initialization_method="estimated")
    model_fit = model.fit()

    # Ambil fitted dan forecast
    fitted = model_fit.fittedvalues
    fitted.index = series.index
    forecast = model_fit.forecast(tahun_forecast)
    forecast.index = range(tahun_max + 1, tahun_max + tahun_forecast + 1)

    # Gabungkan prediksi penuh
    df_pred = pd.concat([fitted, forecast])
    df_pred = df_pred.reset_index()
    df_pred.columns = ["Tahun", "Prediksi"]

    # Gabungkan dengan aktual
    df_aktual = df.rename(columns={"tahun": "Tahun", "total_pnbp": "Aktual"})
    df_final = pd.merge(df_pred, df_aktual[["Tahun", "Aktual"]], on="Tahun", how="left")
    df_final["Jenis Tahun"] = df_final["Aktual"].apply(lambda x: "Historis" if pd.notnull(x) else "Prediksi")

    # Simpan data mentah ke session_state
    st.session_state["prediksi_pnbp"] = df_final.copy()

    # Format tampilan ke Rupiah
    def format_rupiah(x):
        return f"Rp {x:,.0f}".replace(",", ".") if pd.notnull(x) else "-"

    df_display = df_final.copy()
    df_display["Aktual"] = df_display["Aktual"].apply(format_rupiah)
    df_display["Prediksi"] = df_display["Prediksi"].apply(format_rupiah)

    # Tampilkan hasil
    st.subheader("📄 Tabel Prediksi vs Aktual (dalam Rupiah)")
    st.dataframe(df_display, use_container_width=True)
