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

case = 2

# Setting parameter values and attaching keyframe sequence using SetParam
if case == 0:
    Sine1Params['offset'].set_value(2)
    Sine2Params['offset'].set_value(-2)
    sequence1 = [KeyFrame([SetParam(Sine1Params['offset'], 1)], start_t=.33, end_t=.66),
                 KeyFrame([SetParam(Sine1Params['offset'], 0)], start_t=.66, end_t=1.0)]
    sequence2 = [KeyFrame([SetParam(Sine2Params['offset'], -1)], start_t=.33, end_t=0.66),
                 KeyFrame([SetParam(Sine2Params['offset'], 0)],  start_t=.66, end_t=1.0)]
    Sine1.attach_sequence(sequence1)
    Sine2.attach_sequence(sequence2)

# Using InterpParam
elif case == 1:
    Sine1Params['offset'].set_value(2)
    Sine2Params['offset'].set_value(-2)
    sequence1 = [KeyFrame([InterpParam(Sine1Params['offset'], 2, 0)], start_t=.33, end_t=0.66)]
    sequence2 = [KeyFrame([InterpParam(Sine2Params['offset'], -2, 0)], start_t=.33, end_t=0.66)]
    Sine1.attach_sequence(sequence1)
    Sine2.attach_sequence(sequence2)

# Linking of parameters, reactive programming?
elif case == 2:
    Sine2Params['offset'] = Sine1Params['offset']
    Sine1Params['offset'].set_value(0)
    sequenceA = [KeyFrame([SetParam(Sine1Params['offset'], 1)], start_t=.33, end_t=.66),
                 KeyFrame([SetParam(Sine1Params['offset'], 2)], start_t=.66, end_t=1.0)]
    Sine1.attach_sequence(sequenceA)
    # Note Sine2.attach_keyframes not needed as when the Sine1 offset parameter changes it automatically updates
    # Sine2 offset (they are the same object)


ae.browse(10)
