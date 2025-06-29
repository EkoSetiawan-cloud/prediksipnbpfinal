st.subheader("🧠 Metode Prediksi yang Digunakan")
st.markdown("""
Aplikasi ini menggunakan metode **Double Exponential Smoothing (Holt’s Method)** untuk memprediksi total PNBP tahunan.

### 🧠 Alasan Pemilihan
Model ini sangat cocok untuk data PNBP karena:
- Memiliki tren linier tahunan yang konsisten
- Tidak menunjukkan pola musiman yang kompleks
- Diperlukan model yang cepat, stabil, dan mudah dijelaskan
""")

st.markdown("""
### ⚙️ Cara Kerja Model
Double exponential smoothing menggunakan dua komponen utama:
- **Level (L_t)**: estimasi nilai saat ini
- **Trend (T_t)**: estimasi arah perubahan
""")

st.latex(r"""
\begin{aligned}
L_t &= \alpha y_t + (1 - \alpha)(L_{t-1} + T_{t-1}) \\
T_t &= \beta (L_t - L_{t-1}) + (1 - \beta) T_{t-1} \\
\hat{y}_{t+m} &= L_t + m \cdot T_t
\end{aligned}
""")

st.markdown("""
### ✅ Keunggulan
- Cepat dan efisien
- Sederhana untuk interpretasi dan visualisasi
- Cocok untuk data dengan tren linier

### ⚠️ Keterbatasan
- Tidak bisa menangani musiman
- Kurang fleksibel jika tren berubah drastis

### 📚 Dukungan Ilmiah
- Dikembangkan oleh Charles Holt (1957) dan disempurnakan oleh Winters
- Digunakan luas dalam ekonomi, industri, dan bisnis ([Penn State Online](https://online.stat.psu.edu/stat501/lesson/6/6.2))
- Validasi empiris oleh berbagai studi time series forecasting
""")
