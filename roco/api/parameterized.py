"""Parameterized class.

This module contains the Parameterized class which is a base class for
Component.

"""

class Parameterized(object):
    """An object represented by parameters, constraints, and relations.

    Acts as a base class to represent an object with parameters that can
    be constrained and has relations between parameters.

    Attributes:
        parameters (dict): contains parameters by name, can be symbolic
            variables.
        allParameters (dict): contains parameters by symbolic variable.
            Includes ones inherited from other parameterized objects.
            The variable key points to a tuple, (name, value).
        constraints (list): list of sympy relations that define constraints
            on the parameterized object.
        relations (list): list of sympy relations that define soft relations
            between parameters.
        subs (dict): contains tuples from ambiguous symbolic variable to
            specific symbolic variable which includes parameter
            inheritance.

    """
    def __init__(self):
        """Creates a parameterized object.

        Args:
            None
        """
        self._name = None
        self.parameters = {}

    def get_name(self):
        """Returns the name of the parameterized object.

        Args:
            None

        Returns:
            A str representation of the object's name
        """
        return self._name if self._name is not None else str(self.__class__)

    def set_name(self, name):
        """Sets the name of the parameterized object.

        Args:
            name (str): the new object name
        """
        self._name = name

    def add_parameter(self, name, value, is_symbol=True, **kwargs):
        """Adds a k/v pair to the internal store if the key has not been added
            before

        Args:
            name (str): the parameter name
            value (int): an integer representing the default value for the
                parameter
            is_symbol (bool): if True, the parameter's value will be stored as a
                Dummy symbol whose value can be changed. Else, it will be stored
                as is
            **kwargs (dict): kwargs for the creation of the Dummy

        Returns:
            The newly added parameter

        Raises:
            KeyError: A parameter called name has already been created
            ValueError: Invalid characters in name
        """
        if name in self.parameters:
            raise KeyError("Parameter %s already exists" % name)
        if "." in name:
            raise ValueError("Invalid character '.' in parameter name " + name)

        if is_symbol:
            variable = Variable(name, default=value, real=True, **kwargs)
            self.parameters[name] = variable
        else:
            self.parameters[name] = value

        return self.get_parameter(name)

    def set_parameter(self, name, value, force_constant=False):
        """Sets a k/v pair to the internal store if the key has been added previously

        Args:
            name (str): the parameter name
            value (int): an integer representing the default value for the
                parameter
            force_constant (bool): if True, the old value of the parameter will
                be overwritten even if it was not symbolic

        Returns:
            The newly modified parameter

        Raises:
            KeyError: A parameter called name does not exist
            ValueError: Old parameter value is a constant and cannot be changed
        """
        if name not in self.parameters:
            raise KeyError("Parameter %s not initialized" % name)

        self.get_parameter(name).set_solved_value(value)

    def get_parameter(self, name):
        """Retrieves the parameter with the given name

        Args:
            name (str): the parameter name

        Returns:
            The parameter with the given name

        Raises:
            KeyError: A parameter called name does not exist or is uninitialized
        """
        return self.parameters[name]


    def inherit_parameters(self, other, prefix):
        """Adds parameters from another parameterized object to the current object

        Args:
            other (Parameterized): the parameterized object to inherit
                parameters from
            prefix (str): a prefix string to be added to the name of inherited
                parameters
        """
        for name, variable in other.all_parameters():
            self.parameters[prefixString(prefix, name)] = variable  # Is this how we want to do it?

    def all_parameters(self):
        """***SHOULD THIS BE INCLUDED TO AVOID ENCAPSULATION VIOLATION?"""
        for name in self.parameters:
            yield name, self.get_parameter(name)

    def del_parameter(self, name):
        """Removes the parameter with the given name

        Args:
            name (str): the parameter name

        Returns:
            The removed parameter with the given name

        Raises:
            KeyError: A parameter called name does not exist
        """

    def get_variable_sub(self, parameter):
        """Gets the non ambiguous variable for the parameter

        Args:
            parameter (Dummy): the parameter object desired

        Returns:
            The non ambiguous variable for the parameter

        Raises:
            KeyError: The parameter does not exist in the scope of the object
        """

    def get_all_subs(self):
        """Gets the variable substitutions for all the parameters in the object

        Args:
            None

        Returns:
            A dictionary containing all (parameter, value) pairs found
        """

    def get_constraints(self):
        """Gets all the constraints associated with the parameterized object

        Args:
            None

        Returns:
            A list containing all constraint expressions
        """

    def add_constraint(self, expression):
        """Adds a new sympy constraint to the parameterized object

        Args:
            expression(sympy.core.relational): A sympy expression representing a
                relationship between two or more parameters
        """

    def check_constraints(self):
        """Verifies that all constraints are satisfied

        Args:
            None

        Returns:
            True if the constraints are all satisfied, false otherwise
        """

    def solve(self):
        """Performs the solving that is necessary

        """
