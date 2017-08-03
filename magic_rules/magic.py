#! /usr/bin/env python3
import json, os
from settings import *
from datastore import *
from views import *
from flask import Flask, request, make_response, jsonify, render_template, Response, redirect

app = Flask(__name__)

@app.route('/api', methods=['GET'])
def get_api_root():
    return make_response(jsonify(get_api_data()))

@app.route('/api/prototypes/<action>', methods=['GET', 'POST'])
def api_get_prototypes(action):
    if action == 'read':
        prototypes = MagicDB(PROTOTYPE_FILE).all()
        return make_response(jsonify(prototypes))
    elif action == 'write':
        data = process_incoming_prototype(request.get_json())
        return make_response(jsonify(data[1]))
    else:
        return make_response('Not found.')

@app.route("/api/calculations/<action>", methods=['GET', 'POST'])
def api_get_calculation(action):
    if action == 'read':
        calculations = MagicDB(CALCULATION_FILE).all()
        return make_response(jsonify(calculations))
    elif action == 'write':
        data = process_incoming_calculation(request.get_json())
        return make_response(jsonify(data[1]))
    else:
        return make_response('Not found.')

@app.route("/api/rules/<action>", methods=['GET', 'POST'])
def api_get_rules(action):
    if action == 'read':
        rules = MagicDB(RULES_FILE).all()
        return make_response(jsonify(rules))
    elif action == 'write':
        data = process_incoming_rules(request.get_json())
        return make_response(jsonify(data[1]))
    else:
        return make_response('Not found.')

@app.route("/api/data/<action>", methods=['GET', 'POST'])
def api_get_data(action):
    if action == 'read':
        data = MagicDB(DATA_FILE).all()
        return make_response(jsonify(data))
    elif action == 'write':
        data = process_incoming_data(request.get_json())
        return make_response(jsonify(data[1]))
    else:
        return make_response('Not found.')

@app.route('/', methods=['GET'])
def get_root():
    return render_template('steps.html')

@app.route("/prototypes/<action>", methods=['GET', 'POST'])
def get_prototypes(action):
    if action == 'create':
        return render_template('create_prototypes.html')
    elif action == 'view':
        return make_response(jsonify(MagicDB(PROTOTYPE_FILE).all()))
    elif action == '_incoming':
        data = process_incoming_prototype(request.form.to_dict())
        return redirect('/')
    elif action == 'clear':
        with open(PROTOTYPE_FILE, 'w') as outfile:
            outfile.write(json.dumps({}))
        return redirect('/')
    else:
        return make_response('Not found.')

@app.route("/calculations/<action>", methods=['GET', 'POST'])
def get_calculation(action):
    if action == 'create':
        prototypes = MagicDB(PROTOTYPE_FILE).all()
        return render_template('create_calculations.html',
        prototypes=prototypes)
    elif action == 'view':
        return make_response(jsonify(MagicDB(CALCULATION_FILE).all()))
    elif action == '_incoming':
        data = process_incoming_calculation(request.form.to_dict())
        return redirect('/')
    elif action == 'clear':
        with open(CALCULATION_FILE, 'w') as outfile:
            outfile.write(json.dumps({}))
        return redirect('/')
    else:
        return make_response('Not found.')

@app.route("/rules/<action>", methods=['GET', 'POST'])
def get_rules(action):
    if action == 'create':
        prototypes = MagicDB(PROTOTYPE_FILE).all()
        calculations = MagicDB(CALCULATION_FILE).all()
        return render_template(
            'create_rules.html', prototypes=prototypes,
            calculations=calculations)
    elif action == 'view':
        return make_response(jsonify(MagicDB(RULES_FILE).all()))
    elif action == '_incoming':
        data = process_incoming_rules(request.form.to_dict())
        return redirect('/')
    elif action == 'clear':
        with open(RULES_FILE, 'w') as outfile:
            outfile.write(json.dumps({}))
        return redirect('/')
    else:
        return make_response('Not found.')

@app.route("/data/<action>", methods=['GET', 'POST'])
def get_data(action):
    if action == 'view':
        data = MagicDB(DATA_FILE).all()
        return render_template('view_data.html', data=data)
    elif action == 'create':
        prototypes = MagicDB(PROTOTYPE_FILE).all()
        return render_template('create_data.html', prototypes=prototypes)
    elif action == '_incoming':
        data = process_incoming_data(request.form.to_dict())
        return redirect('/data/view')
    elif action == 'clear':
        with open(DATA_FILE, 'w') as outfile:
            outfile.write(json.dumps([]))
        return redirect('/')
    else:
        return make_response('Not found.')

if __name__ == '__main__':
    try:
        port = int(os.getenv("PORT"))
        app.run(host='0.0.0.0', port=port, threaded=True)
    except TypeError:
        app.run(debug=True, threaded=True)
