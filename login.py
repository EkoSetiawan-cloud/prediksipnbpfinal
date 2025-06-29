import streamlit as st

# Data akun (sementara hardcoded)
users = {
    "admin": "admin123",
    "user": "user456"
}

def login_page():
    st.markdown("""
        <div style="text-align:center">
            <h1 style="color:#3C8DBC;">🔐 Selamat Datang di Aplikasi Prediksi PNBP DJID KOMDIGI</h1>
            <p style="font-size:16px; color:gray;">
                Silakan login untuk mengakses fitur lengkap aplikasi. 
                Login digunakan untuk memastikan keamanan dan personalisasi pengguna saat melakukan analisis prediktif.
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Form login
    st.subheader("🔑 Masuk ke Akun Anda")
    username = st.text_input("👤 Username")
    password = st.text_input("🔒 Password", type="password")

    col1, col2 = st.columns([1, 5])
    with col1:
        login_clicked = st.button("Login")
    with col2:
        st.caption("Gunakan username dan password yang telah ditentukan.")

    # Validasi login
    if login_clicked:
        if username in users and users[username] == password:
            st.session_state["logged_in"] = True
            st.session_state["username"] = username
            st.success(f"✅ Login berhasil. Selamat datang, {username}!")
        else:
            st.error("❌ Username atau password salah. Silakan coba lagi.")

    # Jika sudah login
    if st.session_state.get("logged_in"):
        st.success(f"Anda sudah login sebagai **{st.session_state['username']}**.")
        return True

    return False
