from math import atan2, sqrt, degrees, radians, cos, sin
from random import randint

class Documentation():
    """Used to add documentation to Vector2D and Vector3D classes"""

    def random_pos():
        """
        Returns a Vector that will have a random postition within the specified range

        2D
            Vector2D(10, 10) --> x,y between 0, 10
            Vector2D(10, 10, 5, 5) --> x,y between 5, 10

        3D
            Vector2D(10, 10, 10) --> x,y,z between 0, 10
            Vector2D(10, 10, 10, 5, 5, 5) --> x,y,z between 5, 10
        """

    def random_unit():
        """
        Returns a random unit Vector
        """

    def from_angle():
        """
        Generate a unit vector from an angle that will have a heading towards that angle
        """

    def dist():
        """
        Returns the distance between this vector and another (or tuple/list)

        vec.dist(other_vec) --> distance between vec and other_vec
        vec.dist([0, 5]) --> distance between vec and the x0y5 position
        """

    def set():
        """
        sets the Vectors x,y,(z) parameters
        """

    def get():
        """
        Returns a list containing the vectors position
        """

    def get_heading_angle():
        """
        returns angle offset from the x axis
        """

    def copy():
        """
        Returns an identical copy of this vector
        """

    def get_magnitude():
        """
        returns the magnitude of this vector
        """

    def normalise():
        """
        Normalises this vector to make its magnitude 1
        """

    def normalize():
        """
        Normalizes this vector to make its magnitude 1
        """

