import streamlit as st
import google.generativeai as genai
from datetime import datetime
from PIL import Image
import pandas as pd
import matplotlib.pyplot as plt
import re
import os
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Image as PDFImage,
    PageBreak,
)

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
from reportlab.pdfgen import canvas


def add_page_number(canvas, doc):
    page_num = canvas.getPageNumber()
    text = f"Page {page_num}"
    canvas.drawRightString(550, 20, text)


# ---------------- PDF Function ----------------


def create_pdf(report_text, student_name, roll_no, experiment, observation):

    pdf_file = f"lab_report_{datetime.now().strftime('%H%M%S')}.pdf"

    styles = getSampleStyleSheet()
    doc = SimpleDocTemplate(pdf_file)

    from reportlab.lib.enums import TA_CENTER
    from reportlab.lib.styles import ParagraphStyle

    center_style = ParagraphStyle(
        name="Center",
        parent=styles["Title"],
        alignment=TA_CENTER,
        fontSize=18,
        leading=22,
    )

    center_body = ParagraphStyle(
        name="CenterBody",
        parent=styles["BodyText"],
        alignment=TA_CENTER,
        fontSize=12,
        leading=16,
    )

    content = []
    graph_file = create_graph(observation)

    # ---------------- COVER PAGE ----------------

    try:
        logo = PDFImage("logo.jpg", width=100, height=100)
        logo.hAlign = "CENTER"
        content.append(logo)
    except:
        pass

    content.append(Spacer(1, 10))

    content.append(
        Paragraph("<b>UNIVERSITY OF ENGINEERING & MANAGEMENT</b>", center_style)
    )

    content.append(Spacer(1, 10))

    content.append(Paragraph("<b>AI LAB REPORT</b>", styles["Title"]))

    content.append(Spacer(1, 20))

    content.append(
        Paragraph(f"<b>Experiment Name:</b> {experiment}", styles["BodyText"])
    )

    content.append(
        Paragraph(f"<b>Student Name:</b> {student_name}", styles["BodyText"])
    )

    content.append(Paragraph(f"<b>Roll Number:</b> {roll_no}", styles["BodyText"]))

    content.append(
        Paragraph(
            f"<b>Date:</b> {datetime.now().strftime('%d-%m-%Y')}", styles["BodyText"]
        )
    )

    content.append(Spacer(1, 30))

    content.append(
        Paragraph("<b>---------------- REPORT ----------------</b>", styles["Heading2"])
    )
    content.append(PageBreak())

    # ---------------- GRAPH ----------------

    if graph_file:
        content.append(Spacer(1, 20))
        content.append(PDFImage(graph_file, width=400, height=250))

        content.append(Spacer(1, 20))

    # ---------------- REPORT CONTENT ----------------
    content.append(Spacer(1, 20))
    content.append(Paragraph("<b>VIVA QUESTIONS & ANSWERS</b>", styles["Heading2"]))
    content.append(Spacer(1, 10))
    for line in report_text.split("\n"):
        if line.strip():
            content.append(Paragraph(line, styles["BodyText"]))

    content.append(Spacer(1, 6))
    content.append(Spacer(1, 6))
    content.append(Paragraph("__________________________", center_body))
    content.append(Paragraph("Signature of Student", center_body))

    content.append(Spacer(1, 20))

    content.append(Paragraph("__________________________", center_body))
    content.append(Paragraph("Signature of Teacher", center_body))

    doc.build(content, onFirstPage=add_page_number, onLaterPages=add_page_number)
    return pdf_file


# ---------------- Graph Function ----------------


def create_graph(observation):

    lengths = []
    times = []

    pattern = r"Length\s*=\s*(\d+).*?Time\s*=\s*(\d+)"

    matches = re.findall(pattern, observation)

    for match in matches:
        lengths.append(float(match[0]))
        times.append(float(match[1]))

    if len(lengths) > 1:

        plt.figure(figsize=(6, 4))

        plt.plot(lengths, times, marker="o")

        plt.xlabel("Length")
        plt.ylabel("Time")
        plt.title("Length vs Time")

        plt.grid(True)

        plt.savefig("graph.png")

        plt.close()

        return "graph.png"

    return None


# ---------------- Page Settings ----------------
st.set_page_config(page_title="AI Lab Report Assistant", page_icon="🧪", layout="wide")

import os

if os.path.exists("logo.jpg"):
    logo = Image.open("logo.jpg")
else:
    logo = None

# Header
col1, col2 = st.columns([2, 5])

with col1:
    st.image(logo, width=220)

