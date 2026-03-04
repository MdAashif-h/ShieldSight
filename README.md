# 🛡️ ShieldSight - AI-Powered Phishing Detection

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![React](https://img.shields.io/badge/React-18.2-61DAFB.svg)
![TypeScript](https://img.shields.io/badge/TypeScript-5.0-3178C6.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104-009688.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

**ShieldSight** is an advanced phishing detection system leveraging **XGBoost** machine learning with **SHAP** (SHapley Additive exPlanations) for transparent, high-accuracy threat analysis. It achieves **95%+ accuracy** with a low false positive rate.

## ✨ Features

- **🤖 AI-Powered Detection**: Real-time URL analysis using a trained XGBoost model.
- **📊 SHAP Explainability**: Visualizes *why* a URL is flagged (e.g., suspicious domain length, obfuscation).
- **📁 Batch Processing**: Analyze bulk URLs via CSV upload with exportable results.
- **📈 History & Analytics**: Track past scans and view aggregate statistics.
- **🎨 Modern UI**: Responsive React dashboard with Dark/Light mode support.
- **📱 Mobile Optimized**: Fully functional on mobile devices with camera-based QR scanning.
- **🔐 Secure Architecture**: Firebase Authentication and encrypted data handling.

## 🚀 Live Demo

- **Frontend**: [https://sentinelx.vercel.app](https://sentinelx.vercel.app)
- **API Documentation**: [https://api.sentinelx.tech/docs](https://api.sentinelx.tech/docs)

## 🛠️ Tech Stack

### Backend
- **Framework**: FastAPI (Python)
- **ML Engine**: XGBoost, Scikit-learn, SHAP
- **Data Processing**: Pandas, NumPy
- **Deployment**: Railway / Docker

### Frontend
- **Framework**: React 18 (Vite)
- **Language**: TypeScript
- **Styling**: Tailwind CSS, Framer Motion
- **State Management**: Zustand / Context API
- **Authentication**: Firebase Auth

## 📦 Installation & Setup

### Prerequisites
- Python 3.9+
- Node.js 16+
- Git

### 1. Clone the Repository
```bash
git clone https://github.com/MdAashif-h/ShieldSight.git
cd ShieldSight
```

### 2. Backend Setup
```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the server
uvicorn app.main:app --reload
```
The API will be available at `http://localhost:8000`.

### 3. Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Create .env file
# Add your Firebase config keys (VITE_FIREBASE_API_KEY, etc.)

# Run development server
npm run dev
```
The app will be available at `http://localhost:5173`.

## 📊 Model Performance

Evaluated on the **PhiUSIIL** and **Alexa Top-1M** datasets:

- **Accuracy**: 95.2%
- **Precision**: 95.1%
- **Recall**: 95.3%
- **False Positive Rate**: < 4%

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📧 Contact

- **GitHub**: [MdAashif-h](https://github.com/MdAashif-h)
- **Email**: faree.aashif@gmail.com

---
Made with ❤️ by MdAashif-h