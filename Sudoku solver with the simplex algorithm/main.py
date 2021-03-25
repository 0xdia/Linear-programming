#!/usr/bin/env python3

from Structure import Structure
from ReadGrid import read_the_grid

if __name__ == '__main__':
  Grid = read_the_grid()

  struct = Structure(Grid)
  struct.solve()
  struct.retrive_solution()
  #struct.check_solution()
  #print(f"waited value == {struct.WaitedAnswer}, max value = {struct.MaxValue}") 
