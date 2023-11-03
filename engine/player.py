from typing import List

from engine.blocks import Block
from engine.point import Point2D


class Player:
    def __init__(self, game, x, y):
        self.game = game
        self.location: List[Point2D] = [Point2D(x, y)]
        self.char = 'K'

    def move_x(self, dx):
        new_p_x = self.location[0].x + dx
        new_p_y = self.location[0].y
        try:
            cell_value = self.game.board.read_cell(new_p_x, new_p_y)
        except IndexError:
            return

        if isinstance(cell_value, Block):
            self.game.board.remove_object_in_cell(new_p_x, new_p_y)
            self.game.blocks_eaten += 1
        if self.game.board.can_block_be_moved(self, dx, 0):
            self.game.board.move_object(self, dx, 0)

    def move_y(self, dy):
        new_p_x = self.location[0].x
        new_p_y = self.location[0].y + dy
        try:
            cell_value = self.game.board.read_cell(new_p_x, new_p_y)
        except IndexError:
            return

        if isinstance(cell_value, Block) and dy < 0:
            # cannot destroy blocks with down movement
            self.game.board.remove_object_in_cell(new_p_x, new_p_y)
            self.game.blocks_eaten += 1
        if self.game.board.can_block_be_moved(self, 0, dy):
            self.game.board.move_object(self, 0, dy)

    def is_dead(self):
        player_location = self.location[0]
        cell_value = self.game.board.read_cell(player_location.x, player_location.y)
        if isinstance(cell_value, Player):
            return False
        else:
            return True
