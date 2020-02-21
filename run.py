from quart import Quart, jsonify, request

# create app 
app = Quart(__name__)
consume = {
    'users': [],
    'meta': {
        'consumed': 0,
        'total': 0
    }
}


#
# Route for consume value
@app.route('/resume', methods=['GET'])
async def resume():
    return jsonify(consume), 200

#
# Route for add user
@app.route('/user', methods=['POST'])
async def add_user():
    if not request.is_json:
        return jsonify({'error': 'data should be in json'}), 400

    data = await request.get_json()
    if 'name' not in data:
        return jsonify({'error': 'name field not found'}), 400

    user = {
        'id': len(consume['users']),
        'name': data['name'],
        'selected': False,
        'consumed': 0
    }
    consume['users'].append(user)
    return jsonify(user), 201

#
# Route for select user
@app.route('/select/<int:user_id>', methods=['POST'])
async def select_user(user_id):
    if user_id > (len(consume['users']) - 1):
        return jsonify({'error': f'invalid id {user_id}'}), 404

    # Select new user
    for user in consume['users']:
        user['selected'] = user['id'] == user_id

    return jsonify(consume['users'][user_id]), 200

#
# Route for reset
@app.route('/reset', methods=['POST'])
async def reset_user():
    if not request.is_json:
        return jsonify({'error': 'data should be in json'}), 400

    data = await request.get_json()
    if 'total' not in data:
        return jsonify({'error': 'total field not found'}), 400

    consume['users'] = []
    consume['meta'] = {
        'total': data['total'],
        'consumed': 0
    }
    return jsonify(consume), 200


# Start application
app.run(host='0.0.0.0', port=8000)
