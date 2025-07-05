from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from db import add_points
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

@app.get("/")
def root():
    return FileResponse(os.path.join(webapp_dir, "index.html"))

@app.post("/api/reward")
async def reward(request: Request):
    data = await request.json()
    user_id = data.get('userId')
    amount = data.get('amount', 0.25)
    if user_id:
        add_points(user_id, amount)
        return {"status": "ok", "rewarded": amount}
    return {"status": "error", "msg": "No userId"}
