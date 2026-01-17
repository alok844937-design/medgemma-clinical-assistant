# MedGemma Clinical Assistant

## Overview
AI-powered clinical documentation assistant for healthcare providers and patients.

## Features
- Patient Mode: Simplifies medical jargon
- Doctor Mode: Structures clinical notes
- Real-time Processing
- Modern UI

## Quick Start

### Local Development
```bash
pip install -r requirements.txt
python app.py
```

### Docker Deployment
```bash
docker build -t medgemma-assistant .
docker run -p 5000:5000 medgemma-assistant
```

## Project Structure
```
medgemma_clinical_assistant/
├── app.py
├── requirements.txt
├── Dockerfile
├── README.md
├── prompts/
├── demo_data/
├── evaluation/
└── tests/
```

## Technology Stack
- Backend: Flask
- Frontend: HTML/CSS/JavaScript
- Deployment: Docker

## 🎥Demo Video
A 90-second walkthrough demonstrating:
- Offline execution 
- Passing automated tests 
- Patient and doctor workflows 

Demo script available in `demo/VIDEO_SCRIPT.md`.

## License
MIT License

# medgemma-clinical-assistant
Privacy-first offline clinical assistant using MedGemma (HAI-DEF) for structured notes and patient-friendly explanations.