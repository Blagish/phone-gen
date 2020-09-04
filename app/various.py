from random import randint, choice


def randomize(count, intervals):  # Randomize phones from multiple intervals
    if not intervals:
        return set()
    res = set()
    for _ in range(count):
        r = choice(intervals)
        phone = str(randint(r[1], r[2]))
        zeros = '0'*(7-len(phone))
        res.update([r[0]+zeros+phone])
    return res


def interval_bin_search(phone, data, regs):
    low = 0
    high = len(regs)

    while low < high:
        mid = (low+high)//2
        if data[regs[mid]][1] <= phone <= data[regs[mid]][2]:  # if found:
            return mid
        if phone < data[regs[mid]][1]:
            high = mid
        elif data[regs[mid]][2] < phone:
            low = mid+1
    return -1