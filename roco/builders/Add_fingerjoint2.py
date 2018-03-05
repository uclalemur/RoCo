from roco.derived.components.folded_component import FoldedComponent as fc
from roco.derived.composables.fegraph.face import Face as Face, NON_PARAM_LEN
from roco.derived.composables.fegraph.drawing import Face as FaceD
from roco.api.utils.variable import eval_equation
from roco.utils.mymath import arctan2, norm

class FingerDecorationDrawing(FaceD):
    """This class generate the basic element for finger joint decoration.
    It is to add the finger shape not the rectangle tab face.
         argument:
             w is the width of finger;
             t is the half of the height of finger;

    """
    def __init__(self, length, width):
        FaceD.__init__(self, ((length,0), (length,width), (0,width)))


def maleFemaleFingerJointDecoration(face,faceEdge, thick, widget,male=True, **kwargs):
    """
    help to find how many fingers we need for different subcomponent.And add these fingers into the face.
    :param face: The face we add decoration;
    :param faceEdge: the edge we refer to;
    :param thick: the width of finger, it usually is 3.0mm.
    :param male: the type of decoration;
    :param widget: a face object to represent the finger;
    :param kwargs: kwargs;
    :return: None. the decoration will be added into selected face after operation
    """
    coords = face.edge_coords(face.edge_index(faceEdge))
    globalOrigin = coords[0]
    theta = arctan2(coords[1][1] - coords[0][1], coords[1][0] - coords[0][0])
    length = norm((coords[1][1] - coords[0][1], coords[1][0] - coords[0][0]))
    length = eval_equation(length)
    try:
        component = kwargs['component']
        length = float(eval_equation(length))
    except:
        # not sympy
        pass

        ## find the number of fingers and create unwanted edges' index.
    widthOfFinger = 5.0  ## the width of finger. ##
    spaceOfEdge = 20.0
    upperLimitOfMD = eval_equation(length) / (2.0 * widthOfFinger) - 2.5
    nOfmFinger = int(eval_equation(upperLimitOfMD))
    if eval_equation(length) < eval_equation(spaceOfEdge + widthOfFinger * 3.0):
        return "This edge is too short to add finger joint."
    if male:  ##maleFinger
        nOfOFinger = nOfmFinger
    else:
        nOfOFinger = nOfmFinger + 1


    lengthOfSpace = (length-(2*nOfOFinger-1)*widthOfFinger)/2.0
    widthOfFingerForD = widthOfFinger
    widthOfDecoration = widthOfFinger


    t_l = widget(length=eval_equation(lengthOfSpace), width=thick)
    t = widget(length=eval_equation(widthOfDecoration), width=thick)
    t_r = widget(length=eval_equation(lengthOfSpace), width=thick)


    ## for left side space******************
    for (name, edge) in t_l.edges.iteritems():
        e = edge.copy()
        e.transform(angle=theta, origin=globalOrigin)
        face.add_decoration((((e.x1, e.y1), (e.x2, e.y2)), e.edge_type.edge_type))
    try:
        if kwargs["alternating"]:
            t.mirrorY()
            t.transform(origin=(0, thick))
    except:
        pass
    ##****************************

    ## add all of the edges into the face we select ##
    for i in range(1,nOfOFinger):
      if (i==1):
          movementOfOriginal = eval_equation(widthOfFingerForD+lengthOfSpace)
      else:
          movementOfOriginal = eval_equation(widthOfFingerForD+widthOfDecoration)  ## need to revise to be able to fit with assembly
      t.transform(origin=(movementOfOriginal, 0))
      for (name, edge) in t.edges.iteritems():
        e = edge.copy()
        e.transform(angle=theta, origin=globalOrigin)
        face.add_decoration((((e.x1, e.y1), (e.x2, e.y2)), e.edge_type.edge_type))

      try:
          if kwargs["alternating"]:
              t.mirrorY()
              t.transform(origin=(0, thick))
      except:
          pass


    ## for right side space******************
    t_r.transform(origin=((length/ 2.0 + widthOfFingerForD * nOfOFinger - widthOfFingerForD / 2.0), 0))
    for (name, edge) in t_r.edges.iteritems():
        e = edge.copy()
        e.transform(angle=theta, origin=globalOrigin)
        face.add_decoration((((e.x1, e.y1), (e.x2, e.y2)), e.edge_type.edge_type))
    try:
        if kwargs["alternating"]:
            t.mirrorY()
            t.transform(origin=(0, thick))
    except:
        pass
    ##****************************

