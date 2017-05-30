from roco.library.pot import Pot
from roco.api.component import Component
# from roco.library.pot_driver import PotDriver
from roco.library.led import LED

c = Component(name = "LEDPot")
c.add_subcomponent("pot", "pot")
c.add_subcomponent("led", "led
c.add_connection(("pot", "vOut"), ("led", "eIn"))
c.make_output()
