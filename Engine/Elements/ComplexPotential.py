from Engine.Elements.AxesElement import AxesElement, AxesData, AxesStyle
import numpy as np
import numpy.ma as ma
from Engine.MathsHelpers import Vec2D
from matplotlib.collections import LineCollection

import sympy
from sympy.abc import x, y, z
from scipy import integrate

from Engine.Theme import Theme


def ode_scipy(f, pts, dt):
    new_pts = [integrate.odeint(f, xy, [0, dt])[-1] for xy in pts]
    return new_pts


# Joukowski transformation
def Jac(_z, lam):
    return _z+(lam**2)/_z


def Circle(c, a):
    t = np.linspace(0, 2*np.pi, 200)
    return c + a*np.exp(1j*t)


# Must be F(z)
# Returns sf (stream-function), u (x velocity function), v (y velocity function)
def lambda_complex_potential(F):
    sf = sympy.lambdify(z, sympy.im(F), 'numpy')

    dF_dz = sympy.diff(F, z)
    # Needs to be in terms of x and y as odeint cannot use complex values
    dF_dz = dF_dz.subs(z, x + y*1j)
    # Negative as dF/dz = u - iv
    u = sympy.lambdify((x, y), sympy.re(dF_dz), 'numpy')
    v = sympy.lambdify((x, y), -sympy.im(dF_dz), 'numpy')

    return sf, u, v


def displace_func_from_velocity_funcs(u_func, v_func):
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


class ComplexPotential(AxesElement):
    def __init__(self, position: Vec2D, size: Vec2D,
                 complex_potential, levels, body=None, mask=lambda pos: False,
                 axes_data: AxesData = AxesData(), axes_style: AxesStyle = AxesStyle()):

        super(ComplexPotential, self).__init__(position, size, 'sf', axes_data, axes_style)
        self._cp = complex_potential
        self._levels = levels
        self._body = body
        self._mask = mask

    def _contour_plot(self, temp=False):
        if not temp:
            return self._axes.contour(self.Z.real, self.Z.imag, self.SF(self.Z), levels=self._levels, colors=Theme.color.text,
                                      linewidths=1, linestyles='solid')
        else:
            tmp = self._main_fig.add_axes([0, 0, 1, 1],
                                          label="tmp", anchor='C', projection=self.axes_data.projection)
            cp = tmp.contour(self.Z.real, self.Z.imag, self.SF(self.Z), levels=self._levels, colors=Theme.color.text,
                             linewidths=1, linestyles='solid')
            tmp.remove()
            return cp

    def _velocity_plot(self):
        start_points = []

        cp = self._contour_plot(True)
        # This function gets all the start points for velocity plot from the temporary contour plot
        for line in cp.collections:
            paths = line.get_paths()
            if len(paths) == 0:
                continue

            for path in paths:
                start_points.append(path.vertices[0])

        # From start points, integrate until streamline leaves bounds or becomes stationary
        thresh = 0.0001
        sx, sy = [], []
        for point in start_points:
            xs = [point[0]]
            ys = [point[1]]
            while True:

                new_pt = self.displace([[xs[-1], ys[-1]]], 0.05)[0]

                if (not (self.axes_data.xlim[0]*1.2 < new_pt[0] and new_pt[0] < self.axes_data.xlim[1]*1.2) or
                        (not (self.axes_data.ylim[0]*1.2 < new_pt[1] and new_pt[1] < self.axes_data.ylim[1]*1.2))):
                    break
                elif ((new_pt[0] - xs[-1]) < thresh) and ((new_pt[1] - ys[-1]) < thresh):
                    break

                xs.append(new_pt[0])
                ys.append(new_pt[1])

            sx.append(xs)
            sy.append(ys)

        # Make a pretty plot of the streamlines
        self.lengths = []
        self.colors = []
        self.lines = []

        for xs, ys in zip(sx, sy):
            points = np.array([xs, ys]).T.reshape(-1, 1, 2)
            segments = np.concatenate([points[:-1], points[1:]], axis=1)
            n = len(segments)

            D = np.sqrt(((points[1:] - points[:-1]) ** 2).sum(axis=-1))
            D.fill(.1)
            L = D.cumsum().reshape(n, 1)  # + np.random.uniform(0, 1)
            C = np.ones((n, 4))
            C[:, [3]] = (L * 1.5) % 1

            line = LineCollection(segments, color=C, linewidth=0.5)
            self.lengths.append(L)
            self.colors.append(C)
            self.lines.append(line)

            self._axes.add_collection(line)

    def _body_plot(self):
        if self._body is not None:
            self._axes.plot(self._body.real, self._body.imag, color=Theme.color.text)

    def _instantiate(self):
        X = np.arange(self.axes_data.xlim[0]*1.1, self.axes_data.xlim[1]*1.1, 0.025)
        Y = np.arange(self.axes_data.ylim[0]*1.1, self.axes_data.ylim[1]*1.1, 0.025)
        X, Y = np.meshgrid(X, Y)
        self.Z = X + 1j * Y
        self.Z = ma.masked_where(self._mask(self.Z), self.Z)

        self.SF, self.u, self.v = lambda_complex_potential(self._cp)
        self.displace = displace_func_from_velocity_funcs(self.u, self.v)

        self._velocity_plot()
        self._body_plot()

    def _update(self, progress: float, duration: float):
        self._axes.set_xlim(-3 + progress, 3 - progress)
        self._axes.set_ylim(-3 + progress, 3 - progress)

        for i in range(len(self.lines)):
            self.lengths[i] -= 0.05
            self.colors[i][:, [3]] = (self.lengths[i] * 1.5) % 1
            self.lines[i].set_color(self.colors[i])


