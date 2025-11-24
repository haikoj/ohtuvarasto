from varasto import Varasto


class WarehouseManager:
    """Manages multiple warehouses with names and items."""

    def __init__(self):
        self.warehouses = {}
        self.warehouse_items = {}

    def create_warehouse(self, name, capacity):
        """Create a new warehouse with the given name and capacity."""
        if name in self.warehouses:
            raise ValueError(f"Warehouse '{name}' already exists")
        self.warehouses[name] = Varasto(capacity)
        self.warehouse_items[name] = {}
        return self.warehouses[name]

    def delete_warehouse(self, name):
        """Delete a warehouse by name."""
        if name not in self.warehouses:
            raise ValueError(f"Warehouse '{name}' does not exist")
        del self.warehouses[name]
        del self.warehouse_items[name]

    def get_warehouse(self, name):
        """Get a warehouse by name."""
        if name not in self.warehouses:
            raise ValueError(f"Warehouse '{name}' does not exist")
        return self.warehouses[name]

    def get_all_warehouses(self):
        """Get all warehouses as a list of dicts with their info."""
        result = []
        for name, warehouse in self.warehouses.items():
            result.append({
                'name': name,
                'capacity': warehouse.tilavuus,
                'balance': warehouse.saldo,
                'free_space': warehouse.paljonko_mahtuu(),
                'warehouse_items': self.warehouse_items[name]
            })
        return result

    def update_warehouse(self, old_name, new_name, new_capacity):
        """Update warehouse name and/or capacity."""
        if old_name not in self.warehouses:
            raise ValueError(f"Warehouse '{old_name}' does not exist")

        warehouse = self.warehouses[old_name]

        # Check if new capacity is valid (can't be smaller than current balance)
        if new_capacity < warehouse.saldo:
            raise ValueError(
                f"New capacity ({new_capacity}) cannot be smaller than "
                f"current balance ({warehouse.saldo})"
            )

        # If name is changing, check if new name already exists
        if old_name != new_name and new_name in self.warehouses:
            raise ValueError(f"Warehouse '{new_name}' already exists")

        # Create new warehouse with the new capacity
        new_warehouse = Varasto(new_capacity, warehouse.saldo)

        # Handle name change
        if old_name != new_name:
            self.warehouses[new_name] = new_warehouse
            self.warehouse_items[new_name] = self.warehouse_items[old_name]
            del self.warehouses[old_name]
            del self.warehouse_items[old_name]
        else:
            self.warehouses[old_name] = new_warehouse

    def add_item(self, warehouse_name, item_name, amount):
        """Add an item to a warehouse."""
        warehouse = self.get_warehouse(warehouse_name)

        # Check if there's enough space
        if amount > warehouse.paljonko_mahtuu():
            raise ValueError(
                f"Not enough space in warehouse. Available: "
                f"{warehouse.paljonko_mahtuu()}, requested: {amount}"
            )

        # Add to warehouse
        warehouse.lisaa_varastoon(amount)

        # Track the item
        items = self.warehouse_items[warehouse_name]
        if item_name in items:
            items[item_name] += amount
        else:
            items[item_name] = amount

    def remove_item(self, warehouse_name, item_name, amount):
        """Remove an item from a warehouse."""
        warehouse = self.get_warehouse(warehouse_name)
        items = self.warehouse_items[warehouse_name]

        if item_name not in items:
            raise ValueError(f"Item '{item_name}' not found in warehouse")

        # Can't remove more than what exists
        if amount > items[item_name]:
            raise ValueError(
                f"Cannot remove {amount} of '{item_name}'. "
                f"Only {items[item_name]} available"
            )

        # Remove from warehouse
        warehouse.ota_varastosta(amount)

        # Update item tracking
        items[item_name] -= amount
        if items[item_name] == 0:
            del items[item_name]
