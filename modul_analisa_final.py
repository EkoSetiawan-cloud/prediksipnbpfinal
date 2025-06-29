import streamlit as st

def kesimpulan_analisa_page():
    st.title("📋 Kesimpulan & Analisa Prediksi PNBP")

    st.markdown("### 🎯 Tujuan Analisis")
    st.write(\"\"\"
    Evaluasi model prediksi bertujuan untuk:
    - Menilai seberapa dekat nilai prediksi terhadap nilai aktual
    - Menentukan tingkat akurasi dan konsistensi model secara kuantitatif
    - Memberikan dasar argumentatif dalam pengambilan keputusan prediktif berbasis data
    \"\"\")

    st.markdown("### 📈 Hasil Evaluasi Model")
    st.write(\"\"\"
    Berdasarkan hasil perhitungan menggunakan tiga metrik utama:

    - MAE (Mean Absolute Error): rata-rata selisih absolut antara nilai aktual dan prediksi.
    - MAPE (Mean Absolute Percentage Error): error relatif dalam bentuk persentase. MAPE < 10% sangat akurat.
    - RMSE (Root Mean Square Error): cocok untuk mengukur konsistensi model terhadap fluktuasi.

    Validasi berdasarkan MAPE:
    - ≤ 10% = Sangat Akurat
    - ≤ 20% = Akurat
    - ≤ 50% = Cukup Akurat
    - > 50% = Tidak Akurat
    \"\"\")

    st.markdown("### 📊 Interpretasi Akademik")
    st.write(\"\"\"
    Hasil evaluasi menunjukkan model Double Exponential Smoothing mampu memetakan tren linier historis.
    MAE dan RMSE yang rendah mengindikasikan kestabilan model.
    MAPE yang kecil memperlihatkan bahwa model menjaga kesalahan relatif yang kecil terhadap data aktual.

    Dalam konteks data PNBP sebagai dasar kebijakan keuangan digital negara, model ini mendukung pengambilan keputusan berbasis data.
    \"\"\")

    st.markdown("### ✅ Kesimpulan")
    st.write(\"\"\"
    - Model ini cocok untuk data tren linier jangka pendek tanpa musiman.
    - Hasil klasifikasi MAPE menunjukkan tingkat akurasi sangat tinggi.
    - Direkomendasikan untuk digunakan sebagai alat bantu proyeksi kebijakan berbasis data historis PNBP.
    \"\"\")
'''

# Tulis ulang file
file_path.write_text(cleaned_code)
file_path.name
