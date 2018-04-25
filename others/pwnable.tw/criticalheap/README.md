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

![](https://lh3.googleusercontent.com/HRioEtgDubcktNh_fYUY7wU3B97Fhl0N1s_WlziejzYyus1q4n7EOJBMOBYxLH0V0GCDLMOT0Pl9AmmwCNQrr1A6H8xP5g2yT8G3ydgiDkL4OEbt8V-RKgXAhObyCN4wH1400x7kEevBWC7-jb_MVFsXpOY6JNb9dZ9a8Hy7rvnBGx-Y81hJ3Xit91ZcBn6vycAdHBqoS8oXfvRLdyfMdsr7zDaua8HLcBeXV-rUZZxTRLtaAGmQmLN5bME5crfzlYW8qqtdULA-OY9XY_A7eQ09ERImmK2UAw5_guRQNw5NBjakI9QAPkRAiw4SeG0UULshVV9RJ_QFSPd9543hbXYU34Ce58SzhLzAGl-cyG7HRWO4_idvRYGNd-Sp_kV2WM7Q8DkxTusVHPKoEIlUFOn_HR9uN4DYwJSLj3n9CZc_Ih-eKD7g_CXMUVORWrgz6MW5fIVkc76Yhojc0i3reMe4CYu16BEnd7yHsSMsU6LL63s_Tnfrh7gncvVxJ_U8OBMAot5BwAhpaH6ep4HaY9CsrPbO2K9wqNUwhMPWMZkbER1cHYtpTel_J-lu4vTIXNls2CdtvxvWhu6X1l6zOau5ChFA8EP_X278Gw=w1276-h268-no)

#### normal

normal 的部分需要輸入 content，它是直接 read 到 rax + 0x18 (struct 上的 0x18) 的位置，沒有在後面補上 `0x00`

![](https://lh3.googleusercontent.com/o2Wd0w27_WmLaBxm1b7C3f3Ljc8KXm3jgITPIzC85-_egjLALASqWzOTh1MoVSUP3FW7x_kQqWKRV9biNzIg7T_w5a2iexeNO1_Rwt401QVz4VXXsYlWuPb31E7hjRD5XuXzfn8tZT4518TtzD76DpnfgaqgZfi660kVxxjGfaQ0rd5UASBrnIYRtovxf1Sc76dhwSx6GJuxCAkFOkuysmSj8zTXYY3dxPQKRCfgty0lUVbrAxvWUtx7wFp3gJUkWZ1hZ6cyu1Xw9PCajFJDclhuDvPQxmkMXopfe59W_9FnkRqK8yRjfCLyIjN1S0u0M_PHW0tiUv05qJ6IcRrZZsgdm7RbcCdUOlR9Oh2V2Sm2vHu_dLW71z9YRsdU85NuLJ2enXpnbO0yAonhOdw0C7XDVVBVGwdMpiHswh33h45T6W6F-pGiJPd0YXhwvm_RNGzP2qIzalSJgt4Xx0a_ik2dEiqVsl9w3s26wfJZNL1zFUuQiTbj_cM3AuLYQMVLGqTJUQFwibw_JAmJwZb1AiQe7Gl3g-NqwoGEqZAGaJxeVcc8KJM5l_p2IU3j7IGuvhiPfiYPcgzhCPIzMXt45crDOAfudA0YGkeKzg=w1056-h356-no)

#### time

time 會用 localtime 拿取現在的時間以後，處理完存進 struct

![](https://lh3.googleusercontent.com/SAHGnzTC95qnCrmZ-Yft6oQL5Pqd3miPspjdSvJrUFFkroKJxPe5KgqcbJz7nvo4JErhf8vSbUWDUwAHE4u2By6x5jOCiRMqFtLneAD5LJjs2GMxrS5oEyK3EnIClQwx44vij4AsC1qF4YhNVN1UxvDAgiW6CeRz7ZoHD5zlMsYtbURDiQQKF9l6zZ13mOjj3AWitXljCQAI4fBtAIRKjAxCvYxqgWAfjHXBJaMrnSHcq4HHpV789w27GIFNzgXic__--yo6ZN6Zr_xoivtfiMGv7IKQrf-2yBm1q11U8kpkAp7Js6ffchq5G9QvbrKORDY_VhqkCQFiOv8GIELiocCuyRYzvkD7lkmz6Uh7o0FOAlEFMFgcEh2AqpgzImTLeuKX1aK3TsirPf-xuczKyn3-zUkik1Ag5Uaf7kOg93aFlE0SpFFR9eIkiFfjgihSa6DRi9JekqhFjVvOcRKz-FRyr7ANd8nA8rhtw_zEqYkREQJsSmCC7en6fKj1jGJmlamVURslTkVN4K2QA4dBhdLODGLBGWODul819OAaTk1t8thWpGAhZiJew9Gz78NNwH92iDT4nUBYzJCXVmU5Ii11OasbbpqRLKzW_w=w1002-h136-no)

localtime 先使用 getenv 抓取環境變數 TZ 的值，接著讀出 TZ 所指的檔案，並將內容存在 heap 上

![](https://lh3.googleusercontent.com/S-nRWfygmHDW2tbPlXqgsxMg5Meu7dCKK8JufB6iuuAGSrNfFBMpit1CeHasz8FpvBzkZx1ZU0T9dpS25ZXojRhIi5a6AV64Noi-OBAllXM_tIWQKsy1PBhFXHqkViBxx0YUpi1Y2hsiy9G9WygQ5veCY10PUik-tXV2HxFruyDtMPvt_-7zjqbkeYWtA_OUvWcjfMTw7dGpkqdVVBr2uA7GHZMMAYg1-_iJhydOdJwRoq8lGkCgPtKr3a4n07YWq_8pDTCnrqaf_dLGWeh_yGqqMiycjtIIitGST0IQKiXKwsUaN5sh-Rg4mb3Htg-Xa6sbvf_bbA7yDWJQUQa6lOjjdvhy5q9TACYAyogovCNsKeBUd2w2OAIBSjJLOQH9qzHVrRoAAgvl4S2dLslZrdYNGPLGMVY1JufdWrO5A6U0WaNHNEhLuSYjdtAJyVWqrYikZIL-v6iWSN7ipC3GteNZDrqoOV-AzRonWR5e6lfEucvFmeNh0pjtvJhRb_VGeZEYq4e-AWOy5PnehUE9DNc0f-EFmSrA2QbicFSyD2CkIDfSWXd-xssBASTmQIY7_5znfDWBp7Lxf72jyMqS-yp8a6I5IpfrfDUdNw=w1710-h456-no)

![](https://lh3.googleusercontent.com/Gj8sVF3MzU6zNKtLC5T6Ue6nC2QdS8mc2MSzHOEUbzOMzVfZ3JClHbqp4fM1Gcb-f9-qD1-zf95K8LwVIj29fYUEbNcIeCQ1i2MjBjMPE6aBwao2pz5MmCB0gaOoF7m9uu4uB65JESAatFIMedlzLTynGsR2s6sixmStuTDwkniCaHKaJd_TF-NJTBSr3GLFRipTDbzmRh0-bZrB2Iuh3QxjC0fv-jq3Mn7Ni3iWHS3F3gNkFcfBNrNJgYHxpTQEOlkeGqI3YSxNk2GMtFVFrekkZp9n8t16_XCr0ms5JRU8AOS2EkMBIX9DfoXB8F-qUbQ7u-xbzuZIvqc0ojSGUrBfVdPYrxFm68CUMuKuJk9AgZnhU-nEJDUGfYP-4cmEl7jDj1C8VBX3lyEpRCzrt9x8IuluKtfv_B4Aef15F27pimpEV2SeM6CQo5uSXF17OY0p_HG6zkgzRFE0GXWDHkEwrRVs1PgiABNI13HpbUgogCbpHOwzJQ3CEcp8yXAAbotKuYbwD752S0FVHA3IyyrQlFZgvzvurGNPW790AK9zvZFVw2Lzdrvzt7Ue4hkxKcDDdK139Jz9fCIws7Kl-3IoBdeAKMBNj39R_Q=w1628-h542-no)

### play_system

#### Set the name for the heap

這個功能其實就是 setenv

![](https://lh3.googleusercontent.com/VUPdLvI-vjhEM5rawdI7-ViPa4z6IEwoBIulyyUv7hnNqwoNWpMcaxUYF07synIZObheb0tnUweo8aXPISRmSikbEe0YHz7zA-uzWdpJbmYVbPXL61Ex63TAYaISlgf_s9wSpwyeRNYVu91aifVho22tjONzzBQqirtPy708HS-itTZdkJjclcxPNqekgvrR_MiqNzaQfPV1_5XmVRbtc6oMqKEs5ByjIVQwLvTYfs5idV61A92TjjLZwURxqCmZ-N48Uh94wOWzzvxajtSJHX2I-p5GjVb_lSYWXGPpFhHCVvlQfsqOx0XicO5yzJH2Kn-Q8vddZIbYNDLDAuWuO7-e5Vom8zSTdo7WWHMlyYswGkvWr4AZ57ltY6dF8Xa2vmqqKsmm2CF2Ey-yEywmt8BgEN3017SVFlX9dg_02xUVGQqOrRkbolIHs-cxUVqhPo8XmsvT2IUsj9UNoK07HQFs8Uvv74wdATHonLtbz4gpIdewwygipAiS8uw2eccjUm22KMBbsJkCmFjCwpo0i0IasbLeq6n2wed8v1YTSIJc-A1rBA60fKnkhbBqMwEK9_PPuLSn5qExpX0wkdDomPjIjiII8jlKo2AAaA=w962-h262-no)

#### Unset the name in the heap

這個功能是 unsetenv

![](https://lh3.googleusercontent.com/iJiuBcOLwCoTHspxZnATe7k4dNRcuECr7NhGETeDmgak82PofrIkHVkg5gF5gJ0I_BUaVWglwn6A0yXJ0bqh0_zdavLgplsZRXrRDZ0sVFV4L69Ghgvm-YYQocJdzI1N8amMMQCKh_hYN_8QTqFQcldw02COdw5_s3y-UqQ4IMbEalBCOyy6XqTDlTlPiCNLwAuvH1htZ7jXZd6lJ7ai1gEg_JyI8CaS8HV0EZ7Vp8HNjXstcenSIOF9N0mjZ8oI6JxKyeV_pv3DI2KUK5JkzZOUcUopNWJNl_-uybpKVKXiVPYilcQ0-lz3eDmXu-inV9JR1tM8ZtzzCh-EjOM604k_rUfTxOnrMzN60Bu3ypRWEoYhJcalsURcaBwiI6SoRFhSbAhfxNZ2PVWHQcPvGad1BvG-p8Y5xtz441JUZarS6IdsDPHsCtE1yClXZdYUC0J3WaPG9gC1H8e2l-cM7xGXZCFatyUTycCLSsImrc1lRNk9t4GrLb9a-PTodszvCc5qERhYceQvPGQhdQWUUupo7b6Y9FjK6Mo3LNh9Cc5lmKR58QT2JIUXpSpIrnmN8j4O6prMkwJPSxOx3NJwx3DOvLFGMBnMWIsxUQ=w1028-h188-no)

#### Get the value of name

這個功能比較特別，會先用 getenv 抓輸入的 name，接著將抓到的指標 (指向 heap 上存 value 處) 存在 rax + 0x20 (struct 上 0x20 的位置)

![](https://lh3.googleusercontent.com/KUYOQYgh4ia7j83GdAI9f3wPbR8dU2U_hyUIpqUlVqTDhbKtVRmxqInCORFFUbaLenS7rVruzWs9zG6ZeUh99ybm_jkSTxThh_sX_wG6ZWyLOn4SQUD0lIRmuQsLfwJdVr7GRyHjJfE2ONbuKD6c7MDBTegtHffmr6LqhWvmZBoRvEuYTCxQNPpJejCaX9G4zjStWmY3ch20M9HdL2V30Hho-n1UhURIlLfC024iqzfQHl1hSz_PBdsW17qJUivOlYyp7p2yZ0YHR0UfgUaLlLb51P08od8_YBNulrUwP7-v_AddRslRmsOPMkLVCgrJXwwb2_T35AcjxxdaR-F3sH1pk-n07oUT5vbCubjDaMxeCnM-NDF11t3nG4dHsTsaOGKmozoL3BIws7Rgl50tN4OSHrLkVr-mqCHTf_Yh35BgHWs6_NZ2LzKABq0gaWLkL7cpJCozw8NyTNqeO_a7CnzjYbAv6rqzsDx8cYSRqVeFY4PLncmPEwu2crmKBbk6dRnjq874AOCdpUIiM3c5E16JS5Tdhucnr4HDp7irYTOIyQX2oN16mb-xgvhDmnGXBnyDGcRn41AX_gHSNzX9qD1apUCPQ9iPOdnDGw=w1166-h406-no)

### play_normal

#### Show the content of heap

這個功能有 format string 的漏洞，而且是使用 printf_chk

![](https://lh3.googleusercontent.com/uIYwP7wKT-MN6iy601b5uR_TKxJVEQjne8OjbF_Z8Fwpcd2EIHpf1_3hGCI4cLIx--OBxAsoLK3jh8gxpMcVZh0pmHfZyZGgfX1lootUx3W39bXIwEWJrDvLHoBSKudon7QxQkjclFtkpWXBS5B_nhAE3BMmRZuaBJG2kieWB-ePU7sIk44NUrXvKaQ3VQIwYT0fA76xXEbzie2RhEWMJdRZg5OXlRIZw0ZphLMMsbdlMpPEwNFx6wgxe4hSf9SV_iXbIAkd0QQliA6rZrpNtoEjMBIq2y2LiBAGOrJlmw3MzXgi7d_TbxBALV9Uqaxr163Aheo8eyTUF02kQ48TvCXZHSuslBtVzXAGn4BHTYRAa-XXT2bexSdn8T7SgME9UFELJLimU3Q2OpHoXhSuPjeEXmwnuvQajTBC9u0Qh-x_dNV5cZS3u59DcYhQAKFvaww0Pe9KHzzlbGXDbmPuh8slyg8J7aabAh6yn_2G6iT2lNfIYLruQsdDOGnTt5Hc_wS1bYWHUDX7m48tD_lx5Vi4CRZEDqK72FLYsyMeyeTJLlZicX9eNqboc4jl6tvTr_cpZbsSvhgg6pEJfUQj0Vf9woaVgsn4Ero4kA=w1318-h494-no)

### delete

delete 實際上只有把指定的 struct 標成 0 而已，上面的資訊並沒有清空

![](https://lh3.googleusercontent.com/WjHYiGRcaEku15F4WnbC-8V2mVZBsTWl6o-WHJDteTh5gZjjtoKIZtfTkei_GXMfthhcPoICihB7IT84R8z98PZMzlaZ0fPhe_7HQFmddIOHKSZUt6W1S4TRBV22n8crP82RS1NpycWu3B0O3tVc8g7jz8sAusQUgN_faPtkdRIlTUuWs0hi4lOfFP37s91pM2q_0BmD5WPLkzgCrox6wubwZAZJ873B5xbMQZpn1i8N5A9cvuK3cmZC9AKx6YVxjMzx03B0_rivHOCMfu_sz0BraVx2hhfgKlzKnrywlrLEdZ9B7lh7VsonTeDGEM0MVagnyHx5eeY6G_4YtRbhARY63zo8N7d_xmMEATbQ_gy8PH63CdvCyhEcpg16OOUMAavZzlq6mi2cti9ydEwAN-qm3fRV5_tB-I0XiPu66aArDRtU5zeiqjmPkYU9iOgP9vgaPcEnqJhI4aGuhvWauDHWPyoy6Tgwlr-TCbTy8z-2rlOQpC7TmWs6PWOATSGwjDsVliWBnTCvb36GCHdCWRa-tBkngtsdS92NnHM4rkNGR2UPk0dcmkIrlsbozPyhZCqZbNuwLL7zAjzod9a7hmR2sRSkigthQFFziw=w1090-h448-no)

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

