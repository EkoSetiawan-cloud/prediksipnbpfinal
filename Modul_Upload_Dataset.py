import streamlit as st
import pandas as pd

def upload_dataset_page():
    st.markdown("""
        <h1 style="color:#3C8DBC;">📂 Upload Dataset PNBP</h1>
        <p style="font-size:16px; color:gray;">
            Silakan upload file Excel (<code>.xlsx</code>) yang berisi <strong>data historis PNBP tahun 2014–2024</strong>. 
            Dataset ini akan digunakan untuk proses <em>preprocessing, prediksi, evaluasi</em>, dan <em>visualisasi</em>.
        </p>
        <ul style="font-size:15px; color:#555;">
            <li>Pastikan data memiliki format yang rapi dan konsisten</li>
            <li>Nama sheet default akan digunakan (bila ada beberapa sheet)</li>
            <li>Ukuran file maksimal: 10MB</li>
        </ul>
        <hr style="margin-top:20px; margin-bottom:20px;">
    """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader("📁 Pilih file Excel", type=["xlsx"])

    if uploaded_file is not None:
        try:
            df = pd.read_excel(uploaded_file)
            st.success("✅ File berhasil diunggah!")
            st.markdown("📄 **Pratinjau Data Awal:**")
            st.dataframe(df, use_container_width=True)

            st.info("💡 Data sudah tersimpan dan siap digunakan di modul selanjutnya.")
            st.session_state["dataset_pnbp"] = df

        except Exception as e:
            st.error(f"❌ Terjadi kesalahan saat membaca file: **{e}**")
    else:
        st.info("⬆️ Silakan unggah file untuk memulai analisis.")

