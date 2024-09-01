'''
Aahan Madhok and Leo Gurevitch
November, 2023
'''


def is_empty(board):
  for row in board:
    for cell in row:
      if cell != " ":
        return False
  return True

def is_bounded(board, y_end, x_end, length, d_y, d_x):

  on_board = True
  if y_end >= len(board) or x_end >= len(board):
    on_board = False

  if on_board:
    is_empty_one_side = True
    is_empty_other_side = True
    if board[y_end + d_y][x_end + d_x] != " ":
      is_empty_one_side = False
    if board[y_end - length * d_y][x_end - length * d_x] != " ":
      is_empty_other_side = False
    if is_empty_one_side and is_empty_other_side:
      return "OPEN"
    elif is_empty_one_side and not is_empty_other_side:
      return "SEMIOPEN"
    elif not is_empty_one_side and is_empty_other_side:
      return "SEMIOPEN"
    else:
      return "CLOSED"
  return "NOT ON BOARD!"

def detect_row(board, col, y_start, x_start, length, d_y, d_x):
  open_seq_count = 0
  semi_open_seq_count = 0
  seq_count = 0
  while y_start < len(board) and x_start < len(board):
    if board[y_start][x_start] == col:
      seq_count += 1
    if board[y_start][x_start] != col:
      seq_count = 0
    if seq_count == length:
      bounded_left = False
      bounded_right = False
      if x_start + d_x >= len(board) or y_start + d_y >= len(board):
        bounded_left = True
      if x_start + d_x < 0 or y_start + d_y < 0:
        bounded_left = True
      if x_start - length * d_x >= len(board) or y_start - length * d_y >= len(board):
        bounded_right = True
      if x_start - length * d_x < 0 or y_start - length * d_y < 0:
        bounded_right = True
      if not bounded_left and not bounded_right:
        if board[y_start + d_y][x_start + d_x] == " " and board[y_start - length * d_y][x_start - length * d_x] == " ":
          open_seq_count += 1
        elif board[y_start + d_y][x_start + d_x] == " ":
          if board[y_start - length * d_y][x_start - length * d_x] != col:
            semi_open_seq_count += 1
        elif board[y_start - length * d_y][x_start - length * d_x] == " ":
          if board[y_start + d_y][x_start + d_x] != col:
            semi_open_seq_count += 1
      elif bounded_left and not bounded_right:
        if board[y_start - length * d_y][x_start - length * d_x] == " ":
          semi_open_seq_count += 1
      elif not bounded_left and bounded_right:
        if board[y_start + d_y][x_start + d_x] == " ":
          semi_open_seq_count += 1
      if length == 5 and not bounded_left and not bounded_right:
        if board[y_start + d_y][x_start + d_x] != col:
          if board[y_start - length * d_y][x_start - length * d_x] != col:
            open_seq_count += 1 #This accounts for closed win situations.
            #It was arbitrary to add to the semi open or open sequence count
            #based on the is_win(board) function.
      #Now check the other possibilities where length = 5 (for a win):
      elif length == 5 and not bounded_left and bounded_right:
        if board[y_start + d_y][x_start + d_x] != col:
          open_seq_count += 1
      elif length == 5 and bounded_left and not bounded_right:
        if board[y_start - length * d_y][x_start - length * d_x] != col:
          open_seq_count += 1

    if seq_count > length:
      if board[y_start][x_start] != col:
        seq_count = 0 #This accounts for sequences longer than the given length.

    y_start += d_y
    x_start += d_x


  return open_seq_count, semi_open_seq_count


