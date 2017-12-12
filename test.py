from roco.derived.components.folded_component import FoldedComponent as fc
from roco.derived.composables.fegraph.drawing import Face
from roco.derived.composables.fegraph.face import Face as Fac, NON_PARAM_LEN
from roco.api.utils.variable import eval_equation
from roco.utils.mymath import pi, arctan2, norm

class FingerDrawing(Face):
    """This class generate the basic element for finger joint decoration.
    It is to add the finger shape not the rectangle tab face.
         argument:
             w is the width of finger;
             t is the half of the height of finger;

    """
    def __init__(self, w, t):
      Face.__init__(self,((w,0), (w,t), (0,t)),None)

def maleFemaleFingerJointHelper(face,faceEdge, thick, male=True, widget=FingerDrawing, **kwargs):
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
    ## the faceEdge is changed after add Tab_face. we match the change here. ##
    # try:
    #     coords = face.edge_coords(face.edge_index(faceEdge))
    # except:
    #     try:
    #         coords = face.edge_coords(face.edge_index(faceEdge+'_tabedge'))
    #     except:
    #         coords = face.edge_coords(face.edge_index(faceEdge + '_slotedge'))
    coords = face.edge_coords(face.edge_index(faceEdge))
    globalOrigin = coords[0]
    theta = arctan2(coords[1][1] - coords[0][1], coords[1][0] - coords[0][0])
    length = norm((coords[1][1] - coords[0][1], coords[1][0] - coords[0][0]))

    widthOfFinger = 5.0  ## the width of finger. ##
    spaceOfEdge = 20.0  ## the space left to avoid overlapping in corner, such as cube. ##
    heightOfHalfFinger = thick / 2.0  ## we split the finger into two.
    upperLimitOfM = length / (2.0 * widthOfFinger) - 2.5  ## the upper boundary for the number of fingers. ##


    ## calculate the coordinates of finger joint face. ##
    if eval_equation(length) < eval_equation(spaceOfEdge + widthOfFinger * 3.0):
        return "This edge is too short to add finger joint."
    else:
        nOfmFinger = int(eval_equation(upperLimitOfM))  ## Find out how many fingers we need.##

        ## male or female finger joint. "
        if male:  ##maleFinger
            nOfDFinger = nOfmFinger-1
        else:
            nOfDFinger = nOfmFinger  ## maleFingerDecoration, the number of female fingers must bigger than male by 1. This is the rule. ##


## you need yo solve how to decorate the rectangle into the face we have.##


    ## boundary rectangle 1st ##
    b1 = widget(w=(length-widthOfFinger*(2*nOfDFinger-1))/2.0, t=heightOfHalfFinger)
    b1.transform(angle=2*pi, origin=(-2 * widthOfFinger, 0))  ## use 2*pi to make the finger upper side down ,but it is the correct answer?
    for (name, edge) in b1.edges.iteritems():
        e = edge.copy()
        e.transform(angle=theta, origin=globalOrigin)
        face.add_decoration((((e.x1, e.y1), (e.x2, e.y2)), e.edge_type.edge_type))


    t = widget(w=widthOfFinger, t=heightOfHalfFinger)
    t.transform(angle=2*pi, origin=(-2 * widthOfFinger, 0))

    try:
        if kwargs["mirror"]:
            t.mirrorY()
            t.transform(origin=(0, thick / 2.0))
    except:
        pass

    ## middle fingers ##
    for i in range(nOfDFinger):
        t.transform(origin=(widthOfFinger * 5, 0))
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

    ## boundary rectangle last ##
    b2 = widget(w=(length - widthOfFinger * (2 * nOfDFinger - 1)) / 2.0, t=heightOfHalfFinger)
    b2.transform(angle=2*pi, origin=(-2 * widthOfFinger, 0))
    for (name, edge) in b2.edges.iteritems():
        e = edge.copy()
        e.transform(angle=theta, origin=globalOrigin)
        face.add_decoration((((e.x1, e.y1), (e.x2, e.y2)), e.edge_type.edge_type))


