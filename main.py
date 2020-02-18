import copy
import csv


class SudokuSolver:
    """Solves a sudoku using a backtracking/recursive approach"""
    def __init__(self, grid: list):
        self.grid = grid
        self.found_solutions = []

    def is_possible(self, row, col, num):
        """Check whether a number is possible/valid in a given location"""

        # Check each element in this row, by checking each column index
        for _col in range(9):
            if self.grid[row][_col] == num:
                return False

        # Check each element in this column, by checking each row index
        for _row in range(9):
            if self.grid[_row][col] == num:
                return False

        # Square. Check all elements in this square
        # Work out a start point for both col and row, by checking where the value currently lies between 1-9
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

        # Now search through this square, returning false if the number is found
        for _row in range(row_from, row_from+3):
            for _col in range(col_from, col_from+3):
                if self.grid[_row][_col] == num:
                    return False

        # Must be available if the number hasn't been found.
        return True

    def solve(self, find_all=True) -> bool:
        """Attempt to solve the sudoku"""

        for row in range(9):  # Loop through each row
            for col in range(9):  # Loop through each column
                if self.grid[row][col] == 0:  # Check if the current cell is empty
                    for num in range(1, 10): # Loop through all numbers
                        if self.is_possible(row, col, num):  # Check if the number is a valid option
                            # Update the number, then try solve again based on the new data
                            self.grid[row][col] = num
                            if self.solve(find_all=find_all):
                                if find_all:
                                    # Reset this cell so other options can be attempted one recursion back
                                    self.grid[row][col] = 0
                                else:
                                    return True
                            else:
                                # Reset this cell so other options can be attempted one recursion back
                                self.grid[row][col] = 0

                    return False

        self.found_solutions.append(copy.deepcopy(self.grid))
        return True

    @classmethod
    def csv_to_grid(cls, filename) -> list:
        """Attempts to read a csv file and parse valid grid data from it"""

        with open(filename, "r") as file:
            reader = csv.reader(file, delimiter=",")

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
                                raise ValueError("File not formatted correctly. "
                                           "Only Integers between 0-9 or 'solution' trigger allowed.")
                        except:
                            raise ValueError("File not formatted correctly. "
                                       "Only Integers between 0-9 or 'solution' trigger allowed.")

                if item == "solution":
                    continue
                elif parse_as_solution:
                    solution.append(new_row)
                else:
                    grid.append(new_row)

        # Ignore the solution parse for now, we aren't using it.
        return grid

    @classmethod
    def print_grid(cls, grid):
        """Displays the grid in a prettified way"""
        rows = 0

        for row in grid:
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


if __name__ == "__main__":
    ss = SudokuSolver(SudokuSolver.csv_to_grid('test_files/board1.csv'))
    print("Testing find all solutions: ")
    ss.solve()
    print(f"Solutions found: {len(ss.found_solutions)}")
    for solution in ss.found_solutions:
        print("Solution: ")
        SudokuSolver.print_grid(solution)

    print("\n\nTesting find 1 solution")
    ss = SudokuSolver(SudokuSolver.csv_to_grid('test_files/board1.csv'))
    ss.solve(find_all=False)
    print(f"Solutions found: {len(ss.found_solutions)}")
    for solution in ss.found_solutions:
        print("Solution: ")
        SudokuSolver.print_grid(solution)