from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import declarative_base

# Create a Base class for our models to inherit from
Base = declarative_base()


# Define the Address model which corresponds to the 'addresses' table in the DB
class Address(Base):
    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
