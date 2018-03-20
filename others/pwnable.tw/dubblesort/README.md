# dubblesort

> Challenge link: [dubblesort](https://pwnable.tw/challenge/#4)
>
> Category: pwn

Sort the memory!

`nc chall.pwnable.tw 10101`

[dubblesort](https://pwnable.tw/static/chall/dubblesort)

[libc.so](https://pwnable.tw/static/libc/libc_32.so.6)

## Observation

一開始程式先問了**名字**，接著問要**排列幾個數字** ，最後依序輸入**各個數字**後會排列完輸出結果

看到這題時，我想到之前在 `csie.ctf.tw` 有寫過一題 bubblesort ，那題是透過排列的數字沒有限制數量來蓋到 return address，或許這題有類似的漏洞

```bash
$ ./dubblesort
What your name :a
Hello a
,How many numbers do you what to sort :3
Enter the 0 number : 0
Enter the 1 number : 1
Enter the 2 number : 2
Processing......
Result :
0 1 2
```

### file

```bash
$ file dubblesort
dubblesort: ELF 32-bit LSB shared object, Intel 80386, version 1 (SYSV), dynamically linked, interpreter /lib/ld-linux.so.2, for GNU/Linux 2.6.24, BuildID[sha1]=12a217baf7cbdf2bb5c344ff14adcf7703672fb1, stripped
```

### checksec

保護全開

```bash
gdb-peda$ checksec
CANARY    : ENABLED
FORTIFY   : ENABLED
NX        : ENABLED
PIE       : ENABLED
RELRO     : FULL
```

### input

名字是使用 `read()` 來讀取，讀取的長度是 0x40

```bash
   0x56555a11 <main+78>:	mov    DWORD PTR [esp],0x0
=> 0x56555a18 <main+85>:	call   0x56555630 <read@plt>
   0x56555a1d <main+90>:	mov    DWORD PTR [esp+0x8],esi
Guessed arguments:
arg[0]: 0x0
arg[1]: 0xffffd72c --> 0xff17
arg[2]: 0x40 ('@')
```

要排列的數量是使用 `scanf()` ，且參數是 `%u` 也就是 unsigned int

```bash
   0x56555a45 <main+130>:	mov    DWORD PTR [esp],eax
=> 0x56555a48 <main+133>:	call   0x56555700 <__isoc99_scanf@plt>
   0x56555a4d <main+138>:	mov    eax,DWORD PTR [esp+0x18]
Guessed arguments:
arg[0]: 0x56555bfa --> 0x45007525 ('%u')
arg[1]: 0xffffd708 --> 0xe0
```

接著數字的部分一樣是使用 `scanf()` 加上 `%u` 

```bash
   0x56555a92 <main+207>:	mov    DWORD PTR [esp],eax
=> 0x56555a95 <main+210>:	call   0x56555700 <__isoc99_scanf@plt>
   0x56555a9a <main+215>:	add    esi,0x1
Guessed arguments:
arg[0]: 0x56555bfa --> 0x45007525 ('%u')
arg[1]: 0xffffd70c --> 0xf7f37f0a (mov    edx,DWORD PTR [esp+0x18])
```

### sort

sort 的參數是 要排列的數量 以及 第一個數字在 stack 上的位址，排列的方式看起來沒什麼問題

```bash
   0x56555ab0 <main+237>:	mov    DWORD PTR [esp],eax
=> 0x56555ab3 <main+240>:	call   0x56555931
   0x56555ab8 <main+245>:	lea    eax,[ebx-0x138c]
Guessed arguments:
arg[0]: 0xffffd70c --> 0x0
arg[1]: 0x3
----------------------- stack -----------------------
0028| 0xffffd70c --> 0x0 		# num 0
0032| 0xffffd710 --> 0x1		# num 1
0036| 0xffffd714 --> 0x2 		# num 2
```

### name

在測試 name 的時候，發現有時候會輸出一些不可視字元

```bash
./dubblesort
What your name :aaaa
Hello aaaa
y��/,How many numbers do you what to sort :
```

經過觀察後發現應該是因為 name 沒有將所有空間先歸零，所以輸出時才會連同後面的舊資料一起輸出

### stack canary

因為有開 canary 的關係，就算沒有檢查最多可以輸入幾個數字，再輸入超過時依然會噴錯

```bash
*** stack smashing detected ***: ./dubblesort terminated
```

利用二分搜的方式測試，發現最多只能輸入到 24 個數字，如果到第 25 個數字的話，在排列時就會噴出以上的錯誤訊息

## Solution

總共有三個步驟要做

1. leak libc
2. bypass canary
3. ret2libc

### Leak libc

這邊我利用的是 name

因為 name 的 buffer 沒有先清空的關係，所以可以 leak 出後面的數值

```bash
0060| 0xffffd72c ("aaaa\n\331\377\377/")
0064| 0xffffd730 --> 0xffffd90a --> 0xfb6d2200
0068| 0xffffd734 --> 0x2f ('/')
0072| 0xffffd738 --> 0x8e
0076| 0xffffd73c --> 0x16
0080| 0xffffd740 --> 0x8000
0084| 0xffffd744 --> 0xf7fcb000 --> 0x1b1db0
0088| 0xffffd748 --> 0xf7fc9244 --> 0xf7e31020 (call   0xf7f38b59)    <==
```

由上面 stack 內容可知，第 8 個包含一個位址，可以記錄下此時 libc base 與其之間的差值，並在真正 leak 出此值時減掉差值，即可得到 libc base

```bash
0xf7fc9244 - libc_base = x (固定的)
leak_addr - x = libc_base
```

只要輸入 28 (4*7) 個字元作為 payload ，就可以印出這個位址的值了

```bash
0060| 0xffffd72c ('a' <repeats 28 times>, "\n\222\374\367\001VUV\251WUV\240oUV\001")
0064| 0xffffd730 ('a' <repeats 24 times>, "\n\222\374\367\001VUV\251WUV\240oUV\001")
0068| 0xffffd734 ('a' <repeats 20 times>, "\n\222\374\367\001VUV\251WUV\240oUV\001")
0072| 0xffffd738 ('a' <repeats 16 times>, "\n\222\374\367\001VUV\251WUV\240oUV\001")
0076| 0xffffd73c ('a' <repeats 12 times>, "\n\222\374\367\001VUV\251WUV\240oUV\001")
0080| 0xffffd740 ("aaaaaaaa\n\222\374\367\001VUV\251WUV\240oUV\001")
0084| 0xffffd744 ("aaaa\n\222\374\367\001VUV\251WUV\240oUV\001")
0088| 0xffffd748 --> 0xf7fc920a --> 0x0
```

### bypass canary

在 observation 時，有利用二分搜的方式找到 canary 的位置在第 25 個

此時可以利用輸入時的 `scanf("%u")` ，一般在輸入時，要輸入 unsigned int 才會被接受，但是這樣會蓋掉 canary ，經過搜尋後才知道，原來可以輸入 '+'，此時會被當作正常輸入，但保留此位置原始的值，直接跳到下一個，如此一來就可直接繞過 canary 了

### ret2libc

要做到 ret2libc 的話達成兩個條件

- libc base
- return address

libc base 在先前已經透過 name 取得了，想要控制 return address 的話，可以利用輸入數字時的 buffer overflow，因為已經跳過 canary 了，所以可以一直推到 return 的位置，並進而控制 return address

這邊我一樣用二分搜的方式來做，如果有蓋到 return address 的位置的話會出現以下訊息

```bash
[*] Process './dubblesort' stopped with exit code -11 (SIGSEGV) (pid 2290)
```

搜尋過後知道 return address 是在第 33 個位置

```bash
24(payload) + canary + 7 + ret
```

最後就是使用 libc base 找到 `system` 以及 `/bin/sh` 串接在 return address 的位置即可

## Note

### pwntool libc

因為有給 libc ，所以在本機測試時最好是掛上 libc ，否則位址可能會跟遠端不同

```python
r = process('./dubblesort', env={'LD_PRELOAD':'./libc_32.so.6'})
```

### sort

在輸入 payload 時，因為輸入完後還會進行排序，所以要確保排序過後順序依然不變

我的作法是前 24 個字就直接輸入 0~23 ，canary 的部分輸入 + (43)，接著後面的 7 個字放 libc base，最後 `system` 及 `/bin/sh` 因為要加上 libc base ，所以一定比 libc base 大

### system

在呼叫 system 時，stack 第一個位置是結束後的 return address，因為不會 return 了，所以隨便填就可以了，接著才是 system 的第一個參數 `/bin/sh` 