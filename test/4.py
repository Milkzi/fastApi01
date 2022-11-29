import asyncio
import datetime
import time

a = set()

a.add(1)
a.add(1)
a.add(1)
a.add(1)
a.add(1)


async def func():
    time.sleep(1)
    print(1)
    await asyncio.sleep(1)
    print(2)


# asyncio.run(asyncio.wait([func(),func(),func()]))

a = [1, 2, 3, 4, 5,1]
# for index,item in enumerate(a):
#     if item == 3:
#         assert 4==item,'fsdfsdfs'
#         value = a.pop(index)
#         print(item)
#         print(value)
# print(a)
for value in a.copy():
    print(value)
    if value < 4:
        a.remove(value)

print(a)
