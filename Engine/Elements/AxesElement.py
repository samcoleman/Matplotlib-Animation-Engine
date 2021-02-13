from Engine.Elements.AnimationElement import AnimationElement
from Engine.Keyframe.Transform import *
from Engine.Theme import Theme

from matplotlib.pyplot import Axes as Ax
from mpl_toolkits.mplot3d import Axes3D

from typing import Union


class AxesData:
    axes_on = True
    xlim = [-1, 1]
    ylim = [-1, 1]
    zlim = [-1, 1]
    invert_xaxis = False
    invert_yaxis = False
    invert_zaxis = False
    xlabel = " "
    ylabel = " "
    zlabel = " "
    title = ""
    xscale = "linear"
    yscale = "linear"
    zscale = "linear"
    autoscale = False
    aspect = 'auto'
    minorticks = False
    projection = 'rectilinear'

    def __init__(self, **kwargs):
        members = [attr for attr in dir(AxesData) if not
                   callable(getattr(AxesData, attr)) and not attr.startswith("__")]

        for key, value in kwargs.items():
            if key in members:
                setattr(self, key, value)

    def apply(self, axes: Union[Ax, Axes3D]):
        if self.axes_on:
            axes.set_axis_on()
        else:
            axes.set_axis_off()

        axes.set_xlim(self.xlim[0], self.xlim[1])
        axes.set_ylim(self.ylim[0], self.ylim[1])

        if self.invert_xaxis:
            axes.invert_xaxis()

        if self.invert_yaxis:
            axes.invert_yaxis()

        axes.set_xlabel(self.xlabel)
        axes.set_ylabel(self.ylabel)
        axes.set_title(self.title)
        axes.set_xscale(self.xscale)
        axes.set_yscale(self.yscale)
        axes.autoscale(self.autoscale)

        if type(axes) is Ax:
            if self.minorticks:
                axes.minorticks_on()
            else:
                axes.minorticks_off()

            axes.set_aspect(self.aspect)

        if type(axes) is Axes3D:
            axes.set_zlim(self.zlim[0], self.zlim[1])
            axes.set_zlabel(self.zlabel)
            axes.set_zscale(self.zscale)

            if self.invert_zaxis:
                axes.invert_zaxis()


class AxesStyle:
    facecolor = Theme.color.primary
    alpha = 0
    spine_color = Theme.color.text
    tickline_color = Theme.color.text
    ticklabel_color = Theme.color.text

    def __init__(self, **kwargs):
        members = [attr for attr in dir(AxesData) if not
                   callable(getattr(AxesData, attr)) and not attr.startswith("__")]

        for key, value in kwargs.items():
            if key in members:
                setattr(self, key, value)

    def apply(self, axes: Union[Ax, Axes3D]):
        axes.patch.set_alpha(self.alpha)
        axes.tick_params('both', color=Theme.color.text, labelcolor=Theme.color.text)

        [s.set_color(self.spine_color) for s in axes.spines.values()]


class AxesElement(AnimationElement):
    def __init__(self, start: float, duration: float, position: Vec2D, size: Vec2D,
                 main_fig, label, axes_data: AxesData = AxesData(), axes_style: AxesStyle = AxesStyle()):
        super().__init__(start, duration, position)
        self._size = size
        self._main_fig = main_fig
        self.label = label
        self.axes_data = axes_data
        self.axes_style = axes_style

    def _inset(self):
        self._axes = self._main_fig.add_axes([self._position.x, self._position.y, self._size.x, self._size.y],
                                             label=self.label, anchor='C', projection=self.axes_data.projection)
        self.axes_data.apply(self._axes)

    def _style(self):
        self.axes_style.apply(self._axes)
        """
        self._axes.patch.set_alpha(0)
        self._axes.spines["top"].set_color('white')
        self._axes.spines["bottom"].set_color('white')
        self._axes.spines["left"].set_color('white')
        self._axes.spines["right"].set_color('white')
        self._axes.tick_params(axis='x', colors='white')
        self._axes.set_xlabel("x-label", color="white")
        self._axes.tick_params(axis='y', colors='white')
        self._axes.set_ylabel("y-label", color="white")
        """

    def _instantiate(self):
        self._inset()
        self._style()
        self._keyframeMng.attach_handle(self._axes)
        try:
            return self._init()
        except Exception as detail:
            print("Error:", detail)
        return 0

    def _init(self):
        raise Exception("Figure Init Not Implemented")

    def _update(self, p):
        self._keyframeMng.update(p)
        try:
            return self._refresh(p)
        except Exception as detail:
            print("Error:", detail)
        return 0

    def _refresh(self, p):
        raise Exception("Figure Refresh Not Implemented")

    def _cleanup(self):
        self._axes.remove()
        return 0
