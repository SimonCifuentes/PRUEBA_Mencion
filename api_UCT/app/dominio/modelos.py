from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, JSON, ForeignKey
from app.infraestructura.base_datos import Base

class CategoriaNivel1(Base):
    __tablename__ = 'categorias_n1'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nombre: Mapped[str] = mapped_column(String, index=True)

class CategoriaNivel2(Base):
    __tablename__ = 'categorias_n2'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nombre: Mapped[str] = mapped_column(String, index=True)
    padre_id: Mapped[int] = mapped_column(ForeignKey('categorias_n1.id'))
    padre = relationship('CategoriaNivel1')

class CategoriaNivel3(Base):
    __tablename__ = 'categorias_n3'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nombre: Mapped[str] = mapped_column(String, index=True)
    padre_id: Mapped[int] = mapped_column(ForeignKey('categorias_n2.id'))
    padre = relationship('CategoriaNivel2')

class Producto(Base):
    __tablename__ = 'productos'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nombre: Mapped[str] = mapped_column(String, index=True)
    precio: Mapped[int] = mapped_column(Integer)
    extra_json: Mapped[dict] = mapped_column(JSON, default=dict)
    categoria3_id: Mapped[int | None] = mapped_column(ForeignKey('categorias_n3.id'), nullable=True)
    categoria3 = relationship('CategoriaNivel3')
