from FigureElements import FigureElement
import numpy as np
from myMaths import Vec2D

from matplotlib.patches import Circle

import sympy
from sympy.abc import x, y
from scipy import integrate

from Transform import Sequence


class Cube(FigureElement):
    def __init__(self, start: float, duration: float, position: Vec2D, size: Vec2D, mf):
        super(Cube, self).__init__(start, duration, position, size, mf, '3d', '3d')

        phi = np.arange(1, 10, 2) * np.pi / 4
        self.Phi, self.Theta = np.meshgrid(phi, phi)
        self.x = np.cos(self.Phi) * np.sin(self.Theta)
        self.y = np.sin(self.Phi) * np.sin(self.Theta)
        self.z = np.cos(self.Theta) / np.sqrt(2)

    def _init(self):
        self._axes.set_xlim(-2, 2)
        self._axes.set_ylim(-2, 2)
        self._axes.set_zlim(-2, 2)
        self._my_plot = self._axes.plot_wireframe(self.x, self.y, self.z)
        self._axes.set_axis_off()

    def _refresh(self, p):
        self._axes.view_init(elev=30., azim=p * 360)
        self._axes.set_anchor((0.5 + p / 2, 0.5))
        self._axes.set_xlim(-2 + p, 2 - p)
        self._axes.set_ylim(-2 + p, 2 - p)
        self._axes.set_zlim(-2 + p, 2 - p)


class Sine(FigureElement):
    def __init__(self, start: float, duration: float, position: Vec2D, size: Vec2D, mf):
        super(Sine, self).__init__(start, duration, position, size, mf, 'rect', 'rectilinear')
        self.x = np.arange(0.0, 2.0, 0.01)

    def _style(self):
        super(Sine, self)._style()
        self._axes.spines["bottom"].set_color('red')

    def _init(self):
        self._my_plot, = self._axes.plot(self.x, 1 + np.sin(self.x), color='white')

    def _refresh(self, p):
        print("update")
        self._my_plot.set_data(self.x, 1 + np.sin(self.x - p))


def random_y(ylim):
    yrange = np.diff(ylim)
    return yrange * np.random.rand(1)[0] + ylim[0]


def ode_scipy(f, pts, dt):
    new_pts = [integrate.odeint(f, xy, [0, dt])[-1] for xy in pts]
    return new_pts

def remove_particles(pts, xlim, ylim):
    if len(pts) == 0:
        return []
    outside_xlim = (pts[:, 0] < xlim[0]) | (pts[:, 0] > xlim[1])
    outside_ylim = (pts[:, 1] < ylim[0]) | (pts[:, 1] > ylim[1])
    keep = ~(outside_xlim|outside_ylim)
    return pts[keep]


def displace_func_from_velocity_funcs(u_func, v_func, method='rk4'):
    """Return function that calculates particle positions after time step.

    Parameters
    ----------
    u_func, v_func : functions
        Velocity fields which return velocities at arbitrary coordinates.
    """
    def velocity(xy, t=0):
        """Return (u, v) velocities for given (x, y) coordinates."""
        # Dummy `t` variable required to work with integrators
        # Must return a list (not a tuple) for scipy's integrate functions.
        return [u_func(*xy), v_func(*xy)]

    def displace(xy, dt):
        return ode_scipy(velocity, xy, dt)

    return displace


class StreamFunction(FigureElement):
    def __init__(self, start: float, duration: float, position: Vec2D, size: Vec2D, mf, sf, ax_s: Sequence = None):
        super(StreamFunction, self).__init__(start, duration, position, size, mf, 'sf', 'rectilinear', ax_s)
        self.sf = sf

    def _init(self):
        w = 3

        phi = self.sf()

        u, v = self._velocity_field(phi)

        Y, X = np.mgrid[-w:w:100j, -w:w:100j]

        self.displace = displace_func_from_velocity_funcs(u, v)

        self._axes.set_xlim(-w, w)
        self._axes.set_xlim(-w, w)

        self.pts = np.linspace((-3, -3), (-3, 3), 31)

        thresh = 0.00001
        xs, ys = [], []
        for p in self.pts:
            x = [p[0]]
            y = [p[1]]
            while True:
                new_pt = self.displace([[x[-1], y[-1]]], 0.05)[0]
                if (not (-3 < new_pt[0] and new_pt[0] < 3) or (not (-3 < new_pt[1] and new_pt[1] < 3))):
                    x.append(new_pt[0])
                    y.append(new_pt[1])
                    break
                elif ((new_pt[0] - x[-1]) < thresh) and ((new_pt[1] - y[-1]) < thresh):
                    x.append(new_pt[0])
                    y.append(new_pt[1])
                    break

                x.append(new_pt[0])
                y.append(new_pt[1])

            xs.append(x)
            ys.append(y)

        for x, y in zip(xs, ys):
            self._axes.plot(x, y, color="white")

        self._axes.add_patch(Circle((0, 0), radius=1, edgecolor="white", facecolor='w', linewidth=1))
        self._axes.set_aspect("equal", "datalim")

        self.p = []

    @staticmethod
    def _velocity_field(psi):
        u = sympy.lambdify((x, y), psi.diff(y), 'numpy')
        v = sympy.lambdify((x, y), -psi.diff(x), 'numpy')
        return u, v

    def _refresh(self, p):
        """Update locations of "particles" in flow on each frame frame """
        self.p = list(self.p)
        self.p.append((-3, random_y((-3, 3))))
        self.p = self.displace(self.p, 0.05)
        self.p = np.asarray(self.p)
        self.p = remove_particles(self.p, (-3, 3), (-3, 3))

        x, y = np.asarray(self.p).transpose()
        lines, = self._axes.plot(x, y, 'ro')



