"""Port class.

This module contains the Port class.

"""

from parameterized import Parameterized

class Port(Parameterized):
    """A class representing an abstract port
    
    Attributes:
        is_input (bool): whether the port takes input or not.
        is_output (bool): whether the port gives output or not.
        parent (Component): parent component that this port is tied to.

    """
    def __init__(self, parent, params, name='', **kwargs):
        """Creates a port object.
        
        Args: 
            parent (component): The component to which this port will be added.
            params (dict): a set of parameters for the port.
            name (str): name of the port
            kwargs (dict): additional arguments to override params
        """

    def update(self):
        """Function to be overridden to handle updates

        Args:
            None
        """

    def prefix(self, prefix=""):
        """Function to be overridden to handle prefixing

        Args:
            prefix (str): name of the prefix
        """

    def set_input_value(self, value):
        """Set input value that the port will take.

        Args:
            value (function): anonymous function that handles inputs
        """

    def set_output_value(self, value):
        """Set output value that the port will take.

        Args:
            value (function): anonymous function that handles outputs
        """

    def set_driven_value(self, value):
        """Set driven value that the port will take.

        Args:
            value (function): anonymous function that handles driven inputs? //CHECK
        """

    def get_value(self, default=None):
        """Get anonymous function associated with this port.

        Args:
            default: value to return if there is no anonymous function associated with this variable.
        """

    def can_mate(self, other_port):
        """Returns true if this port can mate with other_port and false otherwise.
        Override this method for better matching.
        
        Args:
            other_port (Port): the port that is compared to this port to check compatibility.

        Returns:
            Boolean denoting whether or not the ports are compatible.
        """

    def should_mate(self, other_port):
        """Returns true if this port is designed to mate with other_port and false otherwise.
        Override this method for better matching.
        
        Args:
            other_port (Port): the port that is compared to this port to check compatibility.

        Returns:
            Boolean denoting whether or not the ports are recommended to match.
        """

    def add_allowable_mate(self, mate_type):
        """Adds mate_type to list of ports that are allowed to mate with this port

        Args:
            mate_type (type): the type of port to be added to the list of ports allowed to mate with this port.
        """

    def add_recommended_mate(self, mate_type):
        """Adds mate_type to list of ports that are recommended to mate with this port

        Args:
            mate_type (type): the type of port to be added to the list of ports recommended to mate with this port.
        """

    def set_parent(self, new_parent):
        """Sets this port's parent to be new_parent

        Args:
            new_parent (component): the parent component of this port.
        """

        
    def get_parent(self):
        """Gets this port's parent component

        Args:
            None
        """


    def set_name(self, name):
        """Sets this port's name to be name

        Args:
            name (str): the name of this port.
        """


    def get_name(self):
        """Gets this port's name

        Args:
            None
        """


    def to_string(self):
        """Returns string representation of this port. Override for customized implementation.

        Args:
            None
        
        Returns:
            String that contains information about this port.
        """


    def get_compatible_ports(self):
        """Returns array of all ports that can match with this one.

        Args:
            None

        Returns:
            Array of all ports that can match with this one.
        """

    def constrain(self, parent, to_port, **kwargs):
        """Return a set of semantic constraints to be satisfied when connecting to to_port object.
        By default, constrain same-named parameters to be equal. Override this method for better matching.

        Args:
            parent (component): parent of to_port //CHECK
            to_port (port): port that is to be connected to this port.
        
        Returns:
            list of semantic constraints 
        """
