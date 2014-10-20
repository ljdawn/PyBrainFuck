#! /usr/bin/env python3

import sys
import io
import os

class BrainFuckError(BaseException):
    def __init__(self, msg):
        self.msg = msg
    def __str__(self):
        return str(self.msg)

class BrainFuck:
    def __init__(self):
        self.cs = ""
        self.ip = 0
        self.ds = [0]
        self.bp = 0
        self.ss = [0]
        self.input_buffer = ""
        self.keywords = list("+-><[].,")
        self.states = {"+": self.__increment_state, "-": self.__decrement_state, ">": self.__forward_state, "<": self.__backward_state, "[": self.__while_entry_state, "]": self.__while_end_state, ".": self.__output_state, ",": self.__input_state}

    def __increment_state(self):
        self.ds[self.bp] += 1

    def __decrement_state(self):
        self.ds[self.bp] -= 1

    def __forward_state(self):
        if self.bp + 1 >= len(self.ds):
            self.ds.append(0)
        self.bp += 1

    def __backward_state(self):
        self.bp -= 1

    def __output_state(self):
        print("%c" % self.ds[self.bp], end="")

    def __input_state(self):
        if len(self.input_buffer) == 0:
            self.input_buffer = input(">> ")
        self.ds[self.bp] = ord(self.input_buffer[0])
        self.input_buffer = self.input_buffer[1:]

    def __while_entry_state(self):
        if self.ds[self.bp] != 0:
            self.ss.append(self.ip - 1)
        else:
            stack = 0
            while (self.ip < len(self.cs)):
                if self.cs[self.ip] == '[':
                    stack += 1
                elif self.cs[self.ip] == ']': 
                    stack -= 1
                self.ip += 1
                if stack == 0:
                    self.ip -= 1
                    break

    def __while_end_state(self):
        if self.ds[self.bp] != 0:
            self.ip = self.ss.pop()
            
    def run(self, program, type = "string"):
        self.cs = program
        while self.ip < len(self.cs):
            if self.cs[self.ip] in self.keywords:
                self.states[self.cs[self.ip]]()
            elif self.cs[self.ip].isspace():
                pass
            else:
                raise BrainFuckError("%s (col %d) syntax error: PyBrainFuck Is not defined '%s' for this grammar rule!" % (type, self.ip, self.cs[self.ip]))
            self.ip += 1    

def main(argc, argv):
    if argc > 1:
        for file in argv:
            if os.path.exists(file):
                program = io.open(file, "r")
                brain_fuck = BrainFuck();
                brain_fuck.run("".join(program.readlines()))
                program.close()
            else:
                print("error: No such file or directory: %s" % file)
    else:
        print("// PyBrainFuck 0.1 interpreter.\n// author: Jrong.\n// email: zuolan.jer#gmail.com.\n// date: 2014.10.19.")
        while True:
            try:
                brain_fuck = BrainFuck();
                program = input("@ ")
                brain_fuck.run(program)
            except BrainFuckError as error:
                print(error, end="")

if __name__ == "__main__":
    main(len(sys.argv), sys.argv[1:])
