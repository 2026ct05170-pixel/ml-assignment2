from pathlib import Path
import csv
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
                                PageBreak, Image, KeepTogether)
from reportlab.graphics.shapes import Drawing, Rect, String, Line

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "assignment2_report.pdf"
SHOT = ROOT / "bits_virtual_lab_execution.png"
with open(ROOT / "model_metrics.csv", newline="", encoding="utf-8-sig") as f:
    metrics = list(csv.DictReader(f))

PAGE_W, PAGE_H = A4
NAVY = colors.HexColor("#17324D")
BLUE = colors.HexColor("#4776A8")
TEAL = colors.HexColor("#3A7CA5")
MUTED = colors.HexColor("#526171")
PALE = colors.HexColor("#EDF3F8")

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="TitleCustom", parent=styles["Title"], fontName="Helvetica-Bold", fontSize=25, leading=30, textColor=NAVY, alignment=TA_LEFT, spaceAfter=5))
styles.add(ParagraphStyle(name="SubtitleCustom", parent=styles["Normal"], fontName="Helvetica", fontSize=12, leading=17, textColor=MUTED, spaceAfter=14))
styles.add(ParagraphStyle(name="H1Custom", parent=styles["Heading1"], fontName="Helvetica-Bold", fontSize=15, leading=19, textColor=NAVY, spaceBefore=10, spaceAfter=6, keepWithNext=True))
styles.add(ParagraphStyle(name="H2Custom", parent=styles["Heading2"], fontName="Helvetica-Bold", fontSize=10.5, leading=14, textColor=TEAL, spaceBefore=7, spaceAfter=4, keepWithNext=True))
styles.add(ParagraphStyle(name="BodyCustom", parent=styles["BodyText"], fontName="Helvetica", fontSize=9.3, leading=13.1, textColor=colors.HexColor("#243447"), spaceAfter=5))
styles.add(ParagraphStyle(name="SmallCustom", parent=styles["BodyText"], fontName="Helvetica", fontSize=7.6, leading=10, textColor=MUTED, spaceAfter=3))
styles.add(ParagraphStyle(name="CellCustom", parent=styles["BodyText"], fontName="Helvetica", fontSize=7.2, leading=9, textColor=colors.HexColor("#243447")))
styles.add(ParagraphStyle(name="CellHeader", parent=styles["BodyText"], fontName="Helvetica-Bold", fontSize=7.2, leading=9, textColor=colors.white, alignment=TA_CENTER))
styles.add(ParagraphStyle(name="CaptionCustom", parent=styles["BodyText"], fontName="Helvetica-Oblique", fontSize=8, leading=10, textColor=MUTED, alignment=TA_CENTER, spaceBefore=4, spaceAfter=8))


def footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(colors.HexColor("#D6E0E8"))
    canvas.line(doc.leftMargin, 15*mm, PAGE_W-doc.rightMargin, 15*mm)
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(MUTED)
    canvas.drawString(doc.leftMargin, 10*mm, "Machine Learning Assignment 2 | Wisconsin Breast Cancer Classification")
    canvas.drawRightString(PAGE_W-doc.rightMargin, 10*mm, f"Page {doc.page}")
    canvas.restoreState()


def metric_chart():
    drawing = Drawing(500, 230)
    drawing.add(String(250, 214, "Held-out metrics by model", textAnchor="middle", fontName="Helvetica-Bold", fontSize=11, fillColor=NAVY))
    left, bottom, plot_h = 40, 56, 126
    plot_w = 445
    for k in range(6):
        v = k / 5
        y = bottom + v * plot_h
        drawing.add(Line(left, y, left+plot_w, y, strokeColor=colors.HexColor("#D9E2EA"), strokeWidth=.5))
        drawing.add(String(left-6, y-2, f"{v:.1f}", textAnchor="end", fontName="Helvetica", fontSize=7, fillColor=MUTED))
    keys = ["Accuracy", "AUC", "Precision", "Recall", "F1"]
    palette = [colors.HexColor("#2F6690"), colors.HexColor("#3A7CA5"), colors.HexColor("#D1495B"), colors.HexColor("#EDAE49"), colors.HexColor("#6A994E")]
    names = ["Logistic Reg.", "Decision Tree", "KNN", "Gaussian NB", "Random Forest", "RBF SVM"]
    group_w = plot_w / len(metrics)
    bar_w = 8
    for i, row in enumerate(metrics):
        gx = left + i*group_w + 8
        for j, key in enumerate(keys):
            v = float(row[key])
            height = v * plot_h
            drawing.add(Rect(gx+j*(bar_w+2), bottom, bar_w, height, fillColor=palette[j], strokeColor=None))
        drawing.add(String(gx+20, 37, names[i], textAnchor="middle", fontName="Helvetica", fontSize=6.7, fillColor=MUTED))
    for j, key in enumerate(keys):
        x = 60 + j*86
        drawing.add(Rect(x, 14, 9, 9, fillColor=palette[j], strokeColor=None))
        drawing.add(String(x+13, 16, key, fontName="Helvetica", fontSize=7, fillColor=MUTED))
    return drawing


