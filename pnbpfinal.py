import streamlit as st

# Konfigurasi halaman Streamlit – WAJIB paling atas sebelum komponen lain
st.set_page_config(page_title="Prediksi PNBP", layout="wide")

# Impor semua modul halaman
from login import login_page  
from Modul_Upload_Dataset import upload_dataset_page
from modul_preprocessing_agregasi import preprocessing_agregasi_page
from Modul_Prediksi import prediksi_pnbp_page
from Modul_Visualisasi import visualisasi_prediksi_page
from Modul_Evaluasi import evaluasi_model_page
from Modul_Kesimpulan_&_Analisa import kesimpulan_analisa_page
from Modul_Export import export_report_page

# Jalankan Login
if not login_page():
    st.stop()

# Navigasi Aplikasi
st.sidebar.title("📊 Aplikasi Prediksi PNBP DJID")
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
    from Modul_Upload_Dataset import upload_dataset_page
    upload_dataset_page()
elif menu == "2. Preprocessing & Agregasi":
    from modul_preprocessing_agregasi import preprocessing_agregasi_page
    preprocessing_agregasi_page()
elif menu == "3. Prediksi Model":
    from Modul_Prediksi import prediksi_pnbp_page
    prediksi_pnbp_page()
elif menu == "4. Visualisasi":
    from Modul_Visualisasi import visualisasi_prediksi_page
    visualisasi_prediksi_page()
elif menu == "5. Evaluasi":
    from Modul_Evaluasi import evaluasi_model_page
    evaluasi_model_page()
elif menu == "6. Kesimpulan & Analisa":
    from Modul_Kesimpulan_Analisa import kesimpulan_analisa_page
    kesimpulan_analisa_page()
elif menu == "7. Export & Report Generator":
    from Modul_Export import export_report_page
    export_report_page()
