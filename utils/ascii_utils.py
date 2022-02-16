class AsciiParser:
    def __init__(self, lines):
        self.lines = lines  # type:list

    def parse_int(self):
        return int(self.lines.pop(0))

    def parse_float(self):
        return float(self.lines.pop(0))

    def parse_string(self):
        return self.lines.pop(0)

    def parse_float_vector(self):
        return [float(v) for v in self.lines.pop(0).split(' ')]

    def parse_int_vector(self):
        return [float(v) for v in self.lines.pop(0).split(' ')]
