from Engine.AnimationEngine import AnimationEngine

from Engine.Keyframe.Keyframe import *
from Engine.Keyframe.Transform import *

if __name__ == '__main__':
    ae = AnimationEngine(1080, 24)

    sequence = [KeyFrame([TranslateY(-.6)], 1.)]

    text = ae.add_element(TextElement(Vec2D(.5, .8), "Hello", 72,
                                      horizontalalignment='center', verticalalignment='center', color='white'),
                          0, 10)

    text.attach_sequence([KeyFrame([Translate2D(Vec2D(.5, .5)), Rotate(45)], .5),
                          KeyFrame([TranslateX(0), Scale(2, absolute=False)], 1.)])

    # cp = ae.add_element(Sine(0, 10, Vec2D(.25, .25), Vec2D(.5, .5), main_fig))
    # params = cp.get_parameters()

    # sequence3 = [KeyFrame([InterpParam(params['height'], 1, 2)], .5),
    #             KeyFrame([InterpParam(params['height'], 2, 1)], .75)]

    # params['height'].set_value(1.5)

    ae.browse(10)
    # ae.render('test2', 10)
