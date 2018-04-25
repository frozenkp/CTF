# criticalheap

> Challenge link: [criticalheap](https://pwnable.tw/challenge/#8)
>
> Category: pwn

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

![](https://lh3.googleusercontent.com/cRTTnoeKFITCAopJinU_H_dcCwJGHZkoHBqEpY98waDoucfi3o9R9_CdOSts1AWNs_fMWZd9BNL-5O2H3RPnTV-S3SyJ6J4J_e22LvYhZAL49glH0nNIdUnyfK_N99nxYz6MibZp89KQsosYapg5ZCEzjA_mqUBQu62SFvGxboPLZiAPwoA0cSqzAWxXltYchPD1Znaf_7glpktkcGk1EHLXOJyJFgPO1Eh5J3a4931TTDf2TCGwaa9QpE-5P2esGOga9MJfpruqT5xc7AvmYk3yekVamN6btmtVMX7ePgcNSlRU6mymJ92AzSwU6NJO1ssZighMGW6N5esFlsvjOqvyl1ncAbYIgTg6XL411jF1HNsJp4-gIy91JQZ2tbE14xezwCWKNbcPzvz4pBEk2EwXQBgjVIe498xfEf9QXjNK0pvbxprdfU65iyOLeVUoPf0zUftYI73pUtfm7bg6GLm_UTMHjdgNoEw804x0QAmPA5ghvznIUU2u3ll6Wqpkbc7q_rsq1PpCoZxrhlNkmWryd3k7BSl2becKZs0tZUve-_Q1L5plTKrIdmFSE7CULIqGl8VgpYoU108ZnGbR1EF8D-jdJXyXZCidhg=w1276-h268-no)

#### normal

normal 的部分需要輸入 content，它是直接 read 到 rax + 0x18 (struct 上的 0x18) 的位置，沒有在後面補上 `0x00`

![](https://lh3.googleusercontent.com/vI-cgKNMdpdN5WcdkYpr65PsJN285NEBwX7L3ykzVfGoxPO3zRND1c_SVKYe8CVFGbZ00LXQTmQ31ezy85ErEi69khnf5EwGkYKN1y3ou3WIqI5UveKDj-4CX8STRm_TkGT872R6dxTiyqXxQTQKz9tf2rqRPYWUrVta8eddCyZGoN-a2Bia75CuNrb9mG3bBumvxNQma58yAdjAa2Wt56gwJnvChAmetUk_SGC6adZ-IDqNBGapGV28nexQWGxTJPerD7lTuMu0mJxwmMlKRjxfwJCooo8iycJbHl9wW6d6zUlz6-oavLDuyFshF4TaN6ZAzZC3Pm43x_GKnFHz5KzFCLGhGNaPe4Rfr8MJmsU8hhCkOECao85NceP-2GiCUIPh_78mVWBTVj2c1qMJXy2z92GKHd82GAT9ZompjJYU-TrTJl3ezbHGQ-Si7Wru8uj9d2P6sqeBcofPm-_lID38tSCgQ1MUPuhPYD39VaBkmNT1lUE3S0RahSZ8xuDbHWm3Lkxxa5mSO51M26GNfbAzv9optgyD7E6Qsl1Xoh6BwVnXN56P_izxyQxflrlyVT4vilx8zllKQKM_1VqS_Drtfh0ilVqJEviuxg=w1056-h356-no)

#### time

time 會用 localtime 拿取現在的時間以後，處理完存進 struct

![](https://lh3.googleusercontent.com/KtEuqCT0AElcVu1C6K3LzIgaYmPia2SZQELMpuJETNP-oCYGNclwjbADHqeZA_m5nNz_AfVXdzG68A2Rvl-kubJamdHc6T1As0kZ1fvGMr5FFZmOidVMhIgAaqlg3QuUnBOifMj_0WfzxwAaYg64a6HDg6WrbZI_dv5qFSd-OPn6u4PJyUzn5DZau8foycKIVOuL6VAfr2PQ_yX68iXrypR6pCz6Pl8UQtIFe_SW3ewp4A8Ge01L-SkpDQxt8DHkM73oqrlBrH1yBdgGqJ7JDz9LC1smSYPkoweRMKKo8pGZMQ61B3Ba08yt_y7VzguSDBCYfA0j5FS-nShRl3y5SN50RQ9rrcLTfO-4-rG37KVSEn8_NkA5XwYQA7yyHe2wDG2R_NthaYRdFJIC-HgC4mdPY2YwSfCudPlKJYCG0vr4BcA8FpvLQUICVXcbgljZGGhsBf1UoXKzXZnCEmV9Xi0skiI-SHRDlnldjmZKM1enXj9QUvSFN6a2WL2cX-DtKSfYyEvN89JnGBxiBUxRE0Z_eXbswtX_vCJYwKqlrPme8Kw4vluQ44Uvgt8EhKBT4CL3EZy8uSH6CN6WdYotTwdjyZxqnM0zo95gXg=w1002-h136-no)

localtime 先使用 getenv 抓取環境變數 TZ 的值，接著讀出 TZ 所指的檔案，並將內容存在 heap 上

![](https://lh3.googleusercontent.com/PG9GXIWpWmIhcjI7kUlh1__ZxGAbOSs69G1BEJ4r0qVEe5rU9HIcpI_rca1Nmb399KAT7Z0pnHuRosnJkOVGp4Fymxyxar4xIO39Pqy2nvJPRNxRSUoGzgVkEsH708z3cgYOEaSDOPUP-PFrbHuujJTAyoiGd5xiRuHjAL_CfxCm6s8qsnq6NJWFYFJfIpzlOH09nQ45ed2UrHmlBSnZYz-q5RleGrl-vhtPpjB5EkyBl5_z1_8Lv6i_yTaqIN9vr4_ta_WNf8KcVo9r_7A8SOvCIT61Fe5PagF7z1SEWarqVxq_vNTF7y9k690W-LBLoEFN82sZIdiDhaVl7FKPkdzzp8c-z7BnpDKH1yAxo37NJRA6R7CZdGdnIr3zFQkIm0hdH3q3U5iorKHthYV7M1KLIo_mJMacvPbtkMn0ccIHEpM6P6_pMnFbMHfZH-3HM4jeBT7-AnXcLIvALvdeLpQtH4B68rP11vY4XFTD5npLoLY9SRSUixc8eiKWH0jo_S8vczY8TVgwsmn9m_3F32Pww0Kq8mAvrldVIMR1tWGxS9e_gckqnDGkjvs4g7ODwxNqYg5etRIyV6dsoULWZnGoD8pBtWZ9QCXbUw=w1710-h456-no)

![](https://lh3.googleusercontent.com/MtXYZAf6FxdwR6Apkj0Y_6G0LVjE0sNgFQOjL94z52nmFkdFCnoqRlF6J7kpSMf-Jv-2pIdLBOrJ_gmHinpuooe5-wMnQqsH7kVZiJpLTA0Ryz9sVmoMpGl6tksSiASc_5mYtv-Qw0UdXAGmmiAuKz4BUG3WkPf5zHLJdJqFN_-vwVmznL9QDsjBUe-MSnwStGMrXM6vkO6hZKD97emH42_kdc5R5cFurCOpHEzgs4VDPnCX0t-JKNTqAnID56uULAo1j3hXOrn9CofMTGTNUwguhIfr1UHWlaBC6XWhT6ax4J_jwFPgMTaPHVYbQBq2H-qQ8MzMLJ5mlQHRCKr3ki1gdU7fYKrYg9pGNKonBr4EATdOIfTB9z_5CClpxLL89YdgL9AGBrHCbt39SddSjVOpLneye28fKZKd6jdXLDu7MMCJuW8VMMJ5K1utUbCFT1M-AS6MGHacOm4pAHjXRm_U4o3UctXMJ46LnGsV6zdGKg6Jd5Vix9Er7UYJork9W_Ia7Sz5UPRW3fIo56XxAmFA7ZK1ncMJMIaE18in0XyzXujFXbZziNnOzKS0l6hqqudFuZkfDwySK5NGtXk1ccmAhEI1o1_E1ke7ug=w1628-h542-no)

### play_system

#### Set the name for the heap

這個功能其實就是 setenv

![](https://lh3.googleusercontent.com/KdQWIK5RdEtqX28DyvEsoYypn3z_ifzaL-cRpYsc2-c4By71fcYYrAqf0DQgOzmlCIlZ02C_HOUE6wiQMz2finFfWnVZyA31zm8XpwCziXKO4KDsHlrJVLYVFEVS4B_BQKgEbvvpTuBCbCODlhd0FS9pnQ8L1yjjhXsO7CF2ry8XSkhwHkFBhvwTTeQUoLc3opuVHE-2v06fxaqGCHV9dAz3RQXlpPzoFFzXM1F-DOn2CIHQZEwIyCBmQgNkH9m-07S3OGCvMylz0T9MRLC-MMVHdGfhjF5GuQ6X0mzu6kWQOa80SpySplSuYnbcO9qqGw1UTK6s2N6ng1YRxmkUDrvoBfZBTBoA3lUXNgRROom08vP9gt6T_NcMi7zlAcpX5tqPzB-pCj191P26OFGlqzZdlr_ZDx9ujohKDhQCaTGcBOS8QM6WGncja--xVLVBLHgpNKTnZjU9qgHpz1lpl49krTyVXFw34HvjNxr9cuIdChFSP56h87gsPXWqdKz_myMM9Tww3PV8DLmA8N73t6wT04V_euYbi-u3HjtGUT1fcJ1zZ7sGTDEcPB-1ZYAdYwvhx1gLjkj52Prva_wE26HQe0W60tuIlQD0Ng=w962-h262-no)

#### Unset the name in the heap

這個功能是 unsetenv

![](https://lh3.googleusercontent.com/Dm4mNcmPdsgdvI-AuaPvN63bSeVbq7pZQrUaEqig6yobMlW_HNLlb5lS6MoMO58DT4oPN2T3oqfFMQ8FBbgFeQCVjRtsFs7gRsX6EcB8iarHTYw4O2VqnguY3OdaT3WZNULaTPXq6UZyI1JfnUSfkNp7Q3McEiMVKNbDjaXjdBTeeGbdt3CseLUlXmax3c50WvfS3f7AuYYkTvyzlvW5w3CzFdoskXudaZGxACaE77tDITwkIq4-hQuZNpvlRbwx8uVv_sLh3SGJ1ZHiGkrbFhMz_rYlwX8GUiC-wgz7vmYDDvJxnL3C0DXbmus8Q4vbOY-plDSF4Nh4d0PGsuGXe4twTT1hFucyhE63rJCNVmSQr_DmkZK4q_30Q9618fIX0czxtG3ksfWDzCKDkkag-hA4JYXy6lFkG7_jHiPf7LnBv6zLay7PuYnXuqFhz_A8lCPes848qsZrnoe8cbYCZ1W13h7pQW4Fi9TkWUwxywO6gxB0DSIIu_-D020bLdAw3M56lyITaasYAsxIIceOA-rro02LBfUd-XhyDqN6BmH-xucZnog_DTxL0X3I5N4m54brQBfO5tM32SVoEY8u7QUCKcp8FkFUN_P89w=w1028-h188-no)

#### Get the value of name

這個功能比較特別，會先用 getenv 抓輸入的 name，接著將抓到的指標 (指向 heap 上存 value 處) 存在 rax + 0x20 (struct 上 0x20 的位置)

![](https://lh3.googleusercontent.com/WRD3giNGiEyj9BDFXZ2w7NsNJqQqLtRaw5khzYNEQGZcXxVfLypNxe6U_6F1cD8gGYO3R8_7w2vLmRdHNdMs0VWfZvu1_65ayZw6FREidtSnYmX5Hq2HlShyFkTg84uLYO7sLEEoBlwqjX3hTz2AT22wqNMY-Jg-oxeICWGP8d-2T4ek1L3N7aYk_VPKboBYQmCfxT8fJCWly2ujeY3_bxM5mJ4LMJfFQm2fOHqxB7lpWZsz3HKPG-fn_OtA4WaJL6CWZfGlvo-b2BpYHB9f8vTA7bZxp-a3jjXYXPzJQWDDx8kLmGKT34Px_7s4xPykDZBN75uu2usyeidLmIeT0uAd50AsC2E9lxc317ws3g1pyNLVmexYbHDQt8DWsuSACHjOGj-gJsmeCqp_6tKTKLXykQvN2acb6iicHAKC0HKeXoBww0eKoAlJi8uwYlawXfMdG0z7rIBYIMfqDKwxTU7u-zjgoHodgba0W-Yv8ifa2GtMwUTlCWA1LQSyCPsghcrpycWWIhYmArHZAPU5AXk5H3fAf5U_YYiRFsYaliioCRnAny_MvyeJpaFj9YOFbselWvAsF4cHnmnEzt721P-s27e4VQ03Aha7pw=w1166-h406-no)

### play_normal

#### Show the content of heap

這個功能有 format string 的漏洞，而且是使用 printf_chk

![](https://lh3.googleusercontent.com/9Lg0-CLj24zPq904FsB79Vi5pHxvdGtT9QzHb3ZQ-qwhiWzLFdf_kFtbg2O-WqU77eB_ugP1emPcM2RbovybUxE3yg3OfUTV1U3RJ201A0nexa1u_-QDmKcAwxH7dQpOEsIwdOyLnTJ9YlcHSjQZ1iVYZ58NjurxC4qD6-6JpejOIBto-RRvb8k6-G4xh-3ez4LgJJLqwauB1ap3z9oxG-4wpVR26iS8aGFY9EcVOhYuq9WIJZTINGfKYM4q76LuAjkw8ay3K2eUc8YuDMkLd8JV-_4wAVy4jA-QIyGxp9QwE5-_5ZBGMyXViRRPqXyn3qm3wjg_Qcyeg9PAjRxsQ2EqD_4Aj_F8IPxYlzHkvUYc_tJXc1fe6IwPJfEjyB_Pj2xAk1wHyTt62NZ299Af6hT2AM6opnS2J2GkzN8bvK5bYxlYmUcU2033AEfC-JDVSFGOLxV5zCDgHOjXiL2ZXRYc0JdK1FhK23eLetJyE3ZJzZw5OrLKwGFXKxagdB0crorlmOcBmdXhg887R8YaEkt5aqtsEeXsoEUU7dJ5IzNRgqda1XchI_tELTtO_28WXCTf-ELOWbyeoEC434GLBE1GfDSz0H_kKt2_WQ=w1318-h494-no)

### delete

delete 實際上只有把指定的 struct 標成 0 而已，上面的資訊並沒有清空

![](https://lh3.googleusercontent.com/cbKj_uIbSZW6YlwijBufYIXETYjHkARepJ6h8UQF--4TKjBeedl5mfp4nikGla9W68FscAtcJnUtAz-80gmR5YF6GyztDy2G4QiOc4hh9-YnB_-MdF8V9Ltwmq4i4ZHqYv6HgF8sOWPpbTGf5gTHFCkOd8gPogKZk3Awfn2TG8nRlmxrSoj8YiWKwDfJauNaD0yused_OL-V1LkGOYlTZhDgmgC5SZAlyOaJZqFLwvBHbsecDYK4OFnZGWm7G4S2BXNjsWM94KG8M2frpTg-BXtHUFXKUWxRf5diwSWj5PYRn-rGEWQ1zopU8Zr0UgPZf9AZhH6H3KzngcEx59YxwCpg94qxtE82UqbA5ZoFwck5c0UZ_GvZz4XZ2my7jB76QKUZev7AY_m8tYy-GBbBfJZunNrlNpa1-zCA1plTEhn3n3uirf8hRUGvh-hHiIMJKu9sX2azJ9Z1pv1xXmwR_c5gwihodaS7Ew70jhvG6tzr45-TcI57eGyJ0oyYjeBcGqLW6dWZ8noL8Sn092--7rm9YT8BWYMYsqaM6REElllGF2S62G3DPdNS-Yn6CC-ChjrF5_5l9Oqd1c29p1aLaNttVnwOObxg0vz7Bg=w1090-h448-no)

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

![](https://lh3.googleusercontent.com/Kyn4pR56pdq8SDxyx-nCH3SUIQ3X5nPs2w7J3A83lBs79-FGJMFZAroE_qzvLddXrWOoUGA7q-UgVlZI2cCkY5DKAI9A2U4Z8ZyKWLta2Z8c9Lu7C6PpsuM85LciaiA8FAiEHiexjJ5IWVadfH1ro5TjEuoFigzkNL1eFFsMteUkGaXP0keIlqnkbMmlMOdUg8Vdu2tzaDltKoG55MudTTZinVzGE1WjLPq4NwZ8bKCsCNWGGuAz07CQqB0GVT-AJxQ_h2Ny5dzmfPia_c93eDDIJrszgkyaxXzyn_Vp-ydacc0jc4ku4-tpmc5gdLbJNwxxMScSudTCAwmG6JUz_StQRAdRRPJkrTo1dIerzfOCXvOh7k2QqAWvfEeYsIzbEzCFraYCDtaFgNHjQdQdWjAQDXrsb65a6Bc8ZDatDeRYkECL7brbOuFxvy4DjjC8PbiFkP05W5M9vkiwChR25NXX1dXaR5fG9HRxhnUIsSqZPBUTAAZ-r_IYq_NSVGraJvZALsWXruKL5a6LXNdvnFnT8X1FuIcBbS2wwLZVrnWJZ3QyyOreF5aMxGz5O6ZMlu7GcajaRrBlHALdWJv6M3BelUqhBRZRlD240w=w1990-h750-no)

### format string

利用 format string 搭配 %s 可以 leak 任意位址的特性來 leak flag address

另外，因為是使用 printf_chk 的關係，不能使用 `$` 要自己用 %c 來跳到指定區域

![](https://lh3.googleusercontent.com/OgYVPHk-ayIh0_tNudYfMMNJHLux-M_oW3gicAzh2YOpFhJugoYx6oAix7OqDqoGo5Q3s-ZJeoiVs7BzRNCa-ZgrDzGAvpjc5moz-ecE-6aFBM9aCooCcMmTPyZJHzmM2RGA9IP9N30n55TryLkhT895zQEP1v2DO8e-5LJJpg9K5LqJVtVHCvZ3UpivGOL2x_SnnqDbDEXsjlhUBxeFPjNHVm336THU28k4As_m4Wn6rttwlPUxA9vCywCVimZv5AP1841Ki_p9uAu5sBkWeNLYusBkJypTnvHbQLK-Z6vL64c5_HvXgR1sIYffo-BB2RqKLP51oDw4EvSiMVOslbhSC7LXEFZTZyaxGkaFwkSACYRn6A91EBR0Wy409eDyqiJ16X5hDivntwkKYY0k7qS46YrKgtUZGDczA9ihpM-rg6ps9NT4irKhULFjn3G14XNkWNlL9w3ErYLqyaqCDb7ARWJ6uAdukSGBRcym70YUA0eeMp9_5t8z8nl9XDOYCKDZn_2_OUmlGyfvvvJzINq1-3T8qlaPCzzVd_mZikSUF-XorwN7EW5g98pBmU4aXtCQQwl5IXLgSa1vvt-XPeGfkXs_DcfHsIQifQ=w1488-h932-no)

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

