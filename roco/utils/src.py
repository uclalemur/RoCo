from roco.api.component import Component
from roco.library import *

c = Component(name="comp")
c.add_subcomponent("str", "string_source")
c.add_subcomponent("rev", "reverse_string")
c.add_connection(("str", "outStr"), ("rev", "inStr"))
c.inherit_interface("out", ("rev", "outStr"))
c.make_output()
