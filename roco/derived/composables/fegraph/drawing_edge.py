
import roco.utils.mymath as np
"""The DrawingEdge module

The Drawing edge module contains the EdgeType class, defining how edges are
treated by output methods, and the DrawingEdge class representing the edges
that make up a Drawing
"""

class EdgeType(object):
    """Representation of the different modes of Edge instances

    Attributes:
        edge_type (int): An enum representing the edge type
        angle (int): the angle between the faces of the edge
    """
    #Enum for the various edge types
    (   REG,
        CUT,
        FOLD,
        FLEX,
        FLAT,
        TAB,
        NOEDGE,
    ) = range(7)

    def __init__(self, edge_type, angle=0):
        """Creates a new EdgeType instance

        Args:
            edge_type (int): One of the seven enum edge types
            angle (float): The angle between the two faces associated with the
                edge
        """
        self.edge_type = edge_type
        self.angle = angle

    def __repr__(self):
        """Returns the string representation of the EdgeType

        Args:
            None
        """

        rep = ( "REG",
                "CUT",
                "FOLD",
                "FLEX",
                "FLAT",
                "TAB",
                "NOEDGE",
                "TAB",
              )[self.edge_type]
        if self.angle: #If the angle is not the default 0
          rep += " (%d)" % self.angle
        return rep

    def invert(self):
        """Inverts the edge angle

        Args:
            None
        """
        self.angle = -self.angle

    @classmethod
    def make_linetypes(cls, drawing, dxf):
        """Adds a fold line type to a drawing

        Args:
            cls (class): The implicity recieve class argument
            drawing: The drawing to add the linetype to
            dxf: The drawing engine used to generate the line pattern
        """
        drawing.add_linetype("FOLD", pattern=dxf.linepattern([1, 0, -1]))

    def draw_args(self, name, mode):
        """Returns the kwargs for creating the drawing in the proper mode

        Args:
            name: The name for the drawing
            mode: the mode to request the args in

        Returns:
            The kwargs for creating the drawing in the mode specified by the
                mode argument
        """
        if self.edge_type in (EdgeType.FLAT, EdgeType.NOEDGE):
            return

        svg_args = [{"stroke": c} for c in ["#00ff00", "#ff0000", "#0000ff", "#0000ff"]]
        dxf_args = [{"color": c} for c in [3, 5, 1, 1, 6]]
        layer_args = [{"layer": c} for c in ["Registration", "Cut", "xxx", "Flex"]]

        if mode == "dxf":
          ret = dxf_args[self.edge_type]
          if self.edge_type in (EdgeType.FOLD, EdgeType.FLEX) :
            ret["linetype"] = "FOLD"
          return ret

        elif mode == "silhouette":
          et = self.edge_type
          if et in (EdgeType.FOLD, EdgeType.FLEX) and self.angle % 360 > 180:
            et = 4
          ret = dxf_args[et]
          if self.edge_type in (EdgeType.FOLD, EdgeType.FLEX) :
            ret["linetype"] = "FOLD"
          return ret
        elif mode == "autofold":
          ret = dxf_args[self.edge_type]
          ret.update(layer_args[self.edge_type])
          if self.edge_type == EdgeType.FOLD:
            ret["layer"] = repr(self.angle)
          return ret

        kwargs = {"id" : name}
        kwargs.update(svg_args[self.edge_type])

        if self.edge_type in (EdgeType.FOLD, EdgeType.FLEX) :
          if mode == "print":
            if self.angle % 360 > 180:
              kwargs["stroke"] = "#00ff00"
            else:
              kwargs["stroke"] = "#0000ff"
            kwargs["stroke-dasharray"] = "2 6"
            kwargs["stroke-dashoffset"] = "5"
          if mode == "foldanimate":
            kwargs["stroke"] ='#%02x0000' % (256*self.angle / 180)
          else:
            kwargs["kerning"] = self.angle

        return kwargs

#Helper functions to create the various predefined EdgeTypes
class Flat(EdgeType):
  def __init__(self):
    EdgeType.__init__(self, EdgeType.FLAT)
class Reg(EdgeType):
  def __init__(self):
    EdgeType.__init__(self, EdgeType.REG)
class Cut(EdgeType):
  def __init__(self):
    EdgeType.__init__(self, EdgeType.CUT)
class NoEdge(EdgeType):
  def __init__(self):
    EdgeType.__init__(self, EdgeType.NOEDGE)
def Fold(angle=0):
  if isinstance(angle, (list, tuple)):
    return [EdgeType(EdgeType.FOLD, angle=x) for x in angle]
  else:
    return EdgeType(EdgeType.FOLD, angle=angle)
def Flex(angle=0):
  if isinstance(angle, (list, tuple)):
    return [EdgeType(EdgeType.FLEX, angle=x) for x in angle]
  else:
    return EdgeType(EdgeType.FLEX, angle=angle)

def diag(dx, dy):
  """Returns the diagonal distance between two points.

  Args:
      dx (float): the change in x distance between the two points
      dy (float): the change in y distance between the two points

  Returns:
    The diagonal distance between two points
  """
  return np.sqrt(dx*dx + dy*dy)

all_edges = ["Reg", "Cut", "Fold", "Flex", "Flat", "Tab", "NoEdge"]

