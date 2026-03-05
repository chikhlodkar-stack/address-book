from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.models.address import Address as AddressModel


# Note: We don't need to import `app`, `schemas`, or `crud` directly in tests
# because `client` and `db_session` fixtures provide the necessary setup.


def test_create_address(client: TestClient, db_session: Session):
    """
    Test creating a new address.
    """
    response = client.post(
        "/api/v1/addresses/",
        json={"name": "Test Address 1", "latitude": 10.0, "longitude": 20.0},
    )
    assert response.status_code == 201
    created_address = response.json()
    assert created_address["name"] == "Test Address 1"
    assert created_address["latitude"] == 10.0
    assert created_address["longitude"] == 20.0
    assert "id" in created_address  # ID should be assigned

    # Verify it exists in the database
    address_in_db = (
        db_session.query(AddressModel)
        .filter(AddressModel.id == created_address["id"])
        .first()
    )
    assert address_in_db is not None
    assert address_in_db.name == "Test Address 1"


def test_read_address(client: TestClient, db_session: Session):
    """
    Test retrieving a single address.
    """
    # First, create an address to read
    address_to_create = AddressModel(
        name="Test Read Address", latitude=11.1, longitude=22.2
    )
    db_session.add(address_to_create)
    db_session.commit()
    db_session.refresh(address_to_create)

    response = client.get(f"/api/v1/addresses/{address_to_create.id}")
    assert response.status_code == 200
    read_address = response.json()
    assert read_address["id"] == address_to_create.id
    assert read_address["name"] == "Test Read Address"


def test_read_non_existent_address(client: TestClient):
    """
    Test retrieving a non-existent address returns 404.
    """
    response = client.get("/api/v1/addresses/9999")  # Assuming 9999 does not exist
    assert response.status_code == 404
    assert response.json()["detail"] == "Address not found"


def test_update_address(client: TestClient, db_session: Session):
    """
    Test updating an existing address.
    """
    # First, create an address to update
    address_to_update = AddressModel(
        name="Original Name", latitude=12.1, longitude=23.2
    )
    db_session.add(address_to_update)
    db_session.commit()
    db_session.refresh(address_to_update)

    updated_data = {"name": "Updated Name", "latitude": 13.3, "longitude": 24.4}
    response = client.put(
        f"/api/v1/addresses/{address_to_update.id}", json=updated_data
    )
    assert response.status_code == 200
    updated_address = response.json()
    assert updated_address["name"] == "Updated Name"
    assert updated_address["latitude"] == 13.3

    # Verify the update in the database
    address_in_db = (
        db_session.query(AddressModel)
        .filter(AddressModel.id == updated_address["id"])
        .first()
    )
    assert address_in_db.name == "Updated Name"


