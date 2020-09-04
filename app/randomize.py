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
