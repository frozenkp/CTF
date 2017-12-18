# Pasty

> Challenge Link: [Pasty](http://hitb.xctf.org.cn/contest_challenge/)
>
> Category: Web

Can you find the administrator's secret message?

## 分析

此題提供一個可以用帳密登入的記事本網站，目標是取得管理員帳密
- 發現登入後用jwt作為token來認證
- 只要改動token中，使用者的名字就可以達成了

## 嘗試

上網找jwt的漏洞之類的 -> 找到的不能用QQ

## 解法

jwt的header中有一個**kid**，這個代表的是公鑰的位址
-> 可以自己產生公私鑰，用私鑰加密後，把kid改成公鑰位址送回去

但是公鑰的位址在伺服器底下的目錄，所以要先把公鑰貼在pasty上，接著取出在伺服器上的位址貼進去

> 公鑰會自動加上.pem該如何處理？
> 在網址最後面加上?，讓.pem變成參數