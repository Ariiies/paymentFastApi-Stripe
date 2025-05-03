# 💳 FastAPI + Stripe Payment Example

This is a **mini project** that integrates **Stripe** as a payment gateway using **FastAPI** for the backend and HTML + JavaScript for the frontend. The Stripe public key is securely passed to the client using **Jinja2Templates**, avoiding direct exposure in static files.

## 📁 Project Structure

```
project/
├── front/
│   ├── index.html
│   └── hooks/
│       └── script.js
├── .env
├── main.py
└── README.md
```

## 🔐 Environment Variables (`.env`)

```env
STRIPE_SECRET_KEY=your_stripe_secret_key_here
STRIPE_PUBLIC_KEY=your_stripe_public_key_here
```

> Make sure this file is included in your `.gitignore` to avoid exposing sensitive keys.

## 🧪 Requirements

- Python 3.8+
- Stripe account
- Install dependencies:
  
```bash
pip install -r requirements.txt
```

## 🚀 How to Run

```bash
uvicorn main:app --reload
```

Then open [http://localhost:8000](http://localhost:8000) in your browser.

## 💡 How It Works

- **Backend**: FastAPI uses Jinja2 to render `index.html`, injecting the public key from the environment
- **Frontend**: Uses `script.js` to handle Stripe Elements and payment flow
- **Security**: Keys are managed through environment variables, never exposed directly

## ✅ Features

- Clean separation between backend and frontend
- Securely injected public Stripe key
- Ideal as a base for real-world apps

## 📄 License

Free to use for educational or commercial purposes.