class Vector2D(Documentation):
    def __init__(self, *args):
        if len(args) == 0:
            self.x = 0
            self.y = 0
        elif len(args) == 1:
            if type(args) in [list, tuple]:
                self.x = args[0][0]
                self.y = args[0][1]
            else:
                self.x = args[0]
                self.y = args[0]
        elif len(args) == 2:
            self.x = args[0]
            self.y = args[1]

        self.data = {}

    #region automatic creation methods

    def random_pos(max_x, max_y, min_x=0, min_y=0):
        return Vector2D(randint(min_x, max_x), randint(min_y, max_y))

    def random_unit():
        vec = Vector2D.random_pos(100000, 100000)
        vec.normalise()
        return vec

    def from_angle(angle, mode='deg'):
        if mode == 'deg':
            x = cos(radians(angle))
            y = sin(radians(angle))
        if mode == 'rad':
            x = cos(angle)
            y = sin(angle)

        return Vector2D(x, y)

    #endregion

    #region custom other methods

    def dist(self, other, use_sqrt=True):
        d = 0
        if type(other) == Vector2D:
            d = (other.x - self.x)**2 + (other.y - self.y)**2
        if type(other) in [tuple, list]:
            d = (other[0] - self.x)**2 + (other[1] - self.y)**2

        if use_sqrt : return sqrt(d)
        else : return d

    def set(self, *args):
        if len(args) == 0:
            self.x = 0
            self.y = 0
        elif len(args) == 1:
            if type(args) in [list, tuple]:
                self.x = args[0][0]
                self.y = args[0][1]
            else:
                self.x = args[0]
                self.y = args[0]
        elif len(args) == 2:
            self.x = args[0]
            self.y = args[1]

    def get(self, mode=int):
        return [mode(self.x), mode(self.y)]

    def get_heading_angle(self, mode='deg'):
        a = atan2(self.x, self.y)

        if mode == 'deg' : return degrees(a)
        if mode == 'rad' : return a

    def copy(self):
        return Vector2D(self.x, self.y)

    def get_magnitude(self):
        return sqrt(self.x**2 + self.y**2)

    def normalise(self):
        mag = self.get_magnitude()
        self.div(mag)
    def normalize(self):
        self.normalise()

    #endregion

    #region custom mathematical methods

    def add(self, *args):
        if len(args) == 1:
            if type(args[0]) in [int, float]:
                self.x += args[0]
                self.y += args[0]
            if type(args[0]) in [tuple, list]:
                self.x += args[0]
                self.y += args[1]
            if type(args[0]) == Vector2D:
                self.x += args[0].x
                self.y += args[0].y
        if len(args) == 2:
            if type(args[0]) in [int, float] and type(args[1]) in [int, float]:
                self.x += args[0]
                self.y += args[1]

    def sub(self, *args):
        if len(args) == 1:
            if type(args[0]) in [int, float]:
                self.x -= args[0]
                self.y -= args[0]
            if type(args[0]) in [tuple, list]:
                self.x -= args[0]
                self.y -= args[1]
            if type(args[0]) == Vector2D:
                self.x -= args[0].x
                self.y -= args[0].y
        if len(args) == 2:
            if type(args[0]) in [int, float] and type(args[1]) in [int, float]:
                self.x -= args[0]
                self.y -= args[1]

    def mult(self, *args):
        if len(args) == 1:
            if type(args[0]) in [int, float]:
                self.x *= args[0]
                self.y *= args[0]
            if type(args[0]) in [tuple, list]:
                self.x *= args[0]
                self.y *= args[1]
            if type(args[0]) == Vector2D:
                self.x *= args[0].x
                self.y *= args[0].y
        if len(args) == 2:
            if type(args[0]) in [int, float] and type(args[1]) in [int, float]:
                self.x *= args[0]
                self.y *= args[1]

    def div(self, *args):
        if len(args) == 1:
            if type(args[0]) in [int, float]:
                self.x /= args[0]
                self.y /= args[0]
            if type(args[0]) in [tuple, list]:
                self.x /= args[0]
                self.y /= args[1]
            if type(args[0]) == Vector2D:
                self.x /= args[0].x
                self.y /= args[0].y
        if len(args) == 2:
            if type(args[0]) in [int, float] and type(args[1]) in [int, float]:
                self.x /= args[0]
                self.y /= args[1]

    #endregion

    #region magic methods

    def __add__(self, *args):
        if len(args) == 1:
            if type(args[0]) in [int, float]:
                return Vector2D(self.x + args[0], self.y + args[0])
            if type(args[0]) in [tuple, list]:
                return Vector2D(self.x + args[0], self.y + args[1])
            if type(args[0]) == Vector2D:
                return Vector2D(self.x + args[0].x, self.y + args[0].y)
        if len(args) == 2:
            if type(args[0]) in [int, float] and type(args[1]) in [int, float]:
                return Vector2D(self.x + args[0], self.y + args[1])

    def __sub__(self, *args):
        if len(args) == 1:
            if type(args[0]) in [int, float]:
                return Vector2D(self.x - args[0], self.y - args[0])
            if type(args[0]) in [tuple, list]:
                return Vector2D(self.x - args[0], self.y - args[1])
            if type(args[0]) == Vector2D:
                return Vector2D(self.x - args[0].x, self.y - args[0].y)
        if len(args) == 2:
            if type(args[0]) in [int, float] and type(args[1]) in [int, float]:
                return Vector2D(self.x - args[0], self.y - args[1])

    def __mult__(self, *args):
        if len(args) == 1:
            if type(args[0]) in [int, float]:
                return Vector2D(self.x / args[0], self.y / args[0])
            if type(args[0]) in [tuple, list]:
                return Vector2D(self.x / args[0], self.y / args[1])
            if type(args[0]) == Vector2D:
                return Vector2D(self.x / args[0].x, self.y / args[0].y)
        if len(args) == 2:
            if type(args[0]) in [int, float] and type(args[1]) in [int, float]:
                return Vector2D(self.x / args[0], self.y / args[1])

    def __div__(self, *args):
        if len(args) == 1:
            if type(args[0]) in [int, float]:
                return Vector2D(self.x / args[0], self.y / args[0])
            if type(args[0]) in [tuple, list]:
                return Vector2D(self.x / args[0], self.y / args[1])
            if type(args[0]) == Vector2D:
                return Vector2D(self.x / args[0].x, self.y / args[0].y)
        if len(args) == 2:
            if type(args[0]) in [int, float] and type(args[1]) in [int, float]:
                return Vector2D(self.x / args[0], self.y / args[1])

    #endregion

