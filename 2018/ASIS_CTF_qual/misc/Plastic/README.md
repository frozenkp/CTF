# Plastic

> Challenge Link: [Plastic](https://asisctf.com/challenges/)
>
> Category: misc
>
> Writeup: [Plastic](https://github.com/frozenkp/CTF/tree/master/2018/ASIS_CTF_qual/misc/Plastic)

Are LaTeX and [PlAsTiC](https://asisctf.com/tasks/plastic_b3a67f6e7ad52d6ca559d1aafa79c6fd6a80c73360664e7330dd6303d60b789b) the Same? It seems that they have very different compounds.

## Solution

檔案載下來是一個 PNG 檔

```
% file plastic
plastic: PNG image data, 1612 x 74, 8-bit/color RGBA, non-interlaced
```

![](https://i.imgur.com/lSItWe9.png)

 用 strings 看一下，可以發現奇怪的資料

```Xml
<x:xmpmeta xmlns:x="adobe:ns:meta/" x:xmptk="XMP Core 5.4.0">
   <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
      <rdf:Description rdf:about=""
            xmlns:exif="http://ns.adobe.com/exif/1.0/"
            xmlns:tiff="http://ns.adobe.com/tiff/1.0/">
         <exif:UserComment>
            <rdf:Alt>
               <rdf:li xml:lang="x-default">AAAFWHjabVRfbBRFGJ/ZOeifa+m2hVJaoNf2iohQtndX9ipS29IeVuwVe/1zbfc4&#xA;5/bm7pbu7V5255DjaDISozExaggxSIxC+2KRqBhjCPFBQwgmPggtSnySFx98IP57&#xA;ML4590dEw2w2+33fzHzz+37fbyeW0TWbStIdKCDHuvUvngi7jxPL1kwj7DZjx4hK&#xA;7Vk3ttSUxsOTbmpmGgB85cLHYntFZXtHp7trx2M7H9/1RI+/78DgoWeC4zNhJarG&#xA;U7pp0ym3kdX1tapqZ02TayYY6l4gOXuOf8t5p92qjm17pXZDnVjf0LhxExMYYg62&#xA;jq1nFaySVbHqlc3NW1pat27b3sacrIZtYHWsnrWwVraNbWeucAzbRNcMMqWaumlN&#xA;ps04maIa1Uk4YxGcjukkksZJQ0toKqa8pMk4piQq1sWwupC0zKwRP1jYOGebWUsl&#xA;k+QE7QTlsbZ7j7N7rzQVDE0cGlKCoeLCUAarZFzcJXX3+fd5fL19/j6/S+qWJLnH&#xA;I/XxIXsLrkf2eX0Sj/YCEbLaVY/X1ztXKtbAaRIumcSeKadd2if/Y4aDofEiO6Jj&#xA;1fnk/qdmOV02tTQjycQjPFH/0xx+MDSWpZhXFyrOLPcPyHxfyVkbch4cHgk88Dn0&#xA;QcqtWJYSmzWwLawxKq4qcVPNpolBi0jme6QMjeSxRTVVJ4vVStYmvNIFnCTz3Cxg&#xA;tiP5IseLri4eibsSpsVfg7qK0Yd35HHatnPpGF+ZxjRl/3+uEHzU3HyWJvyRvGZk&#xA;OFJDLR2UyOouarpoLkNccc3ivOg5bmDV0jhWl5rCFlYp12t1QWajh8cuPss2XnyO&#xA;bWLN08FQgAO8c+T5CWdocmqa+yHtJOHEJAI6TtrcD/LCOgd2lhouiqyJbZ4eMw2s&#xA;mpzp2blyhqV5uWzxaOQoJ3RYUwtqwlZuKSLz4As4KjY8xHO8RP1STH5kvHNgqHTk&#xA;KnEmkoUfg2ocyOCXfrLwp/oT28pTasf4mcNcrUsLctkqKDK9Vwr0uPgDWG2h05mR&#xA;AGsr9fRAXoklXIOh0dCiku+V0l4l6stkbCWa7R1RomNeGXPx+5RofNyQlehonyFN&#xA;ECVKU96x9nZlkR+ZPR4VGx9I698al7MRuSi6wyRH4oPlq+B27uSkZZqUQVAJ6kEL&#xA;6AR7gAfIYB5gkAIZkAenwevgDfAWOAPOgrfBOXAevAveAx+AS+Ay+Ah8Aj4Fn4HP&#xA;wVVwDXwBboBvwC3wPfgR3Ae/Qwesg82wDXZBD4xCDFWYgjY8BV+Gr8I34Tl4Hr4P&#xA;V+CH8DK8Aq/Dm/AWvAvvwfvwF/gb/EP4WvhWuC2sCd8Jd4UfhHvCz8Kvwl8IoCrk&#xA;RLWoDjWhVtSButBu1IP60SAKoHl0FNnoFHoJvYbOoLPoHXQBLaNL6Aq6iq6hr9B1&#xA;dAPddFQ4ahwdjh0Ov2O/Y6DUQQGWr4s8+M9wDP0NfUGwlA==&#xA;</rdf:li>
            </rdf:Alt>
         </exif:UserComment>
         <tiff:Orientation>1</tiff:Orientation>
      </rdf:Description>
   </rdf:RDF>
</x:xmpmeta>
```

把中間那段整理一下，看起來是 23 段經過 base64 的字串，不過解開看不出來是啥

```
AAAFWHjabVRfbBRFGJ/ZOeifa+m2hVJaoNf2iohQtndX9ipS29IeVuwVe/1zbfc4
5/bm7pbu7V5255DjaDISozExaggxSIxC+2KRqBhjCPFBQwgmPggtSnySFx98IP57
ML4590dEw2w2+33fzHzz+37fbyeW0TWbStIdKCDHuvUvngi7jxPL1kwj7DZjx4hK
7Vk3ttSUxsOTbmpmGgB85cLHYntFZXtHp7trx2M7H9/1RI+/78DgoWeC4zNhJarG
U7pp0ym3kdX1tapqZ02TayYY6l4gOXuOf8t5p92qjm17pXZDnVjf0LhxExMYYg62
jq1nFaySVbHqlc3NW1pat27b3sacrIZtYHWsnrWwVraNbWeucAzbRNcMMqWaumlN
ps04maIa1Uk4YxGcjukkksZJQ0toKqa8pMk4piQq1sWwupC0zKwRP1jYOGebWUsl
k+QE7QTlsbZ7j7N7rzQVDE0cGlKCoeLCUAarZFzcJXX3+fd5fL19/j6/S+qWJLnH
I/XxIXsLrkf2eX0Sj/YCEbLaVY/X1ztXKtbAaRIumcSeKadd2if/Y4aDofEiO6Jj
1fnk/qdmOV02tTQjycQjPFH/0xx+MDSWpZhXFyrOLPcPyHxfyVkbch4cHgk88Dn0
QcqtWJYSmzWwLawxKq4qcVPNpolBi0jme6QMjeSxRTVVJ4vVStYmvNIFnCTz3Cxg
tiP5IseLri4eibsSpsVfg7qK0Yd35HHatnPpGF+ZxjRl/3+uEHzU3HyWJvyRvGZk
OFJDLR2UyOouarpoLkNccc3ivOg5bmDV0jhWl5rCFlYp12t1QWajh8cuPss2XnyO
bWLN08FQgAO8c+T5CWdocmqa+yHtJOHEJAI6TtrcD/LCOgd2lhouiqyJbZ4eMw2s
mpzp2blyhqV5uWzxaOQoJ3RYUwtqwlZuKSLz4As4KjY8xHO8RP1STH5kvHNgqHTk
KnEmkoUfg2ocyOCXfrLwp/oT28pTasf4mcNcrUsLctkqKDK9Vwr0uPgDWG2h05mR
AGsr9fRAXoklXIOh0dCiku+V0l4l6stkbCWa7R1RomNeGXPx+5RofNyQlehonyFN
ECVKU96x9nZlkR+ZPR4VGx9I698al7MRuSi6wyRH4oPlq+B27uSkZZqUQVAJ6kEL
6AR7gAfIYB5gkAIZkAenwevgDfAWOAPOgrfBOXAevAveAx+AS+Ay+Ah8Aj4Fn4HP
wVVwDXwBboBvwC3wPfgR3Ae/Qwesg82wDXZBD4xCDFWYgjY8BV+Gr8I34Tl4Hr4P
V+CH8DK8Aq/Dm/AWvAvvwfvwF/gb/EP4WvhWuC2sCd8Jd4UfhHvCz8Kvwl8IoCrk
RLWoDjWhVtSButBu1IP60SAKoHl0FNnoFHoJvYbOoLPoHXQBLaNL6Aq6iq6hr9B1
dAPddFQ4ahwdjh0Ov2O/Y6DUQQGWr4s8+M9wDP0NfUGwlA==
```

後來將所有的字串合起來解開後，出現的是一個 data Orz

接著用 binwalk 跑一下，發現裡面還有裝其他東西

```
% file tmp
tmp: data

% binwalk tmp

DECIMAL       HEXADECIMAL     DESCRIPTION
--------------------------------------------------------------------------------
4             0x4             Zlib compressed data, best compression
```

解開後出現的是 Apple binary property list ，不過不重要，直接 strings 就可以在裡面找到 flag 了

```
% file 4
4: Apple binary property list

% strings 4 | grep ASIS
={\bf ASIS}\{50m3\_4pps\_u5E\_M37adat4\_dOn7\_I9n0Re\_th3M!!\}
```

