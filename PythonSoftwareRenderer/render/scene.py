from PIL import Image
from core import Mat4D, normalize, cross
from camera import Camera
class Scene:
    def __init__(self, camera, *objects):
        self.camera = camera
        self.objects = objects

    def render(self, file_path):
        
        ### MVP
        ## Model Transformation
        model_mat = Mat4D([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
        
        ## View Transformation
        # z
        facing_vec = normalize(self.camera.target - self.camera.eye)
        # y
        right_vec = normalize(cross(self.camera.up, facing_vec))
        # x
        other_vec = cross(facing_vec, right_vec) #정규화 되어있는 두 벡터의 외적이므로 정규화할 필요 없음
        # 
        rot_mat = Mat4D(
            [
             [l.x, l.y, l.z, 0], 
             [u.x, u.y, u.z, 0], 
             [f.x, f.y, f.z, 0], 
             [0, 0, 0, 1.0]
            ]
        )

        trans_mat = Mat4D(
            [
                [1, 0, 0, -self.camera.eye.x]
            ]
        )

        view_mat = rot_mat * trans_mat

        ## Projection Transformation
        near = 1
        far = 1000

        world_vertices = []