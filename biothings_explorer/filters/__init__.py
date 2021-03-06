# main class

from .co_occurs import filter_co_occur
from .labels import filter_label
from .edges import filter_node_degree
from .api import filter_api

class Filter():

    def __init__(self, G, filtdict={}):
        self.G = G
        self.name = filtdict['name'] if 'name' in filtdict.keys() else None
        self.count = filtdict['count'] if 'count' in filtdict.keys() else 50
        self.label = filtdict['label'] if 'label' in filtdict.keys() else None

    def filter_results(self):
        if not self.name:
            return self.G
        if self.name == 'NodeDegree':
            return filter_node_degree(self.G, self.count)
        if self.name == 'EdgeLabel':
            if not self.label:
                print('Please include a label for this filter')
            else:
                return filter_label(self.G, self.label, self.count)
        if self.name == 'CoOccurrence':
            return filter_co_occur(self.G, self.count)
        if self.name == 'UniqueAPIs':
            return filter_api(self.G, self.count)
        return self.G
