import process_log as pl

if __name__ == '__main__':
    input_file = 'log/input.log'
    output_file = 'log/output.log'

    with open(input_file, 'r') as f:
        lines = f.readlines()

    filtered_lines = pl.filter_line_by_diff(lines[2:], 0)

    with open(output_file, 'w') as f:
        # Write header
        f.write(lines[0])
        f.write("Index       Time                           Information     FAA       \n")
        f.write("---------------------------------------------------------------------\n")
        for line in filtered_lines:
            f.write(line.lstrip())
