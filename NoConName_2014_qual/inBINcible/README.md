# inBINcible

> Challenge Link: Nope
>
> Category: reverse

Get the key. The flag is: “NcN_” + sha1sum(key)

[inbincible](https://mega.co.nz/#!sER23Y6Q!zN_jO3hT6q8onHj6B-qFeapb7vif81omSa2Ap0Or9Kk)

## 觀察

這支程式執行後直接輸出 `Nope!` ，沒有任何輸入

```
% ./inbincible                   
Nope!
```

### 起手式

這個執行檔是 32 位元的，且是 static link

```
% file inbincible
inbincible: ELF 32-bit LSB executable, Intel 80386, version 1 (SYSV), statically linked, not stripped
```

發現 `main.main` 應該是 go 的執行檔

```
% objdump -M intel -d inbincible
inbincible：     檔案格式 elf32-i386


Disassembly of section .text:

08048c00 <main.main>:
 8048c00:       65 8b 0d 00 00 00 00    mov    ecx,DWORD PTR gs:0x0
 8048c07:       8b 89 f8 ff ff ff       mov    ecx,DWORD PTR [ecx-0x8]
 8048c0d:       8d 44 24 c0             lea    eax,[esp-0x40]
 8048c11:       3b 01                   cmp    eax,DWORD PTR [ecx]
 8048c13:       77 0b                   ja     8048c20 <main.main+0x20>
 8048c15:       31 ff                   xor    edi,edi
 8048c17:       31 c0                   xor    eax,eax
 ...
```

### go 起手式

總共有兩個函式在 main package 中

```
% go tool objdump inbincible | grep 'TEXT main\.' 
TEXT main.main(SB) /home/n/ctf/ncn_quals_2014/rev400/main.go
TEXT main.func.001(SB) /home/n/ctf/ncn_quals_2014/rev400/main.go
TEXT main.init(SB) /home/n/ctf/ncn_quals_2014/rev400/main.go
```

### 分析 main

過程中發現有取出 `os.Args`，可能是藉由參數輸入

```
   0x8048ef1 <main.main+753>:   cmp    DWORD PTR ds:0x814e17c,0x1
   0x8048ef8 <main.main+760>:   jbe    0x804937d <main.main+1917>
=> 0x8048efe <main.main+766>:   mov    ebx,DWORD PTR ds:0x814e178
   0x8048f04 <main.main+772>:   add    ebx,0x8
   0x8048f07 <main.main+775>:   mov    esi,DWORD PTR [ebx+0x4]
```

```
gdb-peda$ x/10gx 0x814e178
0x814e178 <os.Args>:    0x0000000218300000      0x0000000000000002
0x814e188 <persistent>: 0xf7fc91a400000000      0x00000000f7ff9000
0x814e198 <reflect.dummy>:      0x0000000000000000      0x0000000000000000
0x814e1a8 <sync.allPools>:      0x000000000814e03c      0x0000000000000000
0x814e1b8 <syscall.envs>:       0x0000004e1830e000      0x000000000000004e
```

接著比較 `esi` 和 `ebp` ，此時的 `ebp` 是固定的 `0x10` ，而 `esi` 是參數的長度

猜測參數長度應該要是 `0x10`

```
   0x8048f07 <main.main+775>:   mov    esi,DWORD PTR [ebx+0x4]
   0x8048f0a <main.main+778>:   mov    ebx,DWORD PTR [esp+0x6c]
   0x8048f0e <main.main+782>:   mov    ebp,DWORD PTR [ebx+0x4]
=> 0x8048f11 <main.main+785>:   cmp    esi,ebp
   0x8048f13 <main.main+787>:   je     0x8049048 <main.main+1096>
   0x8048f19 <main.main+793>:   xor    ecx,ecx
   0x8048f1b <main.main+795>:   mov    ebp,DWORD PTR [esp+0x88]
```

### 分析 func.001

在中間發現 reverse 題常見的 xor ，目標是 `ecx` 及 `ebp` 

此時的 `ecx` 是 `0x12` ，`ebp` 則是參數的第一個字`x47 ( 'G' ) `

```
0x8049456 <main.func+150>:   xor    ecx,ebp
```

接著比較了 `cl` 及 `al`

此時的 `cl` 是 xor 的結果，`al` 是前面取出的值

```
0x804946a <main.func+170>:   cmp    cl,al
```

如果兩者一樣的話，會透過 go channel 送出 0x1 給 main

猜測可能是只要 16 個字經過 xor 以後都一樣就可以通過了

## 解法

因為 xor 可以直接使用一樣的 key 來找到原始字串，所以只要取出 xor key 以及最後的答案就可以了

### xor key

實際查看該位置後發現 key 只有 5 bytes ，經過測試後發現這 5 bytes 會一直循環

也就是 `0x12, 0x45, 0x33, 0x87, 0x65, 0x12, 0x45, 0x33, 0x87, 0x65, 0x12, 0x45, 0x33, 0x87, 0x65, 0x12`

```
gdb-peda$ x/2gx 0x18300024-0x8
0x1830001c:     0x4533876500000000      0x0000000000000012
```

### ans

```
gdb-peda$ x/2gx 0x18300040
0x18300040:     0x0306330bb6447555      0x3344b247716002e9
```

### xor

將兩個字串經過 xor 以後就可以得到原字串 `G0w1n!C0ngr4t5!!`