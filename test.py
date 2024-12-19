import time
import random


arr = []

start = time.time() # засекает время

for i in range(10000000):
    arr.append(random.randrange(100))

print(len(arr))
print("\n created in %.5f" % (time.time() - start))

start = time.time() # засекает время


random.shuffle(arr)
arr.pop()


print("\n shuffled in %.5f" % (time.time() - start))

print(len(arr))