from roco.api.composable import Composable
from roco.derived.ports.electrical_port import ElectricalPort
from copy import copy, deepcopy
import pdb

class ElectricalComposable(Composable):

    def new(self):
        """Returns a new instance of a ElectricalComposable, identical to this one.

        Args:
            None

        Returns:
            Electrical Composable object.

        """
        cc = deepcopy(self)
        return cc

    def __init__(self, name, physical, is_virtual=False):
        """Initializes a Electrical Composable.

        Args:
            name (string):  of Electrical component attached to this composable
            physical (dict): dictionary containing physical properties of Electrical component
                including power, aliases, and connections
            is_virtual (Boolean): Whether or not the component is virtual

        """
        self.physical = dict()
        self.physical[name] = dict()
        self.physical[name]["power"] = physical["power"]
        self.physical[name]["aliases"] = physical["aliases"]
        self.physical[name]["connections"] = [list() for i in range(physical["numPins"])]
        self.physical[name]["virtual"] = is_virtual

    def resolve_virtuals(self):
        for (c_name, c_val) in self.physical.iteritems():
           if not c_val["virtual"]:
               continue
           for i in range(len(c_val["connections"])):
               cc = c_val["connections"][i]
               if len(cc) > 1:
                   self.physical[cc[0][0]]["connections"][cc[0][1]] = cc[1]
                   self.physical[cc[1][0]]["connections"][cc[1][1]] = cc[0]
               elif len(cc) > 0:
                   self.physical[c_name]["connections"][i] = cc[0]



    def attach(self, from_port, to_port, **kwargs):
        """Attaches two ports inside the composable together

        Args:
            from_port (Port):
            to_port(Port):
            kwargs (dict): args relating to the connection between the ports.

        """
        if not isinstance(from_port, ElectricalPort) or not isinstance(to_port, ElectricalPort):
            return

        from_name = from_port.get_component_name()
        from_pins = from_port.get_pins()
        to_name = to_port.get_component_name()
        to_pins = to_port.get_pins()

        if len(from_pins) != len(to_pins):
            raise Exception("Number of pins on ports do not match!")

        f_virtual = self.physical[from_name]["virtual"]
        t_virtual = self.physical[to_name]["virtual"]

        for fpin, tpin in zip(from_pins, to_pins):
            if f_virtual:
                self.physical[from_name]["connections"][fpin].append([to_name, tpin, False])
            else:
                self.physical[from_name]["connections"][fpin] = [to_name, tpin, False]
            if t_virtual:
                self.physical[to_name]["connections"][tpin].append([from_name, fpin, False])
            else:
                self.physical[to_name]["connections"][tpin] = [from_name, fpin, False]

    def append(self, new_composable, new_prefix):
        """Combines two composables with the new one being prefixed.

        Args:
            new_composable (Composable): the composable that is being appended to this one.
            new_prefix (str): the prefix of all the names for the composable being appended.

        """
        self.physical.update(new_composable.physical)

    def make_output(self, file_dir, **kwargs):
        """Creates wiring instructions for the composable.

        Args:
            file_dir (str): the directory to place to output
            kwargs (dict): arguments for the output generation

        """
        filename = "%s/wiring_instructions.txt" % file_dir
        f = open(filename, "w")

        f.write("Wiring Instructions:\n")
        self.resolve_virtuals()

        new_physical = deepcopy(self.physical)

        for (name, val) in new_physical.iteritems():
            if "Component." in name:
                name = name.replace("Component.", "")

            if val["virtual"]:
                continue
            for f_pin, connect in list(enumerate(val["connections"])):
                f_pin_name = val["aliases"][f_pin]
                if connect:
                    if connect[2]:
                        continue

                    t_name = connect[0]
                    t_pin = connect[1]
                    t_pin_name = new_physical[t_name]["aliases"][t_pin]
                    # pdb.set_trace()
                    new_physical[t_name]["connections"][t_pin][2] = True

                    if "Component." in t_name:
                        t_name = t_name.replace("Component.", "")

                    f.write("Connect %s on %s to %s on %s\n" % (f_pin_name, name, t_pin_name, t_name))
                elif f_pin in val["power"]["Vin"]:
                    f.write("Connect %s on %s to Vout\n" % (f_pin_name, name))
                elif f_pin in val["power"]["Ground"]:
                    f.write("Connect %s on %s to ground\n" % (f_pin_name, name))
