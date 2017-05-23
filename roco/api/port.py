"""Port class.

This module contains the Port class.

"""

from roco.api.parameterized import Parameterized

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
        super(Port, self).__init__()

        self.is_input = False
        self.is_output = False
        self.value_function = False

        self.parent = parent
        self._allowable_mates = []
        self._recommended_mates = []

    def update(self):
        """Function to be overridden to handle updates

        Args:
            None
        """
        pass

    def prefix(self, prefix=""):
        """Function to be overridden to handle prefixing

        Args:
            prefix (str): name of the prefix
        """
        pass

    def set_input_value(self, value):
        """Set input value that the port will take.

        Args:
            value (function): anonymous function that handles inputs
        """
        self.is_input = True
        self.is_output = False
        self.value_function = lambda : value

    def set_output_value(self, value):
        """Set output value that the port will take.

        Args:
            value (function): anonymous function that handles outputs
        """
        self.is_input = False
        self.is_output = True
        self.value_function = fn

    def set_driven_value(self, value):
        """Set driven value that the port will take.

        Args:
            value (function): anonymous function that handles driven inputs? //CHECK
        """
        self.is_input = False
        self.is_output = False
        self.value_function = fn

    def get_value(self, default=None):
        """Get anonymous function associated with this port.

        Args:
            default: value to return if there is no anonymous function associated with this variable.
        """
        if self.value_function is None:
            return default
        return self.value_function()

    def can_mate(self, other_port):
        """Returns true if this port can mate with other_port and false otherwise.
        Override this method for better matching.

        Args:
            other_port (Port): the port that is compared to this port to check compatibility.

        Returns:
            Boolean denoting whether or not the ports are compatible.
        """
        if len(self._allowable_mates) > 0:
            for next_type in self._allowable_mates:
                if isinstance(other_port, next_type):
                    return True
            return False
        return self.__class__ == other_port.__class__

    def should_mate(self, other_port):
        """Returns true if this port is designed to mate with other_port and false otherwise.
        Override this method for better matching.

        Args:
            other_port (Port): the port that is compared to this port to check compatibility.

        Returns:
            Boolean denoting whether or not the ports are recommended to match.
        """
        if not self.can_mate(other_port):
            return False
        if len(self._recommended_mates) > 0:
            for next_type in self._recommended_mates:
                if isinstance(other_port, next_type):
                    return True
        return False

    def add_allowable_mate(self, mate_type):
        """Adds mate_type to list of ports that are allowed to mate with this port

        Args:
            mate_type (type): the type of port to be added to the list of ports allowed to mate with this port.
        """
        if not isinstance(mate_type, (list, tuple)):
            mate_type = [mate_type]
        for new_type in mate_type:
            if not isinstance(new_type, type(self.__class__)):
                continue
            for mate in self._allowable_mates:
                if issubclass(mate, new_type):
                    return
            for mate in self._allowable_mates:
                if issubclass(new_type, mate):
                    self._allowable_mates.remove(mate)
            self._allowable_mates.append(new_type)

    def add_recommended_mate(self, mate_type):
        """Adds mate_type to list of ports that are recommended to mate with this port

        Args:
            mate_type (type): the type of port to be added to the list of ports recommended to mate with this port.
        """
        if not isinstance(mate_type, (list, tuple)):
            mate_type = [mate_type]
        for new_type in mate_type:
            if not isinstance(new_type, type(self.__class__)):
                continue
            for mate in self._recommended_mates:
                if issubclass(mate, new_type):
                    return None
            for mate in self._recommende_mates:
                if issubclass(new_type, mate):
                    self._recommended_mates.remove(mate)
            self._recommended_mates.append(new_type)

    def set_parent(self, new_parent):
        """Sets this port's parent to be new_parent

        Args:
            new_parent (component): the parent component of this port.
        """
        self.parent = new_parent


    def get_parent(self):
        """Gets this port's parent component

        Args:
            None
        """
        return self.parent


    def to_string(self):
        """Returns string representation of this port. Override for customized implementation.

        Args:
            None

        Returns:
            String that contains information about this port.
        """
        return str(self.parent) + '.' + self.get_name()


    def get_compatible_ports(self):
        """Returns array of all ports that can match with this one.

        Args:
            None

        Returns:
            Array of all ports that can match with this one.
        """
        return self._allowable_mates

    def constrain(self, parent, to_port, **kwargs):
        """Return a set of semantic constraints to be satisfied when connecting to to_port object.
        By default, constrain same-named parameters to be equal. Override this method for better matching.

        Args:
            parent (component): parent of to_port //CHECK
            to_port (port): port that is to be connected to this port.

        Returns:
            list of semantic constraints
        """
        constraints = []
        for p in self.parameters:
            if p in to_port.parameters:
                if "offset_" + p in kwargs:
                    constraints.append(Eq(self.get_parameter(p)+kwargs["offset_" + p], to_port.get_parameter(p)))
                else:
                    constraints.append(Eq(self.get_parameter(p), to_port.get_parameter(p)))