def maleFemaleFingerJointDrawing(l,width,male=True):
    """

    :param l: the length of edge which you want to add finger joint;
    :param width: the width of finger
    :param male: type of finger joint, male or female
    :return: return the coordinates of finger joint face.
    """
    ## create the coordinates for male finger joint. ##

    # thickOfMaterial = 3.0  ## the thickness of material. #
    widthOfFinger = 5.0  ## the width of finger. ##
    spaceOfEdge = 20.0  ## the space left to avoid overlapping in corner, such as cube. ##
    extraSpaceOfFingerJoint = 0.0 ## the extra space needed to connect all fingers. ##
     #width = thickOfMaterial# add more parameters for real world assemble. ##
    heightOfHalfFinger = width/2.0 ## we split the
    upperLimitOfM = l/(2.0*widthOfFinger) - 2.5 ## the upper boundary for the number of fingers. ##

    ## calculate the coordinates of finger joint face. ##
    if eval_equation(l) < eval_equation(spaceOfEdge + widthOfFinger * 3.0):
        return "This edge is too short to add finger joint."
    else:
        nOfmFinger = int(eval_equation(upperLimitOfM))   ## Find out how many fingers we need.##

        ## male or female finger joint. "
        if male:   ##maleFinger
            nOfFinger = nOfmFinger
        else:
            nOfFinger = nOfmFinger + 1  ## maleFingerDecoration, the number of female fingers must bigger than male by 1. This is the rule. ##

        ## generate the coordinates module for fingerJoint face (male and female are the same). ##
        fingerModule_rb = ((l / 2.0 + widthOfFinger * nOfFinger - widthOfFinger / 2.0),
                               extraSpaceOfFingerJoint)  ## rb is right and bottom. ##
        fingerModule_rt = ((l / 2.0 + widthOfFinger * nOfFinger - widthOfFinger / 2.0),
                               extraSpaceOfFingerJoint + heightOfHalfFinger)  ## right and top##
        fingerModule_lt = ((l / 2.0 + widthOfFinger * (nOfFinger - 1.0) - widthOfFinger / 2.0),
                               extraSpaceOfFingerJoint + heightOfHalfFinger)  ## lt is left and top. ##
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

        return  coordinatesOfFingerJoint + coordinatesOfFingerSeries



class mFingerJoint(Fac):
    """
    Face class. It takes in the length of the edge and width of finger joint. Then create the coordinates for the finger joint face. Finally it generates a finger joint face.
    """
    def __init__(self, length, width, male=True, **kwargs):
        coordsOfFinger = maleFemaleFingerJointDrawing(eval_equation(length),width, male)
        edge_names = ["e%d" % i for i in range(len(coordsOfFinger))]
        edge_names[2] = "tabedge"
        Fac.__init__(self,'finger_joint',coordsOfFinger,[NON_PARAM_LEN for x in coordsOfFinger],edge_names=edge_names)
        ## NON_PARAM_LEN just fix the length of all edges we have.
class fFingerJoint(Fac):
    """
    Face class. It takes in the length of the edge and width of finger joint. Then create the coordinates for the finger joint face. Finally it generates a finger joint face.
    """
    def __init__(self, length, width, male=False, **kwargs):
        coordsOfFinger = maleFemaleFingerJointDrawing(eval_equation(length),width, male)
        edge_names = ["e%d" % i for i in range(len(coordsOfFinger))]
        edge_names[2] = "slotedge"
        Fac.__init__(self,'finger_joint',coordsOfFinger,[NON_PARAM_LEN for x in coordsOfFinger],edge_names=edge_names)
        ## NON_PARAM_LEN just fix the length of all edges we have.



def maleFingerJointDecoration(face, edge, width, **kwargs):
  return maleFemaleFingerJointHelper(face, edge, width, male=True, shape=FingerDrawing, **kwargs)

def femaleFingerJointDecoration(face, edge, width, **kwargs):
  return maleFemaleFingerJointHelper(face, edge, width, male=False, shape=FingerDrawing, **kwargs)

def maleFingerJoint(length, width, **kwargs):  ## must return a face here.
    face = mFingerJoint(length,width,edge_names=["tabedge","e1","oppedge","e3"],recenter=False)
    return face

def femaleFingerJoint(length, width, **kwargs):
    face = fFingerJoint(length, width,male=False,edge_names=["slotedge","e1","oppedge","e3"],recenter=False)
    return face









## code to execute. ##
c = fc()
c.add_subcomponent('s1','Square')
c.add_subcomponent('s2','Square')
# c.add_subcomponent('s3','Square')
c.add_connection(('s1','r'),('s2','l'),tab=True, width=3)
# c.add_connection(('s1','r'),('s2','l'),tab=True, width=3)  ## width is the width of 'tab'. So it actually equals to the width of material.
# c.add_connection(('s2','r'),('s3','l'))
# c.add_connection(('s3','r'),('s1','l'),tab=True, width=3)
c.make_output(tabFace=maleFingerJoint,tabDecoration=maleFingerJointDecoration,slotFace=femaleFingerJoint, slotDecoration=femaleFingerJointDecoration)
# c.make_output()