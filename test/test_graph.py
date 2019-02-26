"""
Unit and functional tests for the graph module.
"""


import unittest
from reinforce import graph


class TestGraph(unittest.TestCase):
    pass
    

class TestNode(unittest.TestCase):

    def test_init(self):
        node = graph.Node()
        self.assertEqual(node._from_nodes, {})
        self.assertEqual(node._to_nodes, {})
        self.assertEqual(node._attrs, {})

        attrs = {"BOARD": [[0] * 3] * 3}
        node = graph.Node(**attrs)
        self.assertEqual(node._from_nodes, {})
        self.assertEqual(node._to_nodes, {})
        self.assertEqual(node._attrs, attrs)
    
        return

    def test_add_from_node(self):
        node = graph.Node()
        node1 = graph.Node()
        node2 = graph.Node()
        node3 = graph.Node()

        self.assertRaises(TypeError, node.add_from_node, [1], node1)
        self.assertRaises(TypeError, node.add_from_node, 1, 1)

        node.add_from_node(1, node1)
        self.assertRaises(KeyError, node.add_from_node, 1, node1)
        node.add_from_node(2, node2)
        node.add_from_node(3, node3)

        return

    def test_from_nodes(self):
        node = graph.Node()
        node1 = graph.Node()
        node2 = graph.Node()
        node3 = graph.Node()

        node.add_from_node(1, node1)
        node.add_from_node(2, node2)
        node.add_from_node(3, node3)

        self.assertEqual(
            node.from_nodes,
            {1: node1, 2: node2, 3: node3}
        )

        return

    def test_remove_from_node(self):
        node = graph.Node()
        node1 = graph.Node()
        node2 = graph.Node()
        node3 = graph.Node()

        node.add_from_node(1, node1)
        node.add_from_node(2, node2)
        node.add_from_node(3, node3)

        self.assertEqual(
            node.from_nodes,
            {1: node1, 2: node2, 3: node3}
        )

        return


if __name__ == "__main__":
    unittest.main()
