#!/usr/bin/env python3
import hashlib
from z3 import *

with open("map2.txt") as f:
    cipher, (length, gates, check) = eval(f.read().replace("L", ""))

s = Solver()
b = [Bool("b" + str(i)) for i in range(length + len(gates))]

for i, (name, args) in enumerate(gates, length):
    if name == "true":
        s.add(b[i])
    else:
        u1 = Xor(b[args[0][0]], args[0][1])
        u2 = Xor(b[args[1][0]], args[1][1])
        if name == "or":
            s.add(b[i] == Or(u1, u2))
        elif name == "xor":
            s.add(b[i] == Xor(u1, u2))

s.add(Xor(b[check[0]], check[1]))

s.check()
model = s.model()

n = 0
for i in b[length - 1::-1]:
    n = n << 1 | is_true(model[i])

print(bytes.fromhex(hex(cipher ^ int(hashlib.sha512(b"%d" % n).hexdigest(), 16))[2:]).decode())
