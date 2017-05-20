"""Interface class.

This module contains the Interface class which encapsulates ports from composables and makes them available for conneciton at a component level.

"""

import collections

class Interface(object):
    """A single or an ordered list of ports

    This class represents an interface at the component hierarchy level. Two interfaces of components can be connected. At the composable level, an interface merely encapsulates a port or a collection of ports.

    """

    def __init__(self, name, ports=None):
        """Creates an interface.

        Args:
            name (str): name of the interface
            ports (Port or collection): the ports that make up this interface

        """
        self.name = name
        self.ports = []
        if isinstance(ports, collections.Iterable):
            for port in ports:
                self.ports.append(port)
        else:
            self.ports.append(ports)


    def get_name(self):
        """Returns the name of this interface.

        Args:
            None

        Returns:
            name as a string

        """
        return self.name

    def get_ports(self):
        """Returns the collection of ports that represent this interface.

        Args:
            None

        Returns:
            List containing Port object(s)

        """
        return self.ports
