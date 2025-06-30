import streamlit as st 
import pandas as pd
import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error

def evaluasi_model_page():
    st.markdown("<h1 style='color:#3C8DBC;'>📏 Evaluasi Model Prediksi (ARIMA & Lainnya)</h1>", unsafe_allow_html=True)

    st.markdown("""
    Modul ini digunakan untuk mengevaluasi akurasi hasil prediksi model time series (seperti ARIMA, Holt's).
    
    ### Metrik yang dihitung:
    - **MAE**: Mean Absolute Error
    - **MAPE**: Mean Absolute Percentage Error
    - **RMSE**: Root Mean Square Error
    - **Validasi Akurasi**: Sangat Akurat / Akurat / Cukup / Tidak Akurat
    """)

    if "prediksi_pnbp" not in st.session_state:
        st.warning("⚠️ Data prediksi belum tersedia. Jalankan modul prediksi terlebih dahulu.")
        return

    df = st.session_state["prediksi_pnbp"].copy()

    # Konversi ke numerik
    df["Aktual"] = pd.to_numeric(df["Aktual"], errors="coerce")
    df["Prediksi"] = pd.to_numeric(df["Prediksi"], errors="coerce")

    # Buang baris kosong
    df = df.dropna(subset=["Prediksi"])

    # Hitung residual dan error
    df["Error Absolut"] = np.abs(df["Aktual"] - df["Prediksi"])
    df["Error Persentase (%)"] = (df["Error Absolut"] / df["Aktual"]) * 100

    # Validasi klasifikasi MAPE
    def validate_mape(mape):
        if pd.isna(mape): return "-"
        elif mape <= 10: return "Sangat Akurat"
        elif mape <= 20: return "Akurat"
        elif mape <= 50: return "Cukup Akurat"
        else: return "Tidak Akurat"

    df["Validasi"] = df["Error Persentase (%)"].apply(validate_mape)
    df["MAE"] = df["Error Absolut"]
    df["MAPE"] = df["Error Persentase (%)"]
    df["RMSE"] = (df["Aktual"] - df["Prediksi"]) ** 2

    # Format tampilan
    def rupiah(x): return f"Rp {x:,.0f}".replace(",", ".") if pd.notnull(x) else "-"
    def persen(x): return f"{x:.2f}%" if pd.notnull(x) else "-"

    df_tampil = df.copy()
    df_tampil["Aktual"] = df_tampil["Aktual"].apply(rupiah)
    df_tampil["Prediksi"] = df_tampil["Prediksi"].apply(rupiah)
    df_tampil["Error Absolut"] = df_tampil["Error Absolut"].apply(rupiah)
    df_tampil["Error Persentase (%)"] = df_tampil["Error Persentase (%)"].apply(persen)
    df_tampil["MAE"] = df_tampil["MAE"].apply(rupiah)
    df_tampil["MAPE"] = df_tampil["MAPE"].apply(persen)
    df_tampil["RMSE"] = np.sqrt(df["RMSE"]).apply(rupiah)

    st.subheader("📄 Tabel Evaluasi Prediksi")
    st.dataframe(df_tampil[[
        "Tahun", "Aktual", "Prediksi", "Error Absolut", 
        "Error Persentase (%)", "MAE", "MAPE", "RMSE", "Validasi"
    ]], use_container_width=True)

    # Ringkasan Global
    mae_global = mean_absolute_error(df["Aktual"], df["Prediksi"])
    mape_global = df["MAPE"].mean()
    rmse_global = np.sqrt(mean_squared_error(df["Aktual"], df["Prediksi"]))

    st.subheader("📈 Ringkasan Evaluasi Global")
    st.markdown(f"- **MAE**: `{rupiah(mae_global)}`")
    st.markdown(f"- **MAPE**: `{mape_global:.2f}%`")
    st.markdown(f"- **RMSE**: `{rupiah(rmse_global)}`")

    st.info("ℹ️ Kategori Validasi: ≤10% Sangat Akurat, ≤20% Akurat, ≤50% Cukup, >50% Tidak Akurat")
