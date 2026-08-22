# 📘 DERMAVISION AI — COMPLETE FULL PROJECT TECHNICAL DOCUMENTATION

**Institution**: Kongu Engineering College, Perundurai  
**Department**: Department of Computer Science & Engineering (CSE)  
**Project Title**: DERMAVISION AI — AI-Powered Skin Disease Screening & Doctor Consultation Platform  
**Team Name**: BYTEPRENEURS  
**Project Lead**: Yogesh  
**Date**: 20 August 2026  
**Tagline**: *"SCAN ➔ UNDERSTAND ➔ BOOK ➔ CONSULT"*  

---

## 1. EXECUTIVE SUMMARY & PROJECT ABSTRACT

DermaVision AI is an end-to-end medical tele-dermatology platform designed to bridge the critical gap between initial skin concern awareness and professional clinical consultation. Utilizing deep learning computer vision algorithms trained across 153 skin condition classes, the platform provides automated, preliminary AI skin screening, dynamic condition-specific reports, normal/healthy skin detection, screening history tracking, patient appointment booking, and a dedicated doctor consultation workspace with integrated Google Meet video sessions.

### Key Objectives:
- **Assistive AI Screening**: Analyze uploaded or camera-captured skin photos to predict candidate conditions with confidence scores.
- **Normal Skin Recognition**: Identify benign/normal skin (Class Index 101) to reassure healthy users and promote preventive care.
- **Dynamic Report Generation**: Produce condition-specific clinical guidance based 100% on model outputs (zero hardcoded overrides).
- **Patient–Doctor Tele-Health**: Provide a seamless appointment scheduling and Google Meet consultation workflow.

---

## 2. SYSTEM ARCHITECTURE & THREE-TIER PARADIGM

DermaVision AI is built on a decoupled, three-tier modular architecture:

```text
┌─────────────────────────────────────────────────────────────────────────┐
│                      PATIENT WEB APPLICATION (React 18)                 │
│  - Landing Page & Authentication (Firebase Auth)                        │
│  - Camera Capture & Image Upload (Quality Checks)                       │
│  - Dynamic AI Clinical Report & PDF Exporter                            │
│  - Patient Appointment Manager & Meeting Launcher                       │
└────────────────────────────────────┬────────────────────────────────────┘
                                     │ REST APIs & Firestore SDK
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                      BACKEND SERVICES & CLOUD STORAGE                   │
│  - FastAPI Python ASGI Backend Server (Port 8000)                        │
│  - PyTorch Deep Learning Model Engine (trained_skin_model.pth)          │
│  - Firebase Cloud Firestore (users, user_appointments, notifications)   │
│  - Firebase Storage & Cloudflare HTTPS Tunnels                          │
└────────────────────────────────────┬────────────────────────────────────┘
                                     │ REST APIs & Firestore SDK
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                      DOCTOR PORTAL DASHBOARD (React 18)                 │
│  - Filterable Patient Queue & Telemetry Reviewer                        │
│  - Appointments Schedule Manager (All, Today, Upcoming)                 │
│  - 2-Hour Appointment Audio Chime & Visual Banner Alert                 │
│  - REAL Google Meet Tele-Health Session Launcher                        │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 3. DETAILED COMPONENT SPECIFICATIONS

### A. Patient Web Application (`techno/frontend`)
- **`src/pages/Home.tsx`**: Main entry interface with authentication state handler, project introduction, interactive feature grid, and scanner trigger.
- **`src/pages/Scanner.tsx`**: Image acquisition module supporting both live camera capture and file upload. Runs real-time blur, brightness, contrast, and focus quality checks before submitting to the AI model.
- **`src/pages/Report.tsx`**: Renders dynamic, condition-specific clinical screening reports. Features 100% model-driven predictions, top-3 candidates, risk level color coding, audio speech guide synthesis, PDF exporter, and a **"Consult Doctor"** action trigger.
- **`src/pages/Appointments.tsx`**: Dedicated patient page listing scheduled doctor appointments, current status (`Scheduled`, `Ready for Consultation`, `Completed`), and direct Google Meet join buttons.
- **`src/pages/History.tsx`**: Central repository storing past screening records with timestamped diagnostic summaries.
- **`src/components/BookAppointmentModal.tsx`**: Modal allowing patients to select consultation date and time, automatically binding the appointment to their report ID.
- **`src/components/AppointmentNotificationBanner.tsx`**: Global header notification banner providing 2-hour appointment reminders and doctor-started Google Meet alerts with Web Audio API chime.

### B. Standalone Doctor Portal (`doctorweb`)
- **`src/pages/DoctorDashboard.tsx`**: Attending doctor workspace with patient queue filtering (All, High Risk, Pending, Completed), scan specimen viewer, and diagnostic breakdown.
- **`src/pages/DoctorAppointments.tsx`**: Comprehensive appointment management interface. Displays patient details, linked AI report, date/time, 2-hour reminder banner, audio chime synthesizer, custom Google Meet launcher, and consultation completion buttons.
- **`src/components/DoctorNavbar.tsx`**: Workspace mode navigation bar for switching between Patient Queue, Appointments, and Doctor Profile.

---

## 4. AI / MACHINE LEARNING PIPELINE & MODEL SPECIFICATION

### A. Deep Learning Model Architecture
- **Framework**: PyTorch 2.x & Torchvision
- **Backbone**: **EfficientNet-B0** / **ResNet50** Convolutional Neural Network
- **Model Checkpoint**: `backend/trained_skin_model.pth`
- **Output Classes**: **153 trained dermatological condition classes**
- **Class Index 101**: `"Normal / Healthy Skin (Benign Feature)"`

### B. Preprocessing & Inference Pipeline Steps
1. **Image Input**: Photo received via HTTP POST `multipart/form-data`.
2. **Quality Check**: Validates focus (Laplacian variance), brightness, and resolution.
3. **Resizing**: Tensor resized to **224 × 224 pixels**.
4. **Normalization**: Applies ImageNet standard normalization:
   - Mean: `[0.485, 0.456, 0.406]`
   - Standard Deviation: `[0.229, 0.224, 0.225]`
5. **Model Forward Pass**: Computes raw logits $z_i$.
6. **Softmax Probabilities**: Applies $P(C_i) = \frac{{e^{{z_i}}}}{{\sum e^{{z_k}}}}$.
7. **Top Class Selection**: Identifies candidate class and probability score.

---

## 5. DATABASE SCHEMA & CLOUD FIRESTORE DATA MODEL

### A. `users` Collection
- `uid`: Unique User ID
- `name` & `email`: Patient contact info
- `role`: `'patient'` | `'doctor'`
- `preferredLanguage`: `'en'` | `'ta'` | `'hi'`

### B. `user_appointments` Collection
- `id`: Appointment ID (`APPT-timestamp-random`)
- `patientId`: Patient UID
- `patientName` & `patientEmail`: Patient details
- `reportId` & `scanId`: Linked screening report ID
- `diseaseName` & `confidence`: Primary AI prediction & confidence %
- `appointmentDate` & `appointmentTime`: Scheduled slot
- `appointmentStatus`: `'Scheduled'` | `'In Progress'` | `'Completed'` | `'Cancelled'`
- `meetingStatus`: `'NOT_STARTED'` | `'READY'` | `'COMPLETED'`
- `meetingUrl`: Real Google Meet URL initiated by doctor

### C. `user_notifications` Collection
- `id`: Notification ID
- `patientId`: Targeted patient UID
- `appointmentId`: Linked appointment ID
- `title` & `message`: Notification header & content
- `type`: `'APPOINTMENT_BOOKED'` | `'DOCTOR_STARTED_MEETING'`
- `read`: boolean

---

## 6. TELE-HEALTH & DOCTOR CONSULTATION WORKFLOW

The platform uses a deterministic appointment state machine:

```text
PATIENT SIDE                               DOCTOR PORTAL
────────────                               ─────────────
1. View Report & Click "Consult Doctor"
2. Select Date & Time slot
3. Booking saved to Firestore  ─────────►  1. Appears in Appointments Schedule
                                           2. 2-Hour Visual Alert & Sound Chime
                                           3. Review Patient Report & Telemetry
