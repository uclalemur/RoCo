import pdb
from roco.api.component import Component
#pdb.set_trace()

if __name__ == "__main__":
    c = Component()
    c.add_subcomponent("1st","Rectangle")
    c.make_output()
