from Engine.AnimationEngine import AnimationEngine
from Engine.Elements.GraphElements import Sine
from Engine.Elements.AxesElement import AxesData
from Engine.MathsHelpers import Vec2D
from Engine.Keyframe.Keyframe import KeyFrame
from Engine.Keyframe.Parameter import SetParam, InterpParam


ae = AnimationEngine(1080, 24)

Sine1 = ae.add_element(Sine(Vec2D(.1, .25), Vec2D(.35, .5), axes_data=AxesData(xlim=[-3, 3], ylim=[-3, 3])),
                      0, 10)

Sine2 = ae.add_element(Sine(Vec2D(.55, .25), Vec2D(.35, .5), axes_data=AxesData(xlim=[-3, 3], ylim=[-3, 3])),
                       0, 10)

Sine1Params = Sine1.get_parameters()
Sine2Params = Sine2.get_parameters()


Sine2Params['offset'] = Sine1Params['offset']

Sine1Params['offset'].set_value(2)
print(Sine1._parameters)
print(Sine2._parameters)

#Sine2Params['offset'].set_value(-2)

sequenceA = [KeyFrame([SetParam(Sine1Params['offset'], 1)], start_t=.33, end_t=.5),
             KeyFrame([SetParam(Sine1Params['offset'], 2)], start_t=.5, end_t=.66)]

#sequenceB1 = [KeyFrame([InterpParam(Sine1Params['offset'], 2, 0)], start_t=.33, end_t=0.66)]
#sequenceB2 = [KeyFrame([InterpParam(Sine2Params['offset'], -2, 0)], start_t=.33, end_t=0.66)]


Sine1.attach_keyframes(sequenceA)


ae.browse(10)
