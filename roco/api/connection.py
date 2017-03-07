"""Connection class.

This module contains the Connection class which represents two interfaces in separate components being connected with some arguments.

"""

class Connection(object):
    """A connection between interfaces
    
    This class holds data for a named connection. It also provides enforces rules on making connections between interfaces. For example, two interfaces with different number of ports cannot be connected.

    """

    def __init__(self, from_interface, to_interface, name=None):
        """Creates a connection.

        Args:
            from_interface (Interface): the interface to connect from
            to_interface (Interface): the interface to connect to
        
        """

        if len(from_interface.get_ports()) != len(to_interface.get_ports()):
            raise Exception("Interfaces cannot be connected, number of ports is different")

        if name is None:
            self.name = "{}->{}".format(from_interface.get_name(), to_interface.get_name())
        else:
            self.name = name
        
        self.matched_ports = []
        for i in range(from_interface.get_ports()):
            self.matched_ports.append(from_interface[i], to_interface[i])
        
    def get_name(self):
        """Returns the name of this connection.

        Args:
            None

        Returns:
            name as a string

        """
        return self.name

    def get_port_matchings(self):
        """Returns a list of tuples of ports that have been matched
        
        Args:
            None

        Returns:
            List of ordered pairs of ports

        """
        return self.matched_ports
