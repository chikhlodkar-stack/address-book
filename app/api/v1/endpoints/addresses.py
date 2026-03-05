from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import geopy.distance

# Import specific schemas and crud functions directly
from app.schemas.address import (
    AddressCreate,
    Address as AddressSchema,
)  # Import AddressCreate and alias Address as AddressSchema
from app.crud import crud_address
from app.api.dependencies import get_db

# Create a new router object
router = APIRouter()


# ---- CREATE ADDRESS ----
@router.post(
    "/", response_model=AddressSchema, status_code=status.HTTP_201_CREATED
)  # Use AddressSchema
def create_address(
    address: AddressCreate, db: Session = Depends(get_db)
):  # Use AddressCreate
    """
    Create a new address.
    """
    return crud_address.create_address(db=db, address=address)


# ---- READ NEARBY ADDRESSES ----
@router.get("/nearby", response_model=List[AddressSchema])
def get_nearby_addresses(
    latitude: float, longitude: float, radius_km: float, db: Session = Depends(get_db)
):
    """
    Retrieve addresses within a given radius (in kilometers) from a specified location.

    - **latitude**: The latitude of the central point.
    - **longitude**: The longitude of the central point.
    - **radius_km**: The search radius in kilometers.
    """
    # 1. Validate input coordinates (FastAPI/Pydantic already handles basic float validation)
    #    We can add more specific range validation if needed, but Pydantic schemas are
    #    primarily for request bodies. For query params, we often do it here or via `Field`
    #    in Pydantic. For now, let's assume valid float inputs.

    # 2. Get all addresses from the database
    all_addresses = crud_address.get_all_addresses(db)

    # 3. Define the central coordinates for the search
    target_coords = (latitude, longitude)

    nearby_addresses = []
    for address in all_addresses:
        address_coords = (address.latitude, address.longitude)

        # Calculate the distance between the target and the address
        # geopy.distance.distance returns a Distance object, .km gives the value in kilometers
        distance = geopy.distance.distance(target_coords, address_coords).km

        # If the address is within the specified radius, add it to the list
        if distance <= radius_km:
            nearby_addresses.append(address)

    return nearby_addresses


# ---- READ ONE ADDRESS ----
@router.get("/{address_id}", response_model=AddressSchema)  # Use AddressSchema
def read_address(address_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a single address by its ID.
    """
    db_address = crud_address.get_address(db, address_id=address_id)
    if db_address is None:
        raise HTTPException(status_code=404, detail="Address not found")
    return db_address


# ---- UPDATE ADDRESS ----
@router.put("/{address_id}", response_model=AddressSchema)  # Use AddressSchema
def update_address(
    address_id: int, address: AddressCreate, db: Session = Depends(get_db)
):  # Use AddressCreate for input
    """
    Update an existing address.
    """
    db_address = crud_address.update_address(
        db, address_id=address_id, address_data=address
    )
    if db_address is None:
        raise HTTPException(status_code=404, detail="Address not found")
    return db_address


# ---- DELETE ADDRESS ----
@router.delete("/{address_id}", response_model=AddressSchema)  # Use AddressSchema
def delete_address(address_id: int, db: Session = Depends(get_db)):
    """
    Delete an address.
    """
    db_address = crud_address.delete_address(db, address_id=address_id)
    if db_address is None:
        raise HTTPException(status_code=404, detail="Address not found")
    return db_address
