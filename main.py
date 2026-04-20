from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# 🔥 Estado global (simulación)
estado_bomba = False
humedad_actual = 0

# 📦 Modelo para humedad
class Humedad(BaseModel):
    valor: int

# 🟢 Endpoint para cambiar estado (simula webhook)
@app.post("/toggle")
def toggle():
    global estado_bomba
    estado_bomba = not estado_bomba
    return {"estado": estado_bomba}

# 🔵 Endpoint que consulta el ESP32
@app.get("/estado")
def get_estado():
    return {"activar": estado_bomba}

# 🟡 Endpoint para recibir humedad
@app.post("/humedad")
def recibir_humedad(data: Humedad):
    global humedad_actual
    humedad_actual = data.valor
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
