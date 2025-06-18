import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def visualisasi_prediksi_page():
    st.title("📉 Visualisasi Interaktif Prediksi vs Aktual PNBP")

    if "prediksi_pnbp" not in st.session_state:
        st.warning("⚠️ Data prediksi belum tersedia. Jalankan Modul Prediksi terlebih dahulu.")
        return

    # Ambil data dan normalisasi kolom
    df = st.session_state["prediksi_pnbp"].copy()
    df.columns = [col.lower().strip() for col in df.columns]

    # Validasi kolom
    required_cols = ['tahun', 'aktual', 'prediksi', 'jenis tahun']
    if not all(col in df.columns for col in required_cols):
        st.error(f"❌ Dataset prediksi tidak lengkap. Harus punya kolom: {required_cols}")
        return

    # Pastikan numerik
    df["aktual"] = pd.to_numeric(df["aktual"], errors="coerce")
    df["prediksi"] = pd.to_numeric(df["prediksi"], errors="coerce")
    df = df.sort_values("tahun")

    df_hist = df[df["jenis tahun"] == "Historis"]
    df_all = df.copy()

    st.subheader("📈 Grafik Prediksi Holt-Winters (Interaktif)")

    fig = go.Figure()

    # Garis Aktual
    fig.add_trace(go.Scatter(
        x=df_hist["tahun"],
        y=df_hist["aktual"],
        mode="lines+markers",
        name="Aktual (Historis)",
        line=dict(color="blue"),
        hovertemplate="Tahun: %{x}<br>Aktual: Rp %{y:,.0f}<extra></extra>"
    ))

    # Garis Prediksi
    fig.add_trace(go.Scatter(
        x=df_all["tahun"],
        y=df_all["prediksi"],
        mode="lines+markers",
        name="Prediksi Holt-Winters",
        line=dict(color="orange", dash="dash"),
        hovertemplate="Tahun: %{x}<br>Prediksi: Rp %{y:,.0f}<extra></extra>"
    ))

    # Layout
    fig.update_layout(
        title="Prediksi Total PNBP vs Data Aktual",
        xaxis_title="Tahun",
        yaxis_title="Nominal PNBP (Rp)",
        hovermode="x unified",
        legend=dict(x=0, y=1),
        template="plotly_white",
        height=500
    )

    st.plotly_chart(fig, use_container_width=True)
