from roco.api.component import Component

if __name__ == "__main__":
    c = Component()
    # import pdb
    # pdb.set_trace()
    c.add_subcomponent("r1", "Square")
    c.add_subcomponent("r2", "Square")
    c.add_subcomponent("r3", "Square")
    c.add_subcomponent("r4", "Square")
    c.add_connection(("r1", "r"),("r2", "l"),angle=90)
    c.add_connection(("r2", "r"),("r3", "l"),angle=90)
    c.add_connection(("r3", "r"),("r4", "l"),angle=90)
    c.add_connection(("r4", "r"),("r1", "l"),angle=90,tab=True)
    c.make_output(thickness=10)


    # def multiplyTwo(c,d):
    #     print("Originally, c is ", c)
    #     print("Originally, d is ", d)
    #     addOne(c)
    #     addOne(d)
    #     print("Now, c is ", c)
    #     print("Now, d is ", d)
    #     return c*d
    #
    # def addOne(x):
    #     return x+1
    #
    # result = multiplyTwo(1,3)
    # print result