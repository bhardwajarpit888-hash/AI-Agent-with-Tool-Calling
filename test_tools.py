import pytest
from app import calculate_shipping_cost, check_inventory_database

def test_calculate_shipping_cost_valid():
    # Test valid weight and distance
    result = calculate_shipping_cost.invoke({"weight_kg": 2.0, "distance_km": 50.0})
    assert "Shipping Cost:" in result
    assert "$15.0" in result  # 5.0 + (2.0 * 2.5) + (50.0 * 0.1) = 5 + 5 + 5 = 15

def test_calculate_shipping_cost_invalid():
    # Test negative or zero values
    result = calculate_shipping_cost.invoke({"weight_kg": -1.0, "distance_km": 10.0})
    assert "Error:" in result

def test_check_inventory_valid_sku():
    # Test an existing SKU
    result = check_inventory_database.invoke({"item_sku": "SKU-882"})
    assert "In Stock" in result
    assert "Warehouse A" in result

def test_check_inventory_invalid_sku():
    # Test a non-existent SKU
    result = check_inventory_database.invoke({"item_sku": "SKU-999"})
    assert "not found" in result