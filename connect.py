#!/usr/bin/env python3

# école supélec contrale - 2016 - c. dürr
# devoir maison 1 - connect
# www-desir.lip6.fr/~durrc/Iut/optim/t/dm1-connect/

import sys
from random import randint
from Tile import Tile
from CentraleSupelec import CSP
import time
import pprint
import matplotlib.pyplot as plt


def generate(n, with_print=True):
    """Generates a random grid
    """
    # generate random connections, place 0 at the border
    lr = [[randint(0, 1) for j in range(n-1)] + [0] for i in range(n)]
    tb = [[randint(0, 1) for j in range(n)] for i in range(n-1)]
    tb += [[0] * n]
    grid = [[0 for i in range(n)] for j in range(n)]
    for i in range(n):
        for j in range(n):
            # encoding of the cell
            c = tb[i - 1][j] + 2*lr[i][j - 1] + 4*tb[i][j] + 8*lr[i][j]
            cc = c | (c << 4)
            # normalized orientation
            p = min((cc >> i) & 15 for i in range(4))
            if with_print:
                print(hex(p)[-1], end='')
            grid[i][j] = int(p)
        if with_print:
            print()
    return grid


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


def solve(M, with_print=True):
    """
    :param M: the grid to be solved
    :return: solution
    """
    n = len(M)
    L = []
    for t_list in M:
        L.extend(t_list)
    domains = [set(range(4)) for _ in range(n**2)]  # Initialize domain

    # Borders constraints
    for k in range(n):
        domains[0*n+k] = get_border(M[0][k], 0)
        domains[k*n+0] = get_border(M[k][0], 1)
        domains[(n-1)*n+k] = get_border(M[n-1][k], 2)
        domains[k*n+(n-1)] = get_border(M[k][n-1], 3)

    # Angles constraints
    domains[0] = get_border(M[0][0], 0).intersection(get_border(M[0][0], 1))
    domains[n-1] = get_border(M[0][n-1], 0).intersection(get_border(M[0][n-1], 3))
    domains[n**2-n] = get_border(M[n-1][0], 1).intersection(get_border(M[n-1][0], 2))
    domains[n**2-1] = get_border(M[n-1][n-1], 2).intersection(get_border(M[n-1][n-1], 3))

    # Initialize solver
    P = CSP(domains)

    # Top-bottom constraints
    for k in range(n**2-n):
        P.addConstraint(k, k+n, get_link(L[k], L[k+n], 2, 0))
    # Left-right constraints
    for k in range(n**2-1):
        P.addConstraint(k, k+1, get_link(L[k], L[k+1], 3, 1))

    # Building and printing solution (only one solution if not unique)
    l = 0
    M_sol = [[0 for i in range(n)] for j in range(n)]
    if with_print:
        if len(list(P.solve())) == 0:
            print("# Il n'y a pas de solution pour cette grille")
    for sol in P.solve():
        if l != 0:
            if with_print:
                print("# la solution n'est pas unique")
            break
        for k, rot in enumerate(sol):
            M_sol[k//n][k%n] = format(get_hexa_family(L[k])[rot], '01x')
        if with_print:
            for line in M_sol:
                for element in range(len(line)-1):
                    print(line[element], end='')
                print(line[-1])
        l += 1
    if l == 1:
        if with_print:
            print("# la solution est unique")
    return len(list(P.solve())) != 0


def measure_perf(n_max, precision):
    """Measure the performances of the solve method and print a graph from it"""
    durations, averages, minimums, maximums = {}, {}, {}, {}
    for k in range(1, n_max):
        durations[k] = []
        count = 0
        while count < precision:
            grid = generate(k, with_print=False)
            start = time.time()
            hasResult = solve(grid, with_print=False)
            end = time.time()
            if hasResult:
                duration = (end - start) * 1000
                durations[k].append(duration)
                count += 1
        averages[k] = sum(durations[k]) / len(durations[k])
        minimums[k] = min(durations[k])
        maximums[k] = max(durations[k])
    plt.figure(1)
    plt.title('Temps de résolution (en ms) en fonction de n')
    plt.plot(list(range(1, n_max)), list(minimums.values()))
    plt.plot(list(range(1, n_max)), list(averages.values()))
    plt.plot(list(range(1, n_max)), list(maximums.values()))
    plt.show()


def get_hexa_family(hexa):
    """
    Take the hexa of a tile and return the hexas of the tile family
    A Tile family gathers elements with the same number of connections
    """
    hexa_families = [[0], [1, 2, 4, 8], [3, 6, 12, 9], [5, 10], [7, 14, 13, 11], [15]]
    for hexa_family in hexa_families:
        if hexa in hexa_family:
            return hexa_family


def get_link(i, j, i_border, j_border):
    """
    Return a list of possible rotation numbers for tile i and tile j based on constraint i_border-j_border
    For left-right: i_border = 3, j_border = 1
    For top-bottom: i_border = 2, j_border = 0
    """
    i_family, j_family = get_hexa_family(i), get_hexa_family(j)
    tuples = set()
    for i_hexa in i_family:
        for j_hexa in j_family:
            i_tile, j_tile = Tile(i_hexa), Tile(j_hexa)
            if i_tile.connectors[i_border] == j_tile.connectors[j_border]:
                tuples.add((i_tile.nb_rots, j_tile.nb_rots))
    return tuples


def get_border(k, k_border):
    """
    Return a list of possible rotation numbers for tile k on constraint k_border = False
    """
    k_family = get_hexa_family(k)
    border_dom = set()
    for k_hexa in k_family:
        k_tile = Tile(k_hexa)
        if not k_tile.connectors[k_border]:
            border_dom.add(k_tile.nb_rots)
    return border_dom


def help():
    print("Usage: ./connect.py <arguments>")
    print("  -g <n>           to generate a grid of dimension n*n")
    print("  -p               to pretty print a grid given in stdin")
    print("  -s               to solve a grid given in stdin")


if __name__ == '__main__':
    measure_perf(20, 50)
    # if len(sys.argv) == 3 and sys.argv[1] == "-g":
    #     n = int(sys.argv[2])
    #     generate(n)
    # elif len(sys.argv) == 2 and sys.argv[1] == "-p":
    #     prettyprint(read_grid())
    # elif len(sys.argv) == 2 and sys.argv[1] == "-s":
    #     solve(read_grid())
    # else:
    #     help()
