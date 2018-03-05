from roco.derived.composables.fegraph.face import Face, NON_PARAM_LEN
from roco.api.utils.variable import eval_equation

def CoorForFingerjoint(l,male=True):
    ## create the coordinates for male finger joint. ##
    '''l is the length of edge which you want to add finger joint.'''

    thickOfMaterial = 3.0  ## the thickness of material. ##
    widthOfFinger = 5.0  ## the width of finger. ##
    spaceOfEdge = 20.0  ## the space left to avoid overlapping in corner, such as cube. ##
    extraSpaceOfFingerJoint = 0.0 ## the extra space needed to connect all fingers. ##
    heightOfFinger = thickOfMaterial ## add more parameters for real world assemble. ##
    upperLimitOfM = l/(2.0*widthOfFinger) - 2.5 ## the upper boundary for the number of fingers. ##

    ## calculate the coordinates of finger joint face. ##
    if l < (spaceOfEdge + widthOfFinger * 3.0):
        return "This edge is too short to add finger joint."
    else:
        nOfmFinger = int(upperLimitOfM)   ## Find out how many fingers we need.##

        ## male or female finger joint. "
        if male:
            nOfFinger = nOfmFinger

        else:
            nOfFinger = nOfmFinger + 1  ## the number of female fingers must bigger than male by 1. This is the rule. ##

        ## generate the coordinates module for fingerJoint face (male and female are the same). ##
        fingerModule_rb = ((l / 2.0 + widthOfFinger * nOfFinger - widthOfFinger / 2.0),
                               extraSpaceOfFingerJoint)  ## rb is right and bottom. ##
        fingerModule_rt = ((l / 2.0 + widthOfFinger * nOfFinger - widthOfFinger / 2.0),
                               extraSpaceOfFingerJoint + heightOfFinger)  ## right and top##
        fingerModule_lt = ((l / 2.0 + widthOfFinger * (nOfFinger - 1.0) - widthOfFinger / 2.0),
                               extraSpaceOfFingerJoint + heightOfFinger)  ## lt is left and top. ##
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

class FingerJoint(Face):
    def __init__(self, length, male=True,**kwargs):
        coords = CoorForFingerjoint(eval_equation(length),male)
        edge_names = ["e%d" % i for i in range(len(coords))]
        edge_names[2] = "attachedge"
        Face.__init__(self,'finger_joint',coords,[NON_PARAM_LEN for x in coords],edge_names=edge_names)
        ## NON_PARAM_LEN just fix the length of all edges we have.





if __name__ == "__main__":  ## only execute this code when you run the code from this dir
    d = CoorForFingerjoint(40,'female')
    print(d)
    