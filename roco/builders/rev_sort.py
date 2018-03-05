from roco.api.component import Component
from roco.library import *

if __name__ == "__main__":
    c = Component(name="comp")
    c.add_subcomponent("sort", "sort_string")
    c.add_subcomponent("str", "string_source")
    c.add_subcomponent("rev", "reverse_string")
    c.add_connection(("str", "outStr"), ("sort", "inStr"))
    c.add_connection(("sort", "outStr"), ("rev", "inStr"))
    c.inherit_interface("out", ("rev", "outStr"))
    c.make_output()
