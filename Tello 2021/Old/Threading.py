from threading import Thread


def func1():
    for i in range(1,10):
        print(i)

def func2():
    for j in range(9,0,-1):
        print(j)

t1 = Thread(target=func1)
t2 = Thread(target=func2)

t1.start()
t2.start()

t1.join()
t2.join()

print("Done")