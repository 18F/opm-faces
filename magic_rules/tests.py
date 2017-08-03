#! /usr/bin/env python3
import json, os
import magic
import unittest
from settings import *

# Test case data for POST.
PROTOTYPE_DATA = '{"name":"animal","attribute_0":"height"}'
CALCULATION_DATA = '{"name":"double_height", "object":"animal",'\
' "contingent": "TRUE", "static_value_0":"2", "attribute_value_0":"",'\
' "operator_value_0":"*","static_value_1":"",'\
' "attribute_value_1":"__height__"}'
RULE_DATA = '{"name":"test_tall", "object":"animal", "operator":"<=",'\
' "attribute":"height", "compare_value":"5", "concur_static":"",'\
' "concur_calc":"_double_height", '\
'"not_concur_static":"tall enough already", "not_concur_calc":""}'
DATA_DATA_0 = '{"type":"animal","height":"4"}'
DATA_DATA_1 = '{"type":"animal","height":"10"}'

class MagicTestCase(unittest.TestCase):
    def setUp(self):
        # Setup test client.
        magic.app.testing = True
        self.app = magic.app.test_client()
        # Remove all existing data from MagicDB JSON files at beginning.
        self.remove_all_data()

    def tearDown(self):
        # Remove all test data from MagicDB JSON files at end.
        self.remove_all_data()

    def remove_all_data(self):
        with open(PROTOTYPE_FILE, 'w') as outfile:
            outfile.write(json.dumps({}))
        with open(CALCULATION_FILE, 'w') as outfile:
            outfile.write(json.dumps({}))
        with open(RULES_FILE, 'w') as outfile:
            outfile.write(json.dumps({}))
        with open(DATA_FILE, 'w') as outfile:
            outfile.write(json.dumps([]))

    def api_get(self, endpoint):
        r = self.app.get(endpoint)
        return r.status, json.loads(r.data.decode('utf-8'))

    def api_post(self, endpoint, data):
        r = self.app.post(endpoint, data=data, content_type='application/json')
        return r.status, json.loads(r.data.decode('utf-8'))

    def test_prototype_endpoint(self):
        # Load test case data.
        test_data = json.loads(PROTOTYPE_DATA)
        # Write, read responses.
        w_status, w_data = self.api_post('/api/prototypes/write',
            PROTOTYPE_DATA)
        r_status, r_data = self.api_get('/api/prototypes/read')
        # Assertions.
        for i in [w_status, r_status]:
            assert '200 OK' in i
        assert type(r_data[test_data['name']]) == type(dict())
        assert r_data[test_data['name']]['type'] == test_data['name']
        assert r_data[test_data['name']]['rules'] == []

    def test_calculation_endpoint(self):
        # Load test case data.
        test_data = json.loads(CALCULATION_DATA)
        # Write, read responses.
        w_status, w_data = self.api_post('/api/calculations/write',
            CALCULATION_DATA)
        r_status, r_data = self.api_get('/api/calculations/read')
        # Assertions.
        for i in [w_status, r_status]:
            assert '200 OK' in i
        assert type(r_data[test_data['name']]) == type(dict())
        assert r_data[test_data['name']]['type'] == 'calc'

    def test_rule_endpoint(self):
        # Create `animal` prototype for rule.
        self.api_post('/api/prototypes/write',PROTOTYPE_DATA)
        # Write, read responses.
        w_status, w_data = self.api_post('/api/rules/write', RULE_DATA)
        r_status, r_data = self.api_get('/api/rules/read')
        # Prototype read response for update check.
        prototype_status, prototype_data = self.api_get('/api/prototypes/read')
        # Assertions.
        for i in [w_status, r_status]:
            assert '200 OK' in i
        test_data = json.loads(RULE_DATA)
        assert type(r_data[test_data['name']]) == type(dict())
        assert r_data[test_data['name']]['type'] == 'logic'
        assert r_data[test_data['name']]['operator'] == test_data['operator']
        assert test_data['name'] in prototype_data[test_data['object']]['rules']

    def test_data_endpoint(self):
        # Create prototype, calculation, and rule for data.
        self.api_post('/api/prototypes/write', PROTOTYPE_DATA)
        self.api_post('/api/calculations/write', CALCULATION_DATA)
        self.api_post('/api/rules/write', RULE_DATA)
        # Write, read responses, case 0.
        w_status, w_data = self.api_post('/api/data/write', DATA_DATA_0)
        r_status, r_data = self.api_get('/api/data/read')
        # Assertions, case 0.
        assert r_data[0]['test_tall'] == '8'
        # Write, read responses, case 1.
        w_status, w_data = self.api_post('/api/data/write', DATA_DATA_1)
        r_status, r_data = self.api_get('/api/data/read')
        # Assertions, case 1.
        assert r_data[1]['test_tall'] == 'tall enough already'

if __name__ == '__main__':
    unittest.main()
