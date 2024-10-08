#!/usr/bin/env python

import sys

def hamming(bytes1, bytes2):

    bstr1 = "{:08b}".format(int(bytes1.hex(), 16)).zfill(24)
    bstr2 = "{:08b}".format(int(bytes2.hex(), 16)).zfill(24)

    dist = 0
    for i in range(len(bstr1)):
        dist += (bstr1[i] != bstr2[i])
    return dist




init_cmd = b'\x0a\xbf\x45'
select_cmd = b'\x00\x0a\xa4'

print(f"tmp    :\t{init_cmd.hex()} ,\t{select_cmd.hex()}")

with open(sys.argv[1], 'rb') as f:
    while tmp := f.read(3):
        if tmp != init_cmd and tmp != select_cmd:
            print(f"{tmp.hex()} :\t{hamming(tmp, init_cmd)} ,\t\t{hamming(tmp, select_cmd)}")

