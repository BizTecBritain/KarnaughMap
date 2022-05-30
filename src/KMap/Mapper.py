"""Create Karnaugh Map objects which can be solved and manipulated.
Supported characters:
    Any case is supported
    or equivalents: |, ||, +, v
    and equivalents: &, &&, *, ^
    not equivalents: !, ~, ¬

Classes:

    KarnaughMap

Functions:

    KarnaughMapObject.create_map(tot_input=None, expression=None) -> (bool) success
    KarnaughMapObject.print(object, file) -> (None)
    KarnaughMapObject.to_string(object, file) -> (str) reader-friendly table
    KarnaughMap.get_tot_variables(expression: str) -> (Union[int, None]) total number of variables
    KarnaughMapObject.solve_map(self: object) -> (str) simplified binary logic representation of map

Misc variables:

    __all__
    __author__
    __version__
    supported_from
"""

__all__ = ["KarnaughMap"]
__author__ = "Alexander Bisland"
__version__ = "2.5.1"
supported_from = "3.8.1"

import re
import itertools
from typing import Union, TypeVar, List

_KMap = TypeVar("_KMap", bound="KarnaughMap")


class KarnaughMap:  # TODO - map middle for 5+6
    #                      - add CLI
    #                      - add if __name__=="__main__":
    """Create Karnaugh Map objects which can be solved and manipulated.
    Supported characters:
        Any case is supported
        or equivalents: |, ||, +, v
        and equivalents: &, &&, *, ^
        not equivalents: !, ~, ¬

    Functions:

        KarnaughMapObject.create_map(tot_input=None, expression=None) -> (bool) success
        KarnaughMapObject.print(object, file) -> (None)
        KarnaughMapObject.to_string(object, file) -> (str) reader-friendly table
        KarnaughMap.get_tot_variables(expression: str) -> (Union[int, None]) total number of variables
        KarnaughMapObject.solve_map(self: object) -> (str) simplified binary logic representation of map

    GLOBAL static variables:

        SINGLE  - headings for one variable
        DOUBLE  - headings for two variables
        TRIPLE  - headings for three variables
        VALUES  - pairings for a whole table (index=number of variable)
        LETTERS - letters than can be used

    Class variables:

        self.tot_input = None     - total number of variables in the expression (used for table dimensions)
        self.expression = None    - unsimplified expression
        self.valid_symbols = None - list of valid symbols that can be used
        self.debug = debug        - debug mode (enables some prints)
        self.table = []           - the table (can also get access through __repr__)
        self.result = ""          - the simplified expression
        self.raise_error = True   - whether to raise errors or just print them

    Other data:

        Order of operations: BNAO
        Only tested up to 4 variables
    """
    SINGLE = ['0', '1']  # headings for one variable
    DOUBLE = ['00', '01', '11', '10']  # headings for two variables
    TRIPLE = ['000', '001', '011', '010', '110', '111', '101', '100']  # headings for three variables
    VALUES = [(["0"], ["0"]), (["0"], ["0"]), (SINGLE, SINGLE), (DOUBLE, SINGLE), (DOUBLE, DOUBLE), (TRIPLE, DOUBLE),
              (TRIPLE, TRIPLE)]  # pairings for a whole table (index=number of variable)
    LETTERS = ['a', 'b', 'c', 'd', 'e', 'f']  # letters than can be used

    def __init__(self: _KMap, tot_input: int = None, expression: str = None, debug: bool = False,
                 raise_error: bool = True) -> None:
        """Constructor for the class

            Parameters:
                self (_KMap):       The instantiated object
                tot_input (int):    The total number of variables in the expression  in the expression
                                      (used for table dimensions)
                expression (int):   An unsimplified expression to map
                debug (bool):       Whether debug mode is on or not (enables some prints)
                raise_error (bool): Whether to raise an error or just print the error

            Returns:
                Nothing (None): Null
        """
        self.tot_input = tot_input
        self.expression = expression
        self.valid_symbols = None
        self.debug = debug
        self.table = []
        self.result = ""
        self.raise_error = raise_error
        self.groups = []

    def reset(self: _KMap) -> None:
        """Reset all attributes to their defaults (should be used before class is reused)

            Parameters:
                self (_KMap):       The instantiated object

            Returns:
                Nothing (None): Null
        """
        self.tot_input = None
        self.expression = None
        self.valid_symbols = None
        self.debug = False
        self.table = []
        self.result = ""
        self.raise_error = True
        self.groups = []

    def create_map(self: _KMap, tot_input: int = None, expression: str = None) -> bool:
        """Create the actual Karnaugh Map (stored in self.table)

            Parameters:
                self (_KMap):    The instantiated object
                tot_input (int):  The total number of variables in the expression
                expression (int): An unsimplified expression to map

            Returns:
                success (bool): whether the program succeeded
        """
        self.tot_input = self.tot_input if tot_input is None else tot_input
        self.expression = self.expression if expression is None else expression
        if self.__get_valid_expression():
            tableDim = KarnaughMap.VALUES[self.tot_input]
            self.table = [[0 for _ in range(len(tableDim[0]))] for _ in range(len(tableDim[1]))]
            arrayPos = 0
            for heading in itertools.product(tableDim[0], tableDim[1]):
                expression = self.expression[:]
                for index, letter in enumerate(KarnaughMap.LETTERS[:self.tot_input]):
                    expression = expression.replace(letter, str(heading[0] + heading[1])[index])
                self.table[arrayPos % len(tableDim[1])][arrayPos // len(tableDim[1])] = int(
                    KarnaughMap._evaluate_expression(KarnaughMap.__remove_brackets(expression)))
                arrayPos += 1
            return True
        return False

    def print(self: _KMap) -> None:
        """Function to print the table in a user-friendly way

            Parameters:
                self (_KMap): The instantiated object

            Returns:
                Nothing (None): Null
        """
        print(self.__str__())

    def to_string(self: _KMap) -> str:
        """Function to return the table in a user-friendly way

            Parameters:
                self (_KMap): The instantiated object

            Returns:
                table (str): The table as a string in a user-friendly way
                  "  ab  00  01  11  10
                   cd
                   00  [  1,  1,  1,  1],
                   01  [  1,  0,  0,  1],
                   11  [  1,  0,  0,  1],
                   10  [  1,  1,  1,  1]"
        """
        return self.__str__()

    def __str__(self: _KMap) -> str:
        """Function to return the table in a user-friendly way

            Parameters:
                self (_KMap): The instantiated object

            Returns:
                table (str): The table as a string in a user-friendly way e.g.
                  "  ab  00  01  11  10
                   cd
                   00  [  1,  1,  1,  1],
                   01  [  1,  0,  0,  1],
                   11  [  1,  0,  0,  1],
                   10  [  1,  1,  1,  1]"
        """
        tableDimValues = KarnaughMap.VALUES[self.tot_input]
        output = (" " * len(tableDimValues[1][0])) + "".join(KarnaughMap.LETTERS[:len(tableDimValues[0][0])]) + \
                 (" " * (4 - len(tableDimValues[0][0]))) + \
                 (" " * (4 - len(tableDimValues[0][0]))).join(tableDimValues[0]) + "\n"
        output += "".join(KarnaughMap.LETTERS[len(tableDimValues[0][0]):
                                              len(tableDimValues[0][0]) + len(tableDimValues[1][0])]) + "\n"
        for index, row in enumerate(self.table):
            output += tableDimValues[1][index] + " " * len(tableDimValues[0][0]) + "[  " + \
                      ",  ".join([str(cell) for cell in row]) + "],\n"
        return output[:-1]

    def __repr__(self: _KMap) -> List[List[int]]:
        """Function that defines the representation of the class

            Parameters:
                self (_KMap): The instantiated object

            Returns:
                self.table (List[List[str]]): The Karnaugh map stored in the class
        """
        return self.table

    @staticmethod
    def _evaluate_expression(equation: Union[str, List]) -> str:
        """Function to take a multi-dimensional list (seperated by brackets) and solve it

            Parameters:
                equation (Union[str, List]): multi-dimensional list

            Returns:
                solution (str): The solution (bool True/False) as an integer string ("1"/"0")
        """
        for index, element in enumerate(equation):
            if isinstance(element, list):  # if the element is a list then recursively perform this function \
                equation[index] = KarnaughMap._evaluate_expression(element)  # until you have the innermost list
        return KarnaughMap.__solve_simple("".join(equation))

    @staticmethod
    def __solve_simple(equation: str) -> str:
        """Private function to simplify a simple boolean expression (no brackets)

            Parameters:
                equation (str): A simple boolean expression (no brackets)

            Returns:
                solution (str): The solution (bool True/False) as an integer string ("1"/"0")
        """
        equation = list(equation)
        while '¬' in equation:  # find all nots and replace with the solution
            pos = equation.index('¬')
            equation = equation[:pos] + equation[pos + 1:]
            equation[pos] = str(int(not int(equation[pos])))
        while '^' in equation:  # find all ands and replace with the solution
            pos = equation.index('^')
            equation[pos + 1] = str(int(int(equation[pos - 1]) and int(equation[pos + 1])))
            equation = equation[:pos - 1] + equation[pos + 1:]
        while 'v' in equation:  # find all ors and replace with the solution
            pos = equation.index('v')
            equation[pos + 1] = str(int(int(equation[pos - 1]) or int(equation[pos + 1])))
            equation = equation[:pos - 1] + equation[pos + 1:]
        return "".join(equation)  # should be only one character

    def __get_valid_expression(self: _KMap) -> bool:
        """Private function to get an expression, check if it is valid and simplify format (e.g. remove spaces)

            Parameters:
                self (_KMap):    The instantiated object

            Returns:
                valid (bool): whether the expression is valid
        """
        try:  # attempt to get a valid number for the total number of variables
            if self.tot_input is None:  # if not predefined (passed in)
                if self.expression is not None:  # first try to calculate automatically
                    self.tot_input = KarnaughMap.get_tot_variables(self.expression)
                if self.tot_input is None:  # otherwise ask for user input
                    self.tot_input = int(input("How many variables (max 4)? "))
            if self.tot_input not in [2, 3, 4, 5, 6]:  # start the checks for validity
                if self.tot_input < 2:
                    if self.raise_error:
                        raise ValueError("Num of inputs must be greater than or equal to 2: " + str(self.tot_input))
                    elif self.debug:
                        print("Num of inputs must be greater than or equal to 2: " + str(self.tot_input))
                    self.tot_input = None
                elif self.tot_input > 6:
                    if self.raise_error:
                        raise ValueError("Num of inputs must be less than or equal to 6: " + str(self.tot_input))
                    elif self.debug:
                        print("Num of inputs must be less than or equal to 6: " + str(self.tot_input))
                    self.tot_input = None
                return False
        except ValueError:
            if self.raise_error:
                raise ValueError("Num of inputs must be a number")
            elif self.debug:
                print("Num of inputs must be a number")
            self.tot_input = None
            return False
        self.valid_symbols = ['v', '^', '¬', '(', ')'] + KarnaughMap.LETTERS[:self.tot_input]
        if self.expression is None:  # if expression isn't defined ask for user input
            self.expression = input(
                "Type your expression (using " + ",".join(KarnaughMap.LETTERS[:self.tot_input]) + "): ")
        self.expression = self.expression.lower()  # start reformatting of expression to only contain letters and ^v¬
        self.expression = self.expression.replace('|', 'v')
        self.expression = self.expression.replace('&', '^')
        self.expression = self.expression.replace('||', 'v')
        self.expression = self.expression.replace('&&', '^')
        self.expression = self.expression.replace('!', '¬')
        self.expression = self.expression.replace('+', 'v')
        self.expression = self.expression.replace('*', '^')
        self.expression = self.expression.replace('~', '¬')
        self.expression = self.expression.replace('or', 'v')
        self.expression = self.expression.replace('and', '^')
        self.expression = self.expression.replace('not', '¬')
        self.expression = self.expression.replace(' ', '')
        self.expression = self.expression.replace('¬¬', '')
        if len(self.expression) == 0:  # start the checks for validity
            if self.raise_error:
                raise ValueError("Please input an expression")
            elif self.debug:
                print("Please input an expression")
            self.expression = None
            return False
        if all(symbol in ['v', '^', '¬', '(', ')'] + KarnaughMap.LETTERS for symbol in self.expression):
            if not all(symbol in self.valid_symbols for symbol in self.expression):
                if self.raise_error:
                    raise ValueError("Some invalid letters were used, please change the total number of inputs")
                elif self.debug:
                    print("Some invalid letters were used, please change the total number of inputs")
                return False
        else:
            if self.raise_error:
                raise ValueError("Expression contains invalid symbols")
            elif self.debug:
                print("Expression contains invalid symbols")
            self.expression = None
            return False
        if self.expression.count('(') != self.expression.count(')'):
            if self.raise_error:
                raise ValueError("Number of brackets does\'t match")
            elif self.debug:
                print("Number of brackets does\'t match")
            self.expression = None
            return False
        if self.debug:
            print(self.expression)
        return True

    @staticmethod
    def __remove_brackets(text: str) -> List:
        """A private static function to convert a string with brackets into a nested list
        (e.g. "(AvB)^C)" -> [["AvB"],"^C"]

            Parameters:
                text (str):    The string to remove brackets from

            Returns:
                stack (List): A nested list showing where all the brackets are
        """
        tokens = re.split(r'([(]|[)]|,)', text)
        stack = [[]]
        for token in tokens:
            if not token or re.match(r',', token):
                continue
            if re.match(r'[(]', token):
                stack[-1].append([])
                stack.append(stack[-1][-1])
            elif re.match(r'[)]', token):
                stack.pop()
                if not stack:
                    raise ValueError('Error: opening bracket is missing, this shouldn\'t happen')
            else:
                stack[-1].append(token)
        if len(stack) > 1:
            print(stack)
            raise ValueError('Error: closing bracket is missing, this shouldn\'t happen')
        return stack.pop()

    @staticmethod
    def get_tot_variables(expression: str) -> Union[int, None]:
        """Function to calculate the total number of variables used (not recommended)

            Parameters:
                expression (str): An expression to use to calculate the total variables

            Returns:
                variables (Union[int, None]): The total number of variables used
        """
        variables = 5
        try:
            while not KarnaughMap.LETTERS[variables] in expression.lower():
                variables -= 1
            return variables + 1
        except IndexError:
            return None

    def solve_map(self: _KMap) -> str:
        """Function to solve a generated Karnaugh map

            Parameters:
                self (_KMap):    The instantiated object

            Returns:
                self.result (str): The simplified form of the original equation
        """
        self.result = ""
        self.groups = []
        tableDim = [len(self.table[0]), len(self.table)]
        headings = KarnaughMap.VALUES[self.tot_input]
        temp_table = [[self.table[y][x] for x in range(len(self.table[0]))] for y in range(len(self.table))]
        """First check if the entire table is one or zero"""
        if all(cell == 0 for row in self.table for cell in row):
            self.result = "(0)"
            return self.result
        if all(cell == 1 for row in self.table for cell in row):
            self.result = "(1)"
            return self.result
        """This section works by iterating through each cell in the table and creating all the allowed 
        group sizes and then calculating the largest one.
        Variables to note:
          - largest = size of largest group
          - xStart  = starting column
          - yStart  = starting row
          - point   = ending point (x and y)
          - xwrap   = if it wraps around to the first column
          - ywrap   = if it wraps around to the first row
        """
        for yStart in range(tableDim[1]):
            for xStart in range(tableDim[0]):
                if temp_table[yStart][xStart] != 0:
                    largest = 1
                    point = [xStart, yStart]
                    xwrap = False
                    ywrap = False
                    for ySize in [1, 2, 4, 8][:[1, 2, 4, 8].index(tableDim[1]) + 1]:
                        for xSize in [1, 2, 4, 8][:[1, 2, 4, 8].index(tableDim[0]) + 1]:
                            found = 1
                            contain_one = temp_table[yStart][xStart] == 1
                            for yPosition in range(yStart, yStart + ySize):
                                for xPosition in range(xStart, xStart + xSize):
                                    if temp_table[yPosition % tableDim[1]][xPosition % tableDim[0]] == 0:
                                        found = 0
                                    if temp_table[yPosition % tableDim[1]][xPosition % tableDim[0]] == 1:
                                        contain_one = True
                            if ySize * xSize > largest and found == 1 and contain_one:
                                largest = ySize * xSize
                                point = [(xStart + xSize - 1) % tableDim[0], (yStart + ySize - 1) % tableDim[1]]
                                if xStart + xSize - 1 != point[0]:
                                    xwrap = True
                                else:
                                    xwrap = False
                                if yStart + ySize - 1 != point[1]:
                                    ywrap = True
                                else:
                                    ywrap = False
                            found = 1
                            contain_one = temp_table[yStart][xStart] == 1
                            for yPosition in range(yStart, yStart - ySize, -1):
                                for xPosition in range(xStart, xStart - xSize, -1):
                                    if temp_table[yPosition % tableDim[1]][xPosition % tableDim[0]] == 0:
                                        found = 0
                                    if temp_table[yPosition % tableDim[1]][xPosition % tableDim[0]] == 1:
                                        contain_one = True
                            if ySize * xSize > largest and found == 1 and contain_one:
                                largest = ySize * xSize
                                point = [(xStart - xSize + 1) % tableDim[0], (yStart - ySize + 1) % tableDim[1]]
                                if xStart - xSize + 1 != point[0]:
                                    xwrap = True
                                else:
                                    xwrap = False
                                if yStart - ySize + 1 != point[1]:
                                    ywrap = True
                                else:
                                    ywrap = False
                            found = 1
                            contain_one = temp_table[yStart][xStart] == 1
                            for yPosition in range(yStart, yStart + ySize):
                                for xPosition in range(xStart, xStart - xSize, -1):
                                    if temp_table[yPosition % tableDim[1]][xPosition % tableDim[0]] == 0:
                                        found = 0
                                    if temp_table[yPosition % tableDim[1]][xPosition % tableDim[0]] == 1:
                                        contain_one = True
                            if ySize * xSize > largest and found == 1 and contain_one:
                                largest = ySize * xSize
                                point = [(xStart - xSize + 1) % tableDim[0], (yStart + ySize - 1) % tableDim[1]]
                                if xStart - xSize + 1 != point[0]:
                                    xwrap = True
                                else:
                                    xwrap = False
                                if yStart + ySize - 1 != point[1]:
                                    ywrap = True
                                else:
                                    ywrap = False
                            found = 1
                            contain_one = temp_table[yStart][xStart] == 1
                            for yPosition in range(yStart, yStart - ySize, -1):
                                for xPosition in range(xStart, xStart + xSize):
                                    if temp_table[yPosition % tableDim[1]][xPosition % tableDim[0]] == 0:
                                        found = 0
                                    if temp_table[yPosition % tableDim[1]][xPosition % tableDim[0]] == 1:
                                        contain_one = True
                            if ySize * xSize > largest and found == 1 and contain_one:
                                largest = ySize * xSize
                                point = [(xStart + xSize - 1) % tableDim[0], (yStart - ySize + 1) % tableDim[1]]
                                if xStart + xSize - 1 != point[0]:
                                    xwrap = True
                                else:
                                    xwrap = False
                                if yStart - ySize + 1 != point[1]:
                                    ywrap = True
                                else:
                                    ywrap = False
                    """This section works by calculating the minimum and the maximum of the points and then filling
                    the tables with 2s to show that these are already included in a group
                    Variables to note:
                      - changed_vals = list of all coordinates of cells that have been changed
                    """
                    if not (largest == 1 and temp_table[yStart][xStart] == 2):
                        (xmin, xmax) = (xStart, point[0] + 1) if xStart < point[0] else (point[0], xStart + 1)
                        (ymin, ymax) = (yStart, point[1] + 1) if yStart < point[1] else (point[1], yStart + 1)
                        changed_vals = []
                        if ywrap and not xwrap:  # wrap around y
                            for yPosition in range(0, ymin + 1):
                                for xPosition in range(xmin, xmax):
                                    temp_table[yPosition][xPosition] = 2
                                    changed_vals.append([xPosition, yPosition])
                            for yPosition in range(ymax - 1, tableDim[1]):
                                for xPosition in range(xmin, xmax):
                                    temp_table[yPosition][xPosition] = 2
                                    changed_vals.append([xPosition, yPosition])
                        elif xwrap and not ywrap:  # wrap around x
                            for yPosition in range(ymin, ymax):
                                for xPosition in range(0, xmin + 1):
                                    temp_table[yPosition][xPosition] = 2
                                    changed_vals.append([xPosition, yPosition])
                            for yPosition in range(ymin, ymax):
                                for xPosition in range(xmax - 1, tableDim[0]):
                                    temp_table[yPosition][xPosition] = 2
                                    changed_vals.append([xPosition, yPosition])
                        elif not xwrap and not ywrap:  # no wrap around
                            for yPosition in range(ymin, ymax):
                                for xPosition in range(xmin, xmax):
                                    temp_table[yPosition][xPosition] = 2
                                    changed_vals.append([xPosition, yPosition])
                        else:  # wrap around y and x
                            for yPosition in range(0, ymin + 1):
                                for xPosition in range(0, xmin + 1):
                                    temp_table[yPosition][xPosition] = 2
                                    changed_vals.append([xPosition, yPosition])
                            for yPosition in range(0, ymin + 1):
                                for xPosition in range(xmax - 1, tableDim[0]):
                                    temp_table[yPosition][xPosition] = 2
                                    changed_vals.append([xPosition, yPosition])
                            for yPosition in range(ymax - 1, tableDim[1]):
                                for xPosition in range(0, xmin + 1):
                                    temp_table[yPosition][xPosition] = 2
                                    changed_vals.append([xPosition, yPosition])
                            for yPosition in range(ymax - 1, tableDim[1]):
                                for xPosition in range(xmax - 1, tableDim[0]):
                                    temp_table[yPosition][xPosition] = 2
                                    changed_vals.append([xPosition, yPosition])
                        """This section takes the changed_vals and modifies an array to show what the values have in 
                        common, if all of the values have 1 heading in common then it will have a score of the size of 
                        the group and if if all of them dont have it in common (not variable) then it will have a score 
                        of zero
                        Variables to note:
                          - self.result = the result as a string
                        """
                        changed = [0 for _ in range(self.tot_input)]
                        self.groups.append(changed_vals)
                        for i in changed_vals:
                            for index, j in enumerate(headings[0][i[0]]):
                                changed[index] += int(j)
                            for index, j in enumerate(headings[1][i[1]]):
                                changed[index + len(headings[0][0])] += int(j)
                        if len(self.result) != 0:
                            self.result += "v"
                        self.result += "(" + "^".join(
                            [KarnaughMap.LETTERS[i].upper() for i, x in enumerate(changed) if x == len(changed_vals)] +
                            ["¬" + KarnaughMap.LETTERS[i].upper() for i, x in enumerate(changed) if x == 0]) + ")"
        if all(cell == 0 for row in self.table for cell in row):
            self.result = "(0)"
        if all(cell == 1 for row in self.table for cell in row):
            self.result = "(1)"
        return self.result
