import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def visualisasi_prediksi_page():
    st.markdown("<h1 style='color:#3C8DBC;'>📉 Visualisasi Interaktif Prediksi vs Aktual PNBP</h1>", unsafe_allow_html=True)

    st.markdown("""
    Modul ini menyajikan grafik interaktif untuk membandingkan hasil prediksi model **Double Exponential Smoothing** dengan data aktual. 

    Visualisasi ini bertujuan membantu pengguna memahami apakah tren prediksi mengikuti pola historis, serta mengidentifikasi potensi deviasi dari proyeksi. 

    Garis biru menunjukkan data aktual (historis), sementara garis oranye putus-putus menunjukkan hasil prediksi dari model. 
    """)

    if "prediksi_pnbp" not in st.session_state:
        st.warning("⚠️ Data prediksi belum tersedia. Jalankan Modul Prediksi terlebih dahulu.")
        return

    df = st.session_state["prediksi_pnbp"].copy()
    df.columns = [col.lower().strip() for col in df.columns]

    required_cols = ['tahun', 'aktual', 'prediksi', 'jenis tahun']
    if not all(col in df.columns for col in required_cols):
        st.error(f"❌ Dataset prediksi tidak lengkap. Harus punya kolom: {required_cols}")
        return

    df["aktual"] = pd.to_numeric(df["aktual"], errors="coerce")
    df["prediksi"] = pd.to_numeric(df["prediksi"], errors="coerce")
    df = df.sort_values("tahun")

    df_hist = df[df["jenis tahun"] == "Historis"]
    df_all = df.copy()

    st.subheader("📈 Grafik Prediksi Double Smoothing (Interaktif)")
    st.caption("Grafik ini menampilkan perbandingan antara nilai aktual historis dengan hasil prediksi model Double Exponential Smoothing.")

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df_hist["tahun"],
        y=df_hist["aktual"],
        mode="lines+markers",
        name="Aktual (Historis)",
        line=dict(color="blue"),
        hovertemplate="Tahun: %{x}<br>Aktual: Rp %{y:,.0f}<extra></extra>"
    ))

    fig.add_trace(go.Scatter(
        x=df_all["tahun"],
        y=df_all["prediksi"],
        mode="lines+markers",
        name="Prediksi (Double Smoothing)",
        line=dict(color="orange", dash="dash"),
        hovertemplate="Tahun: %{x}<br>Prediksi: Rp %{y:,.0f}<extra></extra>"
    ))

    fig.update_layout(
        title="Prediksi Total PNBP vs Data Aktual (Double Smoothing)",
        xaxis_title="Tahun",
        yaxis_title="Nominal PNBP (Rp)",
        hovermode="x unified",
        legend=dict(x=0, y=1),
        template="plotly_white",
        height=500
    )

    st.plotly_chart(fig, use_container_width=True)
    st.info("ℹ️ Gunakan grafik ini untuk menjelaskan sejauh mana model mengikuti pola aktual, dan untuk mendukung validasi hasil evaluasi prediksi.")
