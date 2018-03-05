from roco.api.component import Component
from roco.library import *
from roco.library import get_component

if __name__ == "__main__":
    c = Component(name = 'GetSerialString')
    c.add_subcomponent('sIn', 'serial_in')
    c.add_subcomponent('s2s', 'serial_to_string')
    c.add_connection(('sIn', 'received'), ('s2s', 'received'))
    c.add_connection(('sIn', 'came'), ('s2s', 'came'))
    c.inherit_interface('out1', ('s2s', 'cameOut'))
    c.inherit_interface('out2', ('s2s', 'receivedString'))
    c.to_yaml("library/getSerialString.yaml")
