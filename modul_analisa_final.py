import streamlit as st

def kesimpulan_analisa_page():
    st.markdown("<h1 style='color:#3C8DBC;'>📋 Kesimpulan & Analisa Prediksi PNBP</h1>", unsafe_allow_html=True)

    st.markdown("### 🎯 Tujuan Analisis")
    st.markdown(
        "Evaluasi model prediksi bertujuan untuk:<br>"
        "- Menilai seberapa dekat nilai prediksi terhadap nilai aktual<br>"
        "- Menentukan tingkat akurasi dan konsistensi model secara kuantitatif<br>"
        "- Memberikan dasar argumentatif dalam pengambilan keputusan prediktif berbasis data",
        unsafe_allow_html=True
    )

    st.markdown("### 📈 Hasil Evaluasi Model")
    st.markdown(
        "Berdasarkan hasil perhitungan menggunakan tiga metrik utama:<br><br>"
        "- **MAE (Mean Absolute Error):** rata-rata selisih absolut antara nilai aktual dan prediksi.<br>"
        "- **MAPE (Mean Absolute Percentage Error):** error relatif dalam bentuk persentase. MAPE < 10% sangat akurat.<br>"
        "- **RMSE (Root Mean Square Error):** cocok untuk mengukur konsistensi model terhadap fluktuasi.<br><br>"
        "Validasi berdasarkan MAPE:<br>"
        "- ≤ 10% = Sangat Akurat<br>"
        "- ≤ 20% = Akurat<br>"
        "- ≤ 50% = Cukup Akurat<br>"
        "- > 50% = Tidak Akurat",
        unsafe_allow_html=True
    )

    st.markdown("### 📊 Interpretasi Akademik")
    st.markdown(
        "Hasil evaluasi menunjukkan model Double Exponential Smoothing mampu memetakan tren linier historis. "
        "MAE dan RMSE yang rendah mengindikasikan kestabilan model. "
        "MAPE yang kecil memperlihatkan bahwa model menjaga kesalahan relatif yang kecil terhadap data aktual.<br><br>"
        "Dalam konteks data PNBP sebagai dasar kebijakan keuangan digital negara, model ini mendukung pengambilan keputusan berbasis data.",
        unsafe_allow_html=True
    )

    st.markdown("### ✅ Kesimpulan")
    st.markdown(
        "- Model ini cocok untuk data tren linier jangka pendek tanpa musiman.<br>"
        "- Hasil klasifikasi MAPE menunjukkan tingkat akurasi sangat tinggi.<br>"
        "- Direkomendasikan untuk digunakan sebagai alat bantu proyeksi kebijakan berbasis data historis PNBP.",
        unsafe_allow_html=True
    )
