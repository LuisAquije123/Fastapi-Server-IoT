from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List

app = FastAPI()

templates = Jinja2Templates(directory="templates")

# =========================================
# ESTADO GLOBAL
# =========================================

estado_bomba = False

telemetry = {
    "soilHumidity": 0,       # Humedad del suelo (%)
    "soilTemperature": 0.0, # Temperatura del suelo (°C)
    "airTemperature": 0.0,  # Temperatura del ambiente (°C)
    "airHumidity": 0.0      # Humedad del aire (%)
}

clientes: List[WebSocket] = []

# =========================================
# MODELO TELEMETRIA
# =========================================

class Telemetria(BaseModel):
    soilHumidity: int
    soilTemperature: float
    airTemperature: float
    airHumidity: float

# =========================================
# WEBSOCKET
# =========================================

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):

    await websocket.accept()

    clientes.append(websocket)

    try:

        while True:
            await websocket.receive_text()

    except WebSocketDisconnect:

        if websocket in clientes:
            clientes.remove(websocket)

# =========================================
# BROADCAST
# =========================================

async def broadcast():

    data = {
        "relay": estado_bomba,

        "soilHumidity": telemetry["soilHumidity"],
        "soilTemperature": telemetry["soilTemperature"],

        "airTemperature": telemetry["airTemperature"],
        "airHumidity": telemetry["airHumidity"]
    }

    disconnected = []

    for cliente in clientes:

        try:

            await cliente.send_json(data)

        except Exception:
            disconnected.append(cliente)

    for cliente in disconnected:

        if cliente in clientes:
            clientes.remove(cliente)

# =========================================
# TOGGLE RELE
# =========================================

@app.post("/toggle")
async def toggle():

    global estado_bomba

    estado_bomba = not estado_bomba

    await broadcast()

    return {
        "relay": estado_bomba
    }

# =========================================
# ESTADO PARA ESP32
# =========================================

@app.get("/estado")
def get_estado():

    return {
        "activar": estado_bomba
    }

# =========================================
# RECIBIR TELEMETRIA
# =========================================

@app.post("/telemetria")
async def recibir(data: Telemetria):

    global telemetry

    telemetry = {
        "soilHumidity": data.soilHumidity,

        "soilTemperature": data.soilTemperature,

        "airTemperature": data.airTemperature,

        "airHumidity": data.airHumidity
    }

    await broadcast()

    return {
        "ok": True,
        "telemetry": telemetry
    }

# =========================================
# DASHBOARD
# =========================================

@app.get("/", response_class=HTMLResponse)
def dashboard(request: Request):

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "relay": estado_bomba,
            "telemetry": telemetry
        }
    )

# =========================================

if __name__ == "__main__":

    import uvicorn

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000
    )