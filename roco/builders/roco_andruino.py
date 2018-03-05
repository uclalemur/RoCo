from roco.api.component import Component
from roco.library import *
from roco.library import get_component

if __name__ == "__main__":
    c = Component(name = 'Roco_andruino')
    c.add_subcomponent('serial', 'serial_in')
    c.add_subcomponent('s2s', 'serial_to_string')
    c.add_subcomponent('checker', 'string_compare')
    c.add_connection(('serial', 'received'), ('s2s', 'received'))
    c.add_connection(('serial', 'came'), ('s2s', 'came'))
    c.add_connection(('s2s', 'cameOut'), ('checker', 'inDetected'))
    c.add_connection(('s2s', 'receivedString'), ('checker', 'inString'))
    c.make_output()