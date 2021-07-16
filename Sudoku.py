import pygame
import copy

pygame.init()

# Constants to do with GUI
SCREEN_WIDTH = 540
SCREEN_LENGTH = 540
BOTTOM_BIT = 60
NUM_ROWS = 9
NUM_COLUMNS = 9
INCREMENT = int(SCREEN_LENGTH / NUM_ROWS)

number_font = pygame.font.SysFont("twcencondensed", 50)
ending_font = pygame.font.SysFont("twocencondensed", 30)
instruction_font = pygame.font.SysFont("twocencondensed", 30)

initial_board = [[5, 3, 4, 6, 7, 8, 9, 1, 2],
                 [6, 7, 2, 1, 9, 5, 3, 4, 8],
                 [1, 9, 8, 3, 4, 2, 5, 6, 7],
                 [8, 5, 9, 7, 6, 1, 4, 2, 3],
                 [4, 2, 6, 8, 5, 3, 7, 9, 1],
                 [7, 1, 3, 9, 2, 4, 8, 5, 6],
                 [9, 6, 1, 5, 3, 7, 2, 8, 4],
                 [2, 8, 7, 4, 1, 9, 6, 3, 5],
                 [3, 4, 5, 2, 8, 6, 1, 7, 0]]

# Creating a clone of initial board. This is the board to be updated throughout the game.
board = copy.deepcopy(initial_board)

# Colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (106, 226, 63)
BLUE = (38, 44, 242)


# Handles the actual puzzle
class Puzzle:
    def __init__(self, initial_board, board):
        self.initial_board = initial_board
        self.board = board

    def make_move(self, coordinate, number):
        x_coord = coordinate[0]
        y_coord = coordinate[1]
        if screen.focused and 1 <= number <= 9:
            board[x_coord][y_coord] = number

    def delete_move(self, coordinate, number):
        x_coord = coordinate[0]
        y_coord = coordinate[1]
        if screen.focused and 1 <= number <= 9:
            board[x_coord][y_coord] = 0

    def check_game_completed(self):
        row_number = 0
        for row in self.board:
            if 0 in row:
                return False
            else:
                row_number += 1

        if row_number == 9:
            return True

    def check_single_row(self, row):
        distinct_numbers = set(row)
        if 0 in distinct_numbers:
            return False
        elif len(row) > len(distinct_numbers):
            return False
        else:
            return True

    # Gets the 9 blocks of the sudoku board (each represented by a row of 9 numbers).
    def get_blocks(self):
        blocks = []
        for i in range(0, NUM_ROWS, 3):
            for j in range(0, NUM_COLUMNS, 3):
                blocks.append(board[i][j:j + 3] + board[i + 1][j: j + 3] + board[i + 2][j: j + 3])
        return blocks

    # Checks if a 3x3 sub matrix is valid.
    def check_block(self, block):
        distinct_numbers = set(block)
        if 0 in distinct_numbers:
            return False
        elif len(block) > len(distinct_numbers):
            return False
        else:
            return True

    # Checks if a single row is valid (or column if we apply this method to the transposed board).
    def check_all_rows(self, board):
        row_number = 0
        for row in board:
            row_number += 1
            if not self.check_single_row(row):
                return False

        if row_number == 9:
            return True

    def check_all_columns(self):
        transposed_board = [[row[i] for row in board] for i in range(NUM_COLUMNS)]
        self.check_all_rows(transposed_board)

    def check_all_blocks(self):
        blocks = self.get_blocks()
        number_blocks = 0
        for block in blocks:
            number_blocks += 1
            if not self.check_block(block):
                return False
        if number_blocks == 9:
            return True

    def check_successful(self):
        if self.check_all_rows(board) and self.check_all_columns and self.check_all_blocks():
            return True
        else:
            return False

    # Checks if an entry of board was in the initial board.
    def part_of_initial_board(self, index):
        if self.initial_board[index[0]][index[1]] == 0:
            return False
        elif 1 <= self.initial_board[index[0]][index[1]] <= 9:
            return True


