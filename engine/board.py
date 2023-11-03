from types import NoneType
from typing import List, Tuple

from engine.blocks import Block
from engine.player import Player
from engine.point import Point2D


class Board:
    def __init__(self, max_x=16, max_y=16):
        self.max_x = max_x
        self.max_y = max_y
        self.cells = [[None for _ in range(self.max_x)] for _ in range(self.max_y)]

    def read_cell(self, x: int, y: int) -> Block | None:
        # standardize x, y order across codebase
        if 0 <= x <= self.max_x and 0 <= y <= self.max_y:
            return self.cells[y][x]
        else:
            raise IndexError(f'There is no ({x}, {y}) cell in the board.')

    def write_cell(self, x: int, y: int, obj: Block | None) -> None:
        # standardize x, y order across codebase
        self.cells[y][x] = obj

    def is_cell_free(self, x: int, y: int) -> bool:
        try:
            cell_value = self.read_cell(x, y)
            if isinstance(cell_value, (Player, NoneType)):
                return True
            return False
        except IndexError:
            return False

    def can_block_be_moved(self, block, dx, dy) -> bool:
        return all(self.is_cell_free(p.x + dx, p.y + dy) for p in block.location if
                   Point2D(p.x + dx, p.y + dy) not in block.location)

    def traverse_all_board_cells(self) -> Tuple[int, int, None | Block | Player]:
        for y, row in enumerate(self.cells):
            for x, cell_value in enumerate(row):
                yield x, y, cell_value

    def traverse_all_board_cells_in_reversed_order(self) -> Tuple[int, int, None | Block | Player]:
        for y, row in reversed(list(enumerate(self.cells))):
            for x, cell_value in reversed(list(enumerate(row))):
                yield x, y, cell_value

    def move_object(self, obj: Block | Player, dx: int, dy: int):
        self.remove_object_in_cell(obj.location[0].x, obj.location[0].y)

        new_block_loation: List[Point2D] = []
        for p in obj.location:
            self.write_cell(p.x + dx, p.y + dy, obj)
            new_block_loation.append(Point2D(p.x + dx, p.y + dy))

        obj.location = new_block_loation

    def move_object_down(self, obj: Block):
        self.move_object(obj, 0, 1)

    def add_object(self, obj, current_iteration=0):
        is_space_free = all(self.is_cell_free(p.x, p.y) for p in obj.location)

        if is_space_free:
            for p in obj.location:
                self.write_cell(p.x, p.y, obj)
                obj.age = current_iteration
        else:
            raise IndexError(f"Cannot place block that occupies: {obj.location} cells")

    def remove_object_in_cell(self, x: int, y: int):
        obj: Block | None = self.read_cell(x, y)

        if obj is None:
            return None

        for p in obj.location:
            self.write_cell(p.x, p.y, None)
