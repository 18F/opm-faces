#! /usr/bin/env python3
import json
import datetime as dt
from settings import *

class RulesObject:
    def run_logic(self, rule, record):
        v1 = self.specific_type(record.__dict__[rule['attribute']])
        v2 = self.specific_type(rule['compare_value'])
        constructed = 'if {} {} {}:\n\tanswer = "{}"\nelse:\n\tanswer = "{}"\n'.format(
            'v1',
            rule['operator'],
            'v2',
            rule['concur'],
            rule['not_concur']
        )
        exec(constructed)
        item = [rule['name'], eval('answer'), {}]
        # Check if result requires an additional calculation.
        if item[1] != '':
            if str(item[1])[0] == '_':
                calc_name = item[1][1:]
                # Get additional calc material.
                with open(CALCULATION_FILE, 'r') as infile:
                    calc = json.loads(infile.read())[calc_name]
                    calc['name'] = rule['name']
                # Add to output for subsequent execution.
                item = (item[0], item[1], {calc_name: calc})
        return item

    def run_calc(self, rule, record):
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
        return (rule['name'], eval(''.join(eq)), {})


    def engine(self, material, record):
        output = [] # List of (attr, value) tuples.
        addl_calcs = []
        for i in material:
            rule = i[list(i.keys())[0]]
            if rule['type'] == 'logic':
                result = self.run_logic(rule, record)
                if result[2]:
                    material.append(result[2])
                output.append(result)
            elif rule['type'] == 'calc':
                output.append(self.run_calc(rule, record))
        return output

    def to_json_dict(self, filename, new_data, key):
        with open(filename, 'r') as infile:
            data = json.loads(infile.read())
        data[key] = new_data
        with open(filename, 'w') as outfile:
            outfile.write(json.dumps(data, indent=4))

    def is_number(self, string):
        if type(string) != type(str()):
            return string
        try:
            return float(string)
        except ValueError or TypeError:
            return '"{}"'.format(string)

    def is_date(self, string):
        if type(string) != type(str()):
            return string
        try:
            return dt.datetime.strptime(string, '%Y-%m-%d')
        except ValueError or TypeError:
            return '"{}"'.format(string)

    def specific_type(self, string):
        a = self.is_date(string)
        b = self.is_number(string)
        if type(a) != type(string):
            return a
        else:
            return b

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
            if i[1] == '' or str(i[1])[0] != '_':
                exec('self.{} = "{}"'.format(i[0], i[1]))
            else:
                exec('self.{} = "{}"'.format(i[0], '[executed calc]'))

    def save_record(self):
        with open(DATA_FILE, 'r') as infile:
            data = json.loads(infile.read())
        out_data = self.__dict__
        out_data.pop('raw_data')
        out_data['type'] = self.type
        data.append(out_data)
        with open(DATA_FILE, 'w') as outfile:
            outfile.write(json.dumps(data, indent=4))
