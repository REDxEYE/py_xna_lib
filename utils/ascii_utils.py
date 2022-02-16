class AsciiParser:
    def __init__(self, lines):
        self.offset = 0
        self.lines = lines  # type:list

    def parse_int(self):
        val = int(self.lines[self.offset])
        self.offset += 1
        return val

    def parse_float(self):
        val = float(self.lines[self.offset])
        self.offset += 1
        return val

    def parse_string(self):
        val = self.lines[self.offset]
        self.offset += 1
        return val

    def parse_float_vector(self):
        val = [float(v) for v in self.lines[self.offset].split(' ')]
        self.offset += 1
        return val

    def parse_int_vector(self):
        val = [int(v) for v in self.lines[self.offset].split(' ')]
        self.offset += 1
        return val
