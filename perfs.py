import time
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from connect import *


def measure_perf(n_max, precision):
    """Measure the performances of the solve method and print a graph from it"""
    dur_no_AC, min_no_AC, avg_no_AC, max_no_AC = {}, {}, {}, {}
    dur_with_AC, min_with_AC, avg_with_AC, max_with_AC = {}, {}, {}, {}
    perfs = {}
    for maintain_AC in {False, True}:
        for k in range(1, n_max):
            if not maintain_AC:
                dur_no_AC[k] = []
            else:
                dur_with_AC[k] = []
            count = 0
            while count < precision:
                grid = generate(k, with_print=False)
                start = time.time()
                hasResult = solve(grid, with_print=False, maintain_AC=maintain_AC)
                end = time.time()
                if hasResult:
                    duration = (end - start) * 1000
                    if not maintain_AC:
                        dur_no_AC[k].append(duration)
                    else:
                        dur_with_AC[k].append(duration)
                    count += 1
            if not maintain_AC:
                min_no_AC[k] = min(dur_no_AC[k])
                avg_no_AC[k] = sum(dur_no_AC[k]) / len(dur_no_AC[k])
                max_no_AC[k] = max(dur_no_AC[k])
            else:
                min_with_AC[k] = min(dur_with_AC[k])
                avg_with_AC[k] = sum(dur_with_AC[k]) / len(dur_with_AC[k])
                max_with_AC[k] = max(dur_with_AC[k])
    perfs['min_no_AC'] = list(min_no_AC.values())
    perfs['avg_no_AC'] = list(avg_no_AC.values())
    perfs['max_no_AC'] = list(max_no_AC.values())
    perfs['min_with_AC'] = list(min_with_AC.values())
    perfs['avg_with_AC'] = list(avg_with_AC.values())
    perfs['max_with_AC'] = list(max_with_AC.values())
    print_perfs(n_max, perfs)


def print_perfs(n_max, perfs):
    # Create patches for the legend
    min = mpatches.Patch(color='blue', label='Minimum')
    avg = mpatches.Patch(color='green', label='Moyenne')
    max = mpatches.Patch(color='red', label='Maximum')
    no_AC = mpatches.Patch(color='blue', label='Sans arc consistance')
    with_AC = mpatches.Patch(color='green', label='Avec arc consistance')
    # Plot graphs
    plt.figure(1)
    plt.subplot(211)
    plt.title('Temps de résolution (en ms) en fonction de n sans arc consistance')
    plt.plot(list(range(1, n_max)), perfs['min_no_AC'])
    plt.plot(list(range(1, n_max)), perfs['avg_no_AC'])
    plt.plot(list(range(1, n_max)), perfs['max_no_AC'])
    plt.legend(handles=[min, avg, max])
    plt.subplot(212)
    plt.title('Temps de résolution (en ms) en fonction de n avec arc consistance')
    plt.plot(list(range(1, n_max)), perfs['min_with_AC'])
    plt.plot(list(range(1, n_max)), perfs['avg_with_AC'])
    plt.plot(list(range(1, n_max)), perfs['max_with_AC'])
    plt.legend(handles=[min, avg, max])
    plt.figure(2)
    plt.title('Comparaison des temps de résolution moyens(en ms) avec et sans arc consistance')
    plt.plot(list(range(1, n_max)), perfs['avg_no_AC'])
    plt.plot(list(range(1, n_max)), perfs['avg_with_AC'])
    plt.legend(handles=[no_AC, with_AC])
    plt.show()

if __name__ == '__main__':
    measure_perf(20, 50)
