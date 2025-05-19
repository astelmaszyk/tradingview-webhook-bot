from fastapi import FastAPI, Request
import uvicorn
import logging
import json
from datetime import datetime

# Konfiguracja logowania
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# 🔐 TOKEN zabezpieczający
SECRET_TOKEN = "moj_super_tajny_token"

app = FastAPI()

@app.post("/webhook")
async def webhook(request: Request):
    try:
        data = await request.json()

        # Weryfikacja tokena
        if data.get("token") != SECRET_TOKEN:
            logging.warning(f"Unauthorized attempt: {data}")
            return {"status": "unauthorized"}

        # Log do terminala
        logging.info(f"Alert received: {data}")

        # Zapis do pliku
        timestamp = datetime.utcnow().isoformat()
        with open("alerts.log", "a") as f:
            f.write(f"{timestamp} - {json.dumps(data)}\n")

        return {"status": "ok"}

    except Exception as e:
        logging.error(f"Error parsing webhook: {e}")
        return {"status": "error", "details": str(e)}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=10000)
