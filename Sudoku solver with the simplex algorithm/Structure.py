#!/usr/bin/env python3

class Structure:
  def __init__(self, grid):
    self.Grid = grid
    self.WaitedAnswer = 405
    self.MaxValue = 0
    self.C = None
    self.B = [45 for _ in range(27)] 
    self.Table = [] 
    self.empty = []

    # getting empty cells, and setting the B vector
    x = 0
    for i in range(9):
      for j in range(9):
        if grid[i][j] == 0:
          self.empty.append((x, i, j)) 
          x += 1
        
        self.WaitedAnswer -= grid[i][j]
        self.B[i]   -= grid[i][j]
        self.B[j+9] -= grid[i][j]

    for i in range(0, 9, 3):
      for j in range(0, 9, 3):
        for a in range(i, i+3):
          for b in range(j, j+3):
            self.B[(a//3)*3 + b//3 + 18] -= grid[a][b]


    # setting the table
    self.Table = [[0 for i in range(len(self.empty))] for _ in range(27)]

    # constraints variables
    for elem in self.empty:
      x, i, j = elem[0], elem[1], elem[2]
      self.Table[i][x] = 1
      self.Table[j+9][x] = 1
      self.Table[(i//3)*3+j//3+18][x] = 1

    self.Table = [[1 for i in range(len(self.empty))]] + self.Table

    # add the constraints <= 9
    constraints = [ [0 for i in range(len(self.empty))] 
                       for j in range(len(self.empty)) ]

    for i in range(len(self.empty)):
      constraints[i][i] = 1

    self.Table += constraints

    # add the constraints >= 1
    _constraints = [ [0 for i in range(len(self.empty))]
                        for j in range(len(self.empty)) ]

    for i in range(len(self.empty)):
      _constraints[i][i] = 1

    self.Table += _constraints

    # adding the identity matrix (some slack vars and artificial vars)
    identity = [ [0 for i in range(28+2*len(self.empty))]
                    for j in range(28+2*len(self.empty)) ]

    for i in range(28+2*len(self.empty)):
      identity[i][i] = 1

    for i in range(len(self.Table)):
      self.Table[i] += identity[i]

    # adding the remaining of slack vars
    remaining = [[0 for i in range(len(self.empty))]
                     for j in range(28+2*len(self.empty))]

    print(len(remaining))
    print(len(remaining[-1]))

    for i in range(28+len(self.empty), len(remaining)):
      remaining[i][i-28-len(self.empty)] = 1

    for i in range(len(self.Table)):
      self.Table[i] += remaining[i]

    # completing B
    self.B = [self.WaitedAnswer] + self.B + [9 for _ in range(len(self.empty))] + [1 for _ in range(len(self.empty))]
    
    # setting C
    self.C = [1 for i in range(len(self.empty))]+[0 for i in range(28+2*len(self.empty))]


  def print_table(self):
    print(end='   ')
    for c in self.C:
      print(f'{c}', end='')
    print(f' {- self.MaxValue}')
    for i in range(len(self.Table)):
      print(f'{str(i).zfill(2)}:', end='')
      for e in self.Table[i]:
        print(e, end='')
      print(end=f' {self.B[i]}\n')

  def solve(self):
    while True:
      indx_max = self.C.index(max(self.C)) 
      if self.C[indx_max] <= 0:
        break

      pivot_indx = -1
      for j in range(len(self.Table)):
        if self.Table[j][indx_max] <= 0:
          continue
        
        if pivot_indx == -1:
          pivot_indx = j
          continue

        if self.B[j]//self.Table[j][indx_max] < self.B[pivot_indx]//self.Table[pivot_indx][indx_max]:
          pivot_indx = j

      if pivot_indx == -1:
        break

      for i in range(len(self.Table[pivot_indx])):
        self.Table[pivot_indx][i] //= self.Table[pivot_indx][indx_max]

      self.B[pivot_indx] //= self.Table[pivot_indx][indx_max]

      self.pivoting(pivot_indx, indx_max)
      

  def pivoting(self, pivot_indx, indx_max):
    for j in range(len(self.Table)):
      if pivot_indx == j:
        continue

      if self.Table[j][indx_max] == 0:
        continue

      P = self.Table[j][indx_max]
      for k in range(len(self.Table[j])):
        self.Table[j][k] -= P * self.Table[pivot_indx][k]

      self.B[j] -= P * self.B[pivot_indx]

    P = self.C[indx_max]
    for k in range(len(self.C)):
      self.C[k] -= P * self.Table[pivot_indx][k]
    
    self.MaxValue -= P * self.B[pivot_indx]
  
  def retrive_solution(self):
    self.print_grid()

    for elem in self.empty:
      x, i, j = elem[0], elem[1], elem[2]
      for _ in range(len(self.Table)):
        if self.Table[_][x] == 1:
          self.Grid[i][j] = self.B[_]
          break

    self.print_grid()

  def print_grid(self):
    print("*"*35)
    for row in self.Grid:
      print(row)
    print("*"*35)

  def check_row(self, i):
    Found = [False for _ in range(10)]
    for j in range(9):
      if Found[self.Grid[i][j]]:
        return False
      Found[self.Grid[i][j]] = True
    return True

  def check_col(self, i):
    Found = [False for _ in range(10)]
    for j in range(9):
      if Found[self.Grid[i][j]]:
        return False
      Found[self.Grid[i][j]] = True
    return True

  def check_box(self, i, j):
    Found = [False for _ in range(10)]
    for x in range(i, i+3):
      for y in range(j, j+3):
        if Found[self.Grid[x][y]]:
          return False
        Found[self.Grid[x][y]] = True
    return True

  def verify_correctness(self):
    for i in range(9):
      for j in range(9):
        if self.Grid[i][j]<1 or 9<self.Grid[i][j]:
          return False

    for i in range(9):
      if not self.check_row(i):
        return False
    
    for i in range(9):
      if not self.check_col(i):
        return False

    for i in range(0, 9, 3):
      for j in range(0, 9, 3):
        if not self.check_box(i, j):
          return False

    return True


  def check_solution(self):
    if self.verify_correctness():
      print("I checked the solution, and it is correct")
    else:
      print("Not a solution")

