import streamlit as st 
import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error

def evaluasi_model_page():
    st.markdown("<h1 style='color:#3C8DBC;'>📏 Evaluasi Model Prediksi - Double Smoothing</h1>", unsafe_allow_html=True)

    st.markdown("""
    Modul ini digunakan untuk mengevaluasi akurasi hasil prediksi model **Double Exponential Smoothing** dibandingkan dengan data aktual. 

    Evaluasi dilakukan menggunakan metrik berikut:
    - **MAE (Mean Absolute Error)**: rata-rata selisih absolut antara prediksi dan aktual.
    - **MAPE (Mean Absolute Percentage Error)**: error relatif dalam persentase.
    - **RMSE (Root Mean Square Error)**: akar dari rata-rata kuadrat error, sensitif terhadap outlier.

    Setiap baris data dievaluasi, dan hasil ringkasan global disediakan di bagian akhir.
    """)

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

    # Error absolut & persen
    df_pred["error_absolut"] = np.abs(df_pred["aktual"] - df_pred["prediksi"])
    df_pred["error_persen"] = (df_pred["error_absolut"] / df_pred["aktual"]) * 100

    # Hanya historis untuk evaluasi global
    df_hist = df_pred[df_pred["jenis tahun"] == "Historis"].copy()
    df_hist.dropna(subset=["aktual", "prediksi"], inplace=True)

    mean_aktual = df_hist["aktual"].mean()
    rmse_global = np.sqrt(mean_squared_error(df_hist["aktual"], df_hist["prediksi"]))

    # Hitung juga untuk prediksi masa depan
    for idx, row in df_pred.iterrows():
        if pd.isna(row["aktual"]):
            pred = row["prediksi"]
            if not pd.isna(pred):
                mae = np.abs(mean_aktual - pred)
                mape = (mae / mean_aktual) * 100 if mean_aktual != 0 else np.nan
                df_pred.at[idx, "error_absolut"] = mae
                df_pred.at[idx, "error_persen"] = mape

    # Validasi
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

    # Format
    def format_rupiah(x):
        return f"Rp {x:,.0f}".replace(",", ".") if pd.notnull(x) else "-"

    def format_persen(x):
        return f"{x:.2f}%" if pd.notnull(x) else "-"

    df_tampil = df_pred.copy()
    df_tampil["Aktual"] = df_tampil["aktual"].apply(format_rupiah)
    df_tampil["Prediksi"] = df_tampil["prediksi"].apply(format_rupiah)
    df_tampil["Error Absolut"] = df_tampil["error_absolut"].apply(format_rupiah)
    df_tampil["Error Persentase (%)"] = df_tampil["error_persen"].apply(format_persen)

    df_pred["rmse"] = np.sqrt((df_pred["aktual"] - df_pred["prediksi"]) ** 2)
    df_tampil["RMSE"] = df_pred["rmse"].apply(format_rupiah)
    df_tampil["MAE"] = df_pred["error_absolut"].apply(format_rupiah)
    df_tampil["MAPE"] = df_pred["error_persen"].apply(format_persen)
    df_tampil["Validasi"] = df_pred["validasi"]

    st.subheader("📄 Tabel Evaluasi Error per Tahun")
    st.caption("Menampilkan error absolut dan persentase antara prediksi dan data aktual.")
    st.dataframe(df_tampil[["tahun", "Aktual", "Prediksi", "Error Absolut", "Error Persentase (%)"]], use_container_width=True)

    st.subheader("📊 Tabel Evaluasi Performa Model")
    st.caption("Tabel ini menunjukkan performa model prediksi dalam bentuk MAE, MAPE, RMSE, dan validasi akurasi.")
    st.dataframe(df_tampil[["tahun", "Aktual", "Prediksi", "MAE", "MAPE", "RMSE", "Validasi"]], use_container_width=True)

    st.subheader("📈 Ringkasan Skor Evaluasi Global")
    st.markdown(f"- **Model**: `Double Smoothing`")
    st.markdown(f"- **MAE**: `{format_rupiah(df_hist['error_absolut'].mean())}`")
    st.markdown(f"- **MAPE**: `{df_hist['error_persen'].mean():.2f}%`")
    st.markdown(f"- **RMSE**: `{format_rupiah(rmse_global)}`")

    st.info("ℹ️ Validasi model berdasarkan MAPE: ≤10% = Sangat Akurat, ≤20% = Akurat, ≤50% = Cukup Akurat, >50% = Tidak Akurat.")
