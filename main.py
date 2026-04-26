from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

app = FastAPI()

templates = Jinja2Templates(directory="templates")

# =========================================
# ESTADO GLOBAL
# =========================================

estado_bomba = False

telemetry = {
    "soilHumidity": 0,
    "temperature": 0,
    "airHumidity": 0
}

clientes = []

# =========================================
# MODELO TELEMETRIA
# =========================================

class Telemetria(BaseModel):
    soilHumidity: int
    temperature: float
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

        clientes.remove(websocket)

# =========================================
# BROADCAST
# =========================================

async def broadcast():

    data = {
        "relay": estado_bomba,
        "soilHumidity": telemetry["soilHumidity"],
        "temperature": telemetry["temperature"],
        "airHumidity": telemetry["airHumidity"]
    }

    for cliente in clientes:

        await cliente.send_json(data)

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
        "temperature": data.temperature,
        "airHumidity": data.airHumidity
    }

    await broadcast()

    return {
        "ok": True
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

    uvicorn.run(app, host="0.0.0.0", port=8000)