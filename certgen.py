#!/usr/bin/env python3
"""Certificates for the NAVKIS embedded systems workshop.

Usage:  python3 certgen.py gradebook.csv out_dir [--hod "Dr. X Y"] [--sdc "Dr. A B"] [--sdc-title "..."] [--sample]
The CSV is the Gradebook tab exported from the Google Sheet (File > Download > CSV).
Columns used: Name, USN, Total, Rating, Certificate No.
Writes one PDF per student plus ALL_certificates.pdf for printing.
"""
import csv, os, sys, argparse, math
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor

HERE = os.path.dirname(os.path.abspath(__file__))
F = os.path.join(HERE, "fonts")
for name, file in [("Gar", "EBGaramond-Regular.ttf"), ("GarSB", "EBGaramond-SemiBold.ttf"), ("GarB", "EBGaramond-Bold.ttf"),
                   ("GarI", "EBGaramond-Italic.ttf"), ("Script", "GreatVibes-Regular.ttf")]:
    pdfmetrics.registerFont(TTFont(name, os.path.join(F, file)))

NAVY, TEAL, GOLD, INK, MUTE = HexColor("#14213D"), HexColor("#0B7F6E"), HexColor("#B8862B"), HexColor("#22293A"), HexColor("#5A6780")
W, H = landscape(A4)

RATINGS = {  # rating -> (stars, certificate title, appreciation line)
    "Outstanding": (5, "Certificate of Excellence",
                    "In appreciation of exceptional skill in embedded programming and an outstanding solution to the Smart Street Light design challenge."),
    "Excellent": (4, "Certificate of Achievement",
                  "In appreciation of excellent performance across the hands-on labs and the design challenge."),
    "Very Good": (3, "Certificate of Achievement",
                  "In appreciation of very good performance and steady progress through the hands-on labs."),
    "Good": (2, "Certificate of Merit",
             "In appreciation of good effort and active participation in the hands-on labs."),
    "Participated": (1, "Certificate of Participation",
                     "In appreciation of participation in the hands-on labs."),
}

def star(c, cx, cy, r, filled):
    pts = []
    for i in range(10):
        a = math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.42
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    p = c.beginPath(); p.moveTo(*pts[0])
    for q in pts[1:]: p.lineTo(*q)
    p.close()
    c.setStrokeColor(GOLD); c.setLineWidth(1.2); c.setFillColor(GOLD)
    c.drawPath(p, fill=1 if filled else 0, stroke=1)

