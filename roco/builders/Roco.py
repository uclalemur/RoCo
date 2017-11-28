from roco.api.component import Component
from roco.library import *
from roco.library import get_component

c = Component(name = 'Roco')
c.add_subcomponent('serial', 'serial_in')
c.add_subcomponent('s2s', 'serial_to_string')
c.add_subcomponent('compare', 'string_compare')
c.add_connection(('serial', 'received'), ('s2s', 'received'))
c.add_connection(('serial', 'came'), ('s2s', 'came'))
c.add_connection(('s2s', 'cameOut'), ('compare', 'inDetected'))
c.add_connection(('s2s', 'receivedString'), ('compare', 'inString'))
c.to_yaml("library/Roco.yaml")
