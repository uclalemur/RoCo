from roco.api.utils.variable import eval_equation
from roco.derived.composables.fegraph.drawing import Drawing
from roco.derived.utils.tabs import TabDrawing
from roco.utils.mymath import pi, arctan2, norm

tab = TabDrawing(3,4)
print tab
tab.transform(origin=(1,2))
print tab


