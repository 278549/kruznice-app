import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont

# Registrace fontu s podporou češtiny
pdfmetrics.registerFont(UnicodeCIDFont('HeiseiMin-W3'))

# ----------------------------
# TITULEK
# ----------------------------
st.title("Body na kružnici")

# ----------------------------
# VSTUPY V SIDEBARU
# ----------------------------
st.sidebar.header("Nastavení kružnice")

x_center = st.sidebar.number_input("Souřadnice středu X", value=0.0)
y_center = st.sidebar.number_input("Souřadnice středu Y", value=0.0)
radius = st.sidebar.number_input("Poloměr", min_value=0.1, value=5.0)
num_points = st.sidebar.slider("Počet bodů na kružnici", min_value=3, max_value=100, value=10)
color = st.sidebar.color_picker("Barva bodů", value="#FF0000")

# ----------------------------
# VÝPOČET BODŮ NA KRUŽNICI
# ----------------------------
angles = np.linspace(0, 2 * np.pi, num_points, endpoint=False)
x_points = x_center + radius * np.cos(angles)
y_points = y_center + radius * np.sin(angles)

# ----------------------------
# VYTVOŘENÍ ZÁLOŽEK
# ----------------------------
tab1, tab2 = st.tabs(["Kružnice", "O aplikaci"])

with tab1:
    # Vykreslení grafu
    fig, ax = plt.subplots()
    ax.scatter(x_points, y_points, color=color, label="Body")
    ax.plot(x_points, y_points, color=color, alpha=0.3, linestyle='--')

    # Očíslování bodů
    for i, (x, y) in enumerate(zip(x_points, y_points), start=1):
        ax.text(x, y, f"P{i}", fontsize=9, ha="right", va="bottom")

    # Osy s nulovým bodem
    ax.axhline(0, color="black", linewidth=0.8)
    ax.axvline(0, color="black", linewidth=0.8)
    ax.set_xlim(x_center - radius - 1, x_center + radius + 1)
    ax.set_ylim(y_center - radius - 1, y_center + radius + 1)

    ax.set_aspect('equal', 'box')
    ax.set_xlabel("X [m]")
    ax.set_ylabel("Y [m]")
    ax.grid(True)
    ax.legend()
    ax.set_title("Kružnice s body")

    st.pyplot(fig)

with tab2:
    st.header("Informace o aplikaci")
    st.write("""
    **Autor:** Dominik Zábranský  
    **Kontakt:** 278549@vut.cz  

    **Použité technologie:**  
    - Python  
    - Streamlit  
    - Matplotlib  
    - ReportLab  
    """)

# ----------------------------
# FUNKCE PRO PDF S DIKRITIKOU
# ----------------------------
def create_pdf():
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)

    # Textové informace nahoře
    text = c.beginText(40, 800)
    text.setFont("HeiseiMin-W3", 14)
    text.textLine("Parametry úlohy")
    text.setFont("HeiseiMin-W3", 12)
    text.textLine(f"Střed kružnice: ({x_center}, {y_center})")
    text.textLine(f"Poloměr: {radius} m")
    text.textLine(f"Počet bodů: {num_points}")
    text.textLine(f"Barva bodů: {color}")
    text.textLine("")
    text.textLine("Autor: Dominik Zábranský")
    text.textLine("Kontakt: 278549@vut.cz")
    text.textLine("")
    text.textLine("Vytvořeno pomocí Python + Streamlit + ReportLab")
    c.drawText(text)

    # Vložení obrázku grafu pod text
    img_buffer = BytesIO()
    fig.savefig(img_buffer, format='PNG')
    img_buffer.seek(0)
    img = ImageReader(img_buffer)
    c.drawImage(img, 40, 200, width=500, preserveAspectRatio=True, mask='auto')

    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer

# ----------------------------
# TLAČÍTKA KE STAŽENÍ
# ----------------------------
st.download_button(
    label="📄 Stáhnout PDF s parametry a grafem",
    data=create_pdf(),
    file_name="parametry_kruznice.pdf",
    mime="application/pdf"
)

# PNG export grafu
img_buffer = BytesIO()
fig.savefig(img_buffer, format="PNG")
img_buffer.seek(0)

st.download_button(
    label="📷 Stáhnout graf jako PNG",
    data=img_buffer,
    file_name="kruznice.png",
    mime="image/png"
)
