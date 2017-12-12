
# def prefix(s1, s2):
#   """
#   Prefixes s2 with s1 with a specific delimiter

#   Args:
#       s1 (str): prefix
#       s2 (str): string to prefix

#   Returns:
#       prefixed string
#   """

#   if s1 and s2:
#     return s1 + "_" + s2
#   return s1 or s2





# a = "hi"
# b = ""
# print(prefix(a,b))



## flush the buffering


# import time
# import sys

# for i in range(5):
#     print i,
#     sys.stdout.flush()
#     time.sleep(1)
class person(object):
  def __init__(self):
      self.name = ''
      self.age = ''

  def get_name(self,name):
      self.name = name

  def get_age(self,age):
      self.age = age

me = 'Wenzhong'
c = person()
c.get_name(me)
c.get_age(27)
print c.age

