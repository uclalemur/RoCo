from roco.derived.components.folded_component import FoldedComponent as fc
from roco.derived.composables.fegraph.face import Face as Face, NON_PARAM_LEN
from roco.derived.composables.fegraph.drawing import Face as FaceD
from roco.api.utils.variable import eval_equation
from roco.utils.mymath import arctan2, norm

class mFingerDrawing(FaceD):
    """This class generate the basic element for finger joint decoration.
    It is to add the finger shape not the rectangle tab face.

    Args:
        w is the width of finger;
        t is the half of the height of finger;

    """
    def __init__(self, length, width, male=True):
        coordsOfDecoration = maleFemaleFingerJointDecorationDrawing(length, width,male=True)
        FaceD.__init__(self, coordsOfDecoration,origin=False)

class fFingerDrawing(FaceD):
    """This class generate the basic element for finger joint decoration.
    It is to add the finger shape not the rectangle tab face.
    
    Args:
        w is the width of finger;
        t is the half of the height of finger;

    """
    def __init__(self, length, width, male=False):
        coordsOfDecoration = maleFemaleFingerJointDecorationDrawing(length, width,male=False)
        FaceD.__init__(self, coordsOfDecoration,origin=False)


def maleFemaleFingerJointDecorationDrawing(length, width,male=True):
    """
    :param length: the length of edge to add finger joint;
    :param width: the width of finger joint;
    :return: return coordinates of finger joint decoration;
    """
    widthOfFingerForD = 5.0  ## the width of finger. ##
    extraSpaceOfFingerJointForD =0.0
    compensationForAssembly = 0.5
    spaceOfEdgeForD = 20.0  ## the space left to avoid overlapping in corner, such as cube. ##
    upperLimitOfMD = eval_equation(length) / (2.0 * widthOfFingerForD) - 2.5  ## the upper boundary for the number of fingers. ##
    length= eval_equation(length)
    width = eval_equation(width)

    ## calculate the coordinates of finger joint face. ##
    if length < eval_equation(spaceOfEdgeForD + widthOfFingerForD * 3.0):
        return "This edge is too short to add finger joint."
    else:
        nOfmFinger = int(eval_equation(upperLimitOfMD))## Find out how many fingers we need.##
        # print (nOfmFinger)

        if male:  ##maleFinger
            nOfOFinger = nOfmFinger
            adjustment = compensationForAssembly
            ## nOfOFinger is the number of opposite finger joint. it is the same as finger joints. ##
        else:
            nOfOFinger = nOfmFinger + 1
            adjustment = - compensationForAssembly
        ## maleFingerDecoration, the number of female fingers must bigger than male by 1. This is the rule. ##
        ## the module here is slightly different from finger joint ##
        fingerModule_rb = ((length / 2.0 + widthOfFingerForD * nOfOFinger - widthOfFingerForD / 2.0)+adjustment, extraSpaceOfFingerJointForD)  ## rb is right and bottom. ##
        fingerModule_rt = ((length / 2.0 + widthOfFingerForD * nOfOFinger - widthOfFingerForD / 2.0)+adjustment, width+extraSpaceOfFingerJointForD)  ## right and top##
        fingerModule_lt = ((length/ 2.0 + widthOfFingerForD * (nOfOFinger - 1.0) - widthOfFingerForD / 2.0)-adjustment, width+extraSpaceOfFingerJointForD)  ## lt is left and top. ##
        fingerModule_lb = ((length / 2.0 + widthOfFingerForD * (nOfOFinger - 1.0) - widthOfFingerForD / 2.0)-adjustment, extraSpaceOfFingerJointForD)  ## left and bottom.##
        ## the order should be shown as following.  ##
        fingerDecorationModule = (fingerModule_rt, fingerModule_rb,fingerModule_lb, fingerModule_lt)
        ## define the coordinates of rest points except the fingers. ##
        # coordinatesOfFingerJoint = ((length, 0), (length, width))
        coordinatesOfFingerDecoration = ((0, width+extraSpaceOfFingerJointForD), (0, 0), (length, 0), (length, width+extraSpaceOfFingerJointForD))
        coordinatesOfFingerSeriesDecoration = ()  ## to save the coordinates of points of fingers. ##

        ## generate coordinates for fingers with a for loop.##
        if nOfOFinger == 1:
            coordinatesOfFingerSeriesDecoration = fingerDecorationModule
        else:
            listOfDFingerModule = [list(x) for x in fingerDecorationModule]  ## convert the nested tuple into nested list because tuple is immutable. ##
        for i in range(nOfOFinger):
            if i == 0:  ## when i = 0, just append the tuple. ##
                coordinatesOfFingerSeriesDecoration += fingerDecorationModule
            else:  ## subtract 10 every time
                for j in range(len(listOfDFingerModule)):
                    listOfDFingerModule[j][0] = listOfDFingerModule[j][0] - 2 * widthOfFingerForD
                tupleOfFingerModule = tuple(tuple(li) for li in listOfDFingerModule)  ##convert the nested list into nested tuple. ##
                coordinatesOfFingerSeriesDecoration += tupleOfFingerModule
        return coordinatesOfFingerDecoration + coordinatesOfFingerSeriesDecoration




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
    try:
        component = kwargs['component']
        length = float(eval_equation(length))
    except:
        # not sympy
        pass

    t = widget(length=length, width=thick, male=male)

    try:
        if kwargs["mirror"]:
            t.mirrorY()
            t.transform(origin=(0, thick / 2.0))
    except:
        pass

    ## find the number of fingers and create unwanted edges' index.
    widthOfFingerForD = 5.0  ## the width of finger. ##
    upperLimitOfMD = eval_equation(length) / (2.0 * widthOfFingerForD) - 2.5
    nOfmFinger = int(eval_equation(upperLimitOfMD))
    if male:  ##maleFinger
        nOfOFinger = nOfmFinger
    else:
        nOfOFinger = nOfmFinger + 1
    unWantedIndex = range(2, 3 + nOfOFinger * 4, 4) ## 2, 6, 10, 14 and so on.
    unWantedIndex.append(1)
    unWantedIndex.append(3)
    unWantedEdgeNames = ["e%d" % i for i in unWantedIndex]

    ## add all of the edges into the face we select ##
    for (name, edge) in t.edges.iteritems():
        e = edge.copy()
        e.transform(angle=theta, origin=globalOrigin)
        if name in unWantedEdgeNames: ## ignore all the bottom edge. ##
            continue
        face.add_decoration((((e.x1, e.y1), (e.x2, e.y2)), e.edge_type.edge_type))
    try:
        if kwargs["alternating"]:
            t.mirrorY()
            t.transform(origin=(0, thick))
    except:
        pass


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
    extraSpaceOfFingerJoint =0.0  ## need calibration ##
    compensationForAssembly = 0.5 ## compensation for laser cutter.##
    #width = thickOfMaterial# add more parameters for real world assemble. ##
    upperLimitOfM = l/(2.0*widthOfFinger) - 2.5 ## the upper boundary for the number of fingers. ##

    ## calculate the coordinates of finger joint face. ##
    if eval_equation(l) < eval_equation(spaceOfEdge + widthOfFinger * 3.0):
        return "This edge is too short to add finger joint."
    else:
        nOfmFinger = int(eval_equation(upperLimitOfM))   ## Find out how many fingers we need.##

        ## male or female finger joint. "
        if male:   ##maleFinger
            nOfFinger = nOfmFinger
            adjustment = compensationForAssembly
        else:
            nOfFinger = nOfmFinger + 1
            adjustment = -compensationForAssembly ## maleFingerDecoration, the number of female fingers must bigger than male by 1. This is the rule. ##
        # print("The number of finger joint",nOfFinger)
        ## generate the coordinates module for fingerJoint face (male and female are the same). ##
        fingerModule_rb = ((l / 2.0 + widthOfFinger * nOfFinger - widthOfFinger / 2.0)+adjustment,extraSpaceOfFingerJoint)  ## rb is right and bottom. ##
        fingerModule_rt = ((l / 2.0 + widthOfFinger * nOfFinger - widthOfFinger / 2.0)+adjustment,extraSpaceOfFingerJoint + width)  ## right and top##
        fingerModule_lt = ((l / 2.0 + widthOfFinger * (nOfFinger - 1.0) - widthOfFinger / 2.0)-adjustment,extraSpaceOfFingerJoint + width)  ## lt is left and top. ##
        fingerModule_lb = ((l / 2.0 + widthOfFinger * (nOfFinger - 1.0) - widthOfFinger / 2.0)-adjustment,extraSpaceOfFingerJoint)  ## left and bottom.##
        fingerModule = (fingerModule_rb, fingerModule_rt, fingerModule_lt, fingerModule_lb)

        ## define the coordinates of rest points except the fingers. ##
        coordinatesOfFingerJoint = ((0, extraSpaceOfFingerJoint), (0, 0), (l, 0), (l, extraSpaceOfFingerJoint))
        coordinatesOfFingerSeries = () ## to save the coordinates of points of fingers. ##


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
        # print(coordinatesOfFingerJoint + coordinatesOfFingerSeries)
        return  coordinatesOfFingerJoint + coordinatesOfFingerSeries



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
  return maleFemaleFingerJointDecoration(face, edge, width, mFingerDrawing,male=True, **kwargs)