def detect_rows(board, col, length):

  open_seq_count, semi_open_seq_count = 0, 0  #Initialize the function
  opens = 0
  semi_open = 0
  new = 0, 0
  open
  #Start by checking all of the horizontal and vertical rows
  for i in range(len(board)):
    new = detect_row(board, col, i, 0, length, 0, 1)
    opens += new[0]
    semi_open += new[1]
  for i in range(len(board)):
    new = detect_row(board, col, 0, i, length, 1, 0)
    opens += new[0]
    semi_open += new[1]

  #Start checking the diagonals in direction 1, 1
  y_start = 0
  x_start = 0
  #num_squares = len(board)
  for i in range(len(board) - 1):  #We don't need to check the corner
    #since length >= 2
    new = detect_row(board, col, y_start, x_start, length, 1, 1)
    opens += new[0]
    semi_open += new[1]
    #num_squares -= 1
    x_start += 1
  #Do it again to check the other diagonals
  y_start = 1
  x_start = 0
  #num_squares = len(board) - 1
  for i in range(len(board) - 2):  #We can't check the largest diagonal twice.
    #We also don't need to check the corner - length >= 2
    new = detect_row(board, col, y_start, x_start, length, 1, 1)
    opens += new[0]
    semi_open += new[1]
    #num_squares -= 1
    y_start += 1

  #Now check the diagonals in direction 1, -1
  y_start = 0
  x_start = len(board) - 1
  #num_squares = len(board)
  for i in range(len(board) - 1):
    new = detect_row(board, col, y_start, x_start, length, 1, -1)
    opens += new[0]
    semi_open += new[1]
    #num_squares -= 1
    x_start -= 1
  #Do it again for the other diagonals
  y_start = 1
  x_start = len(board) - 1
  #num_squares = len(board) - 1
  for i in range(len(board) - 2):
    new = detect_row(board, col, y_start, x_start, length, 1, -1)
    opens += new[0]
    semi_open += new[1]
    #num_squares -= 1
    y_start += 1

  open_seq_count, semi_open_seq_count = opens, semi_open

  return open_seq_count, semi_open_seq_count

def score(board):
  MAX_SCORE = 100000

  open_b = {}
  semi_open_b = {}
  open_w = {}
  semi_open_w = {}

  for i in range(2, 6):
    open_b[i], semi_open_b[i] = detect_rows(board, "b", i)
    open_w[i], semi_open_w[i] = detect_rows(board, "w", i)

  if open_b[5] >= 1 or semi_open_b[5] >= 1:
    return MAX_SCORE

  elif open_w[5] >= 1 or semi_open_w[5] >= 1:
    return -MAX_SCORE

  return (-10000 * (open_w[4] + semi_open_w[4]) + 500 * open_b[4] +
          50 * semi_open_b[4] + -100 * open_w[3] + -30 * semi_open_w[3] +
          50 * open_b[3] + 10 * semi_open_b[3] + open_b[2] + semi_open_b[2] -
          open_w[2] - semi_open_w[2])

def search_max(board):
  #First, we need to get all of the free squares on the board.
  #We then need to check if making a move there would maximize the score,
  #and if it would, then we need to save the coordinates of the move before setting it
  #back to " " (which we need to do for every time we check a space anyways).

  free_squares = []
  for i in range(len(board)):
    for l in range(len(board[i])):
      if board[i][l] == " ":
        y_coord = i
        x_coord = l
        free_squares.append([y_coord, x_coord])

  move_y = []
  move_x = []
  current_max_score = -1000000

  for e in free_squares:
    board[e[0]][e[1]] = "b"
    if score(board) >= current_max_score:
      current_max_score = score(board)
      move_y = e[0]
      move_x = e[1]
    board[e[0]][e[1]] = " "

  return move_y, move_x

def is_win(board):
  free_squares = []
  for i in range(len(board)):
    for l in range(len(board[i])):
      if board[i][l] == " ":
        y_coord = i
        x_coord = l
        free_squares.append([y_coord, x_coord])
  white_win_test = detect_rows(board, "w", 5)
  black_win_test = detect_rows(board, "b", 5)
  if white_win_test[0] + white_win_test[1] > 0:
    return "White won"
  elif black_win_test[0] + black_win_test[1] > 0:
    return "Black won"
  elif len(free_squares) == 0:
    return "Draw"
  else:
    return "Continue playing"

