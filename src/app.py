from flask import Flask, render_template, request, redirect, url_for, flash
from warehouse_manager import WarehouseManager

app = Flask(__name__)
app.secret_key = 'warehouse-secret-key-change-in-production'

# Global warehouse manager instance
warehouse_manager = WarehouseManager()


@app.route('/')
def index():
    """Display all warehouses and their items."""
    warehouses = warehouse_manager.get_all_warehouses()
    return render_template('index.html', warehouses=warehouses)


@app.route('/warehouse/create', methods=['GET', 'POST'])
def create_warehouse():  # pylint: disable=too-many-statements
    """Create a new warehouse."""
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        capacity = request.form.get('capacity', '').strip()

        try:
            capacity_float = float(capacity)
            if capacity_float <= 0:
                flash('Capacity must be greater than 0', 'error')
                return render_template('create_warehouse.html')

            warehouse_manager.create_warehouse(name, capacity_float)
            flash(f"Warehouse '{name}' created successfully!", 'success')
            return redirect(url_for('index'))
        except ValueError as e:
            flash(str(e), 'error')
            return render_template('create_warehouse.html')

    return render_template('create_warehouse.html')


@app.route('/warehouse/<warehouse_name>/edit', methods=['GET', 'POST'])
def edit_warehouse(warehouse_name):  # pylint: disable=too-many-statements
    """Edit a warehouse's name and capacity."""
    if request.method == 'POST':
        new_name = request.form.get('name', '').strip()
        new_capacity = request.form.get('capacity', '').strip()

        try:
            capacity_float = float(new_capacity)
            if capacity_float <= 0:
                flash('Capacity must be greater than 0', 'error')
                warehouse = warehouse_manager.get_warehouse(warehouse_name)
                return render_template('edit_warehouse.html',
                                       warehouse_name=warehouse_name,
                                       capacity=warehouse.tilavuus)

            warehouse_manager.update_warehouse(
                warehouse_name, new_name, capacity_float
            )
            flash("Warehouse updated successfully!", 'success')
            return redirect(url_for('index'))
        except ValueError as e:
            flash(str(e), 'error')
            warehouse = warehouse_manager.get_warehouse(warehouse_name)
            return render_template('edit_warehouse.html',
                                   warehouse_name=warehouse_name,
                                   capacity=warehouse.tilavuus)

    try:
        warehouse = warehouse_manager.get_warehouse(warehouse_name)
        return render_template('edit_warehouse.html',
                               warehouse_name=warehouse_name,
                               capacity=warehouse.tilavuus)
    except ValueError as e:
        flash(str(e), 'error')
        return redirect(url_for('index'))


@app.route('/warehouse/<warehouse_name>/delete', methods=['POST'])
def delete_warehouse(warehouse_name):
    """Delete a warehouse."""
    try:
        warehouse_manager.delete_warehouse(warehouse_name)
        flash(f"Warehouse '{warehouse_name}' deleted successfully!", 'success')
    except ValueError as e:
        flash(str(e), 'error')
    return redirect(url_for('index'))


@app.route('/warehouse/<warehouse_name>/add_item', methods=['GET', 'POST'])
def add_item(warehouse_name):  # pylint: disable=too-many-statements
    """Add an item to a warehouse."""
    if request.method == 'POST':
        item_name = request.form.get('item_name', '').strip()
        amount = request.form.get('amount', '').strip()

        try:
            amount_float = float(amount)
            if amount_float <= 0:
                flash('Amount must be greater than 0', 'error')
                return render_template(
                    'add_item.html', warehouse_name=warehouse_name
                )

            warehouse_manager.add_item(
                warehouse_name, item_name, amount_float
            )
            flash(f"Item '{item_name}' added successfully!", 'success')
            return redirect(url_for('index'))
        except ValueError as e:
            flash(str(e), 'error')
            return render_template(
                'add_item.html', warehouse_name=warehouse_name
            )

    return render_template('add_item.html', warehouse_name=warehouse_name)


@app.route('/warehouse/<warehouse_name>/remove_item', methods=['GET', 'POST'])
def remove_item(warehouse_name):  # pylint: disable=too-many-statements
    """Remove an item from a warehouse."""
    try:
        items = warehouse_manager.warehouse_items[warehouse_name]
    except (ValueError, KeyError) as e:
        flash(str(e), 'error')
        return redirect(url_for('index'))

    if request.method == 'POST':
        item_name = request.form.get('item_name', '').strip()
        amount = request.form.get('amount', '').strip()

        try:
            amount_float = float(amount)
            if amount_float <= 0:
                flash('Amount must be greater than 0', 'error')
                return render_template('remove_item.html',
                                       warehouse_name=warehouse_name,
                                       items=items)

            warehouse_manager.remove_item(
                warehouse_name, item_name, amount_float
            )
            flash(f"Item '{item_name}' removed successfully!", 'success')
            return redirect(url_for('index'))
        except ValueError as e:
            flash(str(e), 'error')
            return render_template('remove_item.html',
                                   warehouse_name=warehouse_name,
                                   items=items)

    return render_template('remove_item.html',
                           warehouse_name=warehouse_name,
                           items=items)


if __name__ == '__main__':
    app.run(debug=True)
