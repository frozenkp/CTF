## Trashy Or Classy

> Challenge Link: [Trashy Or Classy](https://asisctf.com/challenges/)
>
> Category: forensic
>
> Writeup: [Trashy Or Classy](https://github.com/frozenkp/CTF/tree/master/2018/ASIS_CTF_qual/forensic/Trashy_Or_Classy)

Don't be [Trashy](https://asisctf.com/tasks/Trashy_Or_Classy_1afb5f5911a97860e181722b55dae50bb765285cd8dcbb38837d1a1094e53444). Try being Classy!!

## Solution

檔案載下來以後是一個 pcap

### pcap

用 wireshark 大概看一下，好像是在暴力搜 http://167.99.233.88 的子目錄

> Filter: http

![](https://i.imgur.com/iJHHeVn.png)

看看有成功找到的目錄，有一個回覆是有 Index 的

> Filter: http.response.code == 200

![](https://i.imgur.com/zCbt4kn.png)

![](https://i.imgur.com/4Mcvqzz.png)

實際到這個[網址](http://167.99.233.88/private/)去看，發現是要輸入帳密的，仔細研究一下這個封包，發現是 Digest Auth，且有一些資訊

利用這些資訊搭配 rockyou.txt ，暴力算出密碼是 `rainbow`

![](https://i.imgur.com/B8Sj616.png)

### Casync

連上去後，可以載到 `flag.caidx` ，不過還有一個資料夾 `flag.castr` 進不去，猜測可能是不能進去但知道檔名的情況下可以下載

根據檔名，找到了 [casync](https://github.com/systemd/casync) 和 [desync](https://github.com/folbricht/desync) 

> casync 在 ubuntu 17.10 上的版本會出現 Operaion not supported 的錯誤，需要自己編

我們使用 desync 加上自己接的 proxy (通過 Digest Auth) 從遠端 server 上把整份資料夾抓下來

```
% desync extract -s http://167.99.233.88/private/flag.castr/ flag.caidx flagdesync.tar
```

抓下來後看到一大堆的 chunk，大概翻了一遍還是不知道是幹嘛用的，結束後看 writeup 才知道要用 casync 把檔案還原 Orz

```
% casync extract --store=./flag.castr ./flag.caidx ./flag
```

還原後就拿到了一個 flag.png

![](https://i.imgur.com/SdPfcyH.png)