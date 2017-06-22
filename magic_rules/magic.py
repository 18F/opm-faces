#! /usr/bin/env python3
import json, os
from settings import *
from engine import RulesInstance, ObjectPrototype, ObjectInstance
from tests import test_setup, test_instance
from flask import Flask, request, make_response, jsonify, render_template, Response, redirect

app = Flask(__name__)

@app.route('/', methods=['GET'])
def get_root():
    return render_template('steps.html')

@app.route("/prototypes", methods=['GET'])
def get_prototypes():
    with open(OBJECT_FILE) as infile:
        return make_response(jsonify(infile.read()))

@app.route("/prototypes/create", methods=['GET'])
def get_prototypes_create():
    return render_template('create_prototypes.html')

@app.route("/prototypes/_incoming", methods=['POST'])
def post_prototypes__incoming():
    data = request.form.to_dict()
    name = data['name']
    attributes = { k: None for k in \
        [ data[i] for i in data.keys() if data[i] != ''] \
    if k != name }
    attributes['rules'] = []
    attributes['type'] = name
    obj = {name: attributes}
    with open(OBJECT_FILE, 'r') as infile:
        objects = json.loads(infile.read())
    objects[name] = obj[name]
    with open(OBJECT_FILE, 'w') as outfile:
        outfile.write(json.dumps(objects, indent=4))
    return redirect('/')

@app.route("/calculation", methods=['GET'])
def get_calculation():
    with open(CALCULATION_FILE) as infile:
        return make_response(jsonify(infile.read()))

@app.route("/calculation/create", methods=['GET'])
def get_calculation_create():
    with open(OBJECT_FILE, 'r') as infile:
        objects = json.loads(infile.read())
    return render_template('create_calculations.html', objects=objects)

@app.route('/calculation/_incoming', methods=['POST'])
def post_cacluation__incoming():
    data = request.form.to_dict()
    name = data['name']
    apply_to = data['object']
    categories = ['static', 'attribute', 'operator']
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
    with open(CALCULATION_FILE, 'r') as infile:
        calculations = json.loads(infile.read())
    calculations[name] = result
    with open(CALCULATION_FILE, 'w') as outfile:
        outfile.write(json.dumps(calculations, indent=4))
    # Conditionally add calculation reference to prototype.
    if data['contingent'] == 'FALSE':
        with open(OBJECT_FILE, 'r') as infile:
            objects = json.loads(infile.read())
        objects[apply_to]['rules'].append(name)
        with open(OBJECT_FILE, 'w') as outfile:
            outfile.write(json.dumps(objects, indent=4))
    return redirect('/')

@app.route("/rules", methods=['GET'])
def get_rules():
    with open(RULES_FILE) as infile:
        return make_response(jsonify(infile.read()))

@app.route("/rules/create", methods=['GET'])
def get_rules_create():
    with open(OBJECT_FILE, 'r') as infile:
        objects = json.loads(infile.read())
    with open(CALCULATION_FILE, 'r') as infile:
        calculations = json.loads(infile.read())
    return render_template(
        'create_rules.html',
        objects=objects,
        calculations=calculations)

@app.route("/rules/_incoming", methods=['POST'])
def post_rules__incoming():
    data = request.form.to_dict()
    apply_to = data['object']
    name = data['name']
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
    with open(OBJECT_FILE, 'r') as infile:
        objects = json.loads(infile.read())
    objects[apply_to]['rules'].append(name)
    with open(OBJECT_FILE, 'w') as outfile:
        outfile.write(json.dumps(objects, indent=4))
    rules = RulesInstance(data)
    rules.save_rule()
    return redirect('/')

@app.route("/data", methods=['GET'])
def get_data():
    with open(DATA_FILE) as infile:
        return make_response(jsonify(infile.read()))

@app.route("/data/view", methods=['GET'])
def get_data_view():
    with open(DATA_FILE, 'r') as infile:
        data = json.loads(infile.read())
    return render_template('view_data.html', data=data)

@app.route("/data/create", methods=['GET'])
def get_data_create():
    with open(OBJECT_FILE, 'r') as infile:
        objects = json.loads(infile.read())
    return render_template('create_data.html', objects=objects)

@app.route("/data/_incoming", methods=['POST'])
def post_data__incoming():
    data = request.form.to_dict()
    record = ObjectInstance(data)
    record.populate_instance()
    record.calculate_instance()
    record.save_record()
    return redirect('/data/view')

@app.route('/clear/rules', methods=['GET'])
def get_clear_rules():
    for i in [OBJECT_FILE, RULES_FILE, CALCULATION_FILE]:
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
