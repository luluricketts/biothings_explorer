"""
Tests for edges.py
"""

import unittest
import pandas as pd
from biothings_explorer.user_query_dispatcher import SingleEdgeQueryDispatcher
from biothings_explorer.filters.edges import filter_node_degree

class TestFilterEdges(unittest.TestCase):

    # test for count values
    def test_count_values(self):
        counts = [10, 20, 40, 50, 100]
        seqd = SingleEdgeQueryDispatcher(input_cls='Gene',
                                 output_cls='ChemicalSubstance',
                                 input_id='NCBIGene',
                                 values='1017')
        seqd.query()
        for count in counts:
            newG = filter_node_degree(seqd.G, count)
            self.assertEqual(len(newG.nodes), count+1)

    # edge case test if count > num nodes, then returns num_nodes results
    def test_num_nodes(self):
        count = 1000
        seqd = SingleEdgeQueryDispatcher(input_cls='Gene',
                                         output_cls='ChemicalSubstance',
                                         input_id='NCBIGene',
                                         values='1017')
        seqd.query()
        newG = filter_node_degree(seqd.G, count)
        self.assertEqual(len(newG.nodes), len(seqd.G.nodes))

    # test for correct ordering of ranks
    def test_ranks(self):
        seqd = SingleEdgeQueryDispatcher(input_cls='Disease',
                                         input_id='MONDO',
                                         output_cls='PhenotypicFeature',
                                         pred='related_to',
                                         values='MONDO:0010997')
        seqd.query()
        newG = filter_node_degree(seqd.G)
        for i1,node1 in enumerate(newG.nodes):
            if node1 == 'MONDO:MONDO:0010997':
                continue
            for i2,node2 in enumerate(newG.nodes):
                if node2 == 'MONDO:MONDO:0010997':
                    continue
                if newG.degree(node1) > newG.degree(node2):
                    self.assertLess(newG.nodes.data()[node1]['rank'], newG.nodes.data()[node2]['rank'])
                elif newG.degree(node1) < newG.degree(node2):
                    self.assertGreater(newG.nodes.data()[node1]['rank'], newG.nodes.data()[node2]['rank'])

if __name__ == '__main__':
    unittest.main()
