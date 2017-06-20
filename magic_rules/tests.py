from settings import *
from engine import *

def test_setup():
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
    ServiceHistory = ObjectPrototype(OBJECT_DATA) # Create prototype custom obj.
    ServiceHistory.save_prototype() # Save prototype to objects.json.

def test_instance():
    # Hypothetical web form data to create instance from existing obj prototype.
    INSTANCE_DATA = {
        'type': 'service_history',
        'start_date': '2014-12-01',
        'end_date': '2015-01-01',
        'ret_type': '1'
    }
    TestInstance = ObjectInstance(INSTANCE_DATA) # Create new object instance.
    TestInstance.populate_instance() # Populate with supplied data.
    TestInstance.calculate_instance() # Calculate fields based on rules.
    TestInstance.save_record() # Save record to data.json.
    return TestInstance.__dict__
