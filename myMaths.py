'''
Simple class for 3D vectors.
Requires: Python 2.5 and numpy 1.0.4

(c) Ilan Schnell, 2008
'''
import numpy
import math

"""
class Vec2D:
    # Constructor creates a vector from components x and y
    def __init__(self, x, y):
        self.x = x
        self.y = y

    # self is this instance of Vec2D, other is another instance.

    def __add__(self, other):
        return Vec2D(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vec2D(self.x - other.x, self.y - other.y)

    # dot product,

    def __mul__(self, other):
        return self.x*other.x + self.y*other.y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return '(%g, %g)' % (self.x, self.y)

    def __repr__(self):
        return '(%g, %g)' % (self.x, self.y)

    def __abs__(self):
        return math.sqrt(self.x**2 + self.y**2)

    def __ne__(self, other):
        return not self.__eq__(other)  # reuse __eq__a
"""


_TINY = 1e-15


def _xyzto012(c):
    if c in 'xyz':
        return ord(c) - ord('x')
    else:
        raise AttributeError("vec3 instance has no attribute '%s'" % c)


def _xyto01(c):
    if c in 'xy':
        return ord(c) - ord('x')
    else:
        raise AttributeError("vec3 instance has no attribute '%s'" % c)


def _args2tuple2D(funcname, args):
    narg = len(args)
    if narg == 0:
        data = 2 * (0,)
    elif narg == 1:
        data = args[0]
        if len(data) != 2:
            raise TypeError('vec3.%s() takes sequence with 2 elements '
                            '(%d given),\n\t   when 1 argument is given' %
                            (funcname, len(data)))
    elif narg == 2:
        data = args
    else:
        raise TypeError('vec3.%s() takes 0, 1 or 2 arguments (%d given)' %
                        (funcname, narg))
    assert len(data) == 2
    try:
        return tuple(map(float, data))
    except (TypeError, ValueError):
        raise TypeError("vec3.%s() can't convert elements to float" % funcname)


def _args2tuple3D(funcname, args):
    narg = len(args)
    if narg == 0:
        data = 3 * (0,)
    elif narg == 1:
        data = args[0]
        if len(data) != 3:
            raise TypeError('vec3.%s() takes sequence with 3 elements '
                            '(%d given),\n\t   when 1 argument is given' %
                            (funcname, len(data)))
    elif narg == 3:
        data = args
    else:
        raise TypeError('vec3.%s() takes 0, 1 or 3 arguments (%d given)' %
                        (funcname, narg))
    assert len(data) == 3
    try:
        return tuple(map(float, data))
    except (TypeError, ValueError):
        raise TypeError("vec3.%s() can't convert elements to float" % funcname)

class Vec2D(numpy.ndarray):
    def __new__(cls, *args):
        if len(args) == 1:
            if isinstance(args[0], Vec2D):
                return args[0].copy()
            if isinstance(args[0], numpy.matrix):
                return Vec2D(args[0].flatten().tolist()[0])
        data = _args2tuple2D('__new__', args)
        arr = numpy.array(data, dtype=numpy.float, copy=True)
        return numpy.ndarray.__new__(cls, shape=(2,), buffer=arr)

    def __repr__(self):
        return 'vec3' + repr(tuple(self))

    def __mul__(self, other):
        return numpy.dot(self, other)

    def __abs__(self):
        return math.sqrt(self * self)

    def __pow__(self, x):
        return (self * self) if x == 2 else pow(abs(self), x)

    def __eq__(self, other):
        return abs(self - other) < _TINY

    def __ne__(self, other):
        return not self == other

    def __getattr__(self, name):
        return self[_xyto01(name)]

    def __setattr__(self, name, val):
        self[_xyto01(name)] = val


class Vec3D(numpy.ndarray):
    def __new__(cls, *args):
        if len(args) == 1:
            if isinstance(args[0], Vec3D):
                return args[0].copy()
            if isinstance(args[0], numpy.matrix):
                return Vec3D(args[0].flatten().tolist()[0])
        data = _args2tuple3D('__new__', args)
        arr = numpy.array(data, dtype=numpy.float, copy=True)
        return numpy.ndarray.__new__(cls, shape=(3,), buffer=arr)

    def __repr__(self):
        return 'vec3' + repr(tuple(self))

    def __mul__(self, other):
        return numpy.dot(self, other)

    def __abs__(self):
        return math.sqrt(self * self)

    def __pow__(self, x):
        return (self * self) if x == 2 else pow(abs(self), x)

    def __eq__(self, other):
        return abs(self - other) < _TINY

    def __ne__(self, other):
        return not self == other

    def __getattr__(self, name):
        return self[_xyzto012(name)]

    def __setattr__(self, name, val):
        self[_xyzto012(name)] = val

    def get_spherical(self):
        r = abs(self)
        if r < _TINY:
            theta = phi = 0.0
        else:
            x, y, z = self
            theta = math.acos(z / r)
            phi = math.atan2(y, x)

        return r, theta, phi

    def set_spherical(self, *args):
        r, theta, phi = _args2tuple3D('set_spherical', args)
        self[0] = r * math.sin(theta) * math.cos(phi)
        self[1] = r * math.sin(theta) * math.sin(phi)
        self[2] = r * math.cos(theta)

    def get_cylindrical(self):
        x, y, z = self
        rho = math.sqrt(x * x + y * y)
        phi = math.atan2(y, x)
        return rho, phi, z

    def set_cylindrical(self, *args):
        rho, phi, z = _args2tuple3D('set_cylindrical', args)
        self[0] = rho * math.cos(phi)
        self[1] = rho * math.sin(phi)
        self[2] = z


def cross(a, b):
    return Vec3D(numpy.cross(a, b))
