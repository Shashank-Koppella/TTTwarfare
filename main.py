import pygame
from pygame.locals import *

# Initializing Pygame
pygame.init()

# Screen
info = pygame.display.Info()
screen_width = info.current_w
screen_height = info.current_h - 60
screen = pygame.display.set_mode((screen_width, screen_height))

# Title
pygame.display.set_caption("TicTacToe Warfare")

# Board
board_length = min(screen.get_width(), screen.get_height()) * 0.9
board_x = (screen_width - board_length) // 2
board_y = (screen_height - board_length) // 2
board_line_thickness = 10

# Cells
cell_length = board_length // 3

# Reduction factor for sub-boards
reduction_factor = 0.8

# Sub-Board
sub_board_length = cell_length * reduction_factor
sub_board_win = 0

# Sub-Cells
sub_cell_length = sub_board_length // 3
sub_cell_line_thickness = 2

# To check if a sub cell is being highlighted
highlighted_sub_cell = None

# Defining colour constants
Background_Colour = (230, 204, 153)
Highlight_Colour = (240, 240, 240, 100)  # Light gray with transparency
Sub_Board_Colour = (0, 0, 0)
Board_Colour = (0, 0, 0)

# Symbol images
symbol1_image = pygame.image.load("x.png")  # Replace "symbol1.png" with the actual filename and extension
symbol1_image = pygame.transform.scale(symbol1_image, (sub_cell_length, sub_cell_length))
symbol2_image = pygame.image.load("o.png")  # Replace "symbol2.png" with the actual filename and extension
symbol2_image = pygame.transform.scale(symbol2_image, (sub_cell_length, sub_cell_length))
symbol_size = int(sub_cell_length * 0.5)
symbol1_image_scaled = pygame.transform.scale(symbol1_image, (symbol_size, symbol_size))
symbol2_image_scaled = pygame.transform.scale(symbol2_image, (symbol_size, symbol_size))
symbol_offset = (sub_cell_length - symbol_size) // 2

# Initialize the state of each cell
cell_states = [[[[None for i in range(3)] for i in range(3)] for i in range(3)] for i in range(3)]

# Game Loop
FPS = 30
running = True
clock = pygame.time.Clock()
current_symbol = symbol1_image_scaled  # Start with symbol1


def check_subboard_win(row, col, srow, scol):
    symbol = cell_states[row][col][srow][scol]

    # Check rows
    if all(cell_states[row][col][srow][i] == symbol for i in range(3)):
        return True

    # Check columns
    if all(cell_states[row][col][i][scol] == symbol for i in range(3)):
        return True

    # Check diagonal from top-left to bottom-right
    if (
            cell_states[row][col][0][0] == symbol
            and cell_states[row][col][1][1] == symbol
            and cell_states[row][col][2][2] == symbol
    ):
        return True

    # Check diagonal from top-right to bottom-left
    if (
            cell_states[row][col][0][2] == symbol
            and cell_states[row][col][1][1] == symbol
            and cell_states[row][col][2][0] == symbol
    ):
        return True

    return False


