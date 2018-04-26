# criticalheap

> Challenge link: [criticalheap](https://pwnable.tw/challenge/#8)
>
> Category: pwn
>
> Writeup: [criticalheap](https://github.com/frozenkp/CTF/tree/master/others/pwnable.tw/criticalheap)

There are some secrets . Try to capture `/home/critical_heap++/flag`.

We recommend you to use the provided docker environment to develop your exploit:

`nc chall.pwnable.tw 10500`

[critical_heap.tar.gz](https://pwnable.tw/static/chall/critical_heap.tar.gz)

## Observation

這題有很多個選項可以使用，以下講可能會用到的部分

### struct

這題有三個 struct (normal, time, system) 在一個 union，一開始就先在 .bss 段宣告長度 10 的 struct 陣列，其中某些變數 (name, value...) 是存字串的指標

#### normal

```
00000000 name
...
00000018 content
...
```

#### system

```
00000000 name
...
00000020 value
...
```

### create

#### name

name 的部分是先 read 進來以後，用 strdup 放到 struct 上的，所以也是存在 heap 上

![](https://i.imgur.com/fbl69dp.png)

#### normal

normal 的部分需要輸入 content，它是直接 read 到 rax + 0x18 (struct 上的 0x18) 的位置，沒有在後面補上 `0x00`

![](https://i.imgur.com/7ZPpc3s.png)

#### time

time 會用 localtime 拿取現在的時間以後，處理完存進 struct

![](https://i.imgur.com/Th8VE6i.png)

localtime 先使用 getenv 抓取環境變數 TZ 的值，接著讀出 TZ 所指的檔案，並將內容存在 heap 上

![](https://i.imgur.com/kzabx9I.png)

![](https://i.imgur.com/XUBYeD0.png)

### play_system

#### Set the name for the heap

這個功能其實就是 setenv

![](https://i.imgur.com/JeUENVX.png)

#### Unset the name in the heap

這個功能是 unsetenv

![](https://i.imgur.com/GtViGDw.png)

#### Get the value of name

這個功能比較特別，會先用 getenv 抓輸入的 name，接著將抓到的指標 (指向 heap 上存 value 處) 存在 rax + 0x20 (struct 上 0x20 的位置)

![](https://i.imgur.com/R67Ah33.png)

### play_normal

#### Show the content of heap

這個功能有 format string 的漏洞，而且是使用 printf_chk

![](https://i.imgur.com/ssfVY7r.png)

### delete

delete 實際上只有把指定的 struct 標成 0 而已，上面的資訊並沒有清空

![](https://i.imgur.com/WLIYn6j.png)

### Conclusion

- create_normal 讀取 content 時沒有結尾
- play_normal 有 format string 的漏洞
- setenv 可以改動 TZ 的值
- delete 沒有清空

## Solution

解法步驟如下：

1. leak heap base 位置
2. 利用 setenv 改動 TZ 以後，用 localtime 將 flag 讀到 heap 上
3. 利用 format string 印出 flag

### leak heap base

這個部分要利用 "delete 沒有清空" 的漏洞

先創 system，接著到 play 隨便創一個環境變數，再使用 play_system_get_value 來將環境變數的位址放到 struct 上，這是為了取得一段 heap address

```
0x000 name
0x020 value  (heap address)
```

接著 delete 掉，然後創一個 normal 的 struct，此時 normal struct 會蓋在 system struct 原本的位置上

因為 content 存在 0x18，與原本的 value 差 0x8，要輸入 8 個字元才能碰到 value 的位置

>不要輸入 \n 不然輸出會被截斷

```
0x000 name
0x018 content ('AAAAAAAA')
0x020 value  (heap address)
```

最後就使用 show 把 struct 印出來就可以得到 heap address 了

因為在 heap 上相對位置不變，用 gdb 看一下跟 base 差多遠，leak 出來後減掉就是 heap base 了

### TZ

這個部分就創一個 system 然後用 setenv 把 TZ 設成 `/home/critical_heap++/flag`

接著創一個 time struct，就會在 localtime 將 flag 讀取到 heap 上了，然後用 gdb 看一下 offset 搭配 heap base 就可以知道 flag address 了

![](https://i.imgur.com/o5RZhBc.png)

### format string

利用 format string 搭配 %s 可以 leak 任意位址的特性來 leak flag address

另外，因為是使用 printf_chk 的關係，不能使用 `$` 要自己用 %c 來跳到指定區域

![](https://i.imgur.com/wniwxLP.png)

## Note

### peda in docker

這次有給一個 docker 的環境，要在裡面使用 gdb-peda 的話，要改動以下設定

#### Dockerfile

```dockerfile
RUN apt-get install gdb git -y
WORKDIR /root
RUN git clone https://github.com/scwuaptx/Pwngdb.git ; cp ~/Pwngdb/.gdbinit ~/
RUN git clone https://github.com/scwuaptx/peda.git ~/peda ; echo "source ~/peda/peda.py" >> ~/.gdbinit ; cp ~/peda/.inputrc ~/
```

#### docker-compose.yml

```yaml
critical_heap:
    cap_add:
        - SYS_PTRACE
```

