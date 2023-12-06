from PIL import Image
from core import Mat4D, normalize, cross, Vec4D, Vec3D
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
             [right_vec.x, right_vec.y, right_vec.z, 0], 
             [other_vec.x, other_vec.y, other_vec.z, 0], 
             [facing_vec.x, facing_vec.y, facing_vec.z, 0], 
             [0, 0, 0, 1.0]
            ]
        )

        trans_mat = Mat4D(
            [
                [1, 0, 0, -self.camera.eye.x], 
                [0, 1, 0, -self.camera.eye.y], 
                [0, 0, 1, -self.camera.eye.z], 
                [0, 0, 0, 1.0]
            ]
        )

        view_mat = rot_mat * trans_mat

        ## Projection Transformation
        near = 3
        far = 1000

        projection_mat = Mat4D(
        [
            [near / 0.5, 0, 0, 0],
            [0, near / 0.5, 0, 0],
            [0, 0, -(far + near) / (far - near), (-2 * far * near) / (far - near)],
            [0, 0, -1, 0],
        ])

        world_vertices = []

        screen_vertices = []

        for object in self.objects:
            for v in object.vertices:
                #MVP
                world_vertex = model_mat * v
                world_vertices.append(Vec4D(world_vertex))
                mvp_vertex = projection_mat * view_mat * world_vertex

                #NDC
                mvp_vertex = mvp_vertex.value
                w = mvp_vertex[3, 0]
                x, y, z = mvp_vertex[0, 0] / w, mvp_vertex[1, 0] / w, mvp_vertex[2, 0] / w
                ndc_vertex = Mat4D([[x], [y], [z], [1 / w]])

                #Viewport
                x = y = 0
                w, h = 800, 600
                n, f = 3, 1000
                screen_vertex = Vec3D(w * 0.5 * v.value[0, 0] + x + w * 0.5, h * 0.5 * v.value[1, 0] + y + h * 0.5, 0.5 * (f - n) * v.value[2, 0] + 0.5 * (f + n),
                
                screen_vertices.append(screen_vertex)