from render import model

# External Module
# Numpy : for fast array 
# PIL : for Canvas 

# 소스코드는 다음을 참고해서 작성함
# https://github.com/tvytlx/render-py

# 사용된 모델 출처
# http://kunzhou.net/tex-models.htm

# Model을 불러준다.
ModelInstance = model.Model("obj/bunny.obj", "texture/oriental_bunny.jpg")

for v in (ModelInstance.uv_indices): 
    print(v.x)
    print(v.y)
    print(v.z)

