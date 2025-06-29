import streamlit as st

# Data akun (bisa diganti atau diambil dari file/database)
users = {
    "admin": "admin123",
    "user": "user456"
}

def login_page():
    if not st.session_state.get("logged_in"):
        st.markdown("<h1 style='color:#80080;'>🔐 Selamat Datang di Aplikasi Prediksi PNBP DJID KOMDIGI</h1>", unsafe_allow_html=True)
        st.markdown("Silakan login untuk mengakses fitur lengkap aplikasi. Login digunakan untuk memastikan keamanan dan personalisasi pengguna saat melakukan analisis prediktif.")

        st.markdown("""
            ### 🎯 Fokus Penelitian
            Penelitian ini berfokus menjawab pertanyaan spesifik sebagai berikut:<br>
            a. **Q1:** Bagaimana tren historis BHP PNBP pada layanan-layanan Ditjen Infradig selama periode 2014–2024?<br>
            b. **Q2:** Bagaimana membangun model prediksi BHP PNBP berbasis time series menggunakan metode exponential smoothing yang mampu menangkap pola historis secara akurat?<br>
            c. **Q3:** Seberapa akurat model yang dikembangkan jika dievaluasi dengan MAE, MAPE, dan RMSE?<br>
            d. **Q4:** Bagaimana strategi pemanfaatan hasil prediksi dalam mendukung kebijakan dan perencanaan Ditjen Infradig?
        """, unsafe_allow_html=True)

        st.subheader("🔑 Masuk ke Akun Anda")
        username = st.text_input("👤 Username")
        password = st.text_input("🔒 Password", type="password")

        if st.button("Login"):
            if username in users and users[username] == password:
                st.session_state["logged_in"] = True
                st.session_state["username"] = username
                st.success(f"Login berhasil. Selamat datang, {username}!")
                st.rerun()
            else:
                st.error("❌ Username atau password salah. Silakan coba lagi.")
        return False

    return True
