from sqlalchemy.orm import Session
from app.dominio.modelos import Producto, CategoriaNivel1, CategoriaNivel2, CategoriaNivel3

def listar_productos(db: Session):
    return db.query(Producto).all()

def obtener_producto(db: Session, pid: int):
    return db.query(Producto).filter(Producto.id == pid).first()

def guardar_producto(db: Session, obj: Producto):
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def eliminar_producto(db: Session, obj: Producto):
    db.delete(obj)
    db.commit()

def get_n1(db: Session, cid: int): return db.get(CategoriaNivel1, cid)

def get_n2(db: Session, cid: int): return db.get(CategoriaNivel2, cid)

def get_n3(db: Session, cid: int): return db.get(CategoriaNivel3, cid)

def crear_n1(db: Session, nombre: str, id_override: int | None = None):
    c = CategoriaNivel1(id=id_override, nombre=nombre) if id_override else CategoriaNivel1(nombre=nombre)
    db.add(c); db.flush(); return c

def crear_n2(db: Session, nombre: str, padre_id: int, id_override: int | None = None):
    c = CategoriaNivel2(id=id_override, nombre=nombre, padre_id=padre_id) if id_override else CategoriaNivel2(nombre=nombre, padre_id=padre_id)
    db.add(c); db.flush(); return c

def crear_n3(db: Session, nombre: str, padre_id: int, id_override: int | None = None):
    c = CategoriaNivel3(id=id_override, nombre=nombre, padre_id=padre_id) if id_override else CategoriaNivel3(nombre=nombre, padre_id=padre_id)
    db.add(c); db.flush(); return c
