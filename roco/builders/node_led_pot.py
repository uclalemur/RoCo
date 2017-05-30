from roco.library.pot import Pot
from roco.api.component import Component
from roco.library.pot_driver import PotDriver
from roco.library.led import LED
from roco.library.node_mcu import NodeMcu

c = Component(name = "LEDPot")
c.add_subcomponent("pot", "pot")
c.add_subcomponent("dPot", "pot_driver")
c.add_subcomponent("nmcu", "node_mcu")
c.add_subcomponent("led", "led")
c.add_connection(("pot", "vOut"), ("dPot", "vIn"))
c.add_connection(("dPot", "aOut"), ("nmcu", "a1"))
c.make_output()
