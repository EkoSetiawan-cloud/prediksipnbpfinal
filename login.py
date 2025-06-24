import streamlit as st

# Data akun (bisa diganti atau diambil dari file/database)
users = {
    "admin": "admin123",
    "user": "user456"
}

def login_page():
    st.title("🔐 Halaman Login")

    # Cek jika sudah login
    if st.session_state.get("logged_in"):
        st.success(f"Selamat datang, {st.session_state['username']}!")
        return True

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username in users and users[username] == password:
            st.session_state["logged_in"] = True
            st.session_state["username"] = username
            st.success(f"Login berhasil. Selamat datang, {username}!")
        else:
            st.error("Username atau password salah.")

    return False
