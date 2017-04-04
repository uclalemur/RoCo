from roco.api.composable import Composable
from roco.derived.ports.electrical_port import ElectricalPort
from copy import copy, deepcopy

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
            name (string): Name of Electrical component attached to this composable
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

    def resolveVirtuals(self):
        return
        #for (cName, cVal) in self.physical.iteritems():
        #    if not cVal["virtual"]:
        #        continue
        #    for cc in cVal["connections"]:
        #        if cc:
        #            self.physical[cc[0][0]]["connections"][cc[0][1]] = cc[1]
        #            self.physical[cc[1][0]]["connections"][cc[1][1]] = cc[0]


    def attach(self, from_port, to_port, kwargs):
        """Attaches two ports inside the composable together

        Args:
            from_port (Port):
            to_port(Port):
            kwargs (dict): args relating to the connection between the ports.

        """
        if not isinstance(from_port, ElectricalPort) or not isinstance(to_port, ElectricalPort):
            return

        from_name = from_port.getComponentName()
        from_pins = from_port.getPins()
        to_name = to_port.getComponentName()
        to_pins = to_port.getPins()

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

    def makeOutput(self, file_dir, **kwargs):
        """Creates wiring instructions for the composable.

        Args:
            file_dir (str): the directory to place to output
            kwargs (dict): arguments for the output generation

        """
        filename = "%s/wiring_instructions.txt" % file_dir
        f = open(filename, "w")

        f.write("Wiring Instructions:\n")
        #self.resolveVirtuals()

        #newPhysical = deepcopy(self.physical)
        """
        for (name, val) in newPhysical.iteritems():
            if "Component." in name:
                name = name.replace("Component.", "")

            if val["virtual"]:
                continue
            for fPin, connect in list(enumerate(val["connections"])):
                fPinName = val["aliases"][fPin]
                if connect:
                    if connect[2]:
                        continue

                    tName = connect[0]
                    tPin = connect[1]
                    tPinName = newPhysical[tName]["aliases"][tPin]
                    newPhysical[tName]["connections"][tPin][2] = True

                    if "Component." in tName:
                        tName = tName.replace("Component.", "")

                    f.write("Connect %s on %s to %s on %s\n" % (fPinName, name, tPinName, tName))
                elif fPin in val["power"]["Vin"]:
                    f.write("Connect %s on %s to Vout\n" % (fPinName, name))
                elif fPin in val["power"]["Ground"]:
                    f.write("Connect %s on %s to ground\n" % (fPinName, name))
        """
