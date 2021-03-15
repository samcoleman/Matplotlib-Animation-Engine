from Engine.AnimationEngine import AnimationEngine
from Engine.Elements.TextElement import TextElement
from Engine.MathsHelpers import Vec2D

ae = AnimationEngine(1080, 24)

text = ae.add_element(TextElement(Vec2D(.5, .8), "Hello", 72,
                      horizontalalignment='center', verticalalignment='center', color='white'),
                      2, 10)

ae.browse(10)
