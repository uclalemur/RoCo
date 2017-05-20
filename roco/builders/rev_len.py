from roco.api.component import Component
from roco.library import *

c = Component()
c.add_subcomponent("sort", "sort_string")
c.add_subcomponent("str", "string_source")
c.add_connection(("str", "outStr"), ("sort", "inStr"))
c.inherit_interface("out", ("sort", "outStr"))
print c.connections
c.make_output()
c.to_yaml("sort_hello")
