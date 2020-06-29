# AIS3 pre-exam 2020 Misc 官方 Writeup

## 💤 Piquero
### Description

I can’t see the flag. Where is it?

![](https://i.imgur.com/QOdvP4N.jpg)

### Solution
這題是編碼的題目，用的是 Braille，也就是生活中常見的盲人點字，這題會遇到的問題是 Braille 有多種語系，會需要推敲一下，不過 Flag 是英、數、符號組成，且網路上多數工具也是以英文為主，應該蠻容易試出來的(?)。

解法的部分，只要參考英文版 [wiki](https://en.wikipedia.org/wiki/Braille) 就可以逐字解開了，解答如下圖：

![](https://i.imgur.com/Uovcyfy.jpg)

### Note
這題的難度定位是最簡單的，想蠻久要出什麼題目的，後來看了網路上各種知識型頻道，剛好看到[啾啾鞋在講盲人點字](https://www.youtube.com/watch?v=1aop1ursHVE)，覺得挺有趣的，而且是同學日常生活中都見過，卻沒注意過的編碼，就出了這題。

在比賽過程中，很多同學都使用線上工具來解，得到類似下圖的結果，雖然說看到這個再通靈一下就知道 Flag 了(也確實有些同學是用通靈的)，不過在這個結果中可以發現，`AIS` 前面都有一個符號，且比賽有公告格式為 `AIS3{...}`，可推測該符號為大寫字母的前綴符號，而 `AIS3` 後方的兩個符號在前後都有，應為 `{}`，可得 `AIS3{I-feel-sleepy-Good-Night!!!}`，但這還是錯的，之後觀察一下一般 Flag 的寫法，應該就可以發現要將 `-` 改成 `_` 了。

![](https://i.imgur.com/PrXxm6T.png)

## 🐥 Karuego

### Description

Students who fail to summon will be dropped out.

![](https://i.imgur.com/pYqUF4f.jpg)

### Solution

先用 binwalk 掃一下可以發現圖片後面有一個加密過後的壓縮檔，接著用 lsb 掃一下原圖可以找到 `The key is : lafire` 的字串，使用 `lafire` 作為密碼解開壓縮檔即可得到下圖。

![](https://i.imgur.com/CAVz5ex.png)

### Note

這題是想出簡單的 stego 題，所以綜合了各種圖片常用的技巧來出題，上述解法只是其中一種，其實加密的壓縮檔可以直接使用 `rockyou.txt` 或是 John the Ripper 等工具暴力破解，另外壓縮檔的檔案結構沒有加密，可以在其中找到一張圖片 (`3a66fa5887bcb740438f1fb49f78569cb56e9233_hq.jpg`)，搜尋一下這張圖的原圖，再使用 `pkcrack` 做 known-plaintext attack 也可以解開。

## 👿 Shichirou

### Description

Don’t cheat!!!

```python
#!/usr/bin/env python3

import os
import sys
import tempfile
import subprocess
import resource

resource.setrlimit(resource.RLIMIT_FSIZE, (65536, 65536))
os.chdir(os.environ['HOME'])

size = int(sys.stdin.readline().rstrip('\r\n'))
if size > 65536:
    print('File is too large.')
    quit()

data = sys.stdin.read(size)
with tempfile.NamedTemporaryFile(mode='w+', suffix='.tar', delete=True, dir='.') as tarf:
    with tempfile.TemporaryDirectory(dir='.') as outdir:
        tarf.write(data)
        tarf.flush()
        try:
            subprocess.check_output(['/bin/tar', '-xf', tarf.name, '-C', outdir])
        except:
            print('Broken tar file.')
            raise

        try:
            a = subprocess.check_output(['/usr/bin/sha1sum', 'flag.txt'])
            b = subprocess.check_output(['/usr/bin/sha1sum', os.path.join(outdir, 'guess.txt')])
            a = a.split(b' ')[0]
            b = b.split(b' ')[0]
            assert len(a) == 40 and len(b) == 40
            if a != b:
                raise Exception('sha1')
        except:
            print('Different.')
            raise

        print(open('flag.txt', 'r').readline())
```

### Solution

這題是要上傳一個 tar 檔，裡面要有寫有 Flag 的 `guess.txt`，這邊可以使用 `ln` 來將 `guess.txt` 連結到 `flag.txt`，這樣開檔確認時就會開到相同的檔案。

```
ln -s ../flag.txt guess.txt
tar -cf Shichirou.tar guess.txt
```

### Note

這題其實是 AIS3 pre-exam 2016 misc 3，只有題目敘述、flag、以及家目錄的位置有更改，沒想到解出來的人好少QQ

## 👑 Saburo

### Description

Spell you flag and fight with me.
PS. flag is printable characters with `AIS3{…}`

### Solution

這題考的是 timing attack，隨著猜對的字越多，所需的時間就會越久，可以利用這個特性逐字檢驗，找出可能性最高的字。不過檢驗一個字元所需的時間是浮動的，雖說多檢驗一個字的確會花比較多時間，但浮動的範圍卻會越來越大，檢驗一個字元所需的時間為 11~15 ms，假設檢驗到第 10 個字元，得到的結果最快跟最慢可以差到 50 ms，這個問題會增加檢驗的難易度。

為了解決上述問題，必須使用一些技巧來避免誤判，首先是要確定哪個答案是錯的，當不斷往上增加時，得到的數字如果沒有繼續增加就代表前面可能有字元猜錯，這邊可以將前幾個字的差值平均，並與現在的差值做比較 (例如判斷現在的差值是否大於原差值的一半)，如果發現是錯的，就往前一個字元重找，除此之外，也可以將同個字串送多次來取得平均值，來求得比較穩定的答案。

### Note

這題原本的設計是使用 cpu time 來計算，但比賽開始後，因為很多人一起測，得到的時間其實不太穩定，因此比賽開始後幾小時我就將題目回傳的時間改成 `time += 11 + random()%5` 了，但賽中許多同學依然認為是系統不穩定造成的，並沒有發現這題真正的考點並加以改善，有點可惜QQ。

## 👻 Soy

### Description

Here is your flag.
Oops, my bad.

![](https://i.imgur.com/OdhitRq.png)

### Solution

這題可以參考英文版 [Wiki](https://en.wikipedia.org/wiki/QR_code)，在題目的 QRcode 中，被遮住的部分是容錯區塊，格式區塊以及資料區塊都是正常的，如果不管容錯的話，裡面存的資料是可以正確地解開的，而平常使用的解碼程式都會考慮容錯的部分，因此不會輸出儲存的資料。這題可以使用[線上工具](https://merricx.github.io/qrazybox/)或是跟著格式手解，解答請參考下圖：

![](https://i.imgur.com/65QlMr5.png)

### Note

這題是想考 QRcode 的格式的，只要看懂 QRcode 的設計就可以順利解出來，當時沒發現有線上工具可以用，也沒發現 HSCTF 2020 N-95 才剛出過類似的題目，結果就被瞬間解出來了QQ

## 🧸 Clara

### Description

I did nothing special today. >_<

### Solution

這題給了一包 100 mb 的 pcap，先分析一下傳輸的種類 (wireshark 在 statics -> conversations -> tcp)，可以發現有兩筆本機跟 `140.112.42.47` 的傳輸量特別大，且這兩筆是唯一未加密的 (可以用 `http` 過濾出來)。

![](https://i.imgur.com/diTAAkA.png)

follow 其中一筆，可以看到傳遞資料如下圖，比較一下這兩筆可以發現，開頭都是傳 `deadbeeffaceb00c`，後面才不一樣，前 8 bytes 實際上是在做 key exchange，而 key 的長度是 8 bytes，遠端會將 key XOR `deadbeeffaceb00c`，本地端收到後再解密得到 key，接著後面的傳輸都是經由該 key 做 XOR 後傳輸的。

![](https://i.imgur.com/9ILBv9a.png)

其實翻到後面可以發現有些區段是可以看到包含 `AIS3{NO}` 和 `xSECRETx` 的字串，這分別是兩次所使用的 key，因為傳遞的資料中包含 `0x00`，所以經過 XOR 後可以直接看到原本的 key，即便沒有發現前面是 key exchange，一樣可以從這邊推敲出加密方式以及 key。

![](https://i.imgur.com/L3qySut.png)

接著要解密所傳輸的資料，觀察一下格式可以發現後面的資料都是由 4 bytes + n bytes + 4 bytes + m bytes 組成，其中 n 都比較小，而 m 都非常大，這邊可以猜測 m 是資料本身，而 n 則是跟該資料有關的 metadata，前面的 4 bytes 則可能是長度。因為一般後門透過 socket 在傳輸時，必須先溝通好格式，C2 Server 才能順利解讀 backdoor 傳過來的訊息，尤其是在傳送檔案這種不固定大小的資料，一定要先講好長度或是前後綴。

經過解密後可以發現，4 bytes 為 Little Endian 表示的長度 (n / m)，後面 n / m bytes 則分別是檔名以及檔案內容，其中第二次對話的第四張圖片即為 Flag。

![](https://i.imgur.com/5wsqeMz.jpg)

### Note

我最近的研究項目是以單純利用 monitor 錄到的資訊，且盡量避免直接分析 binary 的方式來分析 malware，所以想試著把各種線索匯集在一起出成題目，我最後採用了 pcap 的方式，因為比較好分析，對新手也比較容易上手。因為只有 pcap，所以必須給足線索，我選擇透過 `http` 的方式傳遞數張大型圖片，如果有仔細分析過內容的話，應該是可以很快找到可疑的流量。

接著是加密的部分，直接看的話是看不出到底在傳什麼，因此可以知道是有加密過的，問題是用什麼方式以及什麼 key 加密，如果是直接使用設計時就寫好的 key 加密的話，我覺得這題就太通靈了，因此我用了比較簡單易懂的方式來做 key exchange，為了避免參賽者沒有發現，我故意將 backdoor 斷線並重新連線，且兩次使用不同的 key 來加密，透過觀察初始的 `deadbeeffaceb00c` 應該就可以推敲出來了 (其中一位解開的同學也確實是這麼做的)。另外 key 的長度設定為 8 bytes 也是一個線索，因為圖片會有許多 `0x00` 所以加密後可以直接看到 key 的內容，將 wireshark 切到 hex mode 以後，它是以每 16 bytes 做對齊的，仔細觀察就可以發現同一列會出現多個同樣字元，全部彙集起來後就是該次的 key 了。

最後是傳輸內容的部分，在透過 socket 傳輸時，因為不知道對方要傳什麼內容，所以必須先訂好一些傳輸的規則，否則對方收到的就只是一大片的資料而已，完全不知道怎麼切割。一般來說會分成兩種，第一種是既定的格式，最前面的 key exchange 就屬於這種，事先就講好 backdoor 傳 8 bytes，而 C2 回 8 bytes，第二種則是不固定長度的，常會用在傳檔案或字串的時候，可以像這題一樣，先傳一個固定長度 (這題為 4 bytes) 表示長度，接著就只要接收該長度的資料即可，也可以透過特殊前後綴，例如 `<BEGIN>...<END>` 來標示出資料的範圍。

綜合以上幾個概念，就可以順利的解開這題了，不過一直到最後我丟出一堆提示才有人解開QQ，我覺得可能是因為同學對 backdoor 研究較少，因此對許多線索比較不敏感。其實這題我在出完後還有拿給在 Forensic 方面有研究的前輩看看，我們覺得線索給的夠多，應該是不會太通靈，他有建議我一些降低難度的方法，例如可以直接在流量中傳遞整個 backdoor，之後再透過 backdoor 做之後的傳輸，不過覺得這樣就變成單純的 dump binary 然後 reverse 了，有點無趣，所以才保留了原始的作法。