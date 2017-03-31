class SetPackage:
  use_numpy = False

def use_numpy():
  SetPackage.useNumpy = True
def use_sympy():
  SetPackage.useNumpy = False

def sum(a):
  from operator import add
  return reduce(add, a)

def cumsum(iterable):
  arr = [iterable[0]]
  for c in iterable[1:]:
    arr.append(arr[-1] + c)
  return arr

def difference_exceeds(pts1, pts2, tol):
  return difference(pts1, pts2) > tol

if SetPackage.use_numpy:
  from numpy import dot, array, linalg, transpose, cos, sin, tan, eye, diag, deg2rad, rad2deg, arctan2, arccos, pi, sqrt, round

  from numpy.linalg import norm

  def rows(x):
    return x.shape[0]
  
  def simplify(x):
    return x
  def N(x):
    return x

  def difference(pts1, pts2):
    return norm(array(pts1) - array(pts2))

else:
  from sympy import transpose, cos, sin, tan, eye, pi, sqrt, zeros, N
  from sympy import diag as sdiag
  from sympy import Matrix as array
  from sympy import atan2 as arctan2
  from sympy import acos as arccos
  from sympy import pprint
  from sympy import Symbol as sympySymbol
  from sympy import Dummy as sympyDummy
  from sympy.core.relational import Relational
  from sympy import *

  D = Function('D')

  def deg2rad(x):
    return x * (pi / 180)

  def rad2deg(x):
    return x / (pi / 180)

  def dot(a, b):
    return a * b

  def norm(x):
    return array(x).norm()

  def diag(x):
    return sdiag(*x)

  def rows(x):
    return [x.row(i) for i in range(x.rows)]

  def round(x):
    return x.round()

  def difference(pts1, pts2):
    #XXX Hack to overcome precision errors
    from random import random
    pts1 = array(pts1)
    pts2 = array(pts2)

    syms = pts1.atoms(sympySymbol) | pts2.atoms(sympySymbol)
    subs = [(x, 100 + 100*random()) for x in syms]
    return norm(pts1 - pts2).subs(subs)
    
  array = Matrix
    
  def norm(x):
    if type(x) is tuple:
      x = Matrix(x)
    return x.norm()
        
  def rows(x):
    return x.rows
