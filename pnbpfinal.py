import streamlit as st

# Impor semua modul halaman dengan nama file sesuai
from Modul_Upload_Dataset import upload_dataset_page
from modul_preprocessing_agregasi import preprocessing_agregasi_page
from Modul_Prediksi import prediksi_holt_winters_page
from Modul_Visualisasi import visualisasi_prediksi_page
from Modul_Evaluasi import evaluasi_model_page

# Konfigurasi halaman Streamlit
st.set_page_config(page_title="Prediksi PNBP", layout="wide")

# Sidebar navigasi
st.sidebar.title("📊 Navigasi Aplikasi")
menu = st.sidebar.radio("Pilih Modul", [
    "1. Modul Input",
    "2. Preprocessing & Agregasi",
    "3. Prediksi Holt-Winters",
    "4. Visualisasi",
    "5. Evaluasi"
])

# Routing modul
if menu == "1. Modul Input":
    upload_dataset_page()
elif menu == "2. Preprocessing & Agregasi":
    preprocessing_agregasi_page()
elif menu == "3. Prediksi Holt-Winters":
    prediksi_holt_winters_page()
elif menu == "4. Visualisasi":
    visualisasi_prediksi_page()
elif menu == "5. Evaluasi":
    evaluasi_model_page()
