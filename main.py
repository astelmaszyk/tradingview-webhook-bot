from fastapi import FastAPI, Request
import uvicorn
import logging
import json
from datetime import datetime
from binance.client import Client
from dotenv import load_dotenv
import os

# Wczytaj zmienne środowiskowe
load_dotenv()
API_KEY = os.getenv("BINANCE_API_KEY")
API_SECRET = os.getenv("BINANCE_API_SECRET")

# Inicjalizacja klienta Binance
client = Client(API_KEY, API_SECRET)

# Konfiguracja logowania
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# 🔐 TOKEN zabezpieczający
SECRET_TOKEN = "moj_super_tajny_token"

app = FastAPI()

# 🔁 Funkcja do składania zleceń
def wykonaj_transakcje(symbol, kierunek):
    try:
        logging.info(f"🔁 Próba realizacji zlecenia: {kierunek} {symbol}")

        if kierunek == "BUY":
            order = client.order_market_buy(symbol=symbol, quantity=0.001)
        elif kierunek == "SELL":
            order = client.order_market_sell(symbol=symbol, quantity=0.001)
        else:
            logging.warning(f"Nieznany kierunek: {kierunek}")
            return

        logging.info(f"✅ Zlecenie zrealizowane: {order}")
    except Exception as e:
        logging.error(f"❌ Błąd przy składaniu zlecenia: {e}")

# 📩 Obsługa webhooka
@app.post("/webhook")
async def webhook(request: Request):
    try:
        data = await request.json()

        # Weryfikacja tokena
        if data.get("token") != SECRET_TOKEN:
            logging.warning(f"Unauthorized attempt: {data}")
            return {"status": "unauthorized"}

        logging.info(f"📩 Alert received: {data}")

        # Zapis do logu
        timestamp = datetime.utcnow().isoformat()
        with open("alerts.log", "a") as f:
            f.write(f"{timestamp} - {json.dumps(data)}\n")

        # Wykonanie transakcji na podstawie alertu
        message = data.get("message", "").upper()
        if message == "BUY":
            wykonaj_transakcje("BTCUSDT", "BUY")
        elif message == "SELL":
            wykonaj_transakcje("BTCUSDT", "SELL")
        else:
            logging.info("⚠️ Nieznany typ wiadomości — pomijam")

        return {"status": "ok"}

    except Exception as e:
        logging.error(f"❌ Error parsing webhook: {e}")
        return {"status": "error", "details": str(e)}

# Uruchomienie lokalne (Render tego nie używa)
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=10000)

