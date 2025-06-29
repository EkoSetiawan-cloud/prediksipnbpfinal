import streamlit as st

# Data akun (bisa diganti atau diambil dari file/database)
users = {
    "admin": "admin123",
    "user": "user456"
}

def login_page():
    st.title("🔐 Selamat Datang di Aplikasi Prediksi PNBP DJID KOMDIGI")
    st.markdown("""
        Silakan login untuk mengakses fitur lengkap aplikasi. Login digunakan untuk memastikan keamanan dan personalisasi pengguna saat melakukan analisis prediktif.
    """)

    if st.session_state.get("logged_in"):
        st.success(f"Anda sudah login sebagai **{st.session_state['username']}**.")
        st.stop()

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
