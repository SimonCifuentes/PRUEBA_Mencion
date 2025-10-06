import strawberry
from strawberry.fastapi import GraphQLRouter
from strawberry.scalars import JSON
from typing import List, Optional
from sqlalchemy.orm import Session

from app.infraestructura.base_datos import obtener_db
from app.dominio.servicios import srv_listar, srv_crear, serialize_producto
from app.dominio.esquemas import ProductoCrear

@strawberry.type
class ProductoType:
    id: int
    nombre: str
    precio: int
    extra: Optional[JSON]
    categoria: Optional[JSON]

@strawberry.type
class Consulta:
    @strawberry.field
    def productos(self) -> List[ProductoType]:
        db: Session = next(obtener_db())
        try:
            filas = srv_listar(db)
            serial = [serialize_producto(db, f) for f in filas]
            return [ProductoType(**x) for x in serial]
        finally:
            db.close()

@strawberry.type
class Mutacion:
    @strawberry.mutation
    def crearProducto(self, nombre: str, precio: int, extra: Optional[JSON] = None, categoria: Optional[JSON] = None) -> ProductoType:
        db: Session = next(obtener_db())
        try:
            payload = ProductoCrear(nombre=nombre, precio=precio, extra=extra, categoria=categoria)
            guardado = srv_crear(db, payload)
            data = serialize_producto(db, guardado)
            return ProductoType(**data)
        finally:
            db.close()

schema = strawberry.Schema(query=Consulta, mutation=Mutacion)
graphql_router = GraphQLRouter(schema, path='/graphql')
