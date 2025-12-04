
def load_input(fname = "input.txt"):
    with open(fname, 'r') as f:

        line = f.readline()
        seeds = [int(n) for n in line.split(':')[1].strip().split()]

        transforms = []
        transform = None

        for line in f:
            if "map" in line:
                transform = []
                transforms.append(transform)
            elif transform != None and line.strip():
                transform.append([int(n) for n in line.split()])
            
        return seeds, transforms

def sort_transforms(transforms):
    for transform in transforms:
        # for each transform, sort their ranges by source. This makes them easier to use.
        transform.sort( key=lambda x: x[1] )

def resolve(value, transform):
    for dst, src, length in transform:
        if value >= src and value < (src + length):
            return dst + value - src
    return value # no match

def resolve_all(value, transforms):
    for transform in transforms:
        value = resolve(value, transform)
    return value

def resolve_range(start, count, transforms):

    if len(transforms) == 0:
        return start
    
    transform = transforms[0]
    transforms = transforms[1:]

    starts = []
    
    for dst, src, length in transform:
        src_end = src + length

        if src_end <= start:
            # This range is before us. Skip it.
            continue

        if src > start:
            # This range is ahead of us.
            # Fill the gap

            if start + count < src:
                # We dont even reach this range. Resolve it all.
                starts.append( resolve_range(start, count, transforms) )
                start += count
                count = 0
                break # we are done.
            else:
                # resolve up to the start of the range
                block = src - start
                starts.append( resolve_range(start, block, transforms) )
                start = src
                count -= block

        # We should be within this ranges bounds now.
        # src <= start < src_end
        if start + count < src_end:
            # We dont reach the end of this range. Resolve it all.
            starts.append( resolve_range( dst + start - src, count, transforms ) )
            start += count
            count = 0
            break # We are done.
        else:
            block = src_end - start
            starts.append( resolve_range( dst + start - src, block, transforms ) )
            start += block
            count -= block
            
    if count > 0:
        # Resolve the trailing content
        starts.append( resolve_range(start, count, transforms) )

    return min(starts)

def explode(seeds):
    for i in range(len(seeds) // 2):
        yield seeds[i*2], seeds[i*2 + 1]

if __name__ == "__main__":
    seeds, transforms = list(load_input())
    sort_transforms(transforms)
    print(f"part1: {min( resolve_all(seed, transforms) for seed in seeds )}")
    print(f"part2: {min( resolve_range(start, count, transforms) for start, count in explode(seeds) )}")
