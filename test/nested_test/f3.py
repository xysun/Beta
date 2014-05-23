from beta import Beta

@Beta(3, 4)
def nested_f1(v):
    return v + 1

@Beta(4, 6)
def nested_f2(v):
    return v + 2
