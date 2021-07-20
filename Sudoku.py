import pygame
import copy
import time

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

initial_board = [[7, 8, 0, 4, 0, 0, 1, 2, 0],
                 [6, 0, 0, 0, 7, 5, 0, 0, 9],
                 [0, 0, 0, 6, 0, 1, 0, 7, 8],
                 [0, 0, 7, 0, 4, 0, 2, 6, 0],
                 [0, 0, 1, 0, 5, 0, 9, 3, 0],
                 [9, 0, 4, 0, 6, 0, 0, 0, 5],
                 [0, 7, 0, 3, 0, 0, 0, 1, 2],
                 [1, 2, 0, 0, 0, 7, 4, 0, 0],
                 [0, 4, 9, 2, 0, 6, 0, 0, 7]]
# Creating a clone of initial board. This is the board to be updated throughout the game.
board = copy.deepcopy(initial_board)

# Colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (106, 226, 63)
BLUE = (38, 44, 242)


# Handles the actual puzzle
class Puzzle:
    def __init__(self, initial_board, board, solvable):
        self.initial_board = initial_board
        self.board = board
        self.solvable = solvable

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

    def get_block_number(self, row_number, column_number):
        across_block_number = row_number // 3
        vertical_block_number = column_number // 3
        if (across_block_number, vertical_block_number) == (0, 0):
            return 0
        elif (across_block_number, vertical_block_number) == (0, 1):
            return 1
        elif (across_block_number, vertical_block_number) == (0, 2):
            return 2
        elif (across_block_number, vertical_block_number) == (1, 0):
            return 3
        elif (across_block_number, vertical_block_number) == (1, 1):
            return 4
        elif (across_block_number, vertical_block_number) == (1, 2):
            return 5
        elif (across_block_number, vertical_block_number) == (2, 0):
            return 6
        elif (across_block_number, vertical_block_number) == (2, 1):
            return 7
        elif (across_block_number, vertical_block_number) == (2, 2):
            return 8

    # Checks if the board is completely filled.
    def check_board_filled(self):
        for row in board:
            if 0 in row:
                return False
        return True

    # Here, the row number is between 0 and 8.
    def check_single_row(self, row_number):
        row = self.board[row_number]
        num_zeroes = row.count(0)
        distinct_numbers = set(row)
        if 0 in row:
            if len(row) - num_zeroes + 1 > len(distinct_numbers):
                return False
        elif 0 not in row:
            if len(row) > len(distinct_numbers):
                return False
        return True

    # Here, the column number is between 0 and 8.
    def check_single_column(self, column_number):
        column = []
        for row in self.board:
            column.append(row[column_number])
        num_zeroes = column.count(0)
        distinct_numbers = set(column)
        if 0 in column:
            if len(column) - num_zeroes + 1 > len(distinct_numbers):
                return False
        elif 0 not in column:
            if len(column) > len(distinct_numbers):
                return False
        return True

    # Gets the 9 blocks of the sudoku board (each represented by a row of 9 numbers).
    def get_blocks(self):
        blocks = []
        for i in range(0, NUM_ROWS, 3):
            for j in range(0, NUM_COLUMNS, 3):
                blocks.append(board[i][j:j + 3] + board[i + 1][j: j + 3] + board[i + 2][j: j + 3])
        return blocks

    # Here, the block number is between 0 and 8. The block numbers go left to right (start left when new row).
    def check_single_block(self, block_number):
        block = self.get_blocks()[block_number]
        num_zeroes = block.count(0)
        distinct_numbers = set(block)
        if 0 in block:
            if len(block) - num_zeroes + 1 > len(distinct_numbers):
                return False
        elif 0 not in block:
            if len(block) > len(distinct_numbers):
                return False
        return True

    def check_successful(self):
        if not self.check_board_filled():
            return False
        for i in range(NUM_ROWS):
            if not self.check_single_row(i):
                return False
            elif not self.check_single_column(i):
                return False
            elif not self.check_single_block(i):
                return False
        return True

    def solve(self):

        # Get empty cells
        empty_cells = []
        for i in range(NUM_ROWS):
            for j in range(NUM_COLUMNS):
                if initial_board[i][j] == 0:
                    empty_cells.append((i, j))

        index = 0
        number = 1
        while not self.check_successful():
            time.sleep(0.1)
            row_num = empty_cells[index][0]
            col_num = empty_cells[index][1]
            block_num = self.get_block_number(row_num, col_num)
            self.board[row_num][col_num] = number

            # Visualise the solving process
            screen.window.fill(WHITE)
            screen.draw_lines()
            screen.render_numbers()
            screen.render_single_number(row_num, col_num)
            screen.solve_highlight_box(row_num, col_num)
            screen.render_bottom_instructions()
            pygame.display.update()

            if self.check_single_row(row_num) and self.check_single_column(col_num) \
                    and self.check_single_block(block_num):
                index += 1
                number = 1
            else:
                number += 1

                # We have tried every number for the cell.
                if number == 10:
                    # We have tried every number for the first empty (relative to initial board)
                    # cell and thus, the puzzle is unsolvable (using backtracking).
                    if index == 0:
                        self.solvable = False
                        break
                    else:
                        # Find the empty (relative to initial board) cell that is not 9. Also reset the current cell.
                        self.board[row_num][col_num] = 0
                        index -= 1
                        row_num = empty_cells[index][0]
                        col_num = empty_cells[index][1]
                        number = board[row_num][col_num] + 1
                        while self.board[row_num][col_num] == 9:
                            self.board[row_num][col_num] = 0
                            index -= 1
                            row_num = empty_cells[index][0]
                            col_num = empty_cells[index][1]
                            number = board[row_num][col_num] + 1


