from typing import Optional, Dict, Any
from sqlalchemy.orm import Session
from app.dominio.modelos import Producto as ORMProducto, CategoriaNivel3
from app.dominio.esquemas import ProductoCrear, ProductoParcial
from app.dominio.repositorios import (
    listar_productos, obtener_producto, guardar_producto, eliminar_producto,
    get_n1, get_n2, get_n3, crear_n1, crear_n2, crear_n3
)

def _profundidad(cat: Dict[str, Any] | None) -> int:
    d = 0
    while cat:
        d += 1
        cat = cat.get('subcategoria')
    return d

def _asegurar_cadena(db: Session, cat: Dict[str, Any] | None) -> Optional[int]:
    if not cat:
        return None
    if _profundidad(cat) > 3:
        raise ValueError('La categoría no puede tener más de 3 niveles')
    c1 = get_n1(db, cat['id']) if cat.get('id') else None
    if not c1:
        c1 = crear_n1(db, nombre=cat['nombre'], id_override=cat.get('id'))
    cat2 = cat.get('subcategoria')
    if not cat2:
        db.commit(); return None
    c2 = get_n2(db, cat2['id']) if cat2.get('id') else None
    if not c2:
        c2 = crear_n2(db, nombre=cat2['nombre'], padre_id=c1.id, id_override=cat2.get('id'))
    cat3 = cat2.get('subcategoria')
    if not cat3:
        db.commit(); return None
    c3 = get_n3(db, cat3['id']) if cat3.get('id') else None
    if not c3:
        c3 = crear_n3(db, nombre=cat3['nombre'], padre_id=c2.id, id_override=cat3.get('id'))
    db.commit(); return c3.id

def _cadena_json(c3: CategoriaNivel3 | None):
    if not c3: return None
    c2 = c3.padre; c1 = c2.padre
    return {
        'id': c1.id, 'nombre': c1.nombre,
        'subcategoria': {'id': c2.id, 'nombre': c2.nombre, 'subcategoria': {'id': c3.id, 'nombre': c3.nombre}}
    }

def srv_listar(db: Session):
    return listar_productos(db)

def srv_obtener(db: Session, pid: int) -> Optional[ORMProducto]:
    return obtener_producto(db, pid)

def srv_crear(db: Session, payload: ProductoCrear) -> ORMProducto:
    leaf_id = _asegurar_cadena(db, payload.categoria.model_dump() if payload.categoria else None)
    obj = ORMProducto(nombre=payload.nombre, precio=payload.precio, extra_json=payload.extra or {}, categoria3_id=leaf_id)
    return guardar_producto(db, obj)

def srv_reemplazar(db: Session, pid: int, payload: ProductoCrear) -> Optional[ORMProducto]:
    obj = obtener_producto(db, pid)
    if not obj: return None
    leaf_id = _asegurar_cadena(db, payload.categoria.model_dump() if payload.categoria else None)
    obj.nombre = payload.nombre
    obj.precio = payload.precio
    obj.extra_json = payload.extra or {}
    obj.categoria3_id = leaf_id
    return guardar_producto(db, obj)

def srv_patch(db: Session, pid: int, payload: ProductoParcial) -> Optional[ORMProducto]:
    obj = obtener_producto(db, pid)
    if not obj: return None
    if payload.nombre is not None: obj.nombre = payload.nombre
    if payload.precio is not None: obj.precio = payload.precio
    if payload.extra is not None: obj.extra_json = payload.extra
    if payload.categoria is not None:
        leaf_id = _asegurar_cadena(db, payload.categoria.model_dump() if payload.categoria else None)
        obj.categoria3_id = leaf_id
    return guardar_producto(db, obj)

def srv_eliminar(db: Session, pid: int) -> bool:
    obj = obtener_producto(db, pid)
    if not obj: return False
    eliminar_producto(db, obj)
    return True

def serialize_producto(db: Session, p: ORMProducto):
    c3 = db.get(CategoriaNivel3, p.categoria3_id) if p.categoria3_id else None
    return {'id': p.id, 'nombre': p.nombre, 'precio': p.precio, 'extra': p.extra_json, 'categoria': _cadena_json(c3)}
