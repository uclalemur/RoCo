from roco.api.component import Component
from roco.library import *
from roco.library import get_component

if __name__ == "__main__":
    c = Component(name = 'Car')
    c.add_subcomponent('DrivenServo0', 'DrivenServo')
    c.add_subcomponent('DrivenServo1', 'DrivenServo1|')
    c.add_subcomponent('DrivenServo2', 'DrivenServo')
    c.add_subcomponent('DrivenServo3', 'DrivenServo')
    c.add_subcomponent('node_mcu0', 'node_mcu')
    c.add_connection(('', 'e_mcu0->do8'), ('DrivenServo0', 'PWMin'))
    c.add_connection(('', 'e_mcu0->do2'), ('DrivenServo1', 'PWMin'))
    c.add_connection(('', 'e_mcu0->do3'), ('DrivenServo2', 'PWMin'))
    c.add_connection(('', 'e_mcu0->do0'), ('DrivenServo3', 'PWMin'))
    c.to_yaml("library/car.yaml")