def mcc_chart():
    drawing = Drawing(500, 205)
    drawing.add(String(250, 187, "Matthews correlation coefficient", textAnchor="middle", fontName="Helvetica-Bold", fontSize=11, fillColor=NAVY))
    left, top, width = 130, 160, 330
    names = ["Logistic Regression", "Decision Tree", "K-Nearest Neighbors", "Gaussian Naive Bayes", "Random Forest", "RBF SVM (additional)"]
    for tick in range(6):
        v=tick/5
        x=left+v*width
        drawing.add(Line(x, 18, x, 166, strokeColor=colors.HexColor("#D9E2EA"), strokeWidth=.5))
        drawing.add(String(x, 5, f"{v:.1f}", textAnchor="middle", fontName="Helvetica", fontSize=7, fillColor=MUTED))
    for i,row in enumerate(metrics):
        y=top-i*24
        drawing.add(String(left-7,y+2,names[i],textAnchor="end",fontName="Helvetica",fontSize=7.2,fillColor=MUTED))
        val=float(row["MCC"])
        drawing.add(Rect(left,y-5,val*width,13,fillColor=BLUE,strokeColor=None))
        drawing.add(String(left+val*width+4,y-2,f"{val:.4f}",fontName="Helvetica",fontSize=7,fillColor=MUTED))
    return drawing


def P(txt, style="BodyCustom"):
    return Paragraph(txt, styles[style])

story=[]
story += [P("Machine Learning Assignment 2", "TitleCustom"), P("Classification Models for Wisconsin Breast Cancer Diagnosis", "SubtitleCustom")]
story += [P("In this assignment, I compare six classifiers using the same stratified 80:20 train-test split. Logistic Regression gave the strongest results in this run for accuracy, AUC, F1, and MCC. The instructions list five models, but the results table asks for six. I included an RBF Support Vector Machine as the additional model.")]
story += [P("Problem statement", "H1Custom"), P("The aim is to predict whether a breast mass is malignant or benign from measurements of cell nuclei. I compare the models using Accuracy, ROC AUC, Precision, Recall, F1, and Matthews Correlation Coefficient.")]
story += [P("Dataset description", "H1Custom"), P("The Wisconsin Diagnostic Breast Cancer dataset has 569 cases and 30 numeric measurements from digitized fine needle aspirate images. The target is <b>target</b>: 0 means malignant and 1 means benign. There are 212 malignant cases (37.3%) and 357 benign cases (62.7%). All input features are numeric, so categorical encoding is not needed. The data comes from the UCI Machine Learning Repository: https://archive.ics.uci.edu/dataset/17/breast+cancer+wisconsin+diagnostic.")]
story += [P("Preprocessing", "H1Custom"), P("There were no missing values or duplicate rows. The code checks for duplicates and includes a median imputer in each model pipeline. I split the data into 80% training and 20% testing, keeping the class proportions similar in both parts (random_state=42). Logistic Regression, KNN, Gaussian Naive Bayes, and SVM use scaling. The tree models do not. Preprocessing is fitted on training data only. Benign (label 1) is the positive class for the displayed Precision, Recall, F1, and AUC values.")]
story += [P("Model configurations", "H1Custom")]
config=[
 [P("Model","CellHeader"),P("Configuration","CellHeader")],
 [P("Logistic Regression","CellCustom"),P("StandardScaler; max_iter=5000; seed=42","CellCustom")],
 [P("Decision Tree","CellCustom"),P("Balanced class weights; seed=42","CellCustom")],
 [P("K-Nearest Neighbors","CellCustom"),P("k=5; StandardScaler","CellCustom")],
 [P("Gaussian Naive Bayes","CellCustom"),P("StandardScaler","CellCustom")],
 [P("Random Forest","CellCustom"),P("300 trees; balanced class weights; seed=42","CellCustom")],
 [P("RBF Support Vector Machine (additional)","CellCustom"),P("RBF kernel; balanced class weights; StandardScaler; seed=42","CellCustom")],
]
t=Table(config,colWidths=[185,315],repeatRows=1)
t.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,0),NAVY),("GRID",(0,0),(-1,-1),.35,colors.HexColor("#CFD8E1")),("VALIGN",(0,0),(-1,-1),"MIDDLE"),("LEFTPADDING",(0,0),(-1,-1),6),("RIGHTPADDING",(0,0),(-1,-1),6),("TOPPADDING",(0,0),(-1,-1),4),("BOTTOMPADDING",(0,0),(-1,-1),4),("ROWBACKGROUNDS",(0,1),(-1,-1),[colors.white,PALE])]))
story += [t, PageBreak()]

