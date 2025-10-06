from __future__ import annotations
from pydantic import BaseModel, Field, ConfigDict, field_validator
from typing import Optional, Dict, Any

class Categoria(BaseModel):
    id: Optional[int] = None
    nombre: str
    subcategoria: Optional['Categoria'] = None
    model_config = ConfigDict(extra='forbid')

def _profundidad(cat: Optional['Categoria']) -> int:
    d = 0
    while cat:
        d += 1
        cat = cat.subcategoria
    return d

class ProductoBase(BaseModel):
    nombre: str = Field(..., examples=['Notebook Gamer'])
    precio: int = Field(..., ge=0, examples=[1200000])
    extra: Optional[Dict[str, Any]] = Field(default=None, examples=[{'color':'rojo'}])
    categoria: Optional[Categoria] = Field(default=None, examples=[{
        'id': 1, 'nombre': 'Tecnología',
        'subcategoria': {'id': 2, 'nombre': 'Computación', 'subcategoria': {'id': 3, 'nombre': 'Notebooks'}}
    }])
    model_config = ConfigDict(extra='forbid')

    @field_validator('categoria')
    @classmethod
    def _valida_profundidad(cls, v: Optional[Categoria]):
        if _profundidad(v) > 3:
            raise ValueError('La categoría no puede tener más de 3 niveles')
        return v

class ProductoCrear(ProductoBase):
    pass

class Producto(ProductoBase):
    id: int
    class Config:
        from_attributes = True

class ProductoParcial(BaseModel):
    nombre: Optional[str] = None
    precio: Optional[int] = None
    extra: Optional[Dict[str, Any]] = None
    categoria: Optional[Categoria] = None
    model_config = ConfigDict(extra='forbid')

    @field_validator('categoria')
    @classmethod
    def _valida_profundidad_parcial(cls, v: Optional[Categoria]):
        if _profundidad(v) > 3:
            raise ValueError('La categoría no puede tener más de 3 niveles')
        return v