with col2:
    st.title("🧪 AI Lab Report Assistant")
    st.write("Generate professional laboratory reports using Gemini AI")
    st.caption("University of Engineering & Management")


# ---------------- Sidebar ----------------

# ---------------- Sidebar ----------------

st.sidebar.header("Settings")

api_key = st.secrets.get("GEMINI_API_KEY", None)
if not api_key:
    api_key = st.sidebar.text_input("Gemini API Key", type="password")
dark_mode = st.sidebar.toggle("🌙 Dark Mode")

if dark_mode:
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #0E1117;
            color: white;
        }

        h1, h2, h3, h4, h5, h6, p, label {
            color: white !important;
        }

        .stTextInput input,
        .stTextArea textarea {
            background-color: #262730;
            color: white;
        }

        .stButton button {
            background-color: #4CAF50;
            color: white;
            border-radius: 10px;
        }

        .card {
            background-color: #1e1e1e;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
# ---------------- Student Information ----------------

# ---------------- CARD STYLE UI ----------------

st.markdown("""
<style>
.card {
    background-color: #1e1e1e;
    padding: 20px;
    border-radius: 15px;
    margin-bottom: 15px;
    box-shadow: 0px 4px 10px rgba(0,0,0,0.3);
}
</style>
""", unsafe_allow_html=True)


# 🪪 Student Card
st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("🪪 Student Information")

col1, col2 = st.columns(2)

with col1:
    student_name = st.text_input("Student Name")

with col2:
    roll_no = st.text_input("Roll Number")

st.markdown('</div>', unsafe_allow_html=True)


# 🔬 Experiment Card
st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("🔬 Experiment Details")

experiment = st.text_input("Experiment Name")

st.markdown('</div>', unsafe_allow_html=True)


# 📊 Observation Card
st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("📊 Observation Data")

observation = st.text_area(
    "Observations / Raw Data",
    height=200,
    placeholder="""
Length = 20 cm, Time = 18 sec
Length = 40 cm, Time = 25 sec
Length = 60 cm, Time = 31 sec

Observation:
Time period increases with length.
""",
)

st.markdown('</div>', unsafe_allow_html=True)

# ---------------- Generate Button ----------------

if st.button("🚀 Generate Report", use_container_width=True):

    if not api_key:
        st.error("Please enter your Gemini API Key.")
        st.stop()

    if not student_name:
        st.error("Please enter Student Name.")
        st.stop()

    if not roll_no:
        st.error("Please enter Roll Number.")
        st.stop()

    if not experiment:
        st.error("Please enter Experiment Name.")
        st.stop()

    if not observation:
        st.error("Please enter Observation Data.")
        st.stop()

    try:

        genai.configure(api_key=api_key)

        model = genai.GenerativeModel("gemini-2.5-flash")

        prompt = f"""
You are an engineering laboratory assistant.

Generate a professional laboratory report.

Student Name: {student_name}
Roll Number: {roll_no}
Experiment Name: {experiment}

Observation Data:
{observation}

Instructions:

1. Generate the report with these sections:

- Title
- Student Details
- Aim
- Theory
- Apparatus Required
- Procedure
- Observation
- Data Analysis
- Result
- Conclusion
- Precautions

2. Analyze any numerical data.

3. Explain trends clearly.

4. Use engineering language.

5. Format neatly.

6. Do not mention AI.
Also generate:

VIVA QUESTIONS & ANSWERS

Generate 10 viva questions with short answers.

Format:

Q1:
Answer:

Q2:
Answer:
"""

        with st.spinner("Generating Report..."):
            response = model.generate_content(prompt)

        report = response.text
        graph_file = create_graph(observation)

        pdf_file = create_pdf(report, student_name, roll_no, experiment, observation)

        st.success("✅ Report Generated Successfully!")

        st.markdown(report)
        if graph_file:

            st.subheader("📊 Observation Graph")

            st.image(graph_file)

        # TXT Download
        st.download_button(
            label="📥 Download TXT Report",
            data=report,
            file_name=f"{experiment.replace(' ','_')}_Report.txt",
            mime="text/plain",
        )

        # PDF Download
        with open(pdf_file, "rb") as pdf:

            st.download_button(
                label="📄 Download PDF Report",
                data=pdf,
                file_name=f"{experiment.replace(' ','_')}_Report.pdf",
                mime="application/pdf",
            )

    except Exception as e:

        st.error(f"❌ Error: {str(e)}")


# ---------------- Footer ----------------

st.markdown("---")

st.caption(f"Generated on {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}")
