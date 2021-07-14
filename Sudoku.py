import pygame

pygame.init()

# Constants to do with GUI
SCREEN_WIDTH = 540
SCREEN_LENGTH = 540
NUM_ROWS = 9
NUM_COLUMNS = 9
INCREMENT = int(SCREEN_LENGTH / NUM_ROWS)

font = pygame.font.SysFont("monospace", 50)

board = [[8, 2, 7, 1, 5, 4, 3, 9, 0],
         [9, 6, 5, 3, 2, 7, 1, 4, 8],
         [3, 4, 1, 6, 8, 9, 7, 5, 2],
         [5, 9, 3, 4, 6, 8, 2, 7, 1],
         [4, 7, 2, 5, 1, 3, 6, 8, 9],
         [6, 1, 8, 9, 7, 2, 4, 3, 5],
         [7, 8, 6, 2, 3, 5, 9, 1, 4],
         [1, 5, 4, 7, 9, 6, 8, 2, 3],
         [2, 3, 9, 8, 4, 1, 5, 6, 0]]

# Colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (106, 226, 63)


# Handles the actual puzzle
class Puzzle():
    def __init__(self, board):
        self.board = board

    def make_move(self, coordinate, number):
        x_coord = coordinate[0]
        y_coord = coordinate[1]
        if 1 <= number <= 9:
            board[x_coord][y_coord] = number

    def check_rows(self, board):
        row_number = 0
        for row in board:
            row_number += 1
            distinct_numbers = set(row)

            # This means that not all spaces have been entered yet and thus, the game cannot be completed.
            if 0 in distinct_numbers:
                return False
            # In other words, not all the numbers in thr row are distinct.
            elif len(row) > len(distinct_numbers):
                return False

        if row_number == 9:
            return True

    def check_columns(self):
        transposed_board = [[row[i] for row in board] for i in range(len(board[0]))]
        self.check_rows(transposed_board)

    def check_successful(self):
        if self.check_rows(board) and self.check_columns:
            return True
        else:
            return False


# Handles GUI
class Screen():
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

    def render_numbers(self):
        for i in range(len((self.puzzle.board))):
            for j in range(len(self.puzzle.board)):
                if 1 <= self.puzzle.board[i][j] <= 9:
                    if type(self.window) == pygame.Surface:
                        x_pos = (j * 60 + (j * 60 + 2)) / 2
                        y_pos = (i * 60 + (i * 60 + 2)) / 2
                        number = font.render(str(self.puzzle.board[i][j]), 1, BLACK)
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
            pygame.draw.rect(self.window, GREEN, (left_line, top_line, INCREMENT, INCREMENT))



puzzle = Puzzle(board)
screen = Screen(pygame.display.set_mode((SCREEN_WIDTH, SCREEN_LENGTH)),
                pygame.display.set_caption("Sudoku"), [], [], False, puzzle)
screen.set_rows_and_columns()


def main():
    running = True
    while running:
        screen.window.fill((WHITE))
        screen.draw_lines()
        screen.render_numbers()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                click_pos = pygame.mouse.get_pos()

                # A click that is not on a line
                if (click_pos[0] % 60 != 0) and (click_pos[1] % 60 != 0):
                    # The index of the board to be updated.
                    index = (click_pos[1] // INCREMENT, click_pos[0] // INCREMENT)

                    # Checks that a move has not been made there already.
                    if puzzle.board[index[0]][index[1]] == 0:
                        screen.focused = True

            if event.type == pygame.KEYDOWN:
                # Checks if the key pressed is a number.
                if 49 <= event.key <= 57:
                    key_pressed = event.key - 48
                    if screen.focused:
                        if 1 <= key_pressed <= 9:
                            puzzle.make_move(index, key_pressed)
                            screen.focused = False

        if screen.focused:
            screen.highlight_box(click_pos)

        # Check if the puzzle has successfully been solved.
        if puzzle.check_successful():
            running = False

        pygame.display.update()


main()
