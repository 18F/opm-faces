#! /usr/bin/env python3
import json, os
from settings import *
from datastore import *
from views import *
from tests import test_setup, test_instance
from flask import Flask, request, make_response, jsonify, render_template, Response, redirect

app = Flask(__name__)

@app.route('/api', methods=['GET'])
def get_api_root():
    return make_response(jsonify(get_api_data()))

@app.route('/api/prototypes/read', methods=['GET'])
def api_get_prototypes():
    prototypes = MagicDB(PROTOTYPE_FILE).all()
    return make_response(jsonify(prototypes))

@app.route("/api/prototypes/write", methods=['POST'])
def api_post_prototypes__incoming():
    """
    Structure for POST data:
        {
            "name": "",
            "attribute_0": "",
            "attribute_1": "",
            "attribute_2": "",
            "attribute_3": "",
            "attribute_4": "",
            ...
        }
    Example call and response:
    curl -H "Content-Type: application/json" -X POST -d '{"name":"animal","attribute_0":"height"}' http://127.0.0.1:5000/api/prototypes/write

    {
      "animal": {
        "height": null,
        "rules": [],
        "type": "animal"
      }
    }
    """
    data = process_incoming_prototype(request.json)
    return make_response(jsonify(data[1]))

@app.route("/api/calculations/read", methods=['GET'])
def api_get_calculation():
    calculations = MagicDB(CALCULATION_FILE).all()
    return make_response(jsonify(calculations))

@app.route('/api/calculations/write', methods=['POST'])
def api_post_cacluation__incoming():
    """
    Structure for POST data:
        {
            "object": "",
            "name": "",
            "contingent": "",
            "static_value_0": "",
            "attribute_value_0": "",
            "operator_value_0": "",
            "static_value_1": "",
            "attribute_value_1": "",
            "operator_value_1": "",
            "static_value_2": "",
            "attribute_value_2": "",
            "operator_value_2": "",
            "attribute_value_3": "",
            "static_value_3": "",
            "operator_value_3": "",
            "static_value_4": "",
            "attribute_value_4": "",
            "operator_value_4": "",
            "static_value_5": "",
            "attribute_value_5": "",
            ...
        }
    Example call and response:
    curl -H "Content-Type: application/json" -X POST -d '{"name":"double_height", "object":"animal", "contingent": "TRUE", "static_value_0":"2", "attribute_value_0":"", "operator_value_0":"*","static_value_1":"", "attribute_value_1":"__height__"}' http://127.0.0.1:5000/api/calculations/write

    {
      "data": "2*__height__",
      "name": "double_height",
      "type": "calc"
    }
    """
    data = process_incoming_calculation(request.json)
    return make_response(jsonify(data[1]))

@app.route("/api/rules/read", methods=['GET'])
def api_get_rules():
    rules = MagicDB(RULES_FILE).all()
    return make_response(jsonify(rules))

@app.route("/api/rules/write", methods=['POST'])
def api_post_rules__incoming():
    """
    Structure for POST data:
        {
            "name": "",
            "object": "",
            "operator": ""
            "attribute": "",
            "compare_value": "",
            "concur_static": "",
            "concur_calc": "",
            "not_concur_calc": "",
            "not_concur_static": "",
        }
    Example call and response:
    curl -H "Content-Type: application/json" -X POST -d '{"name":"test_tall", "object":"animal", "operator":"<=", "attribute":"height", "compare_value":"5", "concur_static":"", "concur_calc":"_double_height", "not_concur_static":"tall enough already", "not_concur_calc":""}' http://127.0.0.1:5000/api/rules/write

    {
      "test_tall": {
        "attribute": "height",
        "compare_value": "5",
        "concur": "_double_height",
        "name": "test_tall",
        "not_concur": "tall enough already",
        "operator": "<=",
        "type": "logic"
      }
    }
    """
    data = process_incoming_rules(request.json)
    return make_response(jsonify(data[1]))

@app.route("/api/data/read", methods=['GET'])
def api_get_data():
    data = MagicDB(DATA_FILE).all()
    return make_response(jsonify(data))

@app.route("/api/data/write", methods=['POST'])
def api_post_data__incoming():
    """
    Structure for POST data:
        {
            "type": "",
            ... # Any attributes available from the prototype.

        }
    Example call and response:
    curl -H "Content-Type: application/json" -X POST -d '{"type":"animal","height":"4"}' http://127.0.0.1:5000/api/data/write

    {
      "height": "4",
      "rules": [
        "test_tall"
      ],
      "test_tall": "8",
      "type": "animal"
    }

    """
    data = process_incoming_data(request.json)
    return make_response(jsonify(data[1]))

@app.route('/', methods=['GET'])
def get_root():
    return render_template('steps.html')

@app.route("/prototypes/create", methods=['GET'])
def get_prototypes_create():
    return render_template('create_prototypes.html')

@app.route("/prototypes/_incoming", methods=['POST'])
def post_prototypes__incoming():
    data = process_incoming_prototype(request.form.to_dict())
    return redirect('/')

@app.route("/calculations/create", methods=['GET'])
def get_calculation_create():
    prototypes = MagicDB(PROTOTYPE_FILE).all()
    return render_template('create_calculations.html', prototypes=prototypes)

@app.route('/calculations/_incoming', methods=['POST'])
def post_cacluation__incoming():
    data = process_incoming_calculation(request.form.to_dict())
    return redirect('/')

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
    data = process_incoming_rules(request.form.to_dict())
    return redirect('/')

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
    data = process_incoming_data(request.form.to_dict())
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
