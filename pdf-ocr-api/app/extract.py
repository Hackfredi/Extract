import fitz  # PyMuPDF
import pytesseract
from pdf2image import convert_from_path
import cv2
import numpy as np
import pdfplumber
import re
import sys
import os
import json


def is_scanned(pdf_path):
    try:
        doc = fitz.open(pdf_path)
        return not doc[0].get_text().strip()
    except Exception:
        return True


def extract_text_textbased(pdf_path):
    doc = fitz.open(pdf_path)
    return "\n".join(page.get_text() for page in doc)


def extract_text_scanned(pdf_path):
    images = convert_from_path(pdf_path, dpi=300)
    text = ""
    for img in images:
        gray = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2GRAY)
        _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
        text += pytesseract.image_to_string(thresh) + "\n"
    return text


def extract_text_from_image(image_path):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    return pytesseract.image_to_string(thresh)


def extract_tables(pdf_path):
    tables_data = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            tables = page.extract_tables()
            for table in tables:
                cleaned_table = [
                    [cell.strip() if cell else "" for cell in row]
                    for row in table
                ]
                tables_data.append(cleaned_table)
    return tables_data


def extract_fields(text):
    data = {}

    name_match = re.search(r"(?:Name|Purchased By|Ship To)[:\- ]+([^\n,]+)", text, re.IGNORECASE)
    email_match = re.search(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", text)
    phone_match = re.search(r"(?:Phone|Tel)[:\- ]+(\+?\d[\d\s\-()]{6,})", text, re.IGNORECASE)
    invoice_match = re.search(r"(?:Invoice\s*#|Invoice Number)[:\- ]+(\d+)", text, re.IGNORECASE)
    total_match = re.search(r"(?:Total\s*Amount|Total|Amount Due|Due Amount)[:\- ₹$]*([\d,]+(?:\.\d{1,2})?)", text, re.IGNORECASE)
    date_match = re.search(r"(?:Due Date|Date|Dated)[:\- ]+([\d]{1,2}[/\-.][\d]{1,2}[/\-.][\d]{2,4})", text, re.IGNORECASE)

    if name_match:
        data["name"] = name_match.group(1).strip()
    if email_match:
        data["email"] = email_match.group(0)
    if phone_match:
        data["phone"] = phone_match.group(1).strip()
    if invoice_match:
        data["invoice_id"] = invoice_match.group(1)
    if total_match:
        data["total"] = total_match.group(1)
    if date_match:
        data["due_date"] = date_match.group(1)

    return data


def main(input_path):
    if not os.path.exists(input_path):
        print(json.dumps({"error": "File does not exist."}))
        return

    ext = os.path.splitext(input_path)[-1].lower()

    if ext in [".png", ".jpg", ".jpeg"]:
        print("[INFO] Image file detected.")
        text = extract_text_from_image(input_path)
        scanned = True
        tables = []
    elif ext == ".pdf":
        scanned = is_scanned(input_path)
        if scanned:
            print("[INFO] Scanned PDF detected — using OCR.")
            text = extract_text_scanned(input_path)
        else:
            print("[INFO] Text-based PDF detected.")
            text = extract_text_textbased(input_path)
        tables = extract_tables(input_path)
    else:
        print(json.dumps({"error": "Unsupported file type."}))
        return

    fields = extract_fields(text)

    result = {
        "is_scanned": scanned,
        "extracted_fields": fields
    }

    if tables:
        result["tables"] = tables

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python extract.py <path_to_pdf_or_image>")
    else:
        main(sys.argv[1])
