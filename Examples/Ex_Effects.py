from Engine.AnimationEngine import AnimationEngine

from Engine.Elements.GraphElements import Sine

from Engine.Keyframe.Keyframe import *
from Engine.Keyframe.Transform import *
from Engine.Keyframe.Effects import *

ae = AnimationEngine(1080, 24)

# Consecutive Absolute Transforms
sequence1 = [KeyFrame([Translate2D(Vec2D(.2, .2), True), Alpha(.5)], .33),
             KeyFrame([Translate2D(Vec2D(.8, .2), True)], .66),
             KeyFrame([Translate2D(Vec2D(.5, .8), True), Alpha(1.)], 1.0)]

sequence2 = [KeyFrame([Typewrite()], .33)]

text1 = ae.add_element(TextElement(Vec2D(.5, .8), "Hello", 72,
                       horizontalalignment='center', verticalalignment='center', color='white', alpha=.9),
                       0, 10)
text2 = ae.add_element(TextElement(Vec2D(.5, .5), "Hello", 72,
                       horizontalalignment='left', verticalalignment='center', color='white', alpha=.9),
                       0, 10)

# Switch sequences here
text1.attach_sequence(sequence1)
text2.attach_sequence(sequence2)


ae.browse(10)