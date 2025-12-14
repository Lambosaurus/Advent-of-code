

def load_input(fname = "input.txt"):
    with open(fname, 'r') as f:

        ranges = []
        ids = []
        for line in f.readlines():
            line = line.strip()
            if not line:
                continue
            if '-' in line:
                ranges.append([int(n) for n in line.split('-')])
            else:
                ids.append(int(line))
        
        return ranges, ids

def is_fresh(id, ranges):
    for start, stop in ranges:
        if id >= start and id <= stop:
            return True
    return False

def merge_id_ranges(ranges):
    # sort by start index
    ranges.sort(key = lambda x: x[0])
    ranges = iter(ranges)
    start, stop = next(ranges)
    for next_start, next_stop in ranges:
        if next_start <= stop + 1:
            # merge the active range with the new range
            stop = max(stop, next_stop)
        else:
            # No overlap. Emit the current range then proceed.
            yield start, stop
            start, stop = next_start, next_stop
    yield start, stop

def range_size(range):
    start, stop = range
    return stop + 1 - start

if __name__ == "__main__":
    ranges, ids = load_input()
    print(f"part1: {sum( is_fresh(id, ranges) for id in ids )}")
    print(f"part2: {sum( range_size(r) for r in merge_id_ranges(ranges) )}")
