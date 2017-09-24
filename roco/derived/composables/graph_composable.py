"""The GraphComposable Module

Contains the GraphComposable class, which adds output functionality to the
graph class
"""

from fegraph.face_edge_graph import FaceEdgeGraph
from roco.api.composable import Composable
from roco.utils.utils import try_import, decorate_graph

class Decoration(Composable, FaceEdgeGraph):
    """
    The base decoration class interface
    """
    def __init__(self):
        FaceEdgeGraph.__init__(self)
    def append(self, new_composable, new_prefix):
        pass
    def attach(self, from_interface, to_interface, **kwargs):
        pass
    def make_output(self, filedir, **kwargs):
        pass

class GraphComposable(Composable, FaceEdgeGraph):
    """Class allowing output to be produced from FaceEdgeGraphs

    The GraphComposable class adds the Composable interface to the
    FaceEdgeGraph class. With this class, graphs can be converted to drawings
    and output to a file or drawn using tkinter

    Attributes:
        component (FoldedComponent): Reference to the FoldedComponent
            represented by the graph
    """

    def __init__(self, transform=None):
        """
        Initializes a GraphComposable

        Args:
            transform: optional initial transform
        """
        self.drawing = None
        FaceEdgeGraph.__init__(self, transform=transform)

    def append(self, g2, prefix2):
        """
        Composes two GraphComposables and prefixes the composable being composed if necessary

        Args:
            g2 (GraphComposable): GraphComposable to append to this one
            prefix2 (str): string to prefix g2 with
        """
        if not g2.placed:
            if not g2.prefixed:
                g2.prefix(prefix2)
                g2.prefixed = True
            self.faces.extend(g2.faces)
            self.edges.extend(g2.edges)
            g2.placed = True

    def attach(self, port1, port2, **kwargs):
        """
        Attaches two ports together in this composable

        Args:
            port1 (Port): first port to attach
            port2 (Port): second port to attach
            **kwargs (dict): arguments for the connection
        """
        # Test whether ports are of right type --
        # Attach if both ports contain edges to attach along
        try:
          label1 = port1.get_edges()
          label2 = port2.get_edges()
        except AttributeError:
            pass
        else:
          # XXX associate ports with specific composables so this isn't necessary
          for i in range(len(label1)):
            if label1[i] not in (e.name for e in self.edges):
              return
            if label2[i] not in (e.name for e in self.edges):
              return

          for i in range(len(label1)):
            newargs = {}
            for key, value in kwargs.iteritems():
              if key == 'tab':
                continue
              if isinstance(value, (list, tuple)):
                newargs[key] = value[i]
              else:
                newargs[key] = value
            try:
              if kwargs['tab'] == True:
                self.add_tab(label1[i], label2[i], **newargs)
                continue
            except:
              pass
            self.merge_edge(label1[i], label2[i], **newargs)
        # Attach if one port contains a Face and the other contains a Decoration
        try:
          face = self.get_face(port1.get_face_name())
          deco = port2.get_decoration()
        except AttributeError:
          try:
            face = self.get_face(port2.get_face_name())
            deco = port1.get_decoration()
          except AttributeError:
            return
        if face is None:
          # XXX associate ports with specific composables so this isn't necessary
          return
        decorate_graph(face, decoration=deco, **kwargs)

    def split_merged_edges(self):
        """
        Splits all the edges that have been merged
        """
        for e in self.edges:
            if len(e.faces) > 1:
                self.split_edge(e)

    def make_output(self, filedir, **kwargs):
        """
        Creates output based on the composable to the given directory.
        The output files depend upon the kwargs.

        Args:
            filedir (str): file directory to place output files
            **kwargs (dict): arguments for the make process as well as output files
        """
        import sys
        if "displayOnly" in kwargs:
          kw_default = not kwargs["displayOnly"]
          kwargs["display"] = kwargs["displayOnly"]
        else:
          kw_default = True

        def kw(arg, default=kw_default):
          if arg in kwargs:
            return kwargs[arg]
          return default

        from roco.derived.utils.tabs import BeamTabs, BeamSlotDecoration
        self.tabify(kw("tabFace", BeamTabs), kw("tabDecoration", None),
                    kw("slotFace", None), kw("slotDecoration", BeamSlotDecoration))
        self.place()

        if kw("placeOnly", False):
          return
        '''
        print
        for f in self.faces:
          if f.transform2D is None:
            print "No 2D transform for face" , f.name
          if f.transform3D is None:
            print "No 3D transform for face" , f.name
        '''

        #if kw("placeOnly", False):
        #  return

        if kw("display") or kw("unfolding") or kw("autofolding") or kw("silhouette"):
          from fegraph.drawing import Drawing
          d = Drawing()
          d.from_graph(self)
          d.transform(relative=(0,0))

        if kw("svgString", False):
          self.drawing = d
          d.to_DXF(filedir + "/silhouette.dxf", mode="silhouette")
          return d.to_SVG('nofile', save_to_file=False)

        if kw("display", False):
          from roco.utils.display import displayTkinter
          displayTkinter(d)

        if kw("unfolding"):
          print "Generating cut-and-fold pattern... ",
          sys.stdout.flush()
          d.to_SVG(filedir + "/lasercutter.svg", mode="Corel")
          print "done."

        if kw("unfolding"):
          print "Generating printer pattern... ",
          sys.stdout.flush()
          d.to_SVG(filedir + "/print.svg", mode="print")
          print "done."

        if kw("silhouette"):
          print "Generating cut-and-fold pattern for Silhouette papercutter... ",
          sys.stdout.flush()
          d.to_DXF(filedir + "/silhouette.dxf", mode="silhouette")
          print "done."

        #3D representation cannot be created without evaluating variables
        '''if kw("autofolding"):
          print "Generating autofolding pattern... ",
          sys.stdout.flush()
          d.toDXF(filedir + "/autofold-default.dxf", mode="autofold")
          print "(graph) ... ",
          sys.stdout.flush()
          self.toDXF(filedir + "/autofold-graph.dxf")
          print "done."'''

        if kw("stl"):
          print "Generating 3D model... ",
          sys.stdout.flush()
          self.to_stl(filedir + "/model.stl")
          print "done."
