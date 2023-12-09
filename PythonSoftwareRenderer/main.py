from render import model, camera, core, scene

# External Module
# Numpy : for fast array 
# PIL : for Canvas 

# 소스코드는 다음을 참고해서 작성함
# https://github.com/tvytlx/render-py

# 사용된 모델 출처
# http://kunzhou.net/tex-models.htm

# Model을 불러준다.
ModelInstance = model.Model("obj/lowpoly_bunny.obj", "texture/oriental_bunny.jpg")

CameraInstance = camera.Camera(core.Vec3D(-1, -2,0), core.Vec3D(0,0,0), core.Vec3D(0,-1,0))

SceneInstance = scene.Scene(CameraInstance, ModelInstance)

SceneInstance.render("outputs/output.png")