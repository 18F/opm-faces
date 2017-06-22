#! /usr/bin/env python3
import json
from settings import *

class RulesObject:
    def engine(self, material, record):
        output = [] # List of (attr, value) tuples.
        for i in material:
            rule = i[list(i.keys())[0]]
            if rule['type'] == 'logic':
                constructed = 'if "{}" {} "{}":\n\tanswer = "{}"\nelse:\n\tanswer = "{}"\n'.format(
                    record.__dict__[rule['attribute']],
                    rule['operator'],
                    rule['compare_value'],
                    rule['concur'],
                    rule['not_concur']
                )
                exec(constructed)
                output.append((rule['name'], eval('answer')))
            elif rule['type'] == 'calc':
                if rule['data'].index('__') == -1:
                    eval('record.{} = {}'.format(rule['name'], eval(rule['data'])))
                else:
                    eq = rule['data'].split('__')
                    size = len(eq)
                    for i in range(size):
                        try:
                            value = record.__dict__[eq[i]]
                            index = eq.index(eq[i])
                            eq.insert(i, value)
                            eq.pop(i+1)
                        except KeyError:
                            pass
                output.append((rule['name'], eval(''.join(eq))))
        return output

    def to_json_dict(self, filename, new_data, key):
        with open(filename, 'r') as infile:
            data = json.loads(infile.read())
        data[key] = new_data
        with open(filename, 'w') as outfile:
            outfile.write(json.dumps(data, indent=4))

class RulesInstance(RulesObject):
    def __init__(self, obj):
        self.raw_data = obj

    def save_rule(self):
        key = list(self.raw_data.keys())[0]
        self.to_json_dict(
            RULES_FILE, self.raw_data[key], key)

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
            rules = json.loads(infile.read())
        with open(CALCULATION_FILE, 'r') as infile:
            calculations = json.loads(infile.read())
        combined = { **rules, **calculations }
        return [ {i: combined[i]} for i in self.rules ]

    def calculate_instance(self):
        rules = self.load_rules()
        for i in self.engine(rules, self):
            exec('self.{} = "{}"'.format(i[0], i[1]))

    def save_record(self):
        with open(DATA_FILE, 'r') as infile:
            data = json.loads(infile.read())
        out_data = self.__dict__
        out_data.pop('raw_data')
        out_data['type'] = self.type
        data.append(out_data)
        with open(DATA_FILE, 'w') as outfile:
            outfile.write(json.dumps(data, indent=4))