class DrawingEdge(object):
  """A class representing an Edge.

  Attributes:
      name (str): The name of the edge
      x1 (int): The x coordinate of the first point of the edge
      y1 (int): The y coordinate of the first point of the edge
      x2 (int): The x coordinate of the second point of the edge
      y2 (int): The y coordinate of the second point of the edge
      edge_type (EdgeType): The type of edge being represented
  """

  def __init__(self, name, pt1, pt2, edge_type):
    """
    Initializes an Edge object with pt1 and pt2 in the form ((x1,y1),(x2,y2))

    The Edge can have 5 different types: CUT, FLAT, BEND, FOLD, TAB

    pt1 (tuple): location of point one in the form (x1, y1)
    pt2 (tuple): location of point one in the form (x2, y2)
    mode (str): 5 different types of Edges: CUT, FLAT, BEND, FOLD, TAB
    """

    self.name = name
    self.x1 = pt1[0]
    self.y1 = pt1[1]
    self.x2 = pt2[0]
    self.y2 = pt2[1]
    if edge_type is None:
      edge_type = Cut()
    self.edge_type = edge_type


  def coords(self):
    """Returns a list of the coordinates of the Edge instance endpoints

    Args:
        None
    Returns:
        A list of the coordinates of the Edge instance endpoints
    """
    coords = [[round(self.x1, 6), round(self.y1, 6)], [round(self.x2, 6), round(self.y2, 6)]]
    for i in coords:
      if i[0] == -0.0:
        i[0] = 0.0
      if i[1] == -0.0:
        i[1] = 0.0
    return coords

  def length(self):
    """Uses the diag() function to return the edge length

    Args:
        None

    Returns:
        The length of the edge
    """
    dx = self.x2 - self.x1
    dy = self.y2 - self.y1
    return diag(dx, dy)

  def angle(self, deg=False):
    """Return the angle of the edge with respect to the positive x axis

    Args:
        deg (bool): sets the angle return type to be degrees if True or radians
            otherwise

    Returns:
        Angle of the Edge instance with respect to the positive x axis
    """
    dx = self.x2 - self.x1
    dy = self.y2 - self.y1
    angle = np.arctan2(dy, dx)
    if deg:
      return np.rad2deg(ang)
    else:
      return angle

  def elongate(self, lengths, otherway = False):
    """Returns a list of Edge instances that extend out from the endpoint of another Edge instance.
    Mode of all smaller edges is the same as the original Edge instance.
    Args:
        lengths (list): list of lengths to split the Edge instance into
        otherway (bool): boolean specifying where to start from (pt2 if otherway == False, pt1 if otherway == True)

    Returns:
        A list of Edge instances that extend out from the endpoint of another Edge instance
    """

    edges = []
    if otherway:
      lastpt = (self.x1, self.y1)
      for length in lengths:
        e = DrawingEdge((0, 0),(-length,0), self.edge_type)
        e.transform(angle=self.angle(), origin=lastpt)
        lastpt = (e.x2, e.y2)
      edges.append(e)
    else:
      lastpt = (self.x2, self.y2)
      for length in lengths:
        e = DrawingEdge((0,0), (length, 0), self.edge_type)
        e.transform(angle=self.angle(), origin=lastpt)
        lastpt = (e.x2, e.y2)
      edges.append(e)

    return edges


  def transform(self, scale=1, angle=0, origin=(0,0)):
    """Scales, rotates, and translates an Edge instance.

    Args:
        scale (float): scaling factor
        angle (float): angle to rotate in radians
        origin (tuple): origin
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
    """Swaps mountain and valley folds

    Args:
        None
    """
    self.edge_type.invert()

  def mirror_x(self):
    """Changes the coordinates of an Edge instance so that it is symmetric about the Y axis.

    Args:
        None
    """
    self.x1 = -self.x1
    self.x2 = -self.x2
    self.flip()

  def mirror_y(self):
    """Changes the coordinates of an Edge instance so that it is symmetric about the X axis.

    Args:
        None
    """
    self.y1 = -self.y1
    self.y2 = -self.y2
    self.flip()

  def flip(self):
    """Flips the directionality of an Edge instance around

    Args:
        None
    """
    x = self.x2
    y = self.y2
    self.x2 = self.x1
    self.y2 = self.y1
    self.x1 = x
    self.y1 = y

  def copy(self):
    """Returns a copy of the edge instance

    Args:
        None
    """

    return DrawingEdge(self.name, (self.x1, self.y1), (self.x2, self.y2), self.edge_type)

  def midpt(self):
    """The midpoint of the edge instance

    Args:
        None

    Returns:
        A tuple of the edge midpoint
    """
    pt1 = self.coords()[0]
    pt2 = self.coords()[1]
    midpt = ((pt2[0]+pt1[0])/2, (pt2[1]+pt1[1])/2)
    return midpt

  def to_drawing(self, drawing, label="", mode=None, engine=None):
    """Draws an Edge instance to a CAD file.

    Args:
        drawing: the drawing file to draw to
        label: location of point two in the form (x2,y2).
        mode: the printing mode to draw for
        engine: the drawing engine being used
    """

    if engine is None:
      engine = drawing

    kwargs = self.edge_type.draw_args(self.name, mode)
    if kwargs:

      dpi = None

      if mode in ( 'Corel', 'print'):
        dpi = 96 # scale from mm to 96dpi for CorelDraw
      elif mode == 'Inkscape':
        dpi = 90 # scale from mm to 90dpi for Inkscape
      elif mode == 'autofold':
        if str(self.edge_type.angle) not in drawing.layers:
          drawing.add_layer(str(self.edge_type.angle))

      if dpi: self.transform(scale=(dpi/25.4))
      drawing.add(engine.line((float(self.x1), float(self.y1)), (float(self.x2), float(self.y2)), **kwargs))
      if dpi: self.transform(scale=(25.4/dpi)) # scale back to mm

    if label:
      r = [int(self.angle(deg=True))]*len(label)
      t = engine.text(label, insert=((self.x1+self.x2)/2, (self.y1+self.y2)/2))# , rotate=r)
      # t.rotate=r
      drawing.add(t)