def femaleFingerJointDecoration(face, edge, width, **kwargs):
  return maleFemaleFingerJointDecoration(face, edge, width, fFingerDrawing, male=False,**kwargs)

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
    c.add_subcomponent("s4", "Square")
    # c.add_subcomponent('s3','Square')
    c.add_connection(('s1','r'),('s2','l'),angle= 90)
    # c.add_connection(('s1','r'),('s2','l'),tab=True, angle= 90,width=1.5) ##angle=90)
    # c.add_connection(('s1','r'),('s2','l'),tab=True, width=3)  ## width is the width of 'tab'. So it actually equals to the width of material.
    c.add_connection(('s2','r'),('s3','l'),angle= 90)
    c.add_connection(('s3','r'),('s4','l'),angle= 90)
    c.add_connection(('s4','r'),('s1','l'),tab=True, angle= 90,width=1.5)
    # c.add_connection(('s3','r'),('s1','l'),tab=True, width=3)
    # c.make_output(tabFace=None,tabDecoration=None,slotFace=femaleFingerJoint, slotDecoration=None)
    # c.make_output(display=False,thickness=10,tabFace=maleFingerJoint,tabDecoration=maleFingerJointDecoration,slotFace=femaleFingerJoint, slotDecoration=femaleFingerJointDecoration)
    c.make_output(tabFace=maleFingerJoint,tabDecoration=maleFingerJointDecoration,slotFace=femaleFingerJoint, slotDecoration=femaleFingerJointDecoration)
    # c.make_output(display=False,thickness=10)
    # c.make_output()
