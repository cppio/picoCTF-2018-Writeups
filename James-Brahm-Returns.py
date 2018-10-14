#!/usr/bin/env python3
import socket
import time
import sys


class NC:
    def __init__(self, host, port):
        self.addr = host, port
        self.t = time.time()
        self.s = socket.create_connection((host, port))

    def recvafter(self, s):
        buf = b""
        while s not in buf:
            buf += self.s.recv(4096)
        buf = buf[buf.index(s) + len(s):]
        while b"\n" not in buf:
            buf += self.s.recv(4096)
        return buf[:buf.index(b"\n")]

    def restart(self):
        if time.time() - self.t > 175:
            self.s.close()
            self.__init__(*self.addr)

    def encrypt(self, msg_len, pad_len):
        self.restart()

        self.s.sendall(b"E\n" + b"A" * msg_len + b"\n" + b"B" * pad_len + b"\n")
        return bytes.fromhex(self.recvafter(b"encrypted: ").decode())

    def decrypt(self, enc):
        self.restart()

        self.s.sendall(b"S\n" + enc.hex().encode() + b"\n")
        return self.recvafter(b"message: ")


def get_pad(nc):
    c = len(nc.encrypt(0, 0))
    for i in range(1, 16):
        l = len(nc.encrypt(0, i))
        if l > c:
            return i, l - i - 16
    return 0


msg = """Agent,
Greetings. My situation report is as follows:
{0}
My agent identifying code is: {1}.
Down with the Soviets,
006
"""

msg_len = len(msg.format("", ""))
flag_offset = msg.format("", "\0").index("\0")

try:
    nc = NC(sys.argv[1], int(sys.argv[2]))
except (IndexError, ValueError):
    print("usage:", sys.argv[0], "host port")
    exit(1)

pad, length = get_pad(nc)
flag_len = length - 16 - 20 - msg_len
# IV is 16 bytes
# MAC is 20 bytes

flag = ""

print(end="_" * flag_len + "\b" * flag_len)
for i in range(flag_len):
    message_len = (-1 - flag_offset - i) % 16
    padding_len = (pad - message_len) % 16

    block_offset = message_len + flag_offset + i + 1

    n = 0
    while True:
        enc = bytearray(nc.encrypt(message_len, padding_len))
        enc[-16:] = enc[block_offset:block_offset + 16]
        if b"Success" in nc.decrypt(enc):
            flag += chr(16 ^ enc[-17] ^ enc[block_offset - 1])
            print(end=flag[-1], flush=True)
            break
        else:
            print(end=r"-\|/"[n] + "\b", flush=True)
            n = (n + 1) % 4
print()
