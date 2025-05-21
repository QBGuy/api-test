from fastapi import FastAPI, Request, HTTPException
import httpx, os

EXTERNAL_URL = "https://postman-echo.com/post"
BEARER_TOKEN = os.getenv("API_TOKEN", "FAKE-TOKEN-123")   # demo secret

app = FastAPI()

@app.post("/monday-webhook")
async def from_monday(req: Request):
    body = await req.json()            # raw monday event
    async with httpx.AsyncClient(timeout=10) as client:
        res = await client.post(
            EXTERNAL_URL,
            json={"monday": body},     # transform if you like
            headers={"Authorization": f"Bearer {BEARER_TOKEN}"}
        )
    if res.status_code != 200:
        raise HTTPException(500, "external API error")
    return {"ok": True}
