from fastapi import Depends, FastAPI, HTTPException

from api.schemas.product import ProductCreate, ProductRead
from db.database import get_db
from db.manager import DatabaseManager

app = FastAPI()


@app.post('/products/', response_model=ProductRead)
def create_product(
    product: ProductCreate, db: DatabaseManager = Depends(get_db)
):
    db.create_product(product)
    return product


@app.get('/products/{product_id}', response_model=ProductRead)
def read_product(product_id: int, db: DatabaseManager = Depends(get_db)):
    product = db.get_product_by_id(product_id)
    if product is None:
        raise HTTPException(status_code=404, detail='Product not found')
    return product


@app.get('/products/', response_model=list[ProductRead])
def read_products(
    skip: int = 0, limit: int = 10, db: DatabaseManager = Depends(get_db)
):
    products = db.get_all_products()[skip : skip + limit]
    return products


if __name__ == '__main__':
    pass
