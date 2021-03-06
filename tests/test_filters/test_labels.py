"""
Tests for labels.py
"""

import unittest
from biothings_explorer.user_query_dispatcher import SingleEdgeQueryDispatcher
from biothings_explorer.filters.labels import filter_label
from biothings_explorer.filters.edges import filter_node_degree

class TestFilterLabels(unittest.TestCase):

    # check all labels are the same as Parameters for 1 label
    def test_single_label(self):
        seqd = SingleEdgeQueryDispatcher(input_cls='Gene',
                                 output_cls='ChemicalSubstance',
                                 input_id='NCBIGene',
                                 values='1017')
        seqd.query()
        subG = filter_label(seqd.G, 'related_to')
        for edge in subG.edges.data():
            self.assertEqual('related_to', edge[2]['label'])

    # check label is correct if param is multiple labels
    def test_mult_label(self):
        labels = ['related_to', 'negatively_regulated_by', 'physically_interacts_with']
        seqd = SingleEdgeQueryDispatcher(input_cls='Gene',
                                 output_cls='ChemicalSubstance',
                                 input_id='NCBIGene',
                                 values='1017')
        seqd.query()
        subG = filter_label(seqd.G, labels)
        for edge in subG.edges.data():
            self.assertTrue(edge[2]['label'] in labels)


    # check correct number of results are returned
    def test_count(self):
        count = 15
        seqd = SingleEdgeQueryDispatcher(input_cls='Gene',
                                 output_cls='ChemicalSubstance',
                                 input_id='NCBIGene',
                                 values='1017')
        seqd.query()
        subG = filter_label(seqd.G, ['negatively_regulated_by', 'positively_regulates'], count)
        self.assertEqual(count+1, len(subG.nodes))


    # check that the filteredBy is EdgeLabel
    def test_filter_label(self):
        seqd = SingleEdgeQueryDispatcher(input_cls='Gene',
                                 output_cls='ChemicalSubstance',
                                 input_id='NCBIGene',
                                 values='1017')
        seqd.query()
        subG = filter_label(seqd.G, 'related_to')
        for node,y in subG.nodes(data=True):
            if node != 'NCBIGene:1017':
                self.assertEqual('EdgeLabel', y['filteredBy'])

if __name__ == '__main__':
    unittest.main()
