#! /usr/bin/env python3
import json, os
from settings import *
from datastore import *
from engine import Record
from tests import test_setup, test_instance
from flask import Flask, request, make_response, jsonify, render_template, Response, redirect

app = Flask(__name__)

@app.route('/', methods=['GET'])
def get_root():
    return render_template('steps.html')

@app.route("/prototypes", methods=['GET'])
def get_prototypes():
    prototypes = MagicDB(PROTOTYPE_FILE).all()
    return make_response(jsonify(prototypes))

@app.route("/prototypes/create", methods=['GET'])
def get_prototypes_create():
    return render_template('create_prototypes.html')

@app.route("/prototypes/_incoming", methods=['POST'])
def post_prototypes__incoming():
    data = request.form.to_dict()
    name = data['name']

    # Organize prototype material.
    attributes = { k: None for k in \
        [ data[i] for i in data.keys() if data[i] != ''] \
    if k != name }
    attributes['rules'] = []
    attributes['type'] = name
    obj = {name: attributes}

    # Save prototype material to datastore.
    db = MagicDB(PROTOTYPE_FILE)
    db.update(data=obj[name], key=name)
    return redirect('/')

@app.route("/calculation", methods=['GET'])
def get_calculation():
    calculations = MagicDB(CALCULATION_FILE).all()
    return make_response(jsonify(calculations))

@app.route("/calculation/create", methods=['GET'])
def get_calculation_create():
    prototypes = MagicDB(PROTOTYPE_FILE).all()
    return render_template('create_calculations.html', prototypes=prototypes)

@app.route('/calculation/_incoming', methods=['POST'])
def post_cacluation__incoming():
    data = request.form.to_dict()
    name = data['name']
    apply_to = data['object']
    categories = ['static', 'attribute', 'operator']

    # Organize calculation material.
    result = [ [ {'source': cat, 'value': i[1], 'position':i[0].split('_')[2]} \
            for i in \
            [ i for i in list(data.items())\
                if i[0][0:4] == cat[0:4] and i[1] != '' ]
        ] for cat in categories ]
    result = {
        'name': name,
        'type': 'calc',
        'data': ''.join([ i['value'] for i in sorted(
            [ inner for outer in result for inner in outer ],
            key=lambda x: int(x['position'])) ])
    }
    # Save calculation material.
    MagicDB(CALCULATION_FILE).update(data=result, key=name)

    # Conditionally add calculation reference to prototype.
    if data['contingent'] == 'FALSE':
        db = MagicDB(PROTOTYPE_FILE)
        prototypes = db.all()
        prototypes[apply_to]['rules'].append(name)
        db.write(to_write=prototypes)
    return redirect('/')

@app.route("/rules", methods=['GET'])
def get_rules():
    rules = MagicDB(RULES_FILE).all()
    return make_response(jsonify(rules))

@app.route("/rules/create", methods=['GET'])
def get_rules_create():
    prototypes = MagicDB(PROTOTYPE_FILE).all()
    calculations = MagicDB(CALCULATION_FILE).all()
    return render_template(
        'create_rules.html',
        prototypes=prototypes,
        calculations=calculations)

@app.route("/rules/_incoming", methods=['POST'])
def post_rules__incoming():
    data = request.form.to_dict()
    apply_to = data['object']
    name = data['name']

    # Organize rule material.
    if data['concur_static'] != '':
        concur = data['concur_static']
    else:
        concur = data['concur_calc']
    if data['not_concur_static'] != '':
        not_concur = data['not_concur_static']
    else:
        not_concur = data['not_concur_calc']
    data = {
        name: {
                'name': name,
                'type': 'logic',
                "compare_value": data['compare_value'],
                "attribute": data['attribute'],
                "concur": concur,
                "not_concur": not_concur,
                "operator": data['operator']
            }
    }

    # Update any affected prototypes.
    db = MagicDB(PROTOTYPE_FILE)
    prototypes = db.all()
    prototypes[apply_to]['rules'].append(name)
    db.write(prototypes)

    # Save rule material.
    db = MagicDB(RULES_FILE)
    db.update(data=data[name], key=name)
    return redirect('/')

@app.route("/data", methods=['GET'])
def get_data():
    data = MagicDB(DATA_FILE).all()
    return make_response(jsonify(data))

@app.route("/data/view", methods=['GET'])
def get_data_view():
    data = MagicDB(DATA_FILE).all()
    return render_template('view_data.html', data=data)

@app.route("/data/create", methods=['GET'])
def get_data_create():
    prototypes = MagicDB(PROTOTYPE_FILE).all()
    return render_template('create_data.html', prototypes=prototypes)

@app.route("/data/_incoming", methods=['POST'])
def post_data__incoming():
    data = request.form.to_dict()
    record = Record(data)
    record.calculate_instance()
    record.save()
    return redirect('/data/view')

@app.route('/clear/rules', methods=['GET'])
def get_clear_rules():
    for i in [PROTOTYPE_FILE, RULES_FILE, CALCULATION_FILE]:
        with open(i, 'w') as outfile:
            outfile.write(json.dumps({}))
    return redirect('/')

@app.route('/clear/data', methods=['GET'])
def get_clear_data():
    with open(DATA_FILE, 'w') as outfile:
        outfile.write(json.dumps([]))
    return redirect('/')

if __name__ == '__main__':
    try:
        port = int(os.getenv("PORT"))
        app.run(host='0.0.0.0', port=port, threaded=True)
    except TypeError:
        app.run(debug=True, threaded=True)
