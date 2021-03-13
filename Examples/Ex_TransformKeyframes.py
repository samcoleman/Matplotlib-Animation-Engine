from Engine.AnimationEngine import AnimationEngine

from Engine.Keyframe.Keyframe import *
from Engine.Keyframe.Transform import *


ae = AnimationEngine(1080, 24)

# Consecutive Absolute Transforms
sequence1 = [KeyFrame([Translate2D(Vec2D(.2, .2), True)], .33),
             KeyFrame([Translate2D(Vec2D(.8, .2), True)], .66),
             KeyFrame([Translate2D(Vec2D(.5, .8), True)], 1.0)]

# Consecutive Absolute Transforms, incorrectly ordered
sequence2 = [KeyFrame([Translate2D(Vec2D(.5, .8), True)], start_t=.66, end_t=1.0),
             KeyFrame([Translate2D(Vec2D(.8, .2), True)], start_t=.33, end_t=.66),
             KeyFrame([Translate2D(Vec2D(.2, .2), True)], start_t=0, end_t=.33)]

# Consecutive Relative Transformations
sequence3 = [KeyFrame([Translate2D(Vec2D(.5, .5), True), Rotate(45)], .5),
             KeyFrame([TranslateX(.25), Scale(2)], 1.)]

# Broken Sequence Transformations
sequence4 = [KeyFrame([Translate2D(Vec2D(.5, .2), True)], .25),
             KeyFrame([Translate2D(Vec2D(.5, .8), True)], start_t=0.75, end_t=1.)]

# Broken Sequence Transformations 2
sequence5 = [KeyFrame([Translate2D(Vec2D(.2, .2), True)], .13),
             KeyFrame([Translate2D(Vec2D(.8, .2), True)], start_t=.43, end_t=.56),
             KeyFrame([Translate2D(Vec2D(.5, .8), True)], start_t=.76, end_t=1.0)]

# Unordered, broken links, thought this would break it tbh
sequence6 = [KeyFrame([Translate2D(Vec2D(.2, .2), True)], end_t=.33),
             KeyFrame([Scale(2)], start_t=0, end_t=.15),
             KeyFrame([Translate2D(Vec2D(.8, .2), True)], start_t=.33, end_t=.66),
             KeyFrame([Rotate(180)], start_t=.15, end_t=.33),
             KeyFrame([Rotate(180)], start_t=.66, end_t=.85),
             KeyFrame([Translate2D(Vec2D(.5, .8), True)], start_t=.66, end_t=1.0),
             KeyFrame([Scale(.5)], start_t=.85, end_t=1.0)]

text = ae.add_element(TextElement(Vec2D(.5, .8), "Hello", 72,
                                  horizontalalignment='center', verticalalignment='center', color='white'),
                      0, 10)

text.attach_keyframes(sequence6)

ae.browse(10)
