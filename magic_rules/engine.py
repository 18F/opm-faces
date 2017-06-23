#! /usr/bin/env python3
import json
import datetime as dt
from settings import *
from datastore import *

class MagicObject:
    # Some methods.
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

class Record(MagicObject):
    def __init__(self, record):
        self.record = record
        self.type = self.record['type']
        self.rule_material = self.load_rules()

        # Fetch  correct prototype and add attributes to this Record instance.
        prototype = MagicDB(PROTOTYPE_FILE).all()[self.type]
        for k in prototype:
            if type(prototype[k]) == type(str()):
                exec('self.{} = "{}"'.format(k, prototype[k]))
            else:
                exec('self.{} = {}'.format(k, prototype[k]))

        # Use incoming data to populate applicable attributes.
        for k in self.record:
            if k in list(self.__dict__.keys()):
                exec('self.{} = "{}"'.format(k, self.record[k]))

    def load_rules(self):
        # Figure out what rules are applicable.
        db = MagicDB(PROTOTYPE_FILE)
        prototype = db.single(self.record['type'])
        self.applicable_rules = prototype['rules']

        # Fetch combined set of all rules and calculations.
        rules = MagicDB(RULES_FILE).all()
        calculations = MagicDB(CALCULATION_FILE).all()
        combined = { **rules, **calculations }

        # Return only applicable rule and calculation material.
        return [ {i: combined[i]} for i in self.applicable_rules ]

    def calculate_instance(self):
        # Supply engine with all rule and calc material. For each item
        # of the result, conditionally set attribute of this Record instance.
        output = [] # List of [attr, value, addl_calcs] results.
        this_material = self.rule_material
        for i in this_material:
            rule = i[list(i.keys())[0]] # Assumes a rule is {rule_name: {rule_material}}
            if rule['type'] == 'logic':
                result = self.run_logic(rule)
                if result[2]:
                    this_material.append(result[2])
                output.append(result)
            elif rule['type'] == 'calc':
                output.append(self.run_calc(rule))
        for i in output:
            if i[1] == '' or str(i[1])[0] != '_':
                exec('self.{} = "{}"'.format(i[0], i[1]))
            else:
                exec('self.{} = "{}"'.format(i[0], '[executed calc]'))

    def run_logic(self, rule):
        v1 = self.specific_type(self.__dict__[rule['attribute']])
        v2 = self.specific_type(rule['compare_value'])
        constructed = 'if {} {} {}:'\
            '\n\tanswer = "{}"\nelse:\n\tanswer = "{}"\n'.format(
                'v1',
                rule['operator'],
                'v2',
                rule['concur'],
                rule['not_concur'])
        exec(constructed)
        item = [rule['name'], eval('answer'), {}]
        # Check if result requires an additional calculation.
        if item[1] != '':
            if str(item[1])[0] == '_':
                calc_name = item[1][1:]
                # Get additional calc material.
                calc = MagicDB(CALCULATION_FILE).all()[calc_name]
                calc['name'] = rule['name']
                # Add to output for subsequent execution.
                item = (item[0], item[1], {calc_name: calc})
        return item

    def run_calc(self, rule):
        if rule['data'].index('__') == -1:
            eval('self.record.{} = {}'.format(rule['name'], eval(rule['data'])))
        else:
            eq = rule['data'].split('__')
            size = len(eq)
            for i in range(size):
                try:
                    value = self.__dict__[eq[i]]
                    index = eq.index(eq[i])
                    eq.insert(i, value)
                    eq.pop(i+1)
                except KeyError:
                    pass
        return [rule['name'], eval(''.join(eq)), {}]

    def save(self):
        db = MagicDB(DATA_FILE)
        output = self.__dict__
        [ output.pop(i) for i in \
            ['rule_material', 'applicable_rules', 'record']
        ]
        db.add(self.__dict__)
