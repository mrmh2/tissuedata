import json
import numpy as np
import matplotlib
matplotlib.use('tkagg')
import matplotlib.pyplot as plt


class Leaf(object):
    def __init__(self, json_file):
        self.cell_dict = dict()
        with open(json_file)as data_file:
            data = json.load(data_file)

        for cell_id, cell_dictionary in data['cells'].iteritems():
            self.cell_dict[cell_id] = Cell(cell_dictionary)

    def __iter__(self):
        return self.cell_dict.iteritems()


class Cell(object):
    def __init__(self, dictionary):
        self.has = dictionary['has']
        self.centroid = dictionary['centroid']
        self.vx = dictionary['vx']
        self.vy = dictionary['vy']
        self.pixel_area = dictionary['pixel_area']
        self.top_left = dictionary['top_left']
        self.real_area = self.pixel_area * self.vx * self.vy


def main():
    path = '/Users/carterr/Dropbox/Postdoc_stuff/tissuedata/data/EXPID3002_plantD/T15.json'

    leaf1 = Leaf(path)

    for cell_id, cell in leaf1:
        plt.scatter(cell.centroid[0] * cell.vx,
                    cell.centroid[1] * cell.vy,
                    c='blue', s=cell.real_area, alpha=0.5)

    plt.axis('equal')
    plt.show()

if __name__ == "__main__":
    main()