# Handles GUI
class Screen:
    def __init__(self, window, caption, rows, columns, focused):
        self.window = window
        self.caption = caption
        self.rows = rows
        self.columns = columns
        self.focused = focused

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
        instruction = instruction_font.render("Press spacebar to solve", False, BLACK)
        self.window.blit(instruction, (10, 560))

    def render_single_number(self, row_num, col_num):
        x_pos = (col_num * 60 + col_num * 60 + 2) / 2
        y_pos = (row_num * 60 + row_num * 60 + 2) / 2
        if not puzzle.initial_board[row_num][col_num] == 0:
            number = number_font.render(str(puzzle.board[row_num][col_num]), 1, BLACK)
        else:
            number = number_font.render(str(puzzle.board[row_num][col_num]), 1, BLUE)
        self.window.blit(number, (x_pos, y_pos))

    def render_numbers(self):
        for i in range(len(puzzle.board)):
            for j in range(len(puzzle.board)):
                if 1 <= puzzle.board[i][j] <= 9:
                    self.render_single_number(i, j)

    # Highlights the box that is currently in focus in green.
    def highlight_box(self, click_position):
        x_pos = click_position[0]
        y_pos = click_position[1]
        x_remainder = x_pos % INCREMENT
        y_remainder = y_pos % INCREMENT
        left_line = x_pos - x_remainder
        top_line = y_pos - y_remainder
        pygame.draw.rect(self.window, GREEN, (left_line, top_line, INCREMENT, INCREMENT), 2)

    # Highlights the box currently being solved (used for backtracking algorithm).
    def solve_highlight_box(self, row_num, col_num):
        pygame.draw.rect(self.window, GREEN, (col_num * INCREMENT, row_num * INCREMENT, INCREMENT, INCREMENT), 2)

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
            if puzzle.initial_board[index[0]][index[1]] == 0:
                screen.focused = True

            else:
                screen.focused = False


puzzle = Puzzle(initial_board, board, True)
screen = Screen(pygame.display.set_mode((SCREEN_WIDTH, SCREEN_LENGTH + BOTTOM_BIT)),
                pygame.display.set_caption("Sudoku"), [], [], False)
screen.set_rows_and_columns()


def main():
    running = True
    while running:
        screen.window.fill(WHITE)
        screen.draw_lines()
        screen.render_numbers()
        screen.render_bottom_instructions()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if not puzzle.check_board_filled():
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

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        puzzle.solve()

        if not puzzle.check_board_filled() and screen.focused:
            screen.highlight_box(click_pos)

        elif puzzle.check_board_filled():
            screen.render_ending_message()

        if not puzzle.solvable:
            message1 = ending_font.render("The puzzle cannot be", 1, BLACK)
            message2 = ending_font.render("solved in its current form", 1, BLACK)
            message3 = ending_font.render("(using backtracking algorithm", 1, BLACK)
            screen.window.blit(message1, (260, 540))
            screen.window.blit(message2, (260, 560))
            screen.window.blit(message3, (260, 580))

        pygame.display.update()


main()
