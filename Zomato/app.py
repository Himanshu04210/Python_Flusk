from flask import Flask, request, json, jsonify
from flask_mysqldb import MySQL
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'db11'

mysql = MySQL(app)

def create_tables():
    with app.app_context():
        cursor = mysql.connection.cursor()

        # Check if 'dishes' table exists
        cursor.execute("SHOW TABLES LIKE 'dishes'")
        table_exists = cursor.fetchone()

        if not table_exists:
            create_dishes_table_query = """
            CREATE TABLE dishes (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                price DECIMAL(8, 2) NOT NULL,
                availability BOOLEAN NOT NULL DEFAULT TRUE
            )
            """

            cursor.execute(create_dishes_table_query)
            # Add other table creation queries here...

            mysql.connection.commit()

        cursor.close()


@app.before_request
def initialize():
    create_tables()


@app.route('/menu', methods=['GET'])
def get_menu():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM dishes")
    result = cursor.fetchall()
    cursor.close()
    # Convert the query result to JSON using json.dumps()
    return json.dumps(result)

@app.route('/menu', methods=['POST'])
def add_dish():
    dish = request.get_json()
    cursor = mysql.connection.cursor()
    cursor.execute(
        "INSERT INTO dishes (name, price, availability) VALUES (%s, %s, %s)",
        (dish['name'], dish['price'], dish['availability'])
    )
    mysql.connection.commit()
    cursor.close()
    # Return a JSON response with a success message
    return jsonify({'message': 'Dish added successfully'})

@app.route('/menu/<int:dish_id>', methods=['GET'])
def get_dish(dish_id):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM dishes WHERE id = %s", (dish_id,))
    result = cursor.fetchone()
    cursor.close()
    # Convert the query result to JSON using json.dumps()
    return json.dumps(result)

@app.route('/menu/<int:dish_id>', methods=['PUT'])
def update_dish(dish_id):
    dish = request.get_json()
    cursor = mysql.connection.cursor()
    cursor.execute(
        "UPDATE dishes SET name = %s, price = %s, availability = %s WHERE id = %s",
        (dish['name'], dish['price'], dish['availability'], dish_id)
    )
    mysql.connection.commit()
    cursor.close()
    # Return a JSON response with a success message
    return jsonify({'message': 'Dish updated successfully'})

@app.route('/menu/<int:dish_id>', methods=['DELETE'])
def delete_dish(dish_id):
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM dishes WHERE id = %s", (dish_id,))
    mysql.connection.commit()
    cursor.close()
    # Return a JSON response with a success message
    return jsonify({'message': 'Dish deleted successfully'})



@app.route('/place-order', methods=['POST'])
def place_order():
    order_data = request.get_json()
    customer_name = order_data.get('customerName')
    dish_ids = order_data.get('dishIds')

    # Validate the order data
    if not customer_name or not dish_ids:
        return jsonify({'error': 'Invalid order data'})

    cursor = mysql.connection.cursor()
    
    # Check dish availability and calculate total price
    total_price = 0
    for dish_id in dish_ids:
        cursor.execute("SELECT * FROM dishes WHERE id = %s", (dish_id,))
        dish = cursor.fetchone()
        if not dish or not dish[3]:
            return jsonify({'error': 'Invalid dish ID or dish not available'})
        total_price += dish[2]

    # Generate the order ID
    global order_id_counter
    order_id = order_id_counter
    order_id_counter += 1

    # Process the order and set the initial status to 'received'
    status = 'received'

    # Save the order
    cursor.execute(
        "INSERT INTO orders (orderId, customerName, dishIds, totalPrice, status) VALUES (%s, %s, %s, %s, %s)",
        (order_id, customer_name, json.dumps(dish_ids), total_price, status)
    )
    mysql.connection.commit()
    cursor.close()

    # Return the order details as the response
    order = {
        'orderId': order_id,
        'customerName': customer_name,
        'dishIds': dish_ids,
        'totalPrice': total_price,
        'status': status
    }
    return jsonify(order)

if __name__ == '__main__':
    app.run()
