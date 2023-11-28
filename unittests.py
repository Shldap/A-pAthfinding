import unittest

from pathfinding import Node, find_start_node, find_end_node, generate_neighbors, construct_path


class PathfindingTestCase(unittest.TestCase):
    def setUp(self):
        # Set up the grid for testing
        self.grid = [
            [0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 2, 0, 0],
            [0, 0, 0, 0, 0]
        ]

    def test_find_start_node(self):
        start_node = find_start_node(self.grid)
        self.assertEqual(start_node.row, 1)
        self.assertEqual(start_node.col, 1)

    def test_find_end_node(self):
        end_node = find_end_node(self.grid)
        self.assertEqual(end_node.row, 3)
        self.assertEqual(end_node.col, 2)

    def test_generate_neighbors(self):
        node = Node(2, 2)
        neighbors = generate_neighbors(node, self.grid)
        self.assertEqual(len(neighbors), 4)

        expected_neighbors = [(3, 2), (1, 2), (2, 3), (2, 1)]
        for neighbor in neighbors:
            self.assertIn((neighbor.row, neighbor.col), expected_neighbors)

    def test_construct_path(self):
        end_node = Node(3, 2)
        node_1 = Node(2, 2)
        node_2 = Node(1, 2)
        node_3 = Node(1, 3)

        node_1.parent = end_node
        node_2.parent = node_1
        node_3.parent = node_2

        path = construct_path(node_3)
        expected_path = [(3, 2), (2, 2), (1, 2), (1, 3)]
        self.assertEqual(len(path), len(expected_path))

        for i in range(len(path)):
            self.assertEqual((path[i].row, path[i].col), expected_path[i])


if __name__ == '__main__':
    unittest.main()
