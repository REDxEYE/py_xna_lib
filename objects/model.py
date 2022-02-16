from .bone import Bone
from .mesh import Mesh


class Model:
    def __init__(self):
        self.bones = []  # type: list[Bone]
        self.meshes = []  # type: list[Mesh]

    def add_bone(self, bone):
        self.bones.append(bone)

    def add_mesh(self, mesh):
        self.meshes.append(mesh)
