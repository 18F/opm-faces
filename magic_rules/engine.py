#! /usr/bin/env python3
import json
from settings import *

class RulesObject:
    def constructor(self, rule, value):
        return 'if "{}" {} "{}":\n\t{} = "{}"\nelse:\n\t{} = "{}"'.format(
            value,
            rule['operator'],
            rule['compare_value'],
            rule['attribute'],
            rule['concur'],
            rule['attribute'],
            rule['not_concur']
        )

    def engine(self, rule_set, value):
        for i in rule_set:
            exec(self.constructor(i, value))
            return eval(i['attribute'])

    def to_json_dict(self, filename, new_data, key):
        with open(filename, 'r') as infile:
            data = json.loads(infile.read())
        data[key] = new_data
        with open(OBJECT_FILE, 'w') as outfile:
            outfile.write(json.dumps(data))

class ObjectPrototype(RulesObject):
    def __init__(self, obj):
        for key in obj['attributes']:
            exec('self.{} = None'.format(key))
        self.type = obj['type']
        self.rules = obj['rules']

    def save_prototype(self):
        self.to_json_dict(OBJECT_FILE, self.__dict__, self.type)

class ObjectInstance(ObjectPrototype):
    def __init__(self, data):
        self.raw_data = data
        self.create_instance()

    def load_prototypes(self):
        with open(OBJECT_FILE, 'r') as infile:
            return json.loads(infile.read())

    def create_instance(self):
        prototype = self.load_prototypes()[self.raw_data['type']]
        for k in prototype:
            if type(prototype[k]) == type(str()):
                exec('self.{} = "{}"'.format(k, prototype[k]))
            else:
                exec('self.{} = {}'.format(k, prototype[k]))

    def populate_instance(self):
        for k in self.raw_data:
            if k in list(self.__dict__.keys()):
                exec('self.{} = "{}"'.format(k, self.raw_data[k]))

    def load_rules(self):
        with open(RULES_FILE, 'r') as infile:
            all_rules = json.loads(infile.read())
            return [ {i: all_rules[i]} for i in self.rules ]

    def calculate_instance(self):
        rules = self.load_rules()
        for i in rules:
            rule_name = list(i.keys())[0]
            rule_set = i[rule_name]
            source_attribute = rule_set[0]['attribute']
            source_value = self.__dict__[source_attribute]
            target_attribute = rule_name
            target_value = self.engine(rule_set, source_value)
            exec('self.{} = "{}"'.format(target_attribute, target_value))

    def save_record(self):
        with open(DATA_FILE, 'r') as infile:
            data = json.loads(infile.read())
        out_data = self.__dict__
        out_data.pop('raw_data')
        out_data['type'] = self.type
        data.append(out_data)
        with open(DATA_FILE, 'w') as outfile:
            outfile.write(json.dumps(data))

def run():
    # Hypothetical web form data to create a new object prototype.
    OBJECT_DATA = {
        'type': 'service_history',
        'attributes': [ # Base attributes, does not include calc'd attributes.
            'start_date',
            'end_date',
            'ret_type',
        ],
        'rules': ['ret_type_name'] # Rule sets that are available to this obj.
    }
    # Hypothetical web form data to create instance from existing obj prototype.
    INSTANCE_DATA = {
        'type': 'service_history',
        'start_date': '2014-12-01',
        'end_date': '2015-01-01',
        'ret_type': '1'
    }
    ServiceHistory = ObjectPrototype(OBJECT_DATA) # Create prototype custom obj.
    ServiceHistory.save_prototype() # Save prototype to objects.json.
    TestInstance = ObjectInstance(INSTANCE_DATA) # Create new object instance.
    TestInstance.populate_instance() # Populate with supplied data.
    TestInstance.calculate_instance() # Calculate fields based on rules.
    TestInstance.save_record() # Save record to data.json.
    return TestInstance.__dict__

print(run())
