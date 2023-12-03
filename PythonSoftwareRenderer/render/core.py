import numpy as np
import math

# -------------------- Math Module --------------------
# -------------------- Vector --------------------

class Vec2D:
    __slots__ = "x", "y", "arr"

    def __init__(self, *args):
        if(len(args) == 2):
            arr_value = args
        self.arr = np.array(arr_value, dtype= np.float32)
        self.x = self.arr[0]
        self.y = self.arr[1]

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
        self.arr = np.array(arr_value, dtype = np.float32)
        self.x = self.arr[0]
        self.y = self.arr[1]
        self.z = self.arr[2]

    def __sub__(self, other):
        return 
# -------------------- Matrix --------------------
class Mat4D:
    def __init__(self, NArray = None, Value = None):
        if(Value):
            self.value = Value
        else:
            self.value = np.matrix(NArray)

    def __mul__(self, other):
        return self.__class__(Value = self.value * other.value)
    
class Vec4D(Mat4D):
    def __init__(self, *narr, value=None):
        if value is not None:
            self.value = value
        elif len(narr) == 1 and isinstance(narr[0], Mat4D):
            self.value = narr[0].value
        else:
            assert len(narr) == 4
            self.value = np.matrix([[d] for d in narr])

        self.x, self.y, self.z, self.w = (
            self.value[0, 0],
            self.value[1, 0],
            self.value[2, 0],
            self.value[3, 0],
        )
        self.arr = self.value.reshape((1, 4))
#-------------------- Math Functions --------------------
def normalize(Vec3D):
    length = math.sqrt(pow(Vec3D.x, 2) + pow(Vec3D.y, 2) + pow(Vec3D.z, 2))
    Vec3D.x = Vec3D.x / length
    Vec3D.y = Vec3D.y / length
    Vec3D.z = Vec3D.z / length

    return Vec3D

def dot(v1 : Vec3D, v2 : Vec3D):
    result = Vec3D(v1.arr.dot(v2.arr.dot))
    
    return result

def cross(v1 : Vec3D, v2 : Vec3D):
    result = Vec3D(np.cross(v1.arr, v2.arr))
    
    return result

#-------------------- Drawing Module --------------------
#-------------------- Drawing Func --------------------
def draw_triangle(v1, v2, v3, canvas, color):
