import streamlit as st
import pandas as pd
import io
import os
import zipfile
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import matplotlib.font_manager as fm
import tempfile


def convert_df_to_excel(df_dict):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        for sheet_name, df in df_dict.items():
            df.to_excel(writer, index=False, sheet_name=sheet_name[:31])
    return output.getvalue()

def export_graphs_as_images(df_pred):
    output_files = {}
    df_pred = df_pred.copy()
    df_pred = df_pred.sort_values("Tahun")

    df_pred["Aktual"] = pd.to_numeric(df_pred["Aktual"].astype(str).str.replace("Rp", "").str.replace(".", "").str.replace(",", "."), errors="coerce")
    df_pred["Prediksi"] = pd.to_numeric(df_pred["Prediksi"].astype(str).str.replace("Rp", "").str.replace(".", "").str.replace(",", "."), errors="coerce")

    fig, ax = plt.subplots(figsize=(10, 5))
    hist = df_pred[df_pred["Jenis Tahun"] == "Historis"]
    pred = df_pred[df_pred["Jenis Tahun"] == "Prediksi"]

    scale = 1e12  # Triliun
    font = {'family': 'sans-serif', 'weight': 'normal', 'size': 10}
    plt.rc('font', **font)

    ax.plot(hist["Tahun"], hist["Aktual"] / scale, color="#1f77b4", marker="circle", label="Aktual (Histori)", linewidth=2)
    ax.plot(df_pred["Tahun"], df_pred["Prediksi"] / scale, color="#ff7f0e", linestyle="--", marker="circle", label="Prediksi (Double Smoothing)", linewidth=2)

    ax.set_title("Prediksi Total PNBP vs Data Aktual (Double Smoothing)", fontsize=12, fontweight='bold')
    ax.set_xlabel("Tahun", fontsize=11)
    ax.set_ylabel("Nominal PNBP (Rp Triliun)", fontsize=11)
    ax.grid(True, linestyle=':', linewidth=0.7, alpha=0.7)
    ax.legend(frameon=False, fontsize=10)
    ax.yaxis.set_major_formatter(mtick.FormatStrFormatter('%.0f T'))

    plt.tight_layout()

    for fmt in ["png", "pdf", "svg"]:
        buf = io.BytesIO()
        fig.savefig(buf, format=fmt, dpi=300)
        buf.seek(0)
        output_files[fmt] = buf

    plt.close(fig)
    return output_files

# ... (rest of the unchanged code below)
