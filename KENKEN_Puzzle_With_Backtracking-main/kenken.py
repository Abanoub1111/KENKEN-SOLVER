import sys


class Kenken:
    def __init__(self, file_path):
        self.n, self.grid, self.cages = self.read_input_from_file(file_path)
        if self.cages is None:
            print("Error: Unable to initialize cages.")
            self.cellToCageMap = None  # Set to None in case of error
            return
        self.cellToCageMap = self.mapCellsToCages()

    @staticmethod
    def read_input_from_file(file_path):
        try:
            with open(file_path, 'r') as file:
                n = int(file.readline().strip())
                if(n < 3 or n > 8):
                    print("sorry we only solve puzzles from 3 to 8");
                    sys.exit()
                grid = [[0 for _ in range(n)] for _ in range(n)]
                num_cages = int(file.readline().strip())
                cages = {}
                for i in range(1, num_cages + 1):
                    op = file.readline().strip()
                    value = int(file.readline().strip())
                    cells_input = file.readline().strip()
                    cells = [tuple(map(int, cell.split(','))) for cell in cells_input.split()]
                    cages[i] = {'value': value, 'op': op, 'cells': cells}
                return n, grid, cages
        except FileNotFoundError:
            print(f"Error: File {file_path} not found.")
            return None, None, None
        
    def mapCellsToCages(self):
        cellToCageMap = [[0] * self.n for i in range(self.n)]
        for cage in self.cages:
            cellsOfCageTupleList = self.cages[cage]['cells']
            for cellTuple in cellsOfCageTupleList:
                row = cellTuple[0]
                col = cellTuple[1]
                cellToCageMap[row][col] = cage
        return cellToCageMap


    def Bounding(self, row, col, value):
        isAllConstraintsApplied = False
        conditionsList = [self.check_row(row, value), # --- check row constraint ---
                          self.check_column(col, value), # --- check column constraint ---
                          self.check_cage(row, col, value)] # --- check cage operation constraint ---
        if all(conditionsList):
            isAllConstraintsApplied = True

        return isAllConstraintsApplied

    def check_row(self, row, value):
        isConstraintApplied = True
        for columnItem in self.grid[row]:
            if columnItem == value:
                isConstraintApplied = False

        return isConstraintApplied

    def check_column(self, col, value):
        isConstraintApplied = True
        # --- Iterate over each row ---
        for row in range(len(self.grid)):
            if self.grid[row][col] == value:
                isConstraintApplied = False

        return isConstraintApplied

    
    def check_cage(self, row, col, value):
        isConstraintApplied =False
        # search with the row and col (cell position in cellToCageMap 2D array to get cage number
        cageNumber = self.cellToCageMap[row][col]
        cageNeededToBeChecked = self.cages.get(cageNumber)
        # get cellsList of the cage
        cellsList = cageNeededToBeChecked['cells']
        # get cage operation
        cageOperation = cageNeededToBeChecked['op']

        # FreeBie
        if cageOperation == "none": # freeBie
            if int(value) == int(cageNeededToBeChecked['value']):
                isConstraintApplied = True

        # ADDITION
        elif cageOperation == "+" : # cellsList > = 2
            summationResult = 0
            zerosCount = 0
            for cell in cellsList: # cell is tuple (1,2)
                if (row,col) != cell: # sum all cells except the one Iam checking
                    zerosCount += (self.grid[cell[0]][cell[1]] == 0)
                    summationResult += int(self.grid[cell[0]][cell[1]])
            if zerosCount and summationResult + int(value) < int(cageNeededToBeChecked['value']):
                isConstraintApplied = True
            elif not zerosCount and summationResult + int(value) == int(cageNeededToBeChecked['value']):
                isConstraintApplied = True

        # SUBTRACTION
        elif cageOperation == "-": # cellsList has only 2 cells according to game Rules
            subtractionResult = 0
            for cell in cellsList:
                if (row,col) != cell :
                    if self.grid[cell[0]][cell[1]] == 0:
                        isConstraintApplied = True
                        break
                    subtractionResult = int(value) - int(self.grid[cell[0]][cell[1]])
            # check if constraint is applied
            if abs(subtractionResult) == cageNeededToBeChecked['value']:
                isConstraintApplied = True

        # MULTIPLICATION
        elif cageOperation == "*": # cellsList > = 2
            multiplicationResult = 1
            zerosCount = 0
            for cell in cellsList:
                if (row,col) != cell:
                    if self.grid[cell[0]][cell[1]] == 0:
                        zerosCount += 1
                    else:
                        multiplicationResult *= self.grid[cell[0]][cell[1]]

            if zerosCount and multiplicationResult * value <= cageNeededToBeChecked['value']:
                isConstraintApplied = True
            elif not zerosCount and multiplicationResult * value == cageNeededToBeChecked['value']:
                isConstraintApplied = True

        # DIVISION
        elif cageOperation == "/": # cellsList = 2
            divisionResult = 1
            for cell in cellsList:
                if (row,col) != cell :
                    if self.grid[cell[0]][cell[1]] == 0:
                        isConstraintApplied = True
                        break
                    elif value > self.grid[cell[0]][cell[1]]:
                        # divide greater/smaller
                        divisionResult = value / self.grid[cell[0]][cell[1]]
                    else:
                        # divide greater/smaller
                        divisionResult = self.grid[cell[0]][cell[1]] / value
            # check if constraint is applied
            if divisionResult == cageNeededToBeChecked['value']:
                isConstraintApplied = True

        return isConstraintApplied
    



    def solve(self):
        if self.backtracking():
            print("Puzzle solved:")
            self.print_solution()
        else:
            print("Puzzle unsolvable.")


    def print_solution(self):
        for row in self.grid:
            print(row)


    def backtracking(self):
        row, col = self.find_empty()
        if row is None:
            return True

        # iterate over all possible values to test them
        for i in range(1, len(self.grid) + 1):
            # check if the current value will obey all constraints
            if self.Bounding(row, col, i):
                self.grid[row][col] = i
                if self.backtracking():
                    return True

        # backtrack the value
        self.grid[row][col] = 0
        return False


    def getKenkenGrid(self):
        return self.grid

    def getKenkenCagesDict(self):
        return self.cages


    def find_empty(self):
        # --- Loop over each cell position and check its value ---
        for row in range(len(self.grid)):
            for col in range(len(self.grid)):
                cellValue = self.grid[row][col]
                if int(cellValue) == 0:
                    return (row,col)
        return (None,None)