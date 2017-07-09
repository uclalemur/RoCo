from roco.derived.composables.fegraph.face import Rectangle
from roco.derived.composables.fegraph.drawing import Face
from roco.derived.composables.fegraph.drawing_edge import DrawingEdge, Flex
from roco.utils.mymath import pi, arctan2, norm
from roco.api.utils.variable import eval_equation

class TabDrawing(Face):
  def __init__(self, w, t, noflap=False):
    if (noflap or eval_equation(t) > eval_equation(w)/2):
      Face.__init__(self,
        ((w,0), (w,t), (0,t)))
    else:
      Face.__init__(self,
        ((w,0), (w+t,0), (w,t), (0,t), (-t,0)))
      self.edges['f0'] = DrawingEdge("f0", (0,0), (0,t), Flex())
      self.edges['f1'] = DrawingEdge("f1", (w,0), (w,t), Flex())

    self.edges.pop('e0')
    self.transform(origin=(-w/2.0,-t/2.))

class SlotDrawing(Face):
  def __init__(self, w, t, noflap=False):
    Face.__init__(self, ((w+0.5, 0), (w+0.5, 0.5), (0, 0.5)))
    self.transform(origin=(-w/2. - 0.25, -t/2. - 0.25));

def BeamTabSlotHelper(face, faceEdge, thick, widget, **kwargs):
    coords = face.edge_coords(face.edge_index(faceEdge))
    globalOrigin = coords[0]
    theta = arctan2(coords[1][1]-coords[0][1], coords[1][0]-coords[0][0])
    length = norm((coords[1][1]-coords[0][1], coords[1][0]-coords[0][0]))

    try:
      frac = kwargs['frac']
    except:
      frac = 0.5
    try:
      noflap = kwargs['noflap']
    except:
      noflap = False

    try:
        component = kwargs['component']
        length = float(eval_equation(length))
    except:
        #not sympy
        pass

    n = 0
    tw = thick * 3
    while (eval_equation(tw) > eval_equation(thick) * 2):
      n += 1
      d = length*1.0 / (n*5+1)
      tw = 2 * d

    t = widget(w=tw, t=thick*frac, noflap=noflap)
    t.transform(angle=pi, origin=(-2 * d, thick/2.))
    try:
      if kwargs["mirror"]:
        t.mirrorY()
        t.transform(origin=(0, thick))
    except: pass

    for i in range(n):
      t.transform(origin=(d * 5, 0))
      for (name, edge) in t.edges.iteritems():
        e = edge.copy()
        e.transform(angle = theta, origin = globalOrigin)
        face.add_decoration((((e.x1, e.y1), (e.x2, e.y2)), e.edge_type.edge_type))
      try:
        if kwargs["alternating"]:
          t.mirrorY()
          t.transform(origin=(0, thick))
      except: pass

def BeamTabDecoration(face, edge, width, **kwargs):
  return BeamTabSlotHelper(face, edge, width, TabDrawing, **kwargs)
def BeamSlotDecoration(face, edge, width, **kwargs):
  return BeamTabSlotHelper(face, edge, width, SlotDrawing, **kwargs)

def BeamTabs(length, width, **kwargs):
    face = Rectangle('tab', length, width,
                        edge_names=["tabedge","e1","oppedge","e3"],
                        recenter=False)
    BeamTabSlotHelper(face, "tabedge", width, TabDrawing, **kwargs)
    return face

def BeamSlots(length, width, **kwargs):
    face = Rectangle('slot', length, width,
                        edge_names=["slotedge","e1","oppedge","e3"],
                        recenter=False)
    BeamTabSlotHelper(face, "slotedge", width, SlotDrawing, **kwargs)
    return face
