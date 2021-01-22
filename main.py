from AnimationEngine import AnimationEngine
from BasicElements import *
from GraphElements import *

import sympy
from sympy.abc import x, y


def cylinder_stream_function(U=1, R=1):
    r = sympy.sqrt(x ** 2 + y ** 2)
    theta = sympy.atan2(y, x)
    return U * (r - R ** 2 / r) * sympy.sin(theta)


if __name__ == '__main__':
    ae = AnimationEngine(1080, 24)

    main_fig, main_axes = ae.get_fig()

    #ae.add_element(TextElement(0, 10, Vec2D(0, 75), main_axes, "hi", horizontalalignment='center',
    #                            verticalalignment='center', color='white', fontsize=72))
    ae.add_element(StreamFunction(0, 10, Vec2D(.1, .1), Vec2D(.8*9/16, .8), main_fig, cylinder_stream_function))

    #ae.browse()
    ae.render('test2', 10)
