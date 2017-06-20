#! /usr/bin/env python3
import json, os
from settings import *
from engine import RulesInstance
from tests import test_setup, test_instance
from flask import Flask, request, make_response, jsonify, render_template, Response, redirect

app = Flask(__name__)

@app.route("/rules", methods=['GET'])
def get_rules():
    with open(RULES_FILE) as infile:
        return make_response(jsonify(infile.read()))

@app.route("/prototypes", methods=['GET'])
def get_prototypes():
    with open(OBJECT_FILE) as infile:
        return make_response(jsonify(infile.read()))

@app.route("/data", methods=['GET'])
def get_data():
    with open(DATA_FILE) as infile:
        return make_response(jsonify(infile.read()))

@app.route("/rules/create", methods=['GET'])
def get_rules_create():
    with open(OBJECT_FILE, 'r') as infile:
        objects = list(json.loads(infile.read()).keys())
    return render_template('create_rules.html', objects=objects)

@app.route("/rules/_incoming", methods=['POST'])
def post_rules__incoming():
    test_setup()
    data = request.form.to_dict()
    apply_to = data['object']
    name = data['name']
    data = {
        name: [
            {
                "compare_value": data['compare_value'],
                "attribute": data['attribute'],
                "concur": data['concur'],
                "not_concur": data['not_concur'],
                "operator": data['operator']
            },
        ]
    }
    with open(OBJECT_FILE, 'r') as infile:
        objects = json.loads(infile.read())
    objects[apply_to]['rules'].append(name)
    with open(OBJECT_FILE, 'w') as outfile:
        outfile.write(json.dumps(objects, indent=4))
    rules = RulesInstance(data)
    rules.save_rule()
    test_instance()
    return redirect('/rules')

if __name__ == '__main__':
    try:
        port = int(os.getenv("PORT"))
        app.run(host='0.0.0.0', port=port, threaded=True)
    except TypeError:
        app.run(debug=True, threaded=True)
