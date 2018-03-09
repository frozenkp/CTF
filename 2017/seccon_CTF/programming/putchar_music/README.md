# putchar music

> Challenge Link: [putchar_music](https://score-quals.seccon.jp/question/f6b2af4e26720b6a27b3efbca313097b977b2a8b)
>
> Category: programming

This one line of C program works on Linux Desktop. What is this movie's title? 
Please answer the flag as SECCON{MOVIES_TITLE}, replace all alphabets with capital letters, and spaces with underscores.

```c
main(t,i,j){unsigned char p[]="###<f_YM\204g_YM\204g_Y_H #<f_YM\204g_YM\204g_Y_H #+-?[WKAMYJ/7 #+-?[WKgH #+-?[WKAMYJ/7hk\206\203tk\\YJAfkkk";for(i=0;t=1;i=(i+1)%(sizeof(p)-1)){double x=pow(1.05946309435931,p[i]/6+13);for(j=1+p[i]%6;t++%(8192/j);)putchar(t>>5|(int)(t*x));}}
```

## Solution

I found a cool video "[Creating music in one line of C code](https://www.youtube.com/watch?v=L9KLnN0GczI)"on Youtube, and it looked similar to this challenge.

[![](https://i.imgur.com/5x3jXmM.png)](https://www.youtube.com/watch?v=L9KLnN0GczI)

Here is the instructions mentioned below the video:

1. Compile source code (main.c)

```sh
gcc main.c -lm
```

2. Play with mplayer

```sh
./a.out | mplayer -demuxer rawaudio -rawaudio rate=8000:channels=1:samplesize=1 -
```

Then you will get a cool music like [this](https://youtu.be/NJn6ZZ_Mnvg) !!

