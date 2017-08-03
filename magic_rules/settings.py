import os
# Where all of the data is.
DATASTORE_PATH = '/datastore'
# Where prototype objects are stored.
PROTOTYPE_FILE = '{}{}/objects.json'.format(os.getcwd(), DATASTORE_PATH)
# Where calculated records are stored.
DATA_FILE = '{}{}/data.json'.format(os.getcwd(), DATASTORE_PATH)
# Where rules are stored.
RULES_FILE = '{}{}/rules.json'.format(os.getcwd(), DATASTORE_PATH)
# Where the calculations are stored.
CALCULATION_FILE = '{}{}/calculations.json'.format(
    os.getcwd(), DATASTORE_PATH)
