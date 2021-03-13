from Engine.AnimationEngine import AnimationEngine
from Engine.Elements.GraphElements import Sine, Cube
from Engine.Elements.AxesElement import AxesData
from Engine.MathsHelpers import Vec2D

ae = AnimationEngine(1080, 24)

Sine = ae.add_element(Sine(Vec2D(.11, .33), Vec2D(.33, .33), axes_data=AxesData(xlim=[-3, 3], ylim=[-3, 3], aspect='equal')),
                      2, 10)

Cube = ae.add_element(Cube(Vec2D(.5, .33), Vec2D(.33, .33), axes_data=AxesData(xlim=[-2, 2], ylim=[-2, 2], zlim=[-2, 2], aspect='equal')),
                      2, 10)

ae.browse(10)
