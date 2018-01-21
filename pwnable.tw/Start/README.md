Start
===

## Problem
Just a start.

`nc chall.pwnable.tw 10000`

[start](https://pwnable.tw/static/chall/start)

### nc
```
Let's start the CTF:{input}
```

## Observation
### Read length
can read **0x3c** bytes

![](https://i.imgur.com/PCJNe4r.png)

### Buf
store on stack and **stack excutable**

![](https://i.imgur.com/zMCZ1I7.png)

### Ret
Payload = 20 bytes

## Solution
### Leak stack address
If we want to execute code on stack, we should return $PC to stack at first. However, stack address is not always the same. Thus, we should leak stack address in the beginning.

#### Target
There is an address (`0xffffd220`) after return address.

**$esp** will be `0xffffd21c` ( --> `0xffffd220`) after return, then we can use **write** to print this address.

![](https://i.imgur.com/gevRuVg.png)

#### Return
Return to `mov ecx, esp` before **write** to mov buffer to the target.

![](https://i.imgur.com/2dfPkF0.png)

### Shellcode
After leaking address, we get another chance to write. Buffer is $esp (still on the stack).

#### Target
I found that return address on the stack is `0x%%%%%%T0`
- % from the address leaked in advance
- T is a random number from 0 to f

Therefore, just put `0x%%%%%%T4` at return address. Then write shellcode after it.

![](https://i.imgur.com/EZAE3C4.png)
#### Which number is T ?
There are 16 possible numbers, so just **guess** !!!

You will get shell if you are fortunate enough. OwO

