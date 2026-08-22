# DermaVision AI — Clinical Skin Disease Classifier (v2.0)

A simple, real, working AI skin-scanning website powered by fine-tuned PyTorch ResNet50 deep learning across 10 target skin disease classes.

## Features
- **Frontend**: React + TypeScript + Vite + Tailwind CSS (`frontend/`)
- **Backend**: FastAPI + PyTorch + OpenCV Quality Checker (`backend/`)
- **Multi-Language (i18n)**: English, Tamil, Hindi switcher
- **Image Quality Check**: Automated blur, focus, lighting, and resolution validation before classification
- **Real AI Inference**: Zero dummy/fake scores — runs PyTorch model checkpoint (`skin_classifier.pth`) directly

## How to Run

### 1. Start FastAPI Backend Server
```powershell
& "C:\Users\yoges\Downloads\DermaVision-AI\.python311\python.exe" "c:\Users\yoges\Downloads\techno\backend\main.py"
```

### 2. Start React Frontend Development Server
```powershell
cd c:\Users\yoges\Downloads\techno\frontend
npm install
npm run dev
```

Open `http://localhost:5173` in your browser to launch the web application.
