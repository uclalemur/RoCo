from roco.api.component import Component
from roco.library import *
from roco.library import get_component

c = Component(name = 'Roco_andruino')
c.add_subcomponent('serial', 'serial_in')
c.add_subcomponent('s2s', 'serial_to_string')
c.add_subcomponent('s2m', 'string_to_motor')
c.add_connection(('serial', 'received'), ('s2s', 'received'))
c.add_connection(('serial', 'came'), ('s2s', 'came'))
c.add_connection(('s2s', 'cameOut'), ('s2m', 'motorCame'))
c.add_connection(('s2s', 'receivedString'), ('s2m', 'motorString'))
c.to_yaml("library/roco_andruino.yaml")
