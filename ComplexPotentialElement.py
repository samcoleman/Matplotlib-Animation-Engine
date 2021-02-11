from FigureElements import AxesElement
import numpy as np
import numpy.ma as ma
from myMaths import Vec2D
from matplotlib.collections import LineCollection

import sympy
from sympy.abc import x, y, z
from scipy import integrate


def ode_scipy(f, pts, dt):
    new_pts = [integrate.odeint(f, xy, [0, dt])[-1] for xy in pts]
    return new_pts


# Joukowski transformation
def Jouk(_z, lam):
    return _z+(lam**2)/_z


def Circle(C, a):
    t=np.linspace(0, 2*np.pi, 200)
    return C + a*np.exp(1j*t)

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


class ComplexPotentialElement(AxesElement):
    def __init__(self, start: float, duration: float, position: Vec2D, size: Vec2D, mf, complex_potential):
        super(ComplexPotentialElement, self).__init__(start, duration, position, size, mf, 'sf', 'rectilinear')
        self._cp = complex_potential

    def _init(self):

        w = 3

        U = 1
        a = 1
        c = .1
        alpha = 0#2*np.pi/16
        beta = 0#.1

        lam = a / (a + c)
        c_centre = lam - a * np.exp(-1j * beta)

        X = np.arange(-3.2, 3.2, 0.025)
        Y = np.arange(-3.2, 3.2, 0.025)
        X, Y = np.meshgrid(X, Y)
        Z = X + 1j * Y
        Z = ma.masked_where(np.absolute(Z-c_centre) <= a, Z)
        Zc = Z - c_centre

        J = Jouk(Z, lam)

        C = circle(c_centre, a)
        Aerofoil = Juc(C, lam)

        gamma = -4*np.pi*U*a*np.sin(beta+alpha)#circulation
        # Stagnation flow
        # F = 0.5 * (z**2)
        F = U * z * sympy.exp(-1j * alpha) + \
            U * (a ** 2) * sympy.exp(1j * alpha) / z - \
            1j * gamma * sympy.ln(z) / (2 * np.pi)

        SF, u, v = lambda_complex_potential(F)

        self.displace = displace_func_from_velocity_funcs(u, v)

        levels = np.arange(-2.8, 4.8, 0.2).tolist()

        #self._axes.plot(C.real, C.imag, color='white')
        #cp = self._axes.contour(Z.real, Z.imag, SF(Zc), levels=levels, colors='white', linewidths=1,
        #                        linestyles='solid')  # this means that the flow is evaluated at Juc(z) since c_flow(Z)=C_flow(csi(Z))

        tmp = self._main_fig.add_axes([0, 0, 1, 1],
                                             label="tmp", anchor='C', projection=self.projection)
        cp = tmp.contour(J.real, J.imag, SF(Zc), levels=levels, colors='white', linewidths=1,
                linestyles='solid')# this means that the flow is evaluated at Juc(z) since c_flow(Z)=C_flow(csi(Z))
        tmp.remove()

        self._axes.set_xlim(-w, w)
        self._axes.set_ylim(-w, w)
        self._axes.set_aspect("equal")
        self._axes.plot(Aerofoil.real, Aerofoil.imag, color='white')

        start_points = []

        self.lengths = []
        self.colors = []
        self.lines = []
        for line in cp.collections:
            paths = line.get_paths()
            if len(paths) == 0:
                continue

            for path in paths:
                start_points.append(path.vertices[0])

        def out_of_bounds(line, xlim, ylim):
            outside_xlim = (line[:, 0] < xlim[0]) | (line[:, 0] > xlim[1])
            outside_ylim = (line[:, 1] < ylim[0]) | (line[:, 1] > ylim[1])

            if outside_xlim | outside_ylim:
                return True

            return False

        def stationary(line, e=0.001):
            print(line[-1, 0])
            dispx = line[-1, 0] - line[-2, 0]
            dispy = line[-1, 1] - line[-2, 1]

            if dispx**2 + dispy**2 < e**2:
                return True

            return False

        thresh = 0.00001
        sx, sy = [], []
        for point in start_points:
            xs = [point[0]]
            ys = [point[1]]
            while True:

                new_pt = self.displace([[xs[-1], ys[-1]]], 0.05)[0]

                if (not (-3.5 < new_pt[0] and new_pt[0] < 3.5) or (not (-3.5 < new_pt[1] and new_pt[1] < 3.5))):
                    break
                elif ((new_pt[0] - xs[-1]) < thresh) and ((new_pt[1] - ys[-1]) < thresh):
                    break

                xs.append(new_pt[0])
                ys.append(new_pt[1])

            sx.append(xs)
            sy.append(ys)

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

            # linewidths = np.zeros(n)
            # linewidths[:] = 1.5 - ((L.reshape(n)*1.5) % 1)

            # line = LineCollection(segments, color=colors, linewidth=linewidths)
            line = LineCollection(segments, color=C, linewidth=0.5)
            self.lengths.append(L)
            self.colors.append(C)
            self.lines.append(line)

            self._axes.add_collection(line)

        #self._my_plot = self._axes.streamplot(Zm.real, Zm.imag, u(Zm.real, Zm.imag), v(Zm.real, Zm.imag), color='white')



    def _refresh(self, p):
        for i in range(len(self.lines)):
            self.lengths[i] -= 0.05
            self.colors[i][:, [3]] = (self.lengths[i] * 1.5) % 1
            self.lines[i].set_color(self.colors[i])



