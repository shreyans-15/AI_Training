from fastapi import FastAPI,HTTPException
from config.database import SessionLocal,engine,Base
from services import inventoryproduct_service as service
from schema.inventoryproduct_schema import ProductCreate,ProductUpdate,ProductResponse

app=FastAPI(title="Inventory Product API",version="1.0")
Base.metadata.create_all(bind=engine)

@app.get("/")
def home():
    return {"message":"Inventory Product API"}

@app.post("/products",response_model=ProductResponse)
def create_product(product:ProductCreate):
    db=SessionLocal()
    return service.add_product(db,product)

@app.get("/products",response_model=list[ProductResponse])
def get_products(page:int=1,size:int=10):
    db=SessionLocal()
    return service.get_all_products(db,(page-1)*size,size)

@app.get("/products/{product_id}",response_model=ProductResponse)
def get_product(product_id:int):
    db=SessionLocal()
    product=service.get_product_by_id(db,product_id)
    if not product:
        raise HTTPException(status_code=404,detail="Product not found")
    return product

@app.put("/products/{product_id}",response_model=ProductResponse)
def update_product(product_id:int,data:ProductUpdate):
    db=SessionLocal()
    product=service.update_product(db,product_id,data)
    if not product:
        raise HTTPException(status_code=404,detail="Product not found")
    return product

@app.delete("/products/{product_id}")
def delete_product(product_id:int):
    db=SessionLocal()
    deleted=service.delete_product(db,product_id)
    if not deleted:
        raise HTTPException(status_code=404,detail="Product not found")
    return {"message":"Product deleted successfully"}