# Handles GUI
class Screen:
    def __init__(self, window, caption, rows, columns, focused, puzzle):
        self.window = window
        self.caption = caption
        self.rows = rows
        self.columns = columns
        self.focused = focused
        self.puzzle = puzzle

    def set_rows_and_columns(self):
        for i in range(0, SCREEN_LENGTH + 1, INCREMENT):
            self.rows.append(i)
            self.columns.append(i)

    def draw_lines(self):
        for i in range(len(self.columns)):
            # Only necessary for every third line
            thickness = 2

            if i % 3 != 0:
                pygame.draw.line(self.window, BLACK, (self.columns[i], 0), (self.columns[i], SCREEN_LENGTH))
                pygame.draw.line(self.window, BLACK, (0, self.columns[i]), (SCREEN_WIDTH, self.columns[i]))
            else:
                pygame.draw.line(self.window, BLACK, (self.columns[i], 0), (self.columns[i], SCREEN_LENGTH), thickness)
                pygame.draw.line(self.window, BLACK, (0, self.columns[i]), (SCREEN_WIDTH, self.columns[i]), thickness)

    def render_bottom_instructions(self):
        instruction1 = instruction_font.render("Press enter to submit answer", False, BLACK)
        instruction2 = instruction_font.render("Press spacebar to solve", False, BLACK)
        self.window.blit(instruction1, (10, 540))
        self.window.blit(instruction2, (10, 560))

    def render_numbers(self):
        for i in range(len(self.puzzle.board)):
            for j in range(len(self.puzzle.board)):
                # Checks if the number was on the initial_board (in which case, we render the number blue).
                if not self.puzzle.part_of_initial_board((i, j)) and 1 <= self.puzzle.board[i][j] <= 9:
                    if type(self.window) == pygame.Surface:
                        x_pos = (j * 60 + (j * 60 + 2)) / 2
                        y_pos = (i * 60 + (i * 60 + 2)) / 2
                        number = number_font.render(str(self.puzzle.board[i][j]), 1, BLUE)
                        self.window.blit(number, (x_pos, y_pos))
                elif self.puzzle.part_of_initial_board((i, j)) and 1 <= self.puzzle.board[i][j] <= 9:
                    if type(self.window) == pygame.Surface:
                        x_pos = (j * 60 + (j * 60 + 2)) / 2
                        y_pos = (i * 60 + (i * 60 + 2)) / 2
                        number = number_font.render(str(self.puzzle.board[i][j]), 1, BLACK)
                        self.window.blit(number, (x_pos, y_pos))

    # Highlights the box that is currently in focus in green.
    def highlight_box(self, click_position):
        x_pos = click_position[0]
        y_pos = click_position[1]
        x_remainder = x_pos % INCREMENT
        y_remainder = y_pos % INCREMENT
        left_line = x_pos - x_remainder
        top_line = y_pos - y_remainder
        if type(self.window) == pygame.Surface:
            pygame.draw.rect(self.window, GREEN, (left_line, top_line, INCREMENT, INCREMENT), 2)

    def render_ending_message(self):
        if puzzle.check_successful():
            message = ending_font.render("Success!", 1, BLACK)
            self.window.blit(message, (440, 560))
        else:
            message = ending_font.render("You lose!", 1, BLACK)
            self.window.blit(message, (440, 560))

    def set_screen_focused(self, click_pos):
        # A click that is not on a line
        if (click_pos[0] % 60 != 0) and (click_pos[1] % 60 != 0):
            # The index of the board to be updated.
            index = (click_pos[1] // INCREMENT, click_pos[0] // INCREMENT)

            # Checks that the number was not part of the initial board.
            if self.puzzle.initial_board[index[0]][index[1]] == 0:
                screen.focused = True

            else:
                screen.focused = False


puzzle = Puzzle(initial_board, board)
screen = Screen(pygame.display.set_mode((SCREEN_WIDTH, SCREEN_LENGTH + BOTTOM_BIT)),
                pygame.display.set_caption("Sudoku"), [], [], False, puzzle)
screen.set_rows_and_columns()


def main():
    running = True
    while running:
        screen.window.fill(WHITE)
        screen.draw_lines()
        screen.render_numbers()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if not puzzle.check_game_completed():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    click_pos = pygame.mouse.get_pos()
                    screen.set_screen_focused(click_pos)

                if event.type == pygame.KEYDOWN and screen.focused:
                    # Checks if the key pressed is a number.
                    if 48 <= event.key <= 57:
                        key_pressed = event.key - 48
                        index = (click_pos[1] // INCREMENT, click_pos[0] // INCREMENT)
                        puzzle.make_move(index, key_pressed)
                        screen.focused = False
                    elif event.key == pygame.K_BACKSPACE:
                        index = (click_pos[1] // INCREMENT, click_pos[0] // INCREMENT)
                        number = puzzle.board[index[0]][index[1]]
                        puzzle.delete_move(index, number)

        if not puzzle.check_game_completed() and screen.focused:
            screen.highlight_box(click_pos)

        elif puzzle.check_game_completed():
            screen.render_ending_message()

        screen.render_bottom_instructions()

        pygame.display.update()


main()