def maleFemaleFingerJointDrawing(l,width,male=True):
    """
    :param l: the length of edge which you want to add finger joint;
    :param width: the width of finger
    :param male: type of finger joint, male or female
    :return: return the coordinates of finger joint face.
    """
    ## create the coordinates for male finger joint. ##

    # thickOfMaterial = 3.0  ## the thickness of material. #
    l = eval_equation(l)
    width = eval_equation(width)
    widthOfFinger = 5.0  ## the width of finger. ##
    spaceOfEdge = 20.0  ## the space left to avoid overlapping in corner, such as cube. ##
    extraSpaceOfFingerJoint =0.0  ## need calibration ##
    #width = thickOfMaterial# add more parameters for real world assemble. ##
    upperLimitOfM = l/(2.0*widthOfFinger) - 2.5 ## the upper boundary for the number of fingers. ##

    ## calculate the coordinates of finger joint face. ##
    if l < eval_equation(spaceOfEdge + widthOfFinger * 3.0):
        return "This edge is too short to add finger joint."
    else:
        nOfmFinger = int(eval_equation(upperLimitOfM))   ## Find out how many fingers we need.##

        ## male or female finger joint. "
    if male:  ##maleFinger
        nOfFinger = nOfmFinger
    else:
        nOfFinger = nOfmFinger + 1
    ## maleFingerDecoration, the number of female fingers must bigger than male by 1. This is the rule. ##

    ## generate the coordinates module for fingerJoint face (male and female are the same). ##
    fingerModule_rb = ((l / 2.0 + widthOfFinger * nOfFinger - widthOfFinger / 2.0),
                       extraSpaceOfFingerJoint)  ## rb is right and bottom. ##
    fingerModule_rt = ((l / 2.0 + widthOfFinger * nOfFinger - widthOfFinger / 2.0) ,
                       extraSpaceOfFingerJoint + width)  ## right and top##
    fingerModule_lt = ((l / 2.0 + widthOfFinger * (nOfFinger - 1.0) - widthOfFinger / 2.0) ,
                       extraSpaceOfFingerJoint + width)  ## lt is left and top. ##
    fingerModule_lb = ((l / 2.0 + widthOfFinger * (nOfFinger - 1.0) - widthOfFinger / 2.0),
                       extraSpaceOfFingerJoint)  ## left and bottom.##
    fingerModule = (fingerModule_rb, fingerModule_rt, fingerModule_lt, fingerModule_lb)

    ## define the coordinates of rest points except the fingers. ##
    coordinatesOfFingerJoint = ((0, extraSpaceOfFingerJoint), (0, 0), (l, 0), (l, extraSpaceOfFingerJoint))
    coordinatesOfFingerSeries = ()  ## to save the coordinates of points of fingers. ##

    ## generate coordinates for fingers with a for loop.##
    if nOfFinger == 1:
        coordinatesOfFingerSeries = fingerModule
    else:
        listOfFingerModule = [list(x) for x in fingerModule]  ## convert the nested tuple into nested list because tuple is immutable. ##
    for i in range(nOfFinger):
        if i == 0:  ## when i = 0, just append the tuple. ##
            coordinatesOfFingerSeries += fingerModule
        else:  ## substruct 10 every time
            for j in range(len(listOfFingerModule)):
                listOfFingerModule[j][0] = listOfFingerModule[j][0] - 2 * widthOfFinger
            tupleOfFingerModule = tuple(tuple(li) for li in listOfFingerModule)  ##convert the nested list into nested tuple. ##
            coordinatesOfFingerSeries += tupleOfFingerModule
    return coordinatesOfFingerJoint + coordinatesOfFingerSeries



