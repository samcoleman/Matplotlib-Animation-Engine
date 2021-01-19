from AnimationElement import AnimationElement
from myMaths import Vec2D


class Figure2DElement(AnimationElement):
    def __init__(self, start: float, duration: float, position: Vec2D,
                 main_fig):
        super().__init__(start, duration, position)
        self._main_fig = main_fig

    def _inset(self):
        self._axes = self._main_fig.add_axes([0.1, 0.1, 0.8, 0.8], label='2D', anchor='C', projection='rectilinear')

    def _style(self):
        self._axes.patch.set_alpha(0)
        self._axes.spines["top"].set_color('white')
        self._axes.spines["bottom"].set_color('white')
        self._axes.spines["left"].set_color('white')
        self._axes.spines["right"].set_color('white')
        self._axes.tick_params(axis='x', colors='white')
        self._axes.set_xlabel("x-label", color="white")
        self._axes.tick_params(axis='y', colors='white')
        self._axes.set_xlabel("y-label", color="white")

    def _instantiate(self):
        self._inset()
        self._style()
        try:
            x, y = self.fn(0)
            self._my_plot, = self._axes.plot(x, y, color='white')
        except Exception as detail:
            print("Error:", detail)
        self._axes.set_axis_on()
        return 0

    def fn(self, p):
        raise Exception("Figure Function Not Implemented")

    def _update(self, progress):
        try:
            x, y = self.fn(progress)
            self._my_plot.set_data(x, y)
        except Exception as detail:
            print("Error:", detail)
        return 0

    def _cleanup(self):
        self._axes.remove()
        return 0


class Figure3DElement(AnimationElement):
    def __init__(self, start: float, duration: float, position: Vec2D,
                 main_fig):
        super().__init__(start, duration, position)
        self._fig = main_fig

    def _inset(self):
        self._axes = self._fig.add_axes([0.1, 0.1, 0.8, 0.8], label='3D', anchor='C', projection='3d')

    def _style(self):
        self._axes.patch.set_alpha(0)

    def _instantiate(self):
        self._inset()
        self._style()
        self._axes.set_xlim(-2, 2)
        self._axes.set_ylim(-2, 2)
        self._axes.set_zlim(-2, 2)
        try:
            x, y, z = self.fn(0)
            self._my_plot = self._axes.plot_wireframe(x, y, z)
        except Exception as detail:
            print("Error:", detail)
        self._axes.set_axis_on()
        return 0

    def fn(self, p):
        raise Exception("Figure Function Not Implemented")

    def _update(self, progress):
        try:
            x, y, z = self.fn(progress)
            #self._my_plot = self._axes.plot_wireframe(x, y, z)
        except Exception as detail:
            print("Error:", detail)
        self._axes.view_init(elev=30., azim=progress*360)
        self._axes.set_anchor((0.5+progress/2, 0.5))
        self._axes.set_xlim(-2+progress, 2-progress)
        self._axes.set_ylim(-2+progress, 2-progress)
        self._axes.set_zlim(-2+progress, 2-progress)
        return 0

    def _cleanup(self):
        self._axes.remove()
        return 0
