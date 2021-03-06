from quart import Quart, jsonify, request, Response
import chopp

# create app 
app = Quart(__name__)
chopp_flow = chopp.ChoppFlow(16)

def add_cors(resp):
    resp.headers['Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept, Authorization, If-Match'
    resp.headers['Access-Control-Allow-Methods'] = '*'
    resp.headers['Access-Control-Max-Age'] = '86400'
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Credentials'] = True
    resp.headers['Content-Type'] = 'application/json'

#
# Route for consume value
@app.route('/resume', methods=['GET', 'OPTIONS'])
async def resume():
    resp = None
    if request.method == 'OPTIONS':
        resp = Response('')
    else:
        resp = jsonify(chopp_flow.to_json())
        resp.status_code = 200
    add_cors(resp)
    return resp

#
# Route for add user
@app.route('/user', methods=['POST', 'OPTIONS'])
async def add_user():
    if request.method == 'OPTIONS':
        resp = Response('')
        add_cors(resp)
        return resp
    
    if not request.is_json:
        resp = jsonify({'error': 'data should be in json'})
        resp.status_code = 400
        add_cors(resp)
        return resp

    data = await request.get_json()
    if 'name' not in data:
        resp = jsonify({'error': 'name field not found'})
        resp.status_code = 400
        add_cors(resp)
        return resp

    user = {
        'id': len(chopp_flow.consumers),
        'name': data['name'],
        'selected': False,
        'consumed': 0
    }
    chopp_flow.consumers.append(user)
    resp = jsonify(user)
    add_cors(resp)
    return resp

#
# Route for select user
@app.route('/select/<int:user_id>', methods=['POST', 'OPTIONS'])
async def select_user(user_id):
    if request.method == 'OPTIONS':
        resp = Response('')
        add_cors(resp)
        return resp

    if user_id > (len(chopp_flow.consumers) - 1):
        resp = jsonify({'error': f'invalid id {user_id}'})
        resp.status_code = 404
        add_cors(resp)
        return resp

    # Select new user
    last_id = chopp_flow.selected_user
    if last_id != -1:
        chopp_flow.consumers[last_id]['selected'] = False
    # Select user
    chopp_flow.consumers[user_id]['selected'] = True
    chopp_flow.selected_user = user_id

    resp = jsonify(chopp_flow.consumers[user_id])
    resp.status_code = 200
    add_cors(resp)
    return resp

#
# Route for reset
@app.route('/reset', methods=['POST', 'OPTIONS'])
async def reset_all():
    global chopp_flow
    if request.method == 'OPTIONS':
        resp = Response('')
        add_cors(resp)
        return resp

    if not request.is_json:
        resp = jsonify({'error': 'data should be in json'})
        resp.status_code = 400
        add_cors(resp)
        return resp

    data = await request.get_json()
    if 'total' not in data:
        resp = jsonify({'error': 'total field not found'})
        resp.status_code = 400
        add_cors(resp)
        return resp

    chopp_flow.stop()
    # We cannot restart a stopped thread
    # So we create another object
    chopp_flow = chopp.ChoppFlow(16)
    chopp_flow.start()
    chopp_flow.total = data['total']

    resp = jsonify(chopp_flow.to_json())
    resp.status_code = 200
    add_cors(resp)
    return resp


# Start application
app.run(host='0.0.0.0', port=8000)
