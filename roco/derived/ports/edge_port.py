"""EdgePort class.

This module contains the EdgePort class.

"""

from roco.api.port import Port

class EdgePort(Port):
    """A class representing a physical edge that can be connected to.

    Attributes:
        edge (HyperEdge): holds the edge data that the port is associated with.
        edge_name (str): the name of the edge in the parent graph

    """

    def __init__(self, parent, edge_name):
        """Creates a edge port object.

        Args:
            parent (component): The component to which this port will be added.
            edge_name: the name of the edge in the parent graph

        Raises:
            AttributeError: The edge with the given name does not have a
                length attribute
        """
        graph = parent.get_graph()
        self.edge = graph.get_edge(edge_name)
        # self.placed = False
        params = {}
        try:
            params = {'length': self.edge.length}
            # params = {'pts3D': edge.pts3D}
            # for i in range(2):
            # for j, x in enumerate(["x", "y", "z"]):
            # params["pt%d%s" % (i, x)] = self.edge.pts3D[i][j]
        except AttributeError:
            raise AttributeError("Unplaced edge: " + edge_name)

        Port.__init__(self, parent, params)
        self.edge_name = edge_name

    def get_edges(self):
        """Returns the edge associated with the port

        Args:
            None

        Returns:
            List containing names of edges
        """
        return [self.edgeName]

    def get_points(self):
        """Returns the points associated with the edge

        Args:
            None

        Returns:
            Edge points
        """
        return self.edge.pts_3D

    def prefix(self, prefix=""):
        """Adds a prefix to the edge name

        Args:
            prefix (str): The prefix string
        """
        # if self.placed:
        #  return
        self.edge_name = prefix_string(prefix, self.edge_name)
        # self.placed = True

    def __str__(self):
        return str(self.get_edges())

    def update(self):
        """Updates th edge length parameter

        Args:
            None

        Raises:
            AttributeError: The edge with the given name does not have a
                length attribute
        """
        try:
            self.parameters['length'] = self.edge.length
        except AttributeError:
            raise AttributeError("Unplaced edge: " + self.edge.name)

    def constrain(self, parent, to_port, **kwargs):
        """Return a set of semantic constraints to be satisfied when connecting to to_port object
        By default, constrain same-named parameters to be equal

        Override this method for better matching

        Args:
            parent (component): The component to which this port will be added.
            to_port: The port to be connected to

        Returns:
            list of semantic constraints

        Raises:
            AttributeError: The edge with the given name does not have a
                length attribute
        """

        # Can't use default constrain function because pt1 connects to pt2 and vice versa
        constraints = []
        try:
            if (self.get_parameter("length") != to_port.get_parameter("length")):
                constraints.append((Eq(self.get_parameter("length"), to_port.get_parameter("length"))))
                #      for i in range(2):
                #       for x in ["x", "y", "z"]:
                #         constraints.append(Eq(self.getParameter("pt%d%s" % (i, x)), toPort.getParameter("pt%d%s" % (1-i, x))))
        except AttributeError:
            raise AttributeError("Missing edge coordinates attaching EdgePorts")

            # try:
            #  angle = kwargs["angle"]
            #  if len(self.edge.faces) > 1:
            #    print "Too many faces on", self.edgeName, "-- using the first"
            #  if len(toPort.edge.faces) > 1:
            #    print "Too many faces on", toPort.edgeName, "-- using the first"
            #  myNormal = self.edge.faces.keys()[0].get3DNormal()
            #  toNormal = toPort.edge.faces.keys()[0].get3DNormal()
            # constraints.append(Eq(myNormal.dot(toNormal), cos(deg2rad(angle))))

        except KeyError:
            # no angle given
            pass

        return constraints
