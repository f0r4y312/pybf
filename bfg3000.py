class BrainFuck(object):
    INIT_MEM = {
        16: (
            '++++[>++++[>++[>+>>++>>+++>>++++<<<<<<<-]+[>>+++>>+++++>>+++++++<<<<<<-]<-]<-]',
            [0, 0, 0, 32, 48, 64, 80, 96, 112, 128]
        ),
        32: (
            '++++[>++++[>++[>+>++>+++>++++<<<<-]<-]<-]',
            [0, 0, 0, 32, 64, 96, 128],
        ),
        31: (
            '++++[>++++[>++[>+>>++>>+++>>++++<<<<<<<-]<-]<-]',
            [0, 0, 0, 32, 0, 64, 0, 96, 0, 128],
        ),
    }

    def __init__(self, mem_type):
        self.init, mem = self.INIT_MEM[mem_type]
        self.mem = mem[:]
        self.cur_p = 0

    def build(self, sz):
        generated_code = [self.init]
        for c in map(ord, sz):
            c = self.lookup_symbol(c)
            _, code = self.compile(c)
            generated_code.append(code)
        return generated_code

    def lookup_symbol(self, c):
        min_i, min_d = 0, 256
        for i, d in enumerate(map(lambda m: c - m, self.mem)):
            if abs(d) < abs(min_d):
                min_i, min_d = i, d
        return (min_i, min_d)

    def compile(self, c):
        segment, offset = c
        ascii = chr(self.mem[segment] + offset)
        if offset >= 0:
            code = ('+' * offset) + '.' + ('-' * offset)
        else:
            offset = -offset
            code = ('-' * offset) + '.' + ('+' * offset)
        if segment >= self.cur_p:
            code = ('>' * (segment - self.cur_p)) + code
        else:
            code = ('<' * (self.cur_p - segment)) + code
        self.cur_p = segment
        return ascii, code


if __name__ == '__main__':
    bf_compiler = BrainFuck(32)
    for bf_code in bf_compiler.build('Hello World!'):
        print bf_code
