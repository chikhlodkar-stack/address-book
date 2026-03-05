# In app/crud/crud_address.py

from sqlalchemy.orm import Session
from typing import List

# Import specific schemas and models directly from their files
from app.models.address import (
    Address as AddressModel,
)  # Aliased to avoid conflict if Address schema exists
from app.schemas.address import AddressCreate

# ---- READ Operations ----


def get_address(db: Session, address_id: int):
    """
    Retrieves a single address from the database by its ID.
    """
    return db.query(AddressModel).filter(AddressModel.id == address_id).first()


def get_addresses(db: Session, skip: int = 0, limit: int = 100):
    """
    Retrieves a list of addresses from the database.
    Includes pagination with skip and limit.
    """
    return db.query(AddressModel).offset(skip).limit(limit).all()


def get_all_addresses(db: Session) -> List[AddressModel]:
    """
    Retrieves all addresses from the database.
    Returns a list of AddressModel objects.
    """
    return db.query(AddressModel).all()


# ---- CREATE Operation ----


def create_address(
    db: Session, address: AddressCreate
):  # Use the imported AddressCreate
    """
    Creates a new address record in the database.
    """
    # Create a new SQLAlchemy model instance from the Pydantic schema data
    db_address = AddressModel(  # Use the imported AddressModel
        name=address.name, latitude=address.latitude, longitude=address.longitude
    )
    # Add the new instance to the session
    db.add(db_address)
    # Commit the changes to the database
    db.commit()
    # Refresh the instance to get the new data from the DB (like the generated ID)
    db.refresh(db_address)
    return db_address


# ---- UPDATE Operation ----
# We need AddressUpdate here, so let's import it first
# Add 'AddressUpdate' to the import line above: from app.schemas.address import AddressCreate, Address as AddressSchema, AddressUpdate
def update_address(
    db: Session, address_id: int, address_data: AddressCreate
):  # Changed to AddressCreate from AddressUpdate because we defined it as such in the endpoints for simplicity.
    # For a real app, it's better to have AddressUpdate with optional fields.
    """
    Updates an existing address in the database.
    """
    # First, retrieve the existing address
    db_address = get_address(db=db, address_id=address_id)
    if db_address:
        # Update its fields with the new data
        db_address.name = address_data.name
        db_address.latitude = address_data.latitude
        db_address.longitude = address_data.longitude
        # Commit the changes
        db.commit()
        # Refresh the instance
        db.refresh(db_address)
    return db_address


# ---- DELETE Operation ----


def delete_address(db: Session, address_id: int):
    """
    Deletes an address from the database.
    """
    # Retrieve the existing address
    db_address = get_address(db=db, address_id=address_id)
    if db_address:
        # Delete the record
        db.delete(db_address)
        # Commit the deletion
        db.commit()
    return db_address
