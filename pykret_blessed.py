# https://blessed.readthedocs.io/en/latest/
from time import sleep

from blessed import Terminal

from engine import blocks
from engine.game import Game, GameEnd
from engine.player import Player


def print_board(game: Game, term: Terminal, double_width=True, empty_char='.', **kwargs):
    print(term.clear)
    BLOCK_CHAR = ' '
    BOTTOM_CHAR = '─'

    char_width = 2 if double_width else 1

    color_dict = {
        blocks.SHorizontalBlock: 'green_reverse',
        blocks.SVerticalBlock: 'green_reverse',
        blocks.ZHorizontalBlock: 'yellow_reverse',
        blocks.ZVerticalBlock: 'yellow_reverse',
        blocks.TBlock1: 'red_reverse',
        blocks.HorizontalLine4Block: 'blue_reverse',
        blocks.VerticalLine4Block: 'blue_reverse',
    }

    for x, y, cell_value in game.traverse_visible_board_cells():
        cell_str = f'{cell_value}'
        color = color_dict.get(type(cell_value))
        if color:
            cell_str = getattr(term, color)(BLOCK_CHAR) * char_width
        elif cell_value is None:
            cell_str = empty_char * char_width
        elif isinstance(cell_value, Player):
            # Surprisingly, "rat" emoji takes two character spaces
            cell_str = '🐀'

        print(cell_str, end='')
        if x == game.max_x - 1:
            print()
    print()

    # draw bottom line
    print(BOTTOM_CHAR * char_width * game.max_x)

    print(f'blocks eaten: {game.blocks_eaten}')

    if debug := kwargs.get('debug'):
        print(f'frame:{debug["frame"]}, iteration:{game.current_iteration}')
        print(f'fps_per_iteration: {debug["fps_per_iteration"]}')
        print('You\'ve pressed ' + term.bold(repr(debug["last_keypress"])))


def print_obituary(game: Game, double_width=True):
    char_width = 2 if double_width else 1

    print(term.move_up(10))
    print(' ' * char_width * game.max_x)
    print(game.obituary.center(char_width * game.max_x))
    print(' ' * char_width * game.max_x)


def calculate_new_frames_per_iteration(frames_per_iteration):
    return frames_per_iteration // 2


if __name__ == '__main__':
    # important: pycharm needs to have "run configuration" set to "emulate terminal"
    term = Terminal()

    MAX_X = 16
    MAX_Y = 16
    DOUBLE_WIDTH = True

    game = Game(MAX_X, MAX_Y)

    GAME_SPEED_MULTIPLIER = 1

    FPS = 100
    FRAMELENGTH = 1 / FPS

    frames_per_iteration = FPS // GAME_SPEED_MULTIPLIER
    frames_per_new_block = 6
    frames_per_block_speed_change = 3 * frames_per_iteration
    frames_until_player_fall = 100  # TODO: needs to be relative to iteration speed
    last_up_movement_frame = 0
    last_movement_frame = 0

    frame = 0
    print(term.clear)

    last_keypress = None
    refresh_needed = True

    try:
        while True:
            if refresh_needed:
                debug = {
                    'frame': frame,
                    'last_keypress': last_keypress,
                    'fps_per_iteration': frames_per_iteration
                }
                print_board(game, term, double_width=DOUBLE_WIDTH, debug=debug)
                refresh_needed = False

            frame += 1
            sleep(FRAMELENGTH)

            if game.player.is_dead():
                raise GameEnd()

            if (frame - last_movement_frame) % frames_per_iteration == 0:
                if (frame // frames_per_iteration) % frames_per_new_block:
                    game.generate_new_block()
                game.destroy_static_block()
                game.next_iteration()
                refresh_needed = True

            if (frame - last_up_movement_frame) % frames_until_player_fall == 0:
                game.player.move_y(1)
                refresh_needed = True

            with term.cbreak(), term.hidden_cursor():
                inp = term.inkey(timeout=FRAMELENGTH)
                if inp:
                    if repr(inp) == 'KEY_RIGHT':
                        game.player.move_x(1)
                    if repr(inp) == 'KEY_LEFT':
                        game.player.move_x(-1)
                    if repr(inp) == 'KEY_UP':
                        game.player.move_y(-1)
                        last_up_movement_frame = frame
                    last_keypress = repr(inp)
                    refresh_needed = True
                    last_movement_frame = frame + 1  # That's tricky, because it will force the next iteration

            if frame % frames_per_block_speed_change == 0:
                new_frames_per_iteration = calculate_new_frames_per_iteration(frames_per_iteration)
                if new_frames_per_iteration > 0:
                    frames_per_iteration = new_frames_per_iteration

    except GameEnd:
        print_obituary(game, double_width=DOUBLE_WIDTH)
        sleep(10)
