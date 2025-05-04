from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import uvicorn, stripe, os
from dotenv import load_dotenv

# Cargar claves desde .env
load_dotenv()
stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

# Configuración base
app = FastAPI()
app.add_middleware(CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Archivos estáticos
app.mount("/static", StaticFiles(directory="./front"), name="static")

# Jinja2 templates
templates = Jinja2Templates(directory="front")

# Ruta principal que renderiza la plantilla con la PUBLIC KEY
@app.get("/", response_class=HTMLResponse)
async def serve_index(request: Request):
    stripe_public_key = os.getenv("STRIPE_PUBLIC_KEY")
    return templates.TemplateResponse("index.html", {
        "request": request,
        "stripe_public_key": stripe_public_key
    })

# Endpoint de pago
class PaymentRequest(BaseModel):
    amount: int

@app.post("/create-payment-intent")
async def create_payment_intent(request: PaymentRequest):
    try:
        payment_intent = stripe.PaymentIntent.create(
            amount=request.amount,
            currency="usd",
        )
        print("se acredito el pago por: ",payment_intent.amount, "USD")
        return {"clientSecret": payment_intent.client_secret}
    except Exception as e: 
        print("No se pudo acreditar el pago")
        return {"Error": str(type(e).__name__)}

if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)
