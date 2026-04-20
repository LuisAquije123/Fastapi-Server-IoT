# FastAPI con Jinja2 - Proyecto de Prueba

Proyecto de demostración que integra **FastAPI** con **Jinja2** para renderizar vistas HTML dinámicas.

## 📋 Características

- ✅ Renderización de templates HTML con Jinja2
- ✅ Paso de variables dinámicas desde el backend
- ✅ Multiple rutas con parámetros dinámicos
- ✅ Navegación entre páginas
- ✅ Diseño responsive con CSS moderno
- ✅ Ejemplos de iteración y condicionales en templates
- ✅ Filtros de Jinja2 (title, format, etc)

## 📁 Estructura del Proyecto

```
PRUEBA/
├── main.py              # Aplicación principal (FastAPI)
├── requirements.txt     # Dependencias del proyecto
├── README.md            # Este archivo
├── templates/           # Directorio de templates Jinja2
│   ├── base.html       # Template base con CSS compartido
│   ├── index.html      # Página de inicio
│   ├── lista.html      # Lista de usuarios
│   ├── usuario.html    # Perfil de usuario específico
│   ├── productos.html  # Catálogo de productos
│   └── acerca.html     # Información del proyecto
└── static/             # Archivos estáticos (CSS, JS, imágenes)
```

## 🚀 Instalación

### 1. Crear entorno virtual

```powershell
# Windows
python -m venv venv
.\venv\Scripts\Activate.ps1

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

## 🎯 Ejecutar la Aplicación

```bash
python main.py
```

La aplicación estará disponible en: `http://localhost:8000`

## 📍 Rutas Disponibles

| Ruta | Descripción |
|------|-------------|
| `/` | Página de inicio |
| `/lista` | Lista de todos los usuarios |
| `/usuarios/{id}` | Perfil de un usuario específico |
| `/productos` | Catálogo de productos |
| `/acerca` | Información del proyecto |

## 🔗 Ejemplos de Uso

### Acceder a perfiles de usuario:
- http://localhost:8000/usuarios/1
- http://localhost:8000/usuarios/2
- http://localhost:8000/usuarios/3

## 💡 Conceptos Demostrados

### 1. **Jinja2 - Herencia de Templates**
```html
<!-- base.html -->
{% extends "base.html" %}
{% block contenido %}
    <!-- Contenido específico -->
{% endblock %}
```

### 2. **Jinja2 - Bucles**
```html
{% for usuario in usuarios %}
    <tr>
        <td>{{ usuario.nombre }}</td>
    </tr>
{% endfor %}
```

### 3. **Jinja2 - Condicionales**
```html
{% if usuario.rol == "Admin" %}
    <span class="badge badge-success">Admin</span>
{% else %}
    <span class="badge badge-info">Usuario</span>
{% endif %}
```

### 4. **Jinja2 - Filtros**
```html
{{ usuario.nombre|title }}           <!-- Convierte a título -->
{{ precio|format('%.2f') }}          <!-- Formatea números -->
```

### 5. **FastAPI - Pasar Variables a Templates**
```python
@app.get("/usuarios/{usuario_id}")
async def get_usuario(request: Request, usuario_id: int):
    return templates.TemplateResponse("usuario.html", {
        "request": request,
        "usuario_id": usuario_id,
        "usuario": usuario_data
    })
```

## 📦 Dependencias

| Paquete | Versión | Descripción |
|---------|---------|-------------|
| FastAPI | 0.104.1 | Framework web moderno |
| Uvicorn | 0.24.0 | Servidor ASGI |
| Jinja2 | 3.1.2 | Motor de templates |

## 🎨 Personalización

### Agregar una nueva ruta con vista:

```python
@app.get("/nueva-pagina")
async def nueva_pagina(request: Request):
    return templates.TemplateResponse("nueva_pagina.html", {
        "request": request,
        "datos": "tu_data_aqui"
    })
```

### Crear nuevo template:

```html
{% extends "base.html" %}

{% block titulo %}Mi Nueva Página{% endblock %}

{% block contenido %}
<h2>Contenido de la nueva página</h2>
<p>{{ datos }}</p>
{% endblock %}
```

## 🐛 Troubleshooting

**Error: "TemplateNotFound"**
- Verifica que el archivo existe en la carpeta `templates/`
- Los nombres son sensibles a mayúsculas

**Error: "Port 8000 already in use"**
- Usa otro puerto: `uvicorn.run(app, host="0.0.0.0", port=8001)`

**Templates sin CSS**
- Asegúrate de que la carpeta `static/` existe
- Los estilos CSS están en `base.html`

## 📚 Recursos

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Jinja2 Documentation](https://jinja.palletsprojects.com/)
- [Uvicorn](https://www.uvicorn.org/)

---

**Creado:** Abril 2026
**Versión:** 1.0.0
