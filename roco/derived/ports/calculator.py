def func(x):
    return x*x

def integral(start, finish):
    x = start
    sum = 0
    dx = (finish-start)/1000
    for i in range((finish-start)*1000):
        sum += func(x+dx)*dx
        x = x+dx

integral(-1, 1)
