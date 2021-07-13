import pygame

pygame.init()

SCREEN_WIDTH = 540
SCREEN_LENGTH = 540
NUM_ROWS = 9
NUM_COLUMNS = 9
INCREMENT = int(SCREEN_LENGTH / NUM_ROWS)
font = pygame.font.SysFont("monospace", 15)

board = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 3, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 2, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 8, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0]]

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


# Handles the actual puzzle
class Puzzle():
    def __init__(self, board):
        self.board = board

    def make_move(self, coordinate, number):
        x_coord = coordinate[0]
        y_coord = coordinate[1]
        if 1 <= number <= 9:
            board[x_coord][y_coord] = number


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
                        x_pos = j * 60
                        y_pos = i * 60
                        number = font.render(str(self.puzzle.board[i][j]), 1, BLACK)
                        self.window.blit(number, (x_pos, y_pos))


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

        pygame.display.update()

main()