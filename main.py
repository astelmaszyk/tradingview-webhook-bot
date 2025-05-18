from fastapi import FastAPI, Request
import uvicorn

app = FastAPI()

@app.post("/webhook")
async def webhook(request: Request):
    try:
        data = await request.json()
        print("Alert received:", data)
        return {"status": "ok"}
    except Exception as e:
        print("Error parsing webhook:", e)
        return {"status": "error", "details": str(e)}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=10000)
    
