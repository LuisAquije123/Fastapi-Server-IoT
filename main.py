from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from fastapi import WebSocket, WebSocketDisconnect

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# 🔥 Estado global (simulación)
estado_bomba = False
humedad_actual = 0

# 📦 Modelo para humedad
class Humedad(BaseModel):
    valor: int

clientes = []

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clientes.append(websocket)

    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        clientes.remove(websocket)

async def broadcast():
    for cliente in clientes:
        await cliente.send_json({
            "estado": estado_bomba,
            "humedad": humedad_actual
        })

# 🟢 Endpoint para cambiar estado (simula webhook)
@app.post("/toggle")
async def toggle():
    global estado_bomba
    estado_bomba = not estado_bomba
    await broadcast()
    return {"estado": estado_bomba}

# 🔵 Endpoint que consulta el ESP32
@app.get("/estado")
def get_estado():
    return {"activar": estado_bomba}

# 🟡 Endpoint para recibir humedad
@app.post("/humedad")
async def recibir_humedad(data: Humedad):
    global humedad_actual
    humedad_actual = data.valor
    await broadcast()
    return {"ok": True}

# 🌐 Dashboard
@app.get("/", response_class=HTMLResponse)
def dashboard(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request,
        "estado": estado_bomba,
        "humedad": humedad_actual
    })


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
