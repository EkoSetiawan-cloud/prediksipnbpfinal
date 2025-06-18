import streamlit as st
import pandas as pd
import io
import streamlit.components.v1 as components

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
    <h1>Laporan Prediksi PNBP Holt-Winters</h1>
    <h2>Data Prediksi</h2>
    {table1}
    <h2>Evaluasi Model</h2>
    {table2}
    </body></html>
    """

    t1 = df_pred.to_html(index=False, border=1)
    t2 = df_eval.to_html(index=False, border=1)

    return html.format(table1=t1, table2=t2)

def export_report_page():
    st.title("📦 Export & Report Generator")

    # Validasi data
    if "pnbp_total_tahunan" not in st.session_state or \
       "prediksi_pnbp" not in st.session_state:
        st.warning("⚠️ Dataset belum lengkap. Silakan jalankan semua modul sebelumnya terlebih dahulu.")
        return

    df_agregasi = st.session_state["pnbp_total_tahunan"]
    df_prediksi = st.session_state["prediksi_pnbp"]
    df_evaluasi = st.session_state.get("evaluasi_model", df_prediksi.copy())  # fallback prediksi

    st.subheader("📥 Unduh Semua Data dalam Excel")

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

    st.subheader("🖨️ Pratinjau Laporan PDF Otomatis")

    html_preview = generate_html_report(df_prediksi, df_evaluasi)

    components.html(html_preview, height=600, scrolling=True)

    st.download_button(
        label="⬇️ Download Laporan PDF (HTML)",
        data=html_preview,
        file_name="Laporan_PNBP.html",
        mime="text/html"
    )
