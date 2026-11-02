def count_up_to_linit(limit):
    n=1
    while n<=limit :
        print(f"Making {n}")
        yield n
        n += 1

def add(a: int, b: int) -> int:
    return a + b



for x in count_up_to_linit(3):
    print(f"got { x }")
    
print(add(2, 3))
print(add("hello ", "world")) 