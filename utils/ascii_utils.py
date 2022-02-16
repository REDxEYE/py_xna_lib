class AsciiParser:
    def __init__(self, lines):
        self.offset = 0
        self.lines = lines  # type:list
        for i in range(len(self.lines)):
            if '#' in self.lines[i]:
                self.lines[i] = self.lines[i].split('#')[0]

    def next_line(self, offset=0):
        return self.lines[self.offset + offset]

    def next_vector(self, offset=0):
        return self.next_line(offset).split()

    def __bool__(self):
        return self.offset < len(self.lines)

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
