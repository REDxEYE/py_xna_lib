"""Everything here should be compatible with python 3.2 and up
As Noesis uses python 3.2
"""
import os

from .objects.bone import Bone
from .objects.material import Material
from .objects.mesh import Mesh
from .objects.model import Model
from .utils.ascii_utils import AsciiParser


def parse_ascii_mesh_from_file(path, external_skeleton=False):
    assert os.path.exists(path), 'Specified path "%s" does not exist' % path
    with open(path, 'r', encoding='utf8') as f:
        file_lines = [line.strip('\n\r') for line in f.read().split('\n') if line]
    return parse_ascii_mesh(file_lines, external_skeleton)


def parse_ascii_mesh(file_lines, external_skeleton=False):
    reader = AsciiParser(file_lines)
    model = Model()
    try:
        bone_count = reader.parse_int()
        if bone_count == 0:
            reader.parse_int()
        else:
            assert len(reader.next_vector(2)) >= 3
        reader.offset = 0
    except (AssertionError, ValueError):
        reader.lines.insert(0, 0)
        reader.offset = 0
    for _ in range(reader.parse_int()):
        bone_name = reader.parse_string()
        bone_parent = reader.parse_int()
        bone_mat = reader.parse_float_vector()
        bone = Bone(bone_name, bone_parent, bone_mat[:3], bone_mat[3:])
        model.add_bone(bone)
        del bone_name
        del bone_parent
        del bone_mat
        del bone
    if external_skeleton and model.bones:
        raise Exception('Unexpected state, we have external skeleton and internal skeleton')
    has_bones = bool(model.bones) or external_skeleton
    if not reader:  # Exit early if we don't have mesh data
        return model
    for _ in range(reader.parse_int()):
        mesh = Mesh(reader.parse_string(), reader.parse_int())
        textures = [(reader.parse_string(), reader.parse_int()) for _ in range(reader.parse_int())]
        if textures:
            material = Material(textures[0][0] + '_mat', textures)
            mesh.set_material(material)
        vertex_count = reader.parse_int()
        vertex_data_size = 0
        while len(reader.next_vector(vertex_data_size)) != 1 and reader:
            vertex_data_size += 1
        assert vertex_data_size % vertex_count == 0
        vertex_stride = vertex_data_size // vertex_count
        for _ in range(vertex_count):
            mesh.vertices.append(reader.parse_float_vector())
            mesh.normals.append(reader.parse_float_vector())
            mesh.add_v_color(reader.parse_int_vector())
            for uv_layer_id in mesh.uv_layers.keys():
                mesh.add_uv(reader.parse_float_vector(), uv_layer_id)
            if has_bones or vertex_stride - len(mesh.uv_layers) > 3:
                bone_ids = reader.parse_int_vector()
                weights = reader.parse_float_vector()
                mesh.add_weight(bone_ids, weights)
        for _ in range(reader.parse_int()):
            mesh.add_polygon(reader.parse_int_vector())
        model.add_mesh(mesh)
    return model
