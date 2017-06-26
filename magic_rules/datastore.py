#! /usr/bin/env python3
import json

class MagicDB:
    def __init__(self, filename):
        self.filename = filename
        self.data = self.read()

    def read(self):
        with open(self.filename, 'r') as infile:
            return json.loads(infile.read())

    def write(self, to_write):
        with open(self.filename, 'w') as outfile:
            outfile.write(json.dumps(to_write, indent=4))

    def all(self):
        return self.data

    def single(self, key):
        return self.data[key]

    def update(self, data, key):
        self.data[key] = data
        self.write(self.data)

    def add(self, data):
        self.data.append(data)
        self.write(self.data)
