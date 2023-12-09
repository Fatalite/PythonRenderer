from PIL import Image, ImageColor
from render import core
from copy import deepcopy
import typing as t

def get_light_intensity(face) -> float:
    light = core.Vec3D(-2, 4, 0)
    v1, v2, v3 = face
    up = core.normalize(core.cross(v2 - v1, v3 - v1))
    return core.dot(up, core.normalize(light))

class Scene:
    def __init__(self, camera, *objects):
        self.camera = camera
        self.objects = objects

    def render(self, file_path):
        
        ### MVP
        ## Model Transformation
        model_mat = core.Mat4D([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
        
        ## View Transformation
        # z
        facing_vec = core.normalize(self.camera.target - self.camera.eye)
        # y
        right_vec = core.normalize(core.cross(self.camera.up, facing_vec))
        # x
        other_vec = core.cross(facing_vec, right_vec) #정규화 되어있는 두 벡터의 외적이므로 정규화할 필요 없음
        # 
        rot_mat = core.Mat4D(
            [
             [right_vec.x, right_vec.y, right_vec.z, 0], 
             [other_vec.x, other_vec.y, other_vec.z, 0], 
             [facing_vec.x, facing_vec.y, facing_vec.z, 0], 
             [0, 0, 0, 1.0]
            ]
        )

        trans_mat = core.Mat4D(
            [
                [1, 0, 0, -self.camera.eye.x], 
                [0, 1, 0, -self.camera.eye.y], 
                [0, 0, 1, -self.camera.eye.z], 
                [0, 0, 0, 1.0]
            ]
        )

        view_mat = core.Mat4D(Value=(rot_mat * trans_mat).Value)
        ## Projection Transformation
        near = 5
        far = 1000

        projection_mat = core.Mat4D(
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
                world_vertices.append(core.Vec4D(world_vertex))
                mvp_vertex = projection_mat * view_mat * world_vertex
                #NDC
                mvp_vertex = mvp_vertex.Value
                w = mvp_vertex[3, 0]
                x, y, z = mvp_vertex[0, 0] / w, mvp_vertex[1, 0] / w, mvp_vertex[2, 0] / w
                ndc_vertex = core.Mat4D([[x], [y], [z], [1 / w]])
                #Viewport
                x = y = 0
                w, h = 1920,1080
                n, f = 3, 1000
                screen_vertex = core.Vec3D(w * 0.5 * ndc_vertex.Value[0, 0] + x + w * 0.5,h * 0.5 * ndc_vertex.Value[1, 0] + y + h * 0.5,
                                        0.5 * (f - n) * ndc_vertex.Value[2, 0] + 0.5 * (f + n),)
                screen_vertices.append(screen_vertex)

        render_img = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0))

        def draw( dots, color: t.Union[tuple, str]):
            if isinstance(color, str):
                color = ImageColor.getrgb(color)
            if isinstance(dots, tuple):
                dots = [dots]
            for dot in dots:
                #print(dot)
                #if(dot[0] >= 0 and dot[1] >= 0):
                    #if(dot[0] < 400 and dot[1] <= 400):
                render_img.putpixel(dot, color + (255,))

        def draw_line(v1, v2, color: t.Union[tuple, str] = "white"):
            v1, v2 = deepcopy(v1), deepcopy(v2)
            if v1 == v2:
                draw((v1.x, v1.y), color=color)
                return
            
            steep = abs(v1.y - v2.y) > abs(v1.x - v2.x)
            if steep:
                v1.x, v1.y = v1.y, v1.x
                v2.x, v2.y = v2.y, v2.x
            v1, v2 = (v1, v2) if v1.x < v2.x else (v2, v1)
            slope = abs((v1.y - v2.y) / (v1.x - v2.x))
            y = v1.y
            error: float = 0
            incr = 1 if v1.y < v2.y else -1
            dots = []
            for x in range(int(v1.x), int(v2.x + 0.5)):
                dots.append((int(y), x) if steep else (x, int(y)))
                error += slope
                if abs(error) >= 0.5:
                    y += incr
                    error -= 1

            draw(dots, color=color)
        
        def draw_triangle(v1, v2, v3, color, wireframe=False):
            if wireframe:
                draw_line(v1, v2)
                draw_line(v2, v3)
                draw_line(v1, v3)
                return
            def sort_vertices_asc_by_y(vertices):
                return sorted(vertices, key=lambda v: v.y)

            def fill_bottom_flat_triangle(v1, v2, v3):
                invslope1 = (v2.x - v1.x) / (v2.y - v1.y)
                invslope2 = (v3.x - v1.x) / (v3.y - v1.y)

                x1 = x2 = v1.x
                y = v1.y

                while y <= v2.y:
                    draw_line(core.Vec2D(x1, y), core.Vec2D(x2, y), color)
                    x1 += invslope1
                    x2 += invslope2
                    y += 1

            def fill_top_flat_triangle(v1, v2, v3):
                invslope1 = (v3.x - v1.x) / (v3.y - v1.y)
                invslope2 = (v3.x - v2.x) / (v3.y - v2.y)

                x1 = x2 = v3.x
                y = v3.y

                while y > v2.y:
                    draw_line(core.Vec2D(x1, y), core.Vec2D(x2, y), color)
                    x1 -= invslope1
                    x2 -= invslope2
                    y -= 1

            v1, v2, v3 = sort_vertices_asc_by_y((v1, v2, v3))

            if v1.y == v2.y == v3.y:
                pass
            elif v2.y == v3.y:
                fill_bottom_flat_triangle(v1, v2, v3)
            elif v1.y == v2.y:
                fill_top_flat_triangle(v1, v2, v3)
            else:
                v4 = core.Vec2D(int(v1.x + (v2.y - v1.y) / (v3.y - v1.y) * (v3.x - v1.x)), v2.y)
                fill_bottom_flat_triangle(v1, v2, v4)
                fill_top_flat_triangle(v2, v4, v3)

        print(len(world_vertices))
        print(len(screen_vertices))

        
        for obj in self.objects:
            for triangle_indices in obj.indices:
                vertex_group = [screen_vertices[idx - 1] for idx in triangle_indices]
                face = [core.Vec3D(world_vertices[idx - 1]) for idx in triangle_indices]   
                intensity = get_light_intensity(face)
                #if intensity >= 0:
                    #draw_triangle(*vertex_group, color=(int(intensity * 255),) * 3)
                draw_triangle(*vertex_group, color="black", wireframe= True)
                

        render_img.save(file_path)