# 📄 PDF/Image Data Extractor API

A lightweight Flask-based API (Dockerized) for extracting specific fields from PDF or image files. Designed for microservice architecture, it integrates seamlessly with automation tools like [n8n](https://n8n.io) and runs smoothly inside environments such as Portainer.

---

## 🚀 Features

- 📄 Extracts selected data from PDF and image files  
- 🧼 Returns clean and structured JSON output  
- 🐳 Dockerized for easy deployment  
- 🔗 Built for easy integration with automation workflows (e.g., n8n)  
- ⚡ Fast, minimal, and ready for microservices  

---

## 🧱 Project Structure

pdf-ocr-api/
├── app/
│ ├── main.py # Flask app entry point
│ ├── extract.py # Logic for OCR and field extraction
│ └── requirements.txt # Python dependencies
├── Dockerfile # For containerizing the app
├── README.md # Project documentation
├── .gitignore # Ignore build and environment files
