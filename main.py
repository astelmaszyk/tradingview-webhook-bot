from fastapi import FastAPI, Request
import json

app = FastAPI()

@app.post("/webhook")
async def webhook(request: Request):
    data = await request.json()
    print("Alert received:", data)
    return {"status": "ok"}
