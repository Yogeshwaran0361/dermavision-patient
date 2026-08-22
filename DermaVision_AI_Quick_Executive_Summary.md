# ⚡ DERMAVISION AI — QUICK FULL STACK & WORKFLOW EXECUTIVE SUMMARY

**Institution**: Kongu Engineering College, Perundurai | **Dept**: CSE  
**Project**: DERMAVISION AI — AI-Powered Skin Disease Screening & Doctor Consultation  
**Team**: BYTEPRENEURS (Lead: Yogesh) | **Date**: 20 August 2026  
**Tagline**: *"SCAN ➔ UNDERSTAND ➔ BOOK ➔ CONSULT"*  

---

## 🛠️ 1. FULL STACK TECHNOLOGY MATRIX

```text
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                                 FULL STACK ARCHITECTURE                                 │
├───────────────────┬───────────────────┬───────────────────┬────────────────────────────┤
│   FRONTEND STACK  │   BACKEND STACK   │   AI / ML STACK   │      DATABASE & CLOUD      │
├───────────────────┼───────────────────┼───────────────────┼────────────────────────────┤
│ • React 18        │ • Python 3.11     │ • PyTorch 2.x     │ • Firebase Authentication  │
│ • TypeScript 5.5  │ • FastAPI         │ • EfficientNet-B0 │ • Cloud Firestore          │
│ • Tailwind CSS 3.4│ • Uvicorn ASGI    │ • 153 Classes     │ • Firebase Storage         │
│ • Lucide Icons    │ • Pydantic        │ • Torchvision     │ • LocalStorage Sync        │
│ • Vite 6 Bundler  │ • RESTful APIs    │ • PIL & NumPy     │ • Cloudflare Tunnels       │
└───────────────────┴───────────────────┴───────────────────┴────────────────────────────┘
```

| Layer | Primary Technology | Specific Usage & Purpose |
| :--- | :--- | :--- |
| **User Interface** | **React 18 & TypeScript** | Component-based patient app (`techno/frontend`) and standalone doctor workspace (`doctorweb`). |
| **Styling & Icons** | **Tailwind CSS & Lucide** | Modern glassmorphism UI layouts, responsive design, and vector icon system. |
| **Build & Bundler** | **Vite 6** | Lightning-fast HMR dev server and optimized production asset compiler. |
| **API Server** | **FastAPI & Uvicorn** | High-performance Python ASGI backend server handling image inference requests on port 8000. |
| **AI Classifier** | **PyTorch & EfficientNet-B0** | Deep learning model (`trained_skin_model.pth`) trained across **153 skin condition classes**. |
| **Normal Skin Class**| **Class Index 101** | `"Normal / Healthy Skin (Benign Feature)"` class trained directly to evaluate healthy skin. |
| **Database** | **Cloud Firestore** | NoSQL realtime collections (`users`, `user_appointments`, `user_notifications`, `consultations`). |
| **Authentication** | **Firebase Auth** | Email/Password and Google OAuth Sign-In session management. |
| **Audio Synthesizer**| **Web Audio API** | Synthesizes a loud 2-tone chime (`AudioContext`) 2 hours prior to scheduled doctor appointments. |
| **Public Tunnels** | **Cloudflare Tunnels** | Account-less SSL tunnels (`cloudflared`) enabling secure mobile access over 4G/5G data. |

---

## 🔄 2. FAST 5-STEP END-TO-END WORKFLOW

```text
STEP 1: PATIENT INPUT
📷 Capture skin photo via camera or upload file ➔ Run blur, brightness & focus quality check

STEP 2: PYTORCH AI INFERENCE
🧠 Image resized (224x224) & normalized ➔ PyTorch model computes Softmax probabilities across 153 classes

STEP 3: DYNAMIC REPORT GENERATION
📄 100% Model-Driven Report generated ➔ Branch 1 (Class 101 Healthy) vs Branch 2 (Specific Disease)

STEP 4: REPORT-LINKED APPOINTMENT BOOKING
📅 Patient selects Date & Time slot ➔ Binds appointment to Report ID in Firestore (user_appointments)

STEP 5: DOCTOR PORTAL & GOOGLE MEET
🩺 Doctor receives appointment ➔ 2-Hour Audio Chime ➔ Doctor starts real Google Meet ➔ Patient joins
```

---

## 📋 3. CORE CAPABILITIES AT A GLANCE

### 📱 Patient Portal Features:
- **✓ Secure Auth**: Email/Password & Google Sign-In.
- **✓ Image Validation**: Automated blur, focus, brightness, and resolution check.
- **✓ AI Screening**: PyTorch 153-class cutaneous pattern evaluation.
- **✓ Dynamic Reports**: Condition-specific clinical advice, symptoms, and care guidance.
- **✓ Report PDF Export**: One-click download of screening report.
- **✓ Multilingual UI**: Toggle between English, Tamil, and Hindi.
- **✓ Appointment Booking**: Direct scheduling linked to scan report ID.
- **✓ Real-Time Alerts**: Doctor-started Google Meet notification banner with sound chime.

### 🩺 Doctor Portal Features:
- **✓ Doctor Workspace**: Filterable patient queue (All, High Risk, Pending, Completed).
- **✓ Appointments Manager**: Filter schedule by `ALL`, `TODAY`, `UPCOMING`, `COMPLETED`, `CANCELLED`.
- **✓ Screening Telemetry**: Review patient lesion photo, AI prediction, and confidence score.
- **✓ 2-Hour Reminders**: Visual banner and Web Audio API chime played 2 hours prior to call time.
- **✓ Real Google Meet**: Doctor inputs/launches real meeting link.
- **✓ Targeted Isolation**: Notification sent strictly to `appointment.patientId`.
- **✓ Task Completion**: Mark appointment completed and issue prescriptions.

---

## 🔒 4. KEY ARCHITECTURAL GUARANTEES

1. **Zero Fake Predictions**: Predictions are 100% driven by model softmax outputs. Zero hardcoded disease names or filename heuristics.
2. **Normal Skin Class**: Healthy skin is evaluated by trained Class Index 101 (`"Normal / Healthy Skin"`).
3. **Deterministic Consultation Rule**:
   `"Same Appointment  |  Same Patient  |  Same Real Meeting URL"`
