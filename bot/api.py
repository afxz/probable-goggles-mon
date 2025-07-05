
# Monetag postback endpoint for ad event tracking
from fastapi import FastAPI, Request, status
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from .db import add_points
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve the webapp directory as static files
webapp_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../webapp'))
app.mount("/webapp", StaticFiles(directory=webapp_dir, html=True), name="webapp")

# Serve index.html at root
@app.get("/")
def root():
    return FileResponse(os.path.join(webapp_dir, "index.html"))

@app.post("/api/monetag_event")
async def monetag_event(request: Request):
    data = await request.json()
    # Extract Monetag macros (use .get for safety)
    telegram_id = data.get("telegram_id")
    app_id = data.get("app_id")
    zone_id = data.get("zone_id")
    sub_zone_id = data.get("sub_zone_id")
    event_type = data.get("event_type")
    reward_event_type = data.get("reward_event_type")
    estimated_price = data.get("estimated_price", 0.0)
    ymid = data.get("ymid")
    request_var = data.get("request_var")

    # Only reward if event is paid and telegram_id is present
    if telegram_id and reward_event_type == "yes":
        try:
            telegram_id = int(telegram_id)
        except Exception:
            return JSONResponse({"status": "error", "reason": "Invalid telegram_id"}, status_code=400)
        reward_amount = float(estimated_price) if estimated_price else 0.25
        await add_points(telegram_id, reward_amount)
        return JSONResponse({
            "status": "ok",
            "rewarded": reward_amount,
            "telegram_id": telegram_id,
            "event_type": event_type,
            "zone_id": zone_id
        }, status_code=status.HTTP_200_OK)
    return JSONResponse({"status": "ignored", "reason": "Not a paid event or missing telegram_id"}, status_code=status.HTTP_200_OK)
