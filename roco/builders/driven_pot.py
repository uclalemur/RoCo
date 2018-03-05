from roco.library.pot import Pot
from roco.api.component import Component
from roco.library.pot_driver import PotDriver

if __name__ == "__main__":
    c = Component(name = "DrivenPot")
    c.add_subcomponent("pot", "pot")
    c.add_subcomponent("dPot", "pot_driver")
    c.add_connection(("pot", "vOut"), ("dPot", "vIn"))
    c.inherit_interface("aOut", ("dPot", "aOut"))
    c.inherit_interface("outInt", ("dPot", "outInt"))
    c.make_output()
