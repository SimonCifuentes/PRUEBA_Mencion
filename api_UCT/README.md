# API de Productos (ES) – FastAPI + REST + GraphQL + SQLite

- REST `/productos`: GET, GET por ID, POST protegido (Bearer `secreto123`), PUT, PATCH, DELETE.
- GraphQL `/graphql`: Query `productos` y Mutation `crearProducto`.
- Categorías: 3 tablas enlazadas (`categorias_n1` → `categorias_n2` → `categorias_n3`), el producto se asocia al nivel 3.

## Ejecutar
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
python -m uvicorn app.main:app --reload
```
## Mutation crearProducto
```powershell
mutation {
  crearProducto(
    nombre: "Mouse Inalámbrico"
    precio: 19990
    extra: { dpi: 16000 }
    categoria: {
      nombre: "Tecnología"
      subcategoria: {
        nombre: "Periféricos"
        subcategoria: { nombre: "Mouse" }
      }
    }
  ) {
    id
    nombre
    precio
    extra
    categoria
  }
}
```

## Query productos
```powershell
query {
  productos {
    id
    nombre
    precio
    extra
    categoria
  }
}
```
