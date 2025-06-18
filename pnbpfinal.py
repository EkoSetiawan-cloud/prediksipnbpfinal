import streamlit as st

# Impor semua modul halaman dengan nama file sesuai
from Modul_Upload_Dataset import upload_dataset_page
from modul_preprocessing_agregasi import preprocessing_agregasi_page
from Modul_Prediksi import prediksi_holt_winters_page
from Modul_Visualisasi import visualisasi_prediksi_page
from Modul_Evaluasi import prediksi_holt_winters_page

# Konfigurasi halaman Streamlit
st.set_page_config(page_title="Prediksi PNBP", layout="centered")

st.markdown("<h2 style='text-align: center;'>📊 Navigasi Aplikasi</h2>", unsafe_allow_html=True)

menu = st.radio(
    "Pilih Modul:",
    [
        "1. Modul Input",
        "2. Preprocessing & Agregasi",
        "3. Prediksi Double Smoothing",
        "4. Visualisasi",
        "5. Evaluasi",
        "6. Export & Report Generator"
    ],
    index=0
)

# Routing ke modul
if menu == "1. Modul Input":
    from Modul_Upload_Dataset import upload_dataset_page
    upload_dataset_page()
elif menu == "2. Preprocessing & Agregasi":
    from modul_preprocessing_agregasi import preprocessing_agregasi_page
    preprocessing_agregasi_page()
elif menu == "3. Prediksi Holt-Winters":
    from Modul_Prediksi import prediksi_holt_winters_page
    prediksi_holt_winters_page()
elif menu == "4. Visualisasi":
    from Modul_Visualisasi import visualisasi_prediksi_page
    visualisasi_prediksi_page()
elif menu == "5. Evaluasi":
    from Modul_Evaluasi import evaluasi_model_page
    evaluasi_model_page()
elif menu == "6. Export & Report Generator":
    from Modul_Export import export_report_page
    export_report_page()