class JoukowskiAerofoil(ComplexPotential):
    def __init__(self, position: Vec2D, size: Vec2D,
                 levels,
                 axes_data: AxesData = AxesData(), axes_style: AxesStyle = AxesStyle()):

        super(JoukowskiAerofoil, self).__init__(position, size, 'sf', axes_data, axes_style)
        self._levels = levels

    def _contour_plot(self, temp=False):
        if not temp:
            return self._axes.contour(self.J.real, self.J.imag, self.SF(self.Zc), levels=self._levels, colors=Theme.color.text,
                                      linewidths=1, linestyles='solid')
        else:
            tmp = self._main_fig.add_axes([0, 0, 1, 1],
                                          label="tmp", anchor='C', projection=self.axes_data.projection)
            cp = tmp.contour(self.J.real, self.J.imag, self.SF(self.Zc), levels=self._levels, colors=Theme.color.text,
                             linewidths=1, linestyles='solid')
            tmp.remove()
            return cp

    def _instantiate(self):
        # Why is this needed?

        self.axes_data = AxesData(xlim=[-3, 3], ylim=[-3, 3], aspect='equal')
        self.axes_data.apply(self._axes)
        U = 1
        a = 1
        c = .1
        alpha = 0  # 2*np.pi/16
        beta = 0  # .1

        lam = a / (a + c)
        c_centre = lam - a * np.exp(-1j * beta)

        X = np.arange(self.axes_data.xlim[0] * 1.1, self.axes_data.xlim[1] * 1.1, 0.025)
        Y = np.arange(self.axes_data.ylim[0] * 1.1, self.axes_data.ylim[1] * 1.1, 0.025)
        X, Y = np.meshgrid(X, Y)
        Z = X + 1j * Y
        Z = ma.masked_where(np.absolute(Z - c_centre) <= a, Z)
        self.Zc = Z - c_centre

        self.J = Jac(Z, lam)

        C = Circle(c_centre, a)
        self._body = Jac(C, lam)

        gamma = -4*np.pi*U*a*np.sin(beta+alpha) #Circulation
        # Stagnation flow
        # F = 0.5 * (z**2)
        F = U * z * sympy.exp(-1j * alpha) + \
            U * (a ** 2) * sympy.exp(1j * alpha) / z - \
            1j * gamma * sympy.ln(z) / (2 * np.pi)

        self.SF, self.u, self.v = lambda_complex_potential(F)
        self.displace = displace_func_from_velocity_funcs(self.u, self.v)

        self._contour_plot()
        self._body_plot()

    def _update(self, progress: float, duration: float):
        for i in range(len(self.lines)):
            self.lengths[i] -= 0.05
            self.colors[i][:, [3]] = (self.lengths[i] * 1.5) % 1
            self.lines[i].set_color(self.colors[i])