def test_update_non_existent_address(client: TestClient):
    """
    Test updating a non-existent address returns 404.
    """
    response = client.put(
        "/api/v1/addresses/9999",
        json={"name": "Fake Update", "latitude": 1.0, "longitude": 2.0},
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Address not found"


def test_delete_address(client: TestClient, db_session: Session):
    """
    Test deleting an address.
    """
    # First, create an address to delete
    address_to_delete = AddressModel(
        name="To Be Deleted", latitude=14.1, longitude=25.2
    )
    db_session.add(address_to_delete)
    db_session.commit()
    db_session.refresh(address_to_delete)

    response = client.delete(f"/api/v1/addresses/{address_to_delete.id}")
    assert response.status_code == 200
    deleted_address = response.json()
    assert deleted_address["id"] == address_to_delete.id

    # Verify it's gone from the database
    address_in_db = (
        db_session.query(AddressModel)
        .filter(AddressModel.id == address_to_delete.id)
        .first()
    )
    assert address_in_db is None


def test_delete_non_existent_address(client: TestClient):
    """
    Test deleting a non-existent address returns 404.
    """
    response = client.delete("/api/v1/addresses/9999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Address not found"


def test_get_nearby_addresses(client: TestClient, db_session: Session):
    """
    Test retrieving addresses within a given distance from a location.
    We'll use specific coordinates to ensure accurate filtering.
    """
    # 1. Create some known addresses at specific locations
    # Distances are approximate for demonstration. Real distances would be calculated by geopy.
    # Coordinates of a central point (e.g., London Eye)
    london_eye_lat, london_eye_lon = 51.5033, -0.1196

    # Address 1: Very close to London Eye (e.g., few meters away)
    address1 = AddressModel(name="Near London Eye", latitude=51.5035, longitude=-0.1198)
    # Address 2: A bit further, clearly within 1km (e.g., Houses of Parliament)
    address2 = AddressModel(
        name="Houses of Parliament", latitude=51.4994, longitude=-0.1248
    )  # ~0.5km
    # Address 3: Further away, within 5km but outside 1km (e.g., Buckingham Palace)
    address3 = AddressModel(
        name="Buckingham Palace", latitude=51.5014, longitude=-0.1419
    )  # ~1.8km
    # Address 4: Far away, outside 5km (e.g., Tower Bridge)
    address4 = AddressModel(
        name="Tower Bridge", latitude=51.5055, longitude=0.0754
    )  # ~4km, but let's make one very far.
    address5 = AddressModel(
        name="Eiffel Tower", latitude=48.8584, longitude=2.2945
    )  # Very far

    db_session.add_all([address1, address2, address3, address4, address5])
    db_session.commit()
    db_session.refresh(address1)
    db_session.refresh(address2)
    db_session.refresh(address3)
    db_session.refresh(address4)
    db_session.refresh(address5)

    # 2. Test with a small radius (e.g., 0.6 km from London Eye)
    # Should get Address 1 and Address 2 (near London Eye and Houses of Parliament)
    response_small_radius = client.get(
        f"/api/v1/addresses/nearby?latitude={london_eye_lat}&longitude={london_eye_lon}&radius_km=0.6"
    )
    assert response_small_radius.status_code == 200
    nearby_addresses_small = response_small_radius.json()
    assert len(nearby_addresses_small) == 2
    assert any(a["id"] == address1.id for a in nearby_addresses_small)
    assert any(a["id"] == address2.id for a in nearby_addresses_small)
    assert not any(
        a["id"] == address3.id for a in nearby_addresses_small
    )  # Ensure not included

    # 3. Test with a medium radius (e.g., 2 km from London Eye)
    # Should get Address 1, Address 2, and Address 3 (Buckingham Palace)
    response_medium_radius = client.get(
        f"/api/v1/addresses/nearby?latitude={london_eye_lat}&longitude={london_eye_lon}&radius_km=2.0"
    )
    assert response_medium_radius.status_code == 200
    nearby_addresses_medium = response_medium_radius.json()
    assert len(nearby_addresses_medium) == 3
    assert any(a["id"] == address1.id for a in nearby_addresses_medium)
    assert any(a["id"] == address2.id for a in nearby_addresses_medium)
    assert any(a["id"] == address3.id for a in nearby_addresses_medium)
    assert not any(
        a["id"] == address4.id for a in nearby_addresses_medium
    )  # Ensure not included

    # 4. Test with a large radius (e.g., 50 km from London Eye)
    # Should get Address 1, 2, 3, 4, but not Address 5 (Eiffel Tower)
    response_large_radius = client.get(
        f"/api/v1/addresses/nearby?latitude={london_eye_lat}&longitude={london_eye_lon}&radius_km=50.0"
    )
    assert response_large_radius.status_code == 200
    nearby_addresses_large = response_large_radius.json()
    assert len(nearby_addresses_large) == 4
    assert any(a["id"] == address1.id for a in nearby_addresses_large)
    assert any(a["id"] == address2.id for a in nearby_addresses_large)
    assert any(a["id"] == address3.id for a in nearby_addresses_large)
    assert any(a["id"] == address4.id for a in nearby_addresses_large)
    assert not any(
        a["id"] == address5.id for a in nearby_addresses_large
    )  # Eiffel Tower should still be too far

    # 5. Test with no addresses in DB, should return empty list
    db_session.query(AddressModel).delete()  # Clear all addresses for this sub-test
    db_session.commit()
    response_empty_db = client.get(
        f"/api/v1/addresses/nearby?latitude={london_eye_lat}&longitude={london_eye_lon}&radius_km=10.0"
    )
    assert response_empty_db.status_code == 200
    assert response_empty_db.json() == []