while running:
    clock.tick(FPS)

    event = pygame.event.poll()
    if event.type == pygame.QUIT:
        running = False
    elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        mouse_x, mouse_y = pygame.mouse.get_pos()

        if board_x <= mouse_x <= board_x + board_length and board_y <= mouse_y <= board_y + board_length:
            cell_col = int((mouse_x - board_x) // cell_length)
            cell_row = int((mouse_y - board_y) // cell_length)
            sub_board_x = board_x + cell_col * cell_length + (cell_length - sub_board_length) // 2
            sub_board_y = board_y + cell_row * cell_length + (cell_length - sub_board_length) // 2

            sub_cell_col = int(
                (mouse_x - board_x - cell_col * cell_length - (cell_length - sub_board_length) // 2) // sub_cell_length
            )
            sub_cell_row = int(
                (mouse_y - board_y - cell_row * cell_length - (cell_length - sub_board_length) // 2) // sub_cell_length
            )

            if (
                    0 <= sub_cell_col < 3
                    and 0 <= sub_cell_row < 3
                    and cell_states[cell_row][cell_col][sub_cell_row][sub_cell_col] is None
            ):
                if current_symbol == symbol1_image_scaled:
                    cell_states[cell_row][cell_col][sub_cell_row][sub_cell_col] = "symbol1"
                    current_symbol = symbol2_image_scaled
                    if check_subboard_win(cell_row, cell_col, sub_cell_row, sub_cell_col):
                        sub_board_win = current_symbol
                else:
                    cell_states[cell_row][cell_col][sub_cell_row][sub_cell_col] = "symbol2"
                    current_symbol = symbol1_image_scaled
                    check_subboard_win(cell_row, cell_col, sub_cell_row, sub_cell_col)
                    if check_subboard_win(cell_row, cell_col, sub_cell_row, sub_cell_col):
                        sub_board_win = current_symbol

    screen.fill(Background_Colour)

    mouse_x, mouse_y = pygame.mouse.get_pos()

    # Update highlighted_sub_cell
    highlighted_sub_cell = None

    if board_x <= mouse_x <= board_x + board_length and board_y <= mouse_y <= board_y + board_length:
        cell_col = int((mouse_x - board_x) // cell_length)
        cell_row = int((mouse_y - board_y) // cell_length)
        sub_board_x = board_x + cell_col * cell_length + (cell_length - sub_board_length) // 2
        sub_board_y = board_y + cell_row * cell_length + (cell_length - sub_board_length) // 2

        sub_cell_col = int(
            (mouse_x - board_x - cell_col * cell_length - (cell_length - sub_board_length) // 2) // sub_cell_length
        )
        sub_cell_row = int(
            (mouse_y - board_y - cell_row * cell_length - (cell_length - sub_board_length) // 2) // sub_cell_length
        )

        if (
                0 <= sub_cell_col < 3
                and 0 <= sub_cell_row < 3
                and cell_states[cell_row][cell_col][sub_cell_row][sub_cell_col] is None
        ):
            highlighted_sub_cell = (cell_col, cell_row, sub_cell_col, sub_cell_row)

    for i in range(1, 3):
        pygame.draw.line(
            screen,
            Board_Colour,
            (board_x + i * cell_length, board_y),
            (board_x + i * cell_length, board_y + board_length),
            board_line_thickness,
        )

        pygame.draw.line(
            screen,
            Board_Colour,
            (board_x, board_y + i * cell_length),
            (board_x + board_length, board_y + i * cell_length),
            board_line_thickness,
        )

    for cell_row in range(3):
        for cell_col in range(3):
            sub_board_x = board_x + cell_col * cell_length + (cell_length - sub_board_length) // 2
            sub_board_y = board_y + cell_row * cell_length + (cell_length - sub_board_length) // 2

            for i in range(1, 3):
                pygame.draw.line(
                    screen,
                    Sub_Board_Colour,
                    (sub_board_x + i * sub_cell_length, sub_board_y),
                    (sub_board_x + i * sub_cell_length, sub_board_y + sub_board_length),
                    sub_cell_line_thickness,
                )

                pygame.draw.line(
                    screen,
                    Sub_Board_Colour,
                    (sub_board_x, sub_board_y + i * sub_cell_length),
                    (sub_board_x + sub_board_length, sub_board_y + i * sub_cell_length),
                    sub_cell_line_thickness,
                )

            for sub_cell_row in range(3):
                for sub_cell_col in range(3):
                    sub_board_cell_x = sub_board_x + sub_cell_col * sub_cell_length
                    sub_board_cell_y = sub_board_y + sub_cell_row * sub_cell_length

                    if (
                            cell_states[cell_row][cell_col][sub_cell_row][sub_cell_col] == "symbol1"
                            and (cell_col, cell_row, sub_cell_col, sub_cell_row) != highlighted_sub_cell
                    ):
                        screen.blit(symbol1_image, (sub_board_cell_x, sub_board_cell_y))
                    elif (
                            cell_states[cell_row][cell_col][sub_cell_row][sub_cell_col] == "symbol2"
                            and (cell_col, cell_row, sub_cell_col, sub_cell_row) != highlighted_sub_cell
                    ):
                        screen.blit(symbol2_image, (sub_board_cell_x, sub_board_cell_y))

                    if (cell_col, cell_row, sub_cell_col, sub_cell_row) == highlighted_sub_cell:
                        pygame.draw.rect(
                            screen,
                            Highlight_Colour,
                            (sub_board_cell_x, sub_board_cell_y, sub_cell_length, sub_cell_length),
                        )

                        if cell_states[cell_row][cell_col][sub_cell_row][sub_cell_col] == "symbol1":
                            screen.blit(
                                symbol1_image,
                                (sub_board_cell_x, sub_board_cell_y),
                            )
                        elif cell_states[cell_row][cell_col][sub_cell_row][sub_cell_col] == "symbol2":
                            screen.blit(
                                symbol2_image,
                                (sub_board_cell_x, sub_board_cell_y),
                            )
                        if sub_board_win != 0:
                            screen.blit(
                                sub_board_win,
                                (board_x,board_y),
                            )

    pygame.display.flip()

# Quit the game
pygame.quit()
