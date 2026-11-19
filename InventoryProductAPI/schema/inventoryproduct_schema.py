from decimal import Decimal
from pydantic import BaseModel,Field,ConfigDict

class ProductBase(BaseModel):
    product_name:str
    category:str
    supplier_name:str
    unit_price:Decimal=Field(gt=0)
    quantity_in_stock:int=Field(ge=0)
    reorder_level:int=Field(ge=0)
    warehouse_location:str
    is_active:bool=True

class ProductCreate(ProductBase):
    pass

class ProductUpdate(ProductBase):
    pass

class StockSchema(BaseModel):
    quantity:int=Field(gt=0)

class ProductResponse(ProductBase):
    product_id:int
    model_config=ConfigDict(from_attributes=True)
