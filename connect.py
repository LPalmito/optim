#!/usr/bin/env python3

# école supélec contrale - 2016 - c. dürr
# devoir maison 1 - connect
# www-desir.lip6.fr/~durrc/Iut/optim/t/dm1-connect/

import sys
from random import randint
from Tile import Tile, get_tile
from CentraleSupelec import CSP
import pprint


def generate(n):
    """Generates a random grid
    """
    # generate random connections, place 0 at the border
    lr = [[randint(0, 1) for j in range(n-1)] + [0] for i in range(n)]
    tb = [[randint(0, 1) for j in range(n)] for i in range(n-1)]
    tb += [[0] * n]
    for i in range(n):
        for j in range(n):
            # encoding of the cell
            c = tb[i - 1][j] + 2*lr[i][j - 1] + 4*tb[i][j] + 8*lr[i][j]
            cc = c | (c << 4)
            # normalized orientation
            p = min((cc >> i) & 15 for i in range(4))
            print(hex(p)[-1], end='')
        print()


def read_line():
    return list(int(x, 16) for x in sys.stdin.readline().strip())


def read_grid():
    """reads a grid from stdin
    """
    grid = [read_line()]
    n = len(grid[0])
    for _ in range(n - 1):
        grid.append(read_line())
    return grid


def prettyprint(grid):
    """ reads a grid from stdin and pretty prints it.
    """
    n = len(grid)
    for i in range(n):
        # top row of cell
        for j in range(n):
            if grid[i][j] & 1:
                print("  |  ", end='')
            else:
                print("     ", end='')
        print()
        # center row of cell
        for j in range(n):
            if grid[i][j] & 2:
                print("--o", end='')
            else:
                print("  o", end='')
            if grid[i][j] & 8:
                print("--", end='')
            else:
                print("  ", end='')
        print()
        # bottom row of cell
        for j in range(n):
            if grid[i][j] & 4:
                print("  |  ", end='')
            else:
                print("     ", end='')
        print()


def solve(grid):
    n = len(grid)
    t_grid = [[Tile(grid[i][j]) for i in range(n)] for j in range(n)]
    t_grid_list = []
    for t_list in t_grid:
        t_grid_list.extend(t_list)
    csp = CSP(t_grid_list)
    # Add the constraints
    border = {(False, False)}
    link = {(True, True), (False, False)}
    # Border constraints
    for k in range(n):
        csp.addConstraint(get_tile(0, k, csp.dom, n).connectors[0], get_tile(0, k, csp.dom, n).connectors[0], border)
        csp.addConstraint(get_tile(k, 0, csp.dom, n).connectors[1], get_tile(k, 0, csp.dom, n).connectors[1], border)
        csp.addConstraint(get_tile(n-1, k, csp.dom, n).connectors[2], get_tile(n-1, k, csp.dom, n).connectors[2], border)
        csp.addConstraint(get_tile(k, n-1, csp.dom, n).connectors[3], get_tile(k, n-1, csp.dom, n).connectors[3], border)
    # Inner constraints
    for i in range(n-1):
        for j in range(n-1):
            csp.addConstraint(get_tile(i, j, csp.dom, n).connectors[3], get_tile(i+1, j, csp.dom, n).connectors[1], link)
            csp.addConstraint(get_tile(i, j, csp.dom, n).connectors[2], get_tile(i, j+1, csp.dom, n).connectors[0], link)
    csp.solve()
    # TODO: Understand how the CSP object works


def help():
    print("Usage: ./connect.py <arguments>")
    print("  -g <n>           to generate a grid of dimension n*n")
    print("  -p               to pretty print a grid given in stdin")
    print("  -s               to solve a grid given in stdin")


if __name__ == '__main__':
    solve(read_grid())
    # if len(sys.argv) == 3 and sys.argv[1] == "-g":
    #     n = int(sys.argv[2])
    #     generate()
    # elif len(sys.argv) == 2 and sys.argv[1] == "-p":
    #     prettyprint(read_grid())
    # elif len(sys.argv) == 2 and sys.argv[1] == "-s":
    #     solve(read_grid())
    # else:
    #     help()
