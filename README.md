---
title: Image Data Extract Python
emoji: 📄
colorFrom: blue
colorTo: purple
sdk: docker
pinned: false
---

# Image Data Extract Python

AI-Powered OCR System for Handwritten and Printed Text Recognition

![Python](https://img.shields.io/badge/Python-3.11%20|%203.12%20|%203.13-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

**Developer:** [issu321](https://github.com/issu321)  
**Repository:** [https://github.com/issu321/Image-Data-Extract-Python](https://github.com/issu321/Image-Data-Extract-Python)

---

## Deploy on Hugging Face Spaces

1. Go to [huggingface.co/spaces](https://huggingface.co/spaces) and click **"Create new Space"**
2. Choose **Space name**, set **SDK** to **`Docker`**
3. In your local project folder, run:

```bash
git init
git remote add origin https://huggingface.co/spaces/<your-username>/image-data-extract-python
git add .
git commit -m "Deploy ready"
git push -u origin main
```

Hugging Face will auto-build the Docker image and launch your app at `https://<your-username>-image-data-extract-python.hf.space`

---

## Features

- **Multi Language OCR** — English, Hindi, Kannada
- **Handwriting Recognition**
- **Auto Language Detection**
- **Export TXT**
- **Dark Mode**
- **Crash-Safe Engines** — Tesseract primary, EasyOCR/PaddleOCR optional & isolated
- **Responsive Design**

---

## OCR Architecture

1. **Tesseract OCR** — Primary (stable, supports eng/hin/kan)
2. **EasyOCR** — Optional AI engine (subprocess-tested so crashes never kill the app)
3. **PaddleOCR** — Optional secondary engine
4. **OpenCV** — Preprocessing (grayscale, denoise, CLAHE, threshold, sharpen)

---

## Local Installation

```bash
bash install.sh        # Linux / macOS / Kali
# OR
install.bat            # Windows
```

```bash
source venv/bin/activate
python app.py
```

Open http://localhost:5000