def print_board(board):

  s = "*"
  for i in range(len(board[0]) - 1):
    s += str(i % 10) + "|"
  s += str((len(board[0]) - 1) % 10)
  s += "*\n"

  for i in range(len(board)):
    s += str(i % 10)
    for j in range(len(board[0]) - 1):
      s += str(board[i][j]) + "|"
    s += str(board[i][len(board[0]) - 1])

    s += "*\n"
  s += (len(board[0]) * 2 + 1) * "*"

  print(s)


def make_empty_board(sz):
  board = []
  for i in range(sz):
    board.append([" "] * sz)
  return board


def analysis(board):
  for c, full_name in [["b", "Black"], ["w", "White"]]:
    print("%s stones" % (full_name))
    for i in range(2, 6):
      open, semi_open = detect_rows(board, c, i)
      print("Open rows of length %d: %d" % (i, open))
      print("Semi-open rows of length %d: %d" % (i, semi_open))


def play_gomoku(board_size):
  board = make_empty_board(board_size)
  board_height = len(board)
  board_width = len(board[0])

  while True:
    print_board(board)
    if is_empty(board):
      move_y = board_height // 2
      move_x = board_width // 2
    else:
      move_y, move_x = search_max(board)

    print("Computer move: (%d, %d)" % (move_y, move_x))
    board[move_y][move_x] = "b"
    print_board(board)
    analysis(board)

    game_res = is_win(board)
    if game_res in ["White won", "Black won", "Draw"]:
      return game_res

    print("Your move:")
    move_y = int(input("y coord: "))
    move_x = int(input("x coord: "))
    board[move_y][move_x] = "w"
    print_board(board)
    analysis(board)

    game_res = is_win(board)
    if game_res in ["White won", "Black won", "Draw"]:
      return game_res


def put_seq_on_board(board, y, x, d_y, d_x, length, col):
  for i in range(length):
    board[y][x] = col
    y += d_y
    x += d_x


def test_is_empty():
  board = make_empty_board(8)
  if is_empty(board):
    print("TEST CASE for is_empty PASSED")
  else:
    print("TEST CASE for is_empty FAILED")


def test_is_bounded():
  board = make_empty_board(8)
  x = 5
  y = 1
  d_x = 0
  d_y = 1
  length = 3
  put_seq_on_board(board, y, x, d_y, d_x, length, "w")
  print_board(board)

  y_end = 3
  x_end = 5

  if is_bounded(board, y_end, x_end, length, d_y, d_x) == 'OPEN':
    print("TEST CASE for is_bounded PASSED")
  else:
    print("TEST CASE for is_bounded FAILED")


def test_detect_row():
  board = make_empty_board(8)
  x = 5
  y = 1
  d_x = 0
  d_y = 1
  length = 3
  put_seq_on_board(board, y, x, d_y, d_x, length, "w")
  print_board(board)
  if detect_row(board, "w", 0, x, length, d_y, d_x) == (1, 0):
    print("TEST CASE for detect_row PASSED")
  else:
    print("TEST CASE for detect_row FAILED")


def test_detect_rows():
  board = make_empty_board(8)
  x = 5
  y = 1
  d_x = 0
  d_y = 1
  length = 3
  col = 'w'
  put_seq_on_board(board, y, x, d_y, d_x, length, "w")
  print_board(board)
  if detect_rows(board, col, length) == (1, 0):
    print("TEST CASE for detect_rows PASSED")
  else:
    print("TEST CASE for detect_rows FAILED")


def test_search_max():
  board = make_empty_board(8)
  x = 5
  y = 0
  d_x = 0
  d_y = 1
  length = 4
  col = 'w'
  put_seq_on_board(board, y, x, d_y, d_x, length, col)
  x = 6
  y = 0
  d_x = 0
  d_y = 1
  length = 4
  col = 'b'
  put_seq_on_board(board, y, x, d_y, d_x, length, col)
  print_board(board)
  if search_max(board) == (4, 6):
    print("TEST CASE for search_max PASSED")
  else:
    print("TEST CASE for search_max FAILED")


def easy_testset_for_main_functions():
  test_is_empty()
  test_is_bounded()
  test_detect_row()
  test_detect_rows()
  test_search_max()


