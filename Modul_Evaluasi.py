import streamlit as st 
import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error

def evaluasi_model_page():
    st.title("📏 Evaluasi Model Prediksi Holt-Winters")

    if "prediksi_pnbp" not in st.session_state:
        st.warning("⚠️ Data prediksi belum tersedia. Jalankan Modul Prediksi terlebih dahulu.")
        return

    df_pred = st.session_state["prediksi_pnbp"].copy()
    df_pred.columns = [col.lower().strip() for col in df_pred.columns]

    required = ["tahun", "aktual", "prediksi", "jenis tahun"]
    if not all(col in df_pred.columns for col in required):
        st.error(f"❌ Dataset prediksi tidak lengkap. Harus punya kolom: {required}")
        return

    df_pred["aktual"] = pd.to_numeric(df_pred["aktual"], errors="coerce")
    df_pred["prediksi"] = pd.to_numeric(df_pred["prediksi"], errors="coerce")
    df_pred = df_pred.sort_values("tahun")

    # Hitung error absolut dan persentase
    df_pred["error_absolut"] = np.abs(df_pred["aktual"] - df_pred["prediksi"])
    df_pred["error_persen"] = (df_pred["error_absolut"] / df_pred["aktual"]) * 100

    # Hitung MAE, MAPE, RMSE hanya untuk data yang ada aktualnya
    df_hist = df_pred[df_pred["jenis tahun"] == "Historis"].copy()
    df_hist.dropna(subset=["aktual", "prediksi"], inplace=True)

    mean_aktual = df_hist["aktual"].mean()
    rmse_global = np.sqrt(mean_squared_error(df_hist["aktual"], df_hist["prediksi"]))

    # Tambahkan evaluasi prediksi ke depan
    for idx, row in df_pred.iterrows():
        if pd.isna(row["aktual"]):
            pred = row["prediksi"]
            if not pd.isna(pred):
                mae = np.abs(mean_aktual - pred)
                mape = (mae / mean_aktual) * 100 if mean_aktual != 0 else np.nan
                df_pred.at[idx, "error_absolut"] = mae
                df_pred.at[idx, "error_persen"] = mape

    # Validasi MAPE
    def validate_mape(mape):
        if pd.isna(mape):
            return "-"
        elif mape <= 10:
            return "Sangat Akurat"
        elif mape <= 20:
            return "Akurat"
        elif mape <= 50:
            return "Cukup Akurat"
        else:
            return "Tidak Akurat"

    df_pred["validasi"] = df_pred["error_persen"].apply(validate_mape)

    # Format tampilan
    def format_rupiah(x):
        return f"Rp {x:,.0f}".replace(",", ".") if pd.notnull(x) else "-"

    def format_persen(x):
        return f"{x:.2f}%" if pd.notnull(x) else "-"

    df_tampil = df_pred.copy()
    df_tampil["Aktual"] = df_tampil["aktual"].apply(format_rupiah)
    df_tampil["Prediksi"] = df_tampil["prediksi"].apply(format_rupiah)
    df_tampil["Error Absolut"] = df_tampil["error_absolut"].apply(format_rupiah)
    df_tampil["Error Persentase (%)"] = df_tampil["error_persen"].apply(format_persen)

    # Tampilkan tabel error
    st.subheader("📄 Tabel Evaluasi Error (Aktual vs Prediksi)")
    st.dataframe(df_tampil[["tahun", "Aktual", "Prediksi", "Error Absolut", "Error Persentase (%)"]], use_container_width=True)
    
    # RMSE per baris = sqrt((Aktual - Prediksi)^2)
    df_pred["rmse"] = np.sqrt((df_pred["aktual"] - df_pred["prediksi"]) ** 2)
    df_tampil["RMSE"] = df_pred["rmse"].apply(format_rupiah)


    # Kolom MAE & MAPE (dari error sebelumnya)
    df_tampil["MAE"] = df_pred["error_absolut"].apply(format_rupiah)
    df_tampil["MAPE"] = df_pred["error_persen"].apply(format_persen)

    # Kolom Validasi
    df_tampil["Validasi"] = df_pred["validasi"]

    # Tabel Performa Lengkap
    st.subheader("📊 Tabel Evaluasi Performa Model")
    st.dataframe(df_tampil[[
        "tahun", "Aktual", "Prediksi", "MAE", "MAPE", "RMSE", "Validasi"
    ]], use_container_width=True)
    
    # Tampilkan ringkasan
    st.subheader("📈 Ringkasan Skor Evaluasi Global")
    st.markdown(f"- **MAE**: `{format_rupiah(df_hist['error_absolut'].mean())}`")
    st.markdown(f"- **MAPE**: `{df_hist['error_persen'].mean():.2f}%`")
    st.markdown(f"- **RMSE**: `{format_rupiah(rmse_global)}`")