class Vector3D(Documentation):
    def __init__(self, *args):
        if len(args) == 0:
            self.x = 0
            self.y = 0
            self.z = 0
        elif len(args) == 1:
            if type(args) in [list, tuple]:
                self.x = args[0][0]
                self.y = args[0][1]
                self.z = args[0][2]
            else:
                self.x = args[0]
                self.y = args[0]
                self.z = args[0]
        elif len(args) == 3:
            self.x = args[0]
            self.y = args[1]
            self.z = args[2]

        self.data = {}

    #region automatic creation methods

    def random_pos(max_x, max_y, max_z, min_x=0, min_y=0, min_z=0):
        return Vector3D(randint(min_x, max_x), randint(min_y, max_y), randint(min_z, max_z))

    def random_unit():
        vec = Vector2D.random_pos(100000, 100000)
        vec.normalise()
        return vec

    #endregion

    #region custom other methods

    def dist(self, other, use_sqrt=True):
        d = 0
        if type(other) == Vector3D:
            d = (other.x - self.x)**2 + (other.y - self.y)**2 + (other.z - self.z)**2
        if type(other) in [tuple, list]:
            d = (other[0] - self.x)**2 + (other[1] - self.y)**2 + (other[2] - self.z)**2

        if use_sqrt : return sqrt(d)
        else : return d

    def set(self, *args):
        if len(args) == 0:
            self.x = 0
            self.y = 0
            self.z = 0
        elif len(args) == 1:
            if type(args) in [list, tuple]:
                self.x = args[0][0]
                self.y = args[0][1]
                self.z = args[0][2]
            else:
                self.x = args[0]
                self.y = args[0]
                self.z = args[0]
        elif len(args) == 3:
            self.x = args[0]
            self.y = args[1]
            self.z = args[2]

    def get(self, mode=int):
        return [mode(self.x), mode(self.y), mode(self.z)]

    def copy(self):
        return Vector3D(self.x, self.y, self.z)

    def get_magnitude(self):
        return sqrt(self.x**2 + self.y**2 + self.z**2)

    def normalise(self):
        mag = self.get_magnitude()
        self.div(mag)
    def normalize(self):
        self.normalise()

    #endregion

    #region custom mathematical methods

    def add(self, *args):
        if len(args) == 1:
            if type(args[0]) in [int, float]:
                self.x += args[0]
                self.y += args[0]
                self.z += args[0]
            if type(args[0]) in [tuple, list]:
                self.x += args[0]
                self.y += args[1]
                self.z += args[2]
            if type(args[0]) == Vector3D:
                self.x += args[0].x
                self.y += args[0].y
                self.z += args[0].z
        if len(args) == 3:
            if type(args[0]) in [int, float] and type(args[1]) in [int, float] and type(args[2]) in [int, float]:
                self.x += args[0]
                self.y += args[1]
                self.z += args[2]

    def sub(self, *args):
        if len(args) == 1:
            if type(args[0]) in [int, float]:
                self.x -= args[0]
                self.y -= args[0]
                self.y -= args[0]
            if type(args[0]) in [tuple, list]:
                self.x -= args[0]
                self.y -= args[1]
                self.z -= args[2]
            if type(args[0]) == Vector3D:
                self.x -= args[0].x
                self.y -= args[0].y
                self.z -= args[0].z
        if len(args) == 3:
            if type(args[0]) in [int, float] and type(args[1]) in [int, float] and type(args[2]) in [int, float]:
                self.x -= args[0]
                self.y -= args[1]
                self.z -= args[2]

    def mult(self, *args):
        if len(args) == 1:
            if type(args[0]) in [int, float]:
                self.x *= args[0]
                self.y *= args[0]
                self.z *= args[0]
            if type(args[0]) in [tuple, list]:
                self.x *= args[0]
                self.y *= args[1]
                self.z *= args[2]
            if type(args[0]) == Vector3D:
                self.x *= args[0].x
                self.y *= args[0].y
                self.z *= args[0].z
        if len(args) == 3:
            if type(args[0]) in [int, float] and type(args[1]) in [int, float] and type(args[2]) in [int, float]:
                self.x *= args[0]
                self.y *= args[1]
                self.z *= args[2]

    def div(self, *args):
        if len(args) == 1:
            if type(args[0]) in [int, float]:
                self.x /= args[0]
                self.y /= args[0]
                self.z /= args[0]
            if type(args[0]) in [tuple, list]:
                self.x /= args[0]
                self.y /= args[1]
                self.z /= args[2]
            if type(args[0]) == Vector3D:
                self.x /= args[0].x
                self.y /= args[0].y
                self.z /= args[0].z
        if len(args) == 3:
            if type(args[0]) in [int, float] and type(args[1]) in [int, float] and type(args[2]) in [int, float]:
                self.x /= args[0]
                self.y /= args[1]
                self.z /= args[2]

    #endregion

    #region magic methods

    def __add__(self, *args):
        if len(args) == 1:
            if type(args[0]) in [int, float]:
                return Vector3D(self.x + args[0], self.y + args[0], self.z + args[0])
            if type(args[0]) in [tuple, list]:
                return Vector3D(self.x + args[0], self.y + args[1], self.z + args[2])
            if type(args[0]) == Vector3D:
                return Vector3D(self.x + args[0].x, self.y + args[0].y, self.z + args[0].z)
        if len(args) == 3:
            if type(args[0]) in [int, float] and type(args[1]) in [int, float] and type(args[2]) in [int, float]:
                return Vector3D(self.x + args[0], self.y + args[1], self.z + args[2])

    def __sub__(self, *args):
        if len(args) == 1:
            if type(args[0]) in [int, float]:
                return Vector3D(self.x - args[0], self.y - args[0], self.z - args[0])
            if type(args[0]) in [tuple, list]:
                return Vector3D(self.x - args[0], self.y - args[1], self.z - args[2])
            if type(args[0]) == Vector3D:
                return Vector3D(self.x - args[0].x, self.y - args[0].y, self.z - args[0].z)
        if len(args) == 3:
            if type(args[0]) in [int, float] and type(args[1]) in [int, float] and type(args[2]) in [int, float]:
                return Vector3D(self.x - args[0], self.y - args[1], self.z - args[2])

    def __mult__(self, *args):
        if len(args) == 1:
            if type(args[0]) in [int, float]:
                return Vector3D(self.x * args[0], self.y * args[0], self.z * args[0])
            if type(args[0]) in [tuple, list]:
                return Vector3D(self.x * args[0], self.y * args[1], self.z * args[2])
            if type(args[0]) == Vector3D:
                return Vector3D(self.x * args[0].x, self.y * args[0].y, self.z * args[0].z)
        if len(args) == 3:
            if type(args[0]) in [int, float] and type(args[1]) in [int, float] and type(args[2]) in [int, float]:
                return Vector3D(self.x * args[0], self.y * args[1], self.z * args[2])

    def __div__(self, *args):
        if len(args) == 1:
            if type(args[0]) in [int, float]:
                return Vector3D(self.x / args[0], self.y / args[0], self.z / args[0])
            if type(args[0]) in [tuple, list]:
                return Vector3D(self.x / args[0], self.y / args[1], self.z / args[2])
            if type(args[0]) == Vector3D:
                return Vector3D(self.x / args[0].x, self.y / args[0].y, self.z / args[0].z)
        if len(args) == 3:
            if type(args[0]) in [int, float] and type(args[1]) in [int, float] and type(args[2]) in [int, float]:
                return Vector3D(self.x / args[0], self.y / args[1], self.z / args[2])

    #endregion

