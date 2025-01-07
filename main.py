from tkinter import Tk, BOTH, Canvas
import time
import random


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Line:
    def __init__(self, point1: Point, point2: Point):
        self.point1 = point1
        self.point2 = point2

    def draw(self, canvas: Canvas, fill_color="black"):
        canvas.create_line(
            self.point1.x,
            self.point1.y,
            self.point2.x,
            self.point2.y,
            fill=fill_color,
            width=2
        )


class Window:
    def __init__(self, width, height):
        self.__root = Tk()
        self.__root.title("Maze Solver")
        self.__canvas = Canvas(
            self.__root,
            bg="white",
            height=height,
            width=width
        )
        self.__canvas.pack(fill=BOTH, expand=1)
        self.__running = False
        self.__root.protocol("WM_DELETE_WINDOW", self.close)

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self):
        self.__running = True
        while self.__running:
            self.redraw()
        print("window closed...")

    def close(self):
        self.__running = False

    def draw_line(self, line: Line, fill_color="black"):
        line.draw(self.__canvas, fill_color)

    def draw_cell(self, cell, fill_color="black"):
        cell.draw(self.__canvas, fill_color)


class Cell:
    def __init__(self, win):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self.__x1 = None
        self.__y1 = None
        self.__x2 = None
        self.__y2 = None
        self.__win = win
        self.visited = False

    def draw(self, x1, y1, x2, y2):
        self.__x1 = x1
        self.__y1 = y1
        self.__x2 = x2
        self.__y2 = y2
        self.__win.draw_line(
            Line(
                Point(self.__x1, self.__y1),
                Point(self.__x1, self.__y2)
            ),
            "black" if self.has_left_wall else "white"
        )
        self.__win.draw_line(
            Line(
                Point(self.__x2, self.__y1),
                Point(self.__x2, self.__y2)
            ),
            "black" if self.has_right_wall else "white")
        self.__win.draw_line(
            Line(
                Point(self.__x1, self.__y1),
                Point(self.__x2, self.__y1)
            ),
            "black" if self.has_top_wall else "white"
        )
        self.__win.draw_line(
            Line(
                Point(self.__x1, self.__y2),
                Point(self.__x2, self.__y2)
            ),
            "black" if self.has_bottom_wall else "white"
        )

    def get_top_left(self):
        return Point(self.__x1, self.__y1)

    def get_bottom_left(self):
        return Point(self.__x2, self.__y2)

    def get_center(self):
        return Point(
            self.__x1 + (abs(self.__x2 - self.__x1) // 2),
            self.__y1 + (abs(self.__y2 - self.__y1) // 2)
        )

    def draw_move(self, to_cell, undo=False):
        move_line = Line(self.get_center(), to_cell.get_center())
        self.__win.draw_line(move_line, "gray" if undo else "red")


class Maze:
    def __init__(
        self,
        x1,
        y1,
        num_rows,
        num_cols,
        cell_size_x,
        cell_size_y,
        win=None,
        seed=None
    ):
        self.__x1 = x1
        self.__y1 = y1
        self.__num_rows = num_rows
        self.__num_cols = num_cols
        self.__cell_size_x = cell_size_x
        self.__cell_size_y = cell_size_y
        self.__win = win
        self.__cells = []
        self.__solving = False
        random.seed(seed)

        self.__create_cells()
        self.__break_entrance_and_exit()
        self.__break_walls_r(0, 0)
        self.__reset_cells_visited()

    def __animate(self):
        self.__win.redraw()
        time.sleep(0.05 if self.__solving else 0.01)

    def get_cells(self):
        return self.__cells

    def __draw_cell(self, x, y):
        if self.__win is None:
            return
        x1 = self.__x1 + (x * self.__cell_size_x)
        y1 = self.__y1 + (y * self.__cell_size_y)
        y2 = y1 + self.__cell_size_y
        x2 = x1 + self.__cell_size_x
        self.__cells[x][y].draw(x1, y1, x2, y2)
        self.__animate()

    def __create_cells(self):
        for x in range(0, self.__num_cols):
            column = []
            for y in range(0, self.__num_rows):
                column.append(Cell(self.__win))
            self.__cells.append(column)

        for x in range(0, self.__num_cols):
            for y in range(0, self.__num_rows):
                self.__draw_cell(x, y)

    def __break_entrance_and_exit(self):
        self.__cells[0][0].has_top_wall = False
        self.__draw_cell(0, 0)
        self.__cells[self.__num_cols - 1][self.__num_rows - 1].has_bottom_wall = False  # noqa
        self.__draw_cell(self.__num_cols - 1, self.__num_rows - 1)

    def __break_walls_r(self, x, y):
        self.__cells[x][y].visited = True
        while True:
            to_visit = []
            if x + 1 < self.__num_cols:
                if not self.__cells[x+1][y].visited:
                    to_visit.append((x+1, y))
            if y + 1 < self.__num_rows:
                if not self.__cells[x][y+1].visited:
                    to_visit.append((x, y+1))
            if x - 1 >= 0:
                if not self.__cells[x-1][y].visited:
                    to_visit.append((x-1, y))
            if y - 1 >= 0:
                if not self.__cells[x][y-1].visited:
                    to_visit.append((x, y-1))

            if len(to_visit) == 0:
                self.__draw_cell(x, y)
                break

            direction = random.randint(0, (len(to_visit) - 1))
            if x > to_visit[direction][0]:
                self.__cells[x][y].has_left_wall = False
                self.__cells[to_visit[direction][0]][y].has_right_wall = False
            elif y > to_visit[direction][1]:
                self.__cells[x][y].has_top_wall = False
                self.__cells[x][to_visit[direction][1]].has_bottom_wall = False
            elif x < to_visit[direction][0]:
                self.__cells[x][y].has_right_wall = False
                self.__cells[to_visit[direction][0]][y].has_left_wall = False
            elif y < to_visit[direction][1]:
                self.__cells[x][y].has_bottom_wall = False
                self.__cells[x][to_visit[direction][1]].has_top_wall = False

            self.__break_walls_r(
                to_visit[direction][0], to_visit[direction][1])

    def __reset_cells_visited(self):
        for x in range(0, self.__num_cols):
            for y in range(0, self.__num_rows):
                self.__cells[x][y].visited = False

    def solve(self):
        self.__solving = True
        return self.__solve_r(0, 0)

    def __solve_r(self, x, y):
        self.__animate()
        self.__cells[x][y].visited = True

        if x == self.__num_cols - 1 and y == self.__num_rows - 1:
            return True

        # Check Right
        if x + 1 < self.__num_cols:
            if (not self.__cells[x][y].has_right_wall
                    and not self.__cells[x+1][y].visited):
                self.__cells[x][y].draw_move(self.__cells[x+1][y])
                check_solution = self.__solve_r(x+1, y)
                if check_solution:
                    return True
                else:
                    self.__cells[x][y].draw_move(self.__cells[x+1][y], True)

        # Check Down
        if y + 1 < self.__num_rows:
            if (not self.__cells[x][y].has_bottom_wall
                    and not self.__cells[x][y+1].visited):
                self.__cells[x][y].draw_move(self.__cells[x][y+1])
                check_solution = self.__solve_r(x, y+1)
                if check_solution:
                    return True
                else:
                    self.__cells[x][y].draw_move(self.__cells[x][y+1], True)

        # Check Left
        if x - 1 >= 0:
            if (not self.__cells[x][y].has_left_wall
                    and not self.__cells[x-1][y].visited):
                self.__cells[x][y].draw_move(self.__cells[x-1][y])
                check_solution = self.__solve_r(x-1, y)
                if check_solution:
                    return True
                else:
                    self.__cells[x][y].draw_move(self.__cells[x-1][y], True)

        # Check Up
        if y - 1 >= 0:
            if (not self.__cells[x][y].has_top_wall
                    and not self.__cells[x][y-1].visited):
                self.__cells[x][y].draw_move(self.__cells[x][y-1])
                check_solution = self.__solve_r(x, y-1)
                if check_solution:
                    return True
                else:
                    self.__cells[x][y].draw_move(self.__cells[x][y-1], True)

        return False


def main():
    win = Window(800, 600)

    maze = Maze(50, 50, 10, 10, 25, 25, win)
    maze.solve()

    win.wait_for_close()


main()