def wrap(c, text, font, size, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if c.stringWidth(t, font, size) <= width: cur = t
        else: lines.append(cur); cur = w
    if cur: lines.append(cur)
    return lines

def center_rich(c, y, parts, size):
    """parts = [(text, font, colour)] drawn centred on one line"""
    total = sum(c.stringWidth(t, f, size) for t, f, _ in parts)
    x = (W - total) / 2
    for t, f, col in parts:
        c.setFont(f, size); c.setFillColor(col); c.drawString(x, y, t); x += c.stringWidth(t, f, size)

def page(c, s, hod, sdc="Dr. Nandeesh G S", sdct="Convener, Skill Development Cell", sample=False):
    rating = s["Rating"].strip() if s.get("Rating") else "Participated"
    if rating not in RATINGS: rating = "Participated"
    stars, title, appreciation = RATINGS[rating]
    # frame
    c.setFillColor(HexColor("#FBFAF6")); c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setStrokeColor(NAVY); c.setLineWidth(6); c.rect(22, 22, W - 44, H - 44)
    c.setStrokeColor(GOLD); c.setLineWidth(1.4); c.rect(34, 34, W - 68, H - 68)
    for x, y in [(34, 34), (W - 34, 34), (34, H - 34), (W - 34, H - 34)]:
        c.setFillColor(GOLD); c.circle(x, y, 4, fill=1, stroke=0)
    # header
    c.setFillColor(MUTE); c.setFont("GarSB", 11.5)
    c.drawCentredString(W / 2, H - 70, "SKILL DEVELOPMENT CELL & DEPARTMENT OF ECE  ·  NAVKIS COLLEGE OF ENGINEERING, HASSAN")
    c.setFillColor(NAVY); c.setFont("GarB", 38); c.drawCentredString(W / 2, H - 120, title)
    c.setStrokeColor(GOLD); c.setLineWidth(1); c.line(W / 2 - 120, H - 134, W / 2 + 120, H - 134)
    # body
    c.setFillColor(INK); c.setFont("GarI", 16); c.drawCentredString(W / 2, H - 170, "This is to certify that")
    name = s["Name"].strip()
    size = 46
    while c.stringWidth(name, "Script", size) > W - 220 and size > 28: size -= 2
    c.setFillColor(NAVY); c.setFont("Script", size); c.drawCentredString(W / 2, H - 222, name)
    usn = s.get("USN", "").strip()
    if usn:
        c.setFillColor(MUTE); c.setFont("GarSB", 13); c.drawCentredString(W / 2, H - 246, f"USN: {usn}")
    c.setFillColor(INK); c.setFont("Gar", 16)
    body = ("successfully took part in the one-day hands-on workshop “From Code to Silicon: Blink. Sense. Connect.” "
            "on embedded systems with the ESP32 microcontroller, held on 25 November 2026.")
    y = H - 282
    for ln in wrap(c, body, "Gar", 16, W - 240):
        c.drawCentredString(W / 2, y, ln); y -= 21
    total = s.get("Total", "").strip()
    y -= 8
    parts = [("Performance rating: ", "Gar", INK), (rating.upper(), "GarB", TEAL)]
    if total:
        try: parts.append((f"   ·   Score {float(total):.0f}/100", "Gar", INK))
        except ValueError: pass
    center_rich(c, y, parts, 17)
    for i in range(5):
        star(c, W / 2 - 56 + i * 28, y - 26, 10, i < stars)
    y -= 58
    c.setFillColor(MUTE); c.setFont("GarI", 14.5)
    for ln in wrap(c, appreciation, "GarI", 14.5, W - 300):
        c.drawCentredString(W / 2, y, ln); y -= 18
    # signatures
    sy = 104
    for cx, who, roles in [(W * 0.2, "Dr. Sathisha R N", ["Resource Person", "Assistant Professor, Dept. of ETE", "Siddaganga Institute of Technology, Tumakuru"]),
                           (W * 0.5, sdc, [sdct, "NAVKIS College of Engineering, Hassan"]),
                           (W * 0.8, hod, ["Professor & HOD, Dept. of ECE", "NAVKIS College of Engineering, Hassan"])]:
        c.setStrokeColor(INK); c.setLineWidth(0.8); c.line(cx - 115, sy + 18, cx + 115, sy + 18)
        c.setFillColor(INK); c.setFont("GarB", 13.5); c.drawCentredString(cx, sy, who)
        c.setFillColor(MUTE); c.setFont("Gar", 10.5)
        for k, r in enumerate(roles): c.drawCentredString(cx, sy - 14 - 13 * k, r)
    cert = s.get("Certificate No", "").strip()
    c.setFillColor(MUTE); c.setFont("Gar", 9.5)
    if cert: c.drawString(48, 44, f"Certificate No. {cert}")
    c.drawRightString(W - 48, 44, "Hassan, 25 November 2026")
    if sample:
        c.saveState(); c.setFillColor(HexColor("#C2264B")); c.setFillAlpha(0.12); c.setFont("GarB", 120)
        c.translate(W / 2, H / 2); c.rotate(20); c.drawCentredString(0, -40, "SAMPLE"); c.restoreState()
    c.showPage()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("csv"); ap.add_argument("out")
    ap.add_argument("--hod", default="Dr. Manjunath D V")
    ap.add_argument("--sdc", default="Dr. Nandeesh G S")
    ap.add_argument("--sdc-title", default="Convener, Skill Development Cell")
    ap.add_argument("--sample", action="store_true")
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    rows = [r for r in csv.DictReader(open(a.csv, encoding="utf-8-sig")) if r.get("Name", "").strip()]
    allc = canvas.Canvas(os.path.join(a.out, "ALL_certificates.pdf"), pagesize=landscape(A4))
    allc.setTitle("NAVKIS embedded systems workshop certificates")
    for r in rows:
        fn = "".join(ch if ch.isalnum() else "_" for ch in (r.get("USN") or r["Name"]).strip())
        one = canvas.Canvas(os.path.join(a.out, f"{fn}.pdf"), pagesize=landscape(A4))
        one.setTitle(f"Certificate - {r['Name'].strip()}")
        page(one, r, a.hod, a.sdc, a.sdc_title, a.sample); one.save()
        page(allc, r, a.hod, a.sdc, a.sdc_title, a.sample)
    allc.save()
    print(f"{len(rows)} certificates written to {a.out}")

if __name__ == "__main__":
    main()