story += [P("Model results", "TitleCustom"), P("The metrics below are from the successful BITS Virtual Lab run. Values are rounded to four decimal places.","SubtitleCustom")]
headers=["Model","Accuracy","AUC","Precision","Recall","F1","MCC"]
rows=[[P(h,"CellHeader") for h in headers]]
for r in metrics:
    rows.append([P(r["Model"],"CellCustom")]+[P(f"{float(r[k]):.4f}","CellCustom") for k in headers[1:]])
t=Table(rows,colWidths=[174,53,49,59,53,44,44],repeatRows=1)
t.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,0),NAVY),("GRID",(0,0),(-1,-1),.35,colors.HexColor("#CFD8E1")),("VALIGN",(0,0),(-1,-1),"MIDDLE"),("ALIGN",(1,1),(-1,-1),"CENTER"),("LEFTPADDING",(0,0),(-1,-1),5),("RIGHTPADDING",(0,0),(-1,-1),5),("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5),("ROWBACKGROUNDS",(0,1),(-1,-1),[colors.white,PALE])]))
story += [t, Spacer(1,7), metric_chart(), mcc_chart()]
story += [P("Observations", "H1Custom"), P("Logistic Regression gave the strongest results in this test split: accuracy 0.9825, AUC 0.9954, F1 0.9861, and MCC 0.9623. RBF SVM was also close on several scores. KNN had the highest recall for benign cases (0.9722). Decision Tree and Gaussian Naive Bayes had the lowest MCC scores. These results come from one split, so repeated cross-validation could give a more reliable comparison. I should also check recall for malignant cases, because missing a malignant case matters.")]
story += [PageBreak(), P("Execution evidence and submission details", "TitleCustom"), P("Execution instructions", "H1Custom"), P("Install dependencies with <font name='Courier'>python -m pip install -r requirements.txt</font>, then run <font name='Courier'>python model/model_comparison.py</font>. The script writes the complete dataset CSV, held-out test_data.csv, model_metrics.csv, and comparison graphs into the project folder. The held-out CSV contains 114 rows from the stratified test split.")]
story += [P("Dataset source", "H1Custom"), P("UCI Machine Learning Repository: Wisconsin Diagnostic Breast Cancer dataset. The experiment used the canonical dataset bundled with scikit-learn.")]
story += [P("GitHub Repository Link", "H1Custom"), P("https://github.com/2026ct05170-pixel/ml-assignment2","BodyCustom")]
story += [P("BITS Virtual Lab execution screenshot", "H1Custom")]
img=Image(str(SHOT),width=175*mm,height=49.3*mm)
img.hAlign="CENTER"
story += [img, P("This screenshot is from the BITS Virtual Lab run. It shows the class counts and results for all six models.","CaptionCustom")]

doc=SimpleDocTemplate(str(OUT),pagesize=A4,rightMargin=16*mm,leftMargin=16*mm,topMargin=15*mm,bottomMargin=22*mm,title="Machine Learning Assignment 2 Classification Results",author="")
doc.build(story,onFirstPage=footer,onLaterPages=footer)
print(OUT)
