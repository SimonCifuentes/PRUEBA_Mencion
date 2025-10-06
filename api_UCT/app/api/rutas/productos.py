from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.infraestructura.base_datos import obtener_db
from app.dominio.esquemas import Producto, ProductoCrear, ProductoParcial
from app.dominio.servicios import srv_listar, srv_obtener, srv_crear, srv_reemplazar, srv_patch, srv_eliminar, serialize_producto
from app.seguridad.auth import verificar_token

router = APIRouter(prefix='/productos', tags=['productos'])

@router.get('', response_model=List[Producto])
def listar(db: Session = Depends(obtener_db)):
    return [serialize_producto(db, p) for p in srv_listar(db)]

@router.get('/{producto_id}', response_model=Producto)
def obtener(producto_id: int, db: Session = Depends(obtener_db)):
    p = srv_obtener(db, producto_id)
    if not p: raise HTTPException(status_code=404, detail='Producto no encontrado')
    return serialize_producto(db, p)

@router.post('', response_model=Producto, dependencies=[Depends(verificar_token)])
def crear(payload: ProductoCrear, db: Session = Depends(obtener_db)):
    return serialize_producto(db, srv_crear(db, payload))

@router.put('/{producto_id}', response_model=Producto)
def reemplazar(producto_id: int, payload: ProductoCrear, db: Session = Depends(obtener_db)):
    p = srv_reemplazar(db, producto_id, payload)
    if not p: raise HTTPException(status_code=404, detail='Producto no encontrado')
    return serialize_producto(db, p)

@router.patch('/{producto_id}', response_model=Producto)
def actualizar_parcial(producto_id: int, payload: ProductoParcial, db: Session = Depends(obtener_db)):
    p = srv_patch(db, producto_id, payload)
    if not p: raise HTTPException(status_code=404, detail='Producto no encontrado')
    return serialize_producto(db, p)

@router.delete('/{producto_id}', status_code=204)
def eliminar(producto_id: int, db: Session = Depends(obtener_db)):
    ok = srv_eliminar(db, producto_id)
    if not ok: raise HTTPException(status_code=404, detail='Producto no encontrado')
    return None
