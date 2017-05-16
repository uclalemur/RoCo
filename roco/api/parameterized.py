"""Parameterized class.

This module contains the Parameterized class which is a base class for
Component.

"""

from utils.variable import Variable
from roco.utils.utils import prefix as prefix_string
from sympy.logic.boolalg import BooleanTrue
from sets import Set

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
        self.constraints = {}

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

    def add_parameter(self, name, value, is_literal=False, **kwargs):
        """Adds a k/v pair to the internal store if the key has not been added
        before

        Args:
            name (str): the parameter name
            value (int): an integer representing the default value for the
                parameter
            is_literal (bool): if True, the parameter's value will
                be stored as is. Else, it will be stored in a variable whose value
                can be changed.
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

        if is_literal:
            self.parameters[name] = value
        else:
            variable = Variable(name, default=value, real=True, **kwargs)
            self.parameters[name] = variable

        return self.get_parameter(name)

    def set_parameter(self, name, value, force_literal=False):
        """Sets either the value of the object associated with the parameter,
        or associated object itself

        Args:
            name (str): the parameter name
            value (int): an integer representing the default value for the
                parameter
            force_literal (bool): if True, object associated with the parameter
            will be replaced by value. Otherwise, the value of the object will
            be attempted to be changed

        Returns:
            The newly modified parameter

        Raises:
            KeyError: A parameter called name does not exist
            ValueError: Old parameter value is a constant and cannot be changed
        """
        if name not in self.parameters:
            raise KeyError("Parameter %s not initialized" % name)

        if force_literal:
            self.parameters[name] = value
        else:
            self.get_parameter(name).set_default_value(value)

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
            if isinstance(variable, Variable):
                variable.set_name(prefix_string(prefix,variable.get_name()))
            self.add_parameter(prefix_string(prefix, name), variable, is_literal=True)  # Is this how we want to do it?

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
        return self.parameters.pop(name)


    def get_constraints(self):
        """Gets all the constraints associated with the parameterized object

        Args:
            None

        Returns:
            A list containing all constraint expressions
        """
        return self.constraints

    def extend_constraints(self, constraints):
        """Extends the list of constraints with the input list

        Args:
            constraints (list/dict): List or dictionary of new constraints to add
        """
        try:
            constraint_eqns = constraints.itervalues()
        except AttributeError:
            constraint_eqns = constraints

        for s in constraint_eqns:
            self.add_constraint(s)

    def add_constraint(self, expression, name=None):
        """Adds a new sympy constraint to the parameterized object

        Args:
            expression(sympy.core.relational): A sympy expression representing a
                relationship between two or more parameters
            name: a unique identifying name for the constraint. If none is
                provided, a unique id will be generated
        Returns:
            The identifying name for the expression

        Raises:
            KeyError: A parameter called name has already been created
        """
        if name is None:
            name = id(expression)

        if name in self.constraints:
            raise KeyError("Constraint %s already exists" % name)

        self.constraints[name] = expression
        return name

    def del_constraint(self,name):
        """Removes the constraint with the given name

        Args:
            name (str): the constraint name

        Returns:
            The removed constraint with the given name

        Raises:
            KeyError: A constraint called name does not exist
        """
        return self.constraints.pop(name)

    def check_constraints(self):
        """Verifies that all constraints are satisfied

        Args:
            None

        Returns:
            True if the constraints are all satisfied, false otherwise
        """
        pass

    def solve(self):
        """Performs the solving that is necessary

        """
        # first create equivalence classes
        equiv_classes = []
        classes_map = {}
        classnum = 0
        for (key, constraint) in self.constraints.iteritems():
          if isinstance(constraint, BooleanTrue):
            continue
          if not isinstance(constraint.lhs, Variable) or not isinstance(constraint.rhs, Variable):
            continue
            #raise Exception("Constraints are not simple parameters.")
          if constraint.lhs in classes_map and constraint.rhs not in classes_map:
            equiv_classes[classes_map[constraint.lhs]].add(constraint.rhs)
            classes_map[constraint.rhs] = classes_map[constraint.lhs]
          elif constraint.lhs not in classes_map and constraint.rhs in classes_map:
            equiv_classes[classes_map[constraint.rhs]].add(constraint.lhs)
            classes_map[constraint.lhs] = classes_map[constraint.rhs]
          elif constraint.lhs not in classes_map and constraint.rhs not in classes_map:
            equiv_classes.append(Set([constraint.lhs, constraint.rhs]))
            classes_map[constraint.lhs] = classes_map[constraint.rhs] = classnum
            classnum += 1
          else:
            equiv_classes[classes_map[constraint.lhs]].update(equiv_classes[classes_map[constraint.rhs]])
            equiv_classes[classes_map[constraint.rhs]] = equiv_classes[classes_map[constraint.lhs]]

        # set values of all variables in a single equivalence class to the default
        # of one of them
        for e_class in equiv_classes:
          fixed = next(iter(e_class))
          for var in e_class:
              var.set_solved(fixed.get_value())
