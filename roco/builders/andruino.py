from roco.api.component import Component
from roco.library import *

c = Component(name="Andruino")
c.add_subcomponent("srl","serial_in")
c.add_subcomponent("S2S","serial_to_string")
c.add_subcomponent("S2M","string_to_motor")
c.add_connection(("srl","received"),("S2S","received"))
c.add_connection(("srl","came"),("S2S","came"))
c.add_connection(("S2S","receivedString"),("S2M","motorString"))
c.add_connection(("S2S","cameOut"),("S2M","motorCame"))
c.make_output()