class mFingerJoint(Face):
    """
    Face class. It takes in the length of the edge and width of finger joint. Then create the coordinates for the finger joint face. Finally it generates a finger joint face.
    """
    def __init__(self, length, width, male=True, **kwargs):
        coordsOfFinger = maleFemaleFingerJointDrawing(eval_equation(length),width, male)
        edge_names = ["e%d" % i for i in range(len(coordsOfFinger))]
        edge_names[2] = "tabedge"
        Face.__init__(self,'mfinger_joint',coordsOfFinger,[NON_PARAM_LEN for x in coordsOfFinger],edge_names=edge_names)
        ## NON_PARAM_LEN just fix the length of all edges we have.

class fFingerJoint(Face):
    """
    Face class. It takes in the length of the edge and width of finger joint. Then create the coordinates for the finger joint face. Finally it generates a finger joint face.
    """
    def __init__(self, length, width, male=False, **kwargs):
        coordsOfFinger = maleFemaleFingerJointDrawing(eval_equation(length),width, male)
        edge_names = ["e%d" % i for i in range(len(coordsOfFinger))]
        edge_names[2] = "slotedge"
        Face.__init__(self,'ffinger_joint',coordsOfFinger,[NON_PARAM_LEN for x in coordsOfFinger],edge_names=edge_names)
        ## NON_PARAM_LEN just fix the length of all edges we have.



def maleFingerJointDecoration(face, edge, width, **kwargs):
  return maleFemaleFingerJointDecoration(face, edge, width, FingerDecorationDrawing,male=True, **kwargs)

def femaleFingerJointDecoration(face, edge, width, **kwargs):
  return maleFemaleFingerJointDecoration(face, edge, width, FingerDecorationDrawing, male=False,**kwargs)

def maleFingerJoint(length, width, **kwargs):  ## must return a face here.
    face = mFingerJoint(length,width,male=True,edge_names=["tabedge","e1","oppedge","e3"],recenter=False)
    return face

def femaleFingerJoint(length, width, **kwargs):
    face = fFingerJoint(length, width,male=False,edge_names=["slotedge","e1","oppedge","e3"],recenter=False)
    return face

if __name__ == "__main__":
    ## code to execute. ##
    c = fc()
    c.add_subcomponent('s1','Square')
    c.add_subcomponent('s2','Square')
    c.add_subcomponent("s3", "Square")
    # c.add_subcomponent("s4", "Square")
    # c.add_subcomponent('s3','Square')
    # c.add_connection(('s1','r'),('s2','l'),angle= 90)
    # c.add_connection(('s1','r'),('s2','l'),tab=True, angle= 90,width=1.5) ##angle=90)
    # c.add_connection(('s1','r'),('s2','l'),tab=True, width=3)  ## width is the width of 'tab'. So it actually equals to the width of material.
    # c.add_connection(('s2','r'),('s3','l'),angle= 90)
    # c.add_connection(('s3','r'),('s4','l'),angle= 90)
    c.add_connection(('s1','r'),('s2','l'),tab=True, angle= 90,width=1.5)
    c.add_connection(('s2','r'),('s3','l'),tab=True, angle= 90,width=1.5)
    # c.add_connection(('s3','r'),('s1','l'),tab=True, width=3)
    # c.make_output(tabFace=None,tabDecoration=None,slotFace=femaleFingerJoint, slotDecoration=None)
    # c.make_output(display=False,thickness=10,tabFace=maleFingerJoint,tabDecoration=maleFingerJointDecoration,slotFace=femaleFingerJoint, slotDecoration=femaleFingerJointDecoration)
    c.make_output(thickness=10,tabFace=maleFingerJoint,tabDecoration=maleFingerJointDecoration,slotFace=femaleFingerJoint, slotDecoration=femaleFingerJointDecoration)
    # c.make_output(display=False,thickness=10)
    # c.make_output()
