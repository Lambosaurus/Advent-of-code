
def load_input(fname = "input.txt"):
    with open(fname, 'r') as f:
        return f.read()

def expand_diskmap(diskmap):
    disk = []
    id = 0
    empty = False
    for ch in diskmap:
        length = int(ch)
        if empty:
            disk.append( (None, length) )
        else:
            disk.append( (id, length) )
            id += 1
        empty = not empty
    return disk

def insert_segment(disk, index, id, length):
    for i in range(index, len(disk)):
        free_id, free_length = disk[i]
        if free_id != None:
            continue
        
        if free_length > length:
            # shrink the free section, and put our data before it.
            disk[i] = (None, free_length - length)
            disk.insert(i, (id, length))
            return i + 1
        
        # copy our id, coopting this section.
        disk[i] = (id, free_length)
        length -= free_length

        if length <= 0:
            return i + 1

    # we ran out of segments to fill
    disk.append( (id, length) )
    return i + 2

def compress_disk(disk):
    free_index = 0
    while free_index < len(disk):
        id, length = disk.pop()
        if id != None:
            free_index = insert_segment(disk, free_index, id, length)
    return disk

def compress_disk_contigous(disk):
    i = len(disk) - 1
    while i > 0:

        id, length = disk[i]
        if id != None:
            for j in range(i):
                free_id, free_length = disk[j]
                if free_id == None and length <= free_length:
                    disk[j] = (id, length)
                    if free_length > length:
                        # Patch in an empty segment
                        disk.insert(j+1, (None, free_length - length))
                        i += 1
                    disk[i] = (None, length)
                    break
        i -= 1
    return disk

def checksum_disk(disk):
    total = 0
    index = 0
    for id, length in disk:
        if id != None:
            total += sum(index + i for i in range(length)) * id
        index += length
    return total

def print_disk(disk):
    line = ""
    for id, length in disk:
        id_ch = f"{id:1X}" if id != None else '.'
        line += id_ch * length
    print(line)
    
if __name__ == "__main__":
    diskmap = load_input()
    print( f"part1: {checksum_disk(compress_disk(expand_diskmap(diskmap)))}" )
    print( f"part2: {checksum_disk(compress_disk_contigous(expand_diskmap(diskmap)))}" )