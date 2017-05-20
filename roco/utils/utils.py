import collections
import functools

class memoized(object):
   '''Decorator. Caches a function's return value each time it is called.
   If called later with the same arguments, the cached value is returned
   (not reevaluated).
   '''
   def __init__(self, func):
      self.func = func
      self.cache = {}
   def __call__(self, *args):
      if not isinstance(args, collections.Hashable):
         # uncacheable. a list, for instance.
         # better to not cache than blow up.
         return self.func(*args)
      if args in self.cache:
         return self.cache[args]
      else:
         value = self.func(*args)
         self.cache[args] = value
         return value
   def __repr__(self):
      '''Return the function's docstring.'''
      return self.func.__doc__
   def __get__(self, obj, objtype):
      '''Support instance methods.'''
      return functools.partial(self.__call__, obj)

def prefix(s1, s2):
  """
  Prefixes s2 with s1 with a specific delimiter

  Args:
      s1 (str): prefix
      s2 (str): string to prefix

  Returns:
      prefixed string
  """
  if s1 and s2:
    return s1 + "_" + s2
  return s1 or s2

def to_camel_case(under):
    """
    Converts a string delimitted with underscores to camelcase. Does not work if
    string uses underscores as content as well as as delimeters.

    Args:
        under (str): string with underscores.

    Returns:
        The camelcase version of under.
    """
    ans = ""
    und = True
    for i in range(len(under)):
        if und is True:
            ans += under[i].upper()
            und = False
        elif under[i] is '_':
            und = True
        else:
            ans += under[i]
    return ans

def try_import(module, attribute):
  """
  Attempts to import a module from multiple locations

  Args:
      module (str): name of module
      attribute: attribute to return from module

  Returns:
      an attribute from a module
  """
  try:
    mod = __import__(module, fromlist=[attribute])
    obj = getattr(mod, attribute)
    return obj
  except ImportError:
    try:
      mod = __import__("roco.library." + module, fromlist=[attribute])
      obj = getattr(mod, attribute)
      return obj
    except ImportError:
      try:
         mod = __import__("roco.derived." + module, fromlist=[attribute])
         obj = getattr(mod, attribute)
         return obj
      except ImportError:
         mod = __import__("roco.api." + module, fromlist=[attribute])
         obj = getattr(mod, attribute)
         return obj


def decorate_graph(face, decoration, offset=(0, 0), offset_dx=None, offset_dy=None, rotate=False, mode=None):
  """
  Adds a decoration to a face at the given offset

  Args:
      face (Face): face to decorate
      decoration (Decoration): decoration to add
      offset (tuple): pair of offsets in the x and y axes
      offset_dx: offset in the x axis
      offset_dy: offset in the y axis
      rotate: whether to rotate the decoration or not
      mode: decoration primitive
  """
  try:
    faces = decoration.faces
  except AttributeError:
    faces = [decoration]

  if mode is None:
    mode = "hole"

  if offset_dx is not None and offset_dy is not None:
    offset = (offset_dx, offset_dy)

  for f in faces:
    if rotate:
      face.add_decoration(([(p[1]+offset[0], p[0]+offset[1]) for p in f.pts2d], mode))
    else:
      face.add_decoration(([(p[0]+offset[0], p[1]+offset[1]) for p in f.pts2d], mode))

def scheme_string(expr, prefix=""):
  """
  Converts an expression to a scheme string

  Args:
      expr: sympy expression object
      prefix (str): string to prefix expression with
  """
  if expr.is_Number or expr.is_Symbol or expr.is_NumberSymbol:
    print prefix, repr(expr)
    return
  elif expr.is_Add:
    print prefix, "( +"
  elif expr.is_Mul:
    print prefix, "( *"
  elif expr.is_Pow:
    print prefix, "( ^"
  else:
    print prefix, "(", type(expr)

  for a in expr.args:
    print_prefix(a, "  " + prefix)
  print prefix, ")"

@memoized
def scheme_list(expr):
  """
  Converts an expression to a prefix list

  Args:
      expr: sympy expression object

  Returns:
      a list that represents the expression in prefix notation
  """
  if expr.is_Rational and expr.q != 1:
    return ["/", repr(expr.p), repr(expr.q)]
  elif expr.is_Number or expr.is_Symbol or expr.is_NumberSymbol:
    return repr(expr)
  elif expr.is_Add:
    elist = ["+"]
  elif expr.is_Mul:
    elist = ["*"]
  elif expr.is_Pow:
    elist = ["^"]
  elif expr.is_Equality:
    elist = ["=="]
  elif expr.is_Relational:
    elist = [expr.rel_op]
  else:
    elist = [repr(type(expr))]

  for a in expr.args:
    elist.append(scheme_list(a))

  return elist

def scheme_repr(elist):
  """
  Converts a scheme list to a scheme expression

  Args:
      elist (list): a list that represents an expression in prefix notation

  Returns:
      a string that represents the expression that can be interpreted in scheme
  """
  if isinstance(elist, (list, tuple)):
    string = "( "
    string += " ".join(map(scheme_repr, elist))
    string += " )"
  else:
    string = elist
  return string

def print_summary(component):
  """
  Prints a summary of a component

  Args:
      component (Component): the component to print a summary of
  """
  print "~~~ Parameters:"
  for v in sorted(component.get_variables(), key = lambda x: repr(x)):
    print v#, [(x, v.assumptions0[x]) for x in v.assumptions0 if x not in "real complex hermitian commutative imaginary".split()]
  print

  print "~~~ Equations:"
  for i,c in enumerate(component.get_relations()):
    print scheme_repr(scheme_list(c))
  print
  '''
  for i,c in enumerate(f.getRelations()):
    print i, ":", c
  print
  '''
  print

def print_parameters(component):
  """
  Prints the parameters of a component

  Args:
      component (Component): the component to print the parameters of
  """
  for v in sorted(component.get_variables(), key = lambda x: repr(x)):
    print v

def print_equations(f):
  """
  Prints the relations of a component

  Args:
      component (Component): the component to print the relations of
  """
  for i,c in enumerate(component.get_relations()):
    print c
  print
