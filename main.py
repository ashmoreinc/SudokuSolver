import csv
import copy

grid = []
solution = []
found_solutions = []


def get_board_from_file(file_name):
    """Reads a CSV file and parses the data into a grid"""
    global grid, solution

    with open(file_name, "r") as file:
        reader = csv.reader(file)

        # Flags whether we should parse what we read as a solution, change triggered by finding solution
        # In the read file
        parse_as_solution = False

        grid = []
        solution = []

        for row in reader:
            new_row = []
            for item in row:
                if item == "solution":
                    parse_as_solution = True

                    break
                elif item == "0":
                    new_row.append(0)
                else:
                    try:
                        item = int(item)
                        if 1 <= item <= 9:
                            new_row.append(item)
                        else:
                            ValueError("File not formatted correctly. "
                                       "Only Integers between 0-9 or 'solution' trigger allowed.")
                    except:
                        ValueError("File not formatted correctly. "
                                   "Only Integers between 0-9 or 'solution' trigger allowed.")

            if item == "solution":
                continue
            elif parse_as_solution:
                solution.append(new_row)
            else:
                grid.append(new_row)


def print_grid(_grid):
    """Displays the grid in a prettified way"""
    rows = 0

    for row in _grid:
        if rows == 3:
            print("-" * 21)
            rows = 0
        cols = 0
        for cell in row:
            if cols == 3:
                cols = 0
                print("|", end=" ")
            print(str(cell), end=" ")
            cols += 1

        print()
        rows += 1


def is_possible(row, col, num):
    """Check if a move is possible by checking the row, column, and square for any other occurrences"""
    global grid

    # Row
    for _col in range(9):
        if grid[row][_col] == num:
            return False

    # Column
    for _row in range(9):
        if grid[_row][col] == num:
            return False

    # Square
    row_from = 0
    col_from = 0

    if row < 3:
        row_from = 0
    elif row < 6:
        row_from = 3
    else:
        row_from = 6

    if col < 3:
        col_from = 0
    elif col < 6:
        col_from = 3
    else:
        col_from = 6

    for _row in range(row_from, row_from+3):
        for _col in range(col_from, col_from + 3):
            if grid[_row][_col] == num:
                return False

    # If nothing is caught, it must be available
    return True


def solve(find_all=True):
    """Attempt to recursively solve the sudoku"""
    # Find all means it will stop everything after finding one solution
    # Useful if the user  only wants a single solution.
    global grid, found_solutions

    for row in range(9):
        for col in range(9):
            if grid[row][col] == 0:
                for num in range(1, 10):
                    if is_possible(row, col, num):
                        grid[row][col] = num
                        if not solve(find_all=find_all) or find_all:
                            grid[row][col] = 0
                        else:
                            return True
                return False
    # Output result
    print("Found a solution:")
    print_grid(grid)

    # Append the solution to the list of possible solutions
    found_solutions.append(copy.deepcopy(grid))

    return True


if __name__ == "__main__":
    get_board_from_file('board3.csv')

    print("Initial Grid")
    print_grid(grid)

    solve(find_all=False)

    for i in range(len(found_solutions)):
        if solution:
            print(f"Solution ({i+1}) matches given solution: {solution == found_solutions[i]}")