def some_tests():
  board = make_empty_board(8)

  board[0][5] = "w"
  board[0][6] = "b"
  y = 5
  x = 2
  d_x = 0
  d_y = 1
  length = 3
  put_seq_on_board(board, y, x, d_y, d_x, length, "w")
  print_board(board)
  analysis(board)

  # Expected output:
  #       *0|1|2|3|4|5|6|7*
  #       0 | | | | |w|b| *
  #       1 | | | | | | | *
  #       2 | | | | | | | *
  #       3 | | | | | | | *
  #       4 | | | | | | | *
  #       5 | |w| | | | | *
  #       6 | |w| | | | | *
  #       7 | |w| | | | | *
  #       *****************
  #       Black stones:
  #       Open rows of length 2: 0
  #       Semi-open rows of length 2: 0
  #       Open rows of length 3: 0
  #       Semi-open rows of length 3: 0
  #       Open rows of length 4: 0
  #       Semi-open rows of length 4: 0
  #       Open rows of length 5: 0
  #       Semi-open rows of length 5: 0
  #       White stones:
  #       Open rows of length 2: 0
  #       Semi-open rows of length 2: 0
  #       Open rows of length 3: 0
  #       Semi-open rows of length 3: 1
  #       Open rows of length 4: 0
  #       Semi-open rows of length 4: 0
  #       Open rows of length 5: 0
  #       Semi-open rows of length 5: 0

  y = 3
  x = 5
  d_x = -1
  d_y = 1
  length = 2

  put_seq_on_board(board, y, x, d_y, d_x, length, "b")
  print_board(board)
  analysis(board)

  # Expected output:
  #        *0|1|2|3|4|5|6|7*
  #        0 | | | | |w|b| *
  #        1 | | | | | | | *
  #        2 | | | | | | | *
  #        3 | | | | |b| | *
  #        4 | | | |b| | | *
  #        5 | |w| | | | | *
  #        6 | |w| | | | | *
  #        7 | |w| | | | | *
  #        *****************
  #
  #         Black stones:
  #         Open rows of length 2: 1
  #         Semi-open rows of length 2: 0
  #         Open rows of length 3: 0
  #         Semi-open rows of length 3: 0
  #         Open rows of length 4: 0
  #         Semi-open rows of length 4: 0
  #         Open rows of length 5: 0
  #         Semi-open rows of length 5: 0
  #         White stones:
  #         Open rows of length 2: 0
  #         Semi-open rows of length 2: 0
  #         Open rows of length 3: 0
  #         Semi-open rows of length 3: 1
  #         Open rows of length 4: 0
  #         Semi-open rows of length 4: 0
  #         Open rows of length 5: 0
  #         Semi-open rows of length 5: 0
  #

  y = 5
  x = 3
  d_x = -1
  d_y = 1
  length = 1
  put_seq_on_board(board, y, x, d_y, d_x, length, "b")
  print_board(board)
  analysis(board)

  #        Expected output:
  #           *0|1|2|3|4|5|6|7*
  #           0 | | | | |w|b| *
  #           1 | | | | | | | *
  #           2 | | | | | | | *
  #           3 | | | | |b| | *
  #           4 | | | |b| | | *
  #           5 | |w|b| | | | *
  #           6 | |w| | | | | *
  #           7 | |w| | | | | *
  #           *****************
  #
  #
  #        Black stones:
  #        Open rows of length 2: 0
  #        Semi-open rows of length 2: 0
  #        Open rows of length 3: 0
  #        Semi-open rows of length 3: 1
  #        Open rows of length 4: 0
  #        Semi-open rows of length 4: 0
  #        Open rows of length 5: 0
  #        Semi-open rows of length 5: 0
  #        White stones:
  #        Open rows of length 2: 0
  #        Semi-open rows of length 2: 0
  #        Open rows of length 3: 0
  #        Semi-open rows of length 3: 1
  #        Open rows of length 4: 0
  #        Semi-open rows of length 4: 0
  #        Open rows of length 5: 0
  #        Semi-open rows of length 5: 0


if __name__ == '__main__':
  play_gomoku(8)