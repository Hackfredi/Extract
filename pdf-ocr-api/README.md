# 📄 PDF/Image Data Extractor API

This is a lightweight Flask API wrapped in Docker to extract **selected fields** from PDF or image files. It’s designed to be used as a microservice with tools like **n8n**, running inside **Portainer**.

---

## 🚀 Features

- Extracts specific data from PDF or image files
- Returns clean JSON output
- Dockerized for deployment
- Easy integration with automation tools (e.g., n8n)

---

## 🧱 Project Structure

pdf-ocr-api/
├── app/
│ ├── main.py
│ ├── extract.py
│ └── requirements.txt
├── Dockerfile
├── README.md
├── .gitignore
