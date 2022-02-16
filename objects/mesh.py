class Mesh:
    def __init__(self, name, uv_layers_count):
        self.name = name
        self.vertices = []
        self.normals = []
        self.vertex_colors = []
        self.uv_layers = {i: [] for i in range(uv_layers_count)}
        self.weights = []
        self.bone_ids = []
        self.indices = []
        self.material = None

    def set_material(self, material):
        self.material = material

    def add_polygon(self, indices):
        self.indices.append(indices)

    def add_vertex(self, pos):
        self.vertices.append(pos)

    def add_normal(self, normal):
        self.normals.append(normal)

    def add_v_color(self, color):
        self.vertex_colors.append([c / 255 for c in color])

    def add_uv(self, uv, layer_id):
        self.uv_layers[layer_id].append((uv[0], uv[1]))

    def add_weight(self, bone_ids, weights):
        self.bone_ids.append(bone_ids)
        self.weights.append(weights)

    def __repr__(self):
        return 'Mesh(name=%r, vertices=%i, polygons=%i)' % (self.name, len(self.vertices), len(self.indices))
