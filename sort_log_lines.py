import process_log as pl

# sort lines by faa
if __name__ == '__main__':
    input_file = 'log/output.log'
    output_file = 'log/sorted_output.log'

    pos = -2
    faa_set = set()

    with open(input_file, 'r') as f:
        lines = f.readlines()

    sorted_lines = sorted(lines[3:], key=lambda line: pl.extract_faa(line, pos=pos))

    with open(output_file, 'w') as f:
        # Write header
        f.write(lines[0])
        f.write("Index       Time                           Information     FAA        (Block, Page, Die, Frag)\n")
        f.write("----------------------------------------------------------------------------------------------\n")

        for line in sorted_lines:
            faa = line.split()[pos]
            faa_tuple = pl.faa_to_tuple(faa)
            block, page, die, frag = faa_tuple

            if faa_tuple in faa_set:
                continue

            faa_set.add(faa_tuple)
            result_line = f'{line.strip()} ({block:>5}, {page:>4}, {die:>3}, {frag:>4})\n'
            f.write(result_line)
