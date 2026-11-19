from sqlalchemy import select
from models.inventoryproduct_model import InventoryProduct

def add_product(db,data):
    product=InventoryProduct(**data.model_dump())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

def get_all_products(db,skip=0,limit=10):
    return db.scalars(select(InventoryProduct).offset(skip).limit(limit)).all()

def get_product_by_id(db,product_id):
    return db.get(InventoryProduct,product_id)

def update_product(db,product_id,data):
    product=db.get(InventoryProduct,product_id)
    if product is None:
        return None
    for k,v in data.model_dump().items():
        setattr(product,k,v)
    db.commit()
    db.refresh(product)
    return product

def delete_product(db,product_id):
    product=db.get(InventoryProduct,product_id)
    if product is None:
        return False
    db.delete(product)
    db.commit()
    return True
