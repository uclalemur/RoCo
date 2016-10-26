"""The DrawingEdge module

The Drawing edge module contains the EdgeType class, defining how edges are
treated by output methods, and the DrawingEdge class representing the edges
that make up a Drawing
"""

class EdgeType():
    """Representation of the different modes of Edge instances

    Attributes:
        edgetype (int): An enum representing the edge type
        angle (int): the angle between the faces of the edge
    """

class DrawingEdge():
  """
  A class representing an Edge.
  """

  def __init__(self, name, pt1, pt2, edgetype):
    """
    Initializes an Edge object with pt1 and pt2 in the form ((x1,y1),(x2,y2))

    The Edge can have 5 different types: CUT, FLAT, BEND, FOLD, TAB

    :param pt1: location of point one in the form (x1, y1)
    :type pt1: tuple
    :param pt2: location of point one in the form (x2, y2)
    :type pt2: tuple
    :param mode: 5 different types of Edges: CUT, FLAT, BEND, FOLD, TAB
    :type mode: string
    """

    self.name = name
    self.x1 = pt1[0]
    self.y1 = pt1[1]
    self.x2 = pt2[0]
    self.y2 = pt2[1]
    if edgetype is None:
      edgetype = Cut()
    self.edgetype = edgetype


  def coords(self):
    """
    :returns: a list of the coordinates of the Edge instance endpoints
    :rtype: list of [[x1,y1],[x2,y2]] rounded to the nearest 1e-6
    """

    coords = [[round(self.x1, 6), round(self.y1, 6)], [round(self.x2, 6), round(self.y2, 6)]]
    for i in coords:
      if i[0] == -0.0:
        i[0] = 0.0
      if i[1] == -0.0:
        i[1] = 0.0
    return coords

  def length(self):
    """
    Uses the diag() function

    :returns: the length of the edge
    :rtype: np.float64
    """
    dx = self.x2 - self.x1
    dy = self.y2 - self.y1
    return diag(dx, dy)

  def angle(self, deg=False):
    """
    :param deg: sets the angle return type to be deg or rad
    :type deg: boolean

    :returns: angle of the Edge instance wrt the positive x axis
    :rtype: numpy.float64
    """
    dx = self.x2 - self.x1
    dy = self.y2 - self.y1
    ang = np.arctan2(dy, dx)
    if deg:
      return np.rad2deg(ang)
    else:
      return ang

  def elongate(self, lengths, otherway = False):
    """
    Returns a list of Edge instances that extend out from the endpoint of another Edge instance.
    Mode of all smaller edges is the same as the original Edge instance.

    :param lengths: list of lengths to split the Edge instance into
    :type lengths: list
    :param otherway: boolean specifying where to start from (pt2 if otherway == False, pt1 if otherway == True)
    :type otherway: boolean

    :returns: a list of Edge instances that extend out from the endpoint of another Edge instance
    :rtype: a list of Edge instances
    """

    edges = []
    if otherway:
      lastpt = (self.x1, self.y1)
      for length in lengths:
        e = Edge((0, 0),(-length,0), self.edgetype)
        e.transform(angle=self.angle(), origin=lastpt)
        lastpt = (e.x2, e.y2)
      edges.append(e)
    else:
      lastpt = (self.x2, self.y2)
      for length in lengths:
        e = Edge((0,0), (length, 0), self.edgetype)
        e.transform(angle=self.angle(), origin=lastpt)
        lastpt = (e.x2, e.y2)
      edges.append(e)

    return edges


  def transform(self, scale=1, angle=0, origin=(0,0)):
    """
    Scales, rotates, and translates an Edge instance.

    :param scale: scaling factor
    :type scale: float
    :param angle: angle to rotate in radians
    :type angle: float
    :param origin: origin
    :type origin: tuple
    """

    r = np.array([[np.cos(angle), -np.sin(angle)],
                  [np.sin(angle),  np.cos(angle)]]) * scale

    o = np.array(origin)

    pt1 = np.dot(r, np.array((self.x1, self.y1))) + o
    pt2 = np.dot(r, np.array((self.x2, self.y2))) + o

    self.x1 = pt1[0]
    self.y1 = pt1[1]
    self.x2 = pt2[0]
    self.y2 = pt2[1]

  def invert(self):
    """
    Swaps mountain and valley folds
    """
    self.edgetype.invert()

  def mirrorX(self):
    """
    Changes the coordinates of an Edge instance so that it is symmetric about the Y axis.
    """
    self.x1 = -self.x1
    self.x2 = -self.x2
    self.flip()

  def mirrorY(self):
    """
    Changes the coordinates of an Edge instance so that it is symmetric about the X axis.
    """
    self.y1 = -self.y1
    self.y2 = -self.y2
    self.flip()

  def flip(self):
    """
    Flips the directionality of an Edge instance around
    """
    x = self.x2
    y = self.y2
    self.x2 = self.x1
    self.y2 = self.y1
    self.x1 = x
    self.y1 = y

  def copy(self):
    return Edge(self.name, (self.x1, self.y1), (self.x2, self.y2), self.edgetype)

  def midpt(self):
    """
    :returns: a tuple of the edge midpoint
    :rtype: tuple
    """
    pt1 = self.coords()[0]
    pt2 = self.coords()[1]
    midpt = ((pt2[0]+pt1[0])/2, (pt2[1]+pt1[1])/2)
    return midpt

  def toDrawing(self, drawing, label="", mode=None, engine=None):
    """
    Draws an Edge instance to a CAD file.

    :type drawing:
    :param drawing:
    :type label: tuple
    :param label: location of point two in the form (x2,y2).
    :type mode:
    :param mode:
    """

    if engine is None:
      engine = drawing

    kwargs = self.edgetype.drawArgs(self.name, mode)
    if kwargs:

      dpi = None

      if mode in ( 'Corel', 'print'):
        dpi = 96 # scale from mm to 96dpi for CorelDraw
      elif mode == 'Inkscape':
        dpi = 90 # scale from mm to 90dpi for Inkscape
      elif mode == 'autofold':
        if str(self.edgetype.angle) not in drawing.layers:
          drawing.add_layer(str(self.edgetype.angle))

      if dpi: self.transform(scale=(dpi/25.4))
      drawing.add(engine.line((float(self.x1), float(self.y1)), (float(self.x2), float(self.y2)), **kwargs))
      if dpi: self.transform(scale=(25.4/dpi)) # scale back to mm

    if label:
      r = [int(self.angle(deg=True))]*len(label)
      t = engine.text(label, insert=((self.x1+self.x2)/2, (self.y1+self.y2)/2))# , rotate=r)
      # t.rotate=r
      drawing.add(t)