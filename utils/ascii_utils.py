class AsciiParser:
    def __init__(self, lines):
        self.offset = 0
        self.lines = lines  # type:list
        for i in range(len(self.lines)):
            if '#' in self.lines[i]:
                self.lines[i] = self.lines[i].split('#')[0]

    def peek_line(self, offset=0):
        return self.lines[self.offset + offset].strip()

    @property
    def line_preview(self):
        return self.peek_line()

    def peek_vector(self, offset=0):
        if offset + self.offset > len(self.lines):
            return []
        return self.peek_line(offset).split()

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
        val = map(float, self.peek_line().split(' '))
        self.offset += 1
        return list(val)

    def parse_int_vector(self):
        val = map(int, self.peek_line().split(' '))
        self.offset += 1
        return list(val)
