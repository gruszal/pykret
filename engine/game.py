from random import choice, randint

from engine import blocks
from engine.blocks import Block
from engine.player import Player
from engine.board import Board
from engine.point import Point2D


class GameEnd(Exception):
    pass


class Game:
    def __init__(self, max_x=16, max_y=16):
        self.upper_lines = 4
        self.max_x = max_x
        self.max_y = max_y + self.upper_lines
        self.current_iteration = 0
        self.possible_blocks = [
            # blocks.HorizontalLine4Block,
            blocks.TBlock1,
            blocks.VerticalLine4Block,
            blocks.SHorizontalBlock,
            blocks.SVerticalBlock,
            blocks.ZHorizontalBlock,
            blocks.ZVerticalBlock,
        ]

        self.board = Board(self.max_x, self.max_y)
        self.populate_starting_board()

        self.player = Player(self, self.max_x // 2, self.max_y - 1)
        self.board.add_object(self.player)

        self.blocks_eaten = 0

    obituary = 'Ś.P. Kret zdechł'

    def next_iteration(self):
        self.current_iteration += 1

        for x, y, cell_value in self.board.traverse_all_board_cells_in_reversed_order():
            if isinstance(cell_value, Block):
                block: Block = cell_value

                if block.age == self.current_iteration:
                    continue

                if self.board.can_block_be_moved(block, 0, 1):
                    self.board.move_object_down(block)
                    block.age_not_in_motion = 0
                else:
                    block.age_not_in_motion += 1
                block.age = self.current_iteration

    def generate_new_block(self, tries=5, location: None | Point2D = None):
        new_block = choice(self.possible_blocks)
        block_location = location or Point2D(randint(0, self.max_x), 0)
        for _ in range(tries):
            try:
                self.board.add_object(new_block(block_location.x, block_location.y), self.current_iteration)
                break
            except IndexError:
                pass

    def destroy_static_block(self):
        x, y = randint(0, self.max_x - 1), randint(0, self.max_y - 1)
        cell_value = self.board.read_cell(x, y)
        if not isinstance(cell_value, Block):
            return
        block: Block = cell_value

        if block.age_not_in_motion != 0:
            self.board.remove_object_in_cell(x, y)

    def populate_starting_board(self):
        for _ in range(self.board.max_x * self.board.max_y // 3):
            self.generate_new_block(tries=1,
                                    location=Point2D(
                                        x=randint(0, self.max_x),
                                        y=randint(0, self.max_y))
                                    )
            self.next_iteration()
            self.board.remove_object_in_cell(self.max_x // 2, self.max_y - 1)
        self.current_iteration = 0

    def traverse_visible_board_cells(self):
        yield from ((x, y - self.upper_lines, cell_value)
                    for x, y, cell_value
                    in self.board.traverse_all_board_cells()
                    if y >= self.upper_lines)
