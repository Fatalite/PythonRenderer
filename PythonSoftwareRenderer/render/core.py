import numpy as np
import math

# -------------------- Math Module --------------------
# -------------------- Vector --------------------

class Vec2D:
    __slots__ = "x", "y", "arr"

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], Vec3D):
            self.arr = Vec3D.narr
        else:
            assert len(args) == 2
            self.arr = list(args)

        self.x, self.y = [d if isinstance(d, int) else int(d + 0.5) for d in self.arr]
    def __truediv__(self, other):
        return (self.y - other.y) / (self.x - other.x)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

class Vec3D:
    __slots__ = "x", "y", "z", "arr"
    
    def __init__(self, *args):
        if(len(args) == 1 and isinstance(args[0], Vec4D)):
            arr_value = (args[0].x, args[0].y, args[0].z)
        else:
            assert len(args) == 3
            arr_value = args
        self.arr = np.array(arr_value, dtype = np.float64)
        self.x, self.y, self.z = self.arr

    def __repr__(self):
        return repr(f"Vec3d({','.join([repr(d) for d in self.arr])})")

    def __sub__(self, other):
        return self.__class__(*[ds - do for ds, do in zip(self.arr, other.arr)])

    def __bool__(self):
        """ False for zero vector (0, 0, 0)
        """
        return any(self.arr)

# -------------------- Matrix --------------------
class Mat4D:
    def __init__(self, narr=None, Value=None):
        self.Value = np.matrix(narr) if Value is None else Value

    def __mul__(self, other):
        return self.__class__(Value = self.Value * other.Value)
    
class Vec4D(Mat4D):
    def __init__(self, *narr, Value=None):
        if Value is not None:
            self.Value = Value
        elif len(narr) == 1 and isinstance(narr[0], Mat4D):
            self.Value = narr[0].Value
        else:
            assert len(narr) == 4
            self.Value = np.matrix([[d] for d in narr])

        self.x, self.y, self.z, self.w = (
            self.Value[0, 0],
            self.Value[1, 0],
            self.Value[2, 0],
            self.Value[3, 0],
        )
        self.arr = self.Value.reshape((1, 4))
#-------------------- Math Functions --------------------
def normalize(Vec3D):
    length = math.sqrt(pow(Vec3D.x, 2) + pow(Vec3D.y, 2) + pow(Vec3D.z, 2))
    Vec3D.x = Vec3D.x / length
    Vec3D.y = Vec3D.y / length
    Vec3D.z = Vec3D.z / length

    return Vec3D

def dot(v1 : Vec3D, v2 : Vec3D):
    result = v1.x * v2.x + v1.y * v2.y + v1.z * v2.z
    return result

def cross(v1 : Vec3D, v2 : Vec3D):
    x = v1.y * v2.z - v1.z * v2.y
    y = v1.z * v2.x - v1.x * v2.z
    z = v1.x * v2.y - v1.y * v2.x 
    result = Vec3D(x, y, z)
    
    return result


