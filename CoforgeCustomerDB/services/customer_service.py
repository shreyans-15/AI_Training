from sqlalchemy.orm import Session
from sqlalchemy import select, func
from sqlalchemy.exc import IntegrityError
from models.customer_model import Customer
from decimal import Decimal


# add customer
def add_customer(db: Session, data):

    customer = Customer(**data.model_dump())

    db.add(customer)
    db.commit()
    db.refresh(customer)

    return customer


# Get all customers
def get_all_customers(db: Session):

    query = select(Customer).order_by(Customer.customer_id)

    result = db.scalars(query)

    customers = result.all()

    return customers


# Search customer by id
def get_customer_by_id(db: Session, customer_id: int):

    return db.get(Customer, customer_id)


# Update customer
def update_customer(db: Session, customer_id: int, data):

    customer = db.get(Customer, customer_id)

    if customer is None:
        return None

    for key, value in data.model_dump().items():
        setattr(customer, key, value)

    try:
        db.commit()
        db.refresh(customer)
        return customer

    except IntegrityError:
        db.rollback()
        raise


# Delete customer
def delete_customer(db: Session, customer_id: int):

    customer = db.get(Customer, customer_id)

    if customer is None:
        return False

    db.delete(customer)
    db.commit()

    return True


# Search customer by name
def get_customer_by_name(db: Session, customer_name: str):

    query = select(Customer).where(
        Customer.customer_name == customer_name
    )

    return db.scalars(query).all()


# Search customer by gender
def get_customer_by_gender(db: Session, customer_gender: str):

    query = select(Customer).where(
        Customer.customer_gender == customer_gender
    )

    return db.scalars(query).all()