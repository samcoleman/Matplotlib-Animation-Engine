from Engine.AnimationEngine import AnimationEngine
from Engine.Elements.ComplexPotential import *
from Engine.Elements.AxesElement import AxesData
from Engine.MathsHelpers import Vec2D


def cylinder_stream_function(U=1, R=1):
    r = sympy.sqrt(x ** 2 + y ** 2)
    theta = sympy.atan2(y, x)
    return U * (r - R ** 2 / r) * sympy.sin(theta)


ae = AnimationEngine(1080, 24)

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

cp = ae.add_element(ComplexPotential(Vec2D(.11, .33), Vec2D(.33, .33),
                                     F, levels, C, lambda Z: np.absolute(Z) <= a,
                                     axes_data=AxesData(xlim=[-3, 3], ylim=[-3, 3], aspect='equal')),
                    0, 10)

# Not working?
"""
jk = ae.add_element(JoukowskiAerofoil(Vec2D(.5, .33), Vec2D(.33, .33),
                                      levels,
                                      axes_data=AxesData(xlim=[-3, 3], ylim=[-3, 3], aspect='equal')),
                    0, 10)
"""

ae.browse(10)
