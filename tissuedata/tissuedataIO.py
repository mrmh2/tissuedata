import os
import json
from pprint import pprint


class Leaf(object):
    def __init__(self, json_file):
        self.cell_dict = dict()
        with open(json_file)as data_file:
            data = json.load(data_file)

        for cell_id, cell_dictionary in data['cells'].iteritems():
            self.cell_dict[cell_id] = cell_dictionary


class Cell(object):
    def __init__(self, cell_id, dictionary):
        self.cell_id = cell_id
        self.dictionary = dictionary


def main():
    path = '/Users/carterr/Dropbox/Postdoc_stuff/tissuedata/data/EXPID3002_plantD/T00.json'

    # with open(path) as data_file:
    #    data = json.load(data_file)

    # pprint(data['cells']['95']['centroid'])

    # for cell_id, cell in data["cells"].iteritems():
    #     print cell_id, cell['has']

    leaf1 = Leaf(path)
    print leaf1.cell_dict['1022']['has']

if __name__ == "__main__":
    main()
