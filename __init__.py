"""Everything here should be compatible with python 3.2 and up
As Noesis uses python 3.2
"""
import os

from .objects.bone import Bone
from .objects.material import Material
from .objects.mesh import Mesh
from .objects.model import Model
from .utils import get_quaternion_from_euler
from .utils.ascii_utils import AsciiParser


def parse_ascii_mesh_from_file(path, external_skeleton=False):
    assert os.path.exists(path), 'Specified path "%s" does not exist' % path
    with open(path, 'r', encoding='utf8') as f:
        file_lines = [line.strip('\n\r') for line in f.read().split('\n') if line]
    return parse_ascii_mesh(file_lines, external_skeleton)


def parse_ascii_mesh(file_lines, external_skeleton=False):
    ts = {
        0: 'Diffuse',
        1: 'Normal',
        2: 'Spec',
    }

    reader = AsciiParser(file_lines)
    model = Model()
    try:
        bone_count = reader.parse_int()
        if bone_count == 0:
            reader.parse_int()
        else:
            assert len(reader.peek_vector(2)) >= 3
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
        print('WARNING: we have external skeleton and internal skeleton')
    has_bones = bool(model.bones) or external_skeleton
    if not reader:  # Exit early if we don't have mesh data
        return model
    for _ in range(reader.parse_int()):
        mesh = Mesh(reader.parse_string(), reader.parse_int())
        textures = [(reader.parse_string(), reader.parse_int()) for _ in range(reader.parse_int())]
        if textures:
            stextures = {ts.get(i, 's_%i' % i): t for (i, t) in enumerate(textures)}
            material = Material(mesh.name, stextures)
            mesh.set_material(material)
        vertex_count = reader.parse_int()
        vertex_data_size = 0
        while len(reader.peek_vector(vertex_data_size)) != 1 and reader:
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


def parse_ascii_material_from_file(path):
    assert os.path.exists(path), 'Specified path "%s" does not exist' % path
    with open(path, 'r', encoding='utf8') as f:
        file_lines = [line.strip('\n\r') for line in f.read().split('\n') if line]
    return parse_ascii_material(file_lines, os.path.splitext(os.path.basename(path))[0])


def parse_ascii_material(file_lines, file_name):
    reader = AsciiParser(file_lines)
    material = Material(file_name, {})
    while reader:
        line = reader.parse_string()
        semantic, texture_and_uv = line.split('=')
        texture, uv = texture_and_uv.split(' ')
        material.add_texture(semantic, texture, uv)
    return material


def parse_smd_bones_from_file(path):
    assert os.path.exists(path), 'Specified path "%s" does not exist' % path
    with open(path, 'r', encoding='utf8') as f:
        file_lines = [line.strip('\n\r') for line in f.read().split('\n') if line]
    return parse_smd_bones(file_lines)


def parse_smd_bones(file_lines):
    reader = AsciiParser(file_lines)

    version = reader.parse_string()
    _, version = version.split(' ')
    assert version == '1'
    bones = []
    tmp_bones = {}  # bone_id[name, parent]
    animations = {}  # frame[bone_id,[pos,rot]]
    while reader:
        keyword = reader.parse_string()
        if keyword == 'nodes':
            while True:
                bone_string = reader.parse_string()
                if bone_string == 'end':
                    break
                bone_id, bone_string = bone_string.split(' ', 1)
                bone_name, bone_parent = bone_string.rsplit(' ', 1)
                bone_id = int(bone_id)
                bone_parent = int(bone_parent)
                bone_name = bone_name.strip('"')
                tmp_bones[bone_id] = bone_name, bone_parent
                del bone_name, bone_id, bone_parent, bone_string
        elif keyword == 'skeleton':
            while True:
                frame_string = reader.parse_string()
                if frame_string == 'end':
                    break
                _, frame = frame_string.split(' ')
                frame = int(frame)
                animations[frame] = {}
                for bone_id, (bone_name, bone_parent) in tmp_bones.items():
                    bone_string = [s for s in reader.parse_string().split(' ') if s]
                    bone_id2 = int(bone_string.pop(0))
                    assert bone_id2 == bone_id, 'Invalid bone order'
                    pos = [float(a) for a in bone_string[:3]]
                    rot = [float(a) for a in bone_string[3:]]

                    bone = Bone(bone_name, bone_parent, pos, get_quaternion_from_euler(*rot))
                    bones.append(bone)
        elif keyword == 'triangles':
            while True:
                string = reader.parse_string()
                if string == 'end':
                    break
        elif keyword == 'vertexanimation':
            while True:
                string = reader.parse_string()
                if string == 'end':
                    break
    return bones


def parse_string_from_file(path):
    assert os.path.exists(path), 'Specified path "%s" does not exist' % path
    with open(path, 'r', encoding='utf8') as f:
        file_lines = [line.strip('\n\r') for line in f.read().split('\n') if line]
    return parse_string_names(file_lines)


def parse_string_names(file_lines):
    remap = {}
    for line in file_lines:
        name_hash, bone_name = line.split('=')
        name_hash = name_hash.strip(' ')
        bone_name = bone_name.strip(' ').rstrip(' ')
        remap[name_hash] = bone_name
    return remap
