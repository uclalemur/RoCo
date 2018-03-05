from sympy import Dummy, Symbol

def eval_equation(equation):
    """Evaluates given sympy expression using the parameters.

    Args:
        equation (sympy symbol or expression): A sympy variable or expression to be evaluated

    Returns:
        Evaluated value for expression.
    """
    try:
        eqn_eval = equation
        for s in eqn_eval.atoms(Variable):
            eqn_eval = eqn_eval.subs(s, s.get_value())
        return eqn_eval
    except:
        return equation

class Variable(Dummy):
    def __new__(cls, name, default=-1, commutative=True, **assumptions):
        """Constructs and returns a new Variable object

        Args:
            name (str): the name of the variable to create
            default: the default value to assign to the variable
            commutative (boolean): whether the variable commutes or not
            **assumptions: assumptions that operate on a sympy level

        Returns:
            new instance of a Variable

        """
        instance = Dummy.__new__(cls, name, commutative=commutative, **assumptions)
        instance.default = default
        instance.is_solved = False
        instance.solved = -1
        return instance

    def set_solved(self, value):
        """Sets a new solved value for the variable

        Args:
            value: the new solved value for the variable
        """
        self.solved = value
        self.is_solved = True

    def set_default_value(self, value):
        """Sets a new default value for the variable

        Args:
            value: the new default value for the variable
        """
        self.default = value

    def get_default_value(self):
        """Returns the default value of the variable

        Args:
            None

        Returns:
            The default value of the variable.
        """
        return self.default

    def get_solved(self):
        """Returns the solved value of the variable

        Args:
            None

        Returns:
            The solved value of the variable.

        Raises:
            ValueError: The solved value of the variable has not been set
        """
        return self.solved

    def get_value(self):
        """Returns the current value of the variable. If the variable has been solved, that
            value is returned, otherwise the default is returned

        Args:
            None

        Returns:
            The solved value of the variable.
        """
        if self.is_solved:
            return self.solved
        return self.default

    def set_name(self, name):
        """Returns the name of the variable

        Args:
            name: The name of the variable.
        """
        self.name = name

    def get_name(self):
        """Returns the name of the variable

        Args:
            None

        Returns:
            The name of the variable.
        """
        return self.name

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def __getstate__(self):
      state = Symbol.__getstate__(self)
      state['is_solved'] = self.is_solved
      state['default'] = self.default
      state['solved'] = self.solved
      return state

if __name__ == "__main__":
    pass
