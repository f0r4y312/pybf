class BrainFuck(object):
    INIT_MEM = {
        '16Z': (
            '++++[>++++[>+[>+>>+++>>+++++>>+++++++<<<<<<<-]++[>>>>>>>>>+>>++>>+++>>++++<<<<<<<<<<<<<<<-]<-]<-]',
            [0, 0, 0, 16, 0, 48, 0, 80, 0, 112, 0, 32, 0, 64, 0, 96, 0, 128]
        ),
        '16C': (
            '++++[>++++[>++[>>+>>++>>+++>>++++<<<<<<<<-]+[>+>>+++>>+++++>>+++++++<<<<<<<-]<-]<-]',
            [0, 0, 0, 16, 32, 48, 64, 80, 96, 112, 128]
        ),
        '32Z': (
            '++++[>++++[>++[>+>>++>>+++>>++++<<<<<<<-]<-]<-]',
            [0, 0, 0, 32, 0, 64, 0, 96, 0, 128],
        ),
        '32C': (
            '++++[>++++[>++[>+>++>+++>++++<<<<-]<-]<-]',
            [0, 0, 0, 32, 64, 96, 128],
        ),
    }
    MAX_OP = 8
    LOOPS = 4

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
        generated_code.append(self.move_ptr(0))
        return generated_code

    def lookup_symbol(self, c):
        min_i, min_d = 0, 256
        for i, d in enumerate(map(lambda m: c - m, self.mem)):
            if abs(d) < abs(min_d):
                min_i, min_d = i, d
        return (min_i, min_d)

    def lookup_zero(self):
        zero_p = self.cur_p
        while zero_p and self.mem[zero_p]:
            zero_p -= 1
        return zero_p

    def move_ptr(self, target):
        if target >= self.cur_p:
            code = ('>' * (target - self.cur_p))
        else:
            code = ('<' * (self.cur_p - target))
        self.cur_p = target
        return code

    def compile(self, c):
        segment, offset = c
        # NOTE: move the pointer to the correct segment
        code = self.move_ptr(segment)
        # NOTE: modify the segment to the required char
        self.mem[segment] += offset
        ascii = chr(self.mem[segment])
        if offset >= 0:
            op = '+'
        else:
            op = '-'
            offset = -offset
        if offset > self.MAX_OP:
            loop = offset / self.LOOPS
            remain = offset % self.LOOPS
            zero_d = self.cur_p - self.lookup_zero()
            zero_l = '<' * zero_d
            zero_r = '>' * zero_d
            code += zero_l
            code += '+' * self.LOOPS
            code += '[' + zero_r + op * loop + zero_l + '-]'
            code += zero_r
            code += op * remain
        else:
            code += (op * offset)
        # NOTE: print the char
        code += '.'
        return ascii, code


if __name__ == '__main__':
    sample_sz = 'Hello World!'
    for mem_type in sorted(BrainFuck.INIT_MEM.keys()):
        bf_compiler = BrainFuck(mem_type)
        bf_code = bf_compiler.build(sample_sz)
        print mem_type, ''.join(bf_code)
