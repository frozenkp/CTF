# infant-gotoheaven

> Challenge Link: [infant-gotoheaven](http://ctf.bamboofox.cs.nctu.edu.tw/challenges#infant-gotoheaven)
>
> Category: pwn

What's the token to heaven?

`nc bamboofox.cs.nctu.edu.tw 58796`

[infant-gotoheaven.zip](http://ctf.bamboofox.cs.nctu.edu.tw/files/974c6efa89c277c774f2dfd56500aaf0/infant-gotoheaven.zip)

## Go binanry 小訣竅

開始前先講一下分析 Go 的 binanry 時可以用到的一些工具以及訣竅

###  go tool objdump

`go tool`是 go 的編譯器內建的工具集，其中也有 `objdump`可以使用

使用這個工具的話可以看到 source code 中的**行數**對應到的 assembly

```bash
go tool objdump infant-gotoheaven | less
```

![](https://i.imgur.com/a7202rA.png)

### gdb

使用`gdb`追蹤時，在執行到`main`之前會經過一大堆的程序

在追蹤 C 的 binanry 時，通常會使用 `b main`來設斷點在`main` 的一開始

由上面 `go tool objdump`的圖可以看到，Go 的 `main` 叫做 `main.main` 所以要使用

```
b main.main
```

## 觀察

這支程式可以讓使用者輸入一串字串

```
% ./infant-gotoheaven                     
Give me your text : 
aaaaaaaaaaaaaaaaaaaaaaaaaaaaa
```

### Buffer overflow

通常看到這類題目大概都是 buffer overflow ，所以先試一下能不能觸發 segmentation fault

```
% ./infant-gotoheaven
Give me your text : 
aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
unexpected fault address 0x0
fatal error: fault
[signal SIGSEGV: segmentation violation code=0x80 addr=0x0 pc=0x4a263e]

goroutine 1 [running]:
runtime.throw(0x4d8780, 0x5)
        /usr/local/go/src/runtime/panic.go:605 +0x95 fp=0xc420043f28 sp=0xc420043f08 pc=0x427a05
runtime.sigpanic()
        /usr/local/go/src/runtime/signal_unix.go:374 +0x227 fp=0xc420043f78 sp=0xc420043f28 pc=0x43d037
main.main()
        /home/frozenkp/Downloads/gobin/infant-gotoheaven/infant-gotoheaven.go:27 +0x1ee fp=0xc420043f80 sp=0xc420043f78 pc=0x4a263e
```

最後一行有寫到死在`infant-gotoheaven.go:27`

用`objdump`看一下發現是死在`ret`，所以應該是可以**蓋到 return address**

![](https://i.imgur.com/5yNqs1q.png)

### weird

接著在翻一下`objdump`的結果，發現一個叫 `weird`的 function

![](https://i.imgur.com/zG0ODob.png)

其中有一行`CALL os/exec.Command(SB)`可以執行 system call

檢查一下其他地方的程式碼，發現`main.main`有呼叫到

![](https://i.imgur.com/dOiwh0q.png)

使用`gdb`強制讓`cmp`符合後跳過去後發現這個 system call 的參數是 `/bin/sh`

![](https://i.imgur.com/LSHqpjy.png)

所以只要進入到`weird`應該就能拿到 shell 了

## 解法

### payload

先隨便輸入來造成 segmenataion fault，確定程式會產生 buffer overflow，且是死在 return addresss 錯誤

![img](https://i.imgur.com/sMorU1A.png)

計算一下 payload 是 **224**

### weird

因為可以蓋到 return address，也就是說可以任意指定要跳到哪裡，那就把 return address 改成`weird`的開頭`0x4a2650`就可以跳過去執行囉

執行後果然就成功拿到 shell 了 OwO