import numpy
from PIL import Image
from .core import Vec3D, Vec2D, Vec4D

# References
# https://en.wikipedia.org/wiki/Wavefront_.obj_file

class Model:
    def __init__(self, obj_address, texture_address):
        self.vertices = []
        self.indices = []
        self.uv_vertices = []
        self.uv_indices = []

        ModelFile = open(obj_address, "r")

        #Read Each Line
        for line in ModelFile.readlines():
            #Vertice Data
            if (line.startswith('v ')):
                data_of_list = []
                for data in line.split(" "):
                    if data.startswith('v'): continue
                    data_of_list.append(float(data))
                self.vertices.append(Vec4D(data_of_list[0], data_of_list[1], data_of_list[2],1))

            #UV Coordinate Data
            elif(line.startswith('vt ')):
                 u, v = [float(d) for d in line.strip("vt").strip().split(" ")]
                 self.uv_vertices.append([u, v])
                
            #Face Data
            elif(line.startswith('f ')):
                data_of_list = line.split(" ")
                indice = []
                uv_indice = []
                for datas in data_of_list:
                    
                    if datas.startswith('f'): continue
                    else:
                        indice.append(int(datas.split("/")[0]))
                        if(len(datas.split("/")) >= 2):
                            uv_indice.append(int(datas.split("/")[1]))

                self.indices.append(indice)
                self.uv_indices.append(uv_indice)


        #Read Texture and Store Texture
        #TextureFile = Image.open(texture_address)
        #self.texture = TextureFile

        #Close File
        ModelFile.close()
        #TextureFile.close()



