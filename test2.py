import time
import random


arr = []

start = time.time() # засекает время

for i in range(10000000):
    arr.append(i)

print(len(arr))
print("\n created in %.5f" % (time.time() - start))

start = time.time() # засекает время

arr.remove(500008)


print("\n popped in %.5f" % (time.time() - start))

print(arr[545443])

print(len(arr))