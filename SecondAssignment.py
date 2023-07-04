from flask import Flask, jsonify, request

app = Flask(__name__)

data = {}

@app.route('/create', methods=['POST'])
def create():
    req_data = request.get_json()
    key = req_data.get('key')
    value = req_data.get('value')
    data[key] = value
    return jsonify({'message': 'Entry created successfully'})

@app.route('/read', methods=['GET'])
def read():
    return jsonify(data)

@app.route('/update', methods=['POST'])
def update():
    req_data = request.get_json()
    key = req_data.get('key')
    value = req_data.get('value')
    if key in data:
        data[key] = value
        return jsonify({'message': 'Entry updated successfully'})
    else:
        return jsonify({'error': 'Entry not found'})

@app.route('/delete', methods=['POST'])
def delete():
    req_data = request.get_json()
    key = req_data.get('key')
    if key in data:
        del data[key]
        return jsonify({'message': 'Entry deleted successfully'})
    else:
        return jsonify({'error': 'Entry not found'})

if __name__ == '__main__':
    app.run()
