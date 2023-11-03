from dataclasses import dataclass

import pygame
from pygame import Rect
from engine import blocks
from engine.player import Player
from engine.game import Game, GameEnd

pygame.init()

clock = pygame.time.Clock()
running = True
dt = 0


@dataclass
class Offset:
    x: int
    y: int


class Renderer:
    def __init__(self, game: Game, unit: int):
        self.game = game
        self.unit = unit
        self.screen_x = (game.max_x + 2) * self.unit
        self.screen_y = (game.max_y - game.upper_lines + 2) * self.unit
        self.screen = pygame.display.set_mode((self.screen_x, self.screen_y))

    color_dict = {
        blocks.SHorizontalBlock: 'green',
        blocks.SVerticalBlock: 'green',
        blocks.ZHorizontalBlock: 'yellow',
        blocks.ZVerticalBlock: 'yellow',
        blocks.TBlock1: 'red',
        blocks.HorizontalLine4Block: 'blue',
        blocks.VerticalLine4Block: 'blue',
    }

    def draw_block(self, x, y, color="black"):
        # center
        pygame.draw.rect(self.screen, color, Rect(x * self.unit, y * self.unit, self.unit, self.unit))
        # outline
        # pygame.draw.rect(self.screen, "black", Rect(x * self.unit, y * self.unit, self.unit, self.unit))
        # outline left top
        pygame.draw.line(self.screen, "black", (x * self.unit, y * self.unit), ((x+1) * self.unit - 1, y * self.unit))
        pygame.draw.line(self.screen, "black", (x * self.unit, y * self.unit), (x * self.unit, (y+1) * self.unit))

    def draw_player(self, x, y):
        pygame.draw.circle(self.screen, "black", (x * self.unit + self.unit // 2, y * self.unit + self.unit // 2),
                           self.unit // 2)

    def draw_text(self, x, y, text: str):
        font = pygame.font.Font('freesansbold.ttf', 24)
        text = font.render(text, True, pygame.color.THECOLORS['black'], pygame.color.THECOLORS['white'])
        text_rect = text.get_rect()
        text_rect.topleft = (x, y)
        self.screen.blit(text, text_rect)

    def draw_game(self):
        self.screen.fill("white")
        offset = Offset(x=1, y=1)

        board_border = 5
        pygame.draw.rect(self.screen,
                         "lightblue",
                         Rect(
                             offset.x * self.unit - board_border,
                             offset.y * self.unit - board_border,
                             self.game.max_x * self.unit + board_border * 2,
                             (self.game.max_y - self.game.upper_lines) * self.unit + board_border * 2)
                         )

        for x, y, cell_value in game.traverse_visible_board_cells():
            x = x + offset.x
            y = y + offset.y
            color = self.color_dict.get(type(cell_value))
            if color:
                self.draw_block(x, y, color)
            elif cell_value is None:
                pass
            elif isinstance(cell_value, Player):
                self.draw_player(x, y)

        message = f'blocks eaten: {game.blocks_eaten}'
        self.draw_text(self.unit, 8, message)

        pygame.display.flip()

    def draw_obituary(self):
        font = pygame.font.Font('freesansbold.ttf', 24)
        text = font.render(self.game.obituary, True, pygame.color.THECOLORS['black'], pygame.color.THECOLORS['white'])
        textRect = text.get_rect()
        textRect.center = (self.screen_x // 2, self.screen_y // 2)
        self.screen.blit(text, textRect)


# regular
game = Game(16, 16)
renderer = Renderer(game, unit=50)

# wide
# game = Game(32, 16)
# renderer = Renderer(game, unit=40)

# ultra wide
# game = Game(64, 32)
# renderer = Renderer(game, unit=30)

frame = 0

FPS = 100
FRAMELENGTH = 1 / FPS
GAME_SPEED_MULTIPLIER = 1

frames_per_iteration = FPS // GAME_SPEED_MULTIPLIER
frames_per_new_block = 6
frames_until_player_fall = 100  # TODO: needs to be relative to iteration speed
last_up_movement_frame = 0
last_movement_frame = 0

try:
    while running:
        frame += 1

        if game.player.is_dead():
            raise GameEnd()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_w, pygame.K_UP):
                    game.player.move_y(-1)
                    last_movement_frame = frame + 1
                    last_up_movement_frame = frame - 1  # TODO: fix that
                if event.key in (pygame.K_a, pygame.K_LEFT):
                    game.player.move_x(-1)
                    last_movement_frame = frame + 1
                if event.key in (pygame.K_d, pygame.K_RIGHT):
                    game.player.move_x(1)
                    last_movement_frame = frame + 1
                if event.key == pygame.K_q:
                    running = False

        if (frame - last_movement_frame) % frames_per_iteration == 0:
            if (frame // frames_per_iteration) % frames_per_new_block:
                game.generate_new_block()
            game.destroy_static_block()
            game.next_iteration()
            refresh_needed = True

        if (frame - last_up_movement_frame) % frames_until_player_fall == 0:
            game.player.move_y(1)
            refresh_needed = True

        renderer.draw_game()
        dt = clock.tick(60) / 1000

except GameEnd:
    renderer.draw_obituary()
    pygame.display.flip()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                running = False

pygame.quit()
