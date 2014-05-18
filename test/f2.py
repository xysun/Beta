from beta import Beta

@Beta(3, 5)
def f1(v):
    return v + 1

@Beta(4, 5)
def f2(v):
    return v + 2

if __name__ == '__main__':
    print(f2(6))
