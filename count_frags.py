import process_log as pl

import re
from collections import defaultdict, OrderedDict

if __name__ == '__main__':
    input_file = 'log/sorted_output.log'
    faa_dict = defaultdict(lambda: OrderedDict())

    with open(input_file, 'r') as f:
        lines = f.readlines()

    faa_dict = pl.count_frags(lines[3:], faa_dict)

    for block, pages in faa_dict.items():
        print(f'Block #{block:>3}:')
        for page, dies in pages.items():
            frags = sum(dies.values())
            print(f'\tPage {page} ({int(frags/4)} Planes, {frags} Frags)')
            for die, count in dies.items():
                print(f'\t\tDie {die:>2}: {count} frags')
