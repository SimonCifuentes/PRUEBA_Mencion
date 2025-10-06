from fastapi import FastAPI
from app.infraestructura.base_datos import engine, Base
from app.api.rutas.productos import router as productos_router
from app.api.rutas.graphql import graphql_router

app = FastAPI(title='API de Productos (ES) – REST + GraphQL')

@app.on_event('startup')
def on_startup():
    Base.metadata.create_all(bind=engine)

@app.get('/', tags=['health'])
def salud():
    return {'estado': 'ok', 'servicio': 'api-productos-es'}

app.include_router(productos_router)
app.include_router(graphql_router)
