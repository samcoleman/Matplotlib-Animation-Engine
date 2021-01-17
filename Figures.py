import numpy as np
import matplotlib.pyplot as plt


class FigureObj:
    def __init__(self, main_fig):
        self._main_fig = main_fig

        # Create blank axes and plot
        self._axes = plt.axes([0, 0, 1, 1])
        self._my_plot = self._axes.plot([], [])
        self.hide_axes()

    def hide_axes(self):
        self._axes.set_axis_off()

    def show_axes(self):
        self._axes.set_axis_on()

    def _inset(self):
        return 0

    def _style(self):
        return 0

    def plot(self):
        self._inset()
        self._style()
        try:
            return self._plot()
        except Exception as detail:
            print("Error:", detail)
        return None

    def _plot(self):
        raise Exception("Figure Plot Not Implemented")

    def update(self, progress):
        self._update()

    def _update(self, progress):
        return 0

    def cleanup(self):
        self._axes.remove()


class FigureObj2D(FigureObj):
    def __init__(self, main_fig, fn):
        FigureObj.__init__(self, main_fig)

        # Data for plotting
        self.t = np.arange(0.0, 2.0, 0.01)
        self.fn = fn

    def _inset(self):
        self._axes = self._main_fig.add_axes([0.1, 0.1, 0.8, 0.8], anchor='C', projection='rectilinear')

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

    def _plot(self):
        self._my_plot, = self._axes.plot(self.t, self.fn(self.t, 0), color='white')
        self.show_axes()
        print("\nplot")

    def update(self, progress):
        self._my_plot.set_data(self.t, self.fn(self.t, progress))


def get_cube():
    phi = np.arange(1,10,2)*np.pi/4
    Phi, Theta = np.meshgrid(phi, phi)

    x = np.cos(Phi)*np.sin(Theta)
    y = np.sin(Phi)*np.sin(Theta)
    z = np.cos(Theta)/np.sqrt(2)
    return x,y,z


class FigureObj3D(FigureObj):
    def __init__(self, main_fig):
        FigureObj.__init__(self, main_fig)
        self._fig = main_fig

        self.x, self.y, self.z = get_cube()

    def _inset(self):
        self._axes = self._fig.add_axes([0.1, 0.1, 0.8, 0.8], anchor='C', projection='3d')

    def _style(self):
        self._axes.patch.set_alpha(0)

    def _plot(self):
        self._axes.set_xlim(-2, 2)
        self._axes.set_ylim(-2, 2)
        self._axes.set_zlim(-2, 2)
        self._my_plot = self._axes.plot_wireframe(self.x, self.y, self.z)
        self.hide_axes()

    def update(self, progress):
        self._axes.view_init(elev=30., azim=progress*360)
        self._axes.set_anchor((0.5+progress/2, 0.5))
        self._axes.set_xlim(-2+progress, 2-progress)
        self._axes.set_ylim(-2+progress, 2-progress)
        self._axes.set_zlim(-2+progress, 2-progress)
        return 0
