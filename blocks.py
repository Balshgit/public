import copy
from random import randint

LIST_HEIGHT = 8
LIST_WIDTH = 7


# List generator for check
def list_generator() -> None:
    test_list = [[randint(0, 1) for _ in range(LIST_WIDTH)] for _ in range(LIST_HEIGHT)]
    print('arr = [\n', end='')
    for row in range(LIST_HEIGHT):
        print(f'{test_list[row]},')
    print(']')

# list_generator()


arr = [
 #   0  1  2  3  4  5  6
    [1, 0, 1, 1, 0, 1, 1, ],  # 0
    [1, 0, 0, 0, 0, 1, 0, ],  # 1
    [1, 1, 1, 0, 1, 0, 0, ],  # 2
    [0, 0, 1, 0, 1, 0, 0, ],  # 3
    [1, 0, 1, 0, 1, 0, 1, ],  # 4
    [1, 0, 1, 0, 1, 0, 1, ],  # 5
 #   0  1  2  3  4  5  6
]


class BlockSearcher:
    def __init__(self, array: list):
        self.array = array
        self.array_copy = copy.deepcopy(array)
        self.width = len(array[1])
        self.height = len(array)
        self.block_number = 0

    def exists(self, row: int, column: int) -> int:
        if self.array[row][column] == 1:
            for row_index in range(-1, 1):
                columns = range(-1, 1) if row_index == 0 else range(-1, 2)
                for column_index in columns:
                    current_row = row + row_index
                    current_column = column + column_index
                    if 0 <= current_row < self.height and 0 <= current_column < self.width:
                        element = self.array_copy[current_row][current_column]
                        if current_row == row and current_column == column:
                            continue
                        if element != 0:
                            return element

    # add number to the element if it exists
    def search(self, row: int, column: int) -> None:
        element = self.exists(row, column)
        if self.array[row][column] == 1 and not element:
            self.block_number += 1
            self.array_copy[row][column] = f'1{self.block_number}'
        elif self.array[row][column] == 1 and element:
            self.array_copy[row][column] = element

    # check each element if it the same as all elements around him
    def morf_to_neighbor_element(self, row: int, column: int) -> None:
        if self.array[row][column] == 1:
            element = self.array_copy[row][column]
            for row_index in range(-1, 2):
                for column_index in range(-1, 2):
                    current_row = row + row_index
                    current_column = column + column_index
                    if 0 <= current_row < self.height and 0 <= current_column < self.width:
                        temp_element = self.array_copy[current_row][current_column]
                        if current_row == row and current_column == column:
                            continue
                        if temp_element != 0 and temp_element != element:
                            self.changer(self.array_copy, element, temp_element)

    # change doubled values
    def changer(self, array: list, element: str, insert: str) -> list:
        for row in range(self.height):
            for column in range(self.width):
                if array[row][column] == element:
                    array[row][column] = insert
        return array

    def analyze(self) -> None:
        # Create new array
        for row in range(self.height):
            for column in range(self.width):
                self.search(row, column)
        # Remove doubles from it
        for row in range(self.height):
            for column in range(self.width):
                self.morf_to_neighbor_element(row, column)

    # count unique items in doubled array
    def blocks_count(self) -> int:
        elements = set()
        for row in range(self.height):
            for elem in self.array_copy[row]:
                elements.add(elem)
        elements.remove(0)
        return len(elements)

    # print both arrays for debug
    def print(self) -> None:
        for row in range(self.height):
            print(self.array[row], self.array_copy[row])


bs = BlockSearcher(arr)
bs.analyze()
# bs.print()  # use for DEBUG
print(f'Total blocks: {bs.blocks_count()}')
