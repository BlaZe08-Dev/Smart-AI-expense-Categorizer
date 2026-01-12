🧠 Smart AI Expense Categorizer & Analytics Dashboard

A Smart AI-powered expense categorization system that automatically extracts transactions from PDFs, categorizes expenses using a hybrid rule-based + ML pipeline, and visualizes insights through an interactive analytics dashboard.

🚀 Features
🔹 Backend (FastAPI)
  * 📄 PDF bank statement ingestion
  * 🧠 AI + rule-based expense categorization
  * ✏️ User category overrides (learning from corrections)
  * 📊 Analytics generation:
  * Category totals
  * Monthly trends
  * Merchant insights
  * ⚡ High-performance REST AP

🔹 Frontend (React + Vite)
  📈 Interactive dashboard
  🥧 Category pie chart
  📆 Monthly spending trends
  🏪 Top merchants view
  ✏️ Edit categories in real time
  📱 Responsive UI (desktop + mobile)

🏗️ Tech Stack
Frontend:
  React
  Vite
  JavaScript
  Chart.js / Recharts
Backend:
  Python
  FastAPI
  Uvicorn
  Scikit-learn
  Joblib

How to run locally 
For Backend:
cd Backend
uvicorn Backend.main:app --reload

For Frontend:
cd Frontend/frontend
npm install
npm run dev
