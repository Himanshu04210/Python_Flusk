import json
from flask import Flask, jsonify, request

DISHES_FILE = 'dishes.json'
ORDERS_FILE = 'orders.json'
app = Flask(__name__)
app.secret_key = 'Kirti@1807'

def load_data(file_name):
    try:
        with open(file_name, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        data = []
    return data

def save_data(data, file_name):
    with open(file_name, 'w') as file:
        json.dump(data, file, indent=4)

dishes = load_data(DISHES_FILE)
orders = load_data(ORDERS_FILE)
order_id_counter = max(order['id'] for order in orders if 'id' in order) if orders else 0

def get_next_order_id():
    global order_id_counter
    order_id_counter += 1
    return order_id_counter

def get_dish_by_id(dish_id):
    return next((dish for dish in dishes if dish['id'] == dish_id), None)

@app.route('/dishes', methods=['GET'])
def get_dishes():
    return jsonify(dishes)

@app.route('/dishes/<int:dish_id>', methods=['GET'])
def get_dish(dish_id):
    dish = get_dish_by_id(dish_id)
    if dish:
        return jsonify(dish)
    else:
        return jsonify({'error': 'Dish not found'}), 404

@app.route('/dishes', methods=['POST'])
def create_dish():
    new_dish = {
        'id': get_next_order_id(),
        'name': request.json['name'],
        'price': request.json['price'],
        'availability': bool(request.json['availability'])
    }
    dishes.append(new_dish)
    save_data(dishes, DISHES_FILE)
    return jsonify(new_dish), 201

@app.route('/dishes/<int:dish_id>', methods=['PUT'])
def update_dish(dish_id):
    dish = get_dish_by_id(dish_id)
    if dish:
        dish['name'] = request.json.get('name', dish['name'])
        dish['price'] = request.json.get('price', dish['price'])
        dish['availability'] = bool(request.json.get('availability', dish['availability']))
        save_data(dishes, DISHES_FILE)
        return jsonify(dish)
    else:
        return jsonify({'error': 'Dish not found'}), 404

@app.route('/dishes/<int:dish_id>', methods=['DELETE'])
def delete_dish(dish_id):
    dish = get_dish_by_id(dish_id)
    if dish:
        dishes.remove(dish)
        save_data(dishes, DISHES_FILE)
        return jsonify({'message': 'Dish deleted'})
    else:
        return jsonify({'error': 'Dish not found'}), 404

@app.route('/orders', methods=['POST'])
def create_order():
    try:
        # Retrieve the request data
        data = request.get_json()

        # Add an ID to the new order
        order_id = get_next_order_id()
        data['id'] = order_id

        # Calculate total price for the order
        total_price = 0
        for item in data['items']:
            dish = get_dish_by_id(item['dish_id'])
            if dish:
                total_price += dish['price'] * item['quantity']
        
        data['total_price'] = total_price

        # Add the new order to the orders list
        orders.append(data)
        
        # Save the updated orders to file
        save_data(orders, ORDERS_FILE)

        return jsonify({'message': 'Order created successfully', 'order_id': order_id}), 201
    except Exception as e:
        return jsonify({'error': 'Internal Server Error'})

@app.route('/orders/<int:order_id>', methods=['PUT'])
def update_order(order_id):
    new_status = request.json.get('status', '')
    order = next((order for order in orders if order['id'] == order_id), None)
    if order:
        order['status'] = new_status
        save_data(orders, ORDERS_FILE)
        return jsonify(order)
    else:
        return jsonify({'error': 'Order not found'}), 404

@app.route('/orders', methods=['GET'])
def get_orders():
    try:
        # Retrieve orders from the file
        orders = load_data(ORDERS_FILE)

        # Check if a status filter is provided in the query parameters
        status = request.args.get('status')
        if status:
            filtered_orders = [order for order in orders if order['status'] == status]
        else:
            filtered_orders = orders

        return jsonify(filtered_orders)
    except Exception as e:
        return jsonify({'error': 'Internal Server Error'})

if __name__ == '__main__':
    app.run(port=5000, debug=True)
