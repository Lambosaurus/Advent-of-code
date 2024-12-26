

def load_input(fname = "input.txt"):
    reports = []
    with open(fname, 'r') as f:
        for line in f:
            report = tuple(int(s) for s in line.split(' '))
            reports.append(report)
    return reports

def to_deltas(report):
    for i in range(len(report)-1):
        yield report[i+1] - report[i]

def is_safe(report):
    ascending = None
    for delta in to_deltas(report):
        if delta == 0 or delta < -3 or delta > 3:
            return False
        if ascending != None:
            if (delta > 0) != ascending:
                return False
        else:
            ascending = delta > 0
    return True

def count(sequence):
    return sum(int(s) for s in sequence)

def exclude_index(report, i):
    return report[:i] + report[i+1:]

def damped_is_safe(report):
    if is_safe(report):
        return True
    for i in range(len(report)):
        if is_safe(exclude_index(report, i)):
            return True
    return False
        

if __name__ == "__main__":
    reports = load_input()
    print(f"part1: {count( is_safe(r) for r in reports)} of {len(reports)}")
    print(f"part2: {count( damped_is_safe(r) for r in reports)} of {len(reports)}")
