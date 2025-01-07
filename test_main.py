import unittest
from main import Maze


class Tests(unittest.TestCase):
    def test_maze_create_cells(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertEqual(
            len(m1.get_cells()),
            num_cols,
        )
        self.assertEqual(
            len(m1.get_cells()[0]),
            num_rows,
        )

    def test_maze_break_entrance_and_exit(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertEqual(
            m1.get_cells()[0][0].has_top_wall,
            False,
        )
        self.assertEqual(
            m1.get_cells()[num_cols - 1][num_rows - 1].has_bottom_wall,
            False,
        )

    def test_maze_reset_self_visited(self):
        num_cols = 15
        num_rows = 20
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        for x in range(0, num_cols):
            for y in range(0, num_rows):
                self.assertFalse(
                    m1.get_cells()[x][y].visited
                )


if __name__ == "__main__":
    unittest.main()
