# Flying_High

> Challenge Link: [Flying_High](http://hitb.xctf.org.cn/contest_challenge/)
>
> Category: MISC

We found a crashed drone, are you able to recover information what this drone was doing?
[Flying_High.tar.gz](http://hitb.xctf.org.cn/media/task/158195de-cd06-4837-98e5-1129101fb2e4.gz):43ce56686b4f38b68108140825434f76bfed47530a92f3a6469c202746c257f2

## 分析

附件打開後有四個binanry檔

```
image0.bin
image1.bin
image2.bin
image3.bin
```

用binwalk發現裡面有很多檔案

```
DECIMAL HEXADECIMAL DESCRIPTION
0 0x0 UBIFS filesystem superblock node, CRC: 0x3A905A7, flags: 0x0, min I/O unit size: 2048, erase block size: 126976, erase block count: 58, max erase blocks: 58, format version: 4, compression type: none
…
262144 0x40000 UBIFS filesystem master node, CRC: 0x40782ADA, highest inode: 72, commit number: 61
264192 0x40800 UBIFS filesystem master node, CRC: 0x6D072259, highest inode: 72, commit number: 62
266240 0x41000 UBIFS filesystem master node, CRC: 0x13DCBFF9, highest inode: 72, commit number: 63
268288 0x41800 UBIFS filesystem master node, CRC: 0x1EDB0C74, highest inode: 73, commit number: 64
270336 0x42000 UBIFS filesystem master node, CRC: 0x5E9D0073, highest inode: 73, commit number: 65
272384 0x42800 UBIFS filesystem master node, CRC: 0xFF510C2, highest inode: 74, commit number: 66
274432 0x43000 UBIFS filesystem master node, CRC: 0xB70FE71F, highest inode: 74, commit number: 67
1525808 0x174830 XML document, version: "1.0"
1527856 0x175030 XML document, version: "1.0"
1529904 0x175830 XML document, version: "1.0"
1531952 0x176030 XML document, version: "1.0"
1534000 0x176830 XML document, version: "1.0"
1536048 0x177030 XML document, version: "1.0"
1538168 0x177878 XML document, version: "1.0"
1540144 0x178030 XML document, version: "1.0"
1542192 0x178830 XML document, version: "1.0"
1544240 0x179030 XML document, version: "1.0"
1546288 0x179830 XML document, version: "1.0"
1548336 0x17A030 XML document, version: "1.0"
1550384 0x17A830 XML document, version: "1.0"
1552432 0x17B030 XML document, version: "1.0"
1554480 0x17B830 XML document, version: "1.0"
1556528 0x17C030 XML document, version: "1.0"
1558576 0x17C830 XML document, version: "1.0"
1560624 0x17D030 Zip archive data, at least v2.0 to extract, compressed size: 3725, uncompressed size: 23763, name: FVT1_MB\FVT1_MB.xml
1564398 0x17DEEE Zip archive data, at least v2.0 to extract, compressed size: 1414, uncompressed size: 5298, name: FVT1_MB\SETTINGS\SETTINGS_FVT1_MB_TESTER_1.xml
1565936 0x17E4F0 Zip archive data, at least v2.0 to extract, compressed size: 433, uncompressed size: 1440, name: FVT1_MB\TRACE.xml
1566416 0x17E6D0 Zip archive data, at least v2.0 to extract, compressed size: 1340, uncompressed size: 20339, name: HMI_1_TESTER.xml
1567802 0x17EC3A Zip archive data, at least v2.0 to extract, compressed size: 304, uncompressed size: 815, name: MAIN.xml
…
```

## 嘗試

每個binanry都dump出來看看，內含多個xml檔
- 稍微看了下，不太明白內容是啥
- 用strings掃過，沒找到hitb, flag之類的字眼

## 解法

- 用`file`確定檔案型別 -> 發現UBIfs
```
% file image0.bin
image0.bin: UBIfs image, sequence number 1, length 4096, CRC 0x03a905a7
```

- 利用[ubireader](https://github.com/jrspruitt/ubi_reader/)拉出完整的目錄結構
- 在image3.bin中發現一支影片

![flying_high](http://i.imgur.com/q4GsGiX.jpg)