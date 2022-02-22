class Bone:
    def __init__(self, name, parent_id, pos, quat):
        self.name = name
        self.parent_id = parent_id
        self.pos = pos
        self.quat = quat

    @property
    def blender_pos(self):
        return self.pos[2], self.pos[0], self.pos[1]

    @property
    def blender_quat(self):
        return self.quat[3], self.quat[2], self.quat[0], self.quat[1]

    def __repr__(self):
        return 'Bone(name=%r, parent_id=%r, pos=%r, quat=%r)' % (self.name, self.parent_id, self.pos, self.quat)
