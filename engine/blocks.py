from typing import List

from engine.point import Point2D


class Block:
    def __init__(self, x: int, y: int, char: str = 'X'):
        self.location: List[Point2D | None] = [Point2D(x, y)]
        self.char = char
        self.age = 0
        self.age_not_in_motion = 0


class PointBlock(Block):
    def __init__(self, x: int, y: int, char='P'):
        super().__init__(x, y, char=char)
        self.location: List[Point2D] = [Point2D(x, y)]


class HorizontalLine4Block(Block):
    # this block is not present in the original Kret
    def __init__(self, x: int, y: int, char='L'):
        super().__init__(x, y, char=char)
        self.location: List[Point2D] = [Point2D(x, y),
                                        Point2D(x + 1, y),
                                        Point2D(x + 2, y),
                                        Point2D(x + 3, y)]


class VerticalLine4Block(Block):
    def __init__(self, x: int, y: int, char='L'):
        super().__init__(x, y, char=char)
        self.location: List[Point2D] = [Point2D(x, y),
                                        Point2D(x, y + 1),
                                        Point2D(x, y + 2),
                                        Point2D(x, y + 3)]


class TBlock1(Block):
    def __init__(self, x: int, y: int, char='R'):
        super().__init__(x, y, char=char)
        self.location: List[Point2D] = [Point2D(x, y),
                                        Point2D(x + 1, y),
                                        Point2D(x + 2, y),
                                        Point2D(x + 1, y + 1)]


class SHorizontalBlock(Block):
    def __init__(self, x: int, y: int, char='S'):
        super().__init__(x, y, char=char)
        self.location: List[Point2D] = [Point2D(x + 1, y),
                                        Point2D(x + 2, y),
                                        Point2D(x, y + 1),
                                        Point2D(x + 1, y + 1)]


class SVerticalBlock(Block):
    def __init__(self, x: int, y: int, char='S'):
        super().__init__(x, y, char=char)
        self.location: List[Point2D] = [Point2D(x, y),
                                        Point2D(x, y + 1),
                                        Point2D(x + 1, y + 1),
                                        Point2D(x + 1, y + 2)]


class ZHorizontalBlock(Block):
    def __init__(self, x: int, y: int, char='Z'):
        super().__init__(x, y, char=char)
        self.location: List[Point2D] = [Point2D(x, y),
                                        Point2D(x + 1, y),
                                        Point2D(x + 1, y + 1),
                                        Point2D(x + 2, y + 1)]


class ZVerticalBlock(Block):
    def __init__(self, x: int, y: int, char='Z'):
        super().__init__(x, y, char=char)
        self.location: List[Point2D] = [Point2D(x + 1, y),
                                        Point2D(x, y + 1),
                                        Point2D(x + 1, y + 1),
                                        Point2D(x, y + 2)]
