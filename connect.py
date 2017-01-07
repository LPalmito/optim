#!/usr/bin/env python3

# école supélec contrale - 2016 - c. dürr
# devoir maison 1 - connect
# www-desir.lip6.fr/~durrc/Iut/optim/t/dm1-connect/

import sys
from random import randint
from Tile import Tile, M
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
    domains = [set(range(4)) for _ in range(n**2)]
    P = CSP(domains)
    # Border constraints
    for k in range(n):
        # Top border
        top = M(0, k, n)
        P.addConstraint(top, top, get_link(top, top, 0, 0))
        # Left border
        left = M(k, 0, n)
        P.addConstraint(left, left, get_link(left, left, 1, 1))
        # Bottom border
        bottom = M(n - 1, k, n)
        P.addConstraint(bottom, bottom, get_link(bottom, bottom, 2, 2))
        # Right border
        right = M(k, n - 1, n)
        P.addConstraint(right, right, get_link(right, right, 3, 3))
    # Inner constraints
    for i in range(n-1):
        for j in range(n-1):
            P.addConstraint(M(i, j, n), M(i+1, j, n), get_link(M(i, j, n), M(i+1, j, n), 2, 0))     # Top-bottom link
            P.addConstraint(M(i, j, n), M(i, j+1, n), get_link(M(i, j, n), M(i, j+1, n), 3, 1))     # Left-right link
    for test in P.solve():
        print(test)


def get_hexa_family(hexa):
    """Take the hexa of a tile and return the hexas of the tile family"""
    hexa_families = [[0], [1, 2, 4, 8], [3, 6, 12, 9], [5, 10], [7, 14, 13, 11], [15]]
    for hexa_family in hexa_families:
        if hexa in hexa_family:
            return hexa_family


def get_link(i, j, i_border, j_border):
    """
    Return a list of possible rotation numbers for tile i and tile j based on constraint i_border-j_border
    For left-right: i_border = 3, j_border = 1
    For top-bottom: i_border = 2, j_border = 0
    For border: i = j, i_border = j_border = 0, 1, 2 or 3
    """
    i_family, j_family = get_hexa_family(i), get_hexa_family(j)
    tuples = set()
    for i_hexa in i_family:
        for j_hexa in j_family:
            i_tile, j_tile = Tile(i_hexa), Tile(j_hexa)
            if i_tile.connectors[i_border] == j_tile.connectors[j_border]:
                tuples.add((i_tile.nb_rots, j_tile.nb_rots))
    return tuples


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
