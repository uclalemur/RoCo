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
