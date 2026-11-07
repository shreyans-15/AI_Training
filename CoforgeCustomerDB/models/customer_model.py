from sqlalchemy import (Column, Integer, String)
from config.database import Base

class Customer(Base):
    __tablename__ = "Customers"

    customer_id = Column(
        Integer,
        primary_key=True,
        index=True,
        autoincrement=True
    )

    customer_name = Column(
        String(100),
        nullable=False
    )

    email = Column(
        String(150),
        unique=True,
        nullable=False
    )

    age = Column(
        Integer,
        nullable=False
    )

    gender = Column(
        String(20),
        nullable=False
    )