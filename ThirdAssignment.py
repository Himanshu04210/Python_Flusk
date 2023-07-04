from flask import Flask, jsonify, request

menu = ['Pasta', 'Pizza', 'Burger', 'Salad']

app = Flask(__name__)

@app.route("/")
def home():
    return "Welcome to Zesty Zomato!"

@app.route('/menu')
def display_menu():
    return str(menu)

@app.route('/add_dish', methods=['POST'])
def add_dish():
    dish = request.form['dish']
    menu.append(dish)
    return "Dish '{}' added to the menu.".format(dish)

@app.route('/remove_dish', methods=['POST'])
def remove_dish():
    dish = request.form['dish']
    if dish in menu:
        menu.remove(dish)
        return "Dish '{}' removed from the menu.".format(dish)
    else:
        return "Dish '{}' not found in the menu.".format(dish)

if __name__ == '__main__':
    app.run(debug=True)
