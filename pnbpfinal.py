import streamlit as st

# Konfigurasi halaman Streamlit – WAJIB paling atas sebelum komponen lain
st.set_page_config(page_title="Prediksi PNBP", layout="wide")

# Impor semua modul halaman
from login import login_page  
from Modul_Upload_Dataset import upload_dataset_page
from modul_preprocessing_agregasi import preprocessing_agregasi_page
from Modul_Prediksi_ARIMA_FINAL import prediksi_pnbp_page
from Modul_Visualisasi import visualisasi_prediksi_page
from Modul_Evaluasi import evaluasi_model_page
from modul_analisa_final import kesimpulan_analisa_page
from Modul_Export import export_report_page

# Jalankan Login
if not login_page():
    st.stop()

# Navigasi Aplikasi
st.sidebar.markdown("<h1 style='color:#800080;'>📊 Aplikasi Prediksi PNBP DJID</h1>", unsafe_allow_html=True)
menu = st.sidebar.radio("Pilih Modul", [
        "1. Modul Input",
        "2. Preprocessing & Agregasi",
        "3. Prediksi Model",
        "4. Visualisasi",
        "5. Evaluasi",
        "6. Kesimpulan & Analisa",
        "7. Export & Report Generator"
    ],
    index=0
)

# Routing ke modul
if menu == "1. Modul Input":
    upload_dataset_page()
elif menu == "2. Preprocessing & Agregasi":
    preprocessing_agregasi_page()
elif menu == "3. Prediksi Model":
    prediksi_pnbp_page()
elif menu == "4. Visualisasi":
    visualisasi_prediksi_page()
elif menu == "5. Evaluasi":
    evaluasi_model_page()
elif menu == "6. Kesimpulan & Analisa":
    kesimpulan_analisa_page()
elif menu == "7. Export & Report Generator":
    export_report_page()
