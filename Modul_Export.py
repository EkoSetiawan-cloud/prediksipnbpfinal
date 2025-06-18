import streamlit as st
import pandas as pd
import io
import os
import zipfile
import matplotlib.pyplot as plt
import streamlit.components.v1 as components
import tempfile

def convert_df_to_excel(df_dict):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        for sheet_name, df in df_dict.items():
            df.to_excel(writer, index=False, sheet_name=sheet_name[:31])
    return output.getvalue()

def generate_html_report(df_pred, df_eval):
    html = """
    <html><head><style>
    body {{ font-family: Arial; margin: 40px; color: #000; }}
    h1, h2 {{ text-align: center; }}
    table {{ border-collapse: collapse; width: 100%; margin-bottom: 40px; }}
    th, td {{ border: 1px solid #000; padding: 8px; text-align: center; }}
    th {{ background-color: #f2f2f2; }}
    </style></head><body>
    <h1>Laporan Prediksi PNBP</h1>
    <h2>Data Prediksi</h2>
    {table1}
    <h2>Evaluasi Model</h2>
    {table2}
    </body></html>
    """
    t1 = df_pred.to_html(index=False, border=1)
    t2 = df_eval.to_html(index=False, border=1)
    return html.format(table1=t1, table2=t2)

def export_graphs_as_images(df_pred):
    output_files = {}
    df_pred = df_pred.copy()
    df_pred = df_pred.sort_values("Tahun")

    # Parsing nominal dari "Rp"
    df_pred["Aktual"] = pd.to_numeric(df_pred["Aktual"].astype(str).str.replace("Rp", "").str.replace(".", "").str.replace(",", "."), errors="coerce")
    df_pred["Prediksi"] = pd.to_numeric(df_pred["Prediksi"].astype(str).str.replace("Rp", "").str.replace(".", "").str.replace(",", "."), errors="coerce")

    fig, ax = plt.subplots(figsize=(10, 5))
    hist = df_pred[df_pred["Jenis Tahun"] == "Historis"]
    pred = df_pred[df_pred["Jenis Tahun"] == "Prediksi"]

    ax.plot(hist["Tahun"], hist["Aktual"], marker="o", label="Aktual", linewidth=2)
    ax.plot(hist["Tahun"], hist["Prediksi"], marker="o", linestyle="--", label="Prediksi (Historis)", linewidth=2)
    ax.plot(pred["Tahun"], pred["Prediksi"], marker="s", linestyle="--", label="Prediksi (Masa Depan)", linewidth=2)

    ax.set_title("Grafik Prediksi PNBP")
    ax.set_xlabel("Tahun")
    ax.set_ylabel("Nominal PNBP")
    ax.grid(True)
    ax.legend()

    for fmt in ["png", "pdf", "svg"]:
        buf = io.BytesIO()
        fig.savefig(buf, format=fmt)
        buf.seek(0)
        output_files[fmt] = buf

    plt.close(fig)
    return output_files

def generate_zip_file(excel_data, images, html_report):
    with tempfile.TemporaryDirectory() as tmpdir:
        # Simpan Excel
        excel_path = os.path.join(tmpdir, "Prediksi_PNBP_Report.xlsx")
        with open(excel_path, "wb") as f:
            f.write(excel_data)

        # Simpan Grafik
        for fmt, buf in images.items():
            img_path = os.path.join(tmpdir, f"Grafik_Prediksi_PNBP.{fmt}")
            with open(img_path, "wb") as f:
                f.write(buf.read())

        # Simpan HTML
        html_path = os.path.join(tmpdir, "Laporan_PNBP.html")
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html_report)

        # Buat file ZIP
        zip_path = os.path.join(tmpdir, "Semua_Laporan_PNBP.zip")
        with zipfile.ZipFile(zip_path, "w") as zipf:
            zipf.write(excel_path, arcname="Prediksi_PNBP_Report.xlsx")
            zipf.write(html_path, arcname="Laporan_PNBP.html")
            for fmt in images:
                zipf.write(os.path.join(tmpdir, f"Grafik_Prediksi_PNBP.{fmt}"),
                           arcname=f"Grafik_Prediksi_PNBP.{fmt}")

        with open(zip_path, "rb") as f:
            return f.read()

def export_report_page():
    st.title("📦 Export & Report Generator")

    if "pnbp_total_tahunan" not in st.session_state or "prediksi_pnbp" not in st.session_state:
        st.warning("⚠️ Dataset belum lengkap. Jalankan semua modul terlebih dahulu.")
        return

    df_agregasi = st.session_state["pnbp_total_tahunan"]
    df_prediksi = st.session_state["prediksi_pnbp"]
    df_evaluasi = st.session_state.get("evaluasi_model", df_prediksi.copy())

    st.subheader("📥 Unduh Semua Tabel dalam Excel")
    df_dict = {
        "Agregasi PNBP per Tahun": df_agregasi,
        "Prediksi PNBP": df_prediksi,
        "Evaluasi Model": df_evaluasi
    }

    excel_data = convert_df_to_excel(df_dict)

    st.download_button(
        label="⬇️ Download Semua Tabel (.xlsx)",
        data=excel_data,
        file_name="Prediksi_PNBP_Report.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    st.markdown("---")
    st.subheader("🖼️ Unduh Grafik Prediksi (PNG / PDF / SVG)")

    images = export_graphs_as_images(df_prediksi)

    for fmt, buf in images.items():
        st.download_button(
            label=f"⬇️ Download Grafik ({fmt.upper()})",
            data=buf,
            file_name=f"Grafik_Prediksi_PNBP.{fmt}",
            mime=f"image/{'svg+xml' if fmt=='svg' else fmt}"
        )

    st.markdown("---")
    st.subheader("🖨️ Pratinjau & Download Laporan PDF (HTML)")

    html_preview = generate_html_report(df_prediksi, df_evaluasi)

    components.html(html_preview, height=600, scrolling=True)

    st.download_button(
        label="⬇️ Download Laporan (HTML)",
        data=html_preview,
        file_name="Laporan_PNBP.html",
        mime="text/html"
    )

    st.markdown("---")
    st.subheader("📦 Unduh Semua File Sekaligus (ZIP)")

    zip_data = generate_zip_file(excel_data, images, html_preview)

    st.download_button(
        label="⬇️ Export ZIP Semua File",
        data=zip_data,
        file_name="Semua_Laporan_PNBP.zip",
        mime="application/zip"
    )
