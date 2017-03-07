from sympy import Dummy

def eval_equation(self, equation):
    """Evaluates given sympy expression using the parameters.

    Args:
        equation (sympy symbol or expression): A sympy variable or expression to be evaluated

    Returns:
        Evaluated value for expression.
    """

class Variable(Dummy):
    def set_solved_value(self, value):
        """Sets a new solved value for the variable

        Args:
            value: the new solved value for the variable
        """
    def set_default_value(self, value):
        """Sets a new default value for the variable

        Args:
            value: the new default value for the variable
        """
    def get_default_value(self):
        """Returns the default value of the variable

        Args:
            None

        Returns:
            The default value of the variable.
        """
    def get_solved_value(self):
        """Returns the solved value of the variable

        Args:
            None

        Returns:
            The solved value of the variable.

        Raises:
            ValueError: The solved value of the variable has not been set
        """
    def get_value(self):
        """Returns the current value of the variable. If the variable has been solved, that
            value is returned, otherwise the default is returned

        Args:
            None

        Returns:
            The solved value of the variable.
        """
    def set_name(self, name):
        """Returns the name of the variable

        Args:
            name: The name of the variable.
        """
    def get_name(self):
        """Returns the name of the variable

        Args:
            None

        Returns:
            The name of the variable.
        """