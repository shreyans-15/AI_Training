from fastapi import FastAPI,HTTPException
from services import customer_service as service
from config.database import Base, SessionLocal, engine
from schema.customer_schema import CustomerResponse, CustomerCreate
from config.logging_config import logger

app = FastAPI(
    title="Coforge customer management API",
    version="1.0.1"
)

Base.metadata.create_all(bind=engine)

#home route
@app.get("/")
def home():
    return {
        "message": "Welcome to Coforge Management Management API"
    }

#get all customer
@app.get("/customers", response_model=list[CustomerResponse])
def get_all_customer():
    logger.info("GetAllCustomers API called")
    db = SessionLocal()

    try:
        customers = service.get_all_customers(db)
        logger.info(f"Successfully retrieved %s customers{len(customers)}"),
        return customers
    finally:
        db.close()

@app.get("/customers/{id}", response_model=CustomerResponse)
def getcustomerbyid(id: int):

    db = SessionLocal()
    

    try:
        customer = service.GetCustomerById(db, id)

        if customer is None:
            raise HTTPException(
                status_code=404,
                detail="Customer not found"
            )
        
        return customer

    finally:
        db.close()


@app.post("/customers", response_model=CustomerResponse)
def createcustomer(customer: CustomerCreate):
    db = SessionLocal()
    return service.add_customer(db, customer)