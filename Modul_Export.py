import streamlit as st
import pandas as pd
import io
import os
import zipfile
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import tempfile


def convert_df_to_excel(df_dict):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        for sheet_name, df in df_dict.items():
            df.to_excel(writer, index=False, sheet_name=sheet_name[:31])
    return output.getvalue()

def export_graphs_as_images(df_pred):
    output_files = {}
    df_pred = df_pred.copy()
    df_pred = df_pred.sort_values("Tahun")

    df_pred["Aktual"] = pd.to_numeric(df_pred["Aktual"].astype(str).str.replace("Rp", "").str.replace(".", "").str.replace(",", "."), errors="coerce")
    df_pred["Prediksi"] = pd.to_numeric(df_pred["Prediksi"].astype(str).str.replace("Rp", "").str.replace(".", "").str.replace(",", "."), errors="coerce")

    fig, ax = plt.subplots(figsize=(10, 5))
    hist = df_pred[df_pred["Jenis Tahun"] == "Historis"]
    pred = df_pred[df_pred["Jenis Tahun"] == "Prediksi"]

    scale = 1e12  # Triliun
    ax.plot(hist["Tahun"], hist["Aktual"] / scale, color="blue", marker="o", label="Aktual (Histori)", linewidth=2)
    ax.plot(df_pred["Tahun"], df_pred["Prediksi"] / scale, color="orange", linestyle="--", marker="o", label="Prediksi (Double Smoothing)", linewidth=2)

    ax.set_title("Prediksi Total PNBP vs Data Aktual (Double Smoothing)")
    ax.set_xlabel("Tahun")
    ax.set_ylabel("Nominal PNBP (Rp Triliun)")
    ax.grid(True)
    ax.legend()
    ax.yaxis.set_major_formatter(mtick.FormatStrFormatter('%.0f T'))

    for fmt in ["png", "pdf", "svg"]:
        buf = io.BytesIO()
        fig.savefig(buf, format=fmt, dpi=300)
        buf.seek(0)
        output_files[fmt] = buf

    plt.close(fig)
    return output_files

def generate_zip_file(excel_data, images):
    with tempfile.TemporaryDirectory() as tmpdir:
        excel_path = os.path.join(tmpdir, "Laporan_Prediksi_PNBP.xlsx")
        with open(excel_path, "wb") as f:
            f.write(excel_data)

        for fmt, buf in images.items():
            img_path = os.path.join(tmpdir, f"Grafik_Prediksi_PNBP.{fmt}")
            with open(img_path, "wb") as f:
                f.write(buf.read())

        zip_path = os.path.join(tmpdir, "Semua_Laporan_PNBP.zip")
        with zipfile.ZipFile(zip_path, "w") as zipf:
            zipf.write(excel_path, arcname="Laporan_Prediksi_PNBP.xlsx")
            for fmt in images:
                zipf.write(os.path.join(tmpdir, f"Grafik_Prediksi_PNBP.{fmt}"),
                           arcname=f"Grafik_Prediksi_PNBP.{fmt}")

        with open(zip_path, "rb") as f:
            return f.read()

def export_report_page():
    st.title("\U0001F4E5 Export & Report Generator")

    if not all(key in st.session_state for key in ["dataset_pnbp", "pnbp_total_tahunan", "prediksi_pnbp"]):
        st.warning("⚠️ Dataset belum lengkap. Jalankan semua modul terlebih dahulu.")
        return

    df_asli = st.session_state["dataset_pnbp"]
    df_transpose = st.session_state.get("transposed_data")
    df_agregasi = st.session_state["pnbp_total_tahunan"]
    df_prediksi = st.session_state["prediksi_pnbp"]
    df_evaluasi = st.session_state.get("evaluasi_model", df_prediksi.copy())

    st.subheader("\U0001F4C5 Unduh Semua Tabel dalam Excel (.xlsx)")
    st.markdown("""
    File Excel akan berisi enam sheet:
    1. \U0001F4C4 Dataset Asli (Tampilan Awal)
    2. \U0001F501 Data Setelah Transpose
    3. \U0001F4CA Agregasi Total PNBP per Tahun
    4. \U0001F4C4 Hasil Prediksi
    5. \U0001F4C4 Tabel Evaluasi Error per Tahun
    6. \U0001F4CA Tabel Evaluasi Performa Model
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