4. Receive Targeted Notification  ◄──────  4. Input Real Meet URL & Click "Start"
5. Click "Join Google Meet"    ─────────►  5. Conduct Live Video Session
                                           6. Mark Consultation Completed
```

### Security & Isolation Rule:
Notifications and Google Meet URLs are transmitted **strictly to `appointment.patientId`**. Patient A receives the alert; Patient B receives nothing.

---

## 7. COMPLETE TECHNOLOGIES & LIBRARIES SUMMARY

| Category | Technology / Library | Version / Detail |
| :--- | :--- | :--- |
| **Frontend Framework** | React | 18.3.1 |
| **Language** | TypeScript | 5.5.3 |
| **Styling** | Tailwind CSS | 3.4.1 |
| **Icons** | Lucide React | 0.344.0 |
| **Build Tool** | Vite | 6.4.3 |
| **Audio Synthesis** | Web Audio API | `AudioContext` Synthesizer |
| **Backend Language** | Python | 3.11 |
| **Backend Web Server** | FastAPI & Uvicorn | Asynchronous ASGI Server |
| **Deep Learning** | PyTorch & Torchvision | 2.2.0 |
| **Image Processing** | Pillow (PIL) & NumPy | 10.2.0 |
| **Authentication** | Firebase Auth | Google OAuth & Email/Password |
| **Cloud Database** | Cloud Firestore | NoSQL Realtime Collection Database |
| **Public HTTPS Tunnels** | Cloudflare Tunnels (`cloudflared`) | Account-less SSL Tunnels |

---

## 8. SUSTAINABLE DEVELOPMENT GOALS (SDGs)
- 🎯 **SDG 3: Good Health & Well-Being**: Early skin condition awareness, accessible preliminary screening, and rapid tele-health connectivity.
- 🎯 **SDG 9: Industry, Innovation & Infrastructure**: Cutting-edge AI computer vision applied to healthcare infrastructure.
