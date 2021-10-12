def check(arr, i_num, j_num, n_i, n_j, list_cells):
    arr[i_num][j_num] = 0
    for row in list_cells:
        if row[2] == 1:
            check_cell(arr, row[0], row[1], n_i, n_j)


def check_cell(arr, i, j, n_i, n_j):
    if i == 0 and j == 0:
        print(f'I: {i}, J: {j}, VALUE: {arr[i][j]}')

        check(arr, i, j, n_i, n_j, [
            [i + 1, j + 1, arr[i + 1][j + 1]],
            [i, j + 1, arr[i][j + 1]],
            [i + 1, j, arr[i + 1][j]]])
    elif i == 0 and j != 0 and j != n_j - 1:
        print(f'I: {i}, J: {j}, VALUE: {arr[i][j]}')
        check(arr, i, j, n_i, n_j,
              [
                  [i, j - 1, arr[i][j - 1]],
                  [i, j + 1, arr[i][j + 1]],
                  [i + 1, j - 1, arr[i + 1][j - 1]],
                  [i + 1, j, arr[i + 1][j]],
                  [i + 1, j + 1, arr[i + 1][j + 1]]
              ])
    elif i != 0 and i != n_i - 1 and j == 0:
        print(f'I: {i}, J: {j}, VALUE: {arr[i][j]}')
        print('nya')
        check(arr, i, j, n_i, n_j, [
            [i - 1, j, arr[i - 1][j]],
            [i + 1, j, arr[i + 1][j]],
            [i - 1, j + 1, arr[i - 1][j + 1]],
            [i, j + 1, arr[i][j + 1]],
            [i - 1, j + 1, arr[i - 1][j + 1]]
        ])
    elif i != 0 and i != n_i - 1 and j == 0:
        print(f'I: {i}, J: {j}, VALUE: {arr[i][j]}')
        print('truru')
        check(arr, i, j, n_i, n_j,
              [
                  [i - 1, j, arr[i - 1][j]],
                  [i + 1, j, arr[i + 1][j]],
                  [i - 1, j + 1, arr[i - 1][j + 1]],
                  [i, j + 1, arr[i][j + 1]],
                  [i - 1, j + 1, arr[i - 1][j + 1]]
              ])
    elif i == n_i - 1 and j == n_j - 1:
        print(f'I: {i}, J: {j}, VALUE: {arr[i][j]}')
        check(arr, i, j, n_i, n_j,
              [
                  [i - 1, j, arr[i - 1][j]],
                  [i - 1, j - 1, arr[i - 1][j - 1]],
                  [i, j - 1, arr[i][j - 1]]
              ])
    elif i == n_i - 1 and j != n_j - 1 and j != 0:
        print(f'I: {i}, J: {j}, VALUE: {arr[i][j]}')
        check(arr, i, j, n_i, n_j,
              [
                  [i - 1, j, arr[i - 1][j]],
                  [i - 1, j - 1, arr[i - 1][j - 1]],
                  [i - 1, j + 1, arr[i - 1][j + 1]],
                  [i, j - 1, arr[i][j - 1]],
                  [i, j + 1, arr[i][j + 1]]

              ])
    elif i == n_i - 1 and j == 0:
        print(f'I: {i}, J: {j}, VALUE: {arr[i][j]}')
        print('trata')
        check(arr, i, j, n_i, n_j,
              [
                  [i - 1, j, arr[i - 1][j]],
                  [i - 1, j + 1, arr[i - 1][j + 1]],
                  [i, j + 1, arr[i][j + 1]]

              ])
    elif i != n_i - 1 and i != 0 and j == n_j - 1:
        print(f'I: {i}, J: {j}, VALUE: {arr[i][j]}')
        check(arr, i, j, n_i, n_j,
              [
                  [i - 1, j, arr[i - 1][j]],
                  [i + 1, j, arr[i + 1][j]],
                  [i + 1, j - 1, arr[i + 1][j - 1]],
                  [i, j - 1, arr[i][j - 1]],
                  [i - 1, j - 1, arr[i - 1][j - 1]]
              ])
    elif i == 0 and j == n_j - 1:
        print(f'I: {i}, J: {j}, VALUE: {arr[i][j]}')
        check(arr, i, j, n_i, n_j,
              [

                  [i + 1, j, arr[i + 1][j]],
                  [i + 1, j - 1, arr[i + 1][j - 1]],
                  [i, j - 1, arr[i][j - 1]],
              ])
    else:
        print(f'I: {i}, J: {j}, VALUE: {arr[i][j]}')
        print('tut')
        check(arr, i, j, n_i, n_j,
              [
                  [i, j - 1, arr[i][j - 1]],
                  [i, j + 1, arr[i][j + 1]],
                  [i + 1, j - 1, arr[i + 1][j - 1]],
                  [i + 1, j, arr[i + 1][j]],
                  [i + 1, j + 1, arr[i + 1][j + 1]],
                  [i - 1, j - 1, arr[i - 1][j - 1]],
                  [i - 1, j, arr[i - 1][j]],
                  [i - 1, j + 1, arr[i - 1][j + 1]]
              ])


array = [[1, 0, 1, 0, 1, 0],
         [0, 1, 0, 0, 0, 0],
         [0, 1, 0, 0, 0, 0],
         [0, 0, 1, 0, 0, 0],
         [0, 1, 0, 1, 0, 0],
         ]


n_i = len(array)
n_j = len(array[0])
count = 0
for i in range(len(array)):
    for j in range(len(array[i])):

        if array[i][j] == 1:
            cell = [i, j]
            count += 1
            check_cell(array, i, j, n_i, n_j)

print('Total blocks', count)
