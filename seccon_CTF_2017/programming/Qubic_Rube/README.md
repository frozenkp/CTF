# Qubic Rube

> Challenge Link: [Qubic_Rube](https://score-quals.seccon.jp/question/1a33d91bd704cbbc91e11b42bb27dba7812399ec)
>
> Category: programming

Please continue to solve Rubic's Cube and read QR code.

http://qubicrube.pwn.seccon.jp:33654

## Solusion

This challenge is really a "**programming challenge**". Orz

This site give you a Rubik's Cube like the photo below, you should **solve** it and **scan** the QRcode. Then, you will get a link to the next Rubik's Cube......

![](https://i.imgur.com/MFFWlPd.png)

**Be careful: The URLs are not always the same color**

1. download all six images and split each one to nine parts.
2. categorized depend on the background color.
3. there are four possible pieces at same place because of rotation.
4. try every possible QRcode brutally to find the right one.

```
******************11ed5b705e72e9fa2e57******************
11 : (255, 213, 0)
SECCON 2017 Online CTF                                   
11 : (196, 30, 58)
Qubic Rube                                               
11 : (255, 88, 0)
Next URL is:                                             
11 : (255, 255, 255)
Have fun!                                                
11 : (0, 81, 186)
No. 11 / 50                                              
11 : (0, 158, 96)
http://qubicrube.pwn.seccon.jp:33654/12de86366ccad8ad3f0e
find at color (0, 158, 96)
******************12de86366ccad8ad3f0e******************
12 : (255, 213, 0)
No. 12 / 50                                              
12 : (196, 30, 58)
Next URL is:                                             
12 : (255, 88, 0)
Qubic Rube                                               
12 : (255, 255, 255)
http://qubicrube.pwn.seccon.jp:33654/131c139206e8120f4e89
find at color (255, 255, 255)
******************131c139206e8120f4e89******************
13 : (255, 213, 0)
Next URL is:
```

## Dependency

- [PIL](http://www.pythonware.com/products/pil/)
- [zbarlight](https://github.com/Polyconseil/zbarlight)