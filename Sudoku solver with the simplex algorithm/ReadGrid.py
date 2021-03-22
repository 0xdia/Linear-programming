#!/usr/bin/env python3

def read_the_grid():
  # Assuming Grid.txt file exists in the same directory
  lines = open("Grid.txt").read().strip().split('\n')
  grid = [line.split(' ') for line in lines] 

  assert(len(grid) == 9)
  for i in range(9):
    assert(len(grid[i]) == 9)
    for j in range(9):
      grid[i][j] = int(grid[i][j])

  return grid

