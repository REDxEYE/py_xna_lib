class Material:
    def __init__(self, name, textures):
        self.name = name
        self.textures = textures  # dict[str,tuple[str,int]]

    def add_texture(self, semantic, texture, uv_layer):
        if semantic in self.textures:
            print('Same semantic (%s) used multiple times' % semantic)
        self.textures[semantic] = texture, uv_layer
