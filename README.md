# Paperframe: Automatic Question Paper Generator

Paperframe is a Flask-based web application that automates the creation of question papers by extracting questions from uploaded PDF files. It supports both text-based and scanned PDFs using Optical Character Recognition (OCR), randomly selects questions based on user preferences, and generates a well-formatted downloadable PDF.

---

## 🎯 Project Objective

To reduce the manual effort involved in question paper preparation by providing an automated, reliable, and customizable system for educators and institutions.

---

## 🚀 Key Features

* Upload up to **three PDF files** containing questions
* Supports **text-based PDFs** and **scanned image PDFs** (OCR enabled)
* Automatic **question identification** using pattern matching
* **Randomized question selection** for unbiased papers
* Customizable question paper structure
* Generates a **professional PDF output**
* Secure **user authentication** and session management

---

## 🛠️ Tech Stack

### Backend

* Python
* Flask
* MySQL

### OCR & PDF Processing

* Tesseract OCR (via pytesseract)
* PyMuPDF (fitz)
* PyPDF2 / PDFMiner
* ReportLab / FPDF

### Frontend

* HTML
* CSS
* JavaScript

---

## ⚙️ System Requirements

### Hardware

* Processor: Intel i5 (2.53 GHz or above)
* RAM: 4 GB or higher
* Storage: Minimum 30 GB

### Software

* OS: Windows 8 or above
* Python 3.8+
* MySQL Server
* Tesseract OCR Engine

---

## 📂 Project Structure

```
Paperframe/
│── app.py
│── templates/
│   ├── login.html
│   ├── dashboard.html
│   └── upload.html
│── static/
│   ├── css/
│   └── js/
│── uploads/
│── generated_papers/
│── requirements.txt
│── README.md
```



⭐ If you find this project useful, consider starring the repository.
