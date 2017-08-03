from datastore import MagicDB
from settings import *
from engine import Record

def process_incoming_prototype(data):
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
    return [data, obj]

def process_incoming_calculation(data):
    name = data['name']
    apply_to = data['object']
    categories = ['static', 'attribute', 'operator']

    # Organize calculation material.
    obj = [ [ {'source': cat, 'value': i[1], 'position':i[0].split('_')[2]} \
            for i in \
            [ i for i in list(data.items())\
                if i[0][0:4] == cat[0:4] and i[1] != '' ]
        ] for cat in categories ]
    obj = sorted([ i for i in [ inner for outer in obj for inner in outer ] ],
        key=lambda x: int(x['position']))
    # Correctly organize values and operators in a calcuable fashion.
    values = [ i['value'] for i in obj if i['source'] != 'operator' ]
    operators = [ i['value'] for i in obj if i['source'] == 'operator' ]
    ct = 0
    for i in range(len(operators)):
        values.insert(i+1+ct, operators[i])
        ct += 1
    obj = {
        'name': name,
        'type': 'calc',
        'data': ''.join(values)
    }
    # Save calculation material.
    MagicDB(CALCULATION_FILE).update(data=obj, key=name)

    # Conditionally add calculation reference to prototype.
    if data['contingent'] == 'FALSE':
        db = MagicDB(PROTOTYPE_FILE)
        prototypes = db.all()
        prototypes[apply_to]['rules'].append(name)
        db.write(to_write=prototypes)
    return [data, obj]

def process_incoming_rules(data):
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
    obj = {
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
    db.update(data=obj[name], key=name)
    return [data, obj]

def process_incoming_data(data):
    # Instantiate Record object, calcuate, clean result.
    record = Record(data)
    record.calculate_instance()
    obj = record.clean()
    # Save result to datastore.
    db = MagicDB(DATA_FILE)
    db.add(obj)
    return [data, obj]

def get_api_data():
    return {
        'endpoints': [
            {
                'route': '/prototypes',
                'actions': [
                    {'route': './read', 'method': 'GET'},
                    {'route': './write', 'method': 'POST'}
                ]
            },
            {
                 'route': '/calculations',
                 'actions': [
                     {'route': './read', 'method': 'GET'},
                     {'route': './write', 'method': 'POST'}
                 ]
            },
            {
                'route': '/rules',
                'actions': [
                    {'route': './read', 'method': 'GET'},
                    {'route': './write', 'method': 'POST'}
                ]
            },
            {
                'route': '/data',
                'actions': [
                    {'route': './read', 'method': 'GET'},
                    {'route': './write', 'method': 'POST'}
                ]
            },
        ]
    }
