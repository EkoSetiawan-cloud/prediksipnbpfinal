import streamlit as st
import pandas as pd
import io
import os
import zipfile
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import matplotlib.font_manager as fm
import tempfile


def convert_df_to_excel(df_dict):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        for sheet_name, df in df_dict.items():
            df.to_excel(writer, index=False, sheet_name=sheet_name[:31])
    return output.getvalue()

def export_report_page():
    st.title("📥 Export & Report Generator")

    if not all(key in st.session_state for key in ["dataset_pnbp", "pnbp_total_tahunan", "prediksi_pnbp"]):
        st.warning("⚠️ Dataset belum lengkap. Jalankan semua modul terlebih dahulu.")
        return

    df_asli = st.session_state["dataset_pnbp"]
    df_transpose = st.session_state.get("transposed_data")
    df_agregasi = st.session_state["pnbp_total_tahunan"]
    df_prediksi = st.session_state["prediksi_pnbp"]
    df_evaluasi = st.session_state.get("evaluasi_model", df_prediksi.copy())

    st.subheader("📅 Unduh Semua Tabel dalam Excel (.xlsx)")
    st.markdown("""
    File Excel akan berisi enam sheet:
    1. 📄 Dataset Asli (Tampilan Awal)
    2. 🔁 Data Setelah Transpose
    3. 📊 Agregasi Total PNBP per Tahun
    4. 📄 Hasil Prediksi
    5. 📄 Tabel Evaluasi Error per Tahun
    6. 📊 Tabel Evaluasi Performa Model
    """)

    df_dict = {
        "Dataset Asli": df_asli,
        "Data Setelah Transpose": df_transpose if df_transpose is not None else pd.DataFrame(),
        "Agregasi PNBP per Tahun": df_agregasi,
        "Hasil Prediksi": df_prediksi,
        "Tabel Evaluasi Error": df_evaluasi[["Tahun", "Aktual", "Prediksi", "Error Absolut", "Error Persentase (%)"]] if "Error Absolut" in df_evaluasi.columns else df_evaluasi,
        "Tabel Evaluasi Performa": df_evaluasi[["Tahun", "Aktual", "Prediksi", "MAE", "MAPE", "RMSE", "Validasi"]] if "Validasi" in df_evaluasi.columns else df_evaluasi
    }

    excel_data = convert_df_to_excel(df_dict)

    st.download_button(
        label="⬇️ Download Semua Tabel (.xlsx)",
        data=excel_data,
        file_name="Laporan_Prediksi_PNBP.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    st.markdown("---")
    st.subheader("📈 Grafik Prediksi Double Smoothing (Interaktif)")
    st.markdown("🖼️ Unduh Grafik Prediksi dalam format PNG, PDF, atau SVG.")

    images = export_graphs_as_images(df_prediksi)

    for fmt, buf in images.items():
        st.download_button(
            label=f"⬇️ Download Grafik ({fmt.upper()})",
            data=buf,
            file_name=f"Grafik_Prediksi_PNBP.{fmt}",
            mime=f"image/{'svg+xml' if fmt=='svg' else fmt}"
        )

    st.markdown("---")
    st.subheader("📦 Unduh Semua File Sekaligus (ZIP)")

    zip_data = generate_zip_file(excel_data, images)

    st.download_button(
        label="⬇️ Export ZIP Semua File",
        data=zip_data,
        file_name="Semua_Laporan_PNBP.zip",
        mime="application/zip"
    )
