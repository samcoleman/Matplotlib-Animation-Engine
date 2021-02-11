from AnimationEngine import AnimationEngine
from BasicElements import *
from GraphElements import *
from ComplexPotential import *

import sympy
from sympy.abc import x, y, z

from KeyFrame import KeyFrame
from Transform import TranslateX

from typing import List, Tuple
from myMaths import Vec3D

from AxesElements import AxesData


def cylinder_stream_function(U=1, R=1):
    r = sympy.sqrt(x ** 2 + y ** 2)
    theta = sympy.atan2(y, x)
    return U * (r - R ** 2 / r) * sympy.sin(theta)


if __name__ == '__main__':
    ae = AnimationEngine(1080, 24)

    ar = ae.get_ar()

    main_fig, main_axes = ae.get_fig()

    """
    sequence = [([Translate2D(Vec2D(.25, .75)),
                  Rotate(45)], .5),
                ([Translate2D(Vec2D(.75, .25)),
                  Scale(2, False),
                  Rotate(45, False)], 1.)]

    sequence2 = [([Translate2D(Vec2D(.25, 0), False),
                   Scale2D(Vec2D(2, 0))], 1.)]
    """

    text = ae.add_element(TextElement(0, 10, Vec2D(.5, .8), main_axes, "Hello", 72,
                                      horizontalalignment='center', verticalalignment='center', color='white'))
    #text.attach_keyframes([KeyFrame([Translate2D(Vec2D(.5, .5))], .5),
    #                       KeyFrame([TranslateX(0), Scale(2)], 1.)])

    U = 1
    a = 1
    c = .1
    alpha = 0  # 2*np.pi/16
    beta = 0  # .1

    C = Circle(0, a)

    gamma = -4 * np.pi * U * a * np.sin(beta + alpha)  # Circulation

    F = U * z * sympy.exp(-1j * alpha) + \
        U * (a ** 2) * sympy.exp(1j * alpha) / z - \
        1j * gamma * sympy.ln(z) / (2 * np.pi)

    levels = np.arange(-2.8, 4.8, 0.2).tolist()

    cp = ae.add_element(JoukowskiAerofoil(0, 10, Vec2D(.25, .25), Vec2D(.5, .5), main_fig,
                                          levels, axes_data=AxesData(xlim=[-3, 3], ylim=[-3, 3], aspect='equal')))

    #sf = ae.add_element(StreamFunction(0, 10, Vec2D(.25, .25), Vec2D(.5, .5),
    #                                   main_fig, cylinder_stream_function))

    ae.browse()

    #ae.render('test2', 5)
