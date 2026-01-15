# 💰 AI Smart Expense Analyzer

An AI-powered web app that analyzes bank statement PDFs and provides
smart insights into spending habits.

## 🚀 Features
- Upload password-protected bank PDFs
- Automatic transaction extraction
- AI-based expense categorization
- Editable categories with live updates
- Interactive pie charts & insights
- Fully responsive (mobile + desktop)

## 🧠 Tech Stack
- Frontend: React, Recharts
- Backend: FastAPI, Python
- PDF Parsing: pdfplumber + Tabula
- AI: Custom ML categorization pipeline

## 🖥️ How to Run Locally

### Backend
```bash
cd Real Project
pip install -r requirements.txt
uvicorn Backend.main:app --reload

### Frontend
```bash
cd frontend
npm install
npm run dev
📍 Frontend URL: http://localhost:5173
