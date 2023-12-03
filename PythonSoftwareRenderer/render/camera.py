import core 


class Camera:
    def __init__(self, eye, target, up):
        self.up = up
        self.eye = eye 
        self.target